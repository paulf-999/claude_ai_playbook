"""File saved plans and plan-mode drafts into subfolders named after their plan status.

Saved plans in <config>/_plans/ move to active/, parked/, done/ or dropped/, following
each plan's "**Plan status:**" line (see _plan_file_format.md). Plans saved before that
line existed count as Done only when every phase in their table reads Done, and Active
otherwise. The status line stays the source of truth, so a plan whose status changes is
simply moved again on the next run.

Drafts in <config>/plans/ move to plans/draft/ once a day old, and to plans/archive/ once
unchanged for min_age_days: a draft worth keeping was copied into _plans/ when approved.
Nothing is deleted or overwritten, and every move is previewed and confirmed first.

<config> is $CLAUDE_CONFIG_DIR, falling back to ~/.claude.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):  # pragma: no cover
    sys.exit("This script needs Python 3.10 or newer — you're running " + sys.version.split()[0] + ".")

import os
import re
import shutil
from datetime import date
from pathlib import Path

# A Status cell counts as finished when it starts with Done, with or without the ✅ emoji
DONE_RE = re.compile(r"^(✅\s*)?done\b", re.IGNORECASE)


def _default_plans_dir() -> Path:
    """Return the _plans/ folder of the config named by CLAUDE_CONFIG_DIR.

    :return: ``$CLAUDE_CONFIG_DIR/_plans``, or ``~/.claude/_plans`` when the variable is unset.
    :rtype: Path
    """
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    return (Path(config_dir) if config_dir else Path.home() / ".claude") / "_plans"


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


PLAN_STATUSES = ("Draft", "Active", "Parked", "Done", "Dropped")
FINISHED = ("Done", "Dropped")
# The plan-level line from _plan_file_format.md, e.g. "**Plan status:** 🟢 Active"
PLAN_STATUS_RE = re.compile(
    r"^\*\*Plan status:\*\*\s*(?:\S+\s+)?(Draft|Active|Parked|Done|Dropped)\b", re.IGNORECASE | re.MULTILINE
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


# Each status files into a subfolder named after it, e.g. _plans/active/ or plans/draft/
STATUS_FOLDERS = {status: status.lower() for status in PLAN_STATUSES}
DRAFTS_ARCHIVE = "archive"  # plans/archive/ holds drafts untouched for min_age_days


def saved_plan_files(plans_dir: Path) -> list[Path]:
    """Return every saved plan: loose in _plans/ or in one of its status subfolders.

    Any other subfolder, such as the archive/ used before status folders, is never read.

    :param plans_dir: The _plans/ folder.
    :return: Plan paths, sorted.
    """
    files = list(plans_dir.glob("*.md"))
    for folder in STATUS_FOLDERS.values():
        files += (plans_dir / folder).glob("*.md")
    return sorted(files)


def find_plan_moves(plans_dir: Path) -> list[tuple[Path, Path]]:
    """List saved plans not yet in the subfolder their status names, with the folder each belongs in.

    :param plans_dir: The _plans/ folder.
    :return: (plan, target folder) pairs, sorted by plan path.
    """
    moves = []
    for path in saved_plan_files(plans_dir):
        status, _ = plan_status(path.read_text(encoding="utf-8"))
        target = plans_dir / STATUS_FOLDERS[status]
        if path.parent != target:
            moves.append((path, target))
    return moves


def draft_files(drafts_dir: Path) -> list[Path]:
    """Return every plan-mode draft: loose in plans/ or already filed in plans/draft/."""
    return sorted([*drafts_dir.glob("*.md"), *(drafts_dir / STATUS_FOLDERS["Draft"]).glob("*.md")])


def find_draft_moves(drafts_dir: Path, min_age_days: int = 14, today: date | None = None) -> list[tuple[Path, Path]]:
    """List drafts to file: into plans/draft/ once a day old, or plans/archive/ once min_age_days old.

    Drafts changed today stay put, since plan mode may still be writing to them. A draft worth
    keeping was copied into _plans/ when approved, so an old one is almost always abandoned —
    archiving rather than deleting keeps one whose copy was missed recoverable.

    :param drafts_dir: The plans/ folder plan mode writes to.
    :param min_age_days: Archive drafts unchanged for this many days or more.
    :param today: Reference date for age calculations. Defaults to date.today().
    :return: (draft, target folder) pairs, sorted by draft path.
    """
    today = today or date.today()
    filed = drafts_dir / STATUS_FOLDERS["Draft"]
    moves = []
    for path in draft_files(drafts_dir):
        age = (today - date.fromtimestamp(path.stat().st_mtime)).days
        if age >= min_age_days:
            moves.append((path, drafts_dir / DRAFTS_ARCHIVE))
        elif age >= 1 and path.parent != filed:
            moves.append((path, filed))
    return moves


def _move_all(moves: list[tuple[Path, Path]], root: Path) -> int:
    """Move each file into its target folder, never overwriting; return how many moved."""
    moved = 0
    for path, target in moves:
        target.mkdir(parents=True, exist_ok=True)
        if (target / path.name).exists():
            print(f"  Skipped (already in {target.relative_to(root)}/): {path.name}")
            continue
        shutil.move(path, target / path.name)
        moved += 1
    return moved


def _preview(moves: list[tuple[Path, Path]], root: Path) -> None:
    """Print the planned moves, grouped by target folder."""
    for target in sorted({target for _, target in moves}):
        names = [path.name for path, folder in moves if folder == target]
        print(f"To {root.name}/{target.relative_to(root)}/ ({len(names)}):")
        print("\n".join(f"  {name}" for name in names) + "\n")


def main(
    plans_dir: str | Path | None = None,
    min_age_days: int = 14,
    today: date | None = None,
    drafts_dir: str | Path | None = None,
    assume_yes: bool = False,
):
    """Preview filing saved plans and drafts into their status subfolders, ask once, then move them.

    With assume_yes, as ``make install`` runs it, there's no preview or question, and one summary
    line is printed only when something moved — the install has already been confirmed and backed up.

    :param plans_dir: Override the saved plans folder. Defaults to $CLAUDE_CONFIG_DIR/_plans.
        Intended for use in tests.
    :param min_age_days: Archive drafts unchanged for this many days or more.
    :param today: Reference date for draft ages. Defaults to date.today(). Intended for use in tests.
    :param drafts_dir: Override the drafts folder. Defaults to plans/ beside the saved plans folder.
    :param assume_yes: Move without asking, printing one summary line. Set by ``--yes``.
    """
    plans_dir = _default_plans_dir() if plans_dir is None else Path(plans_dir)
    drafts_dir = plans_dir.parent / "plans" if drafts_dir is None else Path(drafts_dir)
    if not plans_dir.is_dir() and not drafts_dir.is_dir():
        if not assume_yes:
            print(f"No plans folder found at {plans_dir} or {drafts_dir}.")
        return

    plan_moves = find_plan_moves(plans_dir) if plans_dir.is_dir() else []
    draft_moves = find_draft_moves(drafts_dir, min_age_days=min_age_days, today=today) if drafts_dir.is_dir() else []
    if not plan_moves and not draft_moves:
        if not assume_yes:
            print("Every plan and draft is already in its status folder.")
        return

    if assume_yes:
        plans_moved = _move_all(plan_moves, plans_dir)
        drafts_moved = _move_all(draft_moves, drafts_dir)
        print(f"Filed {plans_moved} plans and {drafts_moved} drafts into their status folders")
        return

    _preview(plan_moves, plans_dir)
    _preview(draft_moves, drafts_dir)
    try:
        confirm = input("Move these? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(0)

    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    plans_moved = _move_all(plan_moves, plans_dir)
    drafts_moved = _move_all(draft_moves, drafts_dir)
    print(f"\nDone. {plans_moved} plans and {drafts_moved} drafts filed.")


if __name__ == "__main__":
    main(assume_yes="--yes" in sys.argv[1:])
