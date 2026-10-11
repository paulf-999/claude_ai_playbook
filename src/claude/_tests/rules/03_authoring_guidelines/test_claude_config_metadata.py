# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-28
# Date updated:      2026-10-11
# Version:           3.0.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the three-line rule metadata header defined in _claude_config_metadata.md.

Lines 1–3 must be ``<!-- version: X.Y.Z -->``, ``<!-- created: YYYY-MM-DD -->`` and
``<!-- updated: YYYY-MM-DD -->``, with ``updated`` on or after ``created``. A path-scoped rule's
``paths:`` frontmatter comes first, and the header sits straight after it.
Format cases for the shared validator live in ``_tests/test_metadata_header_format.py``.
"""
from _metadata_header import FRONTMATTER_RE, metadata_header_errors
from _shared_paths import RULES_DIR, native_rule_files

HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"


def test_every_rule_file_has_a_valid_header():
    """Every rule file must open with a valid three-line metadata header."""
    rule_files = [path for path in native_rule_files(RULES_DIR)
                  if path.name != "README.md"]
    assert rule_files, f"no rule files found under {RULES_DIR}"
    for rule_file in rule_files:
        content, name = rule_file.read_text(), rule_file.relative_to(RULES_DIR)
        frontmatter = FRONTMATTER_RE.match(content)
        offset = frontmatter.group(0).count("\n") if frontmatter else 0
        body = content[frontmatter.end():] if frontmatter else content
        assert body.startswith("<!-- version:"), f"{name}: missing metadata header after any frontmatter {HINT}"
        errors = metadata_header_errors(body, line_offset=offset)
        assert not errors, f"{name}: {errors} {HINT}"
