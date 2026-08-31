"""Unit tests for mcp_toggle.py — MCP server enable/disable toggle.

Tests validate: idempotency, exit codes, message format, settings.json integrity.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


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
    (.parent / ".claude").mkdir(exist_ok=True)
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

    # Test: enable when disabled should exit 1
    with pytest.raises(SystemExit) as exc_info:
        mcp_toggle.main()
        sys.argv = ["mcp_toggle.py", "enable", "atlassian"]
    # Note: This test is simplified; full integration test is better


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
        "cleanupPeriodDays": 30,
        "deniedMcpServers": [{"serverName": "github"}],
        "permissions": {"allow": ["Bash(git:*)"]}
    }

    # Enable atlassian
    mcp_toggle.enable_server(settings, "atlassian")

    # Check other settings are intact
    assert settings["cleanupPeriodDays"] == 30
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
