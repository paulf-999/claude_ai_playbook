"""Behavioural tests for the premortem skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Failure assumed as the starting premise (not hedged as a possibility)
- Three cause chains generated as narrative sequences
- Chains ranked by likelihood x impact
- One mitigation per chain, targeting the earliest breakable link
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

FAILURE_FRAME_TERM = "has failed"
CAUSE_CHAIN_TERM = "cause chain"
LIKELIHOOD_TERM = "likelihood"
MITIGATION_TERM = "mitigation"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_analysis_skills" / "premortem" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: failure framing ───────────────────────────────────────────────────

def test_failure_stated_as_fact(skill_content: str) -> None:
    """SKILL.md must assert failure as a fact, not a hypothesis."""
    assert FAILURE_FRAME_TERM in skill_content, (
        "premortem/SKILL.md must state the failure as an assumed fact ('has failed'), not a possibility"
    )


def test_cause_chains_required(skill_content: str) -> None:
    """SKILL.md must require narrative cause chains, not generic risks."""
    assert CAUSE_CHAIN_TERM in skill_content, (
        "premortem/SKILL.md must require cause chains as narrative sequences of linked events"
    )


# ─── Tests: ranking and mitigation ────────────────────────────────────────────

def test_likelihood_ranking_required(skill_content: str) -> None:
    """SKILL.md must instruct Claude to rank chains by likelihood."""
    assert LIKELIHOOD_TERM in skill_content, (
        "premortem/SKILL.md must require ranking cause chains by likelihood"
    )


def test_mitigations_required(skill_content: str) -> None:
    """SKILL.md must require one mitigation per cause chain."""
    assert MITIGATION_TERM in skill_content, (
        "premortem/SKILL.md must require a concrete mitigation for each cause chain"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_maturity(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a maturity level."""
    assert "maturity:" in skill_content, (
        "premortem/SKILL.md frontmatter must include a maturity field"
    )


def test_frontmatter_has_version(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a version."""
    assert "version:" in skill_content, (
        "premortem/SKILL.md frontmatter must include a version field"
    )


def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /premortem explicit trigger."""
    assert "/premortem" in skill_content, (
        "premortem/SKILL.md frontmatter must include /premortem as an explicit trigger"
    )
