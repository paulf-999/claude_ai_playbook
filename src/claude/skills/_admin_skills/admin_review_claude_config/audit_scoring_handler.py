"""Programmatic scoring and audit trail handler for admin_claude_config_review.

Implements scoring functions for 4 quality dimensions, config validation,
and reproducible audit trails saved to JSON.

Example usage:
    audit = audit_claude_config(config_path="~/.claude", save_trail=True)
    if audit["success"]:
        print(f"Overall grade: {audit['result']['overall_grade']}")
        print(f"Scores: {audit['result']['dimension_scores']}")
    else:
        print(f"Audit failed: {audit['errors']}")
"""

from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json

# Quality dimensions
DIMENSIONS = ["testing", "security", "documentation", "standards"]
DIMENSION_DESCRIPTIONS = {
    "testing": "Test coverage, test organization, test quality",
    "security": "Secret handling, permission guardrails, input validation",
    "documentation": "Clarity, examples, completeness, known gaps",
    "standards": "Naming conventions, file structure, style guide adherence",
}

# Scoring thresholds
MIN_SCORE = 1
MAX_SCORE = 10
GRADE_THRESHOLDS = {
    "A": 9,   # Excellent
    "B": 8,   # Good
    "C": 7,   # Acceptable
    "D": 6,   # Needs improvement
    "F": 0,   # Poor
}

# Config file checklist
REQUIRED_FILES = {
    "CLAUDE.md": "Root config file",
    "_rules/": "Rules directory",
    "memory/MEMORY.md": "Memory index",
    "aliases.md": "Command aliases",
    "settings.json": "Settings configuration",
}

OPTIONAL_FILES = {
    "_rules/guiding_principles.md": "Guiding principles rule",
    "_rules/behaviour.md": "Behavior rule",
    "_rules/testing.md": "Testing rule",
    "_rules/security.md": "Security rule",
}


def validate_config(config_path: str) -> Dict[str, Any]:
    """Validate config directory structure and required files.

    Args:
        config_path: Path to config directory (~/.claude)

    Returns:
        {"valid": True, "issues": []} on success
        {"valid": False, "errors": [...], "issues": [...]} on failure
    """
    config_dir = Path(config_path).expanduser()
    errors = []
    issues = []

    # Check directory exists
    if not config_dir.exists():
        return {"valid": False, "errors": [f"Config directory {config_path} not found"]}

    if not config_dir.is_dir():
        return {"valid": False, "errors": [f"{config_path} is not a directory"]}

    # Check required files
    for file_path, description in REQUIRED_FILES.items():
        full_path = config_dir / file_path
        if not full_path.exists():
            errors.append(f"Missing required file: {file_path}")

    # Check optional files (for scoring only)
    for file_path, description in OPTIONAL_FILES.items():
        full_path = config_dir / file_path
        if not full_path.exists():
            issues.append(f"Missing optional file: {file_path}")

    if errors:
        return {"valid": False, "errors": errors, "issues": issues}

    return {"valid": True, "issues": issues}


def score_testing(config_path: str) -> Tuple[int, str, List[str]]:
    """Score testing dimension: test coverage, organization, quality.

    Checks: test files exist, test organization, test count indicators.

    Args:
        config_path: Path to config directory

    Returns:
        (score: 1-10, reasoning: str, found_issues: [])
    """
    config_dir = Path(config_path).expanduser()
    issues = []
    score_components = []

    # Check for test directories
    test_dir = config_dir / "_tests"
    if test_dir.exists():
        score_components.append(("Test directory exists", 2))
        # Check for test files
        test_files = list(test_dir.glob("**/*.py"))
        if len(test_files) > 5:
            score_components.append(("Comprehensive test coverage (5+ files)", 3))
        elif len(test_files) > 0:
            score_components.append(("Basic test coverage", 1))
        else:
            issues.append("No test files found in _tests/")
    else:
        issues.append("No _tests/ directory found")

    # Check for rules (should have tests)
    rules_dir = config_dir / "_rules"
    if rules_dir.exists():
        rule_files = list(rules_dir.glob("**/*.md"))
        if len(rule_files) > 5:
            score_components.append(("Multiple rules exist (should be tested)", 2))

    # Calculate score (max 10)
    score = min(MAX_SCORE, sum(c[1] for c in score_components))

    reasoning = "Testing: " + "; ".join([f"{name} (+{points})" for name, points in score_components])
    if not score_components:
        score = MIN_SCORE
        reasoning = "Testing: No test infrastructure found"

    return score, reasoning, issues


