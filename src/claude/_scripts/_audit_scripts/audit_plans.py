#!/usr/bin/env python3
"""List saved plans in <config>/_plans/ by plan status, so the ones still being acted on are easy to find.

Each plan's status and last-updated date come from its "**Plan status:**" line
(see _plan_file_format.md). Plans saved before that line existed fall back to their
phase table for the status, and any plan without a date falls back to the file's
modified time. Active plans untouched for stale_days or more are listed again as
stale, to park or drop. Plan-mode drafts live apart in <config>/plans/, and archived
plans in _plans/archive/ are never read, since only files directly in _plans/ are scanned.

Usage:
    make list_plans
    python3 src/claude/_scripts/_audit_scripts/audit_plans.py

<config> is $CLAUDE_CONFIG_DIR, falling back to ~/.claude, as in clean_plans.py. Always exits 0.
"""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path
from typing import NamedTuple

STALE_DAYS = 14
# Parked and Done/Dropped follow Active, which is what you came to find
SHOWN = ("Active", "Parked")


def _load_clean_plans():
    """Import the sibling clean_plans.py, which owns plan parsing, from its own folder."""
    path = Path(__file__).resolve().parents[1] / "_clean_scripts" / "clean_plans.py"
    spec = importlib.util.spec_from_file_location("clean_plans", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLEAN_PLANS = _load_clean_plans()


class Plan(NamedTuple):
    """One saved plan as the listing shows it."""

    name: str
    status: str
    stated: bool  # False when the status was inferred from the phase table
    days_since_update: int
    phases_done: int
    phases: int


def read_plan(path: Path, today: date) -> Plan:
    """Summarise one plan file.

    :param path: The plan file.
    :param today: Reference date for the days-since-update count.
    """
    text = path.read_text(encoding="utf-8")
    status, stated = CLEAN_PLANS.plan_status(text)
    statuses = CLEAN_PLANS.phase_statuses(text)
    done = sum(1 for s in statuses if CLEAN_PLANS.DONE_RE.match(s))
    # The status line's date, falling back to the file's modified time for plans without one
    updated = CLEAN_PLANS.plan_updated(text) or date.fromtimestamp(path.stat().st_mtime)
    return Plan(path.stem, status, stated, (today - updated).days, done, len(statuses))


def collect(plans_dir: Path, today: date) -> list[Plan]:
    """Read every plan directly in plans_dir, most recently updated first."""
    plans = [read_plan(p, today) for p in plans_dir.glob("*.md")]
    return sorted(plans, key=lambda p: (p.days_since_update, p.name))


def stale(plans: list[Plan], stale_days: int = STALE_DAYS) -> list[Plan]:
    """Return Active plans untouched for stale_days or more."""
    return [p for p in plans if p.status == "Active" and p.days_since_update >= stale_days]


def _line(plan: Plan) -> str:
    """Format one plan for the listing."""
    progress = f"{plan.phases_done}/{plan.phases} phases done" if plan.phases else "no phase table"
    inferred = "" if plan.stated else "  (no status line, inferred)"
    return f"  {plan.name}  (updated {plan.days_since_update}d ago)  {progress}{inferred}"


def report(plans: list[Plan], stale_days: int = STALE_DAYS) -> str:
    """Build the listing: Active and Parked plans in full, then stale ones, then a count of archivable ones."""
    if not plans:
        return "No saved plans."
    lines = []
    for status in SHOWN:
        group = [p for p in plans if p.status == status]
        if group:
            lines += [f"{status.upper()} ({len(group)})", *map(_line, group), ""]
    old = stale(plans, stale_days)
    if old:
        lines += [f"STALE — Active, untouched {stale_days}d+ ({len(old)}): park or drop?", *map(_line, old), ""]
    finished = [p for p in plans if p.status in CLEAN_PLANS.ARCHIVABLE]
    if finished:
        lines.append(f"{len(finished)} Done or Dropped — run `make clean_plans` to archive them.")
    return "\n".join(lines).rstrip()


def drafts_line(drafts_dir: Path, today: date, stale_days: int = STALE_DAYS) -> str:
    """Count plan-mode drafts in plans/, and how many are old enough for make clean_plans to archive."""
    if not drafts_dir.is_dir():
        return ""
    total = len(list(drafts_dir.glob("*.md")))
    if not total:
        return ""
    old = len(CLEAN_PLANS.find_old_drafts(drafts_dir, min_age_days=stale_days, today=today))
    hint = f", {old} older than {stale_days}d — run `make clean_plans` to archive them" if old else ""
    return f"Drafts in {drafts_dir.name}/: {total}{hint}."


def main(plans_dir: str | Path | None = None, today: date | None = None):
    """Print the listing for the config's _plans/ folder.

    :param plans_dir: Override the folder, for tests. Defaults to $CLAUDE_CONFIG_DIR/_plans.
    :param today: Override today's date, for tests.
    """
    plans_dir = CLEAN_PLANS._default_plans_dir() if plans_dir is None else Path(plans_dir)
    if not plans_dir.is_dir():
        print(f"No plans folder found at {plans_dir}.")
        return
    today = today or date.today()
    print(report(collect(plans_dir, today)))
    line = drafts_line(plans_dir.parent / "plans", today)  # plan mode's own drafts, beside _plans/
    if line:
        print(f"\n{line}")


if __name__ == "__main__":
    main()
