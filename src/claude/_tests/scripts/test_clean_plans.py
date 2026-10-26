# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-26
# Version:           2.3.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that clean_plans.py files plans and drafts into status subfolders.

A plan's Plan status line decides its folder, and a plan without one counts as
Done only when every Status cell in its phase table reads Done. Drafts are filed
by age alone, and nothing is ever overwritten or moved without a yes.
"""

import builtins
import importlib.util
import os
import time
from datetime import date

import pytest

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "scripts" / "_clean_scripts" / "clean_plans.py"
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


def test_table_without_status_column_is_passed_over():
    """A table with no Status column is skipped, and the next table that has one is read."""
    text = "| Item | Owner |\n|---|---|\n| x | me |\n\n" + plan_text("✅ Done")
    assert clean_plans.phase_statuses(text) == ["✅ Done"], "the Status table after a plain table should be read"


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


def test_draft_status_is_read_and_never_filed_as_done(tmp_path):
    """A Draft line parses, and a Draft left in _plans/ files as draft, even with every phase Done."""
    assert clean_plans.plan_status("**Plan status:** 📝 Draft · updated 2026-09-01\n") == ("Draft", True)
    write_plan(tmp_path, "2026_09_01_draft.md", "**Plan status:** 📝 Draft\n" + plan_text("✅ Done"))
    moves = clean_plans.find_plan_moves(tmp_path)
    assert [target.name for _, target in moves] == ["draft"], f"a Draft must file as draft, not done: {moves}"


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


# ── filing saved plans ────────────────────────────────────────────────────────


def moves_by_name(moves):
    """Map each moved file's name to its target folder's name."""
    return {path.name: target.name for path, target in moves}


def test_each_status_files_into_its_own_folder(tmp_path):
    """Active, Parked, Done and Dropped plans each go to the subfolder named after their status."""
    for status in ("Active", "Parked", "Done", "Dropped"):
        write_plan(tmp_path, f"2026_09_01_{status.lower()}.md", f"**Plan status:** {status}\n")
    expected = {f"2026_09_01_{s}.md": s for s in ("active", "parked", "done", "dropped")}
    assert moves_by_name(clean_plans.find_plan_moves(tmp_path)) == expected


def test_legacy_plan_files_by_inferred_status(tmp_path):
    """A plan with no status line files by its phase table: all Done to done/, anything else to active/."""
    write_plan(tmp_path, "2026_09_01_finished.md", plan_text("✅ Done"))
    write_plan(tmp_path, "2026_09_01_unfinished.md", plan_text("✅ Done", "⏳ Pending"))
    moves = moves_by_name(clean_plans.find_plan_moves(tmp_path))
    assert moves == {"2026_09_01_finished.md": "done", "2026_09_01_unfinished.md": "active"}, moves


def test_plan_already_in_its_folder_stays(tmp_path):
    """A filed plan whose status hasn't changed isn't moved again."""
    (tmp_path / "active").mkdir()
    write_plan(tmp_path / "active", "2026_09_01_a.md", "**Plan status:** Active\n")
    assert clean_plans.find_plan_moves(tmp_path) == [], "a correctly filed plan should stay put"


def test_status_change_moves_a_filed_plan(tmp_path):
    """A plan in active/ whose line now says Done moves to done/ — the line, not the folder, is the truth."""
    (tmp_path / "active").mkdir()
    write_plan(tmp_path / "active", "2026_09_01_a.md", "**Plan status:** Done\n")
    assert moves_by_name(clean_plans.find_plan_moves(tmp_path)) == {"2026_09_01_a.md": "done"}


def test_other_subfolders_are_never_read(tmp_path):
    """Plans in a non-status folder, such as the old archive/, are left alone."""
    (tmp_path / "archive").mkdir()
    write_plan(tmp_path / "archive", "2026_09_01_old.md", "**Plan status:** Active\n")
    assert clean_plans.saved_plan_files(tmp_path) == [], "archive/ should not be read"


# ── filing drafts ─────────────────────────────────────────────────────────────


def write_draft(folder, name, days_old):
    """Write a draft with a modified time days_old before TODAY."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("# Draft\n")
    stamp = time.mktime(TODAY.timetuple()) - days_old * 86400 + 3600
    os.utime(path, (stamp, stamp))
    return path


def test_drafts_file_by_age(tmp_path):
    """Today's drafts stay, older ones go to draft/, and 14-day-old ones go to archive/."""
    write_draft(tmp_path, "today-draft.md", 0)
    write_draft(tmp_path, "recent-draft.md", 3)
    write_draft(tmp_path, "old-draft.md", 14)
    write_draft(tmp_path / "draft", "filed-old-draft.md", 20)
    moves = moves_by_name(clean_plans.find_draft_moves(tmp_path, today=TODAY))
    expected = {"recent-draft.md": "draft", "old-draft.md": "archive", "filed-old-draft.md": "archive"}
    assert moves == expected, f"drafts filed wrongly: {moves}"


def test_filed_recent_draft_stays(tmp_path):
    """A draft already in draft/ and under 14 days old isn't moved again."""
    write_draft(tmp_path / "draft", "filed-draft.md", 5)
    assert clean_plans.find_draft_moves(tmp_path, today=TODAY) == []


# ── the full run ──────────────────────────────────────────────────────────────


def setup_config(tmp_path):
    """Build a config with one unfiled saved plan and one 3-day-old draft."""
    plans, drafts = tmp_path / "_plans", tmp_path / "plans"
    plans.mkdir()
    write_plan(plans, "2026_09_01_done.md", "**Plan status:** Done\n")
    write_draft(drafts, "some-draft.md", 3)
    return plans, drafts


