# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates the ``make install`` preview and its typed ``install`` confirmation (issue #150).

At a real terminal the script previews what it will do, then continues only when the user
types exactly ``install``. Each test runs the script on a pseudo-terminal with a temp ``HOME``
and ``CLAUDE_CONFIG_DIR`` and answers anything but ``install``, so nothing is ever installed.
Split from ``test_install_claude_files.py`` on 2026-10-02.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from _install_sandbox import REPO_ROOT, make_sandbox, nothing_changed, run_with_tty


@pytest.mark.parametrize("answer", [b"no\n", b"INSTALL\n", b"installl\n", b"\n"])
def test_anything_but_install_cancels(tmp_path: Path, answer: bytes) -> None:
    """Any answer other than exactly ``install`` (a no, the wrong case, a typo or nothing) cancels."""
    box = make_sandbox(tmp_path)
    code, output = run_with_tty(box["env"], answer)
    assert code == 1, f"Answer {answer!r} must exit 1"
    assert "Install cancelled" in output, f"Answer {answer!r} must say the install was cancelled"
    assert nothing_changed(box) == [], f"Answer {answer!r} ran the install: {nothing_changed(box)}"


def test_eof_cancels(tmp_path: Path) -> None:
    """Closing input (Ctrl-D) counts as no and still prints the cancel message."""
    box = make_sandbox(tmp_path)
    code, output = run_with_tty(box["env"], b"\x04")
    assert code == 1, "EOF at the prompt must exit 1"
    assert "Install cancelled" in output, "EOF must print the cancel message, not exit silently"


def test_preview_shows_target_and_backup(tmp_path: Path) -> None:
    """The preview names the target and a backup path under ``HOME``."""
    box = make_sandbox(tmp_path)
    _, output = run_with_tty(box["env"], b"no\n")
    assert f"Target:  {box['target']}" in output, "Preview must show CLAUDE_CONFIG_DIR as the target"
    assert f"Backup:  {box['home']}/.claude_backup_" in output, "Preview must show the backup path"


def test_preview_shows_the_repo_source(tmp_path: Path) -> None:
    """The preview names the repo's ``src/claude`` as the source of the files."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    assert f"Source:  {REPO_ROOT / 'src' / 'claude'}" in output, "Preview must show where the files come from"


def test_preview_lists_six_steps(tmp_path: Path) -> None:
    """The preview lists all six install steps."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    steps = (
        "1. Back up",
        "2. Copy",
        "3. Remove files",
        "4. Install the Claude CLI",
        "5. Install the core MCP",
        "6. Install the Claude Code plugins",
    )
    missing = [step for step in steps if step not in output]
    assert not missing, f"Preview is missing steps: {missing}"


def test_preview_comes_before_the_prompt(tmp_path: Path) -> None:
    """The user sees every step before being asked to type ``install``."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    assert output.index("6. Install the Claude Code plugins") < output.index("Type 'install' to continue"), (
        "The prompt must come after the full preview"
    )


def test_cancel_stops_before_any_later_step(tmp_path: Path) -> None:
    """A cancelled install never reaches the CLI, MCP or plugin steps."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    after_cancel = output.split("Install cancelled", 1)[1]
    assert "Optional MCP servers" not in after_cancel, "A cancelled install carried on to the final step"
    assert "Claude CLI not found" not in output, "A cancelled install reached the CLI step"


def test_prompt_asks_for_install_to_be_typed(tmp_path: Path) -> None:
    """The prompt says exactly what to type, so the user knows a plain yes won't do."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    assert "Type 'install' to continue" in output, "Preview must ask for the typed confirmation"


def test_preview_promises_a_copy_backup(tmp_path: Path) -> None:
    """The preview says the backup is a copy, so the live config stays where it is."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    assert "a copy — the target stays in place" in output, "Preview must say the backup is a copy, not a move"


def test_preview_names_the_files_it_keeps(tmp_path: Path) -> None:
    """The preview lists the user-owned files the install never overwrites."""
    _, output = run_with_tty(make_sandbox(tmp_path)["env"], b"no\n")
    kept = ("memory/", "TODO.md", "_plans/", "settings.local.json")
    missing = [name for name in kept if name not in output]
    assert not missing, f"Preview doesn't say these are kept: {missing}"
