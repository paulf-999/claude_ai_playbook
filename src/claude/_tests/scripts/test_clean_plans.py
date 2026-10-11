# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-11
# Version:           1.3.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that clean_plans.py archives only Done or Dropped, old-enough plans.

A plan's Plan status line decides it, and a plan without one is finished only
when every Status cell in its phase table reads Done. Anything else — an Active
or Parked plan, no table, a Pending phase, a recent date or an undated name —
must stay in _plans/, because archiving a live plan would lose work.
"""

import builtins
import importlib.util
import os
import time
from datetime import date

import pytest

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "_scripts" / "_clean_scripts" / "clean_plans.py"
TODAY = date(2026, 10, 2)
TABLE_HEADER = "| Phase | Action | Status |\n|---|---|---|\n"


def load_clean_plans():
    """Import clean_plans.py as a module.

    :return: The loaded module.
    :rtype: module
    """
    spec = importlib.util.spec_from_file_location("clean_plans", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


clean_plans = load_clean_plans()


def plan_text(*statuses: str) -> str:
    """Build a plan whose phase table has one row per status.

    :param statuses: The Status cell for each phase.
    :type statuses: str
    :return: Markdown content for a plan file.
    :rtype: str
    """
    rows = "".join(f"| {number} | Step {number} | {status} |\n" for number, status in enumerate(statuses, 1))
    return f"# Plan\n\n{TABLE_HEADER}{rows}"


def write_plan(folder, name: str, text: str):
    """Write a plan file into folder.

    :param folder: The fake _plans/ folder.
    :type folder: Path
    :param name: The plan's filename.
    :type name: str
    :param text: The plan's content.
    :type text: str
    :return: The written file.
    :rtype: Path
    """
    path = folder / name
    path.write_text(text, encoding="utf-8")
    return path


# ── deciding whether a plan is finished ───────────────────────────────────────


def test_all_done_is_finished():
    """Every phase Done, with or without the emoji, counts as finished."""
    assert clean_plans.is_finished(plan_text("✅ Done", "Done", "✅ Done (PR #12)")), "All-Done plan should be finished"


def test_any_pending_is_not_finished():
    """One Pending phase keeps the plan."""
    assert not clean_plans.is_finished(plan_text("✅ Done", "⏳ Pending")), "A Pending phase should keep the plan"


def test_in_progress_and_dash_are_not_finished():
    """In Progress and a placeholder dash both keep the plan."""
    assert not clean_plans.is_finished(plan_text("✅ Done", "🔄 In Progress")), "In Progress should keep the plan"
    assert not clean_plans.is_finished(plan_text("✅ Done", "—")), "A dash status should keep the plan"


def test_no_phase_table_is_not_finished():
    """A plan without a Status table is never treated as finished."""
    assert not clean_plans.is_finished("# Plan\n\nJust prose.\n"), "A plan with no table should be kept"
    assert clean_plans.phase_statuses("# Plan\n") == [], "No table should give no statuses"


def test_status_column_found_by_name():
    """The Status column is found by its header, wherever it sits."""
    text = "| Status | Phase |\n|---|---|\n| ✅ Done | 1 |\n| ⏳ Pending | 2 |\n"
    assert clean_plans.phase_statuses(text) == ["✅ Done", "⏳ Pending"], "Status column should be read by name"


def test_only_first_status_table_is_read():
    """Rows from a later table don't leak into the phase statuses."""
    text = plan_text("✅ Done") + "\nSome prose.\n\n| Item | Status |\n|---|---|\n| x | ⏳ Pending |\n"
    assert clean_plans.phase_statuses(text) == ["✅ Done"], "Only the first Status table should be read"


# ── reading the plan-level status ─────────────────────────────────────────────


def test_plan_status_line_is_read_with_or_without_emoji():
    """The Plan status line wins over the phase table, in any case, with or without its emoji."""
    assert clean_plans.plan_status("# P\n\n**Plan status:** 🗑️ Dropped\n") == ("Dropped", True)
    assert clean_plans.plan_status("**Plan status:** parked\n" + plan_text("✅ Done")) == ("Parked", True), (
        "a stated Parked must not be overridden by an all-Done table"
    )


def test_plan_status_falls_back_to_phase_table():
    """Without a status line, an all-Done plan reads Done and anything else Active, so nothing hides."""
    assert clean_plans.plan_status(plan_text("✅ Done", "Done")) == ("Done", False)
    assert clean_plans.plan_status(plan_text("✅ Done", "⏳ Pending")) == ("Active", False)
    assert clean_plans.plan_status("# Plan\n\nJust prose.\n") == ("Active", False), "no table must read Active"


