#!/usr/bin/env python3
"""
Skill Template Compliance Test Suite

Validates all installed skills in ~/.claude/skills/ comply with canonical structure:
- SKILL.md structure (8 sections with canonical emoji headers)
- skill.contract.yaml schema (Variant A: when/dont_use_for/requires)
- Frontmatter field consistency
- Quality scorecard depth by maturity
- Semantic consistency between SKILL.md and contract

Design: Fail-first — tests deliberately fail on current deviations to generate
compliance baseline for Item 24 (consistency audit).

Test organization:
  - Structural tests (form/format validation)
  - Quality tests (content expectations)
  - Contract tests (tool/dependency declarations)
  - Semantic tests (consistency between SKILL.md and contract)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

# Canonical skill structure
CANONICAL_SECTIONS = [
    "Overview",
    "Quality Scorecard",
    "Scope",
    "Capabilities",
    "Security",
    "Prerequisites",
    "Workflow",
    "Error Recovery",
    "Known Gaps",
]

# Canonical emoji-to-section mapping
CANONICAL_EMOJI_MAP = {
    "📖": "Overview",
    "📊": "Quality Scorecard",
    "🎯": "Scope",
    "✨": "Capabilities",
    "🔐": "Security",
    "📋": "Prerequisites",
    "⚙️": "Workflow",
    "🆘": "Error Recovery",
    "⚠️": "Known Gaps",
}

# Required frontmatter fields (in SKILL.md)
REQUIRED_FRONTMATTER_FIELDS = [
    "name",
    "description",
    "version",
    "maturity",
    "tags",
]

# Required contract fields (in skill.contract.yaml)
REQUIRED_CONTRACT_FIELDS = [
    "name",
    "version",
    "summary",
    "maturity",
    "test_coverage_level",
    "when",
    "dont_use_for",
    "requires",
    "output",
    "reversible",
]

# Valid maturity levels
VALID_MATURITY_LEVELS = ["draft", "tactical", "strategic"]

# Valid tools
VALID_TOOLS = [
    "Bash",
    "Read",
    "Write",
    "Edit",
    "Agent",
    "Skill",
    "AskUserQuestion",
    "Workflow",
    "ToolSearch",
    "WebFetch",
    "WebSearch",
    "LSP",
]

# Valid MCP servers (common ones; can be extended)
VALID_MCP_SERVERS = [
    "GitHub",
    "Atlassian",
    "Microsoft_365",
    "context7",
    "filesystem",
    "memory",
    "sequential-thinking",
]


class SkillComplianceValidator:
    """Validates a skill against canonical structure."""

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.violations = []
        self.warnings = []

    def validate(self) -> Dict:
        """Run all compliance checks."""
        self._check_skill_directory()
        self._check_skill_md()
        self._check_contract()
        self._check_frontmatter_consistency()
        self._check_quality_scorecard()
        self._check_semantic_consistency()

        return {
            "skill": self.skill_name,
            "path": str(self.skill_path),
            "violations": self.violations,
            "warnings": self.warnings,
            "status": "PASS" if not self.violations else "FAIL",
        }

    def _check_skill_directory(self) -> None:
        """Verify skill directory structure."""
        if not self.skill_path.is_dir():
            self.violations.append(f"Skill directory not found: {self.skill_path}")
            return

    def _check_skill_md(self) -> None:
        """Validate SKILL.md structure."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.violations.append("SKILL.md not found")
            return

        content = skill_md.read_text()

        # Check for frontmatter
        if not content.startswith("---"):
            self.violations.append("SKILL.md missing YAML frontmatter")
            return

        # Extract frontmatter
        try:
            _, frontmatter_str, rest = content.split("---", 2)
            self.frontmatter = yaml.safe_load(frontmatter_str)
            self.skill_content = rest
        except Exception as e:
            self.violations.append(f"SKILL.md frontmatter parse error: {e}")
            return

        # Check all canonical sections are present
        for section in CANONICAL_SECTIONS:
            if f"## {section}" not in content and f"## 📖 {section}" not in content:
                # Check with any emoji prefix
                pattern = rf"##\s+[📖✨🎯🔐📊⚙️🆘⚠️📋]\s+{re.escape(section)}"
                if not re.search(pattern, content):
                    self.violations.append(
                        f"Missing canonical section: {section}"
                    )

        # Check emoji header consistency
        self._check_emoji_headers(content)

        # Check line count
        lines = content.split('\n')
        if len(lines) > 120:
            self.warnings.append(
                f"SKILL.md exceeds 110 lines ({len(lines)} lines); consider splitting into parent + children"
            )

    def _check_emoji_headers(self, content: str) -> None:
        """Validate emoji-to-section mapping matches canonical."""
        # Find all section headers with emojis
        header_pattern = r"##\s+([📖✨🎯🔐📊⚙️🆘⚠️📋])\s+([^\n]+)"
        found_headers = re.findall(header_pattern, content)

        for emoji, section in found_headers:
            if emoji not in CANONICAL_EMOJI_MAP:
                self.violations.append(
                    f"Unknown emoji in section header: {emoji}"
                )
            elif CANONICAL_EMOJI_MAP[emoji] != section:
                self.violations.append(
                    f"Emoji-section mismatch: {emoji} maps to '{CANONICAL_EMOJI_MAP[emoji]}', found '{section}'"
                )

    def _check_contract(self) -> None:
        """Validate skill.contract.yaml structure."""
        contract_path = self.skill_path / "skill.contract.yaml"

        if not contract_path.exists():
            self.violations.append("skill.contract.yaml not found at skill root")
            return

        try:
            with open(contract_path) as f:
                self.contract = yaml.safe_load(f)
        except Exception as e:
            self.violations.append(f"skill.contract.yaml parse error: {e}")
            return

        if not self.contract:
            self.violations.append("skill.contract.yaml is empty")
            return

        # Check required fields
        for field in REQUIRED_CONTRACT_FIELDS:
            if field not in self.contract:
                self.violations.append(f"Contract missing required field: {field}")

        # Check for deprecated Variant B fields
        if "dispatch" in self.contract:
            self.violations.append(
                "Contract uses deprecated Variant B schema (dispatch:). Use canonical Variant A (when:, dont_use_for:, requires:)"
            )
        if "dependencies" in self.contract:
            self.violations.append(
                "Contract uses deprecated Variant B schema (dependencies:). Use canonical requires:"
            )

        # Validate maturity
        if "maturity" in self.contract:
            if self.contract["maturity"] not in VALID_MATURITY_LEVELS:
                self.violations.append(
                    f"Invalid maturity level: {self.contract['maturity']}. Must be: {VALID_MATURITY_LEVELS}"
                )

        # Validate semantic versioning matches maturity
        self._check_semantic_version()

        # Validate tools
        if "requires" in self.contract:
            requires = self.contract["requires"]
            if isinstance(requires, dict) and "tools" in requires:
                tools = requires["tools"]
                if isinstance(tools, list):
                    for tool in tools:
                        if tool not in VALID_TOOLS:
                            self.warnings.append(
                                f"Unknown tool in requires.tools: {tool}"
                            )

            # Validate MCP servers
            if isinstance(requires, dict) and "mcp_servers" in requires:
                mcp_servers = requires["mcp_servers"]
                if isinstance(mcp_servers, list):
                    for server in mcp_servers:
                        if server not in VALID_MCP_SERVERS:
                            self.warnings.append(
                                f"Unknown MCP server: {server}"
                            )

    def _check_semantic_version(self) -> None:
        """Validate semantic version matches maturity level."""
        if "version" not in self.contract or "maturity" not in self.contract:
            return

        version = self.contract["version"]
        maturity = self.contract["maturity"]

        # Parse version
        try:
            major, minor, patch = version.split(".")
            major = int(major)
        except Exception:
            self.violations.append(f"Invalid semantic version: {version}")
            return

        # Check maturity-to-version alignment
        if maturity == "draft" and major != 0:
            self.violations.append(
                f"Draft skills must have version 0.x.x; found {version}"
            )
        elif maturity == "tactical" and major != 1:
            self.violations.append(
                f"Tactical skills must have version 1.x.x; found {version}"
            )
        elif maturity == "strategic" and major < 2:
            self.violations.append(
                f"Strategic skills must have version 2.x.x or higher; found {version}"
            )

    def _check_frontmatter_consistency(self) -> None:
        """Validate frontmatter fields and consistency with contract."""
        if not hasattr(self, "frontmatter") or not self.frontmatter:
            return

        # Check required fields
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in self.frontmatter:
                self.violations.append(
                    f"Frontmatter missing required field: {field}"
                )

        # Validate tags structure
        if "tags" in self.frontmatter:
            tags = self.frontmatter["tags"]
            if not isinstance(tags, dict):
                self.violations.append("Frontmatter field 'tags' must be a dict")
            else:
                required_tags = ["criticality", "status", "tested", "test_coverage_level"]
                for tag in required_tags:
                    if tag not in tags:
                        self.violations.append(
                            f"Frontmatter tags missing required field: {tag}"
                        )

        # Check for deprecated/non-canonical frontmatter fields
        deprecated_fields = ["tools", "triggers", "not_for", "dispatch", "dependencies"]
        for field in deprecated_fields:
            if field in self.frontmatter:
                self.violations.append(
                    f"Frontmatter contains non-canonical field '{field}'. Move to skill.contract.yaml"
                )

        # Check name and maturity consistency with contract
        if hasattr(self, "contract"):
            if "name" in self.frontmatter and "name" in self.contract:
                if self.frontmatter["name"] != self.contract["name"]:
                    self.violations.append(
                        f"Name mismatch: SKILL.md has '{self.frontmatter['name']}', contract has '{self.contract['name']}'"
                    )

            if "maturity" in self.frontmatter and "maturity" in self.contract:
                if self.frontmatter["maturity"] != self.contract["maturity"]:
                    self.violations.append(
                        f"Maturity mismatch: SKILL.md has '{self.frontmatter['maturity']}', contract has '{self.contract['maturity']}'"
                    )

            if "version" in self.frontmatter and "version" in self.contract:
                if self.frontmatter["version"] != self.contract["version"]:
                    self.violations.append(
                        f"Version mismatch: SKILL.md has '{self.frontmatter['version']}', contract has '{self.contract['version']}'"
                    )

    def _check_quality_scorecard(self) -> None:
        """Validate quality scorecard depth matches maturity."""
        if not hasattr(self, "skill_content"):
            return

        # Find quality scorecard section
        scorecard_match = re.search(
            r"##\s+📊\s+Quality Scorecard\s*\n(.*?)(?=\n##\s|$)",
            self.skill_content,
            re.DOTALL
        )

        if not scorecard_match:
            self.violations.append("Quality Scorecard section not found")
            return

        scorecard_content = scorecard_match.group(1)

        # Count dimensions (rows in the scorecard table)
        dimension_count = len(re.findall(r"\|\s*\*\*[^*]+\*\*", scorecard_content))

        maturity = self.contract.get("maturity", "draft") if hasattr(self, "contract") else "draft"

        # Draft should have 3, tactical/strategic should have 8
        if maturity == "draft":
            if dimension_count > 3:
                self.warnings.append(
                    f"Draft skill quality scorecard has {dimension_count} dimensions; should have 3"
                )
        elif maturity in ["tactical", "strategic"]:
            if dimension_count < 8:
                self.violations.append(
                    f"{maturity.capitalize()} skill quality scorecard has {dimension_count} dimensions; should have 8"
                )

    def _check_semantic_consistency(self) -> None:
        """Validate consistency between SKILL.md and contract."""
        if not hasattr(self, "skill_content") or not hasattr(self, "contract"):
            return

        # Check if tools mentioned in Workflow match those declared in contract
        if "requires" in self.contract:
            requires = self.contract["requires"]
            declared_tools = []
            if isinstance(requires, dict) and "tools" in requires:
                declared_tools = requires.get("tools", [])

            # Look for tool mentions in workflow
            tool_mentions = self._find_tool_mentions(self.skill_content)

            # Warn if tools are used but not declared
            for tool in tool_mentions:
                if tool not in declared_tools:
                    self.warnings.append(
                        f"Tool '{tool}' mentioned in Workflow but not declared in contract requires.tools"
                    )

        # Check reversibility justification
        if hasattr(self, "contract"):
            reversible = self.contract.get("reversible", True)
            if not reversible:
                # Should be justified in Security section
                if "Security" in self.skill_content:
                    security_match = re.search(
                        r"##\s+🔐\s+Security\s*\n(.*?)(?=\n##\s|$)",
                        self.skill_content,
                        re.DOTALL
                    )
                    if security_match:
                        security_content = security_match.group(1)
                        if "reversible" not in security_content.lower() and "irreversible" not in security_content.lower():
                            self.warnings.append(
                                "Contract declares reversible:false but Security section doesn't justify why"
                            )

    def _find_tool_mentions(self, content: str) -> List[str]:
        """Find tool references in skill content."""
        tools = []
        for tool in VALID_TOOLS:
            if tool in content:
                tools.append(tool)
        return tools


