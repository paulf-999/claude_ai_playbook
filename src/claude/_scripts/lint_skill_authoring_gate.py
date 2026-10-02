#!/usr/bin/env python3
"""Skill authoring gate linter — validates crawl (C0–C7), walk (W1–W6) and run (R2–R4) criteria.

Validates skill.contract.yaml and SKILL.md against the skill authoring gate.
Crawl checks basic structure and contract; walk checks readability, style,
test coverage and focus; run checks test depth, maturity history and gaps.
Walk and run checks that fail a skill outright are reported as FAIL; those
that need a human to judge are reported as WARN and never block. R1 (version
matches maturity) is the same check as C3, so it is reported once, as C3.

Usage:
    python3 src/claude/_scripts/lint_skill_authoring_gate.py          # scan src/claude/skills/ (default)
    python3 src/claude/_scripts/lint_skill_authoring_gate.py <root>   # scan an explicit root dir
    make lint_skills                                             # via Makefile target

Exit codes:
    0 — all skills pass
    1 — one or more skills have violations
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# ── script location ───────────────────────────────────────────────────────────

# Script lives in <config>/_scripts/, so the config root is one level up.
_CONFIG_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = _CONFIG_ROOT / "skills"
DEFAULT_TESTS_DIR = _CONFIG_ROOT / "_tests" / "skills"

# W4: Claude jargon a reader may not know, when it appears in a SKILL.md's opening prose
JARGON = {
    r"\bmaturity\b": "maturity (development stage)",
    r"\bscope gate\b": "scope gate (feature limitation)",
    r"\btriggers\b": "triggers (invocation phrases)",
    r"\bmcp\b": "MCP (Model Context Protocol)",
    # The compound phrase only: a bare "run" or "walk" is ordinary prose
    r"\bcrawl\b.{0,5}\bwalk\b.{0,5}\brun\b": "crawl/walk/run (progression tiers)",
}
# W1: jargon that is fine in the opening once it's explained in the same opening
EXPLAINED_JARGON = {
    r"\bmaturity\b": "context about skill development stages",
    r"\bscope gate\b": "feature limitations by development tier",
}
# W3: how many evals.yaml scenarios each maturity expects, per authoring_skills.md's maturity table
EVAL_COUNT_RANGE = {"draft": (5, 8), "tactical": (8, 12), "strategic": (12, None)}


# ── validation logic ──────────────────────────────────────────────────────────


def _check_c1_contract_fields(contract: dict) -> list[str]:
    """C1: skill.contract.yaml has all required core fields and a trigger/dependency block.

    Supports both new format (when, requires) and legacy format (dispatch, dependencies).

    :param contract: Parsed skill.contract.yaml content.
    :type contract: dict
    :return: List of failure messages (empty if the contract is complete).
    :rtype: list[str]
    """
    failures = []
    core_required = ["name", "version", "summary", "maturity", "test_coverage_level"]
    for field in core_required:
        if field not in contract or contract[field] is None:
            failures.append(f"C1: skill.contract.yaml missing required field: {field}")

    has_new_format = any(k in contract for k in ["when", "requires"])
    has_legacy_format = any(k in contract for k in ["dispatch", "dependencies"])
    if not has_new_format and not has_legacy_format:
        failures.append(
            "C1: skill.contract.yaml missing trigger/dependency fields "
            "(when/requires or dispatch/dependencies)"
        )
    return failures


def _check_c3_version_maturity(contract: dict) -> list[str]:
    """C3: version is semantic (X.Y.Z) and its major aligns with maturity.

    :param contract: Parsed skill.contract.yaml content.
    :type contract: dict
    :return: List of failure messages (empty if version/maturity are aligned).
    :rtype: list[str]
    """
    version = contract.get("version", "")
    if not version:
        return []

    if not _is_semantic_version(version):
        return [f"C3: version '{version}' is not semantic (X.Y.Z)"]

    maturity = contract.get("maturity")
    if not maturity:
        return []

    version_major = int(version.split(".")[0])
    if not _check_maturity_version_alignment(version_major, maturity):
        return [
            f"C3: version major {version_major} doesn't match maturity '{maturity}' "
            "(draft=0.x, tactical=1.x, strategic=2+.x)"
        ]
    return []


def _check_c2_and_c4_and_c5_skill_md(skill_dir: Path) -> list[str]:
    """C2/C4/C5: SKILL.md exists, has no hardcoded skill names, has the canonical
    5-section structure, and opens with valid YAML frontmatter.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: List of failure messages.
    :rtype: list[str]
    """
    failures = []
    skill_md_path = skill_dir / "SKILL.md"

    if not skill_md_path.exists():
        return ["C4: SKILL.md missing"]

    try:
        skill_md_content = skill_md_path.read_text(encoding="utf-8")
        name_issues = _check_hardcoded_skill_names(skill_md_content, skill_dir.name)
        failures.extend([f"C2: {issue}" for issue in name_issues])
    except Exception as exc:
        failures.append(f"C2: SKILL.md read error: {exc}")

    try:
        structure_issues = _check_skill_md_structure(skill_md_path)
        failures.extend([f"C4: {issue}" for issue in structure_issues])
    except Exception as exc:
        failures.append(f"C4: SKILL.md structure check failed: {exc}")

    try:
        frontmatter_issues = _has_valid_frontmatter(skill_md_path)
        failures.extend([f"C5: {issue}" for issue in frontmatter_issues])
    except Exception as exc:
        failures.append(f"C5: SKILL.md frontmatter check failed: {exc}")

    return failures


def _check_c7_requires_section(contract: dict) -> list[str]:
    """C7: requires section documents tools/mcp_servers/external (advisory only).

    :param contract: Parsed skill.contract.yaml content.
    :type contract: dict
    :return: List of warning messages.
    :rtype: list[str]
    """
    requires = contract.get("requires", {})
    if not isinstance(requires, dict):
        return ["C7: requires field must be a dict with tools, mcp_servers, external keys"]

    warnings = []
    for key in ["tools", "mcp_servers", "external"]:
        if key not in requires:
            warnings.append(f"C7: requires.{key} is empty or missing")
    return warnings


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    """Validate a skill against crawl criteria (C0–C7).

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    # C0: Skill directory exists (implicit in discovery)
    contract_path = skill_dir / "skill.contract.yaml"

    # C1: skill.contract.yaml exists and parses
    if not contract_path.exists():
        return ["C1: skill.contract.yaml missing"], []

    try:
        with open(contract_path, encoding="utf-8") as f:
            contract = yaml.safe_load(f) or {}
    except Exception as exc:
        return [f"C1: skill.contract.yaml parse error: {exc}"], []

    failures: list[str] = []
    failures.extend(_check_c1_contract_fields(contract))
    failures.extend(_check_c3_version_maturity(contract))

    # C6: No hardcoded paths or personal references
    failures.extend(f"C6: {issue}" for issue in _check_hardcoded_paths(yaml.dump(contract)))

    failures.extend(_check_c2_and_c4_and_c5_skill_md(skill_dir))

    warnings = _check_c7_requires_section(contract)

    walk_run_failures, walk_run_warnings = check_walk_run(skill_dir, contract)
    failures.extend(walk_run_failures)
    warnings.extend(walk_run_warnings)

    return failures, warnings


