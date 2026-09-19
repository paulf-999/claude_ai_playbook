# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 3/10
# Python style compliant: Yes
# Date created:      2026-09-18
# Version:           1.0.0
# Date updated:      2026-09-18
# ─────────────────────────────────────────────────────────

"""Tests for portable_paths.md — no hardcoded local-filesystem assumptions.

Catches the exact bug classes found in the 2026-09-17/18 sessions:
- Shell hooks hardcoding `~/.claude/...` or `~/claude/...` instead of resolving
  relative to the script's own location.
- Python files calling `.expanduser()` outside `_shared_paths.py` (the one file
  whose job is real `~` resolution) instead of using `CLAUDE_DIR`.
- Python module-level path constants hardcoding another machine's home
  directory (e.g. `/home/paul/...`, `/Users/someone/...`).
- Python import-line parsers hardcoding the `@~/.claude/` or `@~/claude/`
  prefix string, instead of detecting any `@~/<name>/` prefix generically —
  found in this rule's own sibling test, `test_always_on_reachability.py`,
  minutes after this file was first written.

Deliberately narrow in scope: hooks/*.sh and _tests/**/*.py, matching where
the evidence came from. Test fixture strings (example payloads, illustrative
text) are not flagged — only module-level constants and real path resolution.
"""
import re

import pytest

from _shared_paths import CLAUDE_DIR, HOOKS_DIR

TESTS_DIR = CLAUDE_DIR / "_tests"

# Only real file-operation commands, not prose describing a convention (e.g. hook
# output text like "follows ~/.claude/ conventions" is UX copy, not a path the
# script resolves) — narrow to source/cat and file-test operators.
HARDCODED_SOURCE_PATTERN = re.compile(r"\b(source|cat|\[\[\s*-[fe])\s+.*(~/\.claude/|~/claude/)")
# Matches the call syntax itself, regardless of what precedes it (a bare name,
# a Path(...) constructor, a subscript) — file-level EXPANDUSER_EXEMPT below
# handles the one false-positive case (this file's own docstring/prose).
EXPANDUSER_CALL_PATTERN = re.compile(r"\.expanduser\(\s*\)")
HARDCODED_HOME_CONSTANT = re.compile(r'^[A-Z_]+\s*=\s*["\'](/home/|/Users/)[^"\']+["\']')
# Only real comparisons (.startswith/==), not fixture-data string literals that
# happen to contain the same text as an example payload.
HARDCODED_IMPORT_PREFIX = re.compile(r'\.startswith\(\s*["\']@~/(\.claude|claude)/["\']\s*\)')

# Files whose job is to talk *about* this rule, or to perform the one legitimate
# ~-expansion (turning CLAUDE_CONFIG_DIR's default into a real path) — excluded
# from the scans below so their own strings/calls aren't self-flagged.
EXPANDUSER_EXEMPT = {"_shared_paths.py", "test_portable_paths.py"}


