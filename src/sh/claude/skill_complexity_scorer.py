#!/usr/bin/env python3
"""Skill complexity scorer — calculates complexity score for a skill.

Scores a skill on a 0-10 scale based on:
  1. Number of concepts introduced (0-3 pts)
  2. Implementation scope / phases (0-3 pts)
  3. Dependencies and integrations (0-2 pts)
  4. Prerequisite knowledge required (0-2 pts)

Usage:
    python3 skill_complexity_scorer.py <skill_dir>

Returns:
    JSON with complexity score and breakdown
    Exit code 0 if score is acceptable for maturity
    Exit code 1 if score exceeds maturity limit (crawl violation)
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


# Maturity limits (hard gates)
MATURITY_LIMITS = {
    "draft": 4,
    "tactical": 6,
    "strategic": 8,
}


def count_concepts(skill_md_path: Path) -> int:
    """Count distinct concepts from SKILL.md 'can do' section.

    :param skill_md_path: Path to SKILL.md
    :type skill_md_path: Path
    :return: Concept count (0-5+)
    :rtype: int
    """
    if not skill_md_path.exists():
        return 0

    content = skill_md_path.read_text(encoding="utf-8")

    # Find "can do" section and count bullets until next ## header
    in_can_do = False
    concept_count = 0

    for line in content.split("\n"):
        if "can" in line.lower() and "do" in line.lower() and line.startswith("##"):
            in_can_do = True
            continue
        if in_can_do and line.startswith("##"):
            break
        if in_can_do and line.strip().startswith("-"):
            concept_count += 1

    return concept_count


def score_concepts(count: int) -> int:
    """Convert concept count to points (0-3).

    :param count: Number of concepts
    :type count: int
    :return: Points (0-3)
    :rtype: int
    """
    if count <= 2:
        return 0
    elif count <= 4:
        return 1
    elif count <= 5:
        return 2
    else:
        return 3


def count_phases(skill_dir: Path) -> int:
    """Count phase files in skill directory.

    :param skill_dir: Path to skill directory
    :type skill_dir: Path
    :return: Number of phases
    :rtype: int
    """
    return len(list(skill_dir.glob("phase*.md")))


def count_lines(skill_md_path: Path) -> int:
    """Count lines in SKILL.md.

    :param skill_md_path: Path to SKILL.md
    :type skill_md_path: Path
    :return: Line count
    :rtype: int
    """
    if not skill_md_path.exists():
        return 0
    return len(skill_md_path.read_text(encoding="utf-8").split("\n"))


def score_scope(phases: int, lines: int) -> int:
    """Convert scope (phases + lines) to points (0-3).

    :param phases: Number of phase files
    :type phases: int
    :param lines: Line count in SKILL.md
    :type lines: int
    :return: Points (0-3)
    :rtype: int
    """
    if phases >= 4 or lines > 200:
        return 3
    elif phases >= 2:
        return 2
    elif lines >= 100:
        return 1
    else:
        return 0


def count_dependencies(contract: dict) -> int:
    """Count external dependencies from contract.

    :param contract: Parsed skill.contract.yaml
    :type contract: dict
    :return: Dependency count
    :rtype: int
    """
    count = 0
    requires = contract.get("requires", {})

    # Count MCP servers
    mcp_servers = requires.get("mcp_servers", [])
    count += len(mcp_servers) if mcp_servers else 0

    # Count external systems
    external = requires.get("external", [])
    count += len(external) if external else 0

    return count


def score_dependencies(count: int) -> int:
    """Convert dependency count to points (0-2).

    :param count: Number of external dependencies
    :type count: int
    :return: Points (0-2)
    :rtype: int
    """
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    else:
        return 2


def count_prerequisite_domains(skill_md_path: Path) -> int:
    """Count distinct domains mentioned in prerequisites section.

    :param skill_md_path: Path to SKILL.md
    :type skill_md_path: Path
    :return: Number of prerequisite domains
    :rtype: int
    """
    if not skill_md_path.exists():
        return 0

    content = skill_md_path.read_text(encoding="utf-8")

    # Find prerequisites section
    in_prereqs = False
    prereq_text = ""

    for line in content.split("\n"):
        if "prerequisite" in line.lower() and line.startswith("##"):
            in_prereqs = True
            continue
        if in_prereqs and line.startswith("##"):
            break
        if in_prereqs:
            prereq_text += line.lower()

    # Count domains (heuristic: jira, github, confluence, dbt, airflow, etc.)
    domains = [
        "jira",
        "github",
        "confluence",
        "dbt",
        "airflow",
        "terraform",
        "kubernetes",
        "sql",
        "python",
        "bash",
    ]
    found_domains = set()
    for domain in domains:
        if domain in prereq_text:
            found_domains.add(domain)

    return len(found_domains)


def score_prerequisites(domain_count: int) -> int:
    """Convert prerequisite domain count to points (0-2).

    :param domain_count: Number of domains in prerequisites
    :type domain_count: int
    :return: Points (0-2)
    :rtype: int
    """
    if domain_count == 0:
        return 0
    elif domain_count == 1:
        return 1
    else:
        return 2


def calculate_complexity(skill_dir: Path) -> dict:
    """Calculate complexity score for a skill.

    :param skill_dir: Path to skill directory
    :type skill_dir: Path
    :return: Dict with score, breakdown, and maturity check
    :rtype: dict
    """
    contract_path = skill_dir / "skill.contract.yaml"
    skill_md_path = skill_dir / "SKILL.md"

    # Load contract
    contract = {}
    if contract_path.exists():
        with open(contract_path, encoding="utf-8") as f:
            contract = yaml.safe_load(f) or {}

    # Calculate each dimension
    concepts = count_concepts(skill_md_path)
    concepts_pts = score_concepts(concepts)

    phases = count_phases(skill_dir)
    lines = count_lines(skill_md_path)
    scope_pts = score_scope(phases, lines)

    deps = count_dependencies(contract)
    deps_pts = score_dependencies(deps)

    prereq_domains = count_prerequisite_domains(skill_md_path)
    prereq_pts = score_prerequisites(prereq_domains)

    total_score = concepts_pts + scope_pts + deps_pts + prereq_pts

    # Get maturity and check limit
    maturity = contract.get("maturity", "draft")
    limit = MATURITY_LIMITS.get(maturity, 4)
    exceeds_limit = total_score > limit

    return {
        "skill_name": skill_dir.name,
        "maturity": maturity,
        "total_score": total_score,
        "limit": limit,
        "exceeds_limit": exceeds_limit,
        "breakdown": {
            "concepts": {"count": concepts, "points": concepts_pts, "max": 3},
            "scope": {"phases": phases, "lines": lines, "points": scope_pts, "max": 3},
            "dependencies": {"count": deps, "points": deps_pts, "max": 2},
            "prerequisites": {"domains": prereq_domains, "points": prereq_pts, "max": 2},
        },
    }


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate complexity score for a skill.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON (default: human-readable)",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"error: skill directory not found: {skill_dir}", file=sys.stderr)
        return 1

    result = calculate_complexity(skill_dir)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        score = result["total_score"]
        limit = result["limit"]
        maturity = result["maturity"]
        exceeds = result["exceeds_limit"]

        print(f"Complexity Score: {score}/10 ({maturity} skill, limit: {limit})")
        print()
        print("Breakdown:")
        print(
            f"  Concepts:      {result['breakdown']['concepts']['points']}/{result['breakdown']['concepts']['max']} pts "
            f"({result['breakdown']['concepts']['count']} concepts)"
        )
        print(
            f"  Scope:         {result['breakdown']['scope']['points']}/{result['breakdown']['scope']['max']} pts "
            f"({result['breakdown']['scope']['phases']} phases, {result['breakdown']['scope']['lines']} lines)"
        )
        print(
            f"  Dependencies:  {result['breakdown']['dependencies']['points']}/{result['breakdown']['dependencies']['max']} pts "
            f"({result['breakdown']['dependencies']['count']} dependencies)"
        )
        print(
            f"  Prerequisites: {result['breakdown']['prerequisites']['points']}/{result['breakdown']['prerequisites']['max']} pts "
            f"({result['breakdown']['prerequisites']['domains']} domains)"
        )
        print()
        if exceeds:
            print(f"❌ EXCEEDS LIMIT: Score {score} > {limit} for {maturity} skill")
            return 1
        else:
            print(f"✅ PASS: Score {score} is acceptable for {maturity} skill")
            return 0


if __name__ == "__main__":
    sys.exit(main())
