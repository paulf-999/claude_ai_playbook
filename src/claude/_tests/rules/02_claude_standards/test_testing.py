# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           1.2.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that the testing.md rule is self-consistently followed.

Validates that enforcement hooks and behavior-modifying rules have tests:
- Every enforcement hook in hooks/ must have a corresponding test file
- Every rule file that documents enforcement behavior must have a test
- testing.md itself must document how to verify this compliance

This is a linting test enforcing the "rules require tests" constraint.
"""
from __future__ import annotations

import re

from _shared_paths import CLAUDE_DIR, HOOKS_DIR, RULES_DIR

TESTS_HOOKS_DIR = CLAUDE_DIR / "_tests/hooks"
TESTS_RULES_DIR = CLAUDE_DIR / "_tests/rules"
TESTING_MD = RULES_DIR / "02_claude_standards" / "testing.md"
TEST_METADATA_MD = RULES_DIR / "02_claude_standards" / "testing" / "_test_metadata.md"


def _get_hook_files() -> set[str]:
    """Return the hook script names, e.g. ``hook_enforcement_naming_convention.sh``.

    :return: File names of every ``hook_*.sh`` in hooks/.
    :rtype: set[str]
    """
    if not HOOKS_DIR.exists():
        return set()
    return {f.name for f in HOOKS_DIR.glob("hook_*.sh")}


def _get_test_files() -> set[str]:
    """Return the hook test file names, e.g. ``test_enforcement_naming_convention.py``.

    Recursive, because hook tests are grouped into subfolders such as
    ``enforcement/`` and ``response_standards/``.

    :return: File names of every ``test_*.py`` under _tests/hooks/.
    :rtype: set[str]
    """
    if not TESTS_HOOKS_DIR.exists():
        return set()
    return {f.name for f in TESTS_HOOKS_DIR.rglob("test_*.py")}


def _hook_to_test_name(hook_name: str) -> str:
    """Convert a hook file name to its expected test file name.

    :param hook_name: Hook file name, e.g. ``hook_enforcement_naming_convention.sh``.
    :type hook_name: str
    :return: The test name, e.g. ``test_enforcement_naming_convention.py``.
    :rtype: str
    """
    # Remove 'hook_' prefix and .sh extension, add 'test_' prefix and .py extension
    base = hook_name.replace("hook_", "").replace(".sh", "")
    return f"test_{base}.py"


def _owning_hook(test_name: str, hook_bases: set[str]) -> str | None:
    """Return the hook a test file covers, allowing one hook's tests to be split by aspect.

    ``test_<base>.py`` and ``test_<base>_<aspect>.py`` both belong to ``hook_<base>.sh``.
    When several hook names match, the longest wins, so ``test_x_inject.py`` belongs to
    ``hook_x_inject.sh`` rather than ``hook_x.sh``.

    :param test_name: Test file name, e.g. ``test_enforcement_naming_convention.py``.
    :type test_name: str
    :param hook_bases: Hook names without the ``hook_`` prefix and ``.sh`` suffix.
    :type hook_bases: set[str]
    :return: The matching hook base, or ``None`` when no hook matches.
    :rtype: str | None
    """
    base = test_name.removeprefix("test_").removesuffix(".py")
    matches = [hook for hook in hook_bases if base == hook or base.startswith(f"{hook}_")]
    return max(matches, key=len, default=None)


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
    hook_bases = {h.replace("hook_", "").replace(".sh", "") for h in hooks}
    covered = {_owning_hook(test, hook_bases) for test in tests}

    # Map each hook to its expected test name
    missing_tests = []
    for hook in hooks:
        if hook.replace("hook_", "").replace(".sh", "") not in covered:
            missing_tests.append((hook, _hook_to_test_name(hook)))

    assert not missing_tests, (
        "Enforcement hooks without tests:\n" +
        "\n".join(f"  {hook} → missing {test}" for hook, test in missing_tests) +
        "\n\nAdd tests in _tests/hooks/ per testing.md."
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
        if _owning_hook(test, hook_names) is None:
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


def test_split_test_files_map_to_the_longest_hook_name():
    """Aspect-split test files belong to their hook, and the most specific hook name wins."""
    hooks = {"style_guide_response_standards", "style_guide_response_standards_inject"}
    assert _owning_hook("test_style_guide_response_standards_flags.py", hooks) == "style_guide_response_standards", (
        "a _<aspect> split should belong to the base hook"
    )
    assert _owning_hook("test_style_guide_response_standards_inject.py", hooks) == (
        "style_guide_response_standards_inject"
    ), "an exact match on the longer hook name should win"
    assert _owning_hook("test_unrelated.py", hooks) is None, "a test matching no hook should be orphaned"


def test_owning_hook_needs_a_full_word_boundary():
    """A test name that only shares a prefix with a hook, without an underscore, isn't owned."""
    assert _owning_hook("test_enforcement_namingx.py", {"enforcement_naming"}) is None, (
        "test_enforcement_namingx.py must not count as a test for hook_enforcement_naming.sh"
    )


def test_hook_to_test_name():
    """Hook names map to test names by swapping the prefix and extension."""
    assert _hook_to_test_name("hook_enforcement_naming_convention.sh") == "test_enforcement_naming_convention.py", (
        "the expected test name for a hook changed"
    )


def test_testing_md_children_exist():
    """Every child testing.md imports exists, so none is silently unloaded."""
    children = re.findall(r"^@~/[^/]+/(\S+)$", TESTING_MD.read_text(), re.M)
    assert children, "testing.md should import its children"
    missing = [c for c in children if not (CLAUDE_DIR / c).is_file()]
    assert not missing, f"testing.md imports files that don't exist: {missing}"


def test_score_minimum_names_its_enforcer():
    """_test_metadata.md names the test that enforces the score minimum, and that test exists."""
    assert "`test_test_score_floor.py` fails any test file below quality 9" in TEST_METADATA_MD.read_text(), (
        "_test_metadata.md should say test_test_score_floor.py enforces the minimum"
    )
    assert (TESTS_RULES_DIR / "02_claude_standards" / "test_test_score_floor.py").is_file(), (
        "test_test_score_floor.py is missing, so the score minimum is no longer enforced"
    )


def test_hook_tests_exist_to_check():
    """There are hook tests to check, so the hook-to-test checks can't pass on an empty set."""
    assert _get_hook_files(), "no hook files found — HOOKS_DIR may be wrong"
    assert _get_test_files(), "no hook tests found — TESTS_HOOKS_DIR may be wrong"
