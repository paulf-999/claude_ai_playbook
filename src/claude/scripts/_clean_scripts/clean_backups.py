"""Move old ~/.claude_backup_* directories to ~/.claude_backup_archive/.

Scans the home directory for timestamped backup directories created by
install_claude_files.sh and update_claude_files.sh, and moves those older
than min_age_days to ~/.claude_backup_archive/.
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date
from pathlib import Path

# Pattern: .claude_backup_YYYYMMDD_HHMMSS
_BACKUP_RE = re.compile(r"^\.claude_backup_(\d{4})(\d{2})(\d{2})_\d{6}$")


def _find_candidates(
    home_dir: Path,
    min_age_days: int = 14,
    today: date | None = None,
) -> list[str]:
    """Return backup directory names older than min_age_days.

    Dirs with an unparseable date segment are included conservatively.

    :param home_dir: Directory to scan for backup dirs (normally HOME).
    :type home_dir: Path
    :param min_age_days: Minimum age in days for a dir to be considered for archival.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
    :type today: date or None
    :return: Sorted list of directory names (not full paths) that are candidates.
    :rtype: list[str]
    """
    if today is None:
        today = date.today()

    candidates = []
    try:
        entries = sorted(entry.name for entry in home_dir.iterdir())
    except OSError:
        return []

    for name in entries:
        m = _BACKUP_RE.match(name)
        if not m:
            continue
        if not (home_dir / name).is_dir():
            continue
        try:
            backup_date = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            # Unparseable — include conservatively.
            candidates.append(name)
            continue
        if (today - backup_date).days >= min_age_days:
            candidates.append(name)

    return candidates


def _write_review_md(candidates: list[str], review_path: Path, min_age_days: int):
    """Write a list of archive candidates to a review file.

    :param candidates: Directory names as returned by _find_candidates.
    :type candidates: list[str]
    :param review_path: Absolute path to write the review file.
    :type review_path: Path
    :param min_age_days: Age threshold used for this run (shown in the file header).
    :type min_age_days: int
    """
    lines = [
        "# Backup Directories to Archive — Review\n\n",
        f"> Backup directories aged ≥ {min_age_days} days.\n\n",
    ]
    for name in candidates:
        lines.append(f"- `{name}`\n")
    review_path.write_text("".join(lines))


def main(
    home_dir: str | Path | None = None,
    min_age_days: int = 14,
    today: date | None = None,
):
    """Run the clean_backups archival workflow.

    :param home_dir: Override the home directory to scan. Defaults to ~/.
        Intended for use in tests.
    :type home_dir: str or Path or None
    :param min_age_days: Only archive backup dirs this many days old or older.
    :type min_age_days: int
    :param today: Reference date for age calculations. Defaults to date.today().
        Intended for use in tests.
    :type today: date or None
    """
    home_dir = Path.home() if home_dir is None else Path(home_dir)

    candidates = _find_candidates(home_dir, min_age_days=min_age_days, today=today)

    if not candidates:
        print(f"No backup directories older than {min_age_days} days to archive.")
        sys.exit(0)

    review_path = home_dir / ".claude_backup_review.md"
    _write_review_md(candidates, review_path, min_age_days)
    print(f"Review file: {review_path}\n")

    print(f"Backup directories to archive ({len(candidates)}):\n")
    for name in candidates:
        print(f"  {name}")

    try:
        confirm = input("\nMove these to ~/.claude_backup_archive/? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(0)

    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    archive_dir = home_dir / ".claude_backup_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    for name in candidates:
        shutil.move(home_dir / name, archive_dir / name)
        print(f"  Archived: {name}")

    print(f"\nDone. {len(candidates)} directories moved to {archive_dir}")


if __name__ == "__main__":
    main()
