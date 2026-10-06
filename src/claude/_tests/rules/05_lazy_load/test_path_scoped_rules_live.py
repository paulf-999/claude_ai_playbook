# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves in a live session that a ``paths:`` rule loads when, and only when, a matching file is read.

The other rule tests check files and links. Only a real Claude Code session shows what
actually reaches context, so the live tests run ``claude -p`` in a scratch folder, then read
that session's transcript: a ``nested_memory`` attachment names each rule loaded mid-session.

- **Opt-in:** the live tests skip unless ``CLAUDE_LIVE_CANARY=1``, because each run makes two
  small API calls on the cheapest model.
- **No config edits:** they use the installed ``sql.md`` rule, and delete the transcripts they create.
- **Run:** ``CLAUDE_LIVE_CANARY=1 pytest _tests/rules/05_lazy_load/test_path_scoped_rules_live.py``
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from _shared_paths import CLAUDE_DIR

MODEL = "claude-haiku-4-5-20251001"
RULE_SUFFIX = "/_rules/05_lazy_load/style_guide_standards/sql.md"
TIMEOUT_SECONDS = 180
LIVE = os.environ.get("CLAUDE_LIVE_CANARY") == "1" and shutil.which("claude") is not None


def project_dir_for(cwd: Path) -> Path:
    """Return the folder Claude Code writes a working directory's transcripts to.

    :param cwd: The session's working directory.
    :type cwd: Path
    :return: ``projects/<cwd with every non-alphanumeric character as a hyphen>``.
    :rtype: Path
    """
    return CLAUDE_DIR / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))


def loaded_rule_paths(transcript: Path) -> list[str]:
    """Return the paths of rules a session loaded mid-session, in order.

    :param transcript: A session ``.jsonl`` transcript.
    :type transcript: Path
    :return: Paths from ``nested_memory`` attachments.
    :rtype: list[str]
    """
    found = []
    for line in transcript.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        attachment = record.get("attachment") if isinstance(record, dict) else None
        if isinstance(attachment, dict) and attachment.get("type") == "nested_memory":
            found.append(attachment.get("path", ""))
    return found


def loaded_rule(transcript: Path, suffix: str = RULE_SUFFIX) -> bool:
    """Tell whether a session loaded the rule whose path ends with ``suffix``.

    :param transcript: A session transcript.
    :type transcript: Path
    :param suffix: The end of the rule's path.
    :type suffix: str
    :return: True when a nested_memory attachment names the rule.
    :rtype: bool
    """
    return any(path.endswith(suffix) for path in loaded_rule_paths(transcript))


