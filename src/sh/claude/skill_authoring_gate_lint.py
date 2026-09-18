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

import yaml

# ── script location ───────────────────────────────────────────────────────────

# Script lives at src/sh/claude/; repo root is three levels up.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_ROOT = _REPO_ROOT / "src" / "claude" / "skills"


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
    """Check if SKILL.md has the canonical 5-section structure.

    Per authoring_skills.md's Core Standards, every skill is:
      1. Frontmatter — name, version, maturity, description, tags (checked by C5)
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
    section 1 of the canonical structure, and must declare name, description,
    version, and maturity.

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

    for field in ["name", "description", "version", "maturity"]:
        if field not in data or data[field] is None:
            issues.append(f"SKILL.md frontmatter missing required field: {field}")

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
