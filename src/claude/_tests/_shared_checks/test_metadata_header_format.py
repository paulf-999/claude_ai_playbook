# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-11
# Date updated:      2026-10-11
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Format cases for the shared metadata-header validator in ``_metadata_header.py``.

One standard (``_claude_config_metadata.md``) covers rules, skills, agents and hooks, so its
format is checked here once, on made-up inputs: field order and values, placement on
lines 1–3, the shell style after a shebang, and the header after a SKILL.md or AGENT.md frontmatter.
Merged on 2026-10-11 from the validator cases in the four per-artefact header tests, which
now keep only their real-file scans and artefact-specific checks.
"""
from __future__ import annotations

from _metadata_header import (
    FRONTMATTER_RE,
    frontmatter_header_errors,
    header_version_after_frontmatter,
    metadata_header_errors,
    shell_header_errors,
)

VALID_HEADER = "<!-- version: 1.2.10 -->\n<!-- created: 2026-09-01 -->\n<!-- updated: 2026-09-28 -->"
SHELL_HEADER = "# version: 1.0.0\n# created: 2026-09-07\n# updated: 2026-09-28\n"
FRONTMATTER = "name: demo_agent\nmaturity: tactical\ntriggers:\n  - /demo_agent\nmodel: inherit"


def with_header(**overrides: str) -> str:
    """Build a minimal rule file whose header uses defaults plus any overridden fields."""
    fields = {"version": "1.0.0", "created": "2026-09-28", "updated": "2026-09-28"} | overrides
    header = "".join(f"<!-- {field}: {value} -->\n" for field, value in fields.items())
    return f"{header}# 🗂️ Example rule\n\n**Purpose:** Example.\n"


def build_hook(header: str = SHELL_HEADER, shebang: str = "#!/bin/bash") -> str:
    """Build a minimal hook script from a shebang, header and body."""
    return f"{shebang}\n{header}# Demo hook — does nothing.\nexit 0\n"


def build_frontmatter_file(frontmatter: str = FRONTMATTER, header: str | None = None) -> str:
    """Build a minimal SKILL.md or AGENT.md: frontmatter, then a header (valid by default)."""
    header = f"{VALID_HEADER}\n" if header is None else header
    return f"---\n{frontmatter}\n---\n{header}\n# 🎯 Demo\n"


# --- Markdown header: accepted ---

def test_valid_header_accepted():
    """A well-formed header on lines 1–3 produces no errors."""
    assert metadata_header_errors(f"{VALID_HEADER}\n# 🗂️ Rule\n") == [], "valid header was rejected"


def test_same_day_created_and_updated_accepted():
    """A new file has created == updated, which must be allowed."""
    assert metadata_header_errors(with_header()) == [], "same-day dates were rejected"


def test_zero_components_accepted():
    """Zero is a valid semver component (e.g. 0.1.0, 1.0.0)."""
    for version in ("0.1.0", "1.0.0", "0.0.1"):
        assert metadata_header_errors(with_header(version=version)) == [], f"{version} was rejected"


def test_header_after_paths_frontmatter_accepted():
    """A path-scoped rule keeps its header straight after the ``paths:`` frontmatter."""
    content = f'---\npaths:\n  - "**/*.sql"\n---\n{VALID_HEADER}\n# 🗂️ Rule\n'
    frontmatter = FRONTMATTER_RE.match(content)
    assert frontmatter, "paths frontmatter was not recognised"
    body = content[frontmatter.end():]
    assert metadata_header_errors(body, line_offset=4) == [], "header after frontmatter was rejected"


def test_headerless_file_has_no_format_errors():
    """The format validator ignores absent headers; presence is checked by each real-file scan."""
    assert metadata_header_errors("# 🗂️ Rule without header\n") == [], "header-less file was flagged"
    assert metadata_header_errors("") == [], "empty file was flagged"


def test_header_example_in_code_block_ignored():
    """Header-shaped lines inside a fenced code block are examples, not a second header."""
    content = with_header() + f"\n```markdown\n{VALID_HEADER}\n```\n"
    assert metadata_header_errors(content) == [], "code-block example was treated as a header"
    only_in_block = f"# 🗂️ Rule\n```\n{VALID_HEADER}\n```\n"
    assert metadata_header_errors(only_in_block) == [], "code-block-only header should count as absent"


# --- Markdown header: rejected ---

def test_misplaced_header_rejected():
    """A header below the H1 is rejected with a lines-1–3 message."""
    errors = metadata_header_errors(f"# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "header below the H1 was accepted"
    assert "lines 1–3" in errors[0], f"unexpected error text: {errors}"


def test_duplicate_header_rejected():
    """A second header later in the file is rejected even if lines 1–3 are valid."""
    errors = metadata_header_errors(f"{VALID_HEADER}\n# 🗂️ Rule\n{VALID_HEADER}\n")
    assert errors, "duplicate header was accepted"
    assert "[1, 2, 3, 5, 6, 7]" in errors[0], f"error should name every header line: {errors}"


def test_missing_field_rejected():
    """All three lines are required."""
    errors = metadata_header_errors("<!-- version: 1.0.0 -->\n<!-- created: 2026-09-28 -->\n# 🗂️ Rule\n")
    assert errors, "two-line header was accepted"
    assert "lines 1–3" in errors[0], f"unexpected error text: {errors}"


def test_reordered_fields_rejected():
    """Fields must appear in version → created → updated order."""
    reordered = "<!-- created: 2026-09-28 -->\n<!-- version: 1.0.0 -->\n<!-- updated: 2026-09-28 -->\n"
    errors = metadata_header_errors(reordered)
    assert errors, "reordered fields were accepted"
    assert "version line" in errors[0], f"unexpected error text: {errors}"


def test_single_line_format_rejected():
    """The superseded one-line format is rejected in both comment styles."""
    html = "<!-- version: 1.0.0 | created: 2026-09-28 | updated: 2026-09-28 -->\n# 🗂️ Rule\n"
    shell = "# version: 1.0.0 | created: 2026-09-07 | updated: 2026-09-28\n"
    assert metadata_header_errors(html), "one-line markdown header was accepted"
    assert shell_header_errors(build_hook(header=shell)), "one-line hook header was accepted"


def test_malformed_semver_rejected():
    """Versions that aren't exactly MAJOR.MINOR.PATCH (no leading zeros) are rejected."""
    for version in ("1.0", "1.0.0.0", "v1.0.0", "1.0.x", "01.0.0"):
        assert metadata_header_errors(with_header(version=version)), f"version {version!r} was accepted"


