# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# Date created:      2026-08-28
# Version:           2.0.0
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Every installed skill must pass the skill authoring gate's crawl criteria.

The current skill standard (``authoring_skills/_lazy_load/_core_standards.md``)
is implemented once, in ``src/sh/claude/skill_authoring_gate_lint.py``. The
pre-commit hook only runs it when skill files are staged, so this suite runs
the same checks on every pytest run, and proves each check really fires
using deliberately broken fixture skills.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from _shared_paths import SKILLS_DIR

# The linter lives beside the config in the playbook repo (src/sh/claude/), so
# resolve it from this file's location. A live config install has no src/sh/,
# so the whole module skips there rather than failing.
LINTER_PATH = Path(__file__).resolve().parents[3] / "sh" / "claude" / "skill_authoring_gate_lint.py"
if not LINTER_PATH.exists():
    pytest.skip(f"skill authoring gate linter not found at {LINTER_PATH}", allow_module_level=True)

_spec = importlib.util.spec_from_file_location("skill_authoring_gate_lint", LINTER_PATH)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

VALID_CONTRACT = """\
name: demo_skill
version: 1.0.0
summary: Demonstrates a skill that passes every crawl check
maturity: tactical
test_coverage_level: basic
when:
  - user wants a demo
requires:
  tools: []
  mcp_servers: []
  external: []
"""

VALID_SKILL_MD = """\
---
name: demo_skill
description: Demonstrates a skill that passes every crawl check
maturity: tactical
---
<!-- version: 1.0.0 -->
<!-- created: 2026-09-30 -->
<!-- updated: 2026-09-30 -->
# Demo skill

## 🎯 Purpose

Shows the canonical structure.

## 💡 Example Usage

A user asks for a demo.

## ✨ Best For

Tests only.

## 📚 References

- reference/_implementation.md
"""


def get_all_skills() -> list[Path]:
    """Collect all installed skills from the configured Claude directory's skills/.

    :return: Sorted skill directories, excluding templates, ``_tests`` and dot-prefixed folders.
    :rtype: list[Path]
    """
    if not SKILLS_DIR.exists():
        return []

    skills = []
    for item in SKILLS_DIR.rglob("SKILL.md"):
        skill_path = item.parent
        # Skip templates, test directories, and dot-prefixed dirs (e.g. .trash/ —
        # Claude Code's own auto-managed sync/cleanup artifacts, not authored skills).
        # Match only below SKILLS_DIR: a checkout path such as ~/git/repo_template/
        # must not hide every skill.
        relative_parts = skill_path.relative_to(SKILLS_DIR).parts
        relative_path = "/".join(relative_parts).lower()
        if (
            "template" not in relative_path
            and "_tests" not in relative_path
            and not any(part.startswith(".") for part in relative_parts)
        ):
            skills.append(skill_path)

    return sorted(skills)


def make_fixture_skill(
    root: Path,
    contract: str | None = VALID_CONTRACT,
    skill_md: str | None = VALID_SKILL_MD,
) -> Path:
    """Write a fixture skill, leaving out any file passed as None.

    :param root: Directory to create the skill in.
    :type root: Path
    :param contract: skill.contract.yaml text, or None to omit the file.
    :type contract: str | None
    :param skill_md: SKILL.md text, or None to omit the file.
    :type skill_md: str | None
    :return: The fixture skill's directory.
    :rtype: Path
    """
    skill_dir = root / "demo_skill"
    skill_dir.mkdir(parents=True)
    if contract is not None:
        (skill_dir / "skill.contract.yaml").write_text(contract)
    if skill_md is not None:
        (skill_dir / "SKILL.md").write_text(skill_md)
    return skill_dir


def failures_for(skill_dir: Path) -> list[str]:
    """Return the gate's crawl failures for one skill.

    :param skill_dir: The skill directory to validate.
    :type skill_dir: Path
    :return: Failure messages, empty when the skill passes.
    :rtype: list[str]
    """
    failures, _ = gate.validate_skill(skill_dir)
    return failures


def _make_discovery_skill(skills_dir: Path, relative: str):
    """Create a minimal SKILL.md at skills_dir/relative for discovery tests.

    :param skills_dir: The fake skills/ directory.
    :type skills_dir: Path
    :param relative: Skill folder path below skills_dir.
    :type relative: str
    """
    skill_dir = skills_dir / relative
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: demo\n---\n")


# ── Real skills ──────────────────────────────────────────────────────────────


def test_skills_are_discovered():
    """The suite must find real skills, or every per-skill check passes vacuously."""
    assert get_all_skills(), f"No skills found under {SKILLS_DIR}"


@pytest.mark.parametrize("skill_dir", get_all_skills(), ids=lambda p: p.name)
def test_skill_passes_crawl_gate(skill_dir):
    """Every installed skill meets the crawl criteria of the current skill standard."""
    failures = failures_for(skill_dir)
    assert not failures, f"{skill_dir.name} fails the skill authoring gate: {failures}"


# ── The gate catches each kind of breakage ───────────────────────────────────


def test_valid_fixture_passes(tmp_path):
    """Baseline: the fixture used below passes, so each negative test isolates one break."""
    assert failures_for(make_fixture_skill(tmp_path)) == []


