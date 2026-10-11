"""Archive Done and Dropped plans from <config>/_plans/ into <config>/_plans/archive/.

A plan's status comes from its "**Plan status:**" line (see _plan_file_format.md).
Plans saved before that line existed count as Done only when every Status cell in
their phase table reads Done. Active and Parked plans are always kept, and so are
plans newer than min_age_days (by their YYYY_MM_DD_ filename prefix), so a
just-finished plan stays easy to find.

<config> is $CLAUDE_CONFIG_DIR, falling back to ~/.claude. Plan-mode drafts live apart
in <config>/plans/, and only files directly in _plans/ are read, never archive/.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

# Plan files are named YYYY_MM_DD_<topic>.md
PLAN_NAME_RE = re.compile(r"^(\d{4})_(\d{2})_(\d{2})_[a-z0-9_]+\.md$")
# A Status cell counts as finished when it starts with Done, with or without the ✅ emoji
DONE_RE = re.compile(r"^(✅\s*)?done\b", re.IGNORECASE)


def _default_plans_dir() -> Path:
    """Return the _plans/ folder of the config named by CLAUDE_CONFIG_DIR.

    :return: ``$CLAUDE_CONFIG_DIR/_plans``, or ``~/.claude/_plans`` when the variable is unset.
    :rtype: Path
    """
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude"
    return Path(config_dir).expanduser() / "_plans"


def _split_row(line: str) -> list[str]:
    """Split a markdown table row into its trimmed cells.

    :param line: One table row, e.g. ``| 1 | Build | ✅ Done |``.
    :type line: str
    :return: The cell values, without the empty edges outside the outer pipes.
    :rtype: list[str]
    """
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def phase_statuses(text: str) -> list[str]:
    """Return the Status cells of the first table in a plan that has a Status column.

    :param text: The plan file's content.
    :type text: str
    :return: One status per phase row, or an empty list when the plan has no such table.
    :rtype: list[str]
    """
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        header = _split_row(line)
        if "Status" not in header:
            continue

        status_col = header.index("Status")
        statuses = []
        # Skip the |---| separator row, then read rows until the table ends
        for row in lines[index + 2 :]:
            if not row.lstrip().startswith("|"):
                break
            cells = _split_row(row)
            statuses.append(cells[status_col] if status_col < len(cells) else "")
        return statuses
    return []


def is_finished(text: str) -> bool:
    """Decide whether every phase in a plan is Done.

    :param text: The plan file's content.
    :type text: str
    :return: True only when the plan has a phase table and every Status cell reads Done.
    :rtype: bool
    """
    statuses = phase_statuses(text)
    return bool(statuses) and all(DONE_RE.match(status) for status in statuses)


PLAN_STATUSES = ("Active", "Parked", "Done", "Dropped")
ARCHIVABLE = ("Done", "Dropped")
# The plan-level line from _plan_file_format.md, e.g. "**Plan status:** 🟢 Active"
PLAN_STATUS_RE = re.compile(
    r"^\*\*Plan status:\*\*\s*(?:\S+\s+)?(Active|Parked|Done|Dropped)\b", re.IGNORECASE | re.MULTILINE
)


def plan_status(text: str) -> tuple[str, bool]:
    """Return a plan's overall status, and whether it came from a Plan status line.

    Plans saved before the line existed fall back to their phase table: all Done means Done,
    anything else Active, so an unfinished legacy plan is never hidden.

    :param text: The plan file's content.
    :return: One of PLAN_STATUSES, and True when the plan states it rather than it being inferred.
    """
    match = PLAN_STATUS_RE.search(text)
    if match:
        return match.group(1).capitalize(), True
    return ("Done" if is_finished(text) else "Active"), False


# The optional date on the same line, e.g. "**Plan status:** 🟢 Active · updated 2026-10-11"
PLAN_UPDATED_RE = re.compile(
    r"^\*\*Plan status:\*\*.*?\bupdated (\d{4})-(\d{2})-(\d{2})", re.IGNORECASE | re.MULTILINE
)


def plan_updated(text: str) -> date | None:
    """Return the date on a plan's status line, which Claude moves forward whenever a phase or the status changes.

    A file's modified time can't stand in for it: adding a status line, copying a backup or any small
    edit resets it, which would hide a stale plan.

    :param text: The plan file's content.
    :return: The date, or None when the line has no valid one.
    """
    match = PLAN_UPDATED_RE.search(text)
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def plan_date(name: str) -> date | None:
    """Read the date from a plan's YYYY_MM_DD_ filename prefix.

    :param name: The plan's filename.
    :type name: str
    :return: The date, or None when the name doesn't follow the pattern or the date is invalid.
    :rtype: date or None
    """
    match = PLAN_NAME_RE.match(name)
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def find_candidates(plans_dir: Path, min_age_days: int = 14, today: date | None = None) -> list[Path]:
    """List Done and Dropped plans old enough to archive.

    :param plans_dir: The _plans/ folder to scan; its archive/ subfolder is never scanned.
    :type plans_dir: Path
    :param min_age_days: Keep plans dated fewer than this many days ago.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
    :type today: date or None
    :return: Paths of the plans to archive, sorted by name.
    :rtype: list[Path]
    """
    if today is None:
        today = date.today()

    candidates = []
    for path in sorted(plans_dir.glob("*.md")):
        dated = plan_date(path.name)
        # Undated or too-recent plans are kept, whatever their status
        if dated is None or (today - dated).days < min_age_days:
            continue
        if plan_status(path.read_text(encoding="utf-8"))[0] in ARCHIVABLE:
            candidates.append(path)
    return candidates


def main(
    plans_dir: str | Path | None = None,
    min_age_days: int = 14,
    today: date | None = None,
):
    """Preview the Done and Dropped plans, ask for confirmation, then move them to archive/.

    :param plans_dir: Override the plans directory path. Defaults to $CLAUDE_CONFIG_DIR/_plans.
        Intended for use in tests.
    :type plans_dir: str or Path or None
    :param min_age_days: Only archive plans this many days old or older.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
        Intended for use in tests.
    :type today: date or None
    """
    plans_dir = _default_plans_dir() if plans_dir is None else Path(plans_dir)
    if not plans_dir.is_dir():
        print(f"No plans folder found at {plans_dir}.")
        sys.exit(0)

    candidates = find_candidates(plans_dir, min_age_days=min_age_days, today=today)
    if not candidates:
        print(f"No Done or Dropped plans older than {min_age_days} days to archive.")
        sys.exit(0)

    print(f"Done or Dropped plans to archive ({len(candidates)}):\n")
    for path in candidates:
        print(f"  {path.name}")

    try:
        confirm = input(f"\nMove these to {plans_dir / 'archive'}/? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(0)

    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    archive_dir = plans_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    for path in candidates:
        shutil.move(path, archive_dir / path.name)
        print(f"  Archived: {path.name}")

    print(f"\nDone. {len(candidates)} plans moved to {archive_dir}")


if __name__ == "__main__":
    main()
