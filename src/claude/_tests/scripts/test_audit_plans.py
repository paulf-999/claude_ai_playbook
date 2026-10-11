# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-11
# Date updated:      2026-10-11
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that audit_plans.py lists saved plans by plan status and flags stale Active ones.

Saved plans pile up, and only the ones still being acted on matter, so the listing must
put Active and Parked plans first, never list archived plans, mark statuses it
had to infer, and flag Active plans untouched for 14 days so they can be parked or dropped.
"""

import importlib.util
import os
import time
from datetime import date

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "scripts" / "_audit_scripts" / "audit_plans.py"
TODAY = date(2026, 10, 11)
TABLE = "| Phase | Action | Status |\n|---|---|---|\n| 1 | a | ✅ Done |\n| 2 | b | ⏳ Pending |\n"


def load_audit_plans():
    """Import audit_plans.py as a module."""
    spec = importlib.util.spec_from_file_location("audit_plans", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit_plans()


def write_plan(folder, name, status=None, days_old=0, table=TABLE):
    """Write a plan file, backdating its modified time by days_old from TODAY."""
    line = f"**Plan status:** {status}\n\n" if status else ""
    path = folder / f"{name}.md"
    path.write_text(f"# Plan\n\n{line}{table}")
    stamp = time.mktime(TODAY.timetuple()) - days_old * 86400 + 3600
    os.utime(path, (stamp, stamp))
    return path


# ── Reading one plan ────────────────────────────────────────────────────


def test_stated_status_and_phase_counts_are_read(tmp_path):
    """A plan's own status line wins, and its phase table gives the progress."""
    plan = AUDIT.read_plan(write_plan(tmp_path, "a", "⏸️ Parked", days_old=3), TODAY)
    assert (plan.status, plan.stated) == ("Parked", True), f"expected stated Parked, got {plan}"
    assert (plan.phases_done, plan.phases) == (1, 2), f"expected 1 of 2 phases done, got {plan}"
    assert plan.days_since_update == 3, f"expected 3 days since update, got {plan.days_since_update}"


def test_legacy_plan_status_is_inferred_and_marked(tmp_path):
    """A plan saved before the status line existed is inferred from its phases and marked as such."""
    plan = AUDIT.read_plan(write_plan(tmp_path, "legacy"), TODAY)
    assert (plan.status, plan.stated) == ("Active", False), f"unfinished legacy plan must read Active, got {plan}"
    assert "(no status line, inferred)" in AUDIT._line(plan), "an inferred status must be marked in the listing"


def test_status_line_date_wins_over_file_time(tmp_path):
    """A plan touched today but last progressed long ago is dated by its status line, so it can still go stale."""
    path = write_plan(tmp_path, "edited_today", "🟢 Active · updated 2026-09-01")
    plan = AUDIT.read_plan(path, TODAY)
    assert plan.days_since_update == 40, f"the status line date should win, got {plan.days_since_update}"
    assert [p.name for p in AUDIT.stale([plan])] == ["edited_today"], "an old updated date must flag the plan"


# ── Collecting the folder ───────────────────────────────────────────────


def test_most_recently_updated_plan_comes_first(tmp_path):
    """Plans are listed newest change first, so current work is at the top."""
    write_plan(tmp_path, "old", "Active", days_old=9)
    write_plan(tmp_path, "new", "Active", days_old=1)
    assert [p.name for p in AUDIT.collect(tmp_path, TODAY)] == ["new", "old"]


def test_status_subfolders_are_read(tmp_path):
    """Plans already filed in a status subfolder are listed like loose ones."""
    (tmp_path / "active").mkdir()
    write_plan(tmp_path / "active", "filed", "Active", days_old=1)
    write_plan(tmp_path, "loose", "Active", days_old=2)
    assert [p.name for p in AUDIT.collect(tmp_path, TODAY)] == ["filed", "loose"]


def test_unfiled_line_counts_plans_outside_their_folder(tmp_path):
    """A loose or misfiled plan is counted and points at the filing command, and none gives no line."""
    assert AUDIT.unfiled_line(tmp_path) == "", "an empty folder should add nothing"
    write_plan(tmp_path, "loose", "Active")
    line = AUDIT.unfiled_line(tmp_path)
    assert line.startswith("1 saved plans not in their status folder") and "make clean_plans" in line, line


def test_subfolders_are_never_listed(tmp_path):
    """Only _plans/ itself and its status subfolders count, so archive/ and any other folder stay out."""
    write_plan(tmp_path, "kept", "Active")
    for sub in ("archive", "notes"):
        (tmp_path / sub).mkdir()
        write_plan(tmp_path / sub, f"in_{sub}", "Active")
    names = [p.name for p in AUDIT.collect(tmp_path, TODAY)]
    assert names == ["kept"], f"subfolder plans leaked into the listing: {names}"


# ── Stale flag ──────────────────────────────────────────────────────────


