"""Behavioural tests for the redteam skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Verdict (Strong/Shaky/Broken) issued before analysis
- Attack vectors identified with assumption, exploit scenario, and severity
- Strongest counter-argument stated as if making the case to kill the plan
- Defences provided for High/Medium attack vectors
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

VERDICT_TERMS = ["strong", "shaky", "broken"]
ATTACK_VECTOR_TERM = "attack vector"
COUNTER_ARGUMENT_TERM = "counter-argument"
DEFENCE_TERM = "defence"
SEVERITY_TERMS = ["high", "medium", "low"]

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "redteam" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: verdict ───────────────────────────────────────────────────────────

def test_verdict_options_present(skill_content: str) -> None:
    """SKILL.md must define Strong, Shaky, and Broken as the verdict options."""
    assert all(term in skill_content for term in VERDICT_TERMS), (
        "redteam/SKILL.md must define Strong, Shaky, and Broken as verdict options"
    )


# ─── Tests: attack vector structure ───────────────────────────────────────────

def test_attack_vectors_required(skill_content: str) -> None:
    """SKILL.md must require identification of attack vectors."""
    assert ATTACK_VECTOR_TERM in skill_content, (
        "redteam/SKILL.md must require identification of attack vectors with assumption and exploit scenario"
    )


def test_severity_levels_defined(skill_content: str) -> None:
    """SKILL.md must define High/Medium/Low severity for each attack vector."""
    assert all(term in skill_content for term in SEVERITY_TERMS), (
        "redteam/SKILL.md must define High, Medium, and Low severity levels for attack vectors"
    )


# ─── Tests: counter-argument and defences ────────────────────────────────────

def test_counter_argument_required(skill_content: str) -> None:
    """SKILL.md must require the strongest counter-argument against the plan."""
    assert COUNTER_ARGUMENT_TERM in skill_content, (
        "redteam/SKILL.md must require the strongest counter-argument as if making the case to kill the plan"
    )


def test_defences_required(skill_content: str) -> None:
    """SKILL.md must require defences for High/Medium attack vectors."""
    assert DEFENCE_TERM in skill_content, (
        "redteam/SKILL.md must require concrete defences for High and Medium attack vectors"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_maturity(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a maturity level."""
    assert "maturity:" in skill_content, (
        "redteam/SKILL.md frontmatter must include a maturity field"
    )


def test_frontmatter_has_version(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a version."""
    assert "version:" in skill_content, (
        "redteam/SKILL.md frontmatter must include a version field"
    )


def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /redteam explicit trigger."""
    assert "/redteam" in skill_content, (
        "redteam/SKILL.md frontmatter must include /redteam as an explicit trigger"
    )
