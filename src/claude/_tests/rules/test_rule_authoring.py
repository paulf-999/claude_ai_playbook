"""Structural tests for _rules/01_core/rule_authoring.md.

Verifies that the rule authoring guide is present, well-formed, and contains
the expected sections for pre-creation checklist and quality gates.
"""
import re
from pathlib import Path

RULE_AUTHORING = Path.home() / ".claude" / "_rules" / "01_core" / "rule_authoring.md"

EXPECTED_SECTIONS = [
    "Pre-Creation Checklist",
    "Rule Creation",
    "Quality Gates",
]

EXPECTED_PATTERNS = [
    r"Mechanical enforcement",
    r"Always-on or lazy-loaded",
    r"evidence of need",
    r"Related/conflicting rules",
]


def test_rule_authoring_file_exists():
    """rule_authoring.md must be present at the expected path."""
    assert RULE_AUTHORING.exists(), f"rule_authoring.md missing: {RULE_AUTHORING}"


def test_rule_authoring_has_expected_sections():
    """rule_authoring.md must contain all required section headings."""
    content = RULE_AUTHORING.read_text()
    for section in EXPECTED_SECTIONS:
        assert section.lower() in content.lower(), (
            f"rule_authoring.md missing expected section: '{section}'"
        )


def test_rule_authoring_contains_key_patterns():
    """rule_authoring.md must reference checklist items and quality gates."""
    content = RULE_AUTHORING.read_text()
    for pattern in EXPECTED_PATTERNS:
        assert re.search(pattern, content, re.IGNORECASE), (
            f"rule_authoring.md missing expected pattern: '{pattern}'"
        )


def test_rule_authoring_line_limit():
    """rule_authoring.md must not exceed 110 lines."""
    lines = RULE_AUTHORING.read_text().splitlines()
    assert len(lines) <= 110, f"rule_authoring.md: {len(lines)} lines exceeds 110-line limit"


def test_rule_authoring_ends_with_newline():
    """rule_authoring.md must end with exactly one newline."""
    raw = RULE_AUTHORING.read_bytes()
    assert raw.endswith(b"\n"), "rule_authoring.md does not end with a newline"
    assert not raw.endswith(b"\n\n"), "rule_authoring.md ends with multiple newlines"
