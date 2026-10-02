# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-31
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: No
# ─────────────────────────────────────────────────────────
"""Unit tests for mcp_toggle.py — MCP server enable/disable toggle.

Tests validate: idempotency, exit codes, message format, settings.json integrity.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import pytest

# mcp_toggle.py lives in the helpers folder beside this one
HELPERS_DIR = Path(__file__).resolve().parents[1] / "helpers"
sys.path.insert(0, str(HELPERS_DIR))


@pytest.fixture
def temp_settings_file():
    """Create a temporary settings.json for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"deniedMcpServers": []}, f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def mock_settings_path(temp_settings_file, monkeypatch):
    """Mock settings.json path to use temporary file."""
    monkeypatch.setenv("HOME", str(Path(temp_settings_file).parent))
    monkeypatch.setattr(
        "pathlib.Path.home",
        lambda: Path(temp_settings_file).parent
    )
    Path(temp_settings_file).parent.mkdir(parents=True, exist_ok=True)
    (Path(temp_settings_file).parent / ".claude").mkdir(exist_ok=True)
    (Path(temp_settings_file).parent / ".claude" / "settings.json").write_text(
        json.dumps({"deniedMcpServers": []})
    )


def test_enable_idempotency():
    """First enable returns changed=True, second returns changed=False."""
    import mcp_toggle

    settings = {"deniedMcpServers": [{"serverName": "atlassian"}]}

    # First enable: server is disabled, should return True
    changed = mcp_toggle.enable_server(settings, "atlassian")
    assert changed is True
    assert "deniedMcpServers" in settings
    assert not any(e.get("serverName") == "atlassian" for e in settings["deniedMcpServers"])

    # Second enable: server is already enabled, should return False
    changed = mcp_toggle.enable_server(settings, "atlassian")
    assert changed is False


def test_disable_idempotency():
    """First disable returns changed=True, second returns changed=False."""
    import mcp_toggle

    settings = {"deniedMcpServers": []}

    # First disable: server is enabled, should return True
    changed = mcp_toggle.disable_server(settings, "atlassian")
    assert changed is True
    assert any(e.get("serverName") == "atlassian" for e in settings["deniedMcpServers"])

    # Second disable: server is already disabled, should return False
    changed = mcp_toggle.disable_server(settings, "atlassian")
    assert changed is False


def test_exit_code_on_change(temp_settings_file, monkeypatch):
    """Exit code is 1 when state changes, 0 when no change."""
    # Monkeypatch settings path to use temp file
    mock_path = Path(temp_settings_file).parent / ".claude" / "settings.json"
    mock_path.parent.mkdir(parents=True, exist_ok=True)
    mock_path.write_text(json.dumps({"deniedMcpServers": []}))

    import mcp_toggle
    monkeypatch.setattr("mcp_toggle.SETTINGS_PATH", mock_path)

    # Disable when enabled: state changes, so exit 1 (restart needed)
    monkeypatch.setattr(sys, "argv", ["mcp_toggle.py", "disable", "atlassian"])
    with pytest.raises(SystemExit) as exc_info:
        mcp_toggle.main()
    assert exc_info.value.code == 1
    assert any(e.get("serverName") == "atlassian" for e in json.loads(mock_path.read_text())["deniedMcpServers"])

    # Disable again: no change, so exit 0
    with pytest.raises(SystemExit) as exc_info:
        mcp_toggle.main()
    assert exc_info.value.code == 0


def test_blocking_message_format():
    """Blocking message includes server name, action, and restart instructions."""
    import mcp_toggle

    message = mcp_toggle.format_blocking_message("enable", ["atlassian"])

    assert "RESTART REQUIRED" in message
    assert "ENABLED" in message
    assert "atlassian" in message
    assert "MUST restart Claude Code" in message
    assert "2–6 minutes" in message
    assert "Close Claude Code completely" in message


def test_settings_json_preservation():
    """Enable/disable preserves other settings in settings.json."""
    import mcp_toggle

    settings = {
        "cleanupPeriodDays": 90,
        "deniedMcpServers": [{"serverName": "github"}],
        "permissions": {"allow": ["Bash(git:*)"]}
    }

    # Enable atlassian
    mcp_toggle.enable_server(settings, "atlassian")

    # Check other settings are intact
    assert settings["cleanupPeriodDays"] == 90
    assert settings["permissions"]["allow"] == ["Bash(git:*)"]
    assert any(e.get("serverName") == "github" for e in settings["deniedMcpServers"])


def test_resolve_group_aliases():
    """Group aliases expand to server names."""
    import mcp_toggle

    result = mcp_toggle.resolve_servers(["dev"])
    assert "github" in result

    result = mcp_toggle.resolve_servers(["docs"])
    assert "atlassian" in result

    result = mcp_toggle.resolve_servers(["all"])
    assert "github" in result
    assert "atlassian" in result


def test_multiple_servers():
    """Can enable/disable multiple servers in one call."""
    import mcp_toggle

    settings = {"deniedMcpServers": []}

    # Disable both github and atlassian
    changed_github = mcp_toggle.disable_server(settings, "github")
    changed_atlassian = mcp_toggle.disable_server(settings, "atlassian")

    assert changed_github is True
    assert changed_atlassian is True
    assert len(settings["deniedMcpServers"]) == 2


def test_invalid_action_exit_code():
    """Invalid action exits with code 1."""
    import mcp_toggle

    sys.argv = ["mcp_toggle.py", "invalid", "server"]
    with pytest.raises(SystemExit) as exc_info:
        mcp_toggle.main()
    assert exc_info.value.code == 1


MCP_TOGGLE = HELPERS_DIR / "mcp_toggle.py"


def run_toggle(home: Path, config_dir: Optional[Path]) -> subprocess.CompletedProcess:
    """Run mcp_toggle.py as a script with a temp HOME and an optional CLAUDE_CONFIG_DIR."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env["HOME"] = str(home)
    if config_dir is not None:
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    return subprocess.run(
        [sys.executable, str(MCP_TOGGLE), "disable", "atlassian"],
        env=env, capture_output=True, text=True, timeout=30,
    )


def test_unset_config_dir_refuses(tmp_path):
    """An unset CLAUDE_CONFIG_DIR exits 1, explains the fix, and never falls back to ~/.claude."""
    result = run_toggle(tmp_path, None)
    assert result.returncode == 1
    assert "CLAUDE_CONFIG_DIR is not set" in result.stderr
    assert not (tmp_path / ".claude").exists(), "mcp_toggle fell back to ~/.claude"


def test_writes_to_config_dir(tmp_path):
    """Settings are written under CLAUDE_CONFIG_DIR, not ~/.claude."""
    config_dir = tmp_path / "claude"
    config_dir.mkdir()
    (config_dir / "settings.json").write_text(json.dumps({"deniedMcpServers": []}))
    result = run_toggle(tmp_path, config_dir)
    assert result.returncode == 1, "A change should exit 1 to signal a restart"
    denied = json.loads((config_dir / "settings.json").read_text())["deniedMcpServers"]
    assert any(e.get("serverName") == "atlassian" for e in denied)
    assert not (tmp_path / ".claude").exists(), "mcp_toggle wrote to ~/.claude"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