def test_main_files_plans_and_drafts_on_yes(tmp_path, monkeypatch):
    """One yes files saved plans and drafts together, keeping drafts' modified times."""
    plans, drafts = setup_config(tmp_path)
    before = (drafts / "some-draft.md").stat().st_mtime
    monkeypatch.setattr(builtins, "input", lambda _prompt: "y")
    clean_plans.main(plans_dir=plans, today=TODAY)
    assert (plans / "done" / "2026_09_01_done.md").exists(), "the Done plan should move to done/"
    assert (drafts / "draft" / "some-draft.md").stat().st_mtime == before, "filing must keep a draft's age"


def test_main_moves_nothing_on_no(tmp_path, monkeypatch):
    """Any answer other than y leaves everything in place."""
    plans, drafts = setup_config(tmp_path)
    monkeypatch.setattr(builtins, "input", lambda _prompt: "n")
    with pytest.raises(SystemExit):
        clean_plans.main(plans_dir=plans, today=TODAY)
    assert (plans / "2026_09_01_done.md").exists() and (drafts / "some-draft.md").exists(), "nothing should move"


def test_main_never_overwrites(tmp_path, monkeypatch, capsys):
    """If the target folder already holds a file of the same name, the move is skipped and reported."""
    plans, _ = setup_config(tmp_path)
    (plans / "done").mkdir()
    write_plan(plans / "done", "2026_09_01_done.md", "**Plan status:** Done\n# existing\n")
    monkeypatch.setattr(builtins, "input", lambda _prompt: "y")
    clean_plans.main(plans_dir=plans, today=TODAY)
    kept = (plans / "done" / "2026_09_01_done.md").read_text()
    assert kept.endswith("# existing\n"), "the existing file was overwritten"
    assert "Skipped (already in done/)" in capsys.readouterr().out


def test_yes_moves_without_asking(tmp_path, monkeypatch, capsys):
    """With assume_yes, as make install runs it, everything is filed without a question and one line is printed."""
    plans, drafts = setup_config(tmp_path)
    monkeypatch.setattr(builtins, "input", lambda _prompt: pytest.fail("assume_yes must not ask"))
    clean_plans.main(plans_dir=plans, today=TODAY, assume_yes=True)
    assert (plans / "done" / "2026_09_01_done.md").exists(), "the plan should be filed"
    assert capsys.readouterr().out.strip() == "Filed 1 plans and 1 drafts into their status folders"


def test_yes_with_nothing_to_file_prints_nothing(tmp_path, capsys):
    """An already-filed config adds nothing to the install output."""
    (tmp_path / "_plans").mkdir()
    clean_plans.main(plans_dir=tmp_path / "_plans", today=TODAY, assume_yes=True)
    assert capsys.readouterr().out == "", "nothing to file should print nothing"


def test_default_plans_dir_uses_config_dir(monkeypatch, tmp_path):
    """The default folder is $CLAUDE_CONFIG_DIR/_plans."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    assert clean_plans._default_plans_dir() == tmp_path / "_plans", "Default should follow CLAUDE_CONFIG_DIR"


def test_default_plans_dir_falls_back_to_home(monkeypatch, tmp_path):
    """With CLAUDE_CONFIG_DIR unset, the default is ~/.claude/_plans, resolved through Path.home()."""
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    monkeypatch.setattr(clean_plans.Path, "home", lambda: tmp_path)
    assert clean_plans._default_plans_dir() == tmp_path / ".claude" / "_plans", "Unset should fall back to ~/.claude"


def test_no_folders_says_so_when_asked(tmp_path, capsys):
    """With neither folder present, an interactive run says where it looked."""
    clean_plans.main(plans_dir=tmp_path / "_plans", today=TODAY)
    assert "No plans folder found" in capsys.readouterr().out


def test_no_folders_prints_nothing_on_yes(tmp_path, capsys):
    """With neither folder present, the install's --yes run adds nothing to its output."""
    clean_plans.main(plans_dir=tmp_path / "_plans", today=TODAY, assume_yes=True)
    assert capsys.readouterr().out == "", "a missing folder should print nothing under --yes"


def test_nothing_to_file_says_so_when_asked(tmp_path, monkeypatch, capsys):
    """An already-filed config tells an interactive user so, without asking anything."""
    (tmp_path / "_plans").mkdir()
    monkeypatch.setattr(builtins, "input", lambda _prompt: pytest.fail("nothing to move, so nothing to ask"))
    clean_plans.main(plans_dir=tmp_path / "_plans", today=TODAY)
    assert "already in its status folder" in capsys.readouterr().out


@pytest.mark.parametrize("interrupt", [EOFError, KeyboardInterrupt])
def test_closed_input_aborts_cleanly(tmp_path, monkeypatch, capsys, interrupt):
    """Ctrl-D or Ctrl-C at the question exits 0 and moves nothing."""
    plans, drafts = setup_config(tmp_path)

    def stop(_prompt):
        raise interrupt

    monkeypatch.setattr(builtins, "input", stop)
    with pytest.raises(SystemExit) as exit_info:
        clean_plans.main(plans_dir=plans, today=TODAY)
    assert exit_info.value.code == 0, f"expected exit 0, got {exit_info.value.code}"
    assert "Aborted." in capsys.readouterr().out
    assert (plans / "2026_09_01_done.md").exists() and (drafts / "some-draft.md").exists(), "nothing should move"
