# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the skill authoring gate's run checks (R2–R4) on fake skills, and how findings route.

Run checks look at test depth, the maturity history and documented gaps. R1 (version
matches maturity) is the same check as crawl's C3, so it's reported once, as C3. The
last tests confirm ``validate_skill`` sends walk and run failures to the blocking list
and judgement calls to the advisory one.
"""
from __future__ import annotations

from pathlib import Path

from _gate_fixtures import codes
from _gate_fixtures import gate
from _gate_fixtures import make_skill
from _gate_fixtures import walk_run

HISTORY = "\n## 📜 Version history\n\n- 1.0.0: first tactical release\n"
GAPS = "\n## 🕳️ Known gaps\n\n- None found yet, with a workaround noted here when one is.\n"


def write_test_file(tests_dir: Path, body: str) -> None:
    """Write a fake skill's pytest file.

    :param tests_dir: Folder to write it in.
    :type tests_dir: Path
    :param body: File content.
    :type body: str
    """
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_demo_skill.py").write_text(body)


def test_r2_short_test_file_fails(tmp_path: Path):
    """A pytest file of 30 lines or fewer fails R2."""
    write_test_file(tmp_path / "t", "def test_a():\n    assert True\n")
    failures, _ = walk_run(make_skill(tmp_path), tmp_path / "t")
    assert any(f.startswith("R2:") and "30 lines" in f for f in failures), f"got {failures}"


def test_r2_file_without_tests_fails(tmp_path: Path):
    """A long file with no pytest tests fails R2."""
    write_test_file(tmp_path / "t", "x = 1\n" * 40)
    failures, _ = walk_run(make_skill(tmp_path), tmp_path / "t")
    assert any(f.startswith("R2:") and "no pytest tests" in f for f in failures), f"got {failures}"


def test_r2_deep_test_file_passes(tmp_path: Path):
    """A long pytest file passes R2."""
    write_test_file(tmp_path / "t", "".join(f"def test_{i}():\n    assert {i} == {i}\n\n" for i in range(4)) * 4)
    failures, _ = walk_run(make_skill(tmp_path), tmp_path / "t")
    assert "R2" not in codes(failures), f"a deep test file should pass R2, got {failures}"


def test_r3_missing_history_warns(tmp_path: Path):
    """A tactical skill without a version history section is an R3 warning."""
    failures, warnings = walk_run(make_skill(tmp_path, maturity="tactical"), tmp_path)
    assert "R3" in codes(warnings), f"missing history should warn R3, got {warnings}"
    assert "R3" not in codes(failures), "missing history shouldn't block"


def test_r3_history_section_clears_warning(tmp_path: Path):
    """A version history section clears R3."""
    _, warnings = walk_run(make_skill(tmp_path, maturity="tactical", extra=HISTORY), tmp_path)
    assert "R3" not in codes(warnings), f"a history section should clear R3, got {warnings}"


def test_r4_strategic_without_gaps_fails(tmp_path: Path):
    """A strategic skill with no Known gaps section fails R4."""
    failures, _ = walk_run(make_skill(tmp_path, maturity="strategic", extra=HISTORY), tmp_path)
    assert "R4" in codes(failures), f"a strategic skill without gaps should fail R4, got {failures}"


def test_r4_known_gaps_section_passes(tmp_path: Path):
    """A Known gaps section satisfies R4."""
    failures, _ = walk_run(make_skill(tmp_path, maturity="strategic", extra=HISTORY + GAPS), tmp_path)
    assert "R4" not in codes(failures), f"a Known gaps section should pass R4, got {failures}"


def test_validate_skill_blocks_walk_failures(tmp_path: Path):
    """validate_skill puts a walk failure, such as a tactical TODO, in the blocking list."""
    failures, warnings = gate.validate_skill(make_skill(tmp_path, maturity="tactical", extra="TODO: x\n" + HISTORY))
    assert "W5" in codes(failures), f"W5 should block, got {failures}"
    assert "W5" not in codes(warnings), "W5 shouldn't also appear as a warning"


def test_validate_skill_only_advises_on_judgement_calls(tmp_path: Path):
    """validate_skill puts a judgement call, such as missing history, in the advisory list."""
    failures, warnings = gate.validate_skill(make_skill(tmp_path, maturity="tactical"))
    assert failures == [], f"a judgement call alone shouldn't block, got {failures}"
    assert "R3" in codes(warnings), f"R3 should be advisory, got {warnings}"


def test_version_mismatch_reported_once_as_c3(tmp_path: Path):
    """A version that doesn't match maturity is reported by C3, with no separate R1."""
    skill = make_skill(tmp_path, maturity="tactical", extra=HISTORY)
    contract = skill / "skill.contract.yaml"
    contract.write_text(contract.read_text().replace("version: 1.0.0", "version: 0.1.0"))
    failures, _ = gate.validate_skill(skill)
    assert "C3" in codes(failures), f"a version/maturity mismatch should fail C3, got {failures}"
    assert "R1" not in codes(failures), "R1 duplicated C3 and is no longer reported"


def test_default_tests_dir_is_the_skill_tests_folder():
    """By default the gate looks for skill tests in src/claude/_tests/skills/."""
    assert gate.DEFAULT_TESTS_DIR.parts[-3:] == ("claude", "_tests", "skills"), f"got {gate.DEFAULT_TESTS_DIR}"
    assert gate.DEFAULT_TESTS_DIR.is_dir(), f"{gate.DEFAULT_TESTS_DIR} doesn't exist"
