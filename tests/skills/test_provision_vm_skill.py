"""Behavioural tests for the provision_vm skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Phase coverage (Phase 1 workspace PR and Phase 2 VM config PR)
- /provision_vm phase2 skip path documented
- Scenario A (new workload directory) and Scenario B (existing directory)
- module "compute" deduplication rule in Scenario B
- Pre-check environment verification steps
- Error handling completeness (422, workspaces.tfvars duplicate)
- OS support (ubuntu and windows)
- Confirmation requirement before writing files or raising PRs

These tests serve as a living specification: when SKILL.md rules change, update
the constants and parametrize cases here to match.
"""

from pathlib import Path

import pytest

SKILL_DIR = (
    Path(__file__).parent.parent.parent
    / "src" / "claude" / "skills" / "_infrastructure_skills" / "provision_vm"
)

# ─── Pre-check steps ─────────────────────────────────────────────────────────────
# These must be present in the environment verification section of SKILL.md.

PRE_CHECK_STEPS = [
    "gh auth status",
    "workspaces.tfvars",
]

# ─── Error handling scenarios ─────────────────────────────────────────────────────

ERROR_SCENARIOS = [
    "422",               # gh pr create fails when a PR already exists
    "workspaces.tfvars", # duplicate workspace entry already present
]

# ─── OS types ─────────────────────────────────────────────────────────────────────

SUPPORTED_OS = ["ubuntu", "windows"]


def _skill_content() -> str:
    """Read SKILL.md content.

    :return: Full file content as a string.
    :rtype: str
    """
    return (SKILL_DIR / "SKILL.md").read_text()


def _phase2_content() -> str:
    """Read phase2.md content.

    :return: Full file content as a string.
    :rtype: str
    """
    return (SKILL_DIR / "phase2.md").read_text()


def _parameters_content() -> str:
    """Read parameters.md content.

    :return: Full file content as a string.
    :rtype: str
    """
    return (SKILL_DIR / "parameters.md").read_text()


# ─── Tests: phases ───────────────────────────────────────────────────────────────

def test_phase1_referenced() -> None:
    """Phase 1 (workspace PR) must be referenced in SKILL.md."""
    assert "Phase 1" in _skill_content(), (
        "SKILL.md must reference Phase 1 — workspace PR"
    )


def test_phase2_referenced() -> None:
    """Phase 2 (VM config PR) must be referenced in SKILL.md."""
    assert "Phase 2" in _skill_content(), (
        "SKILL.md must reference Phase 2 — VM config PR"
    )


# ─── Tests: phase2 skip path ─────────────────────────────────────────────────────

def test_phase2_skip_documented() -> None:
    """The /provision_vm phase2 invocation path must be documented in SKILL.md."""
    assert "phase2" in _skill_content(), (
        "SKILL.md must document the /provision_vm phase2 skip path"
    )


# ─── Tests: scenario handling ─────────────────────────────────────────────────────

def test_scenario_a_described() -> None:
    """Scenario A (new workload directory) must be described in phase2.md."""
    assert "Scenario A" in _phase2_content(), (
        "phase2.md must describe Scenario A — new workload directory"
    )


def test_scenario_b_described() -> None:
    """Scenario B (existing workload directory) must be described in phase2.md."""
    assert "Scenario B" in _phase2_content(), (
        "phase2.md must describe Scenario B — adding to an existing workload directory"
    )


def test_module_compute_deduplication_rule() -> None:
    """Scenario B must document the rule to omit duplicate module 'compute' blocks."""
    assert 'module "compute"' in _phase2_content(), (
        "phase2.md must document that only one module 'compute' block is allowed per directory"
    )


# ─── Tests: pre-check ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("step", PRE_CHECK_STEPS)
def test_precheck_step_present(step: str) -> None:
    """Key pre-check environment verification steps must be present in SKILL.md.

    :param step: Step keyword to assert is present.
    :type step: str
    """
    assert step in _skill_content(), (
        f"SKILL.md must include '{step}' as a pre-check verification step"
    )


# ─── Tests: error handling ───────────────────────────────────────────────────────

@pytest.mark.parametrize("scenario", ERROR_SCENARIOS)
def test_error_scenario_handled(scenario: str) -> None:
    """Key error scenarios must be covered in the error handling section.

    :param scenario: Error scenario keyword to assert is present.
    :type scenario: str
    """
    assert scenario in _skill_content(), (
        f"SKILL.md error handling must cover the scenario containing '{scenario}'"
    )


# ─── Tests: OS support ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("os_type", SUPPORTED_OS)
def test_os_type_documented(os_type: str) -> None:
    """Both ubuntu and windows OS types must be documented in parameters.md.

    :param os_type: OS type to assert is documented.
    :type os_type: str
    """
    assert os_type in _parameters_content(), (
        f"parameters.md must document '{os_type}' as a supported OS type"
    )


# ─── Tests: confirmation requirement ─────────────────────────────────────────────

def test_confirmation_required_before_writing() -> None:
    """Skill must require explicit confirmation before writing files or raising PRs."""
    content = _skill_content()
    assert "confirmation" in content.lower() or "wait for" in content.lower(), (
        "SKILL.md must require explicit confirmation before writing files or raising PRs"
    )
