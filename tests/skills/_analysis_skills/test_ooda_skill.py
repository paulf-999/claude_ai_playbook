"""Behavioural tests for the ooda skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- All four OODA phases present (Observe, Orient, Decide, Act)
- Facts separated from assumptions in Observe phase
- Direct recommendation required in Decide phase
- Act phase includes a concrete action, signal, and tripwire
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

OODA_PHASES = ["observe", "orient", "decide", "act"]
ASSUMPTION_TERM = "assumed"
RECOMMENDATION_TERM = "recommendation"
SIGNAL_TERM = "signal"
TRIPWIRE_TERM = "tripwire"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "ooda" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: four phases ────────────────────────────────────────────────────────

@pytest.mark.parametrize("phase", OODA_PHASES)
def test_ooda_phase_present(phase: str, skill_content: str) -> None:
    """All four OODA phases must be present in the skill."""
    assert phase in skill_content, (
        f"ooda/SKILL.md must define the '{phase}' phase"
    )


# ─── Tests: observe rules ─────────────────────────────────────────────────────

def test_assumptions_flagged_in_observe(skill_content: str) -> None:
    """SKILL.md must instruct Claude to flag assumptions explicitly in the Observe phase."""
    assert ASSUMPTION_TERM in skill_content, (
        "ooda/SKILL.md must instruct Claude to mark unverified items as assumed in Observe"
    )


# ─── Tests: decide rules ──────────────────────────────────────────────────────

def test_recommendation_required_in_decide(skill_content: str) -> None:
    """SKILL.md must require a direct recommendation in the Decide phase."""
    assert RECOMMENDATION_TERM in skill_content, (
        "ooda/SKILL.md must require a direct recommendation with rationale in the Decide phase"
    )


# ─── Tests: act rules ─────────────────────────────────────────────────────────

def test_signal_required_in_act(skill_content: str) -> None:
    """SKILL.md must require a signal that confirms the decision worked."""
    assert SIGNAL_TERM in skill_content, (
        "ooda/SKILL.md must require a signal in the Act phase to confirm the decision was correct"
    )


def test_tripwire_required_in_act(skill_content: str) -> None:
    """SKILL.md must require a tripwire that would trigger reassessment."""
    assert TRIPWIRE_TERM in skill_content, (
        "ooda/SKILL.md must require a tripwire in the Act phase to define when to reassess"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /ooda explicit trigger."""
    assert "/ooda" in skill_content, (
        "ooda/SKILL.md frontmatter must include /ooda as an explicit trigger"
    )
