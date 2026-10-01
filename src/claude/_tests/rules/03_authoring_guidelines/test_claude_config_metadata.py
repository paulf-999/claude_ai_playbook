# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-28
# Date updated:      2026-10-01
# Version:           2.2.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the three-line rule metadata header defined in _claude_config_metadata.md.

Lines 1–3 must be ``<!-- version: X.Y.Z -->``, ``<!-- created: YYYY-MM-DD -->`` and
``<!-- updated: YYYY-MM-DD -->``, with ``updated`` on or after ``created``. A path-scoped rule's
``paths:`` frontmatter comes first, and the header sits straight after it.
"""
from _metadata_header import FRONTMATTER_RE, metadata_header_errors
from _shared_paths import RULES_DIR

# Non-rule content under _rules/: a skill-managed tally
EXCLUDED_DIRS = {"learned"}

HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"

VALID_HEADER = "<!-- version: 1.2.10 -->\n<!-- created: 2026-09-01 -->\n<!-- updated: 2026-09-28 -->"


def with_header(**overrides: str) -> str:
    """Build a minimal rule file whose header uses defaults plus any overridden fields.

    :param overrides: Replacement values keyed by ``version``, ``created`` or ``updated``.
    :type overrides: str
    :return: Rule file content.
    :rtype: str
    """
    fields = {"version": "1.0.0", "created": "2026-09-28", "updated": "2026-09-28"} | overrides
    header = "".join(f"<!-- {field}: {value} -->\n" for field, value in fields.items())
    return f"{header}# 🗂️ Example rule\n\n**Purpose:** Example.\n"


# --- Accepted ---

def test_valid_header_accepted():
    """A well-formed header on lines 1–3 produces no errors."""
    assert metadata_header_errors(f"{VALID_HEADER}\n# 🗂️ Rule\n") == [], "valid header was rejected"


def test_same_day_created_and_updated_accepted():
    """A new rule has created == updated, which must be allowed."""
    assert metadata_header_errors(with_header()) == [], "same-day dates were rejected"


def test_zero_components_accepted():
    """Zero is a valid semver component (e.g. 0.1.0, 1.0.0)."""
    for version in ("0.1.0", "1.0.0", "0.0.1"):
        assert metadata_header_errors(with_header(version=version)) == [], f"{version} was rejected"


def test_header_after_paths_frontmatter_accepted():
    """A path-scoped rule keeps its header straight after the ``paths:`` frontmatter."""
    content = f'---\npaths:\n  - "**/*.sql"\n---\n{VALID_HEADER}\n# 🗂️ Rule\n'
    frontmatter = FRONTMATTER_RE.match(content)
    assert frontmatter, "paths frontmatter was not recognised"
    body = content[frontmatter.end():]
    assert metadata_header_errors(body, line_offset=4) == [], "header after frontmatter was rejected"


def test_headerless_file_has_no_format_errors():
    """The format validator ignores absent headers; presence is checked by the real-file test."""
    assert metadata_header_errors("# 🗂️ Rule without header\n") == [], "header-less file was flagged"
    assert metadata_header_errors("") == [], "empty file was flagged"


# --- Rejected: placement ---

def test_misplaced_header_rejected():
    """A header below the H1 is rejected with a lines-1–3 message."""
    errors = metadata_header_errors(f"# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "header below the H1 was accepted"
    assert "lines 1–3" in errors[0], f"unexpected error text: {errors}"


def test_duplicate_header_rejected():
    """A second header later in the file is rejected even if lines 1–3 are valid."""
    errors = metadata_header_errors(f"{VALID_HEADER}\n# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "duplicate header was accepted"
    assert "[1, 2, 3, 5, 6, 7]" in errors[0], f"error should name every header line: {errors}"


def test_header_example_in_code_block_ignored():
    """Header-shaped lines inside a fenced code block are examples, not a second header."""
    content = with_header() + f"\n```markdown\n{VALID_HEADER}\n```\n"
    assert metadata_header_errors(content) == [], "code-block example was treated as a header"
    only_in_block = f"# 🗂️ Rule\n```\n{VALID_HEADER}\n```\n"
    assert metadata_header_errors(only_in_block) == [], "code-block-only header should count as absent"


def test_missing_field_rejected():
    """All three lines are required."""
    two_lines = "<!-- version: 1.0.0 -->\n<!-- created: 2026-09-28 -->\n# 🗂️ Rule\n"
    errors = metadata_header_errors(two_lines)
    assert errors, "two-line header was accepted"
    assert "lines 1–3" in errors[0], f"unexpected error text: {errors}"


def test_reordered_fields_rejected():
    """Fields must appear in version → created → updated order."""
    reordered = "<!-- created: 2026-09-28 -->\n<!-- version: 1.0.0 -->\n<!-- updated: 2026-09-28 -->\n"
    errors = metadata_header_errors(reordered)
    assert errors, "reordered fields were accepted"
    assert "version line" in errors[0], f"unexpected error text: {errors}"


def test_old_single_line_format_rejected():
    """The superseded one-line format is no longer valid."""
    old = "<!-- version: 1.0.0 | created: 2026-09-28 | updated: 2026-09-28 -->\n# 🗂️ Rule\n"
    assert metadata_header_errors(old), "one-line header was accepted"


# --- Rejected: format ---

def test_malformed_semver_rejected():
    """Versions that aren't exactly MAJOR.MINOR.PATCH (no leading zeros) are rejected."""
    for version in ("1.0", "1.0.0.0", "v1.0.0", "1.0.x", "01.0.0"):
        assert metadata_header_errors(with_header(version=version)), f"version {version!r} was accepted"


def test_non_iso_date_format_rejected():
    """Dates must use hyphens (YYYY-MM-DD), not the underscore filename convention."""
    errors = metadata_header_errors(with_header(created="2026_09_28"))
    assert errors, "underscore date was accepted"
    assert "created line does not match format" in errors[0], f"unexpected error text: {errors}"


# --- Rejected: values ---

def test_impossible_date_rejected():
    """A correctly shaped but non-existent date is rejected."""
    errors = metadata_header_errors(with_header(created="2026-02-30"))
    assert errors, "2026-02-30 was accepted"
    assert "invalid date" in errors[0], f"unexpected error text: {errors}"


def test_updated_before_created_rejected():
    """updated must be on or after created."""
    errors = metadata_header_errors(with_header(updated="2026-09-01"))
    assert errors, "updated-before-created was accepted"
    assert "earlier than created" in errors[0], f"unexpected error text: {errors}"


# --- Real files ---

def test_every_rule_file_has_a_valid_header():
    """Every rule file must open with a valid three-line metadata header."""
    rule_files = [path for path in RULES_DIR.rglob("*.md")
                  if path.name != "README.md" and path.relative_to(RULES_DIR).parts[0] not in EXCLUDED_DIRS]
    assert rule_files, f"no rule files found under {RULES_DIR}"
    for rule_file in rule_files:
        content, name = rule_file.read_text(), rule_file.relative_to(RULES_DIR)
        frontmatter = FRONTMATTER_RE.match(content)
        offset = frontmatter.group(0).count("\n") if frontmatter else 0
        body = content[frontmatter.end():] if frontmatter else content
        assert body.startswith("<!-- version:"), f"{name}: missing metadata header after any frontmatter {HINT}"
        errors = metadata_header_errors(body, line_offset=offset)
        assert not errors, f"{name}: {errors} {HINT}"
