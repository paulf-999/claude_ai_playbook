# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-02
# Version:           1.4.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates audit_rule_usage.py against small fixture rules and transcripts.

The audit counts, for each rule, the sessions it applied to and the sessions it was
loaded in, then flags rules and appends a history row per rule. Each test builds a
tiny rules folder and transcript set in ``tmp_path``, so no real session data is read.
"""

import csv
import importlib.util
import json
import sys
from datetime import date, timedelta

import pytest

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "_scripts" / "_audit_scripts" / "audit_rule_usage.py"
TODAY = date(2026, 10, 1)
GUIDES = "05_lazy_load/style_guide_standards"


def load_audit():
    """Import the audit script as a module.

    :return: The loaded module.
    :rtype: module
    """
    spec = importlib.util.spec_from_file_location("audit_rule_usage", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up by name
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit()


def make_rules(tmp_path):
    """Build a rules folder with one always-on parent, one child and four lazy rules.

    :param tmp_path: Pytest tmp_path fixture.
    :return: The ``_rules`` folder.
    :rtype: Path
    """
    rules = tmp_path / "_rules"
    (rules / "01_essentials" / "parent").mkdir(parents=True)
    child_import = "@~/.claude/_rules/01_essentials/parent/_child.md"
    (rules / "01_essentials" / "parent.md").write_text(f"# Parent\n\n## Big\n{'x' * 400}\n{child_import}\n")
    (rules / "01_essentials" / "parent" / "_child.md").write_text("# Child\n\n## Small\n" + "y" * 40 + "\n")
    (rules / "01_essentials" / "README.md").write_text("# Tier\n")
    guides = rules / "05_lazy_load" / "style_guide_standards"
    guides.mkdir(parents=True)
    (guides / "python.md").write_text("<!-- miss_cost: high — breaks style -->\n# Python\n")
    (guides / "sql.md").write_text('---\npaths:\n  - "**/*.sql"\n---\n# SQL\n')
    (rules / "05_lazy_load" / "loose.md").write_text("<!-- miss_cost: low — style -->\n# Loose\n")
    return rules


def write_session(folder, name, day, records):
    """Write one transcript as JSON lines, stamping each record with a date.

    :param folder: Project folder.
    :param name: File stem.
    :param day: The session date.
    :param records: Transcript records.
    """
    folder.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({**r, "timestamp": f"{day}T10:00:00.000Z"}) for r in records]
    (folder / f"{name}.jsonl").write_text("\n".join(lines) + "\n")


def tool(name, path):
    """Build an assistant record that calls a file tool.

    :param name: Tool name, e.g. ``Read``.
    :param path: The file path argument.
    :return: The record.
    :rtype: dict
    """
    call = {"type": "tool_use", "name": name, "input": {"file_path": path}}
    return {"type": "assistant", "message": {"content": [call]}}


def make_transcripts(tmp_path):
    """Build three sessions in one project, plus a sub-agent log that must be skipped.

    - **s1:** edits a .py file and reads python.md, with the always-on parent at startup.
    - **s2:** edits a .py and a .sql file, sql.md auto-loads, python.md never loads.
    - **s3:** touches nothing, with no startup file list.

    :param tmp_path: Pytest tmp_path fixture.
    :return: The transcripts folder.
    :rtype: Path
    """
    project = tmp_path / "projects" / "-repo"
    startup = {"type": "attachment", "attachment": {"type": "instructions", "files": [
        {"path": "/home/u/.claude/_rules/01_essentials/parent.md"}]}}
    write_session(project, "s1", "2026-09-10", [
        startup, tool("Edit", "/repo/app.py"), tool("Read", f"/repo/src/claude/_rules/{GUIDES}/python.md")])
    write_session(project, "s2", "2026-09-20", [
        startup, tool("Write", "/repo/x.py"), tool("Edit", "/repo/q.sql"),
        {"type": "attachment", "attachment": {"type": "nested_memory", "path": f"/u/claude/_rules/{GUIDES}/sql.md"}}])
    write_session(project, "s3", "2026-09-25", [{"type": "user", "message": {"content": "hi"}}])
    write_session(project / "s1" / "subagents", "agent", "2026-09-30", [tool("Edit", "/repo/sub.py")])
    return tmp_path / "projects"


def usage_by_rule(tmp_path):
    """Measure the fixture data.

    :param tmp_path: Pytest tmp_path fixture.
    :return: Usage keyed by the rule's file name.
    :rtype: dict
    """
    rules_dir = make_rules(tmp_path)
    sessions = AUDIT.discover_sessions(make_transcripts(tmp_path), rules_dir)
    return {u.rule.rel.rsplit("/", 1)[1]: u for u in AUDIT.measure(AUDIT.discover_rules(rules_dir), sessions)}


def test_children_and_readmes_are_not_entry_points(tmp_path):
    """Only parent.md, python.md, sql.md and loose.md count as rules."""
    names = sorted(r.rel.rsplit("/", 1)[1] for r in AUDIT.discover_rules(make_rules(tmp_path)))
    assert names == ["loose.md", "parent.md", "python.md", "sql.md"], f"unexpected entry points {names}"


def test_always_on_tokens_include_imported_children(tmp_path):
    """An always-on rule's tokens cover its @imports, and its globs cover every session."""
    parent = next(r for r in AUDIT.discover_rules(make_rules(tmp_path)) if r.rel.endswith("parent.md"))
    assert parent.files == ["01_essentials/parent.md", "01_essentials/parent/_child.md"], parent.files
    assert parent.tokens > 100, f"tokens should include the 400-char section, got {parent.tokens}"
    assert parent.globs == ["*"], "always-on rules apply to every session"


