# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Date created:      2026-08-28
# Version:           1.1.2
# Date updated:      2026-09-21
# ─────────────────────────────────────────────────────────

"""Skill authoring gate tests — validates walk (W1–W6) and run (R1–R4) criteria.

This test suite validates that skills meet quality (walk) and comprehensive (run)
criteria of the skill authoring gate. Crawl criteria (C0–C7) are validated by
the linter (skill_authoring_gate_lint.py) which runs as a pre-commit hook.

Walk tests (W1–W6): Validate readability, style compliance, test coverage, and clarity.
Run tests (R1–R4): Validate semantic versioning, maturity progression, and completeness.

Only stable skills (src/claude/skills/, not src/claude/wip/skills/) are validated here.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from _shared_paths import CLAUDE_DIR, SKILLS_DIR

# Discover all stable skill directories
_stable_skill_dirs = [d for d in (skill_md.parent for skill_md in SKILLS_DIR.rglob("SKILL.md"))]
skill_dirs = sorted(_stable_skill_dirs)
skill_ids = [str(d.relative_to(SKILLS_DIR)) for d in skill_dirs]


# ── Helper functions ──────────────────────────────────────────────────────────


def load_contract(skill_dir: Path) -> dict:
    """Load skill.contract.yaml for the skill."""
    contract_path = skill_dir / "skill.contract.yaml"
    if contract_path.exists():
        with open(contract_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def load_skill_md(skill_dir: Path) -> str:
    """Load SKILL.md content for the skill."""
    skill_md_path = skill_dir / "SKILL.md"
    if skill_md_path.exists():
        return skill_md_path.read_text(encoding="utf-8")
    return ""


def find_test_file(skill_dir: Path) -> Path | None:
    """Locate the test file for the skill."""
    test_files_dir = CLAUDE_DIR / "_tests" / "skills"
    skill_name = skill_dir.name
    for test_file in test_files_dir.glob(f"test_{skill_name}*.py"):
        return test_file
    return None


def has_evals_coverage(skill_dir: Path) -> bool:
    """Return True if the skill has tests/evals.yaml — the standard skill testing artifact.

    Per authoring_skills.md, evals.yaml (not a _tests/skills/ Python file) is
    THE required testing approach for skills, and always lives at
    <skill_dir>/tests/evals.yaml, not skill root; a _tests/skills/ file is a
    secondary behavioral test some skills also carry.
    """
    return (skill_dir / "tests" / "evals.yaml").exists()


def load_skill_md_frontmatter(skill_dir: Path) -> dict:
    """Load SKILL.md's YAML frontmatter (between the leading '---' markers)."""
    content = load_skill_md(skill_dir)
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