def _skill_md_parts(skill_dir: Path) -> tuple[str, dict, list[str]]:
    """Split a skill's SKILL.md into its text, frontmatter and prose lines.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: The full text, the parsed frontmatter (empty if none) and the lines after it.
    :rtype: tuple[str, dict, list[str]]
    """
    path = skill_dir / "SKILL.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
        if end is not None:
            try:
                frontmatter = yaml.safe_load("\n".join(lines[1:end])) or {}
            except yaml.YAMLError:
                frontmatter = {}
            return text, frontmatter if isinstance(frontmatter, dict) else {}, lines[end + 1:]
    return text, {}, lines


def find_test_files(skill_dir: Path, tests_dir: Path = DEFAULT_TESTS_DIR) -> list[Path]:
    """Locate a skill's pytest files: ``test_<skill>*.py`` anywhere, plus every test in ``<tests_dir>/<skill>/``.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param tests_dir: Folder holding the skills' pytest files.
    :type tests_dir: Path
    :return: The matching test files, sorted.
    :rtype: list[Path]
    """
    if not tests_dir.exists():
        return []
    named = set(tests_dir.rglob(f"test_{skill_dir.name}*.py"))
    own_folder = tests_dir / skill_dir.name
    in_folder = set(own_folder.rglob("test_*.py")) if own_folder.is_dir() else set()
    return sorted(named | in_folder)


