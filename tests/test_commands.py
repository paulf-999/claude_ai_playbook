"""Structural tests for Claude command definition files.

Validates that every command .md file in src/claude/commands/ is non-empty,
and that every file linked from commands/README.md exists on disk.
"""

import re
from pathlib import Path

import pytest

COMMANDS_DIR = Path(__file__).parent.parent / "src" / "claude" / "commands"

command_files = [
    path
    for path in COMMANDS_DIR.glob("*.md")
    if path.name.lower() != "readme.md"
]


def _extract_md_links(readme_path: Path) -> list[tuple[str, Path]]:
    """Extract (link_text, resolved_path) pairs for .md file links in a README.

    :param readme_path: Path to the README file to parse.
    :type readme_path: Path
    :return: List of (link_text, resolved_path) tuples for .md links.
    :rtype: list[tuple[str, Path]]
    """
    content = readme_path.read_text()
    # Match markdown links: [text](href) where href ends in .md
    matches = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", content)
    return [
        (text, (readme_path.parent / href).resolve())
        for text, href in matches
        if not href.startswith("http")  # ignore external URLs; only validate local file links
    ]


@pytest.mark.parametrize("command_path", command_files, ids=[p.name for p in command_files])
def test_command_file_is_non_empty(command_path: Path) -> None:
    """Every command file must contain at least one non-blank line of content.

    :param command_path: Path to the command markdown file.
    :type command_path: Path
    """
    content = command_path.read_text().strip()
    assert content, f"{command_path.name}: file is empty"


def test_commands_readme_links_exist() -> None:
    """Every .md file linked from commands/README.md must exist on disk."""
    readme = COMMANDS_DIR / "README.md"
    assert readme.exists(), "commands/README.md is missing"

    links = _extract_md_links(readme)
    assert links, "commands/README.md contains no .md file links"

    missing = [(text, path) for text, path in links if not path.exists()]
    assert not missing, (
        "commands/README.md links to missing files:\n"
        + "\n".join(f"  [{text}] -> {path}" for text, path in missing)
    )