def score_security(config_path: str) -> Tuple[int, str, List[str]]:
    """Score security dimension: secret handling, permissions, validation.

    Checks: security rules exist, .gitignore coverage, secret handling docs.

    Args:
        config_path: Path to config directory

    Returns:
        (score: 1-10, reasoning: str, found_issues: [])
    """
    config_dir = Path(config_path).expanduser()
    issues = []
    score_components = []

    # Check for security rules
    security_rule = config_dir / "_rules" / "security.md"
    if security_rule.exists():
        score_components.append(("Security rule exists", 3))
    else:
        issues.append("No security.md rule found")

    # Check for guardrails rules
    guardrails_rule = config_dir / "_rules" / "claude_internal" / "security_guardrails.md"
    if guardrails_rule.exists():
        score_components.append(("Security guardrails documented", 3))
    else:
        issues.append("No security_guardrails.md found")

    # Check for .env/.gitignore awareness
    gitignore_path = config_dir.parent / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if ".env" in content:
            score_components.append((".env in .gitignore", 2))
        else:
            issues.append(".env not in .gitignore")

    # Check for MCP trust model
    mcp_trust = config_dir / "_rules" / "mcp_trust_model.md"
    if mcp_trust.exists():
        score_components.append(("MCP trust model documented", 2))

    score = min(MAX_SCORE, sum(c[1] for c in score_components))
    reasoning = "Security: " + "; ".join([f"{name} (+{points})" for name, points in score_components])
    if not score_components:
        score = MIN_SCORE
        reasoning = "Security: No security documentation found"

    return score, reasoning, issues


def score_documentation(config_path: str) -> Tuple[int, str, List[str]]:
    """Score documentation dimension: clarity, examples, completeness.

    Checks: README exists, rules documented, examples present.

    Args:
        config_path: Path to config directory

    Returns:
        (score: 1-10, reasoning: str, found_issues: [])
    """
    config_dir = Path(config_path).expanduser()
    issues = []
    score_components = []

    # Check for main CLAUDE.md
    claude_md = config_dir / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()
        score_components.append(("CLAUDE.md exists", 2))
        if len(content) > 500:
            score_components.append(("Substantial documentation (500+ chars)", 2))
    else:
        issues.append("No CLAUDE.md found")

    # Check for rule documentation
    rules_dir = config_dir / "_rules"
    if rules_dir.exists():
        rule_files = list(rules_dir.glob("**/*.md"))
        if len(rule_files) > 0:
            score_components.append(("Rules documented", 2))
            # Check for docstrings/examples in rules
            documented_rules = sum(1 for f in rule_files if f.read_text().count("##") > 2)
            if documented_rules > 0:
                score_components.append(("Rules have examples/structure", 2))

    # Check for skills documentation
    skills_dir = config_dir / "skills"
    if skills_dir.exists():
        skill_files = list(skills_dir.glob("**/SKILL.md"))
        if len(skill_files) > 0:
            score_components.append(("Skills documented", 2))

    score = min(MAX_SCORE, sum(c[1] for c in score_components))
    reasoning = "Documentation: " + "; ".join([f"{name} (+{points})" for name, points in score_components])
    if not score_components:
        score = MIN_SCORE
        reasoning = "Documentation: Minimal documentation found"

    return score, reasoning, issues