def count_evals(skill_dir: Path) -> int | None:
    """Count the scenarios in a skill's tests/evals.yaml.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: The number of entries in the top-level ``evals`` list, or None if the file is missing.
    :rtype: int | None
    :raises ValueError: If the file exists but has no ``evals`` list.
    """
    path = skill_dir / "tests" / "evals.yaml"
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    evals = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(evals, list):
        raise ValueError("tests/evals.yaml has no top-level 'evals' list")
    return len(evals)


def _check_w1_w2_readability(lines: list[str], prose: list[str]) -> tuple[list[str], list[str]]:
    """W1–W2: the opening reads in a minute, and headings and length follow writing_style.md.

    :param lines: SKILL.md lines.
    :type lines: list[str]
    :param prose: SKILL.md lines after the frontmatter, where W1 looks for jargon.
    :type prose: list[str]
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    failures: list[str] = []
    warnings: list[str] = []
    opening_end = next((i for i, line in enumerate(lines) if line.startswith("## ") and i > 5), len(lines))
    if opening_end >= 100:
        failures.append(f"W1: opening is {opening_end} lines — keep it under 100 so it reads in a minute")
    # Frontmatter keys such as "maturity:" are metadata, not prose, so skip them as W4 does
    prose_end = next((i for i, line in enumerate(prose) if line.startswith("## ")), len(prose))
    opening = "\n".join(prose[:prose_end]).lower()
    for pattern, explanation in EXPLAINED_JARGON.items():
        if re.search(pattern, opening) and explanation not in opening:
            warnings.append(f"W1: '{pattern.strip(chr(92) + 'b')}' in the opening isn't explained — review it")
    bare = [line for line in lines if line.startswith("## ") and not re.search(r"[^\x00-\x7F]", line)]
    if bare:
        warnings.append(f"W2: {len(bare)} ## heading(s) have no emoji")
    if len(lines) > 150:
        warnings.append(f"W2: SKILL.md is {len(lines)} lines — consider moving detail to reference/")
    return failures, warnings


def _check_w3_coverage(
    skill_dir: Path, frontmatter: dict, maturity: str, tests_dir: Path
) -> tuple[list[str], list[str]]:
    """W3: the evals.yaml scenario count fits the maturity, and a tested: true claim is backed by tests.

    Pytest files are extra coverage on top of evals.yaml, so they never count toward or cap the range.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param frontmatter: SKILL.md's parsed frontmatter.
    :type frontmatter: dict
    :param maturity: The contract's maturity level.
    :type maturity: str
    :param tests_dir: Folder holding the skills' pytest files.
    :type tests_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    try:
        count = count_evals(skill_dir)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"W3: {exc}"], []
    if count is None:
        tags = frontmatter.get("tags") or {}
        if isinstance(tags, dict) and tags.get("tested") is True and not find_test_files(skill_dir, tests_dir):
            return ["W3: SKILL.md claims tags.tested: true, but there's no tests/evals.yaml or pytest file"], []
        return [], ["W3: no tests/evals.yaml yet — every skill needs one"]
    low, high = EVAL_COUNT_RANGE.get(maturity, (0, None))
    expected = f"{low}+" if high is None else f"{low}–{high}"
    if count < low:
        return [f"W3: {maturity} skill has {count} evals, expected {expected} — add scenarios"], []
    if high is not None and count > high:
        return [], [f"W3: {maturity} skill has {count} evals, above {expected} — it may be ready to promote"]
    return [], []


