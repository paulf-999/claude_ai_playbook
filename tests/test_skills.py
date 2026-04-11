"""Structural tests for Claude skill definition files.

Validates that every skill directory in src/claude/skills/ has:
- A SKILL.md file
- Valid YAML frontmatter with non-empty name and description
- A name that matches the directory name
- All referenced ~/.claude/skills/... file paths exist in the repo

Discovers skills by finding all SKILL.md files at any depth under src/claude/skills/,
so both top-level skills and skills inside subdirectories (e.g. templates/) are covered.
"""

import re
from pathlib import Path

import frontmatter
import pytest

SKILLS_DIR = Path(__file__).parent.parent / "src" / "claude" / "skills"
CLAUDE_CONFIG_DIR = Path(__file__).parent.parent / "src" / "claude"

CLAUDE_HOME_ALIAS = "~/.claude/"
CLAUDE_HOME_REPO = str(CLAUDE_CONFIG_DIR) + "/"

# Discover all skill directories by locating every SKILL.md at any depth
skill_dirs = [skill_md.parent for skill_md in SKILLS_DIR.rglob("SKILL.md")]

# Use relative paths as IDs (e.g. "commit", "templates/create_pptx") for clear test output
skill_ids = [str(d.relative_to(SKILLS_DIR)) for d in skill_dirs]


def _load_skill_md(skill_dir: Path) -> frontmatter.Post:
    """Load the SKILL.md from a skill directory.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: Parsed frontmatter post object.
    :rtype: frontmatter.Post
    """
    return frontmatter.load(str(skill_dir / "SKILL.md"))


def _extract_claude_home_references(content: str) -> list[str]:
    """Extract all ~/.claude/... file path references from skill content.

    :param content: Raw markdown content of a SKILL.md file.
    :type content: str
    :return: List of resolved absolute file paths.
    :rtype: list[str]
    """
    pattern = r"~/.claude/[^\s`'\"\)>]+"  # stop at whitespace or common delimiters (backtick, quotes, brackets)
    matches = re.findall(pattern, content)
    resolved = []
    for match in matches:
        # Strip trailing punctuation that may have been captured as part of the surrounding prose
        match = match.rstrip(".,;:")
        # Skip dynamic template placeholders (e.g. {chosen_style}) — not statically resolvable
        if "{" in match or "}" in match or "<" in match:
            continue
        absolute = match.replace(CLAUDE_HOME_ALIAS, CLAUDE_HOME_REPO)
        resolved.append(absolute)
    return resolved


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_has_skill_md(skill_dir: Path) -> None:
    """Every skill directory must contain a SKILL.md file.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.exists(), f"{skill_dir.name}: missing SKILL.md"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_md_has_valid_frontmatter(skill_dir: Path) -> None:
    """SKILL.md must have parseable YAML frontmatter.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert post.metadata, f"{skill_dir.name}/SKILL.md: missing or empty frontmatter"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_md_frontmatter_has_name_and_description(skill_dir: Path) -> None:
    """SKILL.md frontmatter must have non-empty name and description fields.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert "name" in post.metadata, f"{skill_dir.name}/SKILL.md: frontmatter missing 'name'"
    assert post.metadata["name"], f"{skill_dir.name}/SKILL.md: frontmatter 'name' is empty"
    assert "description" in post.metadata, f"{skill_dir.name}/SKILL.md: frontmatter missing 'description'"
    assert post.metadata["description"], f"{skill_dir.name}/SKILL.md: frontmatter 'description' is empty"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_name_matches_directory(skill_dir: Path) -> None:
    """SKILL.md frontmatter name must match the skill directory name.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert post.metadata.get("name") == skill_dir.name, (
        f"{skill_dir.name}/SKILL.md: frontmatter name '{post.metadata.get('name')}' "
        f"does not match directory name '{skill_dir.name}'"
    )


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_file_references_exist(skill_dir: Path) -> None:
    """All ~/.claude/skills/... paths referenced in SKILL.md must exist in the repo.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    references = _extract_claude_home_references(post.content)

    missing = [ref for ref in references if not Path(ref).exists()]
    assert not missing, (
        f"{skill_dir.name}/SKILL.md: referenced files not found in repo:\n"
        + "\n".join(f"  {ref}" for ref in missing)
    )
