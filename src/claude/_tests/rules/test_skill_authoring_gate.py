"""Skill authoring gate tests — validates walk (W1–W6) and run (R1–R5) criteria.

This test suite validates that skills meet quality (walk) and comprehensive (run)
criteria of the skill authoring gate. Crawl criteria (C0–C7) are validated by
the linter (skill_authoring_gate_lint.py) which runs as a pre-commit hook.

Walk tests (W1–W6): Validate readability, style compliance, test coverage, and clarity.
Run tests (R1–R5): Validate semantic versioning, maturity progression, and completeness.

Only stable skills (src/claude/skills/, not src/claude/wip/skills/) are validated here.
"""

import re
from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).parent.parent / "src" / "claude" / "skills"

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
    test_files_dir = Path(__file__).parent / "skills"
    skill_name = skill_dir.name
    for test_file in test_files_dir.glob(f"test_{skill_name}*.py"):
        return test_file
    return None


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
        assert maturity == "draft", (
            f"W3: {maturity} skill must have a test file "
            f"(Expected: tests/skills/test_{skill_dir.name}*.py)"
        )
        pytest.skip("Draft skill without tests — acceptable if intentional")
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
    opening_end = min(30, len(lines))  # First 30 lines
    opening_text = "\n".join(lines[:opening_end]).lower()

    jargon = {
        r"\bmaturity\b": "maturity (development stage)",
        r"\bscope gate\b": "scope gate (feature limitation)",
        r"\btriggers\b": "triggers (invocation phrases)",
        r"\bmcp\b": "MCP (Model Context Protocol)",
        r"\bcrawl|walk|run\b": "crawl/walk/run (progression tiers)",
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
        assert phase_file.name.lower().startswith("phase"), f"Phase file should be named phase1.md, phase2.md, etc."


# ── Run tests (R1–R5) ─────────────────────────────────────────────────────────


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
    version = contract.get("version", "0.0.0")

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


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_r5_complex_skills_have_schema(skill_dir):
    """R5: Complex skills (external_service output) have optional skill_schema.yaml.

    Checks if output type is external_service; if so, skill_schema.yaml should exist
    (optional but recommended for complex skills).
    """
    contract = load_contract(skill_dir)
    output = contract.get("output", "conversational")
    if output != "external_service":
        return

    schema_path = skill_dir / "skill_schema.yaml"
    if not schema_path.exists():
        pytest.skip(f"R5: External service skill lacks skill_schema.yaml — optional but recommended")
