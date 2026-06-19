"""Behavioural tests for the 10x skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Defined list of cut targets (filler, hedging, passive, redundant pairs, meta-commentary)
- Core argument must be preserved (no substance changes)
- Word count reduction reported in output
- If text is already tight, skill must say so and return it unchanged
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

CUT_TARGETS = ["filler", "hedge", "passive", "redundant"]
PRESERVE_TERM = "substance"
WORD_COUNT_TERM = "word count"
ALREADY_TIGHT_TERM = "already tight"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_communication_skills" / "10x" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: cut rules ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("target", CUT_TARGETS)
def test_cut_target_present(target: str, skill_content: str) -> None:
    """SKILL.md must enumerate each category of content to cut."""
    assert target in skill_content, (
        f"10x/SKILL.md must define '{target}' as a cut target"
    )


# ─── Tests: preserve rules ────────────────────────────────────────────────────

def test_substance_preservation_required(skill_content: str) -> None:
    """SKILL.md must instruct Claude to preserve the core argument."""
    assert PRESERVE_TERM in skill_content, (
        "10x/SKILL.md must instruct Claude not to change the substance of the original text"
    )


# ─── Tests: output rules ──────────────────────────────────────────────────────

def test_word_count_reported(skill_content: str) -> None:
    """SKILL.md must require a word count reduction to be reported."""
    assert WORD_COUNT_TERM in skill_content, (
        "10x/SKILL.md must require Claude to report the word count reduction"
    )


def test_already_tight_handled(skill_content: str) -> None:
    """SKILL.md must define behaviour when the text is already tight."""
    assert ALREADY_TIGHT_TERM in skill_content, (
        "10x/SKILL.md must instruct Claude to return text unchanged and say so if it is already tight"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_maturity(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a maturity level."""
    assert "maturity:" in skill_content, (
        "10x/SKILL.md frontmatter must include a maturity field"
    )


def test_frontmatter_has_version(skill_content: str) -> None:
    """SKILL.md frontmatter must declare a version."""
    assert "version:" in skill_content, (
        "10x/SKILL.md frontmatter must include a version field"
    )


def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /10x explicit trigger."""
    assert "/10x" in skill_content, (
        "10x/SKILL.md frontmatter must include /10x as an explicit trigger"
    )
