# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-02
# Version:           1.0.2
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates how audit_claude_component.py chooses the folder it scans.

The script is installed into the live config as well as the repo, so it must
never guess the repo from its own location. It takes the root as a required
argument and stops with a clear error when the root is missing or not found.
"""

import importlib.util
import sys
from datetime import date

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "_scripts" / "_audit_scripts" / "audit_claude_component.py"


def load_audit():
    """Import the audit script as a module.

    :return: The loaded module.
    """
    spec = importlib.util.spec_from_file_location("audit_claude_component", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_audit(monkeypatch, capsys, *args: str) -> tuple[int, str, str]:
    """Run the audit's main() with the given arguments.

    :param monkeypatch: Pytest monkeypatch fixture.
    :param capsys: Pytest capsys fixture.
    :param args: Command-line arguments after the script name.
    :return: The exit code, stdout and stderr.
    """
    monkeypatch.setattr(sys, "argv", ["audit_claude_component.py", *args])
    code = load_audit().main()
    out = capsys.readouterr()
    return code, out.out, out.err


def make_root(tmp_path):
    """Build a small config tree with one tagged skill, one untagged rule and two skipped files.

    :param tmp_path: Pytest tmp_path fixture.
    :return: The root folder.
    """
    root = tmp_path / "claude"
    (root / "skills" / "demo").mkdir(parents=True)
    (root / "skills" / "demo" / "SKILL.md").write_text("---\nname: demo\nmaturity: draft\n---\n# Demo\n")
    (root / "skills" / "README.md").write_text("# Skills\n")
    (root / "rules" / "style_guide_standards").mkdir(parents=True)
    (root / "rules" / "plain.md").write_text("# Plain rule\n")
    (root / "rules" / "style_guide_standards" / "sql.md").write_text("# SQL\n")
    return root


def test_missing_root_returns_error_code(monkeypatch, capsys):
    """With no root argument, the audit exits 1."""
    code, _, _ = run_audit(monkeypatch, capsys)
    assert code == 1, f"expected exit 1 with no root, got {code}"


def test_missing_root_explains_the_fix(monkeypatch, capsys):
    """With no root argument, stderr says what's missing and shows the usage line."""
    _, _, err = run_audit(monkeypatch, capsys)
    assert "no root directory given" in err, f"stderr should name the missing root, got {err!r}"
    assert "usage:" in err, f"stderr should show the usage line, got {err!r}"


def test_missing_root_prints_no_report(monkeypatch, capsys):
    """With no root argument, nothing is scanned, so no report reaches stdout."""
    _, out, _ = run_audit(monkeypatch, capsys)
    assert out == "", f"no report should print without a root, got {out!r}"


def test_root_not_found_is_an_error(monkeypatch, capsys, tmp_path):
    """A root that doesn't exist exits 1 and names the missing folder."""
    code, _, err = run_audit(monkeypatch, capsys, str(tmp_path / "absent"))
    assert code == 1, f"expected exit 1 for a missing folder, got {code}"
    assert "not found" in err, f"stderr should say the folder wasn't found, got {err!r}"


def test_explicit_root_returns_zero(monkeypatch, capsys, tmp_path):
    """A real root prints the report and exits 0."""
    code, out, _ = run_audit(monkeypatch, capsys, str(make_root(tmp_path)))
    assert code == 0, f"expected exit 0 for a real root, got {code}"
    assert "SUMMARY" in out, "the report should include its SUMMARY section"


def test_explicit_root_is_the_only_folder_scanned(monkeypatch, capsys, tmp_path):
    """Only the given root is scanned, so the counts match the fixture tree exactly."""
    _, out, _ = run_audit(monkeypatch, capsys, str(make_root(tmp_path)))
    assert "Scanned:        2 components" in out, f"expected 2 components from the fixture, got:\n{out}"
    assert "Tagged:         1  |  Untagged: 1" in out, f"expected 1 tagged and 1 untagged, got:\n{out}"


def test_readme_and_excluded_folders_are_skipped(monkeypatch, capsys, tmp_path):
    """README.md and style_guide_standards/ files are not counted as components."""
    tagged, untagged = load_audit().find_all_components(make_root(tmp_path))
    names = [p.name for p in tagged + untagged]
    assert "README.md" not in names, "README.md files should be skipped"
    assert "sql.md" not in names, "style_guide_standards/ files should be skipped"


def test_relative_root_resolves_from_working_dir(monkeypatch, capsys, tmp_path):
    """A relative root is resolved from the current folder, as make passes it."""
    make_root(tmp_path)
    monkeypatch.chdir(tmp_path)
    code, out, _ = run_audit(monkeypatch, capsys, "claude")
    assert code == 0, f"expected exit 0 for a relative root, got {code}"
    assert "Scanned:        2 components" in out, f"relative root scanned the wrong folder:\n{out}"


def test_root_without_component_folders_reports_zero(monkeypatch, capsys, tmp_path):
    """An empty but real root exits 0 and reports no components."""
    code, out, _ = run_audit(monkeypatch, capsys, str(tmp_path))
    assert code == 0, f"expected exit 0 for an empty root, got {code}"
    assert "Scanned:        0 components" in out, f"expected 0 components, got:\n{out}"


def test_report_is_dated_today(monkeypatch, capsys, tmp_path):
    """The report header carries today's date."""
    _, out, _ = run_audit(monkeypatch, capsys, str(make_root(tmp_path)))
    assert str(date.today()) in out, "the report header should show today's date"


def test_script_has_no_guessed_default_root():
    """The script defines no default root, so it can't silently scan the wrong config."""
    module = load_audit()
    assert not hasattr(module, "DEFAULT_ROOT"), "DEFAULT_ROOT is back — the root must come from the caller"
    assert not hasattr(module, "_REPO_ROOT"), "_REPO_ROOT is back — never guess the repo from the script's location"


def test_real_config_root_runs(monkeypatch, capsys):
    """The config under test audits cleanly, as make audit_components runs it."""
    code, out, _ = run_audit(monkeypatch, capsys, str(CLAUDE_DIR))
    assert code == 0, f"the audit failed on {CLAUDE_DIR}"
    assert "HEALTH SIGNALS" in out, "the report should include its HEALTH SIGNALS section"
