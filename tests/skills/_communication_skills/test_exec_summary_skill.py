"""Behavioural tests for the exec_summary skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Four enforced output blocks: Context, What happened, So what, Action required
- No internal tool names in output
- Sentence length capped at 25 words
- Total output under 100 words
"""

from pathlib import Path

import pytest

# ─── Constants ─────────────────────────────────────────────────────────────────

CONTEXT_TERM = "context"
SO_WHAT_TERM = "so what"
ACTION_TERM = "action required"
WORD_LIMIT_TERM = "100 words"
SENTENCE_LIMIT_TERM = "25 words"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_communication_skills" / "exec_summary" / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    """Return lowercased SKILL.md content for assertion checks."""
    return SKILL_MD.read_text().lower()


# ─── Tests: output structure ───────────────────────────────────────────────────

def test_context_block_required(skill_content: str) -> None:
    """SKILL.md must require a Context block in the output."""
    assert CONTEXT_TERM in skill_content, (
        "exec_summary/SKILL.md must require a 'Context' block in the output"
    )


def test_so_what_block_required(skill_content: str) -> None:
    """SKILL.md must require a So what (business impact) block."""
    assert SO_WHAT_TERM in skill_content, (
        "exec_summary/SKILL.md must require a 'So what' business impact block"
    )


def test_action_required_block_required(skill_content: str) -> None:
    """SKILL.md must require an Action required block."""
    assert ACTION_TERM in skill_content, (
        "exec_summary/SKILL.md must require an 'Action required' block"
    )


def test_word_limit_enforced(skill_content: str) -> None:
    """SKILL.md must enforce a maximum total word count on the output."""
    assert WORD_LIMIT_TERM in skill_content, (
        "exec_summary/SKILL.md must enforce a 100-word maximum on the total output"
    )


def test_sentence_length_enforced(skill_content: str) -> None:
    """SKILL.md must cap individual sentence length."""
    assert SENTENCE_LIMIT_TERM in skill_content, (
        "exec_summary/SKILL.md must cap sentence length at 25 words"
    )


# ─── Tests: frontmatter structure ─────────────────────────────────────────────

def test_frontmatter_has_explicit_trigger(skill_content: str) -> None:
    """SKILL.md frontmatter must declare the /exec_summary explicit trigger."""
    assert "/exec_summary" in skill_content, (
        "exec_summary/SKILL.md frontmatter must include /exec_summary as an explicit trigger"
    )
