# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that clean_plans.py archives only finished, old-enough plans.

A plan is finished when every Status cell in its phase table reads Done. Anything
else — no table, a Pending or In Progress phase, a recent date or an undated
name — must stay in _plans/, because archiving a live plan would lose work.
"""

import builtins
import importlib.util
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
    clean_plans.main(plans_dir=tmp_path, today=TODAY)
    assert (tmp_path / "archive" / "2026_09_01_old_done.md").exists(), "Finished plan should move to archive/"
    assert not (tmp_path / "2026_09_01_old_done.md").exists(), "Finished plan should leave _plans/"
    assert (tmp_path / "2026_09_01_old_pending.md").exists(), "Unfinished plan should stay"


def test_main_moves_nothing_on_no(tmp_path, monkeypatch):
    """Any answer other than y leaves every plan in place."""
    write_plan(tmp_path, "2026_09_01_old_done.md", plan_text("✅ Done"))
    monkeypatch.setattr(builtins, "input", lambda _prompt: "n")
    with pytest.raises(SystemExit):
        clean_plans.main(plans_dir=tmp_path, today=TODAY)
    assert (tmp_path / "2026_09_01_old_done.md").exists(), "Plan should stay when the user says no"
    assert not (tmp_path / "archive").exists(), "archive/ should not be created when the user says no"


def test_default_plans_dir_uses_config_dir(monkeypatch, tmp_path):
    """The default folder is $CLAUDE_CONFIG_DIR/_plans."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    assert clean_plans._default_plans_dir() == tmp_path / "_plans", "Default should follow CLAUDE_CONFIG_DIR"
