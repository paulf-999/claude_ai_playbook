# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 3/10
# Test complexity score: 2/10
# Python style compliant: Yes
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      2026-09-18
# ─────────────────────────────────────────────────────────

"""Tests for lazy_load/ discoverability coverage.

Verifies the design constraint that every file in _rules/05_lazy_load/ is
reachable through at least one documented discovery path, per README.md's
own stated design ("Discoverable — included in this README and referenced
from related rules"):
- Hook coverage: the file is explicitly referenced in a hook script.
- README coverage: the file (or an ancestor directory) is named in
  README.md's "What's in this directory" table — the primary discovery
  path for files with no dedicated enforcement hook.
- Transitive coverage: the file lives inside a directory whose index file
  (e.g. dbt/macros.md → dbt.md) is directly referenced by a hook.

Also verifies the inverse: every lazy_load/ path referenced by a hook
resolves to a real file on disk, so hooks cannot silently load nothing.
"""
import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, HOOKS_DIR
LAZY_LOAD_DIR = CLAUDE_DIR / "_rules" / "05_lazy_load"
README_FILE = LAZY_LOAD_DIR / "README.md"


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


def _readme_covered_files_and_dirs() -> tuple[set[Path], set[Path]]:
    """Return lazy_load files and directories named in README.md's index table.

    :return: (covered file paths, covered directory paths) mentioned by name.
    :rtype: tuple[set[Path], set[Path]]
    """
    if not README_FILE.exists():
        return set(), set()
    content = README_FILE.read_text()
    files = {LAZY_LOAD_DIR / m for m in re.findall(r"\b([\w-]+\.md)\b", content)}
    dirs = {LAZY_LOAD_DIR / m for m in re.findall(r"\b([\w-]+)/", content)}
    return files, dirs


def _has_covered_ancestor(file_path: Path, covered: set[Path], covered_dirs: set[Path]) -> bool:
    """Return True if any ancestor directory is covered by a hook index or README entry.

    A directory foo/bar/ is covered when foo/bar.md is hook-referenced (index
    convention), or when "bar/" itself is named in README.md's table.

    :param file_path: The lazy_load .md file to check.
    :type file_path: Path
    :param covered: Set of lazy_load files directly referenced by hooks.
    :type covered: set[Path]
    :param covered_dirs: Set of lazy_load directories named in README.md.
    :type covered_dirs: set[Path]
    :return: Whether the file is transitively reachable via a covered ancestor.
    :rtype: bool
    """
    current = file_path.parent
    while current != LAZY_LOAD_DIR.parent:
        if current in covered_dirs:
            return True
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
    """Every .md in lazy_load/ must be covered by a hook or named in README.md."""
    covered = _hook_lazy_load_refs()
    readme_files, readme_dirs = _readme_covered_files_and_dirs()
    covered |= readme_files
    for md_file in LAZY_LOAD_DIR.rglob("*.md"):
        if md_file.name == "README.md" or md_file in covered:
            continue
        assert _has_covered_ancestor(md_file, covered, readme_dirs), (
            f"Orphaned lazy_load file — no hook, no README.md entry, and no "
            f"covered ancestor: {md_file.relative_to(CLAUDE_DIR)}"
        )