def test_unknown_plan_status_word_is_ignored():
    """A word outside the four statuses falls back to the phase table rather than being trusted."""
    assert clean_plans.plan_status("**Plan status:** Maybe\n" + plan_text("⏳ Pending")) == ("Active", False)


def test_plan_updated_date_is_read_from_the_status_line():
    """The status line's updated date is read, and the status still parses with the date after it."""
    line = "**Plan status:** 🟢 Active · updated 2026-09-20\n"
    assert clean_plans.plan_updated(line) == date(2026, 9, 20)
    assert clean_plans.plan_status(line) == ("Active", True), "a date after the status must not break the status"


def test_missing_or_invalid_updated_date_gives_none():
    """No date, an impossible date, or a date outside the status line all give None."""
    assert clean_plans.plan_updated("**Plan status:** Active\n") is None
    assert clean_plans.plan_updated("**Plan status:** Active · updated 2026-13-40\n") is None
    assert clean_plans.plan_updated("Plan updated 2026-09-20 in prose\n") is None, "only the status line counts"


# ── reading plan dates ────────────────────────────────────────────────────────


def test_plan_date_parsed_from_prefix():
    """A YYYY_MM_DD_ prefix gives the plan's date."""
    assert clean_plans.plan_date("2026_09_17_tidy_rules.md") == date(2026, 9, 17), "Date prefix should parse"


def test_plan_date_none_for_bad_names():
    """Undated names and impossible dates give None."""
    assert clean_plans.plan_date("notes.md") is None, "An undated name should give None"
    assert clean_plans.plan_date("2026_13_40_bad_date.md") is None, "An impossible date should give None"


# ── choosing what to archive ──────────────────────────────────────────────────


def test_find_candidates_picks_only_old_finished_plans(tmp_path):
    """Only finished plans at least min_age_days old are picked."""
    write_plan(tmp_path, "2026_09_01_old_done.md", plan_text("✅ Done"))
    write_plan(tmp_path, "2026_09_01_old_pending.md", plan_text("⏳ Pending"))
    write_plan(tmp_path, "2026_09_30_new_done.md", plan_text("✅ Done"))
    write_plan(tmp_path, "undated_done.md", plan_text("✅ Done"))
    names = [path.name for path in clean_plans.find_candidates(tmp_path, min_age_days=14, today=TODAY)]
    assert names == ["2026_09_01_old_done.md"], f"Only the old finished plan should be picked, got {names}"


def test_find_candidates_follows_plan_status(tmp_path):
    """Dropped plans are archived, and a stated Active or Parked plan is kept even with every phase Done."""
    write_plan(tmp_path, "2026_09_01_dropped.md", "**Plan status:** 🗑️ Dropped\n" + plan_text("⏳ Pending"))
    write_plan(tmp_path, "2026_09_01_done.md", "**Plan status:** ✅ Done\n" + plan_text("✅ Done"))
    write_plan(tmp_path, "2026_09_01_active.md", "**Plan status:** 🟢 Active\n" + plan_text("✅ Done"))
    write_plan(tmp_path, "2026_09_01_parked.md", "**Plan status:** ⏸️ Parked\n" + plan_text("✅ Done"))
    names = [path.name for path in clean_plans.find_candidates(tmp_path, min_age_days=14, today=TODAY)]
    assert names == ["2026_09_01_done.md", "2026_09_01_dropped.md"], f"Only Done and Dropped should go, got {names}"


def test_recent_dropped_plan_is_kept(tmp_path):
    """The age floor applies to Dropped plans too, so a plan dropped by mistake can still be found."""
    write_plan(tmp_path, "2026_09_30_dropped.md", "**Plan status:** Dropped\n")
    assert clean_plans.find_candidates(tmp_path, min_age_days=14, today=TODAY) == [], "a recent drop must be kept"


def test_find_candidates_skips_archive_folder(tmp_path):
    """Plans already in archive/ are never picked again."""
    archive = tmp_path / "archive"
    archive.mkdir()
    write_plan(archive, "2026_09_01_old_done.md", plan_text("✅ Done"))
    assert clean_plans.find_candidates(tmp_path, today=TODAY) == [], "archive/ should not be scanned"


# ── the full run ──────────────────────────────────────────────────────────────


