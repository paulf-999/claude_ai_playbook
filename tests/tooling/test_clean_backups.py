"""Tests for src/sh/claude/clean_backups.py.

Covers the candidate detection logic, the review file writer, the no-candidates
path, the user-abort paths, and the full archive workflow.
"""

from datetime import date, timedelta
from pathlib import Path

import pytest

from src.sh.claude.clean_backups import _find_candidates, _write_review_md, main

# ── shared fixtures ───────────────────────────────────────────────────────────

# Fixed reference date for deterministic age filter tests.
FIXED_TODAY = date(2026, 5, 12)

# A backup dir name dated 20 days before FIXED_TODAY — above the 14-day threshold.
OLD_BACKUP = ".claude_backup_20260422_120000"  # 20 days before 2026-05-12

# A backup dir name dated 6 days before FIXED_TODAY — below the 14-day threshold.
RECENT_BACKUP = ".claude_backup_20260506_120000"  # 6 days before 2026-05-12


def _make_backup_dirs(home: Path, names: list[str]) -> None:
    """Create stub backup directories in home."""
    for name in names:
        (home / name).mkdir()


# ── _find_candidates ──────────────────────────────────────────────────────────


def test_find_candidates_returns_old_backup(tmp_path):
    """A backup dir dated 20 days ago is returned as a candidate."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == [OLD_BACKUP]


def test_find_candidates_excludes_recent_backup(tmp_path):
    """A backup dir dated 6 days ago is not returned when min_age_days=14."""
    _make_backup_dirs(tmp_path, [RECENT_BACKUP])
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == []


def test_find_candidates_includes_at_age_boundary(tmp_path):
    """A backup dir dated exactly 14 days ago is returned as a candidate."""
    boundary_date = FIXED_TODAY - timedelta(days=14)
    name = f".claude_backup_{boundary_date.strftime('%Y%m%d')}_090000"
    _make_backup_dirs(tmp_path, [name])
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == [name]


def test_find_candidates_excludes_one_day_inside_threshold(tmp_path):
    """A backup dir dated 13 days ago is not returned when min_age_days=14."""
    near_date = FIXED_TODAY - timedelta(days=13)
    name = f".claude_backup_{near_date.strftime('%Y%m%d')}_090000"
    _make_backup_dirs(tmp_path, [name])
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == []


def test_find_candidates_ignores_non_matching_dirs(tmp_path):
    """Directories that don't match the backup pattern are ignored."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude_backup_archive").mkdir()
    (tmp_path / "some_other_dir").mkdir()
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == []


def test_find_candidates_ignores_files_not_dirs(tmp_path):
    """A file matching the pattern is not returned (only directories)."""
    (tmp_path / OLD_BACKUP).write_text("not a directory")
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == []


def test_find_candidates_returns_sorted_results(tmp_path):
    """Multiple candidates are returned in sorted order."""
    names = [
        ".claude_backup_20260310_120000",
        ".claude_backup_20260401_120000",
        ".claude_backup_20260315_120000",
    ]
    _make_backup_dirs(tmp_path, names)
    result = _find_candidates(str(tmp_path), today=FIXED_TODAY)
    assert result == sorted(names)


# ── _write_review_md ──────────────────────────────────────────────────────────


def test_write_review_md_creates_file(tmp_path):
    """_write_review_md creates the review file at the given path."""
    review_path = str(tmp_path / "review.md")
    _write_review_md([OLD_BACKUP], review_path, min_age_days=14)
    assert (tmp_path / "review.md").exists()


def test_write_review_md_contains_candidates(tmp_path):
    """The review file lists all candidate directory names."""
    review_path = str(tmp_path / "review.md")
    candidates = [OLD_BACKUP, ".claude_backup_20260301_090000"]
    _write_review_md(candidates, review_path, min_age_days=14)
    content = (tmp_path / "review.md").read_text()
    for name in candidates:
        assert name in content


def test_write_review_md_includes_age_threshold(tmp_path):
    """The review file header states the age threshold."""
    review_path = str(tmp_path / "review.md")
    _write_review_md([OLD_BACKUP], review_path, min_age_days=30)
    content = (tmp_path / "review.md").read_text()
    assert "30" in content


# ── main — no candidates ──────────────────────────────────────────────────────


def test_main_exits_when_no_candidates(tmp_path, capsys):
    """main() exits cleanly when no backup dirs meet the age threshold."""
    _make_backup_dirs(tmp_path, [RECENT_BACKUP])
    with pytest.raises(SystemExit):
        main(home_dir=str(tmp_path), today=FIXED_TODAY)
    out = capsys.readouterr().out
    assert "No backup directories" in out


# ── main — abort paths ────────────────────────────────────────────────────────


def test_main_aborts_on_n_response(tmp_path, monkeypatch, capsys):
    """main() aborts and does not move directories when user enters 'n'."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        main(home_dir=str(tmp_path), today=FIXED_TODAY)
    assert (tmp_path / OLD_BACKUP).exists()
    assert not (tmp_path / ".claude_backup_archive").exists()


def test_main_aborts_on_eof(tmp_path, monkeypatch, capsys):
    """main() aborts cleanly when input raises EOFError."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError()))
    with pytest.raises(SystemExit):
        main(home_dir=str(tmp_path), today=FIXED_TODAY)
    assert (tmp_path / OLD_BACKUP).exists()


# ── main — full archive workflow ──────────────────────────────────────────────


def test_main_moves_old_backup_to_archive(tmp_path, monkeypatch, capsys):
    """main() moves old backup dirs to .claude_backup_archive/ on confirmation."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main(home_dir=str(tmp_path), today=FIXED_TODAY)
    assert not (tmp_path / OLD_BACKUP).exists()
    assert (tmp_path / ".claude_backup_archive" / OLD_BACKUP).exists()


def test_main_does_not_move_recent_backup(tmp_path, monkeypatch):
    """main() does not touch backup dirs below the age threshold."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP, RECENT_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main(home_dir=str(tmp_path), today=FIXED_TODAY)
    assert not (tmp_path / OLD_BACKUP).exists()
    assert (tmp_path / RECENT_BACKUP).exists()


def test_main_writes_review_file_before_prompt(tmp_path, monkeypatch):
    """main() writes .claude_backup_review.md before asking for confirmation."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        main(home_dir=str(tmp_path), today=FIXED_TODAY)
    review = tmp_path / ".claude_backup_review.md"
    assert review.exists()
    assert OLD_BACKUP in review.read_text()


def test_main_creates_archive_dir_if_missing(tmp_path, monkeypatch):
    """main() creates .claude_backup_archive/ if it does not already exist."""
    _make_backup_dirs(tmp_path, [OLD_BACKUP])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert not (tmp_path / ".claude_backup_archive").exists()
    main(home_dir=str(tmp_path), today=FIXED_TODAY)
    assert (tmp_path / ".claude_backup_archive").is_dir()


def test_main_reports_count_in_output(tmp_path, monkeypatch, capsys):
    """main() reports the number of directories archived."""
    names = [OLD_BACKUP, ".claude_backup_20260301_090000"]
    _make_backup_dirs(tmp_path, names)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main(home_dir=str(tmp_path), today=FIXED_TODAY)
    out = capsys.readouterr().out
    assert "2" in out