def test_no_hardcoded_home_in_hooks():
    """Hook scripts must not source/read via ~/.claude/ or ~/claude/ — resolve relative to the script."""
    violations = []
    for hook in HOOKS_DIR.glob("*.sh"):
        for lineno, line in enumerate(hook.read_text().splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if HARDCODED_SOURCE_PATTERN.search(line):
                violations.append(f"{hook.name}:{lineno}: {stripped}")

    assert not violations, (
        "Hooks hardcode a literal ~/.claude/ or ~/claude/ path for a real file "
        "operation instead of resolving relative to the script's own location "
        "(see portable_paths.md):\n" + "\n".join(violations)
    )


def test_no_expanduser_outside_shared_paths_py():
    """Only _shared_paths.py may call .expanduser() — everywhere else should use CLAUDE_DIR."""
    violations = []
    for py_file in TESTS_DIR.rglob("*.py"):
        if py_file.name in EXPANDUSER_EXEMPT:
            continue
        for lineno, line in enumerate(py_file.read_text().splitlines(), start=1):
            if line.strip().startswith("#"):
                continue
            if EXPANDUSER_CALL_PATTERN.search(line):
                violations.append(f"{py_file.relative_to(CLAUDE_DIR)}:{lineno}: {line.strip()}")

    assert not violations, (
        "Files outside _shared_paths.py call .expanduser(), resolving ~ against the real "
        "$HOME instead of CLAUDE_DIR (see portable_paths.md):\n" + "\n".join(violations)
    )


def test_no_hardcoded_home_constants_in_tests():
    """Test files must not hardcode another machine's home directory as a path constant."""
    violations = []
    for py_file in TESTS_DIR.rglob("*.py"):
        for lineno, line in enumerate(py_file.read_text().splitlines(), start=1):
            if HARDCODED_HOME_CONSTANT.match(line.strip()):
                violations.append(f"{py_file.relative_to(CLAUDE_DIR)}:{lineno}: {line.strip()}")

    assert not violations, (
        "Test files hardcode a machine-specific home directory as a path constant "
        "instead of resolving via CLAUDE_DIR (see portable_paths.md):\n" +
        "\n".join(violations)
    )


def test_no_hardcoded_import_prefix_in_parsers():
    """Import-line parsers must not hardcode '@~/.claude/' or '@~/claude/' as the match string."""
    violations = []
    for py_file in TESTS_DIR.rglob("*.py"):
        for lineno, line in enumerate(py_file.read_text().splitlines(), start=1):
            if HARDCODED_IMPORT_PREFIX.search(line):
                violations.append(f"{py_file.relative_to(CLAUDE_DIR)}:{lineno}: {line.strip()}")

    assert not violations, (
        "A parser hardcodes one config-dir naming convention when matching @import "
        "lines — detect any '@~/<name>/' prefix generically instead "
        "(see portable_paths.md):\n" + "\n".join(violations)
    )


def test_hardcoded_source_pattern_only_matches_real_file_operations():
    """The hook regex must target source/cat/file-test commands, not UX copy mentioning the path."""
    real_violation = 'source ~/.claude/_templates/utils/shell_utils.sh'
    ux_copy = 'additionalContext="confirm this mkdir follows ~/.claude/ conventions"'

    assert HARDCODED_SOURCE_PATTERN.search(real_violation)
    assert not HARDCODED_SOURCE_PATTERN.search(ux_copy), (
        "Prose describing a convention to the user must not be flagged as a real path operation"
    )


def test_expanduser_pattern_matches_common_call_shapes():
    """The .expanduser() regex must match real call syntax regardless of what precedes it."""
    assert EXPANDUSER_CALL_PATTERN.search("Path(x).expanduser()"), "Path(...).expanduser() should match"
    assert EXPANDUSER_CALL_PATTERN.search("paths.append(Path(hook_ref).expanduser())"), (
        "The exact pattern from the test_hook_registry.py bug should match"
    )
    assert not EXPANDUSER_CALL_PATTERN.search("expanduser is a method that resolves ~"), (
        "Prose mentioning the concept without call syntax should not match"
    )


def test_hooks_dir_and_tests_dir_resolve_under_claude_dir():
    """Sanity: the two directories this suite scans must actually live under CLAUDE_DIR."""
    assert HOOKS_DIR.is_relative_to(CLAUDE_DIR)
    assert TESTS_DIR.is_relative_to(CLAUDE_DIR)


@pytest.mark.parametrize(
    "line,should_match",
    [
        ('HOOK_SCRIPT = "/home/paul/.claude/hooks/x.sh"', True),
        ('HOOK_SCRIPT = "/Users/someone/.claude/hooks/x.sh"', True),
        ('CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", ""))', False),
        ('    result = "/home/paul/example.md"  # indented, not a module constant', False),
    ],
)
def test_hardcoded_home_constant_pattern_boundary(line, should_match):
    """The constant-hardcode regex must fire only on uppercase module-level assignments."""
    matched = bool(HARDCODED_HOME_CONSTANT.match(line.strip()))
    assert matched == should_match, f"Expected match={should_match} for: {line!r}"


@pytest.mark.parametrize("prefix", ["@~/.claude/", "@~/claude/"])
def test_hardcoded_import_prefix_pattern_catches_both_conventions(prefix):
    """The import-prefix regex must catch the hardcode regardless of which convention is baked in."""
    violation = f'if not stripped.startswith("{prefix}"):'
    assert HARDCODED_IMPORT_PREFIX.search(violation), (
        f"Should flag a hardcoded '{prefix}' comparison as a portability violation"
    )
