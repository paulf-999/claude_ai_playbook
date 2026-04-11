"""Structural tests for Claude style guide standards files.

Validates that every @./  import reference in any style guide .md file
resolves to an existing file in the repo, and that parent files containing
a Child pages table have all listed files present on disk.
"""

import re
from pathlib import Path

import pytest

STYLE_GUIDE_DIR = Path(__file__).parent.parent / "src" / "claude" / "style_guide_standards"
CLAUDE_DIR = Path(__file__).parent.parent / "src" / "claude"

CLAUDE_HOME_ALIAS = "~/.claude/"
CLAUDE_HOME_REPO = str(CLAUDE_DIR) + "/"


def _extract_at_imports(md_path: Path) -> list[tuple[Path, str]]:
    """Extract all @import references from a markdown file.

    Handles:
    - @./relative/path.md  (relative to the file's directory)
    - @~/.claude/path.md   (relative to src/claude/)

    :param md_path: Path to the markdown file.
    :type md_path: Path
    :return: List of (source_file, resolved_absolute_path) tuples.
    :rtype: list[tuple[Path, str]]
    """
    content = md_path.read_text()
    results = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("@./"):
            # strip the leading '@' only; './' is kept so Path resolves it relative to the file's directory
            relative = line[1:]
            resolved = str((md_path.parent / relative).resolve())
            results.append((md_path, resolved))
        elif line.startswith("@~/.claude/"):
            resolved = line.replace(CLAUDE_HOME_ALIAS, CLAUDE_HOME_REPO)
            results.append((md_path, resolved))
    return results


def _extract_md_links(md_path: Path) -> list[tuple[str, Path]]:
    """Extract (link_text, resolved_path) pairs for .md file links in a markdown file.

    :param md_path: Path to the markdown file to parse.
    :type md_path: Path
    :return: List of (link_text, resolved_path) tuples for relative .md links.
    :rtype: list[tuple[str, Path]]
    """
    content = md_path.read_text()
    matches = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", content)
    return [
        (text, (md_path.parent / href).resolve())
        for text, href in matches
        if not href.startswith("http")
    ]


# Build parametrised list: one entry per (file, import_path) pair
_all_imports: list[tuple[Path, str]] = []
for _md_file in STYLE_GUIDE_DIR.rglob("*.md"):
    _all_imports.extend(_extract_at_imports(_md_file))

_import_ids = [
    f"{imp[0].relative_to(STYLE_GUIDE_DIR)}::{Path(imp[1]).name}"
    for imp in _all_imports
]


@pytest.mark.parametrize("source_file,import_path", _all_imports, ids=_import_ids)
def test_at_import_reference_exists(source_file: Path, import_path: str) -> None:
    """Every @import reference in a style guide file must resolve to an existing file.

    :param source_file: The markdown file containing the @import reference.
    :type source_file: Path
    :param import_path: The resolved absolute path the import points to.
    :type import_path: str
    """
    assert Path(import_path).exists(), (
        f"{source_file.relative_to(STYLE_GUIDE_DIR)}: @import not found: {import_path}"
    )


# Build parametrised list for child page table link validation.
# glob("*.md") is intentional — only top-level style guide files have Child pages tables;
# sub-pages are not expected to reference other sub-pages this way.
_child_page_files: list[Path] = [
    md for md in STYLE_GUIDE_DIR.glob("*.md")
    if "Child pages" in md.read_text() and md.name.lower() != "readme.md"
]

_child_page_ids = [f.name for f in _child_page_files]


@pytest.mark.parametrize("parent_file", _child_page_files, ids=_child_page_ids)
def test_child_pages_table_links_exist(parent_file: Path) -> None:
    """Every .md file linked in a Child pages table must exist on disk.

    :param parent_file: Path to the parent style guide file with a Child pages section.
    :type parent_file: Path
    """
    links = _extract_md_links(parent_file)
    missing = [(text, path) for text, path in links if not path.exists()]
    assert not missing, (
        f"{parent_file.name}: Child pages table links to missing files:\n"
        + "\n".join(f"  [{text}] -> {path}" for text, path in missing)
    )
