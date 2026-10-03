# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-03
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that ``make install`` refuses to run unattended (issue #150).

The install script needs a real terminal, so Claude's Bash tool, or any pipe, can never run it.
It installs into ``CLAUDE_CONFIG_DIR`` when set,
otherwise Claude Code's default ``~/.claude``. Every run uses a temp ``HOME`` and ``CLAUDE_CONFIG_DIR``.
Split from ``test_install_claude_files.py`` on 2026-10-02; the typed confirmation is covered by
``test_install_typed_confirmation.py``.
"""
from __future__ import annotations

from pathlib import Path

from _install_sandbox import (
    INSTALL_SCRIPT,
    make_sandbox,
    nothing_changed,
    run_with_tty,
    run_without_tty,
)


def test_unset_config_dir_targets_default_folder(tmp_path: Path):
    """An unset ``CLAUDE_CONFIG_DIR`` falls back to Claude Code's default ``~/.claude``, shown in the preview."""
    box = make_sandbox(tmp_path)
    del box["env"]["CLAUDE_CONFIG_DIR"]
    code, output = run_with_tty(box["env"], b"no\n")
    assert f"Target:  {box['home'] / '.claude'}" in output, f"preview should target ~/.claude, got: {output}"
    assert code != 0, "cancelling must still exit non-zero"


def test_unset_config_dir_still_needs_confirmation(tmp_path: Path):
    """Falling back to ``~/.claude`` changes nothing until the user types ``install``."""
    box = make_sandbox(tmp_path)
    del box["env"]["CLAUDE_CONFIG_DIR"]
    run_with_tty(box["env"], b"no\n")
    assert not (box["home"] / ".claude").exists(), "cancelling must not create ~/.claude"
    assert nothing_changed(box) == [], f"Install ran past the gate: {nothing_changed(box)}"


def test_empty_config_dir_counts_as_unset(tmp_path: Path):
    """``CLAUDE_CONFIG_DIR=""`` falls back like an unset variable, never read as the current folder."""
    box = make_sandbox(tmp_path)
    box["env"]["CLAUDE_CONFIG_DIR"] = ""
    _, output = run_with_tty(box["env"], b"no\n")
    assert f"Target:  {box['home'] / '.claude'}" in output, f"an empty value should target ~/.claude, got: {output}"
    assert "Target:  \n" not in output, "an empty value must never become an empty target"


def test_set_config_dir_is_the_target(tmp_path: Path):
    """A set ``CLAUDE_CONFIG_DIR``, like ``~/claude``, is the target instead of the default."""
    box = make_sandbox(tmp_path)
    _, output = run_with_tty(box["env"], b"no\n")
    assert f"Target:  {box['target']}" in output, f"preview should target CLAUDE_CONFIG_DIR, got: {output}"
    assert f"Target:  {box['home'] / '.claude'}" not in output, "a set CLAUDE_CONFIG_DIR must not fall back"


def test_no_tty_refuses(tmp_path: Path):
    """Without a terminal, the script exits 1 and says why."""
    result = run_without_tty(make_sandbox(tmp_path)["env"])
    assert result.returncode == 1, "Script must refuse when stdin is not a terminal"
    assert "run from your own terminal" in result.stdout, "Refusal must tell the user to use their own terminal"


def test_no_tty_changes_nothing(tmp_path: Path):
    """A refused run leaves the target and home untouched."""
    box = make_sandbox(tmp_path)
    run_without_tty(box["env"])
    assert nothing_changed(box) == [], f"Install ran past the gate: {nothing_changed(box)}"


def test_piped_answer_still_refuses(tmp_path: Path):
    """Piping ``install`` into the script doesn't count as typing it, so automation can't approve itself."""
    box = make_sandbox(tmp_path)
    result = run_without_tty(box["env"], stdin_text="install\n")
    assert result.returncode == 1, "A piped answer must be refused like no terminal at all"
    assert nothing_changed(box) == [], f"A piped 'install' ran the install: {nothing_changed(box)}"


def test_refusal_shows_no_preview(tmp_path: Path):
    """The terminal check comes first, so a refused run never prints the install preview."""
    output = run_without_tty(make_sandbox(tmp_path)["env"]).stdout
    assert "Type 'install' to continue" not in output, "A refused run must not reach the confirmation prompt"


def test_refusal_does_not_create_missing_target(tmp_path: Path):
    """A refused run doesn't create a config folder that doesn't exist yet."""
    box = make_sandbox(tmp_path)
    missing = tmp_path / "not_yet"
    box["env"]["CLAUDE_CONFIG_DIR"] = str(missing)
    run_without_tty(box["env"])
    assert not missing.exists(), "A refused run created the target folder"


def test_gate_runs_before_install():
    """``confirm_install`` is called before ``install_claude_files`` in the main logic."""
    lines = [line.strip() for line in INSTALL_SCRIPT.read_text().splitlines()]
    assert "confirm_install" in lines, "confirm_install is never called"
    assert lines.index("confirm_install") < lines.index("install_claude_files"), "The gate must run before files change"
