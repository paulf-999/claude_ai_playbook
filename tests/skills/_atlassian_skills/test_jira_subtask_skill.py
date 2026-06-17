"""Behavioural tests for the jira_subtask skill."""

from pathlib import Path

import pytest

_SKILL_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "src"
    / "claude"
    / "skills"
    / "_atlassian_skills"
    / "jira_subtask"
)

SKILL_MD = _SKILL_DIR / "SKILL.md"
PHASE3_MD = _SKILL_DIR / "phase3.md"


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_MD.read_text()


@pytest.fixture(scope="module")
def phase3_content() -> str:
    return PHASE3_MD.read_text()


# ---------------------------------------------------------------------------
# SKILL.md tests
# ---------------------------------------------------------------------------


def test_skill_file_exists():
    """SKILL.md must exist at the expected path under _atlassian_skills."""
    assert SKILL_MD.exists(), "jira_subtask/SKILL.md not found under _atlassian_skills"


def test_phase3_child_page_exists():
    """phase3.md child page must exist alongside SKILL.md."""
    assert PHASE3_MD.exists(), "jira_subtask/phase3.md not found"


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


def test_phase3_child_page_referenced(skill_content):
    """SKILL.md must reference phase3.md for critical field rules."""
    assert "phase3.md" in skill_content, (
        "SKILL.md must reference phase3.md for creation field rules"
    )


def test_confirmation_required_before_phase3(skill_content):
    """SKILL.md must require user confirmation before proceeding to Phase 3."""
    lower = skill_content.lower()
    assert "confirm" in lower or "proceed" in lower, (
        "Skill must require user confirmation before creating sub-tasks"
    )


def test_completion_table_documented(skill_content):
    """SKILL.md must document a Phase 4 results table covering all attempted sub-tasks."""
    assert "| # |" in skill_content or "| 1 |" in skill_content, (
        "Skill must document a Phase 4 results table"
    )


# ---------------------------------------------------------------------------
# phase3.md tests — critical field rules
# ---------------------------------------------------------------------------


def test_issue_type_hyphenated(phase3_content):
    """phase3.md must specify issue type as 'Sub-task' with a hyphen."""
    assert "Sub-task" in phase3_content, (
        "Issue type must be 'Sub-task' (hyphenated) — never 'Subtask' or 'sub-task'"
    )


def test_sprint_field_excluded(phase3_content):
    """phase3.md must explicitly exclude customfield_10020 (sprint) from sub-tasks."""
    assert "customfield_10020" in phase3_content, (
        "phase3.md must document that customfield_10020 (sprint) must never be set on sub-tasks"
    )


def test_story_points_excluded(phase3_content):
    """phase3.md must explicitly exclude customfield_10028 (story points) from sub-tasks."""
    assert "customfield_10028" in phase3_content, (
        "phase3.md must document that customfield_10028 (story points) must never be set on sub-tasks"
    )


def test_dm_claude_created_label_required(phase3_content):
    """phase3.md must require the dm-claude-created label on all sub-tasks."""
    assert "dm-claude-created" in phase3_content, (
        "phase3.md must require the dm-claude-created label"
    )


def test_business_value_excluded(phase3_content):
    """phase3.md must document that Business Value must not be set on sub-tasks."""
    lower = phase3_content.lower()
    assert "business value" in lower, (
        "phase3.md must document that Business Value must not be set on sub-tasks"
    )


def test_null_assignee_omitted_not_null(phase3_content):
    """phase3.md must instruct Claude to omit the assignee field when null, not pass null."""
    assert "null" in phase3_content.lower() and "omit" in phase3_content.lower(), (
        "phase3.md must instruct Claude to omit the assignee field when the parent has no assignee"
    )


def test_continue_on_failure(phase3_content):
    """phase3.md must instruct Claude to continue through all sub-tasks on failure."""
    lower = phase3_content.lower()
    assert "do not stop" in lower or "continue" in lower, (
        "phase3.md must instruct Claude to continue through all sub-tasks even if one fails"
    )
