# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 3/10
# Python style compliant: Yes
# Date created:      2026-09-18
# Version:           1.0.0
# Date updated:      2026-09-18
# ─────────────────────────────────────────────────────────

"""
Test: session_start_mcp_stale_settings hook

Validates that the SessionStart hook correctly detects a recently-modified
settings.json (within the last 5 minutes) and shows a one-time reminder to
restart Claude Code, per the mcp_server_toggling.md restart requirement.

Covers:
- Missing settings.json: exits cleanly, no warning
- Flag file already present: skips the check (once-per-session dedup)
- Fresh settings.json (<300s old): shows the warning and creates the flag
- Stale settings.json (>300s old): no warning
- The 300-second boundary itself
- Warning message content and idempotency across repeated runs
- Paths are resolved relative to the hook's own location, not a hardcoded
  ~/.claude/ or $HOME reference (see portable_paths.md)

Mode: SessionStart, soft injection (never blocks; always exits 0)
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

from _claude_dir import CLAUDE_DIR

HOOK_SOURCE = CLAUDE_DIR / "hooks" / "hook_session_start_mcp_stale_settings.sh"


def _hook_env(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Copy the hook into an isolated tmp_path/hooks/ tree and return key paths.

    Mirrors the hook's own layout assumption (hooks/ as a sibling of the
    config root) so CLAUDE_ROOT_DIR resolves inside tmp_path, never the real
    repo — this is what proves the hook is portable rather than hardcoded.

    :param tmp_path: pytest's per-test temporary directory.
    :type tmp_path: Path
    :return: (hook script path, settings.json path, flag file path) inside tmp_path.
    :rtype: tuple[Path, Path, Path]
    """
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()
    hook_path = hooks_dir / "hook_session_start_mcp_stale_settings.sh"
    shutil.copy(HOOK_SOURCE, hook_path)
    hook_path.chmod(0o755)
    settings_path = tmp_path / "settings.json"
    flag_path = tmp_path / ".stale_settings_warning_shown"
    return hook_path, settings_path, flag_path


def _run(hook_path: Path) -> subprocess.CompletedProcess[str]:
    """Run the hook with no stdin payload — SessionStart hooks receive none.

    :param hook_path: Path to the isolated copy of the hook script.
    :type hook_path: Path
    :return: The completed process result including stdout and returncode.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(
        ["bash", str(hook_path)],
        input="",
        capture_output=True,
        text=True,
    )


def test_missing_settings_file_exits_cleanly(tmp_path):
    """No settings.json at all: hook exits 0 with no output."""
    hook_path, settings_path, _flag_path = _hook_env(tmp_path)
    assert not settings_path.exists()

    result = _run(hook_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_fresh_settings_shows_warning(tmp_path):
    """settings.json modified moments ago triggers the restart reminder."""
    hook_path, settings_path, flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")

    result = _run(hook_path)

    assert result.returncode == 0
    assert "restart" in result.stdout.lower()
    assert "MCP" in result.stdout
    assert flag_path.exists(), "hook should create the dedup flag after warning"


def test_fresh_settings_creates_flag_file_only_once(tmp_path):
    """A second run after the flag exists stays silent — no duplicate warning."""
    hook_path, settings_path, flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")

    first = _run(hook_path)
    second = _run(hook_path)

    assert first.returncode == 0
    assert second.returncode == 0
    assert "restart" in first.stdout.lower()
    assert second.stdout.strip() == "", "second run should be silent once flagged"
    assert flag_path.exists()


def test_flag_file_present_skips_check(tmp_path):
    """Pre-existing flag file suppresses the warning even for fresh settings."""
    hook_path, settings_path, flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")
    flag_path.write_text("")

    result = _run(hook_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_stale_settings_no_warning(tmp_path):
    """settings.json modified well over 5 minutes ago produces no warning."""
    hook_path, settings_path, flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")
    stale_time = time.time() - 600  # 10 minutes ago
    os.utime(settings_path, (stale_time, stale_time))

    result = _run(hook_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""
    assert not flag_path.exists(), "no flag should be written when nothing was shown"


def test_boundary_just_under_five_minutes_warns(tmp_path):
    """A file modified 299 seconds ago is still within the stale window."""
    hook_path, settings_path, _flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")
    just_inside = time.time() - 299
    os.utime(settings_path, (just_inside, just_inside))

    result = _run(hook_path)

    assert result.returncode == 0
    assert "restart" in result.stdout.lower()


def test_boundary_over_five_minutes_no_warning(tmp_path):
    """A file modified 301 seconds ago falls outside the stale window."""
    hook_path, settings_path, _flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")
    just_outside = time.time() - 301
    os.utime(settings_path, (just_outside, just_outside))

    result = _run(hook_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_hook_never_blocks(tmp_path):
    """The hook is a soft reminder — every branch must exit 0, never fail the session."""
    hook_path, settings_path, _flag_path = _hook_env(tmp_path)

    missing_result = _run(hook_path)
    settings_path.write_text("{}")
    fresh_result = _run(hook_path)

    assert missing_result.returncode == 0
    assert fresh_result.returncode == 0


def test_hook_resolves_paths_relative_to_own_location(tmp_path):
    """The hook must never hardcode ~/.claude/ or $HOME — see portable_paths.md."""
    content = HOOK_SOURCE.read_text()

    assert "${HOME}/.claude" not in content
    assert "~/.claude/settings.json" not in content
    assert "BASH_SOURCE" in content, "hook must resolve its own directory dynamically"


def test_warning_message_mentions_restart_and_hang_symptom(tmp_path):
    """The warning text should name both the fix (restart) and the symptom (hanging tools)."""
    hook_path, settings_path, _flag_path = _hook_env(tmp_path)
    settings_path.write_text("{}")

    result = _run(hook_path)

    assert "restart" in result.stdout.lower()
    assert "hanging" in result.stdout.lower() or "hang" in result.stdout.lower()
