"""Behavioural tests for the manage_jira skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Known operation pattern names
- Pattern file path format
- Atlassian MCP pre-check requirement
"""

from pathlib import Path

import pytest

# ─── Pattern names ─────────────────────────────────────────────────────────────

OPERATION_PATTERNS = [
    "batch_create_from_template",
    "bulk_update",
    "hygiene_check",
    "epic_create",
]

PATTERN_FILE_BASE = "~/.claude/skills/_atlassian_skills/manage_jira/patterns/"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_atlassian_skills" / "manage_jira" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: pattern names ──────────────────────────────────────────────────────

@pytest.mark.parametrize("pattern", OPERATION_PATTERNS)
def test_pattern_documented_in_skill(pattern: str) -> None:
    """Every known operation pattern must be referenced in SKILL.md.

    :param pattern: Pattern name to check.
    :type pattern: str
    """
    assert pattern in _skill_content(), (
        f"manage_jira/SKILL.md must document the '{pattern}' operation pattern"
    )


def test_pattern_count() -> None:
    """SKILL.md must document exactly the expected number of operation patterns."""
    content = _skill_content()
    found = [p for p in OPERATION_PATTERNS if p in content]
    assert len(found) == len(OPERATION_PATTERNS), (
        f"Expected {len(OPERATION_PATTERNS)} patterns in SKILL.md, found {len(found)}: "
        f"missing {set(OPERATION_PATTERNS) - set(found)}"
    )


# ─── Tests: pattern file path ──────────────────────────────────────────────────

def test_pattern_file_base_path_documented() -> None:
    """SKILL.md must document the base path where pattern files are stored."""
    assert "manage_jira/patterns" in _skill_content(), (
        "manage_jira/SKILL.md must reference the patterns/ subdirectory for pattern files"
    )


# ─── Tests: MCP pre-check ──────────────────────────────────────────────────────

def test_atlassian_mcp_precheck_required() -> None:
    """SKILL.md must verify the Atlassian MCP is available before proceeding."""
    content = _skill_content()
    assert "getAccessibleAtlassianResources" in content or "Atlassian MCP" in content, (
        "manage_jira/SKILL.md must require an Atlassian MCP pre-check before proceeding"
    )


def test_mcp_failure_stops_execution() -> None:
    """SKILL.md must instruct Claude to stop if the Atlassian MCP is unavailable."""
    content = _skill_content()
    stop_terms = ["stop", "do not proceed"]
    assert any(term in content.lower() for term in stop_terms), (
        "manage_jira/SKILL.md must stop if the Atlassian MCP pre-check fails"
    )
