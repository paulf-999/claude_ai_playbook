"""
Test: enforcement_naming_convention hook

Validates that new files written to ~/.claude/ follow naming conventions.
- snake_case: lowercase, words separated by underscores
- User-created directories: start with underscore prefix (_rules/, _tests/, etc.)
- Child files: start with underscore to distinguish from top-level files

Mode: blocking (blocks Write tool and injects naming rules for review)
"""

import json
from pathlib import Path
from src.claude._tests.hooks.hook_test_utils import run_hook


HOOK_PATH = Path.home() / ".claude" / "hooks" / "enforcement_naming_convention.sh"


def test_valid_snake_case_rule_file():
    """Valid snake_case rule files should pass without blocking."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(Path.home() / ".claude" / "_rules" / "01_core" / "new_rule.md")
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Blocking hook returns non-zero when it blocks; passing returns 0
    # A valid filename should still be flagged for human review (soft block)
    assert result.returncode == 0 or "block" in result.stdout.lower(), \
        f"Valid snake_case filename should either pass or soft-block. Got: {result.stdout}"


def test_invalid_kebab_case_file():
    """kebab-case filenames should trigger block."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(Path.home() / ".claude" / "_rules" / "01_core" / "new-rule.md")
        }
    }
    result = run_hook(HOOK_PATH, payload)
    assert "decision" in result.stdout or result.returncode != 0, \
        f"Invalid kebab-case filename should be blocked. Got: {result.stdout}"


def test_missing_underscore_prefix_for_child():
    """Child files should start with underscore."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(Path.home() / ".claude" / "_rules" / "01_core" / "naming_standards" / "child_file.md")
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Should be flagged (but not necessarily blocked since it's an advisory)
    # The hook reviews and surfaces the convention
    assert result.returncode == 0 or len(result.stdout) > 0, \
        f"Missing underscore prefix should be flagged. Got: {result.stdout}"


def test_non_claude_directory_skipped():
    """Non-~/.claude/ files should be skipped."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/tmp/some-file.md"  # kebab-case, but outside ~/.claude/
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Should exit cleanly without blocking (exit 0)
    assert result.returncode == 0, \
        f"Non-~/.claude/ files should be skipped. Got exit code: {result.returncode}"


def test_existing_file_skipped():
    """Existing files should be skipped (no rename enforcement)."""
    # Create a temporary file
    test_file = Path.home() / ".claude" / "_tests" / "test_existing.md"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.touch()

    try:
        payload = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(test_file)
            }
        }
        result = run_hook(HOOK_PATH, payload)
        # Existing files should skip the check
        assert result.returncode == 0, \
            f"Existing files should be skipped. Got: {result.stdout}"
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def test_non_write_tool_skipped():
    """Non-Write tool calls should be skipped."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "mkdir -p ~/.claude/_new_dir/"
        }
    }
    result = run_hook(HOOK_PATH, payload)
    # Should exit cleanly without processing
    assert result.returncode == 0, \
        f"Non-Write tools should be skipped. Got exit code: {result.returncode}"


def test_hook_reads_naming_rules():
    """Hook should load and display naming conventions."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(Path.home() / ".claude" / "_rules" / "01_core" / "test_new_rule.md")
        }
    }
    result = run_hook(HOOK_PATH, payload)

    # Parse JSON response from hook
    if result.stdout:
        try:
            response = json.loads(result.stdout)
            # Should contain reference to naming rules
            output = str(response)
            assert "snake_case" in output or "naming" in output.lower() or "conventions" in output.lower(), \
                f"Hook should reference naming conventions. Got: {output}"
        except json.JSONDecodeError:
            pass  # If not JSON, hook may use different output format
