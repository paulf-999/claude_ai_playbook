"""Behavioural tests for the ansible_playbook_creation skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Pre-check completeness (all 6 required items before proceeding)
- Confirmation requirement before writing files
- Validation commands (ansible-lint and yamllint)
- Pattern guide references
- End-of-workflow create_pr step

These tests serve as a living specification: when SKILL.md rules change, update
the constants and parametrize cases here to match.
"""

from pathlib import Path

import pytest

SKILL_DIR = (
    Path(__file__).parent.parent.parent
    / "src" / "claude" / "skills" / "_infrastructure_skills" / "ansible_playbook_creation"
)

# ─── Pre-check items ──────────────────────────────────────────────────────────────
# All six must be established before design or implementation begins.

PRE_CHECK_ITEMS = ["Scope", "Target", "Application", "Dependencies", "Secrets", "DC3"]

# ─── Pattern guides ───────────────────────────────────────────────────────────────

PATTERN_GUIDES = [
    "patterns_security.md",
    "patterns_tasks.md",
    "patterns_structure.md",
]

# ─── Validation tools ─────────────────────────────────────────────────────────────

VALIDATION_TOOLS = ["ansible-lint", "yamllint"]


def _skill_content() -> str:
    """Read SKILL.md content.

    :return: Full file content as a string.
    :rtype: str
    """
    return (SKILL_DIR / "SKILL.md").read_text()


# ─── Tests: pre-check completeness ───────────────────────────────────────────────

@pytest.mark.parametrize("item", PRE_CHECK_ITEMS)
def test_precheck_item_present(item: str) -> None:
    """All 6 pre-check items must be required by the skill before proceeding.

    :param item: Pre-check item name to assert is present.
    :type item: str
    """
    assert item in _skill_content(), (
        f"SKILL.md must require '{item}' as a pre-check item before design begins"
    )


# ─── Tests: confirmation requirement ─────────────────────────────────────────────

def test_confirmation_required_before_writing() -> None:
    """Skill must require explicit confirmation before writing any file."""
    content = _skill_content()
    assert "wait for confirmation" in content.lower() or "confirmation" in content.lower(), (
        "SKILL.md must require explicit confirmation before writing files"
    )


# ─── Tests: validation tools ─────────────────────────────────────────────────────

@pytest.mark.parametrize("tool", VALIDATION_TOOLS)
def test_validation_tool_present(tool: str) -> None:
    """Both ansible-lint and yamllint must be referenced in the validation phase.

    :param tool: Tool name to assert is present.
    :type tool: str
    """
    assert tool in _skill_content(), (
        f"SKILL.md must reference '{tool}' in the validation phase"
    )


# ─── Tests: pattern guide references ─────────────────────────────────────────────

@pytest.mark.parametrize("guide", PATTERN_GUIDES)
def test_pattern_guide_referenced(guide: str) -> None:
    """All three pattern guides must be referenced in the skill.

    :param guide: Pattern guide filename to assert is referenced.
    :type guide: str
    """
    assert guide in _skill_content(), (
        f"SKILL.md must reference pattern guide '{guide}'"
    )


# ─── Tests: end-of-workflow step ─────────────────────────────────────────────────

def test_create_pr_invoked_at_end() -> None:
    """Skill must invoke /create_pr as the final step after validation passes."""
    assert "/create_pr" in _skill_content(), (
        "SKILL.md must invoke /create_pr as the final step of the validation phase"
    )
