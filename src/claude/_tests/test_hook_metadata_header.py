# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-29
# Version:           1.0.0
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Validates the hook metadata header defined in _claude_config_metadata.md.

Every hook script carries three ``#`` comment lines on lines 2–4, straight
after the shebang, one field each: version, created, updated.
"""
from pathlib import Path

from _metadata_header import metadata_header_errors, shell_header_errors
from _shared_paths import HOOKS_DIR

HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"
VALID_HEADER = "# version: 1.0.0\n# created: 2026-09-07\n# updated: 2026-09-28\n"


def build_hook(header: str = VALID_HEADER, shebang: str = "#!/bin/bash") -> str:
    """Build a minimal hook script from a shebang, header and body.

    :param header: Lines placed straight after the shebang.
    :type header: str
    :param shebang: The script's first line.
    :type shebang: str
    :return: Script content.
    :rtype: str
    """
    return f"{shebang}\n{header}# Demo hook — does nothing.\nexit 0\n"


def hook_scripts() -> list[Path]:
    """Return every hook script in the hooks directory.

    :return: Sorted ``*.sh`` paths.
    :rtype: list[Path]
    """
    return sorted(HOOKS_DIR.glob("*.sh"))


# --- Accepted ---

def test_valid_hook_header_accepted():
    """A shebang followed by a valid three-line header produces no errors."""
    assert shell_header_errors(build_hook()) == [], "valid hook header was rejected"


def test_env_shebang_accepted():
    """Any shebang form is fine, e.g. ``#!/usr/bin/env bash``."""
    assert shell_header_errors(build_hook(shebang="#!/usr/bin/env bash")) == [], "env shebang was rejected"


# --- Rejected ---

def test_missing_shebang_rejected():
    """The header can't replace the shebang on line 1."""
    errors = shell_header_errors(f"{VALID_HEADER}exit 0\n")
    assert errors, "script without shebang was accepted"
    assert "shebang" in errors[0], f"unexpected error text: {errors}"


def test_header_not_on_line_2_rejected():
    """A comment or blank line between the shebang and the header is rejected."""
    errors = shell_header_errors(build_hook(header=f"# Demo hook\n{VALID_HEADER}"))
    assert errors, "header on line 3 was accepted"
    assert "line 2" in errors[0], f"unexpected error text: {errors}"


def test_missing_header_rejected():
    """A hook with no header at all is rejected."""
    assert shell_header_errors(build_hook(header="")), "hook without header was accepted"


def test_single_line_header_rejected():
    """The combined one-line format is not accepted — each field needs its own line."""
    one_line = "# version: 1.0.0 | created: 2026-09-07 | updated: 2026-09-28\n"
    assert shell_header_errors(build_hook(header=one_line)), "one-line header was accepted"


def test_html_style_header_rejected_in_shell():
    """Markdown-style ``<!-- -->`` lines are the wrong comment syntax for a script."""
    html = "<!-- version: 1.0.0 -->\n<!-- created: 2026-09-07 -->\n<!-- updated: 2026-09-28 -->\n"
    assert shell_header_errors(build_hook(header=html)), "HTML-comment header was accepted in a script"


def test_bad_values_rejected():
    """Field values are validated exactly as for rules — semver, ISO dates, updated ≥ created."""
    bad_version = "# version: 1.0\n# created: 2026-09-07\n# updated: 2026-09-28\n"
    bad_order = "# version: 1.0.0\n# created: 2026-09-28\n# updated: 2026-09-07\n"
    assert shell_header_errors(build_hook(header=bad_version)), "bad version was accepted"
    errors = shell_header_errors(build_hook(header=bad_order))
    assert errors and "earlier than created" in errors[0], f"updated-before-created not caught: {errors}"


def test_shell_style_ignored_by_markdown_validator():
    """The default (HTML) style doesn't mistake ``#`` lines for a markdown header."""
    assert metadata_header_errors(VALID_HEADER) == [], "shell header was treated as an HTML header"
    assert metadata_header_errors(VALID_HEADER, style="shell") == [], "shell header rejected in shell style"


# --- Real hooks ---

def test_hooks_exist():
    """The scan below is meaningful only if hooks are found."""
    assert hook_scripts(), f"no hook scripts found under {HOOKS_DIR}"


def test_every_hook_has_a_valid_header():
    """Every hook script has a valid three-line header on lines 2–4."""
    for hook in hook_scripts():
        errors = shell_header_errors(hook.read_text())
        assert not errors, f"{hook.name}: {errors} {HINT}"
