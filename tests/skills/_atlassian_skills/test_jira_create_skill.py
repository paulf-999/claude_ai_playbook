"""Behavioural tests for the jira_create skill."""

from pathlib import Path

import pytest

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src"
    / "claude"
    / "skills"
    / "_atlassian_skills"
    / "jira_create"
    / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_MD.read_text()


def test_skill_file_exists():
    """SKILL.md must exist at the expected path."""
    assert SKILL_MD.exists(), "jira_create/SKILL.md not found"


def test_batch_create_pattern_documented(skill_content):
    """SKILL.md must reference the batch_create_from_template pattern."""
    assert "batch_create_from_template" in skill_content


def test_epic_create_pattern_documented(skill_content):
    """SKILL.md must reference the epic_create pattern."""
    assert "epic_create" in skill_content


def test_pattern_file_path_documented(skill_content):
    """SKILL.md must document the path to the pattern files."""
    assert "jira_create/patterns" in skill_content


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


def test_confirmation_required_before_creating(skill_content):
    """SKILL.md must require user confirmation before creating tickets."""
    lower = skill_content.lower()
    assert "confirm" in lower or "confirmation_required: true" in skill_content, (
        "Skill must require confirmation before creating tickets"
    )
