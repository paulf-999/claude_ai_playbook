"""Behavioural tests for the first_principles skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Assumptions surfaced and categorised (inherited, untested, validated)
- Atomic truths identified independently of inherited design
- Solution rebuilt using only atomic truths
- Delta produced comparing rebuilt vs original approach
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

ASSUMPTION_CATEGORY_TERMS = ["inherited", "untested", "validated"]
ATOMIC_TERM = "atomic"
REBUILD_TERM = "rebuild"
DELTA_TERM = "delta"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "first_principles" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: decomposition rules ───────────────────────────────────────────────

def test_assumption_categories_present(skill_content: str) -> None:
    """SKILL.md must instruct Claude to categorise assumptions as inherited, untested, or validated."""
    assert all(term in skill_content for term in ASSUMPTION_CATEGORY_TERMS), (
        "first_principles/SKILL.md must categorise assumptions as Inherited, Untested, or Validated"
    )


def test_atomic_truths_required(skill_content: str) -> None:
    """SKILL.md must require identification of atomic truths."""
    assert ATOMIC_TERM in skill_content, (
        "first_principles/SKILL.md must require Claude to identify atomic truths independently of the inherited design"
    )


def test_rebuild_step_required(skill_content: str) -> None:
    """SKILL.md must require a rebuild from atomic truths only."""
    assert REBUILD_TERM in skill_content, (
        "first_principles/SKILL.md must require Claude to rebuild the approach using only atomic truths"
    )


def test_delta_output_required(skill_content: str) -> None:
    """SKILL.md must require a delta comparing the rebuilt approach to the original."""
    assert DELTA_TERM in skill_content, (
        "first_principles/SKILL.md must require a delta comparing rebuilt vs original approach"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /first_principles explicit trigger."""
    assert "/first_principles" in skill_content, (
        "first_principles/SKILL.md frontmatter must include /first_principles as an explicit trigger"
    )
