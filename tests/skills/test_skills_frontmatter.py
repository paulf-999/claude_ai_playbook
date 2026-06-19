"""Parametrised frontmatter tests run against every installed SKILL.md.

Consolidates the shared frontmatter assertions that would otherwise be duplicated
in each skill-specific behavioural test file. Individual test files retain only
their behaviour-specific assertions plus the skill-specific trigger check.
"""

from pathlib import Path


def test_frontmatter_has_maturity(skill_md_path: Path) -> None:
    """Every SKILL.md must declare a maturity level."""
    assert "maturity:" in skill_md_path.read_text().lower(), (
        f"{skill_md_path} must include a maturity field in frontmatter"
    )


def test_frontmatter_has_version(skill_md_path: Path) -> None:
    """Every SKILL.md must declare a version."""
    assert "version:" in skill_md_path.read_text().lower(), (
        f"{skill_md_path} must include a version field in frontmatter"
    )