def test_non_iso_date_format_rejected():
    """Dates must use hyphens (YYYY-MM-DD), not the underscore filename convention."""
    errors = metadata_header_errors(with_header(created="2026_09_28"))
    assert errors, "underscore date was accepted"
    assert "created line does not match format" in errors[0], f"unexpected error text: {errors}"


def test_impossible_date_rejected():
    """A correctly shaped but non-existent date is rejected."""
    errors = metadata_header_errors(with_header(created="2026-02-30"))
    assert errors, "2026-02-30 was accepted"
    assert "invalid date" in errors[0], f"unexpected error text: {errors}"


def test_updated_before_created_rejected():
    """updated must be on or after created."""
    errors = metadata_header_errors(with_header(updated="2026-09-01"))
    assert errors, "updated-before-created was accepted"
    assert "earlier than created" in errors[0], f"unexpected error text: {errors}"


# --- Shell header (hooks) ---

def test_valid_hook_header_accepted():
    """A shebang of any form followed by a valid three-line header produces no errors."""
    assert shell_header_errors(build_hook()) == [], "valid hook header was rejected"
    assert shell_header_errors(build_hook(shebang="#!/usr/bin/env bash")) == [], "env shebang was rejected"


def test_missing_shebang_rejected():
    """The header can't replace the shebang on line 1."""
    errors = shell_header_errors(f"{SHELL_HEADER}exit 0\n")
    assert errors, "script without shebang was accepted"
    assert "shebang" in errors[0], f"unexpected error text: {errors}"


def test_hook_header_not_on_line_2_rejected():
    """A comment or blank line between the shebang and the header is rejected, as is no header."""
    errors = shell_header_errors(build_hook(header=f"# Demo hook\n{SHELL_HEADER}"))
    assert errors, "header on line 3 was accepted"
    assert "line 2" in errors[0], f"unexpected error text: {errors}"
    assert shell_header_errors(build_hook(header="")), "hook without header was accepted"


def test_comment_styles_do_not_cross():
    """An HTML header is rejected in a script, and ``#`` lines aren't mistaken for an HTML header."""
    html = "<!-- version: 1.0.0 -->\n<!-- created: 2026-09-07 -->\n<!-- updated: 2026-09-28 -->\n"
    assert shell_header_errors(build_hook(header=html)), "HTML-comment header was accepted in a script"
    assert metadata_header_errors(SHELL_HEADER) == [], "shell header was treated as an HTML header"
    assert metadata_header_errors(SHELL_HEADER, style="shell") == [], "shell header rejected in shell style"


# --- Header after frontmatter (SKILL.md, AGENT.md) ---

def test_frontmatter_layout_accepted():
    """Lists and nested keys in the frontmatter don't disturb header detection, and the version is read."""
    nested = "name: demo_skill\nmaturity: draft\ntags:\n  status: active\n  tested: false"
    for content in (build_frontmatter_file(), build_frontmatter_file(frontmatter=nested)):
        assert frontmatter_header_errors(content) == [], f"valid layout was rejected: {content[:40]!r}"
        assert header_version_after_frontmatter(content) == "1.2.10", "header version was not read"


def test_file_must_open_with_frontmatter_rejected():
    """The frontmatter must stay on line 1 for Claude Code to parse it, even with a header first."""
    for content in ("<!-- version: 0.1.0 -->\n# demo\n", f"{VALID_HEADER}\n---\n{FRONTMATTER}\n---\n"):
        errors = frontmatter_header_errors(content)
        assert errors and "open with YAML frontmatter" in errors[0], f"missing frontmatter not caught: {errors}"


def test_version_left_in_frontmatter_rejected():
    """version must move out of the frontmatter into the header."""
    errors = frontmatter_header_errors(build_frontmatter_file(frontmatter=f"{FRONTMATTER}\nversion: 1.0.0"))
    assert errors, "frontmatter version was accepted"
    assert "not the frontmatter" in errors[0], f"unexpected error text: {errors}"


def test_header_not_directly_after_frontmatter_rejected():
    """A blank line between frontmatter and header, or no header at all, is rejected."""
    for header in (f"\n{VALID_HEADER}\n", ""):
        errors = frontmatter_header_errors(build_frontmatter_file(header=header))
        assert errors and "line after the frontmatter" in errors[0], f"bad placement not caught: {errors}"