def score_standards(config_path: str) -> Tuple[int, str, List[str]]:
    """Score standards dimension: naming, file structure, style guide.

    Checks: naming conventions, directory organization, file structure.

    Args:
        config_path: Path to config directory

    Returns:
        (score: 1-10, reasoning: str, found_issues: [])
    """
    config_dir = Path(config_path).expanduser()
    issues = []
    score_components = []

    # Check for naming standards rule
    naming_rule = config_dir / "_rules" / "naming_standards.md"
    if naming_rule.exists():
        score_components.append(("Naming standards documented", 3))
    else:
        issues.append("No naming_standards.md found")

    # Check for directory structure
    expected_dirs = ["_rules", "skills", "memory"]
    found_dirs = sum(1 for d in expected_dirs if (config_dir / d).exists())
    if found_dirs >= 2:
        score_components.append(("Standard directory structure", 2))
    else:
        issues.append(f"Only {found_dirs}/3 standard directories found")

    # Check for style guide
    style_guide = config_dir / "style_guide_standards.md"
    if style_guide.exists():
        score_components.append(("Style guide exists", 2))

    # Check for writing standards
    writing_rule = config_dir / "_rules" / "writing_style.md"
    if writing_rule.exists():
        score_components.append(("Writing style rule exists", 2))

    # Check file naming (underscores, no spaces)
    rule_files = list((config_dir / "_rules").glob("**/*.md")) if (config_dir / "_rules").exists() else []
    bad_naming = sum(1 for f in rule_files if " " in f.name or "-" in f.name)
    if bad_naming == 0 and len(rule_files) > 0:
        score_components.append(("Consistent naming (no spaces/hyphens)", 1))

    score = min(MAX_SCORE, sum(c[1] for c in score_components))
    reasoning = "Standards: " + "; ".join([f"{name} (+{points})" for name, points in score_components])
    if not score_components:
        score = MIN_SCORE
        reasoning = "Standards: No standards documentation found"

    return score, reasoning, issues


def calculate_overall_grade(dimension_scores: Dict[str, int]) -> str:
    """Convert numeric average score to letter grade.

    Args:
        dimension_scores: Dict of dimension names to numeric scores (1-10)

    Returns:
        Letter grade (A-F)
    """
    if not dimension_scores:
        return "F"

    avg_score = sum(dimension_scores.values()) / len(dimension_scores)

    for grade, threshold in sorted(GRADE_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if avg_score >= threshold:
            return grade

    return "F"


def audit_claude_config(
    config_path: str = "~/.claude",
    save_trail: bool = True,
    trail_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Orchestrate full audit: validate → score all dimensions → generate audit trail.

    Args:
        config_path: Path to config directory (default ~/.claude)
        save_trail: Whether to save audit trail to JSON
        trail_dir: Directory for audit trail JSON (default ~/.claude/_admin/_audits)

    Returns:
        On success:
            {"success": True, "result": {
                "overall_grade": "A",
                "dimension_scores": {"testing": 7, ...},
                "all_issues": [...],
                "timestamp": "2026-08-18T...",
                "trail_path": "/path/to/audit.json"
            }}

        On failure:
            {"success": False, "errors": [...]}
    """
    # Validate config structure
    validation = validate_config(config_path)
    if not validation["valid"]:
        return {"success": False, "errors": validation["errors"]}

    # Score all four dimensions
    dimension_scores = {}
    all_issues = []
    dimension_reasoning = {}

    for dimension in DIMENSIONS:
        if dimension == "testing":
            score, reasoning, issues = score_testing(config_path)
        elif dimension == "security":
            score, reasoning, issues = score_security(config_path)
        elif dimension == "documentation":
            score, reasoning, issues = score_documentation(config_path)
        elif dimension == "standards":
            score, reasoning, issues = score_standards(config_path)
        else:
            score, reasoning, issues = MIN_SCORE, f"Unknown dimension: {dimension}", []

        dimension_scores[dimension] = score
        dimension_reasoning[dimension] = reasoning
        all_issues.extend(issues)

    # Calculate overall grade
    overall_grade = calculate_overall_grade(dimension_scores)

    # Build result
    result = {
        "overall_grade": overall_grade,
        "dimension_scores": dimension_scores,
        "dimension_reasoning": dimension_reasoning,
        "all_issues": all_issues,
        "timestamp": datetime.now().isoformat(),
        "config_path": config_path,
    }

    # Save audit trail to JSON if requested
    trail_path = None
    if save_trail:
        trail_directory = Path(trail_dir or f"{config_path}/_admin/_audits").expanduser()
        trail_directory.mkdir(parents=True, exist_ok=True)
        trail_path = trail_directory / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            trail_path.write_text(json.dumps(result, indent=2))
            result["trail_path"] = str(trail_path)
        except Exception as e:
            # Non-fatal: audit succeeded but trail save failed
            result["trail_save_error"] = str(e)

    return {"success": True, "result": result}


if __name__ == "__main__":
    # Quick smoke test
    result = audit_claude_config(config_path="~/.claude", save_trail=False)
    if result["success"]:
        r = result["result"]
        print(f"Overall Grade: {r['overall_grade']}")
        print(f"Dimension Scores: {r['dimension_scores']}")
        print(f"Issues Found: {len(r['all_issues'])}")
    else:
        print(f"Audit failed: {result['errors']}")
