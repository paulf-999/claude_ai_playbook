# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-30
# Version:           1.0.1
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Tests for claude_capture_session_prompts' capture_session_prompts.py script.

Covers the fixes made when the script was restored into the skill folder
(2026-09-30): the history file resolves from CLAUDE_CONFIG_DIR, output goes to
~/_sessions/ with a snake_case date-first name, and dates use local time.
Also pins the categorisation heuristics and markdown output the skill's
docs describe.
"""
import importlib.util
import json
from datetime import date, datetime
from pathlib import Path

import pytest

from _shared_paths import SKILLS_DIR

# Grouped in the playbook repo (skills/_claude_skills/<name>/), flat in a live
# config (skills/<name>/) — Claude Code only loads the flat layout.
SCRIPT = next(
    (SKILLS_DIR / rel / "capture_session_prompts.py" for rel in
     ("claude_capture_session_prompts", "_claude_skills/claude_capture_session_prompts")
     if (SKILLS_DIR / rel / "capture_session_prompts.py").is_file()),
    SKILLS_DIR / "claude_capture_session_prompts" / "capture_session_prompts.py",
)


def _load_script():
    """Import the skill script as a module.

    :return: The loaded module.
    """
    spec = importlib.util.spec_from_file_location("capture_session_prompts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


csp = _load_script()


def _ms(moment: datetime) -> int:
    """Convert a local datetime to a millisecond timestamp.

    :param moment: Local datetime.
    :return: Milliseconds since the epoch.
    """
    return int(moment.timestamp() * 1000)


def _write_history(path: Path, entries: list) -> None:
    """Write history entries (dicts or raw strings) as JSON lines.

    :param path: File to write.
    :param entries: Entries; strings are written verbatim to simulate corruption.
    """
    path.write_text("\n".join(e if isinstance(e, str) else json.dumps(e) for e in entries) + "\n")


def test_script_exists_in_skill_folder():
    """The script ships inside the skill folder that SKILL.md documents."""
    assert SCRIPT.is_file(), f"Missing skill script at {SCRIPT}"
    skill_md = (SCRIPT.parent / "SKILL.md").read_text()
    assert "capture_session_prompts.py" in skill_md, "SKILL.md must reference the script by name"


def test_config_dir_uses_claude_config_dir(monkeypatch, tmp_path):
    """History resolves from CLAUDE_CONFIG_DIR when it is set."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    assert csp.config_dir() == tmp_path


def test_config_dir_falls_back_to_dot_claude(monkeypatch, tmp_path):
    """Without CLAUDE_CONFIG_DIR, history resolves from ~/.claude (Claude Code's default)."""
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert csp.config_dir() == tmp_path / ".claude"


def test_default_output_dir_is_home_sessions(monkeypatch, tmp_path):
    """Output defaults to ~/_sessions, not the auto-generated config sessions/ dir."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert csp.default_output_dir() == tmp_path / "_sessions"


def test_output_filename_is_snake_case_date_first(tmp_path):
    """Output files are named YYYY_MM_DD_claude_prompts.md."""
    path = csp.output_path_for(date(2026, 8, 5), tmp_path)
    assert path.name == "2026_08_05_claude_prompts.md"
    assert "-" not in path.name, "Filename must be snake_case (no hyphens)"


def test_target_date_parses_or_defaults_to_today():
    """--date parses YYYY-MM-DD and defaults to today's local date."""
    assert csp.get_target_date("2026-08-20") == date(2026, 8, 20)
    assert csp.get_target_date() == date.today()
    with pytest.raises(ValueError):
        csp.get_target_date("2026-02-30")


def test_read_history_skips_malformed_lines(tmp_path):
    """Corrupt lines are skipped and a missing file yields no entries."""
    history = tmp_path / "history.jsonl"
    _write_history(history, [{"display": "a", "timestamp": 1}, "{not json", {"display": "b", "timestamp": 2}])
    entries = csp.read_history(history)
    assert [e["display"] for e in entries] == ["a", "b"]
    assert csp.read_history(tmp_path / "missing.jsonl") == []


def test_filter_by_date_keeps_only_target_day():
    """Only entries on the target local date survive, and entries without timestamps are dropped."""
    day = date(2026, 8, 20)
    entries = [
        {"display": "keep", "timestamp": _ms(datetime(2026, 8, 20, 9, 15))},
        {"display": "drop", "timestamp": _ms(datetime(2026, 8, 21, 9, 15))},
        {"display": "no timestamp"},
    ]
    assert [e["display"] for e in csp.filter_by_date(entries, day)] == ["keep"]


def test_theme_heuristics():
    """Theme keywords map to the themes the skill documents."""
    assert csp.categorize_theme("yes") == "Unclassified (-)"
    assert csp.categorize_theme("update the naming rule") == "Rules"
    assert csp.categorize_theme("fix the jira skill") == "Skills"
    assert csp.categorize_theme("add to todo list") == "TODOs"
    assert csp.categorize_theme("audit the session prompts") == "Planning"
    assert csp.categorize_theme("hello there friend") == "Other"


def test_status_and_moscow_heuristics():
    """Status markers and MoSCoW labels are detected, with MoSCoW only on pending prompts."""
    assert csp.determine_status("what is this?") == "✔️ Clarifying Question"
    assert csp.determine_status("i want a must-have fix") == "⏳ Pending"
    assert csp.determine_status("create the file") == "✅ Done"
    assert csp.extract_moscow("⏳ Pending", "this must happen") == "Must"
    assert csp.extract_moscow("✅ Done", "this must happen") == ""


def test_markdown_cell_escaping():
    """Pipes are escaped and newlines collapsed so rows stay on one table line."""
    assert csp.escape_markdown_cell("a | b\n  c") == "a \\| b c"
    assert csp.escape_markdown_cell("") == ""


def test_main_writes_report(monkeypatch, tmp_path):
    """End to end: history in CLAUDE_CONFIG_DIR produces a dated report in the output dir."""
    config = tmp_path / "config"
    config.mkdir()
    _write_history(config / "history.jsonl", [
        {"display": "update the naming rule", "timestamp": _ms(datetime(2026, 8, 20, 9, 15))},
        {"display": "a | piped prompt?", "timestamp": _ms(datetime(2026, 8, 20, 10, 30))},
    ])
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    out_dir = tmp_path / "out"

    assert csp.main(["--date", "2026-08-20", "--output-dir", str(out_dir)]) == 0
    report = (out_dir / "2026_08_20_claude_prompts.md").read_text()
    assert report.startswith("# 📊 Prompts — 2026-08-20")
    assert "| 1 | 09 | 15 | Rules |" in report
    assert "a \\| piped prompt?" in report
    assert "- **Total prompts:** 2" in report
    assert "(local time)" in report
    assert "Dublin" not in report, "Fixed Dublin offset was replaced by local time"


def test_main_reports_empty_day_without_writing(monkeypatch, tmp_path, capsys):
    """A day with no prompts prints a message and writes nothing."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    out_dir = tmp_path / "out"
    assert csp.main(["--date", "2026-08-20", "--output-dir", str(out_dir)]) == 0
    assert "No history entries found for 2026-08-20" in capsys.readouterr().out
    assert not out_dir.exists()


def test_script_has_no_hardcoded_config_paths():
    """The script never hardcodes a config-dir path (portable_paths.md)."""
    source = SCRIPT.read_text()
    for literal in ['"~/.claude', '"~/claude', "/Users/", "/home/"]:
        assert literal not in source, f"Script hardcodes '{literal}'"