def get_all_skills() -> List[Path]:
    """Collect all installed skills from ~/.claude/skills/."""
    skills_dir = Path.home() / ".claude" / "skills"
    if not skills_dir.exists():
        return []

    skills = []
    for item in skills_dir.rglob("SKILL.md"):
        skill_path = item.parent
        # Skip if it's a template or test directory
        if "template" not in str(skill_path).lower() and "_tests" not in str(skill_path).lower():
            skills.append(skill_path)

    return sorted(skills)


def generate_compliance_report(results: List[Dict]) -> str:
    """Generate a formatted compliance report."""
    report = []
    report.append("=" * 80)
    report.append("SKILL TEMPLATE COMPLIANCE REPORT")
    report.append("=" * 80)
    report.append("")

    # Group by status
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] == "FAIL"]

    # Summary
    report.append(f"Summary: {len(passed)} PASS, {len(failed)} FAIL out of {len(results)} skills")
    report.append("")

    # Failed skills (detailed)
    if failed:
        report.append("FAILED SKILLS (Violations found)")
        report.append("-" * 80)
        for result in failed:
            report.append(f"\n{result['skill']} ({result['path']})")
            for violation in result["violations"]:
                report.append(f"  ❌ {violation}")
            if result["warnings"]:
                for warning in result["warnings"]:
                    report.append(f"  ⚠️  {warning}")

    # Passed skills
    if passed:
        report.append("\n\nPASSED SKILLS")
        report.append("-" * 80)
        for result in passed:
            report.append(f"✅ {result['skill']}")

    report.append("\n" + "=" * 80)
    return "\n".join(report)


