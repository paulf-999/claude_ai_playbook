"""Tests for audit_scoring_handler: scoring functions, validation, audit trail.

Validates: config validation, dimension scoring, grade calculation, JSON trail.
"""

import pytest
import json
from pathlib import Path
from audit_scoring_handler import (
    validate_config,
    score_testing,
    score_security,
    score_documentation,
    score_standards,
    calculate_overall_grade,
    audit_claude_config,
    MIN_SCORE,
)


class TestValidation:
    """Test config validation."""

    def test_validate_config_missing_directory(self):
        """Config validation fails for non-existent directory."""
        result = validate_config("/nonexistent/path/.claude")
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_config_file_instead_of_dir(self, tmp_path):
        """Config validation fails if path is a file, not directory."""
        fake_file = tmp_path / "fake_config"
        fake_file.write_text("test")
        result = validate_config(str(fake_file))
        assert result["valid"] is False

    def test_validate_config_missing_required_files(self, tmp_path):
        """Config validation detects missing required files."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        result = validate_config(str(config_dir))
        assert result["valid"] is False
        assert "CLAUDE.md" in str(result["errors"])

    def test_validate_config_with_required_files(self, tmp_path):
        """Config validation passes with required files."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = validate_config(str(config_dir))
        assert result["valid"] is True


class TestScoringFunctions:
    """Test individual dimension scoring functions."""

    def test_score_testing_no_tests(self, tmp_path):
        """Testing score is minimal when no _tests/ directory exists."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        score, reasoning, issues = score_testing(str(config_dir))
        assert score == MIN_SCORE
        assert "test" in reasoning.lower()
        assert len(issues) > 0

    def test_score_testing_with_tests(self, tmp_path):
        """Testing score increases with test files."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        tests_dir = config_dir / "_tests"
        tests_dir.mkdir()
        # Create test files
        (tests_dir / "test_foo.py").write_text("def test_foo(): pass")
        (tests_dir / "test_bar.py").write_text("def test_bar(): pass")

        score, reasoning, issues = score_testing(str(config_dir))
        assert score > MIN_SCORE
        assert "test" in reasoning.lower()

    def test_score_security_no_rules(self, tmp_path):
        """Security score is minimal without security rules."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        score, reasoning, issues = score_security(str(config_dir))
        assert score == MIN_SCORE
        assert "security" in reasoning.lower()
        assert len(issues) > 0

    def test_score_security_with_rules(self, tmp_path):
        """Security score increases with security rules."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        rules_dir = config_dir / "_rules"
        rules_dir.mkdir()
        (rules_dir / "security.md").write_text("# Security Rule")

        score, reasoning, issues = score_security(str(config_dir))
        assert score > MIN_SCORE

    def test_score_documentation_with_claude_md(self, tmp_path):
        """Documentation score increases with CLAUDE.md."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config\n" * 100)  # >500 chars

        score, reasoning, issues = score_documentation(str(config_dir))
        assert score > MIN_SCORE
        assert "documentation" in reasoning.lower()

    def test_score_standards_with_dir_structure(self, tmp_path):
        """Standards score increases with proper directory structure."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "_rules").mkdir()
        (config_dir / "skills").mkdir()
        (config_dir / "memory").mkdir()

        score, reasoning, issues = score_standards(str(config_dir))
        assert score > MIN_SCORE
        assert "standards" in reasoning.lower()


class TestGradeCalculation:
    """Test overall grade calculation."""

    def test_calculate_grade_excellent(self):
        """Average 9+ = A grade."""
        scores = {"testing": 9, "security": 10, "documentation": 9, "standards": 9}
        grade = calculate_overall_grade(scores)
        assert grade == "A"

    def test_calculate_grade_good(self):
        """Average 8-8.9 = B grade."""
        scores = {"testing": 8, "security": 8, "documentation": 8, "standards": 8}
        grade = calculate_overall_grade(scores)
        assert grade == "B"

    def test_calculate_grade_acceptable(self):
        """Average 7-7.9 = C grade."""
        scores = {"testing": 7, "security": 7, "documentation": 7, "standards": 7}
        grade = calculate_overall_grade(scores)
        assert grade == "C"

    def test_calculate_grade_poor(self):
        """Average 1-5 = F grade."""
        scores = {"testing": 1, "security": 2, "documentation": 1, "standards": 2}
        grade = calculate_overall_grade(scores)
        assert grade == "F"

    def test_calculate_grade_empty(self):
        """Empty scores = F grade."""
        grade = calculate_overall_grade({})
        assert grade == "F"


