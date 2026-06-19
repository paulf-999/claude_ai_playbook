"""Behavioural tests for the eli5 skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Anchor analogy required before the explanation
- Jargon must be stripped or defined
- Output under 150 words
- So-what sentence required
- No bullet lists in output
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

ANALOGY_TERM = "anchor analogy"
JARGON_TERM = "jargon"
WORD_LIMIT_TERM = "150"
SO_WHAT_TERM = "why it matters"
NO_BULLETS_TERM = "bullet"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_communication_skills" / "eli5" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: explanation rules ─────────────────────────────────────────────────

def test_anchor_analogy_required(skill_content: str) -> None:
    """SKILL.md must require an anchor analogy before the explanation."""
    assert ANALOGY_TERM in skill_content, (
        "eli5/SKILL.md must require an anchor analogy stated before the explanation"
    )


def test_jargon_stripping_required(skill_content: str) -> None:
    """SKILL.md must instruct Claude to strip or define jargon."""
    assert JARGON_TERM in skill_content, (
        "eli5/SKILL.md must instruct Claude to strip jargon or replace with plain English"
    )


def test_word_limit_enforced(skill_content: str) -> None:
    """SKILL.md must enforce a maximum word count on the output."""
    assert WORD_LIMIT_TERM in skill_content, (
        "eli5/SKILL.md must enforce a maximum word count (150 words) on the explanation"
    )


def test_so_what_required(skill_content: str) -> None:
    """SKILL.md must require a so-what sentence explaining why the concept matters."""
    assert SO_WHAT_TERM in skill_content, (
        "eli5/SKILL.md must require a 'why it matters' sentence in the output"
    )


def test_no_bullet_lists_in_output(skill_content: str) -> None:
    """SKILL.md must prohibit bullet lists in the output."""
    assert NO_BULLETS_TERM in skill_content, (
        "eli5/SKILL.md must explicitly prohibit bullet lists in the output"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /eli5 explicit trigger."""
    assert "/eli5" in skill_content, (
        "eli5/SKILL.md frontmatter must include /eli5 as an explicit trigger"
    )