def _check_w4_to_w6_focus(skill_dir: Path, text: str, prose: list[str], maturity: str) -> list[str]:
    """W4–W6: no unexplained jargon, no open TODOs once tactical, and complete phase files.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param text: Full SKILL.md text.
    :type text: str
    :param prose: SKILL.md lines after the frontmatter.
    :type prose: list[str]
    :param maturity: The contract's maturity level.
    :type maturity: str
    :return: Failures.
    :rtype: list[str]
    """
    failures: list[str] = []
    opening_prose = "\n".join(prose[:30]).lower()
    unexplained = [term for pattern, term in JARGON.items() if re.search(pattern, opening_prose)]
    if unexplained:
        failures.append(f"W4: unexplained jargon in the opening: {', '.join(unexplained)} — explain or remove it")
    if maturity in ("tactical", "strategic"):
        todos = len(re.findall(r"\bTODO\b|\bFIXME\b", text, re.IGNORECASE))
        if todos:
            failures.append(f"W5: {maturity} skill has {todos} open TODO/FIXME — resolve them before release")
    for phase_file in sorted(skill_dir.glob("phase*.md")):
        if len(phase_file.read_text(encoding="utf-8")) <= 100:
            failures.append(f"W6: {phase_file.name} is under 100 characters — make it complete")
    return failures


def _check_walk(skill_dir: Path, maturity: str, tests_dir: Path) -> tuple[list[str], list[str]]:
    """W1–W6: readability, style, test coverage, jargon, open TODOs and phase files.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param maturity: The contract's maturity level.
    :type maturity: str
    :param tests_dir: Folder holding the skills' pytest files.
    :type tests_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    text, frontmatter, prose = _skill_md_parts(skill_dir)
    readability_failures, readability_warnings = _check_w1_w2_readability(text.split("\n"), prose)
    coverage_failures, coverage_warnings = _check_w3_coverage(skill_dir, frontmatter, maturity, tests_dir)
    focus_failures = _check_w4_to_w6_focus(skill_dir, text, prose, maturity)
    return readability_failures + coverage_failures + focus_failures, readability_warnings + coverage_warnings


def _check_run(skill_dir: Path, maturity: str, tests_dir: Path) -> tuple[list[str], list[str]]:
    """R2–R4: test depth, maturity history and documented gaps.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param maturity: The contract's maturity level.
    :type maturity: str
    :param tests_dir: Folder holding the skills' pytest files.
    :type tests_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    failures: list[str] = []
    warnings: list[str] = []
    text, _, _ = _skill_md_parts(skill_dir)

    # R2: every pytest file a skill has shows real depth
    for test_file in find_test_files(skill_dir, tests_dir):
        content = test_file.read_text(encoding="utf-8")
        if len(content.split("\n")) <= 30:
            failures.append(f"R2: {test_file.name} is 30 lines or fewer — add error and edge cases")
        if not re.search(r"@pytest|def test_|assert ", content):
            failures.append(f"R2: {test_file.name} has no pytest tests")

    # R3: tactical and strategic skills record how they got there
    if maturity in ("tactical", "strategic") and not re.search(r"##.*(?:version|history|changelog)", text, re.I):
        warnings.append("R3: no version history section recording the maturity progression — review it")

    # R4: strategic skills document their known gaps and workarounds
    if maturity == "strategic" and not re.search(r"##.*known gaps", text, re.IGNORECASE):
        failures.append("R4: strategic skill has no 'Known gaps' section with workarounds")
    return failures, warnings