class TestAuditOrchestration:
    """Test full audit orchestration."""

    def test_audit_missing_config(self):
        """Audit fails gracefully for missing config."""
        result = audit_claude_config(
            config_path="/nonexistent/path/.claude",
            save_trail=False
        )
        assert result["success"] is False
        assert len(result["errors"]) > 0

    def test_audit_valid_config_no_trail(self, tmp_path):
        """Audit succeeds with valid config, no trail saved."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        # Create minimal required files
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(
            config_path=str(config_dir),
            save_trail=False
        )
        assert result["success"] is True
        assert "overall_grade" in result["result"]
        assert "dimension_scores" in result["result"]
        assert len(result["result"]["dimension_scores"]) == 4

    def test_audit_produces_grade(self, tmp_path):
        """Audit produces valid grade (A-F)."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(config_path=str(config_dir), save_trail=False)
        grade = result["result"]["overall_grade"]
        assert grade in ["A", "B", "C", "D", "F"]

    def test_audit_saves_json_trail(self, tmp_path):
        """Audit saves JSON trail to file."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(
            config_path=str(config_dir),
            save_trail=True,
            trail_dir=str(tmp_path / "_audits")
        )
        assert result["success"] is True
        assert "trail_path" in result["result"]

        # Verify JSON file exists and is valid
        trail_path = Path(result["result"]["trail_path"])
        assert trail_path.exists()
        trail_data = json.loads(trail_path.read_text())
        assert "overall_grade" in trail_data
        assert "dimension_scores" in trail_data

    def test_audit_includes_timestamp(self, tmp_path):
        """Audit result includes timestamp for reproducibility."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(config_path=str(config_dir), save_trail=False)
        assert "timestamp" in result["result"]
        # Verify timestamp format (ISO)
        assert "T" in result["result"]["timestamp"]

    def test_audit_collects_all_issues(self, tmp_path):
        """Audit collects issues from all dimensions."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(config_path=str(config_dir), save_trail=False)
        # Should have some issues (no tests, minimal security, etc.)
        assert "all_issues" in result["result"]


class TestAuditReproducibility:
    """Test that audits are reproducible and auditable."""

    def test_audit_deterministic(self, tmp_path):
        """Same config produces same scores (deterministic)."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result1 = audit_claude_config(config_path=str(config_dir), save_trail=False)
        result2 = audit_claude_config(config_path=str(config_dir), save_trail=False)

        assert result1["result"]["dimension_scores"] == result2["result"]["dimension_scores"]
        assert result1["result"]["overall_grade"] == result2["result"]["overall_grade"]

    def test_audit_trail_includes_reasoning(self, tmp_path):
        """Audit trail includes reasoning for each score."""
        config_dir = tmp_path / ".claude"
        config_dir.mkdir()
        (config_dir / "CLAUDE.md").write_text("# Config")
        (config_dir / "_rules").mkdir()
        (config_dir / "memory").mkdir()
        (config_dir / "memory" / "MEMORY.md").write_text("# Memory")
        (config_dir / "aliases.md").write_text("# Aliases")
        (config_dir / "settings.json").write_text("{}")

        result = audit_claude_config(config_path=str(config_dir), save_trail=False)
        assert "dimension_reasoning" in result["result"]
        # Each dimension should have reasoning
        for dimension in ["testing", "security", "documentation", "standards"]:
            assert dimension in result["result"]["dimension_reasoning"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
