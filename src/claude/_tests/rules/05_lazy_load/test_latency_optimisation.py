# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 5/10
# Date created:      2026-09-17
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

"""Tests for latency_optimisation.md structure and content.

Validates that the rule file exists under its correct (British-spelled)
name, its frontmatter matches, and it retains the key sections that guide
temperature-based latency tuning.
"""
from _claude_dir import CLAUDE_DIR

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


def test_frontmatter_name_matches_filename():
    """Frontmatter 'name:' field must match the file's own stem."""
    content = RULE_FILE.read_text()
    assert "name: latency_optimisation" in content, (
        "Frontmatter 'name:' field must read 'latency_optimisation', matching the filename"
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
