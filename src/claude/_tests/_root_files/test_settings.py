# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-27
# Version:           1.5.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for settings.json — validates permissions and configuration.

Ensures:
- Permission structure is valid (allow/deny lists present)
- Deny list includes security-critical paths
- Broad wildcard permissions are intentional and documented
- Git writes and allow-list bypasses are not auto-approved
- GitHub CLI and branch writes are not auto-approved, while their reads still are
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
        # Reading GitHub PRs
        "Bash(gh pr view:*)",
    }

    # Verify each intentional wildcard is present
    allow_set = set(allow_list)
    for expected in intentional_wildcards:
        assert expected in allow_set, (  # wording-check: settings.json values
            f"Expected intentional permission '{expected}' not found in allow list. "
            f"If removed, update this test to reflect the change."
        )


def test_allow_list_git_read_operations_present():
    """Allow list must include the read-only git operations used every session."""
    settings = _load_settings()
    allow_list = settings["permissions"]["allow"]

    # Read-only git operations, safe to run without a prompt
    required_git_ops = {
        "Bash(git branch --show-current)",
        "Bash(git diff:*)",
        "Bash(git log:*)",
        "Bash(git status:*)",
    }

    allow_set = set(allow_list)
    missing = required_git_ops - allow_set

    assert not missing, (
        f"Allow list missing read-only git operations: {missing}. "
        f"These run every session and are safe to auto-approve."
    )


def test_allow_list_gates_git_writes():
    """Allow list must not auto-approve git writes or commands that bypass the allow list.

    `_security_guardrails.md` keeps write commands gated for per-use approval. A prefix
    such as `git push:*` also matches `git push --force`, and `git -C:*` or `bash -c:*`
    match any command at all, including those writes.
    """
    settings = _load_settings()
    allow_list = settings["permissions"]["allow"]

    # Writes and bypasses that must prompt each time
    gated_ops = {
        "Bash(bash -c:*)",
        "Bash(git -C:*)",
        "Bash(git checkout:*)",
        "Bash(git commit:*)",
        "Bash(git merge:*)",
        "Bash(git pull:*)",
        "Bash(git push:*)",
        "Bash(git rebase:*)",
        "Bash(git reset:*)",
        "Bash(git:*)",
    }

    auto_approved = gated_ops & set(allow_list)

    assert not auto_approved, (
        f"Allow list auto-approves git writes or bypasses: {sorted(auto_approved)}. "
        f"Remove them so each one prompts, per _security_guardrails.md."
    )


def auto_approves(allow_list: list[str], command: str) -> bool:
    """Return True if an allow-list entry would run ``command`` without a prompt.

    ``Bash(x:*)`` matches any command starting with ``x``, and ``Bash(x)`` matches ``x`` exactly.

    :param allow_list: The ``permissions.allow`` entries from settings.json.
    :param command: A shell command as Claude would run it.
    :return: Whether any entry matches the command.
    """
    for entry in allow_list:
        if not entry.startswith("Bash(") or not entry.endswith(")"):
            continue
        pattern = entry[len("Bash("):-1]
        if pattern.endswith(":*") and command.startswith(pattern[:-2]):
            return True
        if pattern == command:
            return True
    return False


# Writes that look like reads to a prefix rule: each would change GitHub or delete a branch
GH_AND_BRANCH_WRITES = (
    "gh pr merge 12",
    "gh pr close 12",
    "gh pr comment 12 --body hi",
    "gh pr review 12 --approve",
    "gh issue close 12",
    "gh issue delete 12",
    "gh api -X DELETE repos/o/r/git/refs/heads/x",
    "gh api repos/o/r/issues -f title=x",
    "gh run cancel 99",
    "gh run delete 99",
    "git branch -D feature/x",
    "git branch -m old new",
)

# Reads the narrowed list must keep prompt-free, so the fix doesn't over-correct
GH_AND_BRANCH_READS = (
    "gh pr view 12",
    "gh pr list",
    "gh pr diff 12",
    "gh pr checks 12",
    "gh issue view 12",
    "gh issue list",
    "gh run list",
    "gh run view 99",
    "git branch",
    "git branch --show-current",
)


def test_allow_list_gates_gh_and_branch_writes():
    """No GitHub CLI write or branch delete runs without a prompt, per _security_guardrails.md."""
    allow_list = _load_settings()["permissions"]["allow"]
    approved = [cmd for cmd in GH_AND_BRANCH_WRITES if auto_approves(allow_list, cmd)]
    assert not approved, f"Allow list auto-approves these writes — narrow the entry that matches: {approved}"


def test_allow_list_keeps_gh_and_branch_reads():
    """Common GitHub CLI and branch reads still run without a prompt."""
    allow_list = _load_settings()["permissions"]["allow"]
    prompted = [cmd for cmd in GH_AND_BRANCH_READS if not auto_approves(allow_list, cmd)]
    assert not prompted, f"These reads now prompt — add a read-only entry for them: {prompted}"


def test_auto_approves_matches_prefix_and_exact_entries():
    """A ``:*`` entry matches by prefix, a plain entry only exactly, and non-Bash entries never."""
    allow_list = ["Bash(gh pr view:*)", "Bash(git branch)", "Read(./x)"]
    assert auto_approves(allow_list, "gh pr view 12"), "a prefix entry should match a longer command"
    assert auto_approves(allow_list, "git branch"), "an exact entry should match itself"
    assert not auto_approves(allow_list, "git branch -D x"), "an exact entry must not match a longer command"
    assert not auto_approves(allow_list, "gh pr merge 12"), "a prefix entry must not match a different command"


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


def test_git_c_wildcard_not_allowed():
    """`git -C` is never auto-allowed, since the path sits before the subcommand and the wildcard approves any write.

    Issue #410: `Bash(git -C:*)` auto-approved `git -C <repo> push --force` and `reset --hard`.
    """
    allow_list = _load_settings()["permissions"]["allow"]
    broad = [entry for entry in allow_list if entry.startswith("Bash(git -C")]
    assert not broad, f"git -C must prompt, not be auto-allowed: {broad}"
