# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           2.2.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for hook registry integrity in settings.json.

Verifies that every hook registered in settings.json is well formed and points
to a real hook file. A typo or stale reference would otherwise silently skip a
hook with no error — Claude Code simply would not fire it.

It also checks the reverse: every hook file is either registered or listed in
``RESERVED_HOOKS`` — kept on purpose but not wired in, with the rule that explains
why. That stops a reserved hook being deleted as dead code, and a forgotten one
lingering unnoticed.
"""
import json
from pathlib import Path

from _shared_paths import CLAUDE_DIR, HOOKS_DIR, SETTINGS_FILE

# Hooks kept on purpose but not registered, mapped to the rule that explains why
RESERVED_HOOKS = {
    "hook_style_guide_response_standards.sh": "_rules/05_lazy_load/response_standards_enforcement.md",
}
RESERVED_MARKER = "RESERVED"

# Every hook command starts this way, so it finds the config dir wherever it lives
HOOK_COMMAND_PREFIX = 'bash "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/'
CONFIG_DIR_VAR = "${CLAUDE_CONFIG_DIR"

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
                hook_ref = parts[-1].strip('"') if parts else ""
                if len(parts) < 2 or not hook_ref.endswith(".sh"):
                    continue
                if hook_ref.startswith(CONFIG_DIR_VAR):
                    # "${CLAUDE_CONFIG_DIR:-<fallback>}/rest" — the shell picks the dir at run time
                    paths.append(CLAUDE_DIR / hook_ref.split("}/", 1)[1])
                elif hook_ref.startswith("~/"):
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


def test_config_dir_variable_resolves_against_config_dir():
    """A "${CLAUDE_CONFIG_DIR:-...}/hooks/x.sh" command resolves under CLAUDE_DIR, quotes and all."""
    settings = {"hooks": {"Stop": [{"hooks": [{"command": f'{HOOK_COMMAND_PREFIX}hook_a_b.sh"'}]}]}}
    expected = [CLAUDE_DIR / "hooks" / "hook_a_b.sh"]
    assert hook_paths(settings) == expected, f"should map to CLAUDE_DIR, got {hook_paths(settings)}"


def test_hook_commands_find_config_dir_at_run_time():
    """Every registered command reads CLAUDE_CONFIG_DIR, so hooks fire at ~/.claude or ~/claude alike."""
    hardcoded = [h["command"] for h in registered_hooks() if not h["command"].startswith(HOOK_COMMAND_PREFIX)]
    assert not hardcoded, (
        f"hook commands with a hardcoded config dir: {hardcoded} — "
        f"start each with {HOOK_COMMAND_PREFIX!r}, per portable_paths.md"
    )


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


def test_every_hook_file_is_registered_or_reserved():
    """Every hook script is either wired into settings.json or listed in RESERVED_HOOKS."""
    registered = {p.name for p in hook_paths(load_settings())}
    loose = sorted(p.name for p in HOOKS_DIR.glob("hook_*.sh") if p.name not in registered | set(RESERVED_HOOKS))
    assert not loose, (
        f"hook files neither registered nor reserved: {loose} — register them in settings.json, "
        "or add them to RESERVED_HOOKS with the rule that explains why they're kept"
    )


def test_reserved_hooks_exist_and_stay_unregistered():
    """Each reserved hook is still on disk and still not wired in."""
    registered = {p.name for p in hook_paths(load_settings())}
    for name in RESERVED_HOOKS:
        assert (HOOKS_DIR / name).is_file(), (
            f"reserved hook {name} is missing — restore it or drop it from RESERVED_HOOKS"
        )
        assert name not in registered, f"{name} is now registered — remove it from RESERVED_HOOKS"


def test_reserved_hooks_say_why_they_are_kept():
    """Each reserved hook and its rule both say it is kept on purpose."""
    for name, rule in RESERVED_HOOKS.items():
        header = (HOOKS_DIR / name).read_text()
        assert RESERVED_MARKER in header, f"{name} must say {RESERVED_MARKER} in its header so no one deletes it"
        assert rule in header, f"{name} must point to {rule}, the rule that explains why it's kept"
        assert name in (CLAUDE_DIR / rule).read_text(), f"{rule} must name {name} as a reserved hook"
