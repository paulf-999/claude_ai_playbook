# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for hook registry integrity in settings.json.

Verifies that every hook registered in settings.json is well formed and points
to a real hook file. A typo or stale reference would otherwise silently skip a
hook with no error — Claude Code simply would not fire it.
"""
import json
from pathlib import Path

from _shared_paths import CLAUDE_DIR
from _shared_paths import HOOKS_DIR
from _shared_paths import SETTINGS_FILE

# Hook events Claude Code fires — a name outside this set is never triggered
KNOWN_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
    "Notification",
    "UserPromptSubmit",
    "SessionStart",
    "SessionEnd",
    "Stop",
    "SubagentStart",
    "SubagentStop",
    "PreCompact",
}


def hook_paths(settings: dict) -> list[Path]:
    """Return the hook script paths a settings dict registers.

    :param settings: Parsed settings.json.
    :type settings: dict
    :return: One path per command that ends in a ``.sh`` file.
    :rtype: list[Path]
    """
    paths = []
    for event_groups in settings.get("hooks", {}).values():
        for group in event_groups:
            for hook in group.get("hooks", []):
                parts = hook.get("command", "").split()
                if len(parts) < 2 or not parts[-1].endswith(".sh"):
                    continue
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


def load_settings() -> dict:
    """Parse the real settings.json.

    :return: The parsed settings.
    :rtype: dict
    """
    return json.loads(SETTINGS_FILE.read_text())


def registered_hooks() -> list[dict]:
    """List every hook entry in the real settings.json.

    :return: The hook dicts, each with its ``type`` and ``command``.
    :rtype: list[dict]
    """
    return [
        hook
        for event_groups in load_settings().get("hooks", {}).values()
        for group in event_groups
        for hook in group.get("hooks", [])
    ]


def test_all_registered_hooks_exist():
    """Every hook path in settings.json must resolve to a real file on disk."""
    missing = [str(p) for p in hook_paths(load_settings()) if not p.is_file()]
    assert not missing, "settings.json references hook files that do not exist:\n  " + "\n  ".join(missing)


def test_registry_is_not_empty():
    """settings.json must register at least one hook — an empty registry is a misconfiguration."""
    assert hook_paths(load_settings()), "settings.json registers no hooks"


def test_registered_hooks_live_in_hooks_dir():
    """Every registered script sits in hooks/ and follows the hook_ naming pattern."""
    for path in hook_paths(load_settings()):
        assert path.parent == HOOKS_DIR, f"{path} is registered but isn't in {HOOKS_DIR}"
        assert path.name.startswith("hook_"), f"{path.name} must start with hook_ — see naming_standards.md"


def test_events_are_known():
    """Every event key is one Claude Code fires, so no hook is silently never triggered."""
    unknown = sorted(set(load_settings().get("hooks", {})) - KNOWN_EVENTS)
    assert not unknown, f"settings.json registers hooks under unknown events {unknown} — check the event name"


def test_every_hook_is_a_command():
    """Every hook entry is a command hook with a non-empty command."""
    for hook in registered_hooks():
        assert hook.get("type") == "command", f"hook {hook} must have type 'command'"
        assert hook.get("command", "").strip(), f"hook {hook} has an empty command"


def test_no_hook_registered_twice():
    """No script is registered twice, which would run it twice per event."""
    paths = [str(p) for p in hook_paths(load_settings())]
    duplicates = sorted({p for p in paths if paths.count(p) > 1})
    assert not duplicates, f"hooks registered more than once: {duplicates}"


def test_tilde_path_resolves_against_config_dir():
    """A ~/<config-dir>/hooks/x.sh command resolves under CLAUDE_DIR, whatever the dir is called."""
    for config_dir in (".claude", "claude"):
        settings = {"hooks": {"Stop": [{"hooks": [{"command": f"bash ~/{config_dir}/hooks/hook_a_b.sh"}]}]}}
        expected = [CLAUDE_DIR / "hooks" / "hook_a_b.sh"]
        assert hook_paths(settings) == expected, f"~/{config_dir}/ should map to CLAUDE_DIR"


def test_absolute_path_is_kept():
    """An absolute script path is returned unchanged."""
    settings = {"hooks": {"Stop": [{"hooks": [{"command": "bash /opt/hooks/hook_a_b.sh"}]}]}}
    assert hook_paths(settings) == [Path("/opt/hooks/hook_a_b.sh")], "absolute paths should pass through"


def test_non_script_command_is_ignored():
    """A command that doesn't end in a .sh file isn't treated as a hook script."""
    settings = {"hooks": {"Stop": [{"hooks": [{"command": "echo done"}, {"command": "hook_a_b.sh"}]}]}}
    assert hook_paths(settings) == [], "only '<runner> <path>.sh' commands name a script"
    python_hook = {"hooks": {"Stop": [{"hooks": [{"command": "python3 /h/check.py"}]}]}}
    assert hook_paths(python_hook) == [], "non-shell scripts aren't hook scripts under this registry's convention"


def test_missing_sections_give_no_paths():
    """Settings with no hooks, or a group with no hooks list, give no paths."""
    assert hook_paths({}) == [], "settings without a hooks key register nothing"
    assert hook_paths({"hooks": {"Stop": [{"matcher": "x"}]}}) == [], "a group without hooks registers nothing"


def test_paths_keep_registration_order():
    """Paths come back in the order settings.json lists them, across events."""
    settings = {
        "hooks": {
            "PreToolUse": [{"hooks": [{"command": "bash /h/hook_a_b.sh"}]}],
            "Stop": [{"hooks": [{"command": "bash /h/hook_c_d.sh"}, {"command": "bash /h/hook_e_f.sh"}]}],
        }
    }
    expected = [Path("/h/hook_a_b.sh"), Path("/h/hook_c_d.sh"), Path("/h/hook_e_f.sh")]
    assert hook_paths(settings) == expected, f"got {hook_paths(settings)}"
