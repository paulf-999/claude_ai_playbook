# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           1.2.1
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for settings.json — validates permissions and configuration.

Ensures:
- Permission structure is valid (allow/deny lists present)
- Deny list includes security-critical paths
- Broad wildcard permissions are intentional and documented
- Configuration aligns with guiding principles (least privilege)
- No real secret is written into the file
- Transcript retention is the chosen 90 days
"""
import json
import re

from _shared_paths import SETTINGS_FILE

# Shapes of real credentials — a match means a secret was pasted into settings.json
SECRET_PATTERNS = {
    "OpenAI-style key": r"sk-[A-Za-z0-9_-]{20,}",
    "GitHub token": r"gh[pousr]_[A-Za-z0-9]{36}",
    "AWS access key ID": r"AKIA[0-9A-Z]{16}",
    "Slack token": r"xox[abprs]-[A-Za-z0-9-]{10,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}

# Allow entries security.md names as too broad, because each permits destructive commands
# Transcript retention chosen 2026-10-01 so the rule-usage audit has enough sessions
EXPECTED_CLEANUP_PERIOD_DAYS = 90

BROAD_DESTRUCTIVE_ALLOWS = {"Bash(*)", "Bash(git:*)", "Bash(rm:*)", "Bash(rm -rf:*)", "Bash(sudo:*)"}


def _load_settings():
    """Load and parse settings.json.

    :return: The parsed settings.
    """
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
        # Used for file discovery
        "Bash(find:*)",
        # Used for code search
        "Bash(grep:*)",
        # Git in any directory
        "Bash(git -C:*)",
        # GitHub API flexibility
        "Bash(gh api:*)",
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
    """Settings.json must not contain a real API key, token or private key."""
    content = SETTINGS_FILE.read_text()
    found = [name for name, pattern in SECRET_PATTERNS.items() if re.search(pattern, content)]
    assert not found, f"settings.json contains what looks like a {found} — remove it and rotate it"


def test_allow_list_has_no_broad_destructive_wildcards():
    """Allow list must not hold wildcards that permit destructive commands, per security.md."""
    allow_list = _load_settings()["permissions"]["allow"]
    broad = sorted(BROAD_DESTRUCTIVE_ALLOWS & set(allow_list))
    assert not broad, f"Allow list has over-broad entries {broad} — list specific safe subcommands instead"


def test_allow_and_deny_do_not_overlap():
    """No permission sits in both the allow and deny lists, where one silently overrides the other."""
    perms = _load_settings()["permissions"]
    both = sorted(set(perms["allow"]) & set(perms["deny"]))
    assert not both, f"Permissions in both allow and deny: {both} — keep each in one list only"


def test_enabled_plugins_intentional():
    """If enabledPlugins is present, it must be a well-formed, non-empty dict.

    No plugins are enabled by default (the intentional current state) — the
    key is legitimately absent. This only guards against a malformed or
    silently-empty block if one is ever added.
    """
    settings = _load_settings()
    if "enabledPlugins" not in settings:
        return

    enabled = settings["enabledPlugins"]
    assert isinstance(enabled, dict), "enabledPlugins must be a dict"
    assert enabled, "enabledPlugins should not be present if empty — remove the key instead"


def test_cleanup_period_days_is_chosen_value():
    """Transcript retention must stay at the chosen value, which the rule-usage audit depends on."""
    days = _load_settings().get("cleanupPeriodDays")
    assert days == EXPECTED_CLEANUP_PERIOD_DAYS, (
        f"cleanupPeriodDays is {days}, expected {EXPECTED_CLEANUP_PERIOD_DAYS} — "
        f"update settings_json_readme.md and this test together if the choice changes"
    )