def test_main_archives_on_yes(tmp_path, monkeypatch):
    """Answering y moves finished plans into archive/ and leaves the rest."""
    write_plan(tmp_path, "2026_09_01_old_done.md", plan_text("✅ Done"))
    write_plan(tmp_path, "2026_09_01_old_pending.md", plan_text("⏳ Pending"))
    monkeypatch.setattr(builtins, "input", lambda _prompt: "y")
    clean_plans.main(plans_dir=tmp_path, today=TODAY, drafts_dir=tmp_path / "no_drafts")
    assert (tmp_path / "archive" / "2026_09_01_old_done.md").exists(), "Finished plan should move to archive/"
    assert not (tmp_path / "2026_09_01_old_done.md").exists(), "Finished plan should leave _plans/"
    assert (tmp_path / "2026_09_01_old_pending.md").exists(), "Unfinished plan should stay"


def test_main_moves_nothing_on_no(tmp_path, monkeypatch):
    """Any answer other than y leaves every plan in place."""
    write_plan(tmp_path, "2026_09_01_old_done.md", plan_text("✅ Done"))
    monkeypatch.setattr(builtins, "input", lambda _prompt: "n")
    with pytest.raises(SystemExit):
        clean_plans.main(plans_dir=tmp_path, today=TODAY, drafts_dir=tmp_path / "no_drafts")
    assert (tmp_path / "2026_09_01_old_done.md").exists(), "Plan should stay when the user says no"
    assert not (tmp_path / "archive").exists(), "archive/ should not be created when the user says no"


def test_default_plans_dir_uses_config_dir(monkeypatch, tmp_path):
    """The default folder is $CLAUDE_CONFIG_DIR/_plans."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    assert clean_plans._default_plans_dir() == tmp_path / "_plans", "Default should follow CLAUDE_CONFIG_DIR"


# ── plan-mode drafts ──────────────────────────────────────────────────────────


def write_draft(folder, name, days_old):
    """Write a draft with a modified time days_old before TODAY."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("# Draft\n")
    stamp = time.mktime(TODAY.timetuple()) - days_old * 86400 + 3600
    os.utime(path, (stamp, stamp))
    return path


def test_old_drafts_found_by_age_only(tmp_path):
    """Drafts 14 days old or more are picked, and newer ones and archive/ are left alone."""
    write_draft(tmp_path, "old-draft-name.md", 14)
    write_draft(tmp_path, "new-draft-name.md", 13)
    write_draft(tmp_path / "archive", "archived-draft.md", 40)
    names = [p.name for p in clean_plans.find_old_drafts(tmp_path, min_age_days=14, today=TODAY)]
    assert names == ["old-draft-name.md"], f"only the 14-day-old draft should go, got {names}"


def test_missing_drafts_folder_gives_nothing(tmp_path):
    """A config with no plans/ folder has no drafts to archive."""
    assert clean_plans.find_old_drafts(tmp_path / "plans", today=TODAY) == []


def test_main_archives_drafts_and_plans_together(tmp_path, monkeypatch):
    """One yes moves old drafts to plans/archive/ and finished plans to _plans/archive/."""
    plans, drafts = tmp_path / "_plans", tmp_path / "plans"
    plans.mkdir()
    write_plan(plans, "2026_09_01_old_done.md", plan_text("✅ Done"))
    write_draft(drafts, "abandoned-draft.md", 20)
    write_draft(drafts, "current-draft.md", 1)
    monkeypatch.setattr(builtins, "input", lambda _prompt: "y")
    clean_plans.main(plans_dir=plans, today=TODAY)
    assert (drafts / "archive" / "abandoned-draft.md").exists(), "an old draft should move to plans/archive/"
    assert (drafts / "current-draft.md").exists(), "a recent draft should stay"
    assert (plans / "archive" / "2026_09_01_old_done.md").exists(), "the finished plan should still be archived"


def test_main_archives_drafts_when_no_plan_is_finished(tmp_path, monkeypatch):
    """Old drafts are archived even when no saved plan is ready, rather than the run stopping early."""
    plans, drafts = tmp_path / "_plans", tmp_path / "plans"
    plans.mkdir()
    write_draft(drafts, "abandoned-draft.md", 20)
    monkeypatch.setattr(builtins, "input", lambda _prompt: "y")
    clean_plans.main(plans_dir=plans, today=TODAY)
    assert (drafts / "archive" / "abandoned-draft.md").exists(), "drafts must not wait for a finished plan"
