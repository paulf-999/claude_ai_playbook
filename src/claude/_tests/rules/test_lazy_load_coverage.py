"""Tests for lazy_load/ hook coverage.

Verifies the design constraint that every file in _rules/lazy_load/ is
reachable from at least one enforcement hook:
- Direct coverage: the file is explicitly referenced in a hook script.
- Transitive coverage: the file lives inside a directory whose index file
  (e.g. dbt/macros.md → dbt.md) is directly referenced by a hook.

Also verifies the inverse: every lazy_load/ path referenced by a hook
resolves to a real file on disk, so hooks cannot silently load nothing.
"""
import re
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
HOOKS_DIR = CLAUDE_DIR / "hooks"
LAZY_LOAD_DIR = CLAUDE_DIR / "_rules/lazy_load"


def _hook_lazy_load_refs() -> set[Path]:
    """Return the set of lazy_load .md paths referenced across all hook scripts.

    :return: Absolute paths to lazy_load .md files mentioned in any hook.
    :rtype: set[Path]
    """
    refs = set()
    for hook in HOOKS_DIR.glob("*.sh"):
        for match in re.finditer(r"lazy_load/([\w/.-]+\.md)", hook.read_text()):
            refs.add(LAZY_LOAD_DIR / match.group(1))
    return refs


def _has_covered_ancestor(file_path: Path, covered: set[Path]) -> bool:
    """Return True if any ancestor directory has a corresponding index .md in covered.

    The convention is that a directory foo/bar/ is covered when foo/bar.md is in
    the covered set — i.e. the index file for that directory is hook-referenced.

    :param file_path: The lazy_load .md file to check.
    :type file_path: Path
    :param covered: Set of lazy_load files directly referenced by hooks.
    :type covered: set[Path]
    :return: Whether the file is transitively reachable via a covered index.
    :rtype: bool
    """
    current = file_path.parent
    while current != LAZY_LOAD_DIR.parent:
        # The index for directory foo/bar/ is foo/bar.md
        candidate = current.parent / f"{current.name}.md"
        if candidate in covered:
            return True
        current = current.parent
    return False


def test_hook_references_resolve():
    """Every lazy_load/ path referenced by a hook must exist on disk."""
    for path in _hook_lazy_load_refs():
        assert path.exists(), (
            f"Hook references non-existent file: {path.relative_to(CLAUDE_DIR)}"
        )


def test_no_orphaned_lazy_load_files():
    """Every .md in lazy_load/ must be directly or transitively covered by a hook."""
    covered = _hook_lazy_load_refs()
    for md_file in LAZY_LOAD_DIR.rglob("*.md"):
        if md_file in covered:
            continue
        assert _has_covered_ancestor(md_file, covered), (
            f"Orphaned lazy_load file — no hook and no covered ancestor index: "
            f"{md_file.relative_to(CLAUDE_DIR)}"
        )
