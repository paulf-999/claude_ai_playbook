"""Behavioural tests for the pitfalls skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Five defined pitfall categories checked (implementation, integration, assumptions, rollback, testing)
- Output ranked by likelihood
- Each pitfall includes a mitigation
- Specificity enforced (no generic warnings)
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

PITFALL_CATEGORIES = [
    "implementation",
    "integration",
    "assumptions",
    "rollback",
    "testing",
]
LIKELIHOOD_TERM = "likelihood"
MITIGATION_TERM = "mitigation"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "pitfalls" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: category coverage ─────────────────────────────────────────────────

@pytest.mark.parametrize("category", PITFALL_CATEGORIES)
def test_pitfall_category_present(category: str, skill_content: str) -> None:
    """SKILL.md must define all five pitfall categories."""
    assert category in skill_content, (
        f"pitfalls/SKILL.md must include '{category}' as a pitfall category"
    )


# ─── Tests: output rules ──────────────────────────────────────────────────────

def test_likelihood_ranking_required(skill_content: str) -> None:
    """SKILL.md must instruct Claude to rank pitfalls by likelihood."""
    assert LIKELIHOOD_TERM in skill_content, (
        "pitfalls/SKILL.md must instruct Claude to rank pitfalls by likelihood"
    )


def test_mitigation_required(skill_content: str) -> None:
    """SKILL.md must require a mitigation for each pitfall."""
    assert MITIGATION_TERM in skill_content, (
        "pitfalls/SKILL.md must require a one-line mitigation for each pitfall"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /pitfalls explicit trigger."""
    assert "/pitfalls" in skill_content, (
        "pitfalls/SKILL.md frontmatter must include /pitfalls as an explicit trigger"
    )
