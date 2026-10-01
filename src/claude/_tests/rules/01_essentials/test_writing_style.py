# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           1.1.1
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

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
- Run: pytest test_writing_style.py to verify rule documentation
- Cadence: Quarterly (per guiding_principles.md reset cycles)
"""


from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "01_essentials" / "claude_usage_standards" / "writing_style.md"


def test_writing_style_tables_rule_exists():
    """Tables rule is documented in writing_style.md."""
    assert RULE_FILE.exists(), f"writing_style.md not found at {RULE_FILE}"

    content = RULE_FILE.read_text()
    assert "Tables for structured content" in content, "Tables rule not documented"


def test_writing_style_tables_rule_defines_threshold():
    """Tables rule defines threshold: 'two or more categories'."""
    content = RULE_FILE.read_text()

    # Should define threshold explicitly
    assert "two or more categories" in content, (
        "Rule should define threshold as 'two or more categories' — "
        "clarifies when tables apply vs. stay as bullets"
    )


def test_writing_style_tables_rule_defines_structure():
    """Tables rule defines structure: 'identical column structures'."""
    content = RULE_FILE.read_text()

    # Should define what "identical structure" means
    assert "identical column structures" in content, (
        "Rule should clarify structure requirement — "
        "what does 'similar' mean? Answer: identical column structures"
    )


def test_writing_style_tables_rule_has_signal():
    """Tables rule includes a 'Signal' section that explains the pattern."""
    content = RULE_FILE.read_text()

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
    content = RULE_FILE.read_text()

    assert "**Example:**" in content, (
        "Rule should include a concrete Example showing table usage"
    )
    assert "Can do" in content and "Can't do" in content, (
        "Example should illustrate 2-column table use case"
    )


def test_writing_style_tables_rule_has_counter_example():
    """Tables rule includes a Counter-example showing boundary case."""
    content = RULE_FILE.read_text()

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
    content = RULE_FILE.read_text()
    lines = content.split('\n')

    # Check line count
    assert len(lines) <= 110, (
        f"writing_style.md exceeds 110 lines ({len(lines)}). Split into parent + children if needed."
    )

    # Check trailing newline
    assert content.endswith('\n'), "File must end with trailing newline"

    # Check emoji headers
    assert content.count('# ✏️') >= 1, "Main heading should have emoji"
    assert content.count('## 🎨') >= 1, "Section headings should have emojis"


def test_writing_style_one_sentence_per_bullet():
    """The one-sentence-per-bullet rule survives, with child bullets as the fix."""
    content = RULE_FILE.read_text()
    assert "**One sentence per bullet:**" in content, "the one-sentence-per-bullet rule is missing"
    assert "use child bullets" in content, "the rule should say to use child bullets instead"


def test_writing_style_british_spelling():
    """British spelling is the house style, with code identifiers exempt."""
    content = RULE_FILE.read_text()
    assert "**British English spelling:**" in content, "the British spelling rule is missing"
    assert "code identifiers, filenames, and function names" in content, (
        "the exemption for existing code identifiers is missing"
    )


def test_writing_style_dated_paths_use_underscores():
    """Draft and error file names use YYYY_MM_DD, never hyphenated dates."""
    content = RULE_FILE.read_text()
    assert "`~/_drafts/<domain>/YYYY_MM_DD_<topic>.md`" in content, "the drafts path format changed"
    assert "`~/_errors/<domain>/YYYY_MM_DD_<topic>.md`" in content, "the errors path format changed"
    assert "YYYY-MM-DD_" not in content, "a hyphenated date prefix crept back into a file-name pattern"


def test_writing_style_imports_multifile_child():
    """The multifile-organisation rule is imported and exists."""
    content = RULE_FILE.read_text()
    child = RULE_FILE.parent / "multifile_document_organisation.md"
    assert "/claude_usage_standards/multifile_document_organisation.md" in content, "the multifile import is missing"
    assert child.is_file(), f"the imported child is missing: {child}"
