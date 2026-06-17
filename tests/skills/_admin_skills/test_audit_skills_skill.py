"""Behavioural tests for the audit_skills skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Sub-agent dispatch (skill_auditor)
- Target skills directory (~/.claude/skills/)
- Dispatch prompt completeness (read all SKILL.md before reporting)
- Both-paths fix requirement (installed + repo source)
- Phase ordering (Phase 1 before Phase 2 before Phase 3)
- Stop condition when user declines fixes
"""

from pathlib import Path

# ─── Constants ─────────────────────────────────────────────────────────────────

SUBAGENT_NAME = "skill_auditor"
SKILLS_DIR = "~/.claude/skills/"
READ_ALL_BEFORE_REPORTING = "in full before reporting"
BOTH_PATHS_PHRASE = "both"
PHASE_1_HEADING = "Phase 1"
PHASE_2_HEADING = "Phase 2"
PHASE_3_HEADING = "Phase 3"
STOP_CONDITION = "stop"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_admin_skills" / "audit_skills" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: sub-agent dispatch ─────────────────────────────────────────────────

def test_dispatches_skill_auditor_subagent() -> None:
    """SKILL.md must dispatch the skill_auditor sub-agent by name."""
    assert SUBAGENT_NAME in _skill_content(), (
        "audit_skills/SKILL.md must dispatch the skill_auditor sub-agent by name"
    )


def test_targets_correct_skills_directory() -> None:
    """SKILL.md must reference ~/.claude/skills/ as the target directory."""
    assert SKILLS_DIR in _skill_content(), (
        "audit_skills/SKILL.md must reference ~/.claude/skills/ as the target directory"
    )


# ─── Tests: dispatch prompt ────────────────────────────────────────────────────

def test_dispatch_prompt_requires_reading_all_before_reporting() -> None:
    """Dispatch prompt must instruct the sub-agent to read every SKILL.md before reporting."""
    assert READ_ALL_BEFORE_REPORTING in _skill_content(), (
        "audit_skills/SKILL.md dispatch prompt must require reading every SKILL.md "
        "in full before reporting — no partial reports"
    )


# ─── Tests: fix workflow ───────────────────────────────────────────────────────

def test_fix_applies_to_both_paths() -> None:
    """SKILL.md must require fixes applied to both installed skill and repo source."""
    content = _skill_content()
    assert BOTH_PATHS_PHRASE in content, (
        "audit_skills/SKILL.md must instruct fixes to be applied to both the installed "
        "skill and the playbook repo source file"
    )


def test_stop_on_no_answer() -> None:
    """SKILL.md must stop if the user declines the fix offer in Phase 3."""
    assert STOP_CONDITION in _skill_content().lower(), (
        "audit_skills/SKILL.md must stop execution if the user says no to applying fixes"
    )


# ─── Tests: phase ordering ─────────────────────────────────────────────────────

def test_phase_1_before_phase_2() -> None:
    """Phase 1 (audit dispatch) must appear before Phase 2 (present findings)."""
    content = _skill_content()
    p1_pos = content.find(PHASE_1_HEADING)
    p2_pos = content.find(PHASE_2_HEADING)
    assert p1_pos != -1, "audit_skills/SKILL.md must contain a Phase 1 heading"
    assert p2_pos != -1, "audit_skills/SKILL.md must contain a Phase 2 heading"
    assert p1_pos < p2_pos, (
        "audit_skills/SKILL.md must present Phase 1 before Phase 2"
    )


def test_phase_2_before_phase_3() -> None:
    """Phase 2 (present findings) must appear before Phase 3 (offer to fix)."""
    content = _skill_content()
    p2_pos = content.find(PHASE_2_HEADING)
    p3_pos = content.find(PHASE_3_HEADING)
    assert p2_pos != -1, "audit_skills/SKILL.md must contain a Phase 2 heading"
    assert p3_pos != -1, "audit_skills/SKILL.md must contain a Phase 3 heading"
    assert p2_pos < p3_pos, (
        "audit_skills/SKILL.md must present Phase 2 before Phase 3"
    )
