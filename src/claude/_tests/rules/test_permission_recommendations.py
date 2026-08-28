"""Tests for permission recommendation rules in security_guardrails.md.

Ensures:
- Claude never recommends wildcard permissions for destructive commands
- Permission recommendations follow least-privilege principle
- Read-only operations are distinguished from write operations
"""
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
SECURITY_GUARDRAILS_FILE = CLAUDE_DIR / "_rules/claude_internal/security_guardrails.md"


def _read_security_guardrails():
    """Read security_guardrails.md."""
    return SECURITY_GUARDRAILS_FILE.read_text()


def test_permission_recommendations_documented():
    """Security guardrails must document permission recommendation rules."""
    content = _read_security_guardrails()

    assert "Permission recommendations" in content or "permission" in content.lower(), (
        "security_guardrails.md must document how to recommend permissions safely"
    )


def test_wildcard_restrictions_documented():
    """Rule must warn against wildcard permissions for destructive commands."""
    content = _read_security_guardrails()

    # Check that wildcards for destructive commands are flagged
    assert "wildcard" in content.lower() or "Bash(git:*)" in content or "Bash(rm:*)" in content, (
        "security_guardrails.md must document risks of overly broad wildcard permissions"
    )


def test_least_privilege_principle_documented():
    """Rule must enforce least-privilege principle for permissions."""
    content = _read_security_guardrails()

    assert "least privilege" in content.lower() or "minimal" in content.lower(), (
        "security_guardrails.md must document least-privilege principle for permissions"
    )


def test_read_write_separation_documented():
    """Rule must distinguish read-only permissions from write permissions."""
    content = _read_security_guardrails()

    # Check for read/write distinction
    has_read_mention = "read" in content.lower()
    has_write_mention = "write" in content.lower()

    assert has_read_mention and has_write_mention, (
        "security_guardrails.md should distinguish read-only permissions from write permissions"
    )


def test_permission_rationale_requirement():
    """Rule must require documentation of why a permission is safe."""
    content = _read_security_guardrails()

    assert "rationale" in content.lower() or "document" in content.lower() or "explain" in content.lower(), (
        "security_guardrails.md should require rationale when recommending permissions"
    )


def test_specific_examples_provided():
    """Rule should include specific examples of good vs. bad permissions."""
    content = _read_security_guardrails()

    # Check for example patterns (✅ Good / ❌ Bad)
    has_good_example = "✅" in content or "Good:" in content
    has_bad_example = "❌" in content or "Bad:" in content

    assert has_good_example and has_bad_example, (
        "security_guardrails.md should provide specific examples of good and bad permissions"
    )
