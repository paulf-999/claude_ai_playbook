"""Archive executed/superseded plans from ~/.claude/plans/PLANS.md.

Reads the PLANS.md catalogue, lists all entries with status 'executed' or
'superseded', asks for confirmation, then moves those plan files to
~/.claude/plans/archive/ and removes their rows from PLANS.md.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import date


def _parse_header_cols(lines: list[str]) -> tuple[int | None, int | None, int | None]:
    """Return (file_col, date_col, status_col) indices from the PLANS.md table header.

    :param lines: Lines from PLANS.md.
    :type lines: list[str]
    :return: Column index tuple; any member is None if the column was not found.
    :rtype: tuple[int | None, int | None, int | None]
    """
    for line in lines:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if "File" in parts and "Status" in parts:
            return (
                parts.index("File"),
                parts.index("Date") if "Date" in parts else None,
                parts.index("Status"),
            )
    return None, None, None


def _is_old_enough(parts: list[str], date_col: int | None, min_age_days: int, today: date) -> bool:
    """Return True if the row is old enough to be archived (or has an unparseable/missing date).

    :param parts: Pipe-split, stripped cells from a table row.
    :type parts: list[str]
    :param date_col: Index of the Date column, or None if absent.
    :type date_col: int or None
    :param min_age_days: Minimum age threshold in days.
    :type min_age_days: int
    :param today: Reference date for age calculation.
    :type today: date
    :return: True if the row should be included as an archive candidate.
    :rtype: bool
    """
    if date_col is None or date_col >= len(parts):
        return True
    try:
        return (today - date.fromisoformat(parts[date_col])).days >= min_age_days
    except ValueError:
        return True  # Unparseable date — include conservatively.


def _find_candidates(
    lines: list[str],
    min_age_days: int = 14,
    today: date | None = None,
) -> list[tuple[int, str, str | None]]:
    """Identify PLANS.md rows with status 'executed' or 'superseded' and age >= min_age_days.

    Locates the File, Date, and Status column indices from the table header row so
    the function stays correct if columns are ever reordered. Rows with a missing
    or unparseable date are included (conservative default).

    :param lines: Lines from PLANS.md (as returned by readlines()).
    :type lines: list[str]
    :param min_age_days: Minimum age in days for a plan to be considered for archival.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
    :type today: date or None
    :return: List of (line_index, row_text, filename_or_None) tuples for each candidate row.
    :rtype: list[tuple[int, str, str | None]]
    """
    if today is None:
        today = date.today()

    file_col, date_col, status_col = _parse_header_cols(lines)
    if file_col is None or status_col is None:
        return []

    candidates = []
    for i, line in enumerate(lines):
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) <= max(file_col, status_col):
            continue
        if parts[status_col] not in ("executed", "superseded"):
            continue
        if not _is_old_enough(parts, date_col, min_age_days, today):
            continue
        m = re.search(r"\[([^\]]+)\]\([^)]+\)", parts[file_col])
        candidates.append((i, line.rstrip(), m.group(1) if m else None))
    return candidates


def _write_review_md(candidates: list[tuple[int, str, str | None]], review_path: str, min_age_days: int) -> None:
    """Write a formatted markdown table of archive candidates to a review file.

    :param candidates: Candidate tuples as returned by _find_candidates.
    :type candidates: list[tuple[int, str, str | None]]
    :param review_path: Absolute path to write the review file.
    :type review_path: str
    :param min_age_days: Age threshold used for this run (shown in the file header).
    :type min_age_days: int
    """
    lines = [
        "# Plans to Archive — Review\n\n",
        f"> Plans with status `executed` or `superseded` and age ≥ {min_age_days} days.\n\n",
        "| File | Project | Task | Date | Status |\n",
        "|------|---------|------|------|--------|\n",
    ]
    for _, row, _ in candidates:
        # row is already a pipe-delimited table row — write it as-is.
        lines.append(row + "\n")
    with open(review_path, "w") as f:
        f.writelines(lines)


def main(
    plans_dir: str | None = None,
    min_age_days: int = 14,
    today: date | None = None,
) -> None:
    """Run the clean_plans archival workflow.

    :param plans_dir: Override the plans directory path. Defaults to ~/.claude/plans.
        Intended for use in tests.
    :type plans_dir: str or None
    :param min_age_days: Only archive plans this many days old or older.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
        Intended for use in tests.
    :type today: date or None
    """
    if plans_dir is None:
        plans_dir = os.path.expanduser("~/.claude/plans")
    index_path = os.path.join(plans_dir, "PLANS.md")

    if not os.path.exists(index_path):
        print(f"No PLANS.md found at {index_path}.")
        sys.exit(0)

    with open(index_path) as f:
        lines = f.readlines()

    candidates = _find_candidates(lines, min_age_days=min_age_days, today=today)

    if not candidates:
        print(f"No executed/superseded plans older than {min_age_days} days to archive.")
        sys.exit(0)

    review_path = os.path.join(plans_dir, "archive_review.md")
    _write_review_md(candidates, review_path, min_age_days)
    print(f"Review file: {review_path}\n")

    print(f"Plans to archive ({len(candidates)}):\n")
    for _, row, _ in candidates:
        print(f"  {row}")

    try:
        confirm = input("\nArchive these plans? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(0)

    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    archive_dir = os.path.join(plans_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    archived_indices: set[int] = set()
    for idx, _, filename in candidates:
        archived_indices.add(idx)
        if not filename:
            continue
        src = os.path.join(plans_dir, filename)
        if not os.path.exists(src):
            print(f"  Not found (skipped): {filename}")
            continue
        shutil.move(src, os.path.join(archive_dir, filename))
        print(f"  Archived: {filename}")

    # Remove archived rows from PLANS.md
    new_lines = [line for i, line in enumerate(lines) if i not in archived_indices]
    with open(index_path, "w") as f:
        f.writelines(new_lines)

    print(f"\nDone. View archived plans at {archive_dir}")


if __name__ == "__main__":
    main()
