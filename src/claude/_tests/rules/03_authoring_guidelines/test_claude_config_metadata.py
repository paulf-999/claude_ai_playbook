# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-28
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

"""Validates the rule metadata header defined in _claude_config_metadata.md.

Any _rules/ file that carries a header must have it on line 1, in the exact
``<!-- version: X.Y.Z | created: YYYY-MM-DD | updated: YYYY-MM-DD -->`` format,
with valid semver and ISO dates and ``updated`` on or after ``created``.
Files without a header are skipped until the backfill makes it mandatory.
"""
import re
from datetime import date

from _shared_paths import RULES_DIR

METADATA_HEADER_RE = re.compile(
    r"^<!-- version: (0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r" \| created: (\d{4}-\d{2}-\d{2}) \| updated: (\d{4}-\d{2}-\d{2}) -->$"
)

VALID_HEADER = "<!-- version: 1.2.10 | created: 2026-09-01 | updated: 2026-09-28 -->"


def metadata_header_errors(content: str) -> list[str]:
    """Return format errors for a rule's metadata header; empty if valid or absent.

    :param content: Full text of a rule file.
    :type content: str
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    lines = content.splitlines()
    header_idx = [line_idx for line_idx, line in enumerate(lines) if line.startswith("<!-- version:")]
    if not header_idx:
        return []
    if header_idx != [0]:
        return [f"header must be on line 1 only, found on line(s) {[line_idx + 1 for line_idx in header_idx]}"]
    match = METADATA_HEADER_RE.match(lines[0])
    if not match:
        return [f"header does not match format: {lines[0]!r}"]
    try:
        created = date.fromisoformat(match.group(4))
        updated = date.fromisoformat(match.group(5))
    except ValueError as exc:
        return [f"invalid date: {exc}"]
    if updated < created:
        return [f"updated ({updated}) is earlier than created ({created})"]
    return []


def with_header(header: str) -> str:
    """Build a minimal rule file body with the given first line.

    :param header: The line to place above the H1.
    :type header: str
    :return: Rule file content.
    :rtype: str
    """
    return f"{header}\n# 🗂️ Example rule\n\n**Purpose:** Example.\n"


# --- Accepted ---

def test_valid_header_accepted():
    """A well-formed header on line 1 produces no errors."""
    assert metadata_header_errors(with_header(VALID_HEADER)) == [], "valid header was rejected"


def test_same_day_created_and_updated_accepted():
    """A new rule has created == updated, which must be allowed."""
    header = "<!-- version: 1.0.0 | created: 2026-09-28 | updated: 2026-09-28 -->"
    assert metadata_header_errors(with_header(header)) == [], "same-day dates were rejected"


def test_zero_components_accepted():
    """Zero is a valid semver component (e.g. 0.1.0, 1.0.0)."""
    for version in ("0.1.0", "1.0.0", "0.0.1"):
        header = f"<!-- version: {version} | created: 2026-09-28 | updated: 2026-09-28 -->"
        assert metadata_header_errors(with_header(header)) == [], f"{version} was rejected"


def test_headerless_file_skipped():
    """Files without a header are skipped until the backfill is done."""
    assert metadata_header_errors("# 🗂️ Rule without header\n") == [], "header-less file was flagged"
    assert metadata_header_errors("") == [], "empty file was flagged"


# --- Rejected: placement ---

def test_misplaced_header_rejected():
    """A header below line 1 is rejected with a line-1 message."""
    errors = metadata_header_errors(f"# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "header on line 2 was accepted"
    assert "line 1" in errors[0], f"unexpected error text: {errors}"


def test_duplicate_header_rejected():
    """A second header later in the file is rejected even if line 1 is valid."""
    errors = metadata_header_errors(f"{VALID_HEADER}\n# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "duplicate header was accepted"
    assert "[1, 3]" in errors[0], f"error should name both lines: {errors}"


# --- Rejected: format ---

def test_malformed_semver_rejected():
    """Versions that aren't exactly MAJOR.MINOR.PATCH are rejected."""
    for version in ("1.0", "1.0.0.0", "v1.0.0", "1.0.x"):
        header = f"<!-- version: {version} | created: 2026-09-28 | updated: 2026-09-28 -->"
        assert metadata_header_errors(with_header(header)), f"version {version!r} was accepted"


def test_leading_zero_version_rejected():
    """Semver forbids leading zeros in numeric components."""
    header = "<!-- version: 01.0.0 | created: 2026-09-28 | updated: 2026-09-28 -->"
    assert metadata_header_errors(with_header(header)), "leading-zero version was accepted"


def test_non_iso_date_format_rejected():
    """Dates must use hyphens (YYYY-MM-DD), not the underscore filename convention."""
    header = "<!-- version: 1.0.0 | created: 2026_09_28 | updated: 2026-09-28 -->"
    errors = metadata_header_errors(with_header(header))
    assert errors, "underscore date was accepted"
    assert "does not match format" in errors[0], f"unexpected error text: {errors}"


def test_missing_or_reordered_fields_rejected():
    """All three fields are required, in version → created → updated order."""
    missing = "<!-- version: 1.0.0 | created: 2026-09-28 -->"
    reordered = "<!-- version: 1.0.0 | updated: 2026-09-28 | created: 2026-09-28 -->"
    assert metadata_header_errors(with_header(missing)), "missing field was accepted"
    assert metadata_header_errors(with_header(reordered)), "reordered fields were accepted"


# --- Rejected: values ---

def test_impossible_date_rejected():
    """A correctly shaped but non-existent date is rejected."""
    header = "<!-- version: 1.0.0 | created: 2026-02-30 | updated: 2026-09-28 -->"
    errors = metadata_header_errors(with_header(header))
    assert errors, "2026-02-30 was accepted"
    assert "invalid date" in errors[0], f"unexpected error text: {errors}"


def test_updated_before_created_rejected():
    """updated must be on or after created."""
    header = "<!-- version: 1.0.0 | created: 2026-09-28 | updated: 2026-09-01 -->"
    errors = metadata_header_errors(with_header(header))
    assert errors, "updated-before-created was accepted"
    assert "earlier than created" in errors[0], f"unexpected error text: {errors}"


# --- Real files ---

def test_rule_files_have_valid_headers_when_present():
    """Every _rules/ file carrying a header must pass validation."""
    rule_files = [path for path in RULES_DIR.rglob("*.md") if path.name != "README.md"]
    assert rule_files, f"no rule files found under {RULES_DIR}"
    for rule_file in rule_files:
        errors = metadata_header_errors(rule_file.read_text())
        assert not errors, (
            f"{rule_file.relative_to(RULES_DIR)}: {errors} — see 03_authoring_guidelines/_claude_config_metadata.md"
        )
