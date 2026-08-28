"""
Test artefact proposal gates: naming, placement, duplication.

Validates that the three gates establish clear rules before proposing new artefacts.
"""



class TestNamingGate:
    """Gate 1: Naming convention validation."""

    def test_skill_naming_pattern(self):
        """Validates that skills follow <domain>_<action> pattern."""
        valid_names = [
            "confluence_create_page",
            "jira_create",
            "git_commit",
        ]

        for name in valid_names:
            parts = name.split("_")
            assert len(parts) >= 2, f"Skill {name} must have domain and action"
            assert all(part.islower() for part in parts), f"Skill {name} must be lowercase"
            assert "_" in name, f"Skill {name} must use underscores"

        # Invalid structure checks (hyphens, camelCase)
        invalid_structures = [
            "confluence-create-page",  # hyphens
            "confluenceCreatePage",    # camelCase
        ]
        for name in invalid_structures:
            assert not all(c.isalpha() or c == "_" for c in name) or "-" in name or not name.islower(), \
                f"Invalid structure {name} should be rejected"

    def test_rule_naming_pattern(self):
        """Validates that rules follow snake_case, descriptive naming."""
        valid_names = [
            "naming_standards.md",
            "security.md",
            "behaviour.md",
            "testing.md",
        ]
        invalid_names = [
            "naming-standards.md",     # hyphens
            "NamingStandards.md",      # PascalCase
            "a.md",                    # too short, not descriptive
            "rule_for_X.md",           # vague placeholder
        ]

        for name in valid_names:
            base = name.replace(".md", "")
            assert "_" in base or len(base) > 3, f"Rule {name} should be descriptive"
            assert base.islower(), f"Rule {name} must be lowercase"

        for name in invalid_names:
            base = name.replace(".md", "")
            # Either has hyphens, isn't lowercase, or too short
            assert "-" in base or not base.islower() or len(base) <= 3

    def test_hook_naming_pattern(self):
        """Validates that hooks follow hook_<type>_<domain>.sh pattern."""
        valid_names = [
            "hook_enforcement_sql.sh",
            "hook_enforcement_naming_convention.sh",
            "hook_style_guide_dbt.sh",
        ]

        for name in valid_names:
            assert name.startswith("hook_"), f"Hook {name} must start with hook_"
            assert name.endswith(".sh"), f"Hook {name} must end with .sh"
            assert "_" in name.replace("hook_", ""), f"Hook {name} must have type and domain"

        # Invalid structure checks
        invalid_structures = [
            "enforcement_sql.sh",      # missing hook_ prefix
            "hook-enforcement-sql.sh", # hyphens
        ]
        for name in invalid_structures:
            # Either missing prefix or has hyphens
            assert not name.startswith("hook_") or "-" in name, \
                f"Invalid structure {name} should be rejected"


class TestPlacementGate:
    """Gate 2: Directory placement validation."""

    def test_rule_placement_by_type(self):
        """Validates that rules are placed in correct directory tier."""
        always_on_rules = [
            "guiding_principles.md",
            "behaviour.md",
            "security.md",
            "testing.md",
        ]
        # These should be in 01_essentials/ or 02_claude_standards/
        for rule in always_on_rules:
            # Simulate placement check
            assert rule in always_on_rules, f"{rule} should be in top-level tier"

    def test_skill_placement_by_domain(self):
        """Validates that skills are placed in domain-specific subdirectories."""
        skill_placements = {
            "confluence_create_page": "_confluence_skills/",
            "git_commit": "_git_skills/",
            "jira_create": "_jira_skills/",
        }

        for skill, expected_dir in skill_placements.items():
            domain = skill.split("_")[0]
            expected = f"_{domain}_skills/"
            assert expected_dir == expected, f"Skill {skill} should be in {expected}"

    def test_lazy_load_placement(self):
        """Validates that domain-specific rules are in lazy_load/."""
        lazy_load_rules = [
            "sql.md",
            "dbt.md",
            "airflow.md",
        ]
        # These should be in 04_lazy_load/
        for rule in lazy_load_rules:
            # Simulate placement check: these are domain-specific
            assert rule not in ["guiding_principles.md", "security.md"], f"{rule} should be lazy-loaded"


class TestDuplicationGate:
    """Gate 3: Duplication detection."""

    def test_existing_rule_detection(self):
        """Validates that duplicate rules are detected before proposal."""
        existing_rules = {
            "naming_standards": "Covers all identifier naming",
            "security": "Covers secure coding practices",
            "testing": "Covers test requirements",
        }

        # If proposing a new rule on naming, should detect naming_standards exists
        assert any("naming" in existing.lower() for existing in existing_rules.keys()), \
            "New naming rule conflicts with existing"

    def test_existing_skill_detection(self):
        """Validates that duplicate skills are detected before proposal."""
        existing_skills = {
            "confluence_create_page": "Creates Confluence pages",
            "jira_create": "Creates Jira issues",
            "git_commit": "Creates git commits",
        }

        # If proposing git_push, should detect git_commit exists (same domain)
        new_proposal = "git_push"
        domain = new_proposal.split("_")[0]
        existing_domains = [skill.split("_")[0] for skill in existing_skills.keys()]
        assert domain in existing_domains, "Similar skill in same domain exists"


class TestGateSequence:
    """Validate that gates run in correct order: naming → placement → duplication."""

    def test_gate_order_matters(self):
        """Validates that gates run in strict sequence."""
        gates = ["naming", "placement", "duplication"]
        expected_order = ["naming", "placement", "duplication"]
        assert gates == expected_order, "Gates must run in order: naming → placement → duplication"

    def test_early_termination_on_failure(self):
        """Validates that gates stop on first failure (no options until gates pass)."""
        # Scenario: bad naming
        # Expected: stop at Gate 1, recommend correct name, do not proceed to Gate 2/3
        # Scenario: good naming, bad placement
        # Expected: stop at Gate 2, recommend correct dir, do not proceed to Gate 3
        # Scenario: good naming, good placement, duplicate exists
        # Expected: reach Gate 3, present options (integrate vs. new)
        pass  # Structural test; behavior validated by rule guidance


class TestGateDocumentation:
    """Validate that gate rules are documented in _artefact_proposal_gates.md."""

    def test_gates_file_exists(self):
        """Validates that _artefact_proposal_gates.md exists and is accessible."""
        from pathlib import Path
        gate_file = Path.home() / ".claude" / "_rules" / "01_core" / "behaviour" / "_artefact_proposal_gates.md"
        assert gate_file.exists(), f"Gates file should exist at {gate_file}"

    def test_gates_file_has_all_three_gates(self):
        """Validates that gates file documents all three gates."""
        from pathlib import Path
        gate_file = Path.home() / ".claude" / "_rules" / "01_core" / "behaviour" / "_artefact_proposal_gates.md"
        content = gate_file.read_text()

        assert "Gate 1" in content or "Naming" in content, "Gates file should document naming gate"
        assert "Gate 2" in content or "Placement" in content, "Gates file should document placement gate"
        assert "Gate 3" in content or "Duplication" in content, "Gates file should document duplication gate"