def test_only_active_plans_go_stale(tmp_path):
    """Parked plans are deliberately on hold, so age alone never flags them."""
    for status in ("Active", "Parked", "Dropped"):
        write_plan(tmp_path, status.lower(), status, days_old=30)
    flagged = [p.name for p in AUDIT.stale(AUDIT.collect(tmp_path, TODAY))]
    assert flagged == ["active"], f"only the old Active plan should be stale, got {flagged}"


def test_stale_starts_at_fourteen_days(tmp_path):
    """13 days untouched is still current, and 14 days is stale."""
    write_plan(tmp_path, "day13", "Active", days_old=13)
    write_plan(tmp_path, "day14", "Active", days_old=14)
    flagged = [p.name for p in AUDIT.stale(AUDIT.collect(tmp_path, TODAY))]
    assert flagged == ["day14"], f"the cutoff should be 14 days, got {flagged}"


# ── Report ──────────────────────────────────────────────────────────────


def test_report_lists_active_before_parked(tmp_path):
    """Active plans are what you came for, so they print above Parked ones."""
    write_plan(tmp_path, "parked_plan", "Parked")
    write_plan(tmp_path, "active_plan", "Active", days_old=2)
    text = AUDIT.report(AUDIT.collect(tmp_path, TODAY))
    assert text.index("ACTIVE (1)") < text.index("PARKED (1)"), f"Active must come first:\n{text}"
    assert text.index("active_plan") < text.index("parked_plan"), f"plans must sit under their group:\n{text}"


def test_draft_left_in_saved_plans_is_still_listed(tmp_path):
    """A saved plan still marked Draft is listed after Active and Parked, so a missed save step shows up."""
    write_plan(tmp_path, "forgot_to_activate", "📝 Draft")
    write_plan(tmp_path, "parked_plan", "Parked")
    text = AUDIT.report(AUDIT.collect(tmp_path, TODAY))
    assert "DRAFT (1)" in text and "forgot_to_activate" in text, f"a Draft in _plans/ was hidden:\n{text}"
    assert text.index("PARKED (1)") < text.index("DRAFT (1)"), f"Draft should follow Parked:\n{text}"


def test_finished_plans_are_counted_not_listed(tmp_path):
    """Done and Dropped plans only add a count, not one line each."""
    write_plan(tmp_path, "done_plan", "Done")
    write_plan(tmp_path, "dropped_plan", "Dropped")
    text = AUDIT.report(AUDIT.collect(tmp_path, TODAY))
    assert "done_plan" not in text and "dropped_plan" not in text, f"finished plans were listed:\n{text}"
    assert "2 Done or Dropped." in text, f"missing the finished count:\n{text}"


def test_stale_section_names_the_plan_and_the_choice(tmp_path):
    """A stale plan appears in its own section that asks whether to park or drop it."""
    write_plan(tmp_path, "forgotten", "Active", days_old=20)
    text = AUDIT.report(AUDIT.collect(tmp_path, TODAY))
    stale_part = text.split("STALE", 1)[-1]
    assert "park or drop?" in stale_part, f"stale section must offer the choice:\n{text}"
    assert "forgotten" in stale_part, f"stale section must name the plan:\n{text}"


def test_empty_folder_says_so():
    """No plans gives a plain message rather than empty headings."""
    assert AUDIT.report([]) == "No saved plans."


# ── Entry point ─────────────────────────────────────────────────────────


def test_missing_folder_is_reported_not_raised(tmp_path, capsys):
    """A config with no _plans/ folder prints a message and exits cleanly."""
    AUDIT.main(plans_dir=tmp_path / "absent", today=TODAY)
    assert "No plans folder found" in capsys.readouterr().out


def test_default_folder_follows_config_dir(tmp_path, monkeypatch, capsys):
    """With no override, the listing reads $CLAUDE_CONFIG_DIR/_plans, like clean_plans.py."""
    (tmp_path / "_plans").mkdir()
    write_plan(tmp_path / "_plans", "from_config_dir", "Active")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    AUDIT.main(today=TODAY)
    assert "from_config_dir" in capsys.readouterr().out, "default folder must come from CLAUDE_CONFIG_DIR"


# ── Drafts line ─────────────────────────────────────────────────────────


def test_drafts_line_counts_and_points_at_cleanup(tmp_path):
    """The drafts line gives the total, how many need filing, and the command that files them."""
    write_plan(tmp_path, "old-draft", days_old=20)
    write_plan(tmp_path, "new-draft", days_old=1)
    line = AUDIT.drafts_line(tmp_path, TODAY)
    assert line.startswith(f"Drafts in {tmp_path.name}/: 2, 2 to file"), line
    assert "make clean_plans" in line, f"the line should name the filing command: {line}"


def test_drafts_line_is_quiet_without_drafts(tmp_path):
    """No drafts folder, or an empty one, adds nothing to the listing."""
    assert AUDIT.drafts_line(tmp_path / "absent", TODAY) == ""
    assert AUDIT.drafts_line(tmp_path, TODAY) == ""
