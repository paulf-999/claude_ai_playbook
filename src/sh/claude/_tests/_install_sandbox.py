"""Shared helpers for the install-gate tests: a throwaway home and config folder, and ways to run the installer.

Every run points ``HOME`` and ``CLAUDE_CONFIG_DIR`` at temp folders, so no test can touch a real config.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
MARKER_TEXT = "keep me"


def make_sandbox(tmp_path: Path) -> dict:
    """Build a temp home and config folder, with a marker file in the config folder.

    :param tmp_path: pytest's per-test temp directory.
    :type tmp_path: Path
    :return: Paths for ``home``, ``target`` and ``marker``, plus a clean ``env``.
    :rtype: dict
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


def run_without_tty(env: dict, stdin_text: str | None = None) -> subprocess.CompletedProcess:
    """Run the install script without a terminal, as Claude's Bash tool would.

    :param env: Environment for the script.
    :type env: dict
    :param stdin_text: Text piped to the script, or None for ``/dev/null``.
    :type stdin_text: str | None
    :return: The finished process, stdout and stderr merged.
    :rtype: subprocess.CompletedProcess
    """
    stdin = subprocess.DEVNULL if stdin_text is None else None
    return subprocess.run(
        ["bash", str(INSTALL_SCRIPT)], cwd=REPO_ROOT, env=env, input=stdin_text, stdin=stdin,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30,
    )


def run_with_tty(env: dict, keystrokes: bytes) -> tuple[int, str]:
    """Run the install script on a pseudo-terminal and type ``keystrokes`` into it.

    :param env: Environment for the script.
    :type env: dict
    :param keystrokes: Bytes typed at the prompt, e.g. ``b"no\\n"``.
    :type keystrokes: bytes
    :return: The exit code and the script's output.
    :rtype: tuple[int, str]
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


def nothing_changed(box: dict) -> list[str]:
    """List the ways an install ran past the gate: a changed marker, copied files or a backup.

    :param box: A sandbox from :func:`make_sandbox`.
    :type box: dict
    :return: One message per change found, or an empty list when nothing changed.
    :rtype: list[str]
    """
    problems = []
    if box["marker"].read_text() != MARKER_TEXT:
        problems.append("the target marker was changed")
    if [p.name for p in box["target"].iterdir()] != ["marker.txt"]:
        problems.append("files were copied into the target")
    if list(box["home"].glob(".claude_backup_*")):
        problems.append("a backup folder was created")
    return problems
