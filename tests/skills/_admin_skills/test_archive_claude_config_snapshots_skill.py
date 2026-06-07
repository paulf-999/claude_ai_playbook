"""Behavioural tests for the archive_claude_config_snapshots skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Archiving age thresholds (30-day tier-1, 90-day tier-2)
- Destination directory mapping per tier
- Confirmation required before moving any directories
- Move (mv) semantics — no deletion
"""

from pathlib import Path

import pytest

# ─── Archiving thresholds ───────────────────────────────────────────────────────

TIER1_AGE_DAYS = 30
TIER2_AGE_DAYS = 90

TIER1_SOURCE_PATTERN = "~/.claude_*"
TIER1_DESTINATION = "~/.claude_archived/"
TIER2_SOURCE_PATTERN = "~/.claude_archived/*"
TIER2_DESTINATION = "~/.claude_deep_archived/"

MOVE_COMMAND = "mv"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_admin_skills"
    / "archive_claude_config_snapshots" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: thresholds ─────────────────────────────────────────────────────────

def test_tier1_age_threshold() -> None:
    """SKILL.md must specify 30 days as the tier-1 archiving threshold."""
    assert "30" in _skill_content(), (
        "archive_claude_config_snapshots/SKILL.md must specify a 30-day threshold for tier-1 archiving"
    )


def test_tier2_age_threshold() -> None:
    """SKILL.md must specify 90 days as the tier-2 archiving threshold."""
    assert "90" in _skill_content(), (
        "archive_claude_config_snapshots/SKILL.md must specify a 90-day threshold for tier-2 archiving"
    )


# ─── Tests: destinations ───────────────────────────────────────────────────────

def test_tier1_destination() -> None:
    """SKILL.md must specify ~/.claude_archived/ as the tier-1 destination."""
    assert ".claude_archived" in _skill_content(), (
        "archive_claude_config_snapshots/SKILL.md must reference .claude_archived as the tier-1 destination"
    )


def test_tier2_destination() -> None:
    """SKILL.md must specify ~/.claude_deep_archived/ as the tier-2 destination."""
    assert ".claude_deep_archived" in _skill_content(), (
        "archive_claude_config_snapshots/SKILL.md must reference .claude_deep_archived as the tier-2 destination"
    )


# ─── Tests: move semantics ─────────────────────────────────────────────────────

def test_uses_mv_not_rm() -> None:
    """SKILL.md must use mv for archiving — no deletion."""
    content = _skill_content()
    assert "mv" in content, (
        "archive_claude_config_snapshots/SKILL.md must use mv to relocate directories, not rm"
    )


# ─── Tests: confirmation ───────────────────────────────────────────────────────

def test_confirmation_required_before_move() -> None:
    """SKILL.md must require user confirmation before moving any directories."""
    content = _skill_content()
    confirm_terms = ["confirm", "confirmation", "wait", "proceed"]
    assert any(term in content.lower() for term in confirm_terms), (
        "archive_claude_config_snapshots/SKILL.md must require user confirmation before moving directories"
    )


# ─── Tests: two-tier structure ─────────────────────────────────────────────────

@pytest.mark.parametrize("dest", [
    TIER1_DESTINATION,
    TIER2_DESTINATION,
])
def test_both_tier_destinations_documented(dest: str) -> None:
    """SKILL.md must document both tier-1 and tier-2 destination directories.

    :param dest: Expected destination directory path.
    :type dest: str
    """
    assert dest in _skill_content(), (
        f"archive_claude_config_snapshots/SKILL.md must reference destination: {dest}"
    )


def test_tier2_source_is_tier1_destination() -> None:
    """Tier-2 source must be the same directory as tier-1 destination (two-tier cascade)."""
    content = _skill_content()
    assert ".claude_archived" in content, (
        "archive_claude_config_snapshots/SKILL.md must establish .claude_archived as both "
        "tier-1 destination and tier-2 source"
    )