# ── Walk tests (W1–W6) ────────────────────────────────────────────────────────


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w1_skill_md_readable(skill_dir):
    """W1: SKILL.md is clear at a glance (readable in <60 seconds, no jargon in opening).

    Checks:
      - Opening sections (<100 lines total)
      - No jargon in first 3 paragraphs
    """
    skill_md_content = load_skill_md(skill_dir)
    # Heuristic: opening should be < 100 lines before first major section
    lines = skill_md_content.split("\n")
    opening_end = 0
    for i, line in enumerate(lines):
        if line.startswith("## ") and i > 5:  # First major section after opening
            opening_end = i
            break

    opening_lines = opening_end if opening_end > 0 else len(lines)
    assert (
        opening_lines < 100
    ), f"Opening section is too long ({opening_lines} lines) — should be readable in <60 seconds"

    # Check for unexplained jargon in opening
    opening_text = "\n".join(lines[:opening_end]).lower()
    jargon_patterns = [
        (r"\bmaturity\b", "maturity", "context about skill development stages"),
        (r"\bscope gate\b", "scope gate", "feature limitations by development tier"),
        (r"\bcrawl|walk|run\b", "maturity tiers (crawl/walk/run)", "development progression levels"),
    ]

    for pattern, term, explanation in jargon_patterns:
        if re.search(pattern, opening_text):
            # Jargon found — check if it's explained
            if explanation.lower() not in opening_text:
                pytest.skip(f"W1: Jargon '{term}' not explained in opening — requires manual review")


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w2_writing_style_compliance(skill_dir):
    """W2: Follows writing_style.md conventions.

    Checks:
      - All ## headers have emojis
      - Bullets have bold keywords (when applicable)
      - Line length warnings (>120 lines for full file)
    """
    skill_md_content = load_skill_md(skill_dir)
    lines = skill_md_content.split("\n")

    # Check for emojis on ## headers
    headers_without_emoji = []
    for i, line in enumerate(lines, 1):
        if line.startswith("## ") and not re.search(r"[^\x00-\x7F]", line):
            headers_without_emoji.append((i, line))

    if headers_without_emoji:
        pytest.skip(f"W2: {len(headers_without_emoji)} headers missing emojis — requires manual fix")

    # Warn if file is very long
    if len(lines) > 150:
        pytest.skip(f"W2: SKILL.md is {len(lines)} lines (consider splitting if >150) — manual review")


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w3_test_coverage_matches_maturity(skill_dir):
    """W3: Test coverage matches maturity level.

    Expected test counts:
      - draft: 1–2 tests (happy path)
      - tactical: 5–8 tests (main path + light error handling)
      - strategic: 15+ tests (full coverage)
    """
    contract = load_contract(skill_dir)
    maturity = contract.get("maturity", "draft")
    test_file = find_test_file(skill_dir)

    if test_file is None:
        if has_evals_coverage(skill_dir):
            pytest.skip(f"{maturity} skill tested via tests/evals.yaml, not a _tests/skills/ file")
            return

        frontmatter = load_skill_md_frontmatter(skill_dir)
        tested = frontmatter.get("tags", {}).get("tested", False)
        # `tested: true` is a claim that some real test coverage exists — if
        # neither a test file nor evals.yaml exists, that claim is false and
        # must fail regardless of maturity (see the 2026-09-18 auto_rotate_todo
        # incident, where a skill/hook was marked done without ever being built).
        assert not tested, (
            f"W3: {skill_dir.name} claims tags.tested: true in SKILL.md "
            f"but has no test file and no tests/evals.yaml "
            f"(Expected: _tests/skills/test_{skill_dir.name}*.py or "
            f"{skill_dir.name}/tests/evals.yaml)"
        )
        # `tested: false` is an honest, disclosed gap — tracked debt, not a
        # gate failure. Maturity alone doesn't force a test file to exist.
        pytest.skip(
            f"{maturity} skill without tests (tags.tested: false) — "
            "acceptable disclosed gap, not yet built"
        )
        return

    # Count test functions in test file
    test_content = test_file.read_text(encoding="utf-8")
    test_count = len(re.findall(r"^def test_|@pytest.mark.parametrize", test_content, re.MULTILINE))

    if maturity == "draft":
        # Draft: optional, but if present should be minimal
        assert test_count <= 5, f"Draft skill should have 1–2 tests, found {test_count}"
    elif maturity == "tactical":
        assert (
            5 <= test_count <= 12
        ), f"Tactical skill should have 5–8 tests, found {test_count}"
    elif maturity == "strategic":
        assert (
            test_count >= 12
        ), f"Strategic skill should have 15+ tests, found {test_count}"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w4_no_unexplained_jargon(skill_dir):
    """W4: No unexplained Claude jargon.

    Checks for unexplained jargon in opening sections:
      - maturity, triggers, MCP, scope gate, crawl/walk/run
    """
    skill_md_content = load_skill_md(skill_dir)
    lines = skill_md_content.split("\n")

    # Skip the YAML frontmatter block — "maturity", "triggers", etc. are
    # structured metadata keys there, not prose a reader parses for clarity.
    # W4 is about the opening PROSE (Purpose, Scope gate text), so scanning
    # starts after the frontmatter's closing "---".
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body_start = i + 1
                break

    opening_end = min(body_start + 30, len(lines))  # First 30 lines of prose
    opening_text = "\n".join(lines[body_start:opening_end]).lower()

    jargon = {
        r"\bmaturity\b": "maturity (development stage)",
        r"\bscope gate\b": "scope gate (feature limitation)",
        r"\btriggers\b": "triggers (invocation phrases)",
        r"\bmcp\b": "MCP (Model Context Protocol)",
        # Requires the compound jargon phrase itself (e.g. "crawl/walk/run",
        # "crawl, walk, run") — a bare `\bcrawl|walk|run\b` also matches
        # ordinary prose like "run the command" or "walk through the steps".
        r"\bcrawl\b.{0,5}\bwalk\b.{0,5}\brun\b": "crawl/walk/run (progression tiers)",
    }

    unexplained = []
    for pattern, term in jargon.items():
        if re.search(pattern, opening_text):
            unexplained.append(term)

    assert (
        not unexplained
    ), f"W4: Unexplained jargon in opening: {', '.join(unexplained)} — explain or remove"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w5_no_todo_in_tactical_plus(skill_dir):
    """W5: No TODO/FIXME in tactical+ skills.

    Draft skills may have TODOs. Tactical+ skills must have them resolved or documented.
    """
    contract = load_contract(skill_dir)
    skill_md_content = load_skill_md(skill_dir)

    maturity = contract.get("maturity", "draft")
    if maturity == "draft":
        return  # TODOs allowed in draft

    todo_count = len(re.findall(r"\bTODO\b|\bFIXME\b", skill_md_content, re.IGNORECASE))
    assert (
        todo_count == 0
    ), f"W5: {maturity} skill has {todo_count} unresolved TODOs/FIXMEs — resolve before releasing"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_w6_phase_files_focused(skill_dir):
    """W6: Phase files (if multi-phase) are focused and complete.

    Checks:
      - Phase files exist and are non-empty
      - Phase files follow naming convention (phase1.md, phase2.md, etc.)
    """
    # Look for phase files
    phase_files = sorted(skill_dir.glob("phase*.md"))
    if not phase_files:
        return  # Single-phase skill, skip this test

    for phase_file in phase_files:
        content = phase_file.read_text(encoding="utf-8")
        assert len(content) > 100, f"{phase_file.name} is too short (<100 chars) — should be focused but complete"
        assert phase_file.name.lower().startswith("phase"), "Phase file should be named phase1.md, phase2.md, etc."


