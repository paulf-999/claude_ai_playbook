# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the edge cases of the path helpers in ``_shared_paths.py``.

Most tests use these helpers on the real config, where the awkward cases rarely occur.
These tests build tiny fake configs in a temp directory so a link that climbs out of the
config, or frontmatter that has no ``paths:``, is shown to be handled.
"""
from pathlib import Path

import pytest

from _shared_paths import frontmatter_has_paths, resolve_link


def test_link_climbing_out_of_the_config_is_returned_as_written(tmp_path: Path):
    """A missing link target outside the config folder resolves to the plain relative path, not a guess."""
    config = tmp_path.resolve() / "claude"
    (config / "rules").mkdir(parents=True)
    source = config / "rules" / "rule.md"
    source.write_text("# Rule\n")
    reached = resolve_link(source, "../../outside.md")
    assert reached == tmp_path.resolve() / "outside.md", f"expected the plain relative path, got {reached}"


@pytest.mark.parametrize(("text", "expected"), [
    ('---\npaths:\n  - "**/*.py"\n---\n# X\n', True),
    ("---\ntitle: x\n---\npaths: not frontmatter\n", False),
    ("---\ntitle: never closed\n", False),
    ("# No frontmatter\n", False),
])
def test_paths_key_counts_only_inside_the_opening_block(text, expected):
    """paths: counts only inside a frontmatter block that opens the file."""
    assert frontmatter_has_paths(text) is expected, f"wrong answer for {text!r}"
