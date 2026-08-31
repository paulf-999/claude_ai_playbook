#!/usr/bin/env python3
"""Skill authoring gate linter — validates crawl criteria (C0–C7).

Validates skill.contract.yaml and SKILL.md against the skill authoring gate
foundation criteria (crawl level). Ensures all skills meet basic structure,
contract, and no problematic coupling before merging.

Usage:
    python3 src/sh/claude/skill_authoring_gate_lint.py          # scan src/claude/skills/ (default)
    python3 src/sh/claude/skill_authoring_gate_lint.py <root>   # scan an explicit root dir
    make lint_skills                                             # via Makefile target

Exit codes:
    0 — all skills pass
    1 — one or more skills have violations
"""

import argparse
import re
import sys
from pathlib import Path

import frontmatter
import yaml

# ── script location ───────────────────────────────────────────────────────────

# Script lives at src/sh/claude/; repo root is three levels up.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_ROOT = _REPO_ROOT / "src" / "claude" / "skills"


# ── validation logic ──────────────────────────────────────────────────────────


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    """Validate a skill against crawl criteria (C0–C7).

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: Tuple of (failures, warnings).
    :rtype: tuple[list[str], list[str]]
    """
    failures: list[str] = []
    warnings: list[str] = []

    # C0: Skill directory exists (implicit in discovery)
    skill_name = skill_dir.name

    # Read files
    contract_path = skill_dir / "skill.contract.yaml"
    skill_md_path = skill_dir / "SKILL.md"

    # C1: skill.contract.yaml exists and has all required fields
    if not contract_path.exists():
        failures.append("C1: skill.contract.yaml missing")
        return failures, warnings  # Can't validate further without contract

    try:
        with open(contract_path, encoding="utf-8") as f:
            contract = yaml.safe_load(f) or {}
    except Exception as exc:
        failures.append(f"C1: skill.contract.yaml parse error: {exc}")
        return failures, warnings

    # Validate required core fields (flexible format support)
    # Supports both new format (when, dont_use_for, requires, output, reversible)
    # and legacy format (dispatch, dependencies, output)
    core_required = ["name", "version", "summary", "maturity", "test_coverage_level"]
    for field in core_required:
        if field not in contract or contract[field] is None:
            failures.append(f"C1: skill.contract.yaml missing required field: {field}")

    # Check for either new or legacy format fields (at least one must exist)
    has_new_format = any(k in contract for k in ["when", "requires"])
    has_legacy_format = any(k in contract for k in ["dispatch", "dependencies"])
    if not has_new_format and not has_legacy_format:
        failures.append("C1: skill.contract.yaml missing trigger/dependency fields (when/requires or dispatch/dependencies)")

    # C3: Version is semantic and matches maturity
    version = contract.get("version", "")
    if version:
        if not _is_semantic_version(version):
            failures.append(f"C3: version '{version}' is not semantic (X.Y.Z)")
        else:
            maturity = contract.get("maturity")
            if maturity:
                version_major = int(version.split(".")[0])
                maturity_check = _check_maturity_version_alignment(version_major, maturity)
                if not maturity_check:
                    failures.append(
                        f"C3: version major {version_major} doesn't match maturity '{maturity}' "
                        "(draft=0.x, tactical=1.x, strategic=2+.x)"
                    )

    # C6: No hardcoded paths or personal references
    contract_str = yaml.dump(contract)
    path_issues = _check_hardcoded_paths(contract_str)
    if path_issues:
        failures.extend([f"C6: {issue}" for issue in path_issues])

    # C2: No hardcoded skill names in SKILL.md
    if skill_md_path.exists():
        try:
            skill_md_content = skill_md_path.read_text(encoding="utf-8")
            skill_name_issues = _check_hardcoded_skill_names(skill_md_content, skill_name)
            if skill_name_issues:
                failures.extend([f"C2: {issue}" for issue in skill_name_issues])
        except Exception as exc:
            failures.append(f"C2: SKILL.md read error: {exc}")
    else:
        failures.append("C4: SKILL.md missing")

    # C4: SKILL.md has required structure
    if skill_md_path.exists():
        try:
            structure_issues = _check_skill_md_structure(skill_md_path)
            if structure_issues:
                failures.extend([f"C4: {issue}" for issue in structure_issues])
        except Exception as exc:
            failures.append(f"C4: SKILL.md structure check failed: {exc}")

    # C5: SKILL.md is end-user-first (metadata table comes first)
    if skill_md_path.exists():
        try:
            if not _is_end_user_first(skill_md_path):
                failures.append(
                    "C5: SKILL.md should start with metadata table, not YAML frontmatter or prose"
                )
        except Exception as exc:
            failures.append(f"C5: SKILL.md readability check failed: {exc}")

    # C7: All tools/MCP/external listed in requires section
    requires = contract.get("requires", {})
    if not isinstance(requires, dict):
        failures.append("C7: requires field must be a dict with tools, mcp_servers, external keys")
    else:
        # This is documented in contract but not enforced mechanically (requires code analysis)
        if "tools" not in requires:
            warnings.append("C7: requires.tools is empty or missing (list tools this skill uses)")
        if "mcp_servers" not in requires:
            warnings.append("C7: requires.mcp_servers is empty or missing")
        if "external" not in requires:
            warnings.append("C7: requires.external is empty or missing")

    return failures, warnings


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
    """Check if SKILL.md has core required sections.

    New standard requires 8 sections in canonical order:
      1. 📖 Overview — one-sentence plain-language description
      2. 🎯 Scope — maturity level + constraints
      3. ✅ Capabilities — can/can't do
      4. 🔐 Security — data handling + access
      5. 📝 Prerequisites — required setup
      6. 🛠️ Workflow — step-by-step phases
      7. 🚨 Error Recovery — common failures + fixes
      8. 🛣️ Known Gaps — limitations + roadmap

    Legacy sections (still acceptable, but new skills should use canonical naming):
    - "What this skill does", "Description" → Overview
    - "Can do" (without emoji) → Capabilities
    - "Prerequisites" → Prerequisites
    - "How it works", "Phases" → Workflow
    - "Known gaps" (without emoji) → Known Gaps

    :param skill_md_path: Path to SKILL.md.
    :type skill_md_path: Path
    :return: List of issues found.
    :rtype: list[str]
    """
    issues = []
    content = skill_md_path.read_text(encoding="utf-8")

    # Check for core sections (allow both new canonical names and legacy names)
    # Quality Scorecard moved to new-standard-only to avoid breaking legacy skills
    required_sections = {
        r"## .*(📖|overview|what.*does|description)": "Overview/Description section",
        r"## .*(✅|capabilities|can\w*.*do)": "Capabilities/Can do section",
        r"## .*(📝|prerequisites)": "Prerequisites section",
        r"## .*(🛠️|workflow|how it works|phases)": "Workflow/How it works/Phases section",
        r"## .*(🛣️|known gaps)": "Known Gaps section",
    }

    for pattern, description in required_sections.items():
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"missing {description}")

    # New standard sections: Quality Scorecard, Scope, Security, Error Recovery
    # These are required for new skills (with emoji headers) but warned for legacy skills
    new_standard_sections = {
        r"## .*(📊|quality.*scorecard)": "Quality Scorecard section (new standard)",
        r"## .*(🎯|scope)": "Scope section (new standard)",
        r"## .*(🔐|security)": "Security section (new standard)",
        r"## .*(🚨|error recovery)": "Error Recovery section (new standard)",
    }

    # Only require new standard sections if file uses the new canonical structure
    # Detection: has 📖 Overview section (the canonical first section)
    has_new_overview = bool(re.search(r"^## 📖\s+overview", content, re.IGNORECASE | re.MULTILINE))
    if has_new_overview:
        # New-style skill; check for all new standard sections
        for pattern, description in new_standard_sections.items():
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append(f"missing {description}")

    return issues


def _is_end_user_first(skill_md_path: Path) -> bool:
    """Check if SKILL.md opens with end-user content (not frontmatter).

    Should start with metadata table or heading, not YAML frontmatter block.

    :param skill_md_path: Path to SKILL.md.
    :type skill_md_path: Path
    :return: True if structure is end-user-first.
    :rtype: bool
    """
    content = skill_md_path.read_text(encoding="utf-8").strip()

    # Skip frontmatter if present
    if content.startswith("---"):
        return False  # frontmatter is not end-user-first

    # Should start with heading or table
    return content.startswith("#") or content.startswith("|")


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

    print(f"Validating {len(skills)} skill(s) against authoring gate (crawl criteria)...\n")

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
