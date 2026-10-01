# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-01
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that hook scripts follow portable_paths.md — no hardcoded config-dir paths.

The config lives at ``~/.claude``, ``~/claude`` or a repo checkout, so a hook that
reads ``~/.claude/...`` passes on one machine and silently fails on another (found
2026-09-17). Hooks must resolve the config dir from their own location. The
patterns are proven on real and harmless lines, so a loosened regex fails here.
``test_portable_paths_python.py`` covers the Python side.
"""
from __future__ import annotations

import re

from _shared_paths import CLAUDE_DIR
from _shared_paths import HOOKS_DIR

# Only real file operations, not prose that mentions a path to the user
# The word boundary sits inside the group: before "[[" there is no word boundary to match,
# so the old form never caught a file test such as [[ -f ~/.claude/x ]]
HARDCODED_SOURCE_PATTERN = re.compile(r"(\bsource|\bcat|\[\[\s*-[fe])\s+.*(~/\.claude/|~/claude/)")
# Guard clauses that compare against a literal config-dir substring, e.g. *".claude/"*
HARDCODED_GUARD_PATTERN = re.compile(r'\*"[^"$]*claude/"\*')
OWN_LOCATION = 'dirname "${BASH_SOURCE[0]}"'


def hook_lines() -> list[tuple[str, int, str]]:
    """List every non-comment line of every hook script.

    :return: ``(hook name, line number, stripped line)`` for each code line.
    :rtype: list[tuple[str, int, str]]
    """
    return [
        (hook.name, number, line.strip())
        for hook in sorted(HOOKS_DIR.glob("*.sh"))
        for number, line in enumerate(hook.read_text().splitlines(), start=1)
        if line.strip() and not line.strip().startswith("#")
    ]


def test_hooks_exist_to_scan():
    """There are hook scripts to scan, so the checks below can't pass on nothing."""
    assert HOOKS_DIR.is_relative_to(CLAUDE_DIR), f"{HOOKS_DIR} should sit under {CLAUDE_DIR}"
    assert hook_lines(), f"no hook scripts found in {HOOKS_DIR}"


def test_no_hardcoded_home_in_hooks():
    """Hooks never source, cat or file-test a literal ~/.claude/ or ~/claude/ path."""
    bad = [f"{name}:{n}: {line}" for name, n, line in hook_lines() if HARDCODED_SOURCE_PATTERN.search(line)]
    assert not bad, "Hooks hardcode a config-dir path — resolve it from the script's location:\n" + "\n".join(bad)


def test_no_hardcoded_guard_substring():
    """Hooks never guard on a literal '.claude/' substring instead of the resolved root."""
    bad = [f"{name}:{n}: {line}" for name, n, line in hook_lines() if HARDCODED_GUARD_PATTERN.search(line)]
    assert not bad, "Hooks compare against a hardcoded config-dir substring:\n" + "\n".join(bad)


def test_hooks_resolve_root_from_own_location():
    """Every hook that uses CLAUDE_ROOT_DIR works it out from its own location."""
    users = [h for h in sorted(HOOKS_DIR.glob("*.sh")) if "${CLAUDE_ROOT_DIR}" in h.read_text()]
    assert users, "expected at least one hook to use CLAUDE_ROOT_DIR"
    for hook in users:
        text = hook.read_text()
        if "${CLAUDE_ROOT_DIR}" in text:
            assert OWN_LOCATION in text, f"{hook.name} uses CLAUDE_ROOT_DIR without deriving it from {OWN_LOCATION}"


def test_source_pattern_flags_source():
    """Sourcing a file through ~/.claude/ is flagged."""
    assert HARDCODED_SOURCE_PATTERN.search("source ~/.claude/_templates/utils/shell_utils.sh"), "should flag source"


def test_source_pattern_flags_cat_without_dot():
    """Reading a file through ~/claude/ is flagged too, not just ~/.claude/."""
    assert HARDCODED_SOURCE_PATTERN.search("cat ~/claude/settings.json"), "should flag cat with ~/claude/"


def test_source_pattern_flags_file_tests():
    """A file-existence test against ~/.claude/ is flagged."""
    assert HARDCODED_SOURCE_PATTERN.search('[[ -f ~/.claude/settings.json ]]'), "should flag [[ -f ~/.claude/... ]]"
    assert HARDCODED_SOURCE_PATTERN.search('[[ -e ~/claude/hooks ]]'), "should flag [[ -e ~/claude/... ]]"


def test_source_pattern_ignores_user_facing_text():
    """Text that only mentions the path to the user isn't a file operation."""
    line = 'additionalContext="confirm this mkdir follows ~/.claude/ conventions"'
    assert not HARDCODED_SOURCE_PATTERN.search(line), "prose about a convention must not be flagged"


def test_source_pattern_ignores_resolved_paths():
    """Sourcing through the resolved root is the portable form and isn't flagged."""
    line = 'source "${CLAUDE_ROOT_DIR}/_templates/utils/shell_utils.sh"'
    assert not HARDCODED_SOURCE_PATTERN.search(line), "a resolved path must not be flagged"


def test_guard_pattern_flags_literal_substring():
    """The guard anti-pattern from portable_paths.md is flagged."""
    assert HARDCODED_GUARD_PATTERN.search('[[ "$FILE_PATH" != *".claude/"* ]]'), "should flag *\".claude/\"*"
    assert HARDCODED_GUARD_PATTERN.search('[[ "$FILE_PATH" == *"~/claude/"* ]]'), "should flag *\"~/claude/\"*"


def test_guard_pattern_ignores_resolved_comparison():
    """Comparing against the resolved root, as the hooks do, isn't flagged."""
    line = '[[ "${FILE_PATH}" == "${CLAUDE_ROOT_DIR}/"* ]] || exit 0'
    assert not HARDCODED_GUARD_PATTERN.search(line), "a resolved-root comparison must not be flagged"
