"""Toggle MCP servers on/off by adding/removing from deniedMcpServers in ~/.claude/settings.json.

Usage:
    python3 mcp_toggle.py enable <server-name> [server-name ...]
    python3 mcp_toggle.py disable <server-name> [server-name ...]
"""

import json
import pathlib
import sys


SETTINGS_PATH = pathlib.Path.home() / ".claude" / "settings.json"

# Known integration servers (disabled by default)
INTEGRATION_SERVERS = ["github", "atlassian"]

# Convenience group aliases
GROUPS = {
    "dev": ["github"],
    "docs": ["atlassian"],
    "all": INTEGRATION_SERVERS,
}


def load_settings() -> dict:
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    return {}


def save_settings(settings: dict) -> None:
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")


def get_denied(settings: dict) -> list[dict]:
    return settings.get("deniedMcpServers", [])


def is_denied(denied: list[dict], server: str) -> bool:
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


def main() -> None:
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
        print("\nRestart Claude Code for changes to take effect.")


if __name__ == "__main__":
    main()
