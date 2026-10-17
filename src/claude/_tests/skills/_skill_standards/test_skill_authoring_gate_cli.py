# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-17
# Date updated:      2026-10-17
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the skill authoring gate's command line exits and reports as intended.

``main()`` is what pre-commit runs, so its exit code decides whether a commit is
blocked. Each test points it at a folder of fake skills and checks the exit code and
the summary it prints: 1 when a skill fails or the folder is missing, 0 otherwise.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from _gate_fixtures import gate, make_skill


def run_main(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, root: Path) -> tuple[int, str, str]:
    """Run the gate's ``main()`` against one skills folder.

    :return: Tuple of (exit code, stdout, stderr).
    """
    monkeypatch.setattr("sys.argv", ["lint_skill_authoring_gate.py", str(root)])
    code = gate.main()
    out, err = capsys.readouterr()
    return code, out, err


def test_missing_root_is_rejected(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, tmp_path: Path):
    """A skills folder that doesn't exist exits 1 with an error on stderr."""
    code, _, err = run_main(monkeypatch, capsys, tmp_path / "missing")
    assert code == 1, f"a missing folder should exit 1, got {code}"
    assert "root directory not found" in err, f"expected a not-found error on stderr, got {err!r}"


def test_folder_without_skills_passes(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, tmp_path: Path):
    """A folder with no skills exits 0 and says it found none."""
    code, out, _ = run_main(monkeypatch, capsys, tmp_path)
    assert code == 0, f"an empty folder should exit 0, got {code}"
    assert "No skills found" in out, f"expected a no-skills message, got {out!r}"


def test_clean_skill_passes(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, tmp_path: Path):
    """A skill with no findings exits 0 and is counted as clean."""
    make_skill(tmp_path)
    code, out, _ = run_main(monkeypatch, capsys, tmp_path)
    assert code == 0, f"a clean skill should exit 0, got {code}:\n{out}"
    assert "Clean     1" in out, f"the clean skill should be counted, got:\n{out}"
    assert "all skills pass" in out, f"expected the pass line, got:\n{out}"


def test_warning_only_skill_passes(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, tmp_path: Path):
    """A skill with only judgement calls, such as missing history, prints WARN but still exits 0."""
    make_skill(tmp_path, maturity="tactical")
    code, out, _ = run_main(monkeypatch, capsys, tmp_path)
    assert code == 0, f"warnings alone shouldn't block, got exit {code}:\n{out}"
    assert "WARN  R3" in out, f"the R3 warning should be printed, got:\n{out}"
    assert "advisory only" in out, f"the summary should call warnings advisory, got:\n{out}"


def test_failing_skill_is_flagged(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, tmp_path: Path):
    """A skill with a blocking failure, such as a tactical TODO, prints FAIL and exits 1."""
    make_skill(tmp_path, maturity="tactical", extra="TODO: x\n")
    code, out, _ = run_main(monkeypatch, capsys, tmp_path)
    assert code == 1, f"a failing skill should exit 1, got {code}:\n{out}"
    assert "FAIL  W5" in out, f"the W5 failure should be printed, got:\n{out}"
    assert "must be fixed" in out, f"the summary should say failures must be fixed, got:\n{out}"
