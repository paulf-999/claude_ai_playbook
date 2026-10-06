# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           2.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Every SKILL.md must carry its own must-follow instructions for Claude.

Claude reliably reads only ``SKILL.md`` when a skill loads. On 2026-10-01 the
Confluence skill's hard constraints sat in ``reference/_phases.md``, Claude
never read them, and it published straight to Confluence without the draft
review. ``_core_standards.md`` now requires an "Instructions for Claude"
section; this suite checks every installed skill has one.

Skills written before the section was required sit on ``BASELINE``: they may
lack it for now, and must leave the list as soon as they gain it.
"""
from __future__ import annotations

import re

import pytest

from _shared_paths import SKILLS_DIR

HEADING = re.compile(r"^## .*Instructions for Claude\s*$", re.MULTILINE)
PURPOSE = re.compile(r"^## .*\bPurpose\b", re.MULTILINE | re.IGNORECASE)
CONSTRAINT = re.compile(r"^\s*- \*\*(Always|Never):\*\*", re.MULTILINE)
REFERENCE = re.compile(r"reference/_\w+\.md")
NON_CONFIG_DRAFTS = re.compile(r"~/(\.claude/)?_drafts")

BASELINE = {
    "claude_setup_graphify",
    "git_create_pr",
    "jira_create",
}

VALID_SKILL_MD = """\
---
name: demo_skill
description: Create, add or publish a demo page
---
<!-- version: 1.0.0 -->

## 🤖 Instructions for Claude

- **Pre-check:** call the status tool first
- **Never:** publish before the user approves the draft
- **Always:** write drafts to `~/claude/_drafts/demo/`
- **Read first:** read `reference/_phases.md` before acting

## 🎯 Purpose

