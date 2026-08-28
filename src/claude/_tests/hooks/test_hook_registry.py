"""Tests for hook registry integrity in settings.json.

Verifies that every hook file referenced in settings.json exists on disk.
A typo or stale reference in settings.json would otherwise silently skip a
hook with no error — Claude Code simply would not fire it.
"""
import json
from pathlib import Path

SETTINGS = Path.home() / ".claude/settings.json"


def _registered_hook_paths() -> list[Path]:
    """Return all hook file paths referenced in settings.json.

    :return: Absolute paths extracted from hook command strings.
    :rtype: list[Path]
    """
    settings = json.loads(SETTINGS.read_text())
    paths = []
    for event_groups in settings.get("hooks", {}).values():
        for group in event_groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                parts = command.split()
                if len(parts) >= 2 and parts[-1].endswith(".sh"):
                    paths.append(Path(parts[-1]).expanduser())
    return paths


def test_all_registered_hooks_exist():
    """Every hook path in settings.json must resolve to a real file on disk."""
    missing = [str(p) for p in _registered_hook_paths() if not p.exists()]
    assert not missing, (
        "settings.json references hook files that do not exist:\n"
        + "\n".join(f"  - {p}" for p in missing)
    )


def test_registry_is_not_empty():
    """settings.json must register at least one hook — an empty registry is a misconfiguration."""
    assert _registered_hook_paths(), "settings.json registers no hooks"
