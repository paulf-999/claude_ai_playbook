"""Tests for hook_style_guide_writing.sh.

Verifies the hook injects writing_style.md after edits to _rules/ files,
and passes through silently for all other paths.
"""
import json
from pathlib import Path

from hook_test_utils import run_hook

HOOK = Path.home() / ".claude/hooks/style_guides/hook_style_guide_writing.sh"
RULES_FILE = str(Path.home() / ".claude/_rules/behaviour.md")
NON_RULES_FILE = str(Path.home() / ".claude/CLAUDE.md")


def test_injects_style_reminder_for_rules_file():
    """Edit to _rules/ file — should inject writing style reminder."""
    result = run_hook(HOOK, {
        "tool_name": "Edit",
        "tool_input": {"file_path": RULES_FILE},
    })
    output = json.loads(result.stdout)
    assert "additionalContext" in output["hookSpecificOutput"]
    assert "writing style" in output["hookSpecificOutput"]["additionalContext"].lower()


def test_injects_reminder_for_write_tool():
    """Write to _rules/ file — hook must fire for Write as well as Edit."""
    result = run_hook(HOOK, {
        "tool_name": "Write",
        "tool_input": {"file_path": RULES_FILE},
    })
    output = json.loads(result.stdout)
    assert "additionalContext" in output["hookSpecificOutput"]
    assert "writing style" in output["hookSpecificOutput"]["additionalContext"].lower()


def test_ignores_non_rules_files():
    """Edit to non-_rules/ file — not governed by this hook, should pass through."""
    result = run_hook(HOOK, {
        "tool_name": "Edit",
        "tool_input": {"file_path": NON_RULES_FILE},
    })
    assert result.stdout.strip() == ""
    assert result.returncode == 0
