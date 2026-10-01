# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-01
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Test: enforcement_mcp_stale_settings hook.

Validates that the UserPromptSubmit hook snapshots the session's disabled MCP servers on
its first prompt, warns once when ``deniedMcpServers`` changes mid-session, stays silent
otherwise, and fails open on bad input. Each test copies the hook into ``tmp_path`` so its
settings path resolves there, and points ``TMPDIR`` at ``tmp_path`` to isolate its state.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

from _shared_paths import CLAUDE_DIR

HOOK_SOURCE = CLAUDE_DIR / "hooks" / "hook_enforcement_mcp_stale_settings.sh"


class HookSandbox:
    """A copy of the hook with its own settings.json and state directory."""

    def __init__(self, tmp_path: Path):
        """Copy the hook into ``tmp_path/hooks/`` so it resolves settings inside ``tmp_path``.

        :param tmp_path: pytest's per-test temporary directory.
        :type tmp_path: Path
        """
        (tmp_path / "hooks").mkdir()
        self.hook = tmp_path / "hooks" / HOOK_SOURCE.name
        shutil.copy(HOOK_SOURCE, self.hook)
        self.settings = tmp_path / "settings.json"
        self.env = {**os.environ, "TMPDIR": str(tmp_path)}

    def set_denied(self, *servers: str) -> None:
        """Write a settings.json that disables the given MCP servers.

        :param servers: Server names to put in ``deniedMcpServers``.
        :type servers: str
        """
        self.settings.write_text(json.dumps({"deniedMcpServers": [{"serverName": s} for s in servers]}))

    def prompt(self, session_id: str = "session_a") -> subprocess.CompletedProcess[str]:
        """Run the hook as Claude Code would on a prompt.

        :param session_id: The session the prompt belongs to.
        :type session_id: str
        :return: The finished process.
        :rtype: subprocess.CompletedProcess
        """
        payload = json.dumps({"session_id": session_id, "prompt": "hello"})
        return subprocess.run(["bash", str(self.hook)], input=payload, capture_output=True, text=True, env=self.env)


def assert_silent(result: subprocess.CompletedProcess[str], case: str) -> None:
    """Assert the hook exited cleanly without output.

    :param result: The finished hook process.
    :type result: subprocess.CompletedProcess
    :param case: Description of the case, for the failure message.
    :type case: str
    """
    assert result.returncode == 0, f"{case}: hook exited {result.returncode} — {result.stderr}"
    assert result.stdout.strip() == "", f"{case}: expected no output, got {result.stdout!r}"


def warning_text(result: subprocess.CompletedProcess[str]) -> str:
    """Return the warning the hook printed, failing if it printed none.

    :param result: The finished hook process.
    :type result: subprocess.CompletedProcess
    :return: The ``systemMessage`` text.
    :rtype: str
    """
    assert result.returncode == 0, f"hook exited {result.returncode} — {result.stderr}"
    output = json.loads(result.stdout)
    assert output["hookSpecificOutput"]["additionalContext"] == output["systemMessage"], \
        "Claude and the user should see the same warning"
    return output["systemMessage"]


# --- Recording the session's starting state ---

def test_first_prompt_is_silent(tmp_path):
    """The first prompt only records the snapshot."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied("github")
    assert_silent(sandbox.prompt(), "first prompt")


def test_unchanged_settings_stay_silent(tmp_path):
    """Later prompts with the same disabled servers print nothing."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied("github")
    sandbox.prompt()
    assert_silent(sandbox.prompt(), "second prompt, no change")


def test_server_order_does_not_count_as_a_change(tmp_path):
    """Reordering the same servers isn't a change."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied("github", "atlassian")
    sandbox.prompt()
    sandbox.set_denied("atlassian", "github")
    assert_silent(sandbox.prompt(), "same servers, new order")


def test_non_mcp_settings_change_is_silent(tmp_path):
    """Only deniedMcpServers matters, not other settings."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    sandbox.settings.write_text(json.dumps({"deniedMcpServers": [], "cleanupPeriodDays": 30}))
    assert_silent(sandbox.prompt(), "unrelated setting changed")


# --- Warning on change ---

def test_disabling_a_server_mid_session_warns(tmp_path):
    """A server disabled after the first prompt triggers the restart warning."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    sandbox.set_denied("sequential-thinking")
    message = warning_text(sandbox.prompt())
    assert "sequential-thinking" in message, f"warning doesn't name the server: {message}"
    assert "restart" in message.lower(), f"warning doesn't say to restart: {message}"


def test_enabling_a_server_mid_session_warns(tmp_path):
    """Removing a server from the deny list is a change too."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied("atlassian")
    sandbox.prompt()
    sandbox.set_denied()
    assert '["atlassian"]' in warning_text(sandbox.prompt()), "warning doesn't show the starting list"


def test_warns_once_per_change(tmp_path):
    """The same changed list warns once, not on every prompt."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    sandbox.set_denied("github")
    warning_text(sandbox.prompt())
    assert_silent(sandbox.prompt(), "third prompt, same change")


def test_a_second_change_warns_again(tmp_path):
    """A further change after the first warning warns again."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    sandbox.set_denied("github")
    warning_text(sandbox.prompt())
    sandbox.set_denied("github", "atlassian")
    assert "atlassian" in warning_text(sandbox.prompt()), "second change was not reported"


def test_reverting_the_change_goes_quiet(tmp_path):
    """Putting the starting list back means there's nothing to restart for."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    sandbox.set_denied("github")
    warning_text(sandbox.prompt())
    sandbox.set_denied()
    assert_silent(sandbox.prompt(), "change reverted")


def test_sessions_are_tracked_separately(tmp_path):
    """A new session snapshots the current list instead of inheriting the old one."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt("session_a")
    sandbox.set_denied("github")
    assert_silent(sandbox.prompt("session_b"), "first prompt of a new session")
    assert_silent(sandbox.prompt("session_b"), "second prompt of a new session")


# --- Failing open ---

def test_missing_settings_is_silent(tmp_path):
    """No settings.json means nothing to compare."""
    sandbox = HookSandbox(tmp_path)
    assert_silent(sandbox.prompt(), "no settings.json")


def test_invalid_session_id_is_ignored(tmp_path):
    """A missing or path-like session id never writes state."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    assert_silent(sandbox.prompt(""), "empty session id")
    assert_silent(sandbox.prompt("../escape"), "path-like session id")
    assert not (tmp_path / "escape.snapshot").exists(), "a path-like session id wrote outside the state dir"


def test_state_stays_out_of_config_dir(tmp_path):
    """State files go under TMPDIR, never next to settings.json."""
    sandbox = HookSandbox(tmp_path)
    sandbox.set_denied()
    sandbox.prompt()
    state_dir = tmp_path / "claude_mcp_stale_settings"
    assert (state_dir / "session_a.snapshot").is_file(), "snapshot was not written to the state dir"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["claude_mcp_stale_settings", "hooks", "settings.json"], \
        "hook wrote files outside its state dir"
