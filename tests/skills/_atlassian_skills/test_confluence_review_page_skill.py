"""Behavioural tests for the confluence_review_page skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Atlassian MCP pre-check before proceeding
- Phase structure: fetch → analyse → confirm → post
- Confirmation required before posting the review comment
"""

from pathlib import Path

import pytest

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_atlassian_skills"
    / "confluence_review_page" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Load SKILL.md content once for the module."""
    return SKILL_MD.read_text()


# ─── Tests ─────────────────────────────────────────────────────────────────────

def test_skill_file_exists() -> None:
    """SKILL.md must exist at the expected path."""
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"


def test_atlassian_mcp_precheck_required(skill_content: str) -> None:
    """SKILL.md must require the Atlassian MCP pre-check before proceeding."""
    assert "getAccessibleAtlassianResources" in skill_content, (
        "confluence_review_page/SKILL.md must call getAccessibleAtlassianResources before proceeding"
    )


def test_mcp_failure_stops_execution(skill_content: str) -> None:
    """SKILL.md must instruct Claude to stop if the MCP pre-check fails."""
    assert "make enable_mcp server=Atlassian" in skill_content, (
        "confluence_review_page/SKILL.md must tell the user to run 'make enable_mcp server=Atlassian' if the MCP is unavailable"
    )


def test_page_fetch_phase_documented(skill_content: str) -> None:
    """SKILL.md must document a phase for fetching page data."""
    assert "phase2.md" in skill_content or "Fetch" in skill_content, (
        "confluence_review_page/SKILL.md must reference a page-fetch phase"
    )


def test_technical_writer_subagent_used(skill_content: str) -> None:
    """SKILL.md must dispatch analysis to the technical_writer sub-agent."""
    assert "technical_writer" in skill_content, (
        "confluence_review_page/SKILL.md must use the technical_writer sub-agent for analysis"
    )


def test_confirmation_required_before_posting(skill_content: str) -> None:
    """SKILL.md must require user confirmation before posting the review comment."""
    content_lower = skill_content.lower()
    assert any(term in content_lower for term in ["confirm", "y/n", "(y/n)"]), (
        "confluence_review_page/SKILL.md must ask for user confirmation before posting"
    )
