# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-28
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

"""Validates the skill metadata header defined in _claude_config_metadata.md.

Every SKILL.md carries the three-line header straight after its YAML
frontmatter, holds no ``version:`` in that frontmatter, and its header
version matches ``skill.contract.yaml``.
"""
import re
from pathlib import Path
from typing import Optional

import yaml
from _metadata_header import FIELD_PATTERNS, metadata_header_errors
from _shared_paths import CLAUDE_DIR, SKILLS_DIR

SKILL_TEMPLATE = CLAUDE_DIR / "_templates" / "skills" / "SKILL.md.template"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
HINT = "— see 03_authoring_guidelines/_claude_config_metadata.md"


def skill_header_errors(content: str) -> list[str]:
    """Return errors for a SKILL.md's frontmatter-plus-header layout; empty if valid.

    :param content: Full text of a SKILL.md file.
    :type content: str
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return ["SKILL.md must open with YAML frontmatter"]
    if re.search(r"^version:", match.group(1), re.M):
        return ["version belongs in the metadata header, not the frontmatter"]
    after = content[match.end():]
    if not after.startswith("<!-- version:"):
        return ["metadata header must start on the line after the frontmatter"]
    return metadata_header_errors(after)


def header_version(content: str) -> str:
    """Return the version from the header that follows a SKILL.md's frontmatter.

    :param content: Full text of a SKILL.md file with a valid header.
    :type content: str
    :return: The semver string from the header's version line.
    :rtype: str
    """
    first_line = content[FRONTMATTER_RE.match(content).end():].splitlines()[0]
    return ".".join(FIELD_PATTERNS["version"].match(first_line).groups())


def build_skill(frontmatter: str = "name: demo_skill\nmaturity: draft", header: Optional[str] = None) -> str:
    """Build a minimal SKILL.md from a frontmatter body and an optional header.

    :param frontmatter: YAML lines between the ``---`` fences.
    :type frontmatter: str
    :param header: Header lines to place after the frontmatter; a valid default when omitted.
    :type header: Optional[str]
    :return: SKILL.md content.
    :rtype: str
    """
    if header is None:
        header = "<!-- version: 0.1.0 -->\n<!-- created: 2026-09-28 -->\n<!-- updated: 2026-09-28 -->\n"
    return f"---\n{frontmatter}\n---\n{header}\n## 🎯 Purpose\n"


def skill_dirs() -> list[Path]:
    """Return every skill directory that contains a SKILL.md, skipping hidden folders.

    Hidden folders such as Claude Code's own ``.trash/`` hold deleted third-party skills.

    :return: Skill directories under SKILLS_DIR.
    :rtype: list[Path]
    """
    return sorted(
        path.parent for path in SKILLS_DIR.rglob("SKILL.md")
        if not any(part.startswith(".") for part in path.relative_to(SKILLS_DIR).parts)
    )


# --- Validator: accepted ---

def test_valid_skill_layout_accepted():
    """Frontmatter without version, followed by a valid header, produces no errors."""
    assert skill_header_errors(build_skill()) == [], "valid skill layout was rejected"
    nested = "name: demo_skill\nmaturity: draft\ntags:\n  status: active\n  tested: false"
    assert skill_header_errors(build_skill(frontmatter=nested)) == [], "nested frontmatter was rejected"


def test_header_version_is_read_after_frontmatter():
    """The version helper reads the header line, not the frontmatter."""
    assert header_version(build_skill()) == "0.1.0", "header version was not extracted"


# --- Validator: rejected ---

def test_missing_frontmatter_rejected():
    """A SKILL.md must still open with frontmatter."""
    errors = skill_header_errors("<!-- version: 0.1.0 -->\n# demo\n")
    assert errors and "frontmatter" in errors[0], f"missing frontmatter not caught: {errors}"


def test_version_left_in_frontmatter_rejected():
    """version must move out of the frontmatter into the header."""
    errors = skill_header_errors(build_skill(frontmatter="name: demo_skill\nversion: 0.1.0"))
    assert errors and "not the frontmatter" in errors[0], f"frontmatter version not caught: {errors}"


def test_header_not_directly_after_frontmatter_rejected():
    """A blank line or content between frontmatter and header is rejected."""
    errors = skill_header_errors(build_skill(header="\n<!-- version: 0.1.0 -->\n"))
    assert errors and "line after the frontmatter" in errors[0], f"gap not caught: {errors}"


def test_missing_header_rejected():
    """A skill with no header at all is rejected."""
    errors = skill_header_errors(build_skill(header=""))
    assert errors, "missing header was accepted"
    assert "line after the frontmatter" in errors[0], f"unexpected error text: {errors}"


def test_malformed_header_rejected_by_shared_validator():
    """Header format errors come through from the shared validator."""
    bad = "<!-- version: 0.1 -->\n<!-- created: 2026-09-28 -->\n<!-- updated: 2026-09-28 -->\n"
    errors = skill_header_errors(build_skill(header=bad))
    assert errors and "version line" in errors[0], f"bad version not caught: {errors}"


# --- Real files ---

def test_skills_exist():
    """The scan below is meaningful only if skills are found."""
    assert skill_dirs(), f"no SKILL.md files found under {SKILLS_DIR}"


def test_every_skill_has_a_valid_header():
    """Every SKILL.md has a valid header straight after a version-free frontmatter."""
    for skill_dir in skill_dirs():
        errors = skill_header_errors((skill_dir / "SKILL.md").read_text())
        assert not errors, f"{skill_dir.name}: {errors} {HINT}"


def test_header_version_matches_contract():
    """The header version is the single source of truth and must match skill.contract.yaml."""
    for skill_dir in skill_dirs():
        contract = yaml.safe_load((skill_dir / "skill.contract.yaml").read_text())
        md_version = header_version((skill_dir / "SKILL.md").read_text())
        assert md_version == str(contract["version"]), (
            f"{skill_dir.name}: header version {md_version} != contract version {contract['version']}"
        )


def test_template_shows_header_after_frontmatter():
    """SKILL.md.template models the layout new skills should copy."""
    template = SKILL_TEMPLATE.read_text()
    match = FRONTMATTER_RE.match(template)
    assert match, "template does not open with frontmatter"
    assert "version:" not in match.group(1), "template frontmatter still carries version"
    after = template[match.end():].splitlines()[:3]
    assert after[0].startswith("<!-- version:"), f"template header missing: {after}"
    assert after[1].startswith("<!-- created:") and after[2].startswith("<!-- updated:"), (
        f"template header lines out of order: {after}"
    )