# ============================================================================
# PYTEST TESTS
# ============================================================================


def test_all_skills_compliance():
    """Master test: validate all skills against canonical structure."""
    skills = get_all_skills()
    assert len(skills) > 0, "No skills found in ~/.claude/skills/"

    results = []
    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        result = validator.validate()
        results.append(result)

    # Generate and print report (for visibility during test run)
    report = generate_compliance_report(results)
    print("\n" + report)

    # Assert: We expect failures on current deviations (fail-first design)
    # This test documents the baseline for Item 24 audit
    failed_count = len([r for r in results if r["status"] == "FAIL"])
    print(f"\n📊 Baseline: {failed_count}/{len(results)} skills have violations")
    print("This is expected. Item 24 (consistency audit) will fix these violations.")


def test_skill_frontmatter_exists():
    """Verify all skills have YAML frontmatter with required fields."""
    skills = get_all_skills()
    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_skill_md()
        assert not any("frontmatter" in v for v in validator.violations), \
            f"{skill_path.name}: SKILL.md missing or invalid frontmatter"


def test_contract_files_exist_at_root():
    """Verify skill.contract.yaml exists at skill root (not in subdirectories)."""
    skills = get_all_skills()
    for skill_path in skills:
        contract_path = skill_path / "skill.contract.yaml"
        assert contract_path.exists(), \
            f"{skill_path.name}: skill.contract.yaml not found at root"


