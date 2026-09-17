# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 8/10
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

"""Tests for plan-mode phase approval gates in _multi_phase_implementation_gates.md.

Verifies that the expanded rule includes mandatory plan-mode phase gates with
clear examples and blocking requirements.
"""
import re

from _claude_dir import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "02_claude_standards" / "behaviour" / "_multi_phase_implementation_gates.md"

EXPECTED_SECTIONS = [
    "Plan-Mode Phase Gates",
    "MANDATORY",
    "Why plans require gates",
]

EXPECTED_PATTERNS = [
    r"Phase gates are MANDATORY",
    r"explicit approval between phases",
    r"Do NOT proceed automatically",
    r"Audit plan",
    r"Feature plan",
    r"Infrastructure plan",
    r"BLOCKING",
]

PLAN_MODE_MARKER = "## 🗂️ Plan-Mode Phase Gates (MANDATORY)"


def test_plan_mode_gates_section_exists():
    """Rule must include plan-mode phase gates section."""
    content = RULE_FILE.read_text()
    assert PLAN_MODE_MARKER in content, (
        f"Rule missing plan-mode gates section. Expected: '{PLAN_MODE_MARKER}'"
    )


def test_plan_mode_gates_has_expected_sections():
    """Plan-mode section must contain all required subsections."""
    content = RULE_FILE.read_text()
    for section in EXPECTED_SECTIONS:
        assert section.lower() in content.lower(), (
            f"Plan-mode section missing: '{section}'"
        )


def test_plan_mode_gates_contains_mandatory_language():
    """Rule must emphasize that gates are MANDATORY, not optional."""
    content = RULE_FILE.read_text()
    assert re.search(r"MANDATORY.*plan mode", content, re.IGNORECASE), (
        "Rule must explicitly state gates are MANDATORY in plan mode"
    )
    assert re.search(r"non-negotiable", content, re.IGNORECASE), (
        "Rule must use 'non-negotiable' to reinforce mandatory nature"
    )


def test_plan_mode_gates_contains_key_patterns():
    """Rule must reference explicit approval, blocking behavior, and plan types."""
    content = RULE_FILE.read_text()
    for pattern in EXPECTED_PATTERNS:
        assert re.search(pattern, content, re.IGNORECASE), (
            f"Rule missing expected pattern: '{pattern}'"
        )


def test_plan_mode_gates_has_execution_format():
    """Rule must define the format for phase completion + approval request."""
    content = RULE_FILE.read_text()
    assert "✅ Phase N:" in content or "Phase N:" in content, (
        "Rule must show execution format with Phase N marker"
    )
    assert "Proceed?" in content or "proceed?" in content, (
        "Rule must show explicit approval question format"
    )


def test_plan_mode_gates_includes_plan_type_examples():
    """Rule must include examples for different plan types (audit, feature, infrastructure)."""
    content = RULE_FILE.read_text()
    plan_types = ["Audit plan", "Feature plan", "Infrastructure plan"]
    for plan_type in plan_types:
        assert plan_type in content, (
            f"Rule must include example for: {plan_type}"
        )


def test_plan_mode_gates_emphasizes_no_auto_proceed():
    """Rule must explicitly state Claude should NOT auto-proceed to next phase."""
    content = RULE_FILE.read_text()
    assert re.search(r"Do NOT proceed automatically", content, re.IGNORECASE), (
        "Rule must explicitly forbid automatic progression to next phase"
    )
    assert re.search(r"Wait for explicit.*response", content, re.IGNORECASE), (
        "Rule must state to wait for explicit user response"
    )


def test_rule_line_limit():
    """Rule must not exceed 200 lines (expanded from 96 to accommodate plan-mode gates)."""
    lines = RULE_FILE.read_text().splitlines()
    assert len(lines) <= 200, (
        f"Rule exceeds 200 lines ({len(lines)}). Split into parent + child if needed."
    )


def test_rule_ends_with_newline():
    """Rule must end with exactly one newline."""
    raw = RULE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "Rule does not end with a newline"
    assert not raw.endswith(b"\n\n"), "Rule ends with multiple newlines"
