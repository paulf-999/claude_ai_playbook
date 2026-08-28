"""Structural tests for _rules/claude_internal/git.md.

Verifies that the git rules file is present, well-formed, and contains
the expected section headings that give the file its mechanical value.
"""
import re
from pathlib import Path

GIT_RULES = Path.home() / ".claude" / "_rules" / "claude_internal" / "git.md"

EXPECTED_SECTIONS = [
    "Commits",
    "Branch",
    "Pull requests",
]

EXPECTED_PATTERNS = [
    r"Conventional Commits",
    r"feature/|hotfix/|release/",
    r"main",
]


def test_git_rules_file_exists():
    """git.md must be present at the expected path."""
    assert GIT_RULES.exists(), f"git.md missing: {GIT_RULES}"


def test_git_rules_has_expected_sections():
    """git.md must contain headings for commits, branching, and PRs."""
    content = GIT_RULES.read_text()
    for section in EXPECTED_SECTIONS:
        assert section.lower() in content.lower(), (
            f"git.md missing expected section: '{section}'"
        )


def test_git_rules_contains_key_patterns():
    """git.md must reference Conventional Commits, branch prefixes, and main protection."""
    content = GIT_RULES.read_text()
    for pattern in EXPECTED_PATTERNS:
        assert re.search(pattern, content), (
            f"git.md missing expected pattern: '{pattern}'"
        )


def test_git_rules_line_limit():
    """git.md must not exceed 110 lines."""
    lines = GIT_RULES.read_text().splitlines()
    assert len(lines) <= 110, f"git.md: {len(lines)} lines exceeds 110-line limit"


def test_git_rules_ends_with_newline():
    """git.md must end with exactly one newline."""
    raw = GIT_RULES.read_bytes()
    assert raw.endswith(b"\n"), "git.md does not end with a newline"
    assert not raw.endswith(b"\n\n"), "git.md ends with multiple newlines"
