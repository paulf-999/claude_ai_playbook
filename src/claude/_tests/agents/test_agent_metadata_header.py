# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-29
# Date updated:      2026-10-17
# Version:           2.0.2
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the agent metadata header defined in _claude_config_metadata.md.

Every AGENT.md carries the three-line header straight after its YAML
frontmatter, holds no ``version:`` in that frontmatter, and its major
version matches its maturity (0.x draft, 1.x tactical, 2+.x strategic).
Format cases for the shared validator live in ``_tests/_shared_checks/test_metadata_header_format.py``.
"""
from pathlib import Path

import yaml

from _metadata_header import (
    FRONTMATTER_RE,
    frontmatter_header_errors,
    header_version_after_frontmatter,
)
from _shared_paths import CLAUDE_DIR

AGENTS_DIR = CLAUDE_DIR / "agents"
AGENT_TEMPLATE = CLAUDE_DIR / "_templates" / "AGENT.md.template"
HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"


def maturity_version_errors(maturity: str, version: str) -> list[str]:
    """Return an error if a version's major number doesn't match the agent's maturity.

    :param maturity: One of draft, tactical or strategic.
    :type maturity: str
    :param version: Semver string from the metadata header.
    :type version: str
    :return: A single-item error list on mismatch, otherwise empty.
    :rtype: list[str]
    """
    major = int(version.split(".")[0])
    expected = {"draft": major == 0, "tactical": major == 1, "strategic": major >= 2}
    if not expected.get(maturity, False):
        return [f"{maturity} agent must not use version {version} (0.x draft, 1.x tactical, 2+.x strategic)"]
    return []


def agent_files() -> list[Path]:
    """Return every AGENT.md under the agents directory.

    :return: Sorted AGENT.md paths.
    :rtype: list[Path]
    """
    return sorted(AGENTS_DIR.rglob("AGENT.md"))


# --- Maturity ---

def test_maturity_version_alignment():
    """Major version follows maturity: 0.x draft, 1.x tactical, 2+.x strategic."""
    assert maturity_version_errors("draft", "0.3.0") == [], "draft 0.x was rejected"
    assert maturity_version_errors("tactical", "1.2.0") == [], "tactical 1.x was rejected"
    assert maturity_version_errors("strategic", "3.0.0") == [], "strategic 3.x was rejected"
    assert maturity_version_errors("draft", "1.0.0"), "draft 1.x was accepted"
    assert maturity_version_errors("tactical", "2.0.0"), "tactical 2.x was accepted"


# --- Real agents ---

def test_agents_exist():
    """The scans below are meaningful only if agents are found."""
    assert agent_files(), f"no AGENT.md files found under {AGENTS_DIR}"


def test_every_agent_has_a_valid_header():
    """Every AGENT.md has a valid header straight after a version-free frontmatter."""
    for agent in agent_files():
        errors = frontmatter_header_errors(agent.read_text())
        assert not errors, f"{agent.parent.name}: {errors} {HINT}"


def test_agent_version_matches_maturity():
    """Each agent's header major version agrees with its frontmatter maturity."""
    for agent in agent_files():
        content = agent.read_text()
        maturity = yaml.safe_load(FRONTMATTER_RE.match(content).group(1))["maturity"]
        errors = maturity_version_errors(maturity, header_version_after_frontmatter(content))
        assert not errors, f"{agent.parent.name}: {errors}"


# --- Template ---

def test_template_frontmatter_has_no_version():
    """AGENT.md.template keeps version out of the frontmatter."""
    match = FRONTMATTER_RE.match(AGENT_TEMPLATE.read_text())
    assert match, "template does not open with frontmatter"
    assert "version:" not in match.group(1), "template frontmatter still carries version"


def test_template_shows_header_after_frontmatter():
    """The three header lines follow the template's frontmatter in order."""
    template = AGENT_TEMPLATE.read_text()
    after = template[FRONTMATTER_RE.match(template).end():].splitlines()[:3]
    assert after[0].startswith("<!-- version:"), f"template header missing: {after}"
    assert after[1].startswith("<!-- created:"), f"created line out of place: {after}"
    assert after[2].startswith("<!-- updated:"), f"updated line out of place: {after}"


def test_template_points_to_the_standard():
    """The template's guide names the shared standard so authors can find the rules."""
    assert "_claude_config_metadata.md" in AGENT_TEMPLATE.read_text(), "template doesn't reference the standard"
