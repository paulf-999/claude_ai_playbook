# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Test: hook_enforcement_writing_style.sh.

The hook checks where markdown files written inside the Claude config dir live:
only known top-level files may sit at the config root, and ``_reference/`` files
must be snake_case topics with no date. Everything else is left alone. Each test
sends the same JSON payload Claude Code sends on stdin, because the old hook
read a path argument Claude Code never passes and so never fired.
"""
import json
import subprocess

import pytest
from _shared_paths import CLAUDE_DIR, HOOKS_DIR

HOOK_PATH = HOOKS_DIR / "hook_enforcement_writing_style.sh"
STYLE_RULE = "writing_style.md"


def run_hook(file_path: str, tool_name: str = "Write") -> subprocess.CompletedProcess:
    """Run the hook with a PostToolUse payload for one file.

    :param file_path: Value for the payload's ``tool_input.file_path``.
    :type file_path: str
    :param tool_name: Tool that wrote the file.
    :type tool_name: str
    :return: The completed hook run.
    :rtype: subprocess.CompletedProcess
    """
    payload = {"hook_event_name": "PostToolUse", "tool_name": tool_name, "tool_input": {"file_path": file_path}}
    return run_raw(json.dumps(payload))


def run_raw(stdin: str) -> subprocess.CompletedProcess:
    """Run the hook with raw stdin.

    :param stdin: Text to send on stdin.
    :type stdin: str
    :return: The completed hook run.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(["bash", str(HOOK_PATH)], input=stdin, text=True, capture_output=True)


def config_path(relative: str) -> str:
    """Build an absolute path inside the config dir.

    :param relative: Path relative to the config dir.
    :type relative: str
    :return: The absolute path as a string.
    :rtype: str
    """
    return str(CLAUDE_DIR / relative)


def test_valid_reference_file_passes():
    """A snake_case topic in _reference/ is allowed silently."""
    result = run_hook(config_path("_reference/claude_code_automation.md"))
    assert result.returncode == 0, f"valid reference file should pass, got {result.returncode}: {result.stderr}"
    assert result.stderr == "", f"valid reference file should give no message, got {result.stderr}"


def test_reference_child_file_passes():
    """A _<aspect>.md child under a reference topic folder is allowed."""
    result = run_hook(config_path("_reference/claude_config_architecture/_security.md"))
    assert result.returncode == 0, f"reference child file should pass, got {result.returncode}: {result.stderr}"


def test_reference_readme_passes():
    """README.md in _reference/ is allowed."""
    result = run_hook(config_path("_reference/README.md"))
    assert result.returncode == 0, f"_reference/README.md should pass, got {result.returncode}: {result.stderr}"


def test_dated_reference_file_is_flagged():
    """Reference files carry no date, so a date prefix is flagged back to Claude."""
    result = run_hook(config_path("_reference/2026_10_01_topic.md"))
    assert result.returncode == 2, f"dated reference file should exit 2, got {result.returncode}"
    assert "no date" in result.stderr, f"message should explain the no-date rule, got {result.stderr}"
    assert STYLE_RULE in result.stderr, f"message should point to {STYLE_RULE}, got {result.stderr}"


def test_badly_named_reference_file_is_flagged():
    """Hyphens or capitals in a reference file name are flagged."""
    for name in ("claude-code-automation.md", "ClaudeCode.md"):
        result = run_hook(config_path(f"_reference/{name}"))
        assert result.returncode == 2, f"_reference/{name} should exit 2, got {result.returncode}"


def test_reference_child_without_prefix_is_flagged():
    """A file inside a reference topic folder needs the _ child prefix."""
    result = run_hook(config_path("_reference/claude_config_architecture/security.md"))
    assert result.returncode == 2, f"unprefixed reference child should exit 2, got {result.returncode}"


def test_known_root_files_pass():
    """The top-level markdown files the config defines are allowed at the root."""
    for name in ("CLAUDE.md", "README.md", "TODO.md", "aliases.md", "settings_json_readme.md"):
        result = run_hook(config_path(name))
        assert result.returncode == 0, f"{name} should be allowed at the root, got {result.returncode}"


def test_stray_root_markdown_is_flagged():
    """A new markdown file at the config root is flagged back to Claude."""
    result = run_hook(config_path("random_note.md"))
    assert result.returncode == 2, f"stray root markdown should exit 2, got {result.returncode}"
    assert "config root" in result.stderr, f"message should say the root is the problem, got {result.stderr}"
    assert "random_note.md" in result.stderr, f"message should name the file, got {result.stderr}"


def test_other_config_folders_are_ignored():
    """Folders with their own conventions are left to their own checks."""
    for relative in ("_rules/05_lazy_load/Odd-Name.md", "skills/_git_skills/git_create_pr/SKILL.md", "_plans/x.md"):
        result = run_hook(config_path(relative))
        assert result.returncode == 0, f"{relative} should be ignored, got {result.returncode}"


def test_non_markdown_is_ignored():
    """Non-.md files are never checked."""
    result = run_hook(config_path("some_script.sh"))
    assert result.returncode == 0, f"non-markdown should be ignored, got {result.returncode}"
    assert result.stderr == "", f"non-markdown should give no message, got {result.stderr}"


def test_files_outside_config_are_ignored():
    """Markdown outside the config dir, like a project's README, is never checked."""
    result = run_hook(str(CLAUDE_DIR.parent / "random_note.md"))
    assert result.returncode == 0, f"files outside the config dir should be ignored, got {result.returncode}"


def test_bad_or_empty_payload_is_ignored():
    """Bad JSON, an empty payload or a missing file_path never fails the hook."""
    for stdin in ("{not json", "", json.dumps({"tool_input": {}})):
        result = run_raw(stdin)
        assert result.returncode == 0, f"payload {stdin!r} should be ignored, got {result.returncode}: {result.stderr}"


@pytest.mark.parametrize("tool_name", ["Write", "Edit"])
def test_both_registered_tools_are_checked(tool_name: str):
    """The hook is registered for Edit and Write, and flags both the same way."""
    result = run_hook(config_path("random_note.md"), tool_name)
    assert result.returncode == 2, f"{tool_name} of a stray root file should exit 2, got {result.returncode}"


def test_path_argument_still_works_for_manual_runs():
    """A path passed as the first argument is checked without any stdin."""
    result = subprocess.run(
        ["bash", str(HOOK_PATH), config_path("random_note.md")], input="", text=True, capture_output=True
    )
    assert result.returncode == 2, f"manual run with a stray root file should exit 2, got {result.returncode}"
