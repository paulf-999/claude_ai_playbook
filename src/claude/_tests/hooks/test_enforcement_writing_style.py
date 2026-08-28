"""
Test: enforcement_markdown_file_locations hook

Validates that markdown files written to ~/.claude/ follow writing_style.md conventions.
- Drafts: ~/.claude/_drafts/<domain>/YYYY-MM-DD_<topic>.md
- Errors: ~/.claude/_errors/<domain>/YYYY-MM-DD_<topic>.md
- Reference: ~/.claude/_reference/<topic>.md
- Sessions: ~/.claude/_sessions/YYYY-MM-DD_<domain>_<topic>.md

Mode: blocking (returns exit code 1 for invalid paths)
"""

import subprocess
from pathlib import Path


HOOK_PATH = Path.home() / ".claude" / "hooks" / "enforcement_writing_style.sh"


def run_hook(file_path):
    """Run the hook and return exit code."""
    result = subprocess.run(
        [str(HOOK_PATH), str(file_path)],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stderr


class TestMarkdownFileLocationHook:
    """Test the markdown file location enforcement hook."""

    def test_valid_draft_path(self):
        """Valid drafts should exit 0 (no warning)."""
        path = f"{Path.home()}/.claude/_drafts/jira/2026-08-19_dm43319_root_cause.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for valid draft, got {code}\nStderr: {stderr}"

    def test_valid_error_path(self):
        """Valid error paths should exit 0."""
        path = f"{Path.home()}/.claude/_errors/general/2026-08-19_failed_operation.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for valid error, got {code}"

    def test_valid_reference_path(self):
        """Valid reference paths (no date) should exit 0."""
        path = f"{Path.home()}/.claude/_reference/claude_code_automation.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for valid reference, got {code}"

    def test_valid_session_path(self):
        """Valid session paths should exit 0."""
        path = f"{Path.home()}/.claude/_sessions/2026-08-19_data_platform_planning.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for valid session, got {code}"

    def test_exempt_claude_config(self):
        """CLAUDE.md config files should be exempt."""
        path = f"{Path.home()}/.claude/CLAUDE.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for exempt CLAUDE.md, got {code}"

    def test_exempt_memory_index(self):
        """MEMORY.md should be exempt."""
        path = f"{Path.home()}/.claude/memory/MEMORY.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for exempt MEMORY.md, got {code}"

    def test_exempt_skill_documentation(self):
        """Skill SKILL.md files should be exempt."""
        path = f"{Path.home()}/.claude/skills/_git_skills/git_create_pr/SKILL.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for exempt skill SKILL.md, got {code}"

    def test_exempt_rules_readme(self):
        """Rules README.md files should be exempt."""
        path = f"{Path.home()}/.claude/_rules/01_core/README.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Expected exit 0 for exempt rules README, got {code}"

    def test_invalid_path_in_root(self):
        """Random .md files in ~/.claude/ root should be blocked."""
        path = f"{Path.home()}/.claude/random_note.md"
        code, stderr = run_hook(path)
        assert code == 1, f"Hook should block invalid path (exit 1), got {code}"
        assert "❌" in stderr, f"Expected error marker in stderr:\n{stderr}"
        assert "writing_style.md" in stderr, "Expected reference to writing_style.md"

    def test_invalid_draft_missing_domain(self):
        """Draft without domain should be blocked."""
        path = f"{Path.home()}/.claude/_drafts/2026-08-19_topic.md"
        code, stderr = run_hook(path)
        assert code == 1, "Hook should block invalid path (exit 1)"
        assert "❌" in stderr

    def test_invalid_draft_wrong_date_format(self):
        """Draft with wrong date format should be blocked."""
        path = f"{Path.home()}/.claude/_drafts/jira/08-19-2026_topic.md"
        code, stderr = run_hook(path)
        assert code == 1, "Hook should block invalid path (exit 1)"
        assert "❌" in stderr

    def test_non_markdown_ignored(self):
        """Non-.md files should be ignored (exit 0)."""
        path = f"{Path.home()}/.claude/some_script.sh"
        code, stderr = run_hook(path)
        assert code == 0, "Non-.md files should be ignored"
        assert stderr == "", "Should not warn for non-.md files"

    def test_non_claude_directory_ignored(self):
        """Files outside ~/.claude/ should be ignored."""
        path = f"{Path.home()}/some_file.md"
        code, stderr = run_hook(path)
        assert code == 0, "Files outside ~/.claude/ should be ignored"
        assert stderr == "", "Should not warn for files outside ~/.claude/"

    # New blocking behavior tests

    def test_invalid_draft_missing_underscore_prefix(self):
        """Draft written to 'drafts/' (no underscore) should be BLOCKED."""
        path = f"{Path.home()}/.claude/drafts/jira/2026-08-19_dm43319_root_cause.md"
        code, stderr = run_hook(path)
        assert code == 1, f"Hook MUST block invalid path (missing underscore), got exit {code}"
        assert "❌" in stderr, f"Expected error marker in stderr:\n{stderr}"
        assert "drafts/" in stderr or "_drafts/" in stderr, "Error should mention correct path"

    def test_invalid_error_missing_underscore_prefix(self):
        """Error path written to 'errors/' (no underscore) should be BLOCKED."""
        path = f"{Path.home()}/.claude/errors/general/2026-08-19_failed.md"
        code, stderr = run_hook(path)
        assert code == 1, "Hook MUST block invalid path (missing underscore)"
        assert "❌" in stderr

    def test_valid_1on1_domain(self):
        """Draft with '1on1' domain (contains digit) should be ALLOWED."""
        path = f"{Path.home()}/.claude/_drafts/1on1/2026-08-19_meeting_prep.md"
        code, stderr = run_hook(path)
        assert code == 0, f"Hook should allow 1on1 domain, got exit {code}\nStderr: {stderr}"

    def test_valid_all_draft_domains(self):
        """Draft paths with all valid domains should be ALLOWED."""
        domains = [
            "1on1", "confluence", "email", "general", "important",
            "jira", "meetings", "plans", "reference", "teams",
        ]
        for domain in domains:
            path = f"{Path.home()}/.claude/_drafts/{domain}/2026-08-19_test.md"
            code, stderr = run_hook(path)
            assert code == 0, f"Hook should allow domain '{domain}', got exit {code}\nStderr: {stderr}"

    def test_invalid_domain_in_draft(self):
        """Draft with invalid domain should be BLOCKED."""
        path = f"{Path.home()}/.claude/_drafts/invalid_domain/2026-08-19_topic.md"
        code, stderr = run_hook(path)
        assert code == 1, "Hook should block invalid domain"
        assert "❌" in stderr

    def test_valid_error_all_domains(self):
        """Error paths with valid domains should be ALLOWED."""
        domains = ["confluence", "email", "general", "important", "jira"]
        for domain in domains:
            path = f"{Path.home()}/.claude/_errors/{domain}/2026-08-19_error.md"
            code, stderr = run_hook(path)
            assert code == 0, f"Hook should allow error with domain '{domain}', got exit {code}"

    def test_exempt_readme_in_rules(self):
        """README files anywhere in _rules/ should be ALLOWED."""
        path = f"{Path.home()}/.claude/_rules/README.md"
        code, stderr = run_hook(path)
        assert code == 0, "Hook should allow README.md in _rules"

    def test_exempt_rules_all_paths(self):
        """Any .md file in _rules/ should be ALLOWED (rules are exempt)."""
        path = f"{Path.home()}/.claude/_rules/01_core/writing_style.md"
        code, stderr = run_hook(path)
        assert code == 0, "Hook should allow .md files anywhere in _rules"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
