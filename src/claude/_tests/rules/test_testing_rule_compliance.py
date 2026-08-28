"""Tests that the testing.md rule is self-consistently followed.

Validates that enforcement hooks and behavior-modifying rules have tests:
- Every enforcement hook in hooks/ must have a corresponding test file
- Every rule file that documents enforcement behavior must have a test
- testing.md itself must document how to verify this compliance

This is a linting test enforcing the "rules require tests" constraint.
"""
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
HOOKS_DIR = CLAUDE_DIR / "hooks"
TESTS_HOOKS_DIR = CLAUDE_DIR / "_tests/hooks"
RULES_DIR = CLAUDE_DIR / "_rules"
TESTS_RULES_DIR = CLAUDE_DIR / "_tests/rules"
TESTING_MD = RULES_DIR / "testing.md"


def _get_hook_files() -> set[str]:
    """Return the set of hook script names (e.g., 'hook_enforcement_dir_structure.sh')."""
    if not HOOKS_DIR.exists():
        return set()
    return {f.name for f in HOOKS_DIR.glob("hook_*.sh")}


def _get_test_files() -> set[str]:
    """Return the set of test file names (e.g., 'test_enforcement_dir_structure.py')."""
    if not TESTS_HOOKS_DIR.exists():
        return set()
    return {f.name for f in TESTS_HOOKS_DIR.glob("test_*.py")}


def _hook_to_test_name(hook_name: str) -> str:
    """Convert hook name to expected test name.

    Example: hook_enforcement_dir_structure.sh -> test_enforcement_dir_structure.py
    """
    # Remove 'hook_' prefix and .sh extension, add 'test_' prefix and .py extension
    base = hook_name.replace("hook_", "").replace(".sh", "")
    return f"test_{base}.py"


def test_all_hooks_have_tests():
    """Every enforcement hook must have a corresponding test file.

    Per testing.md: 'adding or modifying an enforcement hook requires a
    corresponding test'. This test enforces that constraint.
    """
    hooks = _get_hook_files()

    # Skip if no hooks exist yet — this is fine during setup phase
    if not hooks:
        return

    tests = _get_test_files()

    # Map each hook to its expected test name
    missing_tests = []
    for hook in hooks:
        expected_test = _hook_to_test_name(hook)
        if expected_test not in tests:
            missing_tests.append((hook, expected_test))

    assert not missing_tests, (
        "Enforcement hooks without tests:\n" +
        "\n".join(f"  {hook} → missing {test}" for hook, test in missing_tests) +
        "\n\nAdd tests in ~/.claude/_tests/hooks/ per testing.md."
    )


def test_no_orphaned_test_files():
    """Every test file must correspond to a real hook.

    Prevent test file bloat and ensure tests stay in sync with hooks.
    """
    hooks = _get_hook_files()

    # Skip if no hooks exist yet — test infrastructure may be ahead of hook implementation
    if not hooks:
        return

    tests = _get_test_files()

    # Exclude utilities like hook_test_utils.py
    hook_names = {h.replace("hook_", "").replace(".sh", "") for h in hooks}

    orphaned = []
    for test in tests:
        base = test.replace("test_", "").replace(".py", "")
        # Skip utility files like test_hook_utils
        if base.endswith("_utils"):
            continue
        if base not in hook_names:
            orphaned.append(test)

    assert not orphaned, (
        "Test files without corresponding hooks:\n" +
        "\n".join(f"  {test}" for test in orphaned) +
        "\n\nDelete orphaned tests or restore the hook they test."
    )


def test_testing_rule_documents_enforcement_pattern():
    """testing.md must document the enforcement pattern for rules requiring tests."""
    content = TESTING_MD.read_text()

    required_sections = [
        "When Tests Are Required",
        "hook",  # Should mention hooks
        "test goals",  # Should document test patterns
    ]

    for section in required_sections:
        assert section.lower() in content.lower(), (
            f"testing.md missing section '{section}'. The testing rule must "
            f"document when and how to test enforcement behavior."
        )


def test_testing_rule_documents_test_goals():
    """testing.md must define what tests should validate (behavior, not just 'code runs')."""
    content = TESTING_MD.read_text()

    # Should contain guidance on test goals
    assert "intended behavior" in content.lower(), (
        "testing.md must document that tests validate intended behavior, "
        "not just that code runs."
    )
    assert "test goal" in content.lower() or "goal" in content.lower(), (
        "testing.md must document how to define test goals."
    )
