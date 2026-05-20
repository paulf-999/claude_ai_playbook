"""Tests for the clean_plans archival script.

Covers _find_candidates (candidate detection), the no-candidates exit path,
the missing PLANS.md path, the user-abort paths, and the full archive workflow.
"""

from datetime import date, timedelta
from pathlib import Path

import pytest

from src.sh.claude.clean_plans import _find_candidates, _write_review_md, main

# ── shared fixtures ───────────────────────────────────────────────────────────

HEADER_LINES = [
    "# Plans Index\n",
    "\n",
    "| File | Project | Task | Date | Status |\n",
    "|------|---------|------|------|--------|\n",
]

PENDING_ROW = "| [plan_a.md](plan_a.md) | playbook | Some task | 2026-04-23 | pending |\n"
EXECUTED_ROW = "| [plan_b.md](plan_b.md) | playbook | Another task | 2026-04-22 | executed |\n"
SUPERSEDED_ROW = "| [plan_c.md](plan_c.md) | playbook | Old task | 2026-04-21 | superseded |\n"

# Fixed reference date for deterministic age filter tests.
FIXED_TODAY = date(2026, 5, 11)
# 6 days before FIXED_TODAY — below the 14-day threshold.
RECENT_EXECUTED_ROW = "| [plan_d.md](plan_d.md) | playbook | Recent task | 2026-05-05 | executed |\n"


def _write_plans_md(plans_dir: Path, rows: list[str]) -> None:
    """Write a PLANS.md with the given data rows appended after the standard header.

    :param plans_dir: Directory to write PLANS.md into.
    :type plans_dir: Path
    :param rows: Data rows to append (already newline-terminated).
    :type rows: list[str]
    """
    content = "".join(HEADER_LINES + rows)
    (plans_dir / "PLANS.md").write_text(content)


# ── _find_candidates — detection logic ───────────────────────────────────────


def test_find_candidates_empty_lines_returns_empty():
    """Empty input yields no candidates."""
    assert _find_candidates([]) == []


def test_find_candidates_no_pipe_lines_returns_empty():
    """Lines without pipe delimiters yield no candidates."""
    assert _find_candidates(["# Heading\n", "\n"]) == []


def test_find_candidates_only_pending_returns_empty():
    """A pending row is not a candidate."""
    assert _find_candidates(HEADER_LINES + [PENDING_ROW]) == []


def test_find_candidates_detects_executed_row():
    """An executed row is returned as a candidate with the correct filename."""
    candidates = _find_candidates(HEADER_LINES + [EXECUTED_ROW])
    assert len(candidates) == 1
    _, _, filename = candidates[0]
    assert filename == "plan_b.md"


def test_find_candidates_detects_superseded_row():
    """A superseded row is returned as a candidate with the correct filename."""
    candidates = _find_candidates(HEADER_LINES + [SUPERSEDED_ROW])
    assert len(candidates) == 1
    _, _, filename = candidates[0]
    assert filename == "plan_c.md"


def test_find_candidates_skips_header_and_separator():
    """Table header and separator rows are not returned as candidates."""
    assert _find_candidates(HEADER_LINES) == []


def test_find_candidates_mixed_statuses_returns_only_done():
    """Only executed and superseded rows are returned; pending rows are excluded."""
    lines = HEADER_LINES + [PENDING_ROW, EXECUTED_ROW, SUPERSEDED_ROW]
    candidates = _find_candidates(lines)
    filenames = [c[2] for c in candidates]
    assert len(candidates) == 2
    assert "plan_b.md" in filenames
    assert "plan_c.md" in filenames
    assert "plan_a.md" not in filenames


def test_find_candidates_returns_correct_line_index():
    """Returned tuple contains the correct 0-based line index from the input list."""
    lines = HEADER_LINES + [PENDING_ROW, EXECUTED_ROW]
    candidates = _find_candidates(lines)
    idx, _, _ = candidates[0]
    # 4 header lines (0–3), pending at 4, executed at 5
    assert idx == len(HEADER_LINES) + 1


def test_find_candidates_no_header_returns_empty():
    """Lines with pipe-delimited rows but no File/Status header yield no candidates."""
    row = "| plan_b.md | playbook | Task | 2026-04-22 | executed |\n"
    assert _find_candidates([row]) == []


def test_find_candidates_row_without_markdown_link_returns_none_filename():
    """A data row with a plain-text file cell (no markdown link) yields filename=None."""
    row_no_link = "| plain_name.md | playbook | Task | 2026-04-23 | executed |\n"
    candidates = _find_candidates(HEADER_LINES + [row_no_link])
    assert len(candidates) == 1
    _, _, filename = candidates[0]
    assert filename is None


# ── main() — exit paths ───────────────────────────────────────────────────────


def test_main_missing_plans_md_exits_cleanly(tmp_path: Path, capsys):
    """main() exits 0 with a message when PLANS.md does not exist."""
    with pytest.raises(SystemExit) as exc:
        main(plans_dir=str(tmp_path))
    assert exc.value.code == 0
    assert "No PLANS.md" in capsys.readouterr().out


def test_main_no_candidates_exits_cleanly(tmp_path: Path, capsys):
    """main() exits 0 with a message when all rows are pending."""
    _write_plans_md(tmp_path, [PENDING_ROW])
    with pytest.raises(SystemExit) as exc:
        main(plans_dir=str(tmp_path))
    assert exc.value.code == 0
    assert "No executed/superseded" in capsys.readouterr().out


