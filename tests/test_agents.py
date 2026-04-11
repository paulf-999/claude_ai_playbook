"""Structural tests for Claude agent definition files.

Validates that every agent .md file in src/claude/agents/ has:
- Valid YAML frontmatter with non-empty name and description
- Required sections: Role, Responsibilities, Behaviour
"""

import re
from pathlib import Path

import frontmatter
import pytest

AGENTS_DIR = Path(__file__).parent.parent / "src" / "claude" / "agents"
REQUIRED_SECTIONS = ["role", "responsibilities", "behaviour"]

agent_files = [
    path
    for path in AGENTS_DIR.rglob("*.md")
    if path.name.lower() != "readme.md"
]


def _load(path: Path) -> frontmatter.Post:
    """Load a markdown file with YAML frontmatter.

    :param path: Path to the markdown file.
    :type path: Path
    :return: Parsed frontmatter post object.
    :rtype: frontmatter.Post
    :raises ValueError: If the file cannot be parsed.
    """
    return frontmatter.load(str(path))


def _strip_emoji(text: str) -> str:
    """Remove emoji characters from a string for section matching.

    :param text: Input string that may contain emoji.
    :type text: str
    :return: String with emoji characters removed.
    :rtype: str
    """
    return re.sub(r"[^\x00-\x7F]+", "", text)


@pytest.mark.parametrize("agent_path", agent_files, ids=[p.name for p in agent_files])
def test_agent_has_valid_frontmatter(agent_path: Path) -> None:
    """Agent file must have parseable YAML frontmatter.

    :param agent_path: Path to the agent markdown file.
    :type agent_path: Path
    """
    post = _load(agent_path)
    assert post.metadata, f"{agent_path.name}: missing or empty frontmatter"


@pytest.mark.parametrize("agent_path", agent_files, ids=[p.name for p in agent_files])
def test_agent_frontmatter_has_name_and_description(agent_path: Path) -> None:
    """Agent frontmatter must have non-empty name and description fields.

    :param agent_path: Path to the agent markdown file.
    :type agent_path: Path
    """
    post = _load(agent_path)
    assert "name" in post.metadata, f"{agent_path.name}: frontmatter missing 'name'"
    assert post.metadata["name"], f"{agent_path.name}: frontmatter 'name' is empty"
    assert "description" in post.metadata, f"{agent_path.name}: frontmatter missing 'description'"
    assert post.metadata["description"], f"{agent_path.name}: frontmatter 'description' is empty"


@pytest.mark.parametrize("agent_path", agent_files, ids=[p.name for p in agent_files])
def test_agent_has_required_sections(agent_path: Path) -> None:
    """Agent file must contain Role, Responsibilities, and Behaviour sections.

    :param agent_path: Path to the agent markdown file.
    :type agent_path: Path
    """
    post = _load(agent_path)
    # Section headings may contain emoji (e.g. '## 🧠 Behaviour'); strip before lowercasing for comparison
    content_lower = _strip_emoji(post.content).lower()

    for section in REQUIRED_SECTIONS:
        assert section in content_lower, (
            f"{agent_path.name}: missing required section '{section}'"
        )
