"""Behavioural tests for the compare skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Two or more options must be parsed before comparing
- Criteria identified and labelled by weight before the table is populated
- Comparison table populated with Strong/Acceptable/Weak ratings
- Direct recommendation with conditions for choosing the other option
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

CRITERIA_WEIGHT_TERMS = ["critical", "important", "nice-to-have"]
RATING_TERMS = ["strong", "acceptable", "weak"]
RECOMMENDATION_TERM = "recommendation"
ALTERNATIVE_TERM = "when to choose"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "compare" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: comparison rules ───────────────────────────────────────────────────

def test_criteria_weight_labels_present(skill_content: str) -> None:
    """SKILL.md must instruct Claude to label each criterion by weight."""
    assert any(term in skill_content for term in CRITERIA_WEIGHT_TERMS), (
        "compare/SKILL.md must instruct Claude to label criteria as Critical, Important, or Nice-to-have"
    )


def test_rating_scale_present(skill_content: str) -> None:
    """SKILL.md must define a Strong/Acceptable/Weak rating scale."""
    assert all(term in skill_content for term in RATING_TERMS), (
        "compare/SKILL.md must define a Strong / Acceptable / Weak rating scale for the comparison table"
    )


def test_recommendation_required(skill_content: str) -> None:
    """SKILL.md must require a direct recommendation."""
    assert RECOMMENDATION_TERM in skill_content, (
        "compare/SKILL.md must require a direct recommendation with rationale"
    )


def test_alternative_condition_required(skill_content: str) -> None:
    """SKILL.md must require a condition for choosing the other option."""
    assert ALTERNATIVE_TERM in skill_content, (
        "compare/SKILL.md must state when the other option would be the right call"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /compare explicit trigger."""
    assert "/compare" in skill_content, (
        "compare/SKILL.md frontmatter must include /compare as an explicit trigger"
    )
