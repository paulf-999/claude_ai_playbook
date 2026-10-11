# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-29
# Date updated:      2026-10-11
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the hook metadata header defined in _claude_config_metadata.md.

Every hook script carries three ``#`` comment lines on lines 2–4, straight
after the shebang, one field each: version, created, updated.
Format cases for the shared validator live in ``_tests/test_metadata_header_format.py``.
"""

from pathlib import Path

from _metadata_header import shell_header_errors
from _shared_paths import HOOKS_DIR

HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"


def hook_scripts() -> list[Path]:
    """Return every hook script in the hooks directory.

    :return: Sorted ``*.sh`` paths.
    :rtype: list[Path]
    """
    return sorted(HOOKS_DIR.glob("*.sh"))


def test_hooks_exist():
    """The scan below is meaningful only if hooks are found."""
    assert hook_scripts(), f"no hook scripts found under {HOOKS_DIR}"


def test_every_hook_has_a_valid_header():
    """Every hook script has a valid three-line header on lines 2–4."""
    for hook in hook_scripts():
        errors = shell_header_errors(hook.read_text())
        assert not errors, f"{hook.name}: {errors} {HINT}"
