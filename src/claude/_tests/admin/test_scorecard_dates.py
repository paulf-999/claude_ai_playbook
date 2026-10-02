# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-02
# Version:           1.0.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the per-row Date Updated column in every quality scorecard table.

Each dimension row records when its score last changed, so every table needs a
``Date Updated`` column after ``Score``. Every row date must be a real ISO date,
and none may be later than the file's header ``Date Updated``.
"""

import re
from datetime import date
from pathlib import Path
from typing import Optional

from _shared_paths import CLAUDE_DIR

SCORECARDS_DIR = CLAUDE_DIR / "_admin" / "_quality_scorecards"
TABLE_HEADER = "| Dimension | Score | Date Updated | Notes |"
SEPARATOR = "|---|---|---|---|"
ROW = re.compile(r"^\| \*\*(?P<dim>[^|]+)\*\* \| (?P<score>[^|]+?) \| (?P<date>[^|]+?) \| ")
HEADER_DATE = re.compile(r"^\*\*Date Updated:\*\* (\S+)", re.M)
HINT = "— see _admin/_quality_scorecards/rules/README.md (Row `Date Updated`)"

VALID = """# Quality Scorecard — demo.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 🔍 **Point:** fine |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Clarity |
"""


def parse_iso(value: str) -> Optional[date]:
    """Parse a strict ``YYYY-MM-DD`` date.

    :param value: Text to parse.
    :type value: str
    :return: The date, or ``None`` when the text isn't a real ISO date.
    :rtype: Optional[date]
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def scorecard_date_errors(text: str) -> list[str]:
    """Return every row-date problem in one scorecard's text.

    :param text: Full scorecard markdown.
    :type text: str
    :return: One message per problem; empty when the table is valid.
    :rtype: list[str]
    """
    lines = text.splitlines()
    if TABLE_HEADER not in lines:
        return [f"table header is not '{TABLE_HEADER}'"]
    errors = []
    if lines[lines.index(TABLE_HEADER) + 1] != SEPARATOR:
        errors.append(f"separator row is not '{SEPARATOR}'")
    header_match = HEADER_DATE.search(text)
    header_date = parse_iso(header_match.group(1)) if header_match else None
    rows = [m for line in lines if (m := ROW.match(line))]
    if not rows:
        errors.append("no dimension rows found")
    for row in rows:
        row_date = parse_iso(row["date"])
        if row_date is None:
            errors.append(f"{row['dim']}: '{row['date']}' is not a YYYY-MM-DD date")
        elif header_date and row_date > header_date:
            errors.append(f"{row['dim']}: row date {row_date} is later than header Date Updated {header_date}")
    return errors


def scorecard_files() -> list[Path]:
    """Return every scorecard file under the scorecards directory.

    :return: Sorted ``scorecard_*.md`` paths.
    :rtype: list[Path]
    """
    return sorted(SCORECARDS_DIR.rglob("scorecard_*.md"))


# --- Accepted ---


def test_valid_table_accepted():
    """A 4-column table with valid dates no later than the header passes."""
    assert scorecard_date_errors(VALID) == [], "valid scorecard table was rejected"


def test_row_date_equal_to_header_accepted():
    """A row dated the same day as the header is allowed."""
    assert "2026-10-01 |" in VALID, "fixture should contain a row dated on the header day"
    assert scorecard_date_errors(VALID) == [], "row dated on the header day was rejected"


def test_missing_header_date_skips_comparison():
    """Without a header ``Date Updated`` the row dates are still validated, just not compared."""
    text = VALID.replace("**Date Updated:** 2026-10-01\n", "")
    assert scorecard_date_errors(text) == [], "header-less scorecard with valid rows was rejected"
    assert scorecard_date_errors(text.replace("2026-09-28 |", "28/09/2026 |")), "bad row date passed without header"


# --- Rejected ---


def test_three_column_table_rejected():
    """The old ``| Dimension | Score | Notes |`` table is rejected."""
    old = VALID.replace(TABLE_HEADER, "| Dimension | Score | Notes |")
    errors = scorecard_date_errors(old)
    assert errors, "3-column table was accepted"
    assert "table header" in errors[0], f"unexpected error text: {errors}"


def test_three_column_separator_rejected():
    """A 4-column header over a 3-column separator is rejected."""
    errors = scorecard_date_errors(VALID.replace(SEPARATOR, "|---|---|---|"))
    assert errors and "separator" in errors[0], f"3-column separator not caught: {errors}"


def test_non_iso_date_rejected():
    """A row date in any format other than ``YYYY-MM-DD`` is rejected."""
    errors = scorecard_date_errors(VALID.replace("2026-09-28 |", "28/09/2026 |"))
    assert errors and "Clarity" in errors[0], f"non-ISO date not caught: {errors}"


def test_impossible_date_rejected():
    """A well-shaped but impossible date like month 13 is rejected."""
    assert scorecard_date_errors(VALID.replace("2026-09-28 |", "2026-13-01 |")), "month 13 was accepted"


def test_placeholder_date_rejected():
    """The template's ``YYYY-MM-DD`` placeholder must be replaced in a real scorecard."""
    assert scorecard_date_errors(VALID.replace("2026-09-28 |", "YYYY-MM-DD |")), "placeholder date was accepted"


def test_row_date_after_header_rejected():
    """A row date later than the header ``Date Updated`` is rejected."""
    errors = scorecard_date_errors(VALID.replace("2026-09-28 |", "2026-10-02 |"))
    assert errors, "row dated after header was accepted"
    assert "later than header" in errors[0], f"unexpected error text: {errors}"


def test_table_without_rows_rejected():
    """A table with no dimension rows is rejected, so a malformed table can't pass silently."""
    empty = "\n".join(line for line in VALID.splitlines() if not line.startswith("| **"))
    assert scorecard_date_errors(empty) == ["no dimension rows found"], "empty table was accepted"


# --- Real scorecards ---


def test_scorecards_exist():
    """The scan below is meaningful only if scorecards are found."""
    assert scorecard_files(), f"no scorecards found under {SCORECARDS_DIR}"


def test_every_scorecard_has_valid_row_dates():
    """Every real scorecard has the column, valid ISO row dates, and none after its header date."""
    for path in scorecard_files():
        errors = scorecard_date_errors(path.read_text())
        assert not errors, f"{path.relative_to(SCORECARDS_DIR)}: {errors} {HINT}"
