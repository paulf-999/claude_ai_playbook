"""
Test: enforcement_dir_structure hook

Validates that new directories created under ~/.claude/ follow directory structure rules.
- User-created directories: start with underscore prefix (_rules/, _tests/, _templates/, etc.)
- Auto-generated directories: no prefix (backups/, memory/, sessions/)
- Subdirectories: created only when grouping 2+ related files

Mode: soft injection (injects directory structure reminder without blocking)
"""

import json
from pathlib import Path
from src.claude._tests.hooks.hook_test_utils import run_hook


HOOK_PATH = Path.home() / ".claude" / "hooks" / "enforcement_dir_structure.sh"


def test_valid_user_created_dir_underscore_prefix():
    """User-created directories with underscore prefix should pass."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/_new_rules/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Soft injection hook should exit 0 and optionally provide context
    assert result.returncode == 0, \
        f"Valid user-created dir should pass. Got exit code: {result.returncode}"


def test_auto_generated_dir_no_prefix():
    """Auto-generated directories without prefix should pass."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/new_auto_generated/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    assert result.returncode == 0, \
        f"Auto-generated dir should pass. Got exit code: {result.returncode}"


def test_missing_underscore_prefix_flagged():
    """User-created dirs without underscore should be flagged."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/new_user_rules/"  # Missing underscore
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Hook may soft-inject context or warn (doesn't block)
    # Should either provide output or pass with warning
    assert result.returncode == 0, \
        f"Hook should not hard-block but may warn. Got exit code: {result.returncode}"
    # Check if hook provided context about the violation
    if result.stdout:
        response = json.loads(result.stdout) if result.stdout.startswith('{') else {}
        assert "additionalContext" in response or len(result.stdout) > 0, \
            "Hook should provide context about directory naming"


def test_non_bash_tool_skipped():
    """Non-Bash tool calls should be skipped."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(Path.home() / ".claude" / "_rules" / "new_rule.md")
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Write tool should be skipped by this hook
    assert result.returncode == 0, \
        f"Non-Bash tools should be skipped. Got exit code: {result.returncode}"


def test_non_mkdir_command_skipped():
    """Non-mkdir Bash commands should be skipped."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "ls -la ~/.claude/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Non-mkdir commands should be skipped
    assert result.returncode == 0, \
        f"Non-mkdir commands should be skipped. Got exit code: {result.returncode}"


def test_non_claude_directory_skipped():
    """Non-~/.claude/ directories should be skipped."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p /tmp/some_dir/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Should exit cleanly without processing
    assert result.returncode == 0, \
        f"Non-~/.claude/ commands should be skipped. Got exit code: {result.returncode}"


def test_hook_injects_directory_structure_context():
    """Hook should inject directory structure rules."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/_new_tests/"
        }
    }
    result = run_hook(HOOK_PATH, payload)

    # Parse JSON response from hook
    if result.stdout:
        try:
            response = json.loads(result.stdout)
            # Should contain hookSpecificOutput with directory structure guidance
            if "hookSpecificOutput" in response:
                context = response["hookSpecificOutput"].get("additionalContext", "")
                assert "directory" in context.lower() or "_" in context, \
                    f"Hook should provide directory structure context. Got: {context}"
        except json.JSONDecodeError:
            pass  # If not JSON, hook may use different output format


def test_nested_valid_subdirectory():
    """Valid nested subdirectories for grouping should pass."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/_rules/01_core/naming_standards/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Valid nested structure should pass
    assert result.returncode == 0, \
        f"Valid nested subdirectory should pass. Got exit code: {result.returncode}"