def check_walk_run(
    skill_dir: Path, contract: dict, tests_dir: Path = DEFAULT_TESTS_DIR
) -> tuple[list[str], list[str]]:
    """Validate a skill against the walk (W1–W6) and run (R2–R4) criteria.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :param contract: The parsed skill.contract.yaml.
    :type contract: dict
    :param tests_dir: Folder holding the skills' pytest files.
    :type tests_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    maturity = contract.get("maturity", "draft")
    walk_failures, walk_warnings = _check_walk(skill_dir, maturity, tests_dir)
    run_failures, run_warnings = _check_run(skill_dir, maturity, tests_dir)
    return walk_failures + run_failures, walk_warnings + run_warnings


def _is_semantic_version(version: str) -> bool:
    """Check if version follows semantic versioning (X.Y.Z).

    :param version: Version string to validate.
    :type version: str
    :return: True if version is semantic.
    :rtype: bool
    """
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def _check_maturity_version_alignment(major: int, maturity: str) -> bool:
    """Check if version major aligns with maturity tier.

    :param major: Major version number.
    :type major: int
    :param maturity: Maturity tier (draft, tactical, strategic).
    :type maturity: str
    :return: True if aligned.
    :rtype: bool
    """
    if maturity == "draft":
        return major == 0
    elif maturity == "tactical":
        return major == 1
    elif maturity == "strategic":
        return major >= 2
    return False


def _check_hardcoded_paths(text: str) -> list[str]:
    """Check for hardcoded paths or personal references.

    :param text: Text to check.
    :type text: str
    :return: List of issues found.
    :rtype: list[str]
    """
    issues = []
    hardcoded_patterns = [
        (r"/home/", "hardcoded /home/ path"),
        (r"/Users/", "hardcoded /Users/ path"),
        (r"/root/", "hardcoded /root/ path"),
        (r"/paul/", "personal reference (/paul/)"),
        (r"/home/paul", "personal user path (/home/paul)"),
    ]

    for pattern, description in hardcoded_patterns:
        if re.search(pattern, text):
            issues.append(description)

    return issues


def _check_hardcoded_skill_names(skill_md: str, skill_name: str) -> list[str]:
    """Check for hardcoded skill names (e.g., 'execute <skill-name>').

    :param skill_md: SKILL.md content.
    :type skill_md: str
    :param skill_name: Expected skill name.
    :type skill_name: str
    :return: List of issues found.
    :rtype: list[str]
    """
    issues = []

    # Look for patterns like "execute skill_name" or "requires skill_name"
    hardcoded_patterns = [
        (rf"execute {skill_name}", f"hardcoded skill name: 'execute {skill_name}'"),
        (rf"requires {skill_name}", f"hardcoded skill name: 'requires {skill_name}'"),
    ]

    for pattern, description in hardcoded_patterns:
        if re.search(pattern, skill_md, re.IGNORECASE):
            issues.append(description)

    return issues


def _check_skill_md_structure(skill_md_path: Path) -> list[str]:
    """Check if SKILL.md has the canonical 5-section structure.

    Per authoring_skills.md's Core Standards, every skill is:
      1. Frontmatter — name, maturity, description, tags, then the version header (checked by C5)
      2. Purpose — 1 sentence value prop + 3-4 bullets
      3. Example Usage — realistic end-to-end scenario
      4. Best For — use cases + caveats (an H2 heading, or a "**Best for:**"
         bold lead-in — both are used by current skills)
      5. References — pointers to reference/ files (an H2 heading, a
         "**...see:**" bold lead-in, or a bare reference/_*.md path — all
         three are used by current skills)

    :param skill_md_path: Path to SKILL.md.
    :type skill_md_path: Path
    :return: List of issues found.
    :rtype: list[str]
    """
    issues = []
    content = skill_md_path.read_text(encoding="utf-8")

    required_sections = {
        r"^##.*\bpurpose\b": "Purpose section",
        r"^##.*\bexample usage\b": "Example Usage section",
        r"(^##.*\bbest for\b)|(\*\*best for:?\*\*)": "Best For section",
        r"(^##.*\breferences\b)|(\*\*[^*]*see:?\*\*)|(reference/_)": "References section",
    }

    for pattern, description in required_sections.items():
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            issues.append(f"missing {description}")

    return issues


def _has_valid_frontmatter(skill_md_path: Path) -> list[str]:
    """Check that SKILL.md opens with YAML frontmatter carrying required fields.

    Per authoring_skills.md, frontmatter (not a metadata table or prose) is
    section 1 of the canonical structure, and must declare name, description
    and maturity. Version lives in the three-line metadata header straight
    after the frontmatter (see _claude_config_metadata.md).

    :param skill_md_path: Path to SKILL.md.
    :type skill_md_path: Path
    :return: List of issues found (empty if frontmatter is valid).
    :rtype: list[str]
    """
    issues = []
    content = skill_md_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        issues.append("SKILL.md must start with YAML frontmatter (---) as section 1")
        return issues

    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append("SKILL.md frontmatter block is not closed with a second ---")
        return issues

    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        issues.append(f"SKILL.md frontmatter is not valid YAML: {exc}")
        return issues

    for field in ["name", "description", "maturity"]:
        if field not in data or data[field] is None:
            issues.append(f"SKILL.md frontmatter missing required field: {field}")

    if "version" in data:
        issues.append("SKILL.md frontmatter must not carry version — it belongs in the metadata header")
    if not parts[2].startswith("\n<!-- version:"):
        issues.append("SKILL.md metadata header (<!-- version: X.Y.Z -->) must follow the frontmatter")

    return issues


# ── file discovery ────────────────────────────────────────────────────────────


def find_skills(root: Path) -> list[Path]:
    """Discover skills to validate under root.

    A skill is any directory under root that contains skill.contract.yaml.

    :param root: Root directory to search.
    :type root: Path
    :return: Sorted list of skill directory paths.
    :rtype: list[Path]
    """
    skills = []
    for contract_file in root.rglob("skill.contract.yaml"):
        skill_dir = contract_file.parent
        if skill_dir.parent == root or any(skill_dir.parent.parent == root for _ in [None]):
            skills.append(skill_dir)

    return sorted(skills)


# ── output helpers ────────────────────────────────────────────────────────────


def _rel(path: Path, root: Path) -> str:
    """Return a display-friendly relative path string.

    :param path: Absolute path.
    :type path: Path
    :param root: Root directory for relative calculation.
    :type root: Path
    :return: Relative path string.
    :rtype: str
    """
    try:
        return str(path.relative_to(root.parent))
    except ValueError:
        return str(path)


# ── entry point ───────────────────────────────────────────────────────────────


def main() -> int:
    """Run the skill authoring gate lint scan.

    :return: Exit code — 0 if all skills pass, 1 if any violations found.
    :rtype: int
    """
    parser = argparse.ArgumentParser(
        description="Validate skill authoring gate criteria (crawl level).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help=f"Root skills directory to scan (default: {DEFAULT_ROOT})",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: root directory not found: {root}", file=sys.stderr)
        return 1

    skills = find_skills(root)
    if not skills:
        print(f"No skills found under {root}")
        return 0

    print(f"Validating {len(skills)} skill(s) against the authoring gate (crawl, walk and run)...\n")

    n_clean = 0
    n_warn_only = 0
    n_fail = 0

    for skill_dir in skills:
        failures, warnings = validate_skill(skill_dir)

        if not failures and not warnings:
            n_clean += 1
            continue

        print(_rel(skill_dir, root))
        for msg in failures:
            print(f"  FAIL  {msg}")
        for msg in warnings:
            print(f"  WARN  {msg}")
        print()

        if failures:
            n_fail += 1
        else:
            n_warn_only += 1

    # summary
    print(f"{'─' * 60}")
    print(f"  Validated {len(skills)} skill(s)")
    print(f"  Clean     {n_clean}")
    if n_warn_only:
        print(f"  Warnings  {n_warn_only} skill(s) — advisory only")
    if n_fail:
        print(f"  Failures  {n_fail} skill(s) — must be fixed\n")
        print("Exit: 1 — fix FAILs before merging")
        return 1

    print()
    print("Exit: 0 — all skills pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