def test_globs_come_from_paths_then_defaults(tmp_path):
    """sql.md uses its paths: frontmatter, python.md the built-in default, loose.md has none."""
    rules = {r.rel.rsplit("/", 1)[1]: r for r in AUDIT.discover_rules(make_rules(tmp_path))}
    assert rules["sql.md"].globs == ["**/*.sql"], rules["sql.md"].globs
    assert rules["python.md"].globs == ["**/*.py"], rules["python.md"].globs
    assert rules["loose.md"].globs == [], "a rule with no trigger has no globs"


def test_applies_to_header_wins_over_fallbacks(tmp_path):
    """An applies_to header replaces * on an always-on rule and paths: on a lazy rule."""
    rules_dir = make_rules(tmp_path)
    parent = rules_dir / "01_essentials" / "parent.md"
    parent.write_text("<!-- version: 1.0.0 -->\n<!-- applies_to: **/_rules/**, **/CLAUDE.md -->\n" + parent.read_text())
    sql = rules_dir / GUIDES / "sql.md"
    sql.write_text(sql.read_text().replace("---\n# SQL", "---\n<!-- applies_to: **/models/**/*.sql -->\n# SQL"))
    rules = {r.rel.rsplit("/", 1)[1]: r for r in AUDIT.discover_rules(rules_dir)}
    assert rules["parent.md"].globs == ["**/_rules/**", "**/CLAUDE.md"], rules["parent.md"].globs
    assert rules["sql.md"].globs == ["**/models/**/*.sql"], rules["sql.md"].globs


def test_header_globs_found_below_paths_frontmatter():
    """A path-scoped rule's applies_to, below its frontmatter and 3-line header, is still read."""
    text = (
        '---\npaths:\n  - "**/*.sql"\n---\n<!-- version: 1.0.0 -->\n<!-- created: 2026-10-01 -->\n'
        "<!-- updated: 2026-10-01 -->\n<!-- applies_to: **/models/**/*.sql -->\n# SQL\n"
    )
    assert AUDIT.header_globs(text) == ["**/models/**/*.sql"], AUDIT.header_globs(text)


def test_header_globs_ignore_examples_in_the_body():
    """Only an applies_to line in the header block counts, not an example further down."""
    body = "# Rule\n" + "text\n" * AUDIT.HEADER_LINES + "<!-- applies_to: **/*.py -->\n"
    assert AUDIT.header_globs(body) == [], "an example in the body was read as the header"
    assert AUDIT.header_globs("<!-- applies_to: *, -->\n") == ["*"], "empty entries should be dropped"


