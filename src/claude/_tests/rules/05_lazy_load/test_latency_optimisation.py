# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-17
# Date updated:      2026-10-01
# Version:           1.0.2
# Test quality score: 5/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for latency_optimisation.md structure and content.

Validates that the rule file exists under its correct (British-spelled)
name, its frontmatter matches, and it retains the key sections that guide
temperature-based latency tuning.
"""
from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "05_lazy_load" / "latency_optimisation.md"

EXPECTED_SECTIONS = [
    "When latency matters",
    "Temperature as a conciseness lever",
    "How to apply",
    "Constraint: measure before optimizing",
]


def test_rule_file_exists_with_british_spelling():
    """File must exist as latency_optimisation.md, not the old American spelling."""
    assert RULE_FILE.exists(), (
        f"Expected {RULE_FILE} to exist — file may still be at the old "
        "American-spelled name (latency_optimization.md)"
    )
    old_name = RULE_FILE.parent / "latency_optimization.md"
    assert not old_name.exists(), (
        f"Old American-spelled file still present at {old_name} — should have been renamed"
    )


def test_no_stray_memory_frontmatter():
    """Rule files must not carry memory-schema YAML frontmatter (name/description/metadata).

    Regression test: this file previously opened with a `---`-delimited
    block matching the personal-memory-file schema (name, description,
    metadata: type), left over from an earlier migration. No other file
    under _rules/ has this — rule files start directly with an emoji H1.
    """
    content = RULE_FILE.read_text()
    assert not content.startswith("---\n"), (
        "latency_optimisation.md starts with a YAML frontmatter block — "
        "rule files should open directly with an emoji H1, not memory-schema frontmatter"
    )


def test_has_expected_sections():
    """Rule must retain all key sections guiding latency/temperature decisions."""
    content = RULE_FILE.read_text()
    for section in EXPECTED_SECTIONS:
        assert section in content, f"Rule missing expected section: '{section}'"


def test_ends_with_single_newline():
    """Rule must end with exactly one newline."""
    raw = RULE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "Rule does not end with a newline"
    assert not raw.endswith(b"\n\n"), "Rule ends with multiple trailing newlines"
