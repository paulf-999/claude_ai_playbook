# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-30
# Date updated:      2026-10-02
# Version:           1.0.3
# Test quality score: 9/10
# Test complexity score: 3/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Tests for the ``make install`` approval gate (issue #150).

Validates that ``install_claude_files.sh`` installs only to ``$CLAUDE_CONFIG_DIR``,
refuses to run without a real terminal, and changes nothing unless the user
types ``install``. Every run uses a temp ``HOME`` and ``CLAUDE_CONFIG_DIR``.
"""

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
MAKEFILE = REPO_ROOT / "Makefile"
MARKER_TEXT = "keep me"


@pytest.fixture
def sandbox(tmp_path: Path) -> dict:
    """Build a temp home and config dir, with a marker file in the config dir.

    :param tmp_path: pytest's per-test temp directory.
    :return: Paths for ``home``, ``target`` and ``marker``, plus a clean ``env``.
    """
    home = tmp_path / "home"
    target = tmp_path / "cfg"
    home.mkdir()
    target.mkdir()
    marker = target / "marker.txt"
    marker.write_text(MARKER_TEXT)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env.update({"HOME": str(home), "CLAUDE_CONFIG_DIR": str(target)})
    return {"home": home, "target": target, "marker": marker, "env": env}


def run_without_tty(env: dict) -> subprocess.CompletedProcess:
    """Run the install script with stdin from ``/dev/null``, as Claude's Bash tool would.

    :param env: Environment for the script.
    :return: The finished process, stdout and stderr merged.
    """
    return subprocess.run(
        ["bash", str(INSTALL_SCRIPT)], cwd=REPO_ROOT, env=env,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, timeout=30,
    )


def run_with_tty(env: dict, keystrokes: bytes) -> tuple[int, str]:
    """Run the install script on a pseudo-terminal and type ``keystrokes`` into it.

    :param env: Environment for the script.
    :param keystrokes: Bytes typed at the prompt, e.g. ``b"no\\n"``.
    :return: The exit code and the script's output.
    """
    primary, secondary = os.openpty()
    proc = subprocess.Popen(
        ["bash", str(INSTALL_SCRIPT)], cwd=REPO_ROOT, env=env,
        stdin=secondary, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    os.close(secondary)
    os.write(primary, keystrokes)
    output, _ = proc.communicate(timeout=30)
    os.close(primary)
    return proc.returncode, output.decode()


def assert_nothing_changed(box: dict) -> None:
    """Check the target still holds only the marker and no backup was made.

    :param box: The ``sandbox`` fixture.
    """
    assert box["marker"].read_text() == MARKER_TEXT, "Target marker was changed — install ran past the gate"
    assert [p.name for p in box["target"].iterdir()] == ["marker.txt"], "Files were copied into the target"
    assert not list(box["home"].glob(".claude_backup_*")), "A backup dir was created — install ran past the gate"


def test_unset_config_dir_exits_non_zero(sandbox: dict) -> None:
    """An unset ``CLAUDE_CONFIG_DIR`` stops the script."""
    del sandbox["env"]["CLAUDE_CONFIG_DIR"]
    assert run_without_tty(sandbox["env"]).returncode != 0, "Script must fail when CLAUDE_CONFIG_DIR is unset"


def test_unset_config_dir_explains_fix(sandbox: dict) -> None:
    """The unset-variable error tells the user to export it."""
    del sandbox["env"]["CLAUDE_CONFIG_DIR"]
    output = run_without_tty(sandbox["env"]).stdout
    assert "CLAUDE_CONFIG_DIR is not set" in output, "Error must name the missing variable"
    assert "export CLAUDE_CONFIG_DIR" in output, "Error must show how to set the variable"


def test_unset_config_dir_touches_nothing(sandbox: dict) -> None:
    """An unset variable never falls back to ``~/.claude``."""
    del sandbox["env"]["CLAUDE_CONFIG_DIR"]
    run_without_tty(sandbox["env"])
    assert not (sandbox["home"] / ".claude").exists(), "Script fell back to ~/.claude"
    assert_nothing_changed(sandbox)


def test_no_tty_refuses(sandbox: dict) -> None:
    """Without a terminal, the script exits 1 and says why."""
    result = run_without_tty(sandbox["env"])
    assert result.returncode == 1, "Script must refuse when stdin is not a terminal"
    assert "run from your own terminal" in result.stdout, "Refusal must tell the user to use their own terminal"


def test_no_tty_changes_nothing(sandbox: dict) -> None:
    """A refused run leaves the target and home untouched."""
    run_without_tty(sandbox["env"])
    assert_nothing_changed(sandbox)


def test_tty_wrong_answer_cancels(sandbox: dict) -> None:
    """Typing anything other than ``install`` cancels the install."""
    code, output = run_with_tty(sandbox["env"], b"no\n")
    assert code == 1, "A wrong answer must exit 1"
    assert "Install cancelled" in output, "A wrong answer must say the install was cancelled"
    assert_nothing_changed(sandbox)


def test_tty_eof_cancels(sandbox: dict) -> None:
    """Closing input (Ctrl-D) counts as no and still prints the cancel message."""
    code, output = run_with_tty(sandbox["env"], b"\x04")
    assert code == 1, "EOF at the prompt must exit 1"
    assert "Install cancelled" in output, "EOF must print the cancel message, not exit silently"
    assert_nothing_changed(sandbox)


def test_tty_preview_shows_paths(sandbox: dict) -> None:
    """The preview names the target and a backup path under ``HOME``."""
    _, output = run_with_tty(sandbox["env"], b"no\n")
    assert f"Target:  {sandbox['target']}" in output, "Preview must show CLAUDE_CONFIG_DIR as the target"
    assert f"Backup:  {sandbox['home']}/.claude_backup_" in output, "Preview must show the backup path"
    assert "Type 'install' to continue" in output, "Preview must ask for the typed confirmation"


def test_tty_preview_lists_six_steps(sandbox: dict) -> None:
    """The preview lists all six install steps."""
    _, output = run_with_tty(sandbox["env"], b"no\n")
    steps = (
        "1. Back up",
        "2. Copy",
        "3. Remove files",
        "4. Install the Claude CLI",
        "5. Install the core MCP",
        "6. Install the Claude Code plugins",
    )
    for step in steps:
        assert step in output, f"Preview is missing step: {step}"


def test_gate_runs_before_install() -> None:
    """``confirm_install`` is called before ``install_claude_files`` in the main logic."""
    lines = [line.strip() for line in INSTALL_SCRIPT.read_text().splitlines()]
    assert "confirm_install" in lines, "confirm_install is never called"
    assert lines.index("confirm_install") < lines.index("install_claude_files"), "The gate must run before files change"


def test_makefile_install_target_enabled() -> None:
    """The Makefile's ``install`` target is live, phony and no longer marked disabled."""
    text = MAKEFILE.read_text()
    assert "\ninstall:\n" in text, "Makefile has no live install target"
    phony = next(line for line in text.splitlines() if line.startswith(".PHONY:"))
    assert " install " in phony, "install is not in .PHONY"
    usage = next(line for line in text.splitlines() if line.startswith("# make install "))
    assert "[DISABLED]" not in usage, "Usage line still marks make install as disabled"


def test_make_install_refuses_without_tty(sandbox: dict) -> None:
    """``make install`` from a non-terminal refuses and changes nothing."""
    result = subprocess.run(
        ["make", "install"], cwd=REPO_ROOT, env=sandbox["env"],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, timeout=30,
    )
    assert result.returncode != 0, "make install must fail without a terminal"
    assert "run from your own terminal" in result.stdout, "make install must pass through the refusal message"
    assert_nothing_changed(sandbox)
