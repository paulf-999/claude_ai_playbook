"""Structural tests for Claude rules files.

Validates that every rules .md file is non-empty, and that every file
linked from the README indexes exists on disk.
"""

import re
from pathlib import Path

import pytest

RULES_DIR = Path(__file__).parent.parent / "src" / "claude" / "rules"

rule_files = [
    path
    for path in RULES_DIR.rglob("*.md")
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


@pytest.mark.parametrize("rule_path", rule_files, ids=[p.name for p in rule_files])
def test_rule_file_is_non_empty(rule_path: Path) -> None:
    """Every rules file must contain at least one non-blank line of content.

    :param rule_path: Path to the rules markdown file.
    :type rule_path: Path
    """
    content = rule_path.read_text().strip()
    assert content, f"{rule_path.name}: file is empty"


def test_rules_readme_links_exist() -> None:
    """Every .md file linked from rules/README.md must exist on disk."""
    readme = RULES_DIR / "README.md"
    assert readme.exists(), "rules/README.md is missing"

    links = _extract_md_links(readme)
    assert links, "rules/README.md contains no .md file links"

    missing = [(text, path) for text, path in links if not path.exists()]
    assert not missing, (
        "rules/README.md links to missing files:\n"
        + "\n".join(f"  [{text}] -> {path}" for text, path in missing)
    )


def test_rules_behaviour_readme_links_exist() -> None:
    """Every .md file linked from rules/behaviour/README.md must exist on disk."""
    readme = RULES_DIR / "behaviour" / "README.md"
    assert readme.exists(), "rules/behaviour/README.md is missing"

    links = _extract_md_links(readme)
    assert links, "rules/behaviour/README.md contains no .md file links"

    missing = [(text, path) for text, path in links if not path.exists()]
    assert not missing, (
        "rules/behaviour/README.md links to missing files:\n"
        + "\n".join(f"  [{text}] -> {path}" for text, path in missing)
    )
