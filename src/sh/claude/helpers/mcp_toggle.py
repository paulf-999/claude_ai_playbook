"""Toggle MCP servers on/off by adding/removing from deniedMcpServers in $CLAUDE_CONFIG_DIR/settings.json.

Usage:
    python3 mcp_toggle.py enable <server-name> [server-name ...]
    python3 mcp_toggle.py disable <server-name> [server-name ...]
"""

import json
import os
import pathlib
import sys

# Live Claude config dir: CLAUDE_CONFIG_DIR when set, otherwise Claude Code's default ~/.claude,
# matching make install
_CONFIG_DIR = os.environ.get("CLAUDE_CONFIG_DIR") or str(pathlib.Path.home() / ".claude")
SETTINGS_PATH = pathlib.Path(_CONFIG_DIR) / "settings.json"

# Known integration servers (disabled by default)
INTEGRATION_SERVERS = ["github", "atlassian"]

# Convenience group aliases
GROUPS = {
    "dev": ["github"],
    "docs": ["atlassian"],
    "all": INTEGRATION_SERVERS,
}


def load_settings() -> dict:
    """Read settings.json, or return an empty dict if it does not exist."""
    if SETTINGS_PATH.exists():
        return json.loads(SETTINGS_PATH.read_text())
    return {}


def save_settings(settings: dict) -> None:
    """Write settings back to settings.json with a trailing newline."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2) + "\n")


def get_denied(settings: dict) -> list[dict]:
    """Return the deniedMcpServers list, or an empty list if absent."""
    return settings.get("deniedMcpServers", [])


def is_denied(denied: list[dict], server: str) -> bool:
    """Return True if server is in the denied list."""
    return any(entry.get("serverName") == server for entry in denied)


def enable_server(settings: dict, server: str) -> bool:
    """Remove server from deniedMcpServers. Returns True if a change was made."""
    denied = get_denied(settings)
    new_denied = [e for e in denied if e.get("serverName") != server]
    if len(new_denied) == len(denied):
        return False  # was not denied
    settings["deniedMcpServers"] = new_denied
    return True


def disable_server(settings: dict, server: str) -> bool:
    """Add server to deniedMcpServers. Returns True if a change was made."""
    denied = get_denied(settings)
    if is_denied(denied, server):
        return False  # already denied
    denied.append({"serverName": server})
    settings["deniedMcpServers"] = denied
    return True


def resolve_servers(names: list[str]) -> list[str]:
    """Expand group aliases to individual server names."""
    resolved = []
    for name in names:
        if name in GROUPS:
            resolved.extend(GROUPS[name])
        else:
            resolved.append(name)
    return resolved


def format_blocking_message(action: str, changed: list[str]) -> str:
    """Build the restart-required message shown after a change."""
    action_desc = "ENABLED" if action == "enable" else "DISABLED"
    servers_list = "\n".join(f"  • {s}" for s in changed)
    return f"""\n⚠️  RESTART REQUIRED — MCP SERVER STATE CHANGED
────────────────────────────────────────────────────
Servers: {action_desc}

{servers_list}

⚠️  IMPORTANT: You MUST restart Claude Code NOW.

If you don't restart, tool calls will HANG (2–6 minutes).

✓ Save your work
✓ Close Claude Code completely
✓ Reopen Claude Code
────────────────────────────────────────────────────
"""


def main() -> None:
    """Parse arguments, apply the toggle, and exit 1 if a restart is needed."""
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} enable|disable <server|group> [...]", file=sys.stderr)
        print(f"Groups: {', '.join(GROUPS.keys())}", file=sys.stderr)
        print(f"Integration servers: {', '.join(INTEGRATION_SERVERS)}", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1].lower()
    if action not in ("enable", "disable"):
        print(f"Error: action must be 'enable' or 'disable', got '{action}'", file=sys.stderr)
        sys.exit(1)

    servers = resolve_servers(sys.argv[2:])
    settings = load_settings()
    changed = []

    for server in servers:
        if action == "enable":
            if enable_server(settings, server):
                changed.append(server)
                print(f"  Enabled:  {server}")
            else:
                print(f"  Already enabled: {server}")
        else:
            if disable_server(settings, server):
                changed.append(server)
                print(f"  Disabled: {server}")
            else:
                print(f"  Already disabled: {server}")

    if changed:
        save_settings(settings)
        print(format_blocking_message(action, changed))
        sys.exit(1)  # Exit with failure to signal restart is required

    sys.exit(0)  # Exit with success if no changes


if __name__ == "__main__":
    main()
