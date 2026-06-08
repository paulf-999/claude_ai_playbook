"""Behavioural tests for the jira_update skill."""

from pathlib import Path

import pytest

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src"
    / "claude"
    / "skills"
    / "_atlassian_skills"
    / "jira_update"
    / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_MD.read_text()


def test_skill_file_exists():
    """SKILL.md must exist at the expected path."""
    assert SKILL_MD.exists(), "jira_update/SKILL.md not found"


def test_bulk_update_pattern_documented(skill_content):
    """SKILL.md must reference the bulk_update pattern."""
    assert "bulk_update" in skill_content


def test_pattern_file_path_documented(skill_content):
    """SKILL.md must document the path to the bulk_update pattern file."""
    assert "jira_update/patterns" in skill_content


def test_atlassian_mcp_precheck_required(skill_content):
    """SKILL.md must document an Atlassian MCP pre-check before proceeding."""
    assert (
        "getAccessibleAtlassianResources" in skill_content
        or "Atlassian MCP" in skill_content
    ), "Skill must document an Atlassian MCP pre-check"


def test_mcp_failure_stops_execution(skill_content):
    """SKILL.md must instruct Claude to stop when the MCP server is unavailable."""
    lower = skill_content.lower()
    assert "stop" in lower or "do not proceed" in lower, (
        "Skill must instruct Claude to stop when MCP is unavailable"
    )


def test_confirmation_required_before_applying(skill_content):
    """SKILL.md must require user confirmation before applying bulk updates."""
    lower = skill_content.lower()
    assert "confirm" in lower or "confirmation_required: true" in skill_content, (
        "Skill must require confirmation before applying changes"
    )
