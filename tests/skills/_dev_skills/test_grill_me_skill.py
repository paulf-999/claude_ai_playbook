"""Behavioural tests for the grill_me skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- One question asked at a time (never batched)
- Recommended answer provided before asking the user
- Codebase exploration used instead of asking where possible
- Defined exit condition (stop when decisions are confirmed)

Also validates required frontmatter fields are present.
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

ONE_AT_A_TIME_TERM = "one question at a time"
RECOMMENDED_ANSWER_TERM = "recommended answer"
CODEBASE_TERM = "codebase"
EXIT_TERM = "stop when"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_dev_skills" / "grill_me" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_MD.read_text().lower()


# ─── Tests: interview rules ────────────────────────────────────────────────────

def test_one_question_at_a_time(skill_content: str) -> None:
    """SKILL.md must instruct Claude to ask one question at a time."""
    assert ONE_AT_A_TIME_TERM in skill_content, (
        "grill_me/SKILL.md must instruct Claude to ask one question at a time"
    )


def test_provides_recommended_answer(skill_content: str) -> None:
    """SKILL.md must instruct Claude to provide a recommended answer before asking."""
    assert RECOMMENDED_ANSWER_TERM in skill_content, (
        "grill_me/SKILL.md must instruct Claude to provide a recommended answer for each question"
    )


def test_explores_codebase_instead_of_asking(skill_content: str) -> None:
    """SKILL.md must instruct Claude to explore the codebase rather than ask when possible."""
    assert CODEBASE_TERM in skill_content, (
        "grill_me/SKILL.md must reference codebase exploration as an alternative to asking"
    )


# ─── Tests: exit condition ─────────────────────────────────────────────────────

def test_has_exit_condition(skill_content: str) -> None:
    """SKILL.md must define when the interview stops."""
    assert EXIT_TERM in skill_content, (
        "grill_me/SKILL.md must define an exit condition — when to stop interviewing"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_maturity(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a maturity level."""
    assert "maturity:" in skill_content, (
        "grill_me/SKILL.md frontmatter must include a maturity field"
    )


def test_frontmatter_has_version(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a version."""
    assert "version:" in skill_content, (
        "grill_me/SKILL.md frontmatter must include a version field"
    )


def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /grill_me explicit trigger."""
    assert "/grill_me" in skill_content, (
        "grill_me/SKILL.md frontmatter must include /grill_me as an explicit trigger"
    )