def test_main_abort_on_non_y_input_leaves_files_unchanged(tmp_path: Path, monkeypatch):
    """main() exits 0 without archiving when the user does not confirm."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    _write_plans_md(tmp_path, [EXECUTED_ROW])
    plan_file = tmp_path / "plan_b.md"
    plan_file.write_text("# Plan B")

    with pytest.raises(SystemExit) as exc:
        main(plans_dir=str(tmp_path))

    assert exc.value.code == 0
    assert plan_file.exists()
    assert "plan_b.md" in (tmp_path / "PLANS.md").read_text()


def test_main_abort_on_eof_leaves_files_unchanged(tmp_path: Path, monkeypatch):
    """main() exits 0 without archiving when stdin is closed (EOFError)."""

    def _raise_eof(_: str) -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", _raise_eof)
    _write_plans_md(tmp_path, [EXECUTED_ROW])
    plan_file = tmp_path / "plan_b.md"
    plan_file.write_text("# Plan B")

    with pytest.raises(SystemExit) as exc:
        main(plans_dir=str(tmp_path))

    assert exc.value.code == 0
    assert plan_file.exists()


# ── main() — archive workflow ─────────────────────────────────────────────────


def test_main_archives_executed_and_superseded_files(tmp_path: Path, monkeypatch):
    """main() moves plan files to archive/ and removes their rows from PLANS.md."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    _write_plans_md(tmp_path, [PENDING_ROW, EXECUTED_ROW, SUPERSEDED_ROW])
    for name in ("plan_b.md", "plan_c.md"):
        (tmp_path / name).write_text(f"# {name}")

    main(plans_dir=str(tmp_path))

    archive_dir = tmp_path / "archive"
    assert (archive_dir / "plan_b.md").exists()
    assert (archive_dir / "plan_c.md").exists()
    assert not (tmp_path / "plan_b.md").exists()
    assert not (tmp_path / "plan_c.md").exists()


def test_main_removes_archived_rows_from_plans_md(tmp_path: Path, monkeypatch):
    """Archived rows are removed from PLANS.md; pending rows are preserved."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    _write_plans_md(tmp_path, [PENDING_ROW, EXECUTED_ROW, SUPERSEDED_ROW])
    for name in ("plan_b.md", "plan_c.md"):
        (tmp_path / name).write_text(f"# {name}")

    main(plans_dir=str(tmp_path))

    remaining = (tmp_path / "PLANS.md").read_text()
    assert "plan_a.md" in remaining  # pending row kept
    assert "plan_b.md" not in remaining
    assert "plan_c.md" not in remaining


def test_main_skips_missing_file_but_removes_row(tmp_path: Path, monkeypatch, capsys):
    """When a plan file is absent from disk, the row is still removed from PLANS.md."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    _write_plans_md(tmp_path, [EXECUTED_ROW])
    # plan_b.md deliberately not created on disk

    main(plans_dir=str(tmp_path))

    assert "Not found (skipped)" in capsys.readouterr().out
    assert "plan_b.md" not in (tmp_path / "PLANS.md").read_text()


# ── _find_candidates — age filter ────────────────────────────────────────────


def test_find_candidates_excludes_plan_within_age_threshold():
    """A plan dated 6 days ago is not returned when min_age_days=14."""
    candidates = _find_candidates(HEADER_LINES + [RECENT_EXECUTED_ROW], today=FIXED_TODAY)
    assert candidates == []


def test_find_candidates_includes_plan_at_age_boundary():
    """A plan dated exactly 14 days ago is returned as a candidate."""
    boundary_date = FIXED_TODAY - timedelta(days=14)
    row = f"| [plan_e.md](plan_e.md) | playbook | Boundary task | {boundary_date} | executed |\n"
    candidates = _find_candidates(HEADER_LINES + [row], today=FIXED_TODAY)
    assert len(candidates) == 1
    _, _, filename = candidates[0]
    assert filename == "plan_e.md"


def test_find_candidates_excludes_plan_one_day_inside_threshold():
    """A plan dated 13 days ago is not returned when min_age_days=14."""
    recent_date = FIXED_TODAY - timedelta(days=13)
    row = f"| [plan_f.md](plan_f.md) | playbook | Near task | {recent_date} | executed |\n"
    candidates = _find_candidates(HEADER_LINES + [row], today=FIXED_TODAY)
    assert candidates == []


def test_find_candidates_includes_row_with_unparseable_date():
    """A row with an invalid date cell is included conservatively."""
    row = "| [plan_g.md](plan_g.md) | playbook | Bad date | not-a-date | executed |\n"
    candidates = _find_candidates(HEADER_LINES + [row], today=FIXED_TODAY)
    assert len(candidates) == 1
    _, _, filename = candidates[0]
    assert filename == "plan_g.md"


# ── _write_review_md ─────────────────────────────────────────────────────────


def test_write_review_md_creates_file_with_table(tmp_path: Path):
    """_write_review_md writes a markdown file containing the candidate rows."""
    candidates = _find_candidates(HEADER_LINES + [EXECUTED_ROW, SUPERSEDED_ROW])
    review_path = str(tmp_path / "archive_review.md")
    _write_review_md(candidates, review_path, min_age_days=14)

    content = (tmp_path / "archive_review.md").read_text()
    assert "# Plans to Archive" in content
    assert "plan_b.md" in content
    assert "plan_c.md" in content
    assert "| File | Project | Task | Date | Status |" in content


def test_main_writes_review_file_before_prompt(tmp_path: Path, monkeypatch):
    """main() writes archive_review.md before asking for confirmation."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    _write_plans_md(tmp_path, [EXECUTED_ROW])
    (tmp_path / "plan_b.md").write_text("# Plan B")

    with pytest.raises(SystemExit):
        main(plans_dir=str(tmp_path))

    assert (tmp_path / "archive_review.md").exists()
    assert "plan_b.md" in (tmp_path / "archive_review.md").read_text()
