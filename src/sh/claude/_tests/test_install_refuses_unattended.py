# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that ``make install`` refuses to run unattended (issue #150).

The install script must need ``CLAUDE_CONFIG_DIR`` set and a real terminal, so Claude's Bash
tool, or any pipe, can never run it. Every run uses a temp ``HOME`` and ``CLAUDE_CONFIG_DIR``.
Split from ``test_install_claude_files.py`` on 2026-10-02; the typed confirmation is covered by
``test_install_typed_confirmation.py``.
"""
from __future__ import annotations

from pathlib import Path

from _install_sandbox import (
    INSTALL_SCRIPT,
    make_sandbox,
    nothing_changed,
    run_without_tty,
)


def test_unset_config_dir_exits_non_zero(tmp_path: Path) -> None:
    """An unset ``CLAUDE_CONFIG_DIR`` stops the script."""
    box = make_sandbox(tmp_path)
    del box["env"]["CLAUDE_CONFIG_DIR"]
    assert run_without_tty(box["env"]).returncode != 0, "Script must fail when CLAUDE_CONFIG_DIR is unset"


def test_unset_config_dir_explains_fix(tmp_path: Path) -> None:
    """The unset-variable error tells the user to export it."""
    box = make_sandbox(tmp_path)
    del box["env"]["CLAUDE_CONFIG_DIR"]
    output = run_without_tty(box["env"]).stdout
    assert "CLAUDE_CONFIG_DIR is not set" in output, "Error must name the missing variable"
    assert "export CLAUDE_CONFIG_DIR" in output, "Error must show how to set the variable"


def test_unset_config_dir_touches_nothing(tmp_path: Path) -> None:
    """An unset variable never falls back to ``~/.claude``."""
    box = make_sandbox(tmp_path)
    del box["env"]["CLAUDE_CONFIG_DIR"]
    run_without_tty(box["env"])
    assert not (box["home"] / ".claude").exists(), "Script fell back to ~/.claude"
    assert nothing_changed(box) == [], f"Install ran past the gate: {nothing_changed(box)}"


def test_empty_config_dir_counts_as_unset(tmp_path: Path) -> None:
    """``CLAUDE_CONFIG_DIR=""`` is refused like an unset variable, never read as the current folder."""
    box = make_sandbox(tmp_path)
    box["env"]["CLAUDE_CONFIG_DIR"] = ""
    result = run_without_tty(box["env"])
    assert result.returncode != 0, "An empty CLAUDE_CONFIG_DIR must stop the script"
    assert "CLAUDE_CONFIG_DIR is not set" in result.stdout, "An empty value must get the same explanation"


def test_no_tty_refuses(tmp_path: Path) -> None:
    """Without a terminal, the script exits 1 and says why."""
    result = run_without_tty(make_sandbox(tmp_path)["env"])
    assert result.returncode == 1, "Script must refuse when stdin is not a terminal"
    assert "run from your own terminal" in result.stdout, "Refusal must tell the user to use their own terminal"


def test_no_tty_changes_nothing(tmp_path: Path) -> None:
    """A refused run leaves the target and home untouched."""
    box = make_sandbox(tmp_path)
    run_without_tty(box["env"])
    assert nothing_changed(box) == [], f"Install ran past the gate: {nothing_changed(box)}"


def test_piped_answer_still_refuses(tmp_path: Path) -> None:
    """Piping ``install`` into the script doesn't count as typing it, so automation can't approve itself."""
    box = make_sandbox(tmp_path)
    result = run_without_tty(box["env"], stdin_text="install\n")
    assert result.returncode == 1, "A piped answer must be refused like no terminal at all"
    assert nothing_changed(box) == [], f"A piped 'install' ran the install: {nothing_changed(box)}"


def test_refusal_shows_no_preview(tmp_path: Path) -> None:
    """The terminal check comes first, so a refused run never prints the install preview."""
    output = run_without_tty(make_sandbox(tmp_path)["env"]).stdout
    assert "Type 'install' to continue" not in output, "A refused run must not reach the confirmation prompt"


def test_refusal_does_not_create_missing_target(tmp_path: Path) -> None:
    """A refused run doesn't create a config folder that doesn't exist yet."""
    box = make_sandbox(tmp_path)
    missing = tmp_path / "not_yet"
    box["env"]["CLAUDE_CONFIG_DIR"] = str(missing)
    run_without_tty(box["env"])
    assert not missing.exists(), "A refused run created the target folder"


def test_gate_runs_before_install() -> None:
    """``confirm_install`` is called before ``install_claude_files`` in the main logic."""
    lines = [line.strip() for line in INSTALL_SCRIPT.read_text().splitlines()]
    assert "confirm_install" in lines, "confirm_install is never called"
    assert lines.index("confirm_install") < lines.index("install_claude_files"), "The gate must run before files change"