def test_missing_contract_is_caught(tmp_path):
    """A skill without skill.contract.yaml fails C1."""
    failures = failures_for(make_fixture_skill(tmp_path, contract=None))
    assert failures == ["C1: skill.contract.yaml missing"]


def test_missing_contract_field_is_caught(tmp_path):
    """A contract without a core field fails C1 and names the field."""
    contract = VALID_CONTRACT.replace("summary: Demonstrates a skill that passes every crawl check\n", "")
    failures = failures_for(make_fixture_skill(tmp_path, contract=contract))
    assert any("C1" in f and "summary" in f for f in failures), failures


def test_missing_trigger_block_is_caught(tmp_path):
    """A contract with neither trigger nor dependency fields fails C1."""
    contract = VALID_CONTRACT.split("when:")[0]
    failures = failures_for(make_fixture_skill(tmp_path, contract=contract))
    assert any("trigger/dependency" in f for f in failures), failures


def test_non_semantic_version_is_caught(tmp_path):
    """A version that isn't X.Y.Z fails C3."""
    contract = VALID_CONTRACT.replace("version: 1.0.0", "version: '1.0'")
    failures = failures_for(make_fixture_skill(tmp_path, contract=contract))
    assert any("C3" in f and "not semantic" in f for f in failures), failures


def test_version_maturity_mismatch_is_caught(tmp_path):
    """A tactical skill on a 0.x version fails C3."""
    contract = VALID_CONTRACT.replace("version: 1.0.0", "version: 0.3.0")
    failures = failures_for(make_fixture_skill(tmp_path, contract=contract))
    assert any("C3" in f and "maturity" in f for f in failures), failures


def test_hardcoded_path_is_caught(tmp_path):
    """A contract naming a /Users/ path fails C6."""
    contract = VALID_CONTRACT.replace("external: []", "external: ['/Users/someone/tool']")
    failures = failures_for(make_fixture_skill(tmp_path, contract=contract))
    assert any("C6" in f for f in failures), failures


def test_missing_skill_md_is_caught(tmp_path):
    """A skill without SKILL.md fails C4."""
    failures = failures_for(make_fixture_skill(tmp_path, skill_md=None))
    assert "C4: SKILL.md missing" in failures


@pytest.mark.parametrize(
    "heading, section",
    [
        ("## 🎯 Purpose", "Purpose"),
        ("## 💡 Example Usage", "Example Usage"),
        ("## ✨ Best For", "Best For"),
    ],
)
def test_missing_section_is_caught(tmp_path, heading, section):
    """Dropping any canonical SKILL.md section fails C4 and names it."""
    skill_md = VALID_SKILL_MD.replace(heading, "## Other")
    failures = failures_for(make_fixture_skill(tmp_path, skill_md=skill_md))
    assert f"C4: missing {section} section" in failures, failures


def test_missing_frontmatter_is_caught(tmp_path):
    """A SKILL.md that doesn't open with YAML frontmatter fails C5."""
    skill_md = VALID_SKILL_MD.split("---\n", 2)[2]
    failures = failures_for(make_fixture_skill(tmp_path, skill_md=skill_md))
    assert any("C5" in f and "frontmatter" in f for f in failures), failures


def test_version_in_frontmatter_is_caught(tmp_path):
    """A SKILL.md carrying version in its frontmatter fails C5."""
    skill_md = VALID_SKILL_MD.replace("maturity: tactical\n---", "maturity: tactical\nversion: 1.0.0\n---")
    failures = failures_for(make_fixture_skill(tmp_path, skill_md=skill_md))
    assert any("C5" in f and "must not carry version" in f for f in failures), failures


# ── Skill discovery ──────────────────────────────────────────────────────────


def test_skill_discovery_ignores_words_above_skills_dir(tmp_path, monkeypatch):
    """Skills are still found when the checkout path contains 'template' or '_tests'."""
    skills_dir = tmp_path / "repo_skill_template" / "git_pr_tests" / "skills"
    _make_discovery_skill(skills_dir, "_git_skills/git_create_pr")
    monkeypatch.setattr(sys.modules[__name__], "SKILLS_DIR", skills_dir)

    found = [path.name for path in get_all_skills()]

    assert found == ["git_create_pr"], (
        f"Words in the path above skills/ hid real skills — found {found}"
    )


def test_skill_discovery_still_skips_templates_tests_and_dot_dirs(tmp_path, monkeypatch):
    """Template, _tests and dot-prefixed folders below skills/ are still skipped."""
    skills_dir = tmp_path / "skills"
    _make_discovery_skill(skills_dir, "_git_skills/git_create_pr")
    _make_discovery_skill(skills_dir, "_templates/skill_template")
    _make_discovery_skill(skills_dir, "_git_skills/_tests/fixture_skill")
    _make_discovery_skill(skills_dir, ".trash/old_skill")
    monkeypatch.setattr(sys.modules[__name__], "SKILLS_DIR", skills_dir)

    found = [path.name for path in get_all_skills()]

    assert found == ["git_create_pr"], (
        f"Template, _tests or dot-prefixed folders were not skipped — found {found}"
    )
