"""Behavioural tests for the confluence_create_page skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Known page pattern names (generic and data platform)
- Draft file location and slug format
- Mandatory local draft review before Confluence publication
"""

import re
from pathlib import Path

import pytest

# ─── Pattern names ─────────────────────────────────────────────────────────────

GENERIC_PATTERNS = [
    "general_page",
    "how_to",
    "requirements",
    "incident_report",
    "claude_component",
    "design_decision",
]

DATA_PLATFORM_PATTERNS = [
    "data_platform_sprint_goals",
    "platform_risk_assessment",
    "initiative_idea",
]

ALL_PATTERNS = GENERIC_PATTERNS + DATA_PLATFORM_PATTERNS

# ─── Draft file convention ─────────────────────────────────────────────────────

DRAFT_DIR = "~/_drafts/confluence/"
DRAFT_SLUG_PATTERN = re.compile(r"^[a-z0-9_]+\.md$")

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_atlassian_skills"
    / "confluence_create_page" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: pattern names ──────────────────────────────────────────────────────

@pytest.mark.parametrize("pattern", ALL_PATTERNS)
def test_pattern_documented_in_skill(pattern: str) -> None:
    """Every known pattern must be referenced in SKILL.md.

    :param pattern: Pattern name to check.
    :type pattern: str
    """
    assert pattern in _skill_content(), (
        f"confluence_create_page/SKILL.md must document the '{pattern}' pattern"
    )


def test_generic_pattern_count() -> None:
    """SKILL.md must document exactly the expected number of generic patterns."""
    content = _skill_content()
    found = [p for p in GENERIC_PATTERNS if p in content]
    assert len(found) == len(GENERIC_PATTERNS), (
        f"Expected {len(GENERIC_PATTERNS)} generic patterns in SKILL.md, found {len(found)}: "
        f"missing {set(GENERIC_PATTERNS) - set(found)}"
    )


def test_data_platform_pattern_count() -> None:
    """SKILL.md must document exactly the expected number of data platform patterns."""
    content = _skill_content()
    found = [p for p in DATA_PLATFORM_PATTERNS if p in content]
    assert len(found) == len(DATA_PLATFORM_PATTERNS), (
        f"Expected {len(DATA_PLATFORM_PATTERNS)} data platform patterns in SKILL.md, found {len(found)}: "
        f"missing {set(DATA_PLATFORM_PATTERNS) - set(found)}"
    )


# ─── Tests: draft file convention ─────────────────────────────────────────────

def test_draft_directory_documented() -> None:
    """SKILL.md must document the ~/_drafts/confluence/ directory for draft files."""
    assert DRAFT_DIR in _skill_content(), (
        f"confluence_create_page/SKILL.md must reference {DRAFT_DIR} as the draft directory"
    )


@pytest.mark.parametrize("slug,expected_valid", [
    ("sprint_goals_draft.md", True),
    ("design_decision_draft.md", True),
    ("how_to_use_rundeck_draft.md", True),
    ("My Page Draft.md", False),        # spaces not allowed
    ("design-decision_draft.md", False),  # hyphens not allowed
    ("SPRINT_GOALS_draft.md", False),   # uppercase not allowed
])
def test_draft_slug_format(slug: str, expected_valid: bool) -> None:
    """Draft filenames must be lowercase with underscores only (no spaces or hyphens).

    :param slug: Draft filename to validate.
    :type slug: str
    :param expected_valid: Whether the slug is expected to be valid.
    :type expected_valid: bool
    """
    assert bool(DRAFT_SLUG_PATTERN.match(slug)) == expected_valid, (
        f"Draft slug {slug!r} expected valid={expected_valid}"
    )


# ─── Tests: mandatory draft review ────────────────────────────────────────────

def test_draft_review_mandatory_before_publish() -> None:
    """SKILL.md must require a local draft review before publishing to Confluence."""
    content = _skill_content()
    mandatory_terms = ["mandatory", "must", "before"]
    assert any(term in content.lower() for term in mandatory_terms), (
        "confluence_create_page/SKILL.md must mark local draft review as mandatory before publishing"
    )


def test_draft_review_step_exists() -> None:
    """SKILL.md must include a Local Draft Review phase."""
    assert "Local Draft Review" in _skill_content(), (
        "confluence_create_page/SKILL.md must contain a 'Local Draft Review' phase"
    )


def test_user_approval_required_before_publish() -> None:
    """SKILL.md must require explicit user approval before creating the Confluence page."""
    content = _skill_content()
    approval_terms = ["approved", "approval", "approve"]
    assert any(term in content.lower() for term in approval_terms), (
        "confluence_create_page/SKILL.md must require explicit user approval before publishing"
    )