def test_miss_cost_read_from_header(tmp_path):
    """A miss_cost header sets the rule's cost, and its absence shows a dash."""
    rules = {r.rel.rsplit("/", 1)[1]: r for r in AUDIT.discover_rules(make_rules(tmp_path))}
    assert rules["python.md"].miss_cost == "high", rules["python.md"].miss_cost
    assert rules["sql.md"].miss_cost == "—", rules["sql.md"].miss_cost


def test_applied_counts_sessions_touching_matching_files(tmp_path):
    """python.md applies in s1 and s2, sql.md only in s2, the parent in all three."""
    usage = usage_by_rule(tmp_path)
    assert usage["python.md"].applied == 2, usage["python.md"].applied
    assert usage["sql.md"].applied == 1, usage["sql.md"].applied
    assert usage["parent.md"].applied == 3, usage["parent.md"].applied
    assert usage["loose.md"].applied is None, "a rule with no trigger can't be measured"


def test_subagent_logs_are_skipped(tmp_path):
    """The sub-agent log isn't counted as a session."""
    sessions = AUDIT.discover_sessions(make_transcripts(tmp_path), make_rules(tmp_path))
    assert len(sessions) == 3, f"expected 3 main sessions, got {len(sessions)}"


def test_loaded_from_startup_auto_load_and_read(tmp_path):
    """Startup instructions, nested_memory and Read each count as loading a rule."""
    usage = usage_by_rule(tmp_path)
    assert usage["parent.md"].loaded == 2, "startup instructions in s1 and s2"
    assert usage["sql.md"].loaded == 1, "nested_memory auto-load in s2"
    assert usage["python.md"].loaded == 1, "Read in s1"


def test_misses_are_applied_but_not_loaded(tmp_path):
    """python.md applied in s2 without loading, and the parent was missing from s3's startup."""
    usage = usage_by_rule(tmp_path)
    assert usage["python.md"].misses == 1, usage["python.md"].misses
    assert usage["parent.md"].misses == 1, usage["parent.md"].misses
    assert usage["sql.md"].misses == 0, usage["sql.md"].misses


def test_last_applied_and_last_loaded_dates(tmp_path):
    """Last applied and last loaded use each session's date."""
    usage = usage_by_rule(tmp_path)
    assert usage["python.md"].last_applied == date(2026, 9, 20), usage["python.md"].last_applied
    assert usage["python.md"].last_loaded == date(2026, 9, 10), usage["python.md"].last_loaded


def test_symlinked_rule_path_maps_to_its_rule(tmp_path):
    """A rules/ symlink read by Claude Code maps back to the real rule."""
    rules_dir = make_rules(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "sql.md").symlink_to(rules_dir / "05_lazy_load" / "style_guide_standards" / "sql.md")
    rel = AUDIT.rule_rel(str(tmp_path / "rules" / "sql.md"), rules_dir)
    assert rel == "05_lazy_load/style_guide_standards/sql.md", rel
    assert AUDIT.rule_rel("/repo/app.py", rules_dir) is None, "a non-rule path maps to nothing"


def test_section_sizes_are_largest_first(tmp_path):
    """Section sizes cover always-on files and their imports, biggest first."""
    rules_dir = make_rules(tmp_path)
    sizes = AUDIT.section_sizes(rules_dir, AUDIT.discover_rules(rules_dir))
    assert [s[1] for s in sizes] == ["Big", "Small"], sizes


def usage(always_on, applied, misses, miss_cost):
    """Build a Usage row for flag tests.

    :return: The row.
    :rtype: Usage
    """
    tier = "01_essentials" if always_on else "05_lazy_load"
    rule = AUDIT.Rule(rel="x.md", tier=tier, tokens=1, globs=["*"], miss_cost=miss_cost)
    return AUDIT.Usage(rule, 100, applied, 0, misses, None, None)


def test_flag_not_enough_data_below_minimum():
    """Fewer applied sessions than the minimum sample suppresses every other flag."""
    flag = AUDIT.flag_for(usage(False, AUDIT.MIN_SAMPLE_SESSIONS - 1, 5, "high"), None, None, TODAY)
    assert flag == "not enough data", flag


