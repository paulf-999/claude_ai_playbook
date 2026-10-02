# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that Python test files follow portable_paths.md — no machine-specific paths.

Catches the bug classes found on 2026-09-17/18: calling ``.expanduser()`` outside
``_shared_paths.py``, hardcoding another machine's home directory as a constant, and
parsers that match only one ``@~/<config-dir>/`` import prefix. Each pattern is proven
on real and harmless lines, so a loosened regex fails here.
``test_portable_paths_hooks.py`` covers the hook scripts.
"""
from __future__ import annotations

import re

import pytest
from _shared_paths import CLAUDE_DIR

TESTS_DIR = CLAUDE_DIR / "_tests"
SHARED_PATHS = TESTS_DIR / "_shared_paths.py"
EXPANDUSER_CALL_PATTERN = re.compile(r"\.expanduser\(\s*\)")
HARDCODED_HOME_CONSTANT = re.compile(r'^[A-Z_]+\s*=\s*["\'](/home/|/Users/)[^"\']+["\']')
# Only real comparisons, not fixture strings that contain the same text
HARDCODED_IMPORT_PREFIX = re.compile(r'\.startswith\(\s*["\']@~/(\.claude|claude)/["\']\s*\)')
# The one file that resolves ~, and this file, whose text names the call
EXPANDUSER_EXEMPT = {"_shared_paths.py", "test_portable_paths_python.py"}


def python_lines() -> list[tuple[str, int, str]]:
    """List every line of every Python file under _tests/.

    :return: ``(path relative to the config dir, line number, stripped line)``.
    :rtype: list[tuple[str, int, str]]
    """
    return [
        (str(path.relative_to(CLAUDE_DIR)), number, line.strip())
        for path in sorted(TESTS_DIR.rglob("*.py"))
        for number, line in enumerate(path.read_text().splitlines(), start=1)
    ]


def test_python_files_exist_to_scan():
    """There are Python files to scan, so the checks below can't pass on nothing."""
    assert TESTS_DIR.is_relative_to(CLAUDE_DIR), f"{TESTS_DIR} should sit under {CLAUDE_DIR}"
    assert python_lines(), f"no Python files found under {TESTS_DIR}"


def test_no_expanduser_outside_shared_paths():
    """Only _shared_paths.py calls .expanduser() — everything else uses CLAUDE_DIR."""
    bad = [
        f"{path}:{n}: {line}" for path, n, line in python_lines()
        if path.split("/")[-1] not in EXPANDUSER_EXEMPT
        and not line.startswith("#")
        and EXPANDUSER_CALL_PATTERN.search(line)
    ]
    assert not bad, "Files resolve ~ against the real $HOME instead of CLAUDE_DIR:\n" + "\n".join(bad)


def test_no_hardcoded_home_constants():
    """No test file hardcodes a machine's home directory as a path constant."""
    bad = [f"{path}:{n}: {line}" for path, n, line in python_lines() if HARDCODED_HOME_CONSTANT.match(line)]
    assert not bad, "Test files hardcode a home directory instead of using CLAUDE_DIR:\n" + "\n".join(bad)


def test_no_hardcoded_import_prefix():
    """No parser matches only one @~/<config-dir>/ import prefix."""
    bad = [f"{path}:{n}: {line}" for path, n, line in python_lines() if HARDCODED_IMPORT_PREFIX.search(line)]
    assert not bad, "Parsers hardcode one config-dir prefix — match any '@~/<name>/':\n" + "\n".join(bad)


def test_shared_paths_is_the_one_resolver():
    """_shared_paths.py reads CLAUDE_CONFIG_DIR and falls back to the real home, never a username."""
    text = SHARED_PATHS.read_text()
    assert "CLAUDE_CONFIG_DIR" in text, "_shared_paths.py must read CLAUDE_CONFIG_DIR"
    assert "Path.home()" in text, "_shared_paths.py should fall back to Path.home(), not a hardcoded home"


def test_expanduser_pattern_matches_call_shapes():
    """The .expanduser() pattern matches real calls whatever comes before them."""
    assert EXPANDUSER_CALL_PATTERN.search("Path(x).expanduser()"), "Path(...).expanduser() should match"
    assert EXPANDUSER_CALL_PATTERN.search("paths.append(Path(ref).expanduser())"), "a nested call should match"


def test_expanduser_pattern_ignores_prose():
    """Mentioning expanduser without call syntax isn't flagged."""
    assert not EXPANDUSER_CALL_PATTERN.search("expanduser is a method that resolves ~"), "prose must not match"


@pytest.mark.parametrize(
    "line,should_match",
    [
        ('HOOK_SCRIPT = "/home/paul/.claude/hooks/x.sh"', True),
        ('HOOK_SCRIPT = "/Users/someone/.claude/hooks/x.sh"', True),
        ('CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", ""))', False),
        ('result = "/home/paul/example.md"', False),
    ],
)
def test_home_constant_pattern_boundary(line: str, should_match: bool):
    """The home-constant pattern fires only on uppercase module-level assignments."""
    assert bool(HARDCODED_HOME_CONSTANT.match(line)) == should_match, f"expected match={should_match} for {line!r}"


@pytest.mark.parametrize("prefix", ["@~/.claude/", "@~/claude/"])
def test_import_prefix_pattern_catches_both_conventions(prefix: str):
    """A hardcoded comparison is caught whichever convention is baked in."""
    line = f'if not stripped.startswith("{prefix}"):'
    assert HARDCODED_IMPORT_PREFIX.search(line), f"should flag a hardcoded '{prefix}' comparison"


def test_import_prefix_pattern_allows_generic_parser():
    """Matching the generic '@~/' prefix is the portable form and isn't flagged."""
    assert not HARDCODED_IMPORT_PREFIX.search('if not stripped.startswith("@~/"):'), "a generic prefix must not match"


def test_import_prefix_pattern_ignores_fixture_text():
    """An import line inside fixture text isn't a comparison, so it isn't flagged."""
    line = '(tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\\n")'
    assert not HARDCODED_IMPORT_PREFIX.search(line), "fixture strings must not be flagged"


def test_expanduser_exemptions_exist():
    """Every file exempt from the .expanduser() check still exists, so no stale exemption hides a file."""
    found = {path.name for path in TESTS_DIR.rglob("*.py")}
    stale = sorted(EXPANDUSER_EXEMPT - found)
    assert not stale, f"EXPANDUSER_EXEMPT names files that no longer exist: {stale}"
