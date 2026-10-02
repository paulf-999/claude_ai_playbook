"""Builds fake skills for the skill authoring gate's walk and run tests.

The gate linter lives beside the config in the playbook repo (``src/sh/claude/``), so it
is loaded from this file's location. A live config install has no ``src/sh/``, so tests
that import this module skip there rather than fail.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from _shared_paths import CLAUDE_DIR

LINTER_PATH = CLAUDE_DIR / "_scripts" / "_lint_scripts" / "lint_skill_authoring_gate.py"
if not LINTER_PATH.exists():
    pytest.skip(f"skill authoring gate linter not found at {LINTER_PATH}", allow_module_level=True)

_spec = importlib.util.spec_from_file_location("lint_skill_authoring_gate", LINTER_PATH)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

VERSION_FOR = {"draft": "0.1.0", "tactical": "1.0.0", "strategic": "2.0.0"}
# An evals.yaml scenario count inside each maturity's W3 range
EVALS_FOR = {"draft": 6, "tactical": 9, "strategic": 12}
SECTIONS = """\
## 🎯 Purpose

Shows the canonical structure.

## 💡 Example Usage

A user asks for a demo.

## ✨ Best For

Tests only.

## 📚 References

- reference/_implementation.md
"""


def make_skill(
    root: Path,
    maturity: str = "draft",
    opening: str = "Builds a demo for tests.",
    extra: str = "",
    tested: bool | None = None,
    evals: bool = True,
    eval_count: int | None = None,
) -> Path:
    """Write a fake skill that passes every crawl check.

    :param root: Directory to create the skill in.
    :type root: Path
    :param maturity: ``draft``, ``tactical`` or ``strategic``.
    :type maturity: str
    :param opening: Prose straight after the H1.
    :type opening: str
    :param extra: Markdown appended after the standard sections.
    :type extra: str
    :param tested: Value for ``tags.tested`` in the frontmatter, or None to leave tags out.
    :type tested: bool | None
    :param evals: Whether to write ``tests/evals.yaml``.
    :type evals: bool
    :param eval_count: Scenarios to write, or None for a count inside the maturity's range.
    :type eval_count: int | None
    :return: The fake skill's directory.
    :rtype: Path
    """
    skill_dir = root / "demo_skill"
    skill_dir.mkdir(parents=True)
    version = VERSION_FOR[maturity]
    (skill_dir / "skill.contract.yaml").write_text(
        f"name: demo_skill\nversion: {version}\nsummary: Builds a demo\nmaturity: {maturity}\n"
        "test_coverage_level: basic\nwhen:\n  - user wants a demo\n"
        "requires:\n  tools: [x]\n  mcp_servers: [x]\n  external: [x]\n"
    )
    tags = f"tags:\n  tested: {str(tested).lower()}\n" if tested is not None else ""
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: demo_skill\ndescription: Builds a demo\nmaturity: {maturity}\n{tags}---\n"
        f"<!-- version: {version} -->\n<!-- created: 2026-10-01 -->\n<!-- updated: 2026-10-01 -->\n"
        f"# 🧪 Demo skill\n\n{opening}\n\n{SECTIONS}{extra}"
    )
    if evals:
        (skill_dir / "tests").mkdir()
        count = EVALS_FOR[maturity] if eval_count is None else eval_count
        scenarios = "".join(f"  - name: case_{i}\n" for i in range(count))
        (skill_dir / "tests" / "evals.yaml").write_text(f"evals:\n{scenarios}" if count else "evals: []\n")
    return skill_dir


def walk_run(skill_dir: Path, tests_dir: Path) -> tuple[list[str], list[str]]:
    """Run only the walk and run checks on a fake skill.

    :param skill_dir: The fake skill.
    :type skill_dir: Path
    :param tests_dir: Folder to look in for ``test_<skill>*.py`` files.
    :type tests_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    contract = gate.yaml.safe_load((skill_dir / "skill.contract.yaml").read_text())
    return gate.check_walk_run(skill_dir, contract, tests_dir)


def codes(messages: list[str]) -> list[str]:
    """Return the criterion code (e.g. ``W3``) of each message.

    :param messages: Gate messages such as ``"W3: ..."``.
    :type messages: list[str]
    :return: The codes, in order.
    :rtype: list[str]
    """
    return [m.split(":", 1)[0] for m in messages]
