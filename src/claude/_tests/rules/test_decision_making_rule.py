"""Structural tests for _rules/01_core/behaviour/_decision_making.md.

Verifies that the decision-making rule is present, well-formed, and contains
the expected section headings and patterns that establish the intentionality gate.
"""
import re
from pathlib import Path

DECISION_MAKING_RULE = Path.home() / ".claude" / "_rules" / "01_core" / "behaviour" / "_decision_making.md"

EXPECTED_SECTIONS = [
    "Core principle",
    "When to present options",
    "When NOT to present options",
    "Format & tool use",
    "Examples",
]

EXPECTED_PATTERNS = [
    r"AskUserQuestion",
    r"2–3 options",
    r"one explicitly recommended",
    r"intentionality",
]


def test_decision_making_rule_file_exists():
    """decision_making.md must be present at the expected path."""
    assert DECISION_MAKING_RULE.exists(), f"decision_making.md missing: {DECISION_MAKING_RULE}"


def test_decision_making_rule_has_expected_sections():
    """decision_making.md must contain all required section headings."""
    content = DECISION_MAKING_RULE.read_text()
    for section in EXPECTED_SECTIONS:
        assert section.lower() in content.lower(), (
            f"decision_making.md missing expected section: '{section}'"
        )


def test_decision_making_rule_contains_key_patterns():
    """decision_making.md must reference AskUserQuestion, option count, recommendation, and intentionality."""
    content = DECISION_MAKING_RULE.read_text()
    for pattern in EXPECTED_PATTERNS:
        assert re.search(pattern, content, re.IGNORECASE), (
            f"decision_making.md missing expected pattern: '{pattern}'"
        )


def test_decision_making_rule_line_limit():
    """decision_making.md must not exceed 110 lines."""
    lines = DECISION_MAKING_RULE.read_text().splitlines()
    assert len(lines) <= 110, f"decision_making.md: {len(lines)} lines exceeds 110-line limit"


def test_decision_making_rule_ends_with_newline():
    """decision_making.md must end with exactly one newline."""
    raw = DECISION_MAKING_RULE.read_bytes()
    assert raw.endswith(b"\n"), "decision_making.md does not end with a newline"
    assert not raw.endswith(b"\n\n"), "decision_making.md ends with multiple newlines"