Shows the canonical structure.
"""


def instructions_section(skill_md: str) -> str | None:
    """Return the Instructions for Claude section's body.

    :param skill_md: Full SKILL.md text.
    :type skill_md: str
    :return: Text between the heading and the next ``##`` heading, or ``None`` when absent.
    :rtype: str | None
    """
    match = HEADING.search(skill_md)
    if match is None:
        return None
    rest = skill_md[match.end():]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: next_heading.start()] if next_heading else rest


def instruction_issues(skill_md: str) -> list[str]:
    """List every way a SKILL.md falls short of the instructions standard.

    :param skill_md: Full SKILL.md text.
    :type skill_md: str
    :return: One message per problem — empty when the skill passes.
    :rtype: list[str]
    """
    section = instructions_section(skill_md)
    if section is None:
        return ["missing '## 🤖 Instructions for Claude' section"]
    issues = []
    purpose = PURPOSE.search(skill_md)
    if purpose and purpose.start() < HEADING.search(skill_md).start():
        issues.append("Instructions for Claude must come before Purpose")
    if not CONSTRAINT.search(section):
        issues.append("no '- **Always:**' or '- **Never:**' constraint bullet")
    if not REFERENCE.search(section):
        issues.append("doesn't name the reference/_*.md file to read first")
    if NON_CONFIG_DRAFTS.search(section):
        issues.append("drafts path points outside the Claude config folder — use ~/claude/_drafts/<domain>/")
    return issues


def installed_skills() -> list[str]:
    """Collect installed skill names, skipping templates, tests and dot folders.

    :return: Sorted skill folder names that hold a SKILL.md.
    :rtype: list[str]
    """
    names = set()
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        parts = skill_md.parent.relative_to(SKILLS_DIR).parts
        path = "/".join(parts).lower()
        if "template" in path or "_tests" in path or any(p.startswith(".") for p in parts):
            continue
        names.add(skill_md.parent.name)
    return sorted(names)


def skill_md_for(name: str) -> str:
    """Read one installed skill's SKILL.md.

    :param name: Skill folder name.
    :type name: str
    :return: The SKILL.md text.
    :rtype: str
    """
    matches = [p for p in SKILLS_DIR.rglob(f"{name}/SKILL.md") if "template" not in str(p).lower()]
    return matches[0].read_text(encoding="utf-8")


# ── Real skills ──────────────────────────────────────────────────────────────


def test_skills_are_discovered():
    """The suite must find real skills, or every per-skill check passes vacuously."""
    assert installed_skills(), f"No skills found under {SKILLS_DIR}"


@pytest.mark.parametrize("name", installed_skills())
def test_skill_has_instructions_for_claude(name):
    """Every skill off the baseline meets the instructions standard."""
    if name in BASELINE:
        pytest.skip(f"{name} is on BASELINE — written before the section was required")
    issues = instruction_issues(skill_md_for(name))
    assert not issues, f"{name}/SKILL.md: {issues} — see authoring_skills/_lazy_load/_core_standards.md"


def test_confluence_skill_drafts_to_config_folder():
    """The Confluence skill names ~/claude/_drafts/confluence/ for drafts (moved 2026-10-06)."""
    section = instructions_section(skill_md_for("confluence_create_page"))
    assert section, "confluence_create_page has no Instructions for Claude section"
    assert "~/claude/_drafts/confluence/" in section, "drafts path ~/claude/_drafts/confluence/ is missing"
    assert "getAccessibleAtlassianResources" in section, "the Atlassian MCP pre-check is missing"


@pytest.mark.parametrize("name", sorted(BASELINE))
def test_baseline_skill_leaves_list_once_fixed(name):
    """A baseline skill that now passes must be removed from BASELINE, so the list only shrinks."""
    assert name in installed_skills(), f"{name} is on BASELINE but no longer installed — remove it"
    assert instruction_issues(skill_md_for(name)), f"{name} now passes — remove it from BASELINE"


# ── The check catches each kind of breakage ──────────────────────────────────


def test_valid_fixture_passes():
    """Baseline: the fixture passes, so each negative test isolates one break."""
    assert instruction_issues(VALID_SKILL_MD) == []


def test_missing_section_is_caught():
    """A SKILL.md with no instructions heading fails."""
    skill_md = VALID_SKILL_MD.replace("## 🤖 Instructions for Claude", "## 🤖 Notes")
    assert instruction_issues(skill_md) == ["missing '## 🤖 Instructions for Claude' section"]


def test_section_after_purpose_is_caught():
    """Instructions placed below Purpose fail, because Claude reads top-down."""
    head, body = VALID_SKILL_MD.split("## 🤖 Instructions for Claude")
    instructions, purpose = body.split("## 🎯 Purpose")
    skill_md = f"{head}## 🎯 Purpose{purpose}\n## 🤖 Instructions for Claude{instructions}"
    issues = instruction_issues(skill_md)
    assert "Instructions for Claude must come before Purpose" in issues


def test_missing_constraint_is_caught():
    """A section with no Always/Never bullet fails."""
    skill_md = VALID_SKILL_MD.replace("**Never:**", "**Note:**").replace("**Always:**", "**Tip:**")
    issues = instruction_issues(skill_md)
    assert issues == ["no '- **Always:**' or '- **Never:**' constraint bullet"]


def test_single_constraint_is_enough():
    """One Never bullet on its own satisfies the constraint check."""
    skill_md = VALID_SKILL_MD.replace("**Always:**", "**Tip:**")
    assert instruction_issues(skill_md) == []


def test_missing_reference_pointer_is_caught():
    """A section that doesn't name a reference/ file fails."""
    skill_md = VALID_SKILL_MD.replace("`reference/_phases.md`", "the phases file")
    assert instruction_issues(skill_md) == ["doesn't name the reference/_*.md file to read first"]


@pytest.mark.parametrize("bad_path", ["~/_drafts/demo/", "~/.claude/_drafts/demo/"])
def test_non_config_drafts_path_is_caught(bad_path):
    """A drafts path outside the Claude config folder fails (moved 2026-10-06)."""
    skill_md = VALID_SKILL_MD.replace("~/claude/_drafts/demo/", bad_path)
    issues = instruction_issues(skill_md)
    assert any("outside the Claude config folder" in issue for issue in issues), issues


def test_config_drafts_path_is_allowed():
    """The ~/claude/_drafts/ path doesn't trip the outside-config check."""
    assert "~/claude/_drafts/demo/" in instructions_section(VALID_SKILL_MD)
    assert not NON_CONFIG_DRAFTS.search(instructions_section(VALID_SKILL_MD))


def test_section_stops_at_next_heading():
    """Text under later headings isn't counted as part of the instructions."""
    section = instructions_section(VALID_SKILL_MD)
    assert "Shows the canonical structure" not in section
    assert "**Never:**" in section


def test_constraint_outside_section_does_not_count():
    """An Always bullet under Purpose doesn't satisfy the check."""
    skill_md = VALID_SKILL_MD.replace("**Never:**", "**Note:**").replace("**Always:**", "**Tip:**")
    skill_md += "\n- **Always:** this sits under Purpose\n"
    assert "no '- **Always:**' or '- **Never:**' constraint bullet" in instruction_issues(skill_md)
