# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           2.0.2
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Test: enforcement_naming_convention hook.

Validates that the hook denies a Write only when the new file's name has an error under
``_file_structure_validator.py``'s checks, and lets every other Write through silently:
well-named files, existing files, files outside the config dir, and Claude Code's own folders.
"""
import json

from _shared_paths import CLAUDE_DIR
from hooks.hook_test_utils import run_hook

HOOK_PATH = CLAUDE_DIR / "hooks" / "hook_enforcement_naming_convention.sh"


def write_payload(relative_path: str) -> dict:
    """Build a Write payload for a file under the config dir.

    :param relative_path: Path relative to the config dir.
    :type relative_path: str
    :return: Claude Code PreToolUse payload.
    :rtype: dict
    """
    return {"tool_name": "Write", "tool_input": {"file_path": str(CLAUDE_DIR / relative_path)}}


def deny_reason(relative_path: str) -> str:
    """Run the hook for a new file and return its deny reason, failing if it didn't deny.

    :param relative_path: Path relative to the config dir.
    :type relative_path: str
    :return: The ``permissionDecisionReason`` text.
    :rtype: str
    """
    result = run_hook(HOOK_PATH, write_payload(relative_path))
    assert result.returncode == 0, f"hook crashed for {relative_path}: {result.stderr}"
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["permissionDecision"] == "deny", f"{relative_path} was not denied: {output}"
    return output["permissionDecisionReason"]


def assert_allowed(payload: dict, case: str) -> None:
    """Assert the hook exits cleanly with no output, which lets the Write through.

    :param payload: Claude Code PreToolUse payload.
    :type payload: dict
    :param case: Description of the case, for the failure message.
    :type case: str
    """
    result = run_hook(HOOK_PATH, payload)
    assert result.returncode == 0, f"{case}: hook exited {result.returncode} — {result.stderr}"
    assert result.stdout.strip() == "", f"{case}: hook should stay silent but printed {result.stdout!r}"


# --- Denied ---

def test_kebab_case_name_denied_with_fix():
    """A hyphenated name is denied, and the reason names the file and the rule."""
    reason = deny_reason("_rules/01_essentials/new-rule.md")
    assert "new-rule.md" in reason, f"reason doesn't name the file: {reason}"
    assert "snake_case" in reason, f"reason doesn't say which rule broke: {reason}"
    assert "naming_standards.md" in reason, f"reason doesn't point to the standard: {reason}"


def test_uppercase_name_denied():
    """Capital letters break snake_case."""
    assert "NewRule.md" in deny_reason("_reference/NewRule.md"), "uppercase name was not reported"


def test_name_with_space_denied():
    """Spaces break snake_case."""
    assert "new rule.md" in deny_reason("_reference/new rule.md"), "name with a space was not reported"


def test_bad_hook_script_name_denied():
    """The rule covers every file type, not just markdown."""
    assert "hook-new.sh" in deny_reason("hooks/hook-new.sh"), "hyphenated shell script was not reported"


# --- Allowed ---

def test_snake_case_rule_allowed():
    """A well-named tier rule passes, despite the full scan's advisory "child file" note."""
    assert_allowed(write_payload("_rules/01_essentials/new_rule.md"), "snake_case tier rule")


def test_underscore_child_file_allowed():
    """A child file with the expected underscore prefix passes."""
    assert_allowed(write_payload("_rules/02_claude_standards/behaviour/_new_aspect.md"), "underscore child file")


def test_exact_name_files_allowed():
    """Required exact names such as SKILL.md pass, even though they aren't snake_case."""
    assert_allowed(write_payload("skills/_git_skills/new_skill/SKILL.md"), "new SKILL.md")
    assert_allowed(write_payload("agents/core/new_agent/AGENT.md"), "new AGENT.md")


# --- Skipped ---

def test_auto_generated_folders_skipped():
    """Claude Code's own folders (auto memory, plans) aren't checked."""
    assert_allowed(write_payload("projects/repo/memory/Feedback-Note.md"), "auto memory file")
    assert_allowed(write_payload("plans/Some-Plan.md"), "plan-mode scratch file")


def test_hidden_folders_skipped():
    """Hidden folders such as .git aren't checked."""
    assert_allowed(write_payload(".git/Bad-Name"), "file under .git")


def test_existing_file_skipped():
    """Writing over an existing file isn't a naming decision, so it passes."""
    assert (CLAUDE_DIR / "settings.json").is_file(), "fixture file settings.json is missing"
    assert_allowed(write_payload("settings.json"), "existing settings.json")


def test_outside_config_dir_skipped():
    """Project files follow their own conventions."""
    payload = {"tool_name": "Write", "tool_input": {"file_path": "/tmp/some-file.md"}}
    assert_allowed(payload, "file outside the config dir")


def test_other_tools_skipped():
    """Only Write creates files, so Edit and Bash pass untouched."""
    edit = {"tool_name": "Edit", "tool_input": {"file_path": str(CLAUDE_DIR / "_reference" / "Bad-Name.md")}}
    assert_allowed(edit, "Edit call")
    bash = {"tool_name": "Bash", "tool_input": {"command": "touch Bad-Name.md"}}
    assert_allowed(bash, "Bash call")


def test_malformed_payload_fails_open():
    """An empty payload must never block a write."""
    assert_allowed({}, "empty payload")