def test_flag_promote_and_demote():
    """A missed high-cost lazy rule is promoted, and a rarely applied low-cost always-on rule is demoted."""
    recent = TODAY - timedelta(days=1)
    assert AUDIT.flag_for(usage(False, 20, 3, "high"), recent, None, TODAY) == "promote"
    assert AUDIT.flag_for(usage(True, 20, 0, "low"), recent, None, TODAY) == "demote"
    assert AUDIT.flag_for(usage(True, 90, 0, "low"), recent, None, TODAY) == "", "applied above the cut-off"


def test_flag_stale_after_cutoff():
    """A rule last used before the cut-off is stale, and one with no trigger says so."""
    old = TODAY - timedelta(days=AUDIT.STALE_AFTER_DAYS + 1)
    assert AUDIT.flag_for(usage(False, 20, 0, "medium"), old, None, TODAY) == "stale"
    assert AUDIT.flag_for(usage(False, None, None, "—"), None, None, TODAY) == "no trigger"


def test_history_appends_one_row_per_rule_per_run(tmp_path):
    """Each run appends one row per rule under a single header, and the report is written."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    rows = list(csv.DictReader((out / AUDIT.HISTORY_NAME).open()))
    assert len(rows) == 8, f"2 runs × 4 rules should give 8 rows, got {len(rows)}"
    assert (out / AUDIT.REPORT_NAME).read_text().startswith("# 📊 Rule usage audit"), "report not written"


def test_history_keeps_last_use_after_logs_are_gone(tmp_path):
    """read_history returns each rule's latest use and the first run date."""
    path = tmp_path / "history.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT.HISTORY_FIELDS)
        writer.writeheader()
        writer.writerow({"run_date": "2026-06-01", "rule": "a.md", "last_applied": "2026-05-20", "last_loaded": ""})
    last_used, first_run = AUDIT.read_history(path)
    assert last_used == {"a.md": date(2026, 5, 20)}, last_used
    assert first_run == date(2026, 6, 1), first_run


def test_missing_arguments_exit_with_usage(capsys):
    """Leaving out a required argument stops with argparse's usage error."""
    with pytest.raises(SystemExit) as stop:
        AUDIT.main(["--rules", "x"])
    assert stop.value.code == 2, f"expected exit 2, got {stop.value.code}"
    assert "--transcripts" in capsys.readouterr().err, "the error should name the missing argument"


def test_missing_folder_returns_error(tmp_path, capsys):
    """A rules folder that doesn't exist exits 1 and names the flag."""
    code = AUDIT.main(["--rules", str(tmp_path / "nope"), "--transcripts", str(tmp_path), "--out", str(tmp_path)])
    assert code == 1, f"expected exit 1, got {code}"
    assert "--rules folder not found" in capsys.readouterr().err, "stderr should name the missing folder"


# --- All-time session ledger and summary ---

def ledger_rows(out):
    """Read the ledger CSV.

    :param out: The output folder.
    :return: Ledger rows.
    :rtype: list[dict]
    """
    return list(csv.DictReader((out / AUDIT.LEDGER_NAME).open()))


def python_row(out):
    """Return the python.md line from the summary.

    :param out: The output folder.
    :return: The table line.
    :rtype: str
    """
    lines = (out / AUDIT.SUMMARY_NAME).read_text().splitlines()
    return next(line for line in lines if line.startswith("| `") and "python.md`" in line)


def test_ledger_counts_each_session_once_across_runs(tmp_path):
    """Two runs over the same logs record each session once per rule, not twice."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    first = ledger_rows(out)
    AUDIT.run(rules_dir, transcripts, out, TODAY + timedelta(days=7))
    assert ledger_rows(out) == first, "a second run over the same sessions changed the ledger"
    keys = [(r["session"], r["rule"]) for r in first]
    assert len(keys) == len(set(keys)), "a session appears twice for one rule"


def test_ledger_keeps_sessions_whose_logs_are_gone(tmp_path):
    """A session deleted from disk keeps its rows, so all-time totals don't shrink."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    (transcripts / "-repo" / "s1.jsonl").unlink()
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    python = [r for r in ledger_rows(out) if r["rule"].endswith("python.md")]
    assert sorted(r["session"] for r in python) == ["s1", "s2"], python


