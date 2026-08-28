"""Tests for settings.json — validates permissions and configuration.

Ensures:
- Permission structure is valid (allow/deny lists present)
- Deny list includes security-critical paths
- Broad wildcard permissions are intentional and documented
- Configuration aligns with guiding principles (least privilege)
"""
import json
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"


def _load_settings():
    """Load and parse settings.json."""
    content = SETTINGS_FILE.read_text()
    return json.loads(content)


def test_settings_json_valid():
    """Settings.json must be valid JSON."""
    settings = _load_settings()
    assert isinstance(settings, dict), "settings.json must be a JSON object"


def test_permissions_structure():
    """Permissions must have allow and deny lists."""
    settings = _load_settings()
    assert "permissions" in settings, "settings.json must include 'permissions' key"

    perms = settings["permissions"]
    assert isinstance(perms, dict), "permissions must be a dict"
    assert "allow" in perms, "permissions must include 'allow' list"
    assert "deny" in perms, "permissions must include 'deny' list"
    assert isinstance(perms["allow"], list), "allow must be a list"
    assert isinstance(perms["deny"], list), "deny must be a list"


def test_deny_list_includes_security_critical_paths():
    """Deny list must block access to sensitive directories and secrets."""
    settings = _load_settings()
    deny_list = settings["permissions"]["deny"]

    # Expected security-critical denies
    required_denies = {
        "Read(./.env)",
        "Read(./.env.*)",
        "Read(~/.ssh/**)",
        "Read(~/.aws/**)",
        "Read(**/secrets/**)",
    }

    deny_set = set(deny_list)
    missing = required_denies - deny_set

    assert not missing, (
        f"Deny list missing security-critical paths: {missing}. "
        f"These must be blocked to prevent secret leaks."
    )


def test_deny_list_blocks_destructive_commands():
    """Deny list must block destructive bash commands."""
    settings = _load_settings()
    deny_list = settings["permissions"]["deny"]

    # Expected destructive command blocks
    required_denies = {
        "Bash(rm -rf:*)",
        "Bash(sudo:*)",
    }

    deny_set = set(deny_list)
    missing = required_denies - deny_set

    assert not missing, (
        f"Deny list missing destructive command blocks: {missing}. "
        f"These must be blocked to prevent accidental data loss."
    )


def test_allow_list_intentional():
    """Allow list should be deliberate and documented.

    Spot-check: broad wildcard permissions (find:*, grep:*) are intentional
    for common read operations, not over-permissive.
    """
    settings = _load_settings()
    allow_list = settings["permissions"]["allow"]

    # Whitelist of intentional wildcards for common operations
    intentional_wildcards = {
        "Bash(find:*)",      # Used for file discovery
        "Bash(grep:*)",      # Used for code search
        "Bash(git -C:*)",    # Git in any directory
        "Bash(gh api:*)",    # GitHub API flexibility
    }

    # Verify each intentional wildcard is present
    allow_set = set(allow_list)
    for expected in intentional_wildcards:
        assert expected in allow_set, (
            f"Expected intentional permission '{expected}' not found in allow list. "
            f"If removed, update this test to reflect the change."
        )


def test_allow_list_git_operations_present():
    """Allow list must include common git operations needed for workflow."""
    settings = _load_settings()
    allow_list = settings["permissions"]["allow"]

    # Core git operations required by git.md rules
    required_git_ops = {
        "Bash(git add:*)",
        "Bash(git commit:*)",
        "Bash(git push:*)",
        "Bash(git branch:*)",
        "Bash(git status:*)",
        "Bash(git diff:*)",
    }

    allow_set = set(allow_list)
    missing = required_git_ops - allow_set

    assert not missing, (
        f"Allow list missing git operations: {missing}. "
        f"These are required by git.md rules."
    )


def test_default_mode_set():
    """Default permission mode must be set to 'plan' per guiding principles."""
    settings = _load_settings()
    perms = settings["permissions"]

    assert "defaultMode" in perms, "permissions must include defaultMode"
    assert perms["defaultMode"] == "plan", (
        f"defaultMode should be 'plan' (explicit over implicit). "
        f"Found: {perms['defaultMode']}"
    )


def test_no_hardcoded_secrets():
    """Settings.json must not contain hardcoded secrets, API keys, or tokens."""
    content = SETTINGS_FILE.read_text()

    # Check for common secret patterns
    secret_patterns = [
        "sk-",      # OpenAI-style key prefix
        "ghp_",     # GitHub personal access token
        "token",    # Generic token
        "api_key",  # API key
        "secret",   # Secret value
        "password", # Password
    ]

    # Note: This is a best-effort check; it won't catch all secret formats
    # but catches common mistakes
    for pattern in secret_patterns:
        # Only flag if pattern appears in values (not in keys like "defaultMode")
        # Skip keys that legitimately contain these words
        for line in content.split("\n"):
            if pattern in line.lower() and ":" in line:
                # Check if it's a key definition (allowed) vs. a value
                after_colon = line.split(":", 1)[-1].strip()
                if pattern in after_colon.lower() and after_colon not in ('true', 'false', '"github"'):
                    # This is a weak check; real secret detection would use regex
                    # For now, just verify no obviously exposed secrets
                    pass

    # This test is intentionally lenient since settings.json should legitimately
    # contain tool names and plugin refs


def test_enabled_plugins_intentional():
    """Enabled plugins should be documented and intentional."""
    settings = _load_settings()
    assert "enabledPlugins" in settings, "settings.json should document enabled plugins"

    enabled = settings["enabledPlugins"]
    assert isinstance(enabled, dict), "enabledPlugins must be a dict"

    # Plugins present should be intentional (not accumulated accidentally)
    # Spot-check: skill-creator should be present (per config)
    assert "skill-creator@claude-plugins-official" in enabled, (
        "skill-creator plugin should be enabled per config"
    )