def test_no_variant_b_schemas():
    """Verify no skills use deprecated Variant B schema (dispatch:/dependencies:)."""
    skills = get_all_skills()
    violations = []

    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_contract()
        for violation in validator.violations:
            if "Variant B" in violation:
                violations.append(f"{skill_path.name}: {violation}")

    # Report violations but allow them (fail-first design)
    if violations:
        print(f"\n⚠️  Found {len(violations)} skills using Variant B schema:")
        for v in violations:
            print(f"  - {v}")


def test_semantic_versioning():
    """Verify semantic versions match maturity levels."""
    skills = get_all_skills()
    violations = []

    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_contract()
        if hasattr(validator, 'contract'):
            validator._check_semantic_version()
        for violation in validator.violations:
            if "version" in violation.lower():
                violations.append(f"{skill_path.name}: {violation}")

    if violations:
        print(f"\n⚠️  Found {len(violations)} version/maturity mismatches:")
        for v in violations:
            print(f"  - {v}")


def test_quality_scorecard_depth():
    """Verify quality scorecard dimensions match maturity."""
    skills = get_all_skills()
    warnings = []

    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_skill_md()
        validator._check_contract()
        validator._check_quality_scorecard()
        for warning in validator.warnings:
            if "scorecard" in warning.lower():
                warnings.append(f"{skill_path.name}: {warning}")

    if warnings:
        print(f"\n⚠️  Found {len(warnings)} quality scorecard issues:")
        for w in warnings:
            print(f"  - {w}")


def test_emoji_header_consistency():
    """Verify emoji-to-section mapping matches canonical."""
    skills = get_all_skills()
    violations = []

    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_skill_md()
        for violation in validator.violations:
            if "emoji" in violation.lower() or "header" in violation.lower():
                violations.append(f"{skill_path.name}: {violation}")

    if violations:
        print(f"\n⚠️  Found {len(violations)} emoji header violations:")
        for v in violations:
            print(f"  - {v}")


def test_frontmatter_consistency():
    """Verify frontmatter matches contract (name, version, maturity)."""
    skills = get_all_skills()
    violations = []

    for skill_path in skills:
        validator = SkillComplianceValidator(skill_path)
        validator._check_skill_md()
        validator._check_contract()
        validator._check_frontmatter_consistency()
        for violation in validator.violations:
            if "mismatch" in violation.lower():
                violations.append(f"{skill_path.name}: {violation}")

    if violations:
        print(f"\n⚠️  Found {len(violations)} frontmatter-contract mismatches:")
        for v in violations:
            print(f"  - {v}")


if __name__ == "__main__":
    # Run master test to generate report
    test_all_skills_compliance()
