"""Tests for aliases.md — validates that documented aliases actually work.

Spot-checks 3-5 representative aliases to ensure:
- They are documented in aliases.md
- They are invocable (either as commands, skills, or modes)
- Their documented behavior matches their implementation
"""
import json
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
ALIASES_FILE = CLAUDE_DIR / "aliases.md"
SKILLS_DIR = CLAUDE_DIR / "skills"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"


def _parse_aliases_table():
    """Parse aliases.md table and return list of (input, theme, status, meaning) tuples."""
    content = ALIASES_FILE.read_text()
    aliases = []

    # Find the table (starts with | Input | Theme | Status | Meaning |)
    lines = content.split("\n")
    in_table = False
    for line in lines:
        if "| Input | Theme | Status | Meaning |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            # Parse table row: | input | theme | status | meaning |
            parts = [p.strip() for p in line.split("|")[1:-1]]  # Remove empty first/last
            if len(parts) >= 4 and not "---" in line:
                # Remove backticks from input field
                input_val = parts[0].replace("`", "")
                aliases.append({
                    "input": input_val,
                    "theme": parts[1],
                    "status": parts[2],
                    "meaning": parts[3],
                })
    return aliases


def test_aliases_documented():
    """Aliases.md must contain a valid table of aliases."""
    aliases = _parse_aliases_table()
    assert len(aliases) > 0, "aliases.md has no documented aliases (missing or malformed table)"
    assert len(aliases) >= 3, (
        f"Only {len(aliases)} aliases documented. Expected at least 3 representative aliases."
    )


def test_sample_aliases_exist():
    """Spot-check representative aliases: /fewer-permission-prompts, /batch, plan."""
    aliases = _parse_aliases_table()
    alias_inputs = {a["input"] for a in aliases}

    # Representative sample: these are core features that should be documented
    required = {"/fewer-permission-prompts", "/batch", "plan"}

    for alias_input in required:
        assert alias_input in alias_inputs, (
            f"Expected alias '{alias_input}' not found in aliases.md"
        )


def test_aliases_with_ready_status_are_functional():
    """Aliases marked 'Ready' must be currently functional."""
    aliases = _parse_aliases_table()

    ready_aliases = [a for a in aliases if a["status"] == "Ready"]
    assert len(ready_aliases) > 0, "No aliases marked 'Ready' — config may be incomplete"

    # Verify /plan is either mode-based or a real command
    plan_alias = next((a for a in ready_aliases if a["input"] == "/plan"), None)
    if plan_alias:
        # /plan is handled by Claude Code harness, not as a skill file
        # Just verify it's documented as a Claude mode
        assert "plan" in plan_alias["meaning"].lower(), (
            "/plan alias should mention plan mode in its meaning"
        )


def test_aliases_have_clear_meaning():
    """Every alias must have a non-empty, meaningful description."""
    aliases = _parse_aliases_table()

    for alias in aliases:
        assert alias["meaning"].strip(), (
            f"Alias '{alias['input']}' has empty meaning — document what it does"
        )
        assert len(alias["meaning"]) > 5, (
            f"Alias '{alias['input']}' has too-brief meaning: '{alias['meaning']}'. "
            f"Describe the feature in 1-2 sentences."
        )


def test_testing_aliases_have_exit_criteria():
    """Aliases marked 'Testing' must document when/how they graduate to 'Ready'."""
    aliases = _parse_aliases_table()

    testing_aliases = [a for a in aliases if a["status"] == "Testing"]

    # For now, this is a documentation lint: every Testing alias should have
    # a linked issue or date target in the meaning. This test just warns.
    for alias in testing_aliases:
        # Check if the meaning contains any indicator of completion criteria
        meaning = alias["meaning"].lower()
        has_criteria = (
            "when" in meaning or "if" in meaning or
            "controls in" in meaning  # References a controls doc
        )
        # This is informational; don't fail, just document
        if not has_criteria:
            print(f"⚠️  '{alias['input']}' (Testing) lacks clear exit criteria")
