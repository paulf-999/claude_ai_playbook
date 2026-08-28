"""Tests for automation_controls.md — validates experimental feature guards.

Ensures:
- Turn budgets are defined (default: 10 for /loop, 20 for /goal)
- Minimum intervals are specified (≥5m for loops)
- Controls are documented and enforceable
- Aliases reference documented controls
"""
import re
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
AUTOMATION_CONTROLS_FILE = CLAUDE_DIR / "_rules/claude_internal/automation_controls.md"
ALIASES_FILE = CLAUDE_DIR / "aliases.md"


def _read_automation_controls():
    """Read automation_controls.md."""
    return AUTOMATION_CONTROLS_FILE.read_text()


def _read_aliases():
    """Read aliases.md."""
    return ALIASES_FILE.read_text()


def test_automation_controls_file_exists():
    """automation_controls.md must exist."""
    assert AUTOMATION_CONTROLS_FILE.exists(), (
        f"automation_controls.md not found at {AUTOMATION_CONTROLS_FILE}"
    )


def test_loop_controls_documented():
    """Loop controls must include turn budget and interval minimum."""
    content = _read_automation_controls()

    # Check for turn budget documentation
    assert "or stop after 10 turns" in content or "10 turns" in content, (
        "automation_controls.md must document default turn budget for /loop (10 turns)"
    )

    # Check for interval minimum
    assert "5-minute interval" in content or "5 minute" in content.lower(), (
        "automation_controls.md must document minimum interval for /loop (5 minutes)"
    )

    # Check that sub-minute loops are discouraged
    assert "sub-minute" in content.lower(), (
        "automation_controls.md should warn against sub-minute loops"
    )


def test_goal_controls_documented():
    """Goal controls must include turn budget and mode requirement."""
    content = _read_automation_controls()

    # Check for turn budget documentation
    assert "or stop after 20 turns" in content or ("20 turns" in content and "/goal" in content), (
        "automation_controls.md must document default turn budget for /goal (20 turns)"
    )

    # Check that auto mode is recommended
    assert "auto mode" in content.lower(), (
        "automation_controls.md should recommend pairing /goal with auto mode"
    )


def test_batch_controls_documented():
    """Batch controls must include independence requirement and approval gate."""
    content = _read_automation_controls()

    # Check for independence requirement
    assert "independent" in content.lower() or "independent units" in content.lower(), (
        "automation_controls.md must document independent units requirement for /batch"
    )

    # Check for approval gate
    assert "approve" in content.lower(), (
        "automation_controls.md must document approval gate before /batch execution"
    )


def test_experimental_features_labeled():
    """All three experimental features must be labeled as experimental."""
    content = _read_automation_controls()

    experimental_features = ["/loop", "/batch", "/goal"]
    for feature in experimental_features:
        assert f"{feature}" in content, f"{feature} not documented in automation_controls.md"

    # Check that experimental warning is present
    assert "experimental" in content.lower(), (
        "automation_controls.md should label features as experimental"
    )


def test_kill_switch_procedure_documented():
    """Kill-switch procedure for disabling features must be documented."""
    content = _read_automation_controls()

    # Check for kill-switch section
    assert "kill" in content.lower() or "disable" in content.lower(), (
        "automation_controls.md should document how to disable features"
    )

    # Check for recovery procedure
    assert "recovery" in content.lower() or "re-enable" in content.lower(), (
        "automation_controls.md should document recovery procedure for re-enabling"
    )


def test_aliases_reference_automation_controls():
    """Aliases for experimental features must reference automation_controls.md."""
    aliases_content = _read_aliases()

    # Check that /loop, /batch, /goal are documented in aliases
    experimental_features = ["/loop", "/batch", "/goal"]
    for feature in experimental_features:
        assert feature in aliases_content, (
            f"Alias file missing documentation for {feature}"
        )

    # Check that /batch and /goal reference automation_controls in aliases
    # (per the "Note on automation controls" section in aliases.md)
    assert "automation_controls" in aliases_content.lower(), (
        "aliases.md should reference automation_controls.md for experimental features"
    )


def test_turn_budget_defaults_reasonable():
    """Turn budgets should be reasonable and documented."""
    content = _read_automation_controls()

    # Extract turn budget numbers
    turn_budgets = re.findall(r"(\d+)\s+turns?", content, re.IGNORECASE)
    assert len(turn_budgets) >= 2, (
        "automation_controls.md should document at least 2 turn budgets (/loop, /goal)"
    )

    # Convert to integers and check they're reasonable (between 5 and 100)
    budgets = [int(b) for b in turn_budgets]
    assert all(5 <= b <= 100 for b in budgets), (
        f"Turn budgets {budgets} appear unreasonable (should be 5-100)"
    )


def test_feature_independence_principle():
    """Batch feature controls must emphasize independent units."""
    content = _read_automation_controls()

    # Find /batch section
    batch_section = content.split("## 📦 /batch usage")[1].split("##")[0] if "## 📦 /batch usage" in content else ""

    if batch_section:
        assert "independent" in batch_section.lower(), (
            "/batch controls must emphasize independent units to avoid conflicts"
        )

        assert "cross-unit dependencies" in batch_section.lower() or "dependencies" in batch_section.lower(), (
            "/batch controls should warn against cross-unit dependencies"
        )


def test_goal_verifiable_condition_requirement():
    """Goal feature must require verifiable conditions."""
    content = _read_automation_controls()

    # Find /goal section
    goal_section = content.split("## 🎯 /goal usage")[1].split("##")[0] if "## 🎯 /goal usage" in content else ""

    if goal_section:
        assert "verifiable" in goal_section.lower() or "testable" in goal_section.lower(), (
            "/goal controls must require verifiable/testable conditions"
        )

        assert "tests pass" in goal_section.lower() or "example" in goal_section.lower(), (
            "/goal controls should provide example verifiable conditions"
        )