def run_probe(cwd: Path, file_name: str) -> Path:
    """Ask a headless session to read one file, and return that session's transcript.

    :param cwd: The scratch working directory holding the file.
    :type cwd: Path
    :param file_name: The file Claude should read.
    :type file_name: str
    :return: The new transcript.
    :rtype: Path
    """
    prompt = f"Read the file {file_name} in the current folder, then reply with just OK."
    subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL, "--allowedTools", "Read"],
        cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=True,
    )
    transcripts = sorted(project_dir_for(cwd).glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    assert transcripts, f"no transcript written under {project_dir_for(cwd)}"
    return transcripts[-1]


def remove_project_dir(folder: Path) -> None:
    """Delete the transcripts a probe created, then its now-empty folders.

    :param folder: The probe's ``projects/`` folder.
    :type folder: Path
    """
    if not folder.is_dir():
        return
    for transcript in folder.glob("*.jsonl"):
        transcript.unlink()
    for sub in sorted((p for p in folder.rglob("*") if p.is_dir()), reverse=True):
        if not any(sub.iterdir()):
            sub.rmdir()
    if not any(folder.iterdir()):
        folder.rmdir()


def write_transcript(path: Path, records: list[dict]) -> Path:
    """Write fixture records as a JSON-lines transcript.

    :param path: Where to write.
    :type path: Path
    :param records: Transcript records.
    :type records: list[dict]
    :return: The written path.
    :rtype: Path
    """
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    return path


# ── offline: the transcript reading the live tests rely on ───────────────────


def test_project_dir_encodes_the_working_directory():
    """Every slash and underscore in the working directory becomes a hyphen."""
    assert project_dir_for(Path("/tmp/canary_sql")).name == "-tmp-canary-sql"


def test_nested_memory_paths_are_read(tmp_path):
    """Rules loaded mid-session are read from nested_memory attachments, in order."""
    transcript = write_transcript(tmp_path / "s.jsonl", [
        {"type": "attachment", "attachment": {"type": "nested_memory", "path": "/c/_rules/a.md"}},
        {"type": "attachment", "attachment": {"type": "environment"}},
        {"type": "attachment", "attachment": {"type": "nested_memory", "path": "/c/_rules/b.md"}},
    ])
    assert loaded_rule_paths(transcript) == ["/c/_rules/a.md", "/c/_rules/b.md"]


def test_startup_instructions_are_not_mid_session_loads(tmp_path):
    """The startup file list isn't a paths: load, so it's ignored."""
    transcript = write_transcript(tmp_path / "s.jsonl", [
        {"type": "attachment", "attachment": {"type": "instructions", "files": [{"path": "/c/_rules/x.md"}]}},
    ])
    assert loaded_rule_paths(transcript) == []


def test_broken_lines_are_skipped(tmp_path):
    """A malformed or non-object line doesn't stop the scan."""
    path = tmp_path / "s.jsonl"
    path.write_text('not json\n[]\n{"type": "attachment", "attachment": {"type": "nested_memory", "path": "/r.md"}}\n')
    assert loaded_rule_paths(path) == ["/r.md"]


def test_rule_match_uses_the_path_suffix(tmp_path):
    """The SQL rule counts whether the live config sits at ~/.claude or elsewhere."""
    transcript = write_transcript(tmp_path / "s.jsonl", [
        {"type": "attachment", "attachment": {"type": "nested_memory", "path": f"/home/u/claude{RULE_SUFFIX}"}},
    ])
    assert loaded_rule(transcript), "the SQL rule under a custom config folder was missed"
    assert not loaded_rule(transcript, "/python.md"), "a different rule must not match"


def test_cleanup_removes_only_what_a_probe_created(tmp_path):
    """Transcripts and empty folders go, and the folder disappears once empty."""
    folder = tmp_path / "-tmp-probe"
    (folder / "memory").mkdir(parents=True)
    (folder / "a.jsonl").write_text("{}\n")
    remove_project_dir(folder)
    assert not folder.exists(), "the probe folder should be gone once empty"


def test_cleanup_keeps_unexpected_files(tmp_path):
    """A file the probe didn't create is left alone, along with its folder."""
    folder = tmp_path / "-tmp-probe"
    folder.mkdir()
    (folder / "a.jsonl").write_text("{}\n")
    (folder / "notes.md").write_text("keep\n")
    remove_project_dir(folder)
    assert (folder / "notes.md").is_file(), "a non-transcript file was deleted"
    assert not (folder / "a.jsonl").exists(), "the transcript was not removed"


def test_the_sql_rule_is_installed_with_paths():
    """The live tests rely on sql.md being a paths: rule, linked into rules/ when installed."""
    rule = CLAUDE_DIR / "_rules" / "05_lazy_load" / "style_guide_standards" / "sql.md"
    assert rule.read_text().startswith('---\npaths:\n  - "**/*.sql"'), "sql.md lost its paths: trigger"
    if (CLAUDE_DIR / "rules").is_dir():
        assert (CLAUDE_DIR / "rules" / "sql.md").is_symlink(), "rules/sql.md symlink is missing"


# ── live: a real session ─────────────────────────────────────────────────────


@pytest.mark.skipif(not LIVE, reason="set CLAUDE_LIVE_CANARY=1, with claude on PATH, to run live sessions")
def test_reading_a_sql_file_loads_the_sql_rule(tmp_path):
    """A session that reads a .sql file gets sql.md mid-session."""
    (tmp_path / "sample.sql").write_text("select 1;\n")
    try:
        transcript = run_probe(tmp_path, "sample.sql")
        assert loaded_rule(transcript), f"sql.md did not load: {loaded_rule_paths(transcript)}"
    finally:
        remove_project_dir(project_dir_for(tmp_path))


@pytest.mark.skipif(not LIVE, reason="set CLAUDE_LIVE_CANARY=1, with claude on PATH, to run live sessions")
def test_reading_a_text_file_does_not_load_the_sql_rule(tmp_path):
    """The control: a session that reads only a .txt file never gets sql.md."""
    (tmp_path / "sample.txt").write_text("hello\n")
    try:
        transcript = run_probe(tmp_path, "sample.txt")
        assert not loaded_rule(transcript), "sql.md loaded without a .sql file being read"
    finally:
        remove_project_dir(project_dir_for(tmp_path))
