"""
Test writing_style.md behavioral rules and documentation completeness.

Goals:
- Validates rule documentation is complete (examples, counter-examples)
- Spot-checks that table rule is correctly formulated
- Prepares for quarterly behavioral audits of applied tables in docs/skills

Quarterly behavioral audit (manual):
- Review recent skill/doc files for correct table application
- Check: when 2+ categories with identical structure exist, tables are used
- Check: single lists with no categorical breakout stay as bullets
- Run: pytest test_writing_style_behavior.py to verify rule documentation
- Cadence: Quarterly (per guiding_principles.md reset cycles)
"""

import pytest
from pathlib import Path


def test_writing_style_tables_rule_exists():
    """Tables rule is documented in writing_style.md."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    assert rule_file.exists(), f"writing_style.md not found at {rule_file}"

    content = rule_file.read_text()
    assert "Tables for structured content" in content, "Tables rule not documented"


def test_writing_style_tables_rule_defines_threshold():
    """Tables rule defines threshold: 'two or more categories'."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()

    # Should define threshold explicitly
    assert "two or more categories" in content, (
        "Rule should define threshold as 'two or more categories' — "
        "clarifies when tables apply vs. stay as bullets"
    )


def test_writing_style_tables_rule_defines_structure():
    """Tables rule defines structure: 'identical column structures'."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()

    # Should define what "identical structure" means
    assert "identical column structures" in content, (
        "Rule should clarify structure requirement — "
        "what does 'similar' mean? Answer: identical column structures"
    )


def test_writing_style_tables_rule_has_signal():
    """Tables rule includes a 'Signal' section that explains the pattern."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()

    # Should have clear signal for when to apply the rule
    assert "**Signal:**" in content, (
        "Rule should include a Signal section explaining when the pattern triggers "
        "(you're writing **Category A:** then **Category B:**)"
    )
    assert "**Category A:**" in content, (
        "Signal should include example category naming pattern"
    )


def test_writing_style_tables_rule_has_example():
    """Tables rule includes a concrete Example."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()

    assert "**Example:**" in content, (
        "Rule should include a concrete Example showing table usage"
    )
    assert "Can do" in content and "Can't do" in content, (
        "Example should illustrate 2-column table use case"
    )


def test_writing_style_tables_rule_has_counter_example():
    """Tables rule includes a Counter-example showing boundary case."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()

    assert "**Counter-example:**" in content, (
        "Rule should include a Counter-example clarifying when NOT to use tables — "
        "e.g., single capabilities list with no categorical breakout"
    )
    assert "single capabilities list" in content or "no categorical breakout" in content, (
        "Counter-example should clarify the boundary: "
        "tables only when there's a comparison dimension"
    )


def test_writing_style_file_structure():
    """writing_style.md follows format constraints."""
    rule_file = Path.home() / ".claude" / "_rules" / "01_essentials" / "conventions" / "writing_style.md"
    content = rule_file.read_text()
    lines = content.split('\n')

    # Check line count
    assert len(lines) <= 110, f"writing_style.md exceeds 110 lines ({len(lines)}). Split into parent + children if needed."

    # Check trailing newline
    assert content.endswith('\n'), "File must end with trailing newline"

    # Check emoji headers
    assert content.count('# ✏️') >= 1, "Main heading should have emoji"
    assert content.count('## 🎨') >= 1, "Section headings should have emojis"
