# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-28
# Date updated:      2026-10-17
# Version:           2.0.2
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the skill metadata header defined in _claude_config_metadata.md.

Every SKILL.md carries the three-line header straight after its YAML
frontmatter, holds no ``version:`` in that frontmatter, and its header
version matches ``skill.contract.yaml``.
Format cases for the shared validator live in ``_tests/_shared_checks/test_metadata_header_format.py``.
"""
from pathlib import Path

import yaml

from _metadata_header import FRONTMATTER_RE
from _metadata_header import frontmatter_header_errors as skill_header_errors
from _metadata_header import header_version_after_frontmatter as header_version
from _shared_paths import CLAUDE_DIR, SKILLS_DIR

SKILL_TEMPLATE = CLAUDE_DIR / "_templates" / "skills" / "SKILL.md.template"
HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"


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