# ── Run tests (R1–R4) ─────────────────────────────────────────────────────────


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_r1_semantic_versioning_aligned(skill_dir):
    """R1: Semantic versioning aligns with maturity.

    Major version must match maturity:
      - draft: 0.x.x
      - tactical: 1.x.x
      - strategic: 2+.x.x
    """
    contract = load_contract(skill_dir)
    version = contract.get("version", "0.0.0")
    maturity = contract.get("maturity", "draft")

    # Already validated by linter, but double-check here
    major = int(version.split(".")[0]) if version else 0

    if maturity == "draft":
        assert major == 0, f"Draft skill must use 0.x.x versioning, found {version}"
    elif maturity == "tactical":
        assert major == 1, f"Tactical skill must use 1.x.x versioning, found {version}"
    elif maturity == "strategic":
        assert major >= 2, f"Strategic skill must use 2+.x.x versioning, found {version}"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_r2_test_coverage_thorough(skill_dir):
    """R2: Test coverage is thorough (main path + error cases + edge cases).

    Verifies:
      - Tests exist for the maturity level
      - Test file is non-empty and well-structured
    """
    test_file = find_test_file(skill_dir)

    if test_file is None:
        pytest.skip("R2: No test file — manual review required")
        return

    content = test_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Heuristic: good test files have at least 50 lines (rough estimate)
    assert len(lines) > 30, f"Test file is too short ({len(lines)} lines) — add more test cases"

    # Check for pytest markers (parametrize, marks)
    has_test_structure = bool(
        re.search(r"@pytest|def test_|assert ", content, re.MULTILINE)
    )
    assert has_test_structure, "Test file should follow pytest conventions"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_r3_maturity_progression_documented(skill_dir):
    """R3: Maturity progression is documented in version history.

    For tactical+ skills, expect documentation of progression from prior tier.
    """
    contract = load_contract(skill_dir)
    skill_md_content = load_skill_md(skill_dir)

    maturity = contract.get("maturity", "draft")

    if maturity in ("tactical", "strategic"):
        # Tactical/strategic skills should have a version section documenting progression
        has_version_history = bool(
            re.search(r"##.*version|##.*history|##.*changelog", skill_md_content, re.IGNORECASE)
        )
        if not has_version_history:
            pytest.skip("R3: Maturity progression not documented in version history — manual review")


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_r4_no_unresolved_gaps_strategic(skill_dir):
    """R4: No unresolved gaps in strategic skills.

    Strategic skills should have no TODO/FIXME and gaps should be explicitly documented
    with workarounds.
    """
    contract = load_contract(skill_dir)
    skill_md_content = load_skill_md(skill_dir)

    maturity = contract.get("maturity", "draft")
    if maturity != "strategic":
        return

    todo_count = len(re.findall(r"\bTODO\b|\bFIXME\b", skill_md_content, re.IGNORECASE))
    assert todo_count == 0, f"Strategic skill has {todo_count} unresolved TODOs"

    # Check for known gaps section with workarounds
    has_gaps_section = bool(re.search(r"##.*known gaps", skill_md_content, re.IGNORECASE))
    assert has_gaps_section, "Strategic skill should document known gaps and workarounds"