def test_ledger_replaces_rows_for_a_session_seen_again(tmp_path):
    """A session that grows between runs is re-measured, not added a second time."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    write_session(transcripts / "-repo", "s3", "2026-09-25", [tool("Edit", "/repo/late.py")])
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    s3 = [r for r in ledger_rows(out) if r["session"] == "s3"]
    assert [(r["rule"].rsplit("/", 1)[1], r["applied"]) for r in s3] == [("parent.md", "1"), ("python.md", "1")], s3


def test_summary_shows_all_time_totals(tmp_path):
    """The summary row gives applied, loaded, misses, miss rate, runs and dates for a rule."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    AUDIT.run(rules_dir, transcripts, out, TODAY + timedelta(days=1))
    expected = "| `05_lazy_load/style_guide_standards/python.md` | 2 | 1 | 1 | 50% | 2 | 2026-09-10 | 2026-09-20 |"
    assert python_row(out) == expected, python_row(out)
    assert "**Sessions recorded:** 3 (2026-09-10 to 2026-09-25) · **Runs:** 2" in (out / AUDIT.SUMMARY_NAME).read_text()


def test_summary_marks_removed_rules(tmp_path):
    """A deleted rule keeps its rows from sessions whose logs are gone, and is marked removed."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    (rules_dir / GUIDES / "python.md").unlink()
    (transcripts / "-repo" / "s1.jsonl").unlink()
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    assert "(removed)" in python_row(out), python_row(out)
    assert "| 1 | 1 | 0 | 0% |" in python_row(out), "only s1's row should survive, since s2 was re-measured"


def test_summary_has_one_table_per_tier(tmp_path):
    """Rules are grouped into a titled table per tier, each rule under its own tier."""
    rules_dir, transcripts, out = make_rules(tmp_path), make_transcripts(tmp_path), tmp_path / "out"
    AUDIT.run(rules_dir, transcripts, out, TODAY)
    text = (out / AUDIT.SUMMARY_NAME).read_text()
    essentials, lazy = text.index("### 🧭 01 Essentials"), text.index("### 💤 05 Lazy load")
    assert essentials < text.index("parent.md` |") < lazy, "parent.md should sit in the 01 Essentials table"
    assert lazy < text.index("python.md` |"), "python.md should sit in the 05 Lazy load table"


def totals(applied, loaded, misses):
    """Build one rule's totals for insight tests.

    :return: The totals dict.
    :rtype: dict
    """
    return {"applied": applied, "loaded": loaded, "misses": misses,
            "rate": misses / applied if applied else None, "first": "—", "last": "—"}


def test_insights_rank_worst_miss_rates_with_enough_data():
    """Miss-rate insights rank by rate and skip rules under the minimum sample."""
    data = {"a.md": totals(20, 10, 10), "b.md": totals(30, 3, 27), "tiny.md": totals(2, 0, 2)}
    lines = AUDIT.insight_lines(data, set())
    ranked = [line for line in lines if line[:2] in ("1.", "2.") and "missed" in line]
    expected = ["1. `b.md` — missed 27 of 30 sessions (90%)", "2. `a.md` — missed 10 of 20 sessions (50%)"]
    assert ranked == expected, ranked
    assert any("1 more rules have misses" in line for line in lines), "rules under the minimum sample should be counted"


def test_insights_show_most_used_rules():
    """Every-session rules are summarised together, and the rest are ranked by sessions applied."""
    data = {"star.md": totals(100, 95, 5), "big.md": totals(40, 38, 2), "small.md": totals(12, 12, 0)}
    lines = AUDIT.insight_lines(data, {"star.md"})
    assert any("**Every-session rules:** 1 rules" in line and "loaded in 95–95" in line for line in lines), lines
    assert "1. `big.md` — applied in 40 sessions, loaded in 38" in lines, lines
    assert "2. `small.md` — applied in 12 sessions, loaded in 12" in lines, lines
