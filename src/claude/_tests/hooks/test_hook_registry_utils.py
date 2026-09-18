# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 3/10
# Date created:      2026-08-28
# Version:           1.0.0
# Date updated:      2026-09-18
# ─────────────────────────────────────────────────────────

"""Tests for hook registry integrity in settings.json.

Verifies that every hook file referenced in settings.json exists on disk.
A typo or stale reference in settings.json would otherwise silently skip a
hook with no error — Claude Code simply would not fire it.
"""
import json
from pathlib import Path

from _claude_dir import CLAUDE_DIR

SETTINGS = CLAUDE_DIR / "settings.json"


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
                    hook_ref = parts[-1]
                    if hook_ref.startswith("~/"):
                        # "~/<config-dir-name>/rest" — strip both segments and resolve
                        # against CLAUDE_DIR. Never .expanduser(): the config dir name
                        # varies (.claude, claude, a repo checkout), and expanduser()
                        # only resolves correctly when it happens to match the real $HOME.
                        rest = hook_ref.split("/", 2)[2] if hook_ref.count("/") >= 2 else ""
                        paths.append(CLAUDE_DIR / rest)
                    else:
                        paths.append(Path(hook_ref))
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
