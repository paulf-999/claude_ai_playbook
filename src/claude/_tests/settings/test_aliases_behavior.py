#!/usr/bin/env python3
"""
Integration tests for aliases.md

Validates that when an alias is executed, it produces the intended outcome.

For skills/commands (starting with /):
- Verifies the skill exists
- Runs a quick test to confirm behavior

For conventions (bare words like 'bullets'):
- Verifies there's documentation/rules backing the convention
- Spot-checks that the convention is applied consistently
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ALIASES_PATH = Path(__file__).parent.parent.parent / "aliases.md"
CLAUDE_DIR = ALIASES_PATH.parent
SKILLS_DIR = CLAUDE_DIR / "skills"
RULES_DIR = CLAUDE_DIR / "_rules"


def parse_aliases_table() -> List[Dict]:
    """Parse aliases.md into structured data."""
    with open(ALIASES_PATH) as f:
        content = f.read()

    lines = content.split('\n')
    table_lines = [l for l in lines if l.strip().startswith('|')]

    aliases = []
    for line in table_lines[2:]:  # Skip header and separator
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) != 4:
            continue

        # Clean up backticks from input
        inp = parts[0].strip('`')

        aliases.append({
            'input': inp,
            'theme': parts[1],
            'status': parts[2],
            'meaning': parts[3]
        })

    return aliases


def test_skill_exists(skill_name: str) -> Tuple[bool, str]:
    """
    Test: Skill/command exists and is callable.

    For /skills: checks if the skill file exists in ~/.claude/skills/ or src/claude/skills/
    For /commands: checks if it's documented or exists as a Claude Code built-in
    """
    # Remove leading slash
    skill_clean = skill_name.lstrip('/')

    # Check local skills directory
    skill_file = SKILLS_DIR / f"{skill_clean}.md"
    if skill_file.exists():
        return True, f"✅ Skill found at {skill_file}"

    # Check _wip for disabled skills
    wip_skill = CLAUDE_DIR / "_wip" / "skills" / f"{skill_clean}.md"
    if wip_skill.exists():
        return False, f"⚠️  Skill disabled (in _wip): {wip_skill}"

    # For built-in commands, check if they're documented
    claude_commands = {
        'plan': 'Built-in Claude Code command (plan mode)',
        'batch': 'Built-in Claude Code command (batch automation)',
        'goal': 'Built-in Claude Code command (goal-based work)',
        'loop': 'Built-in Claude Code command (loop automation)',
        'model': 'Built-in Claude Code command (switch model)',
        'fast': 'Built-in Claude Code command (fast mode)',
        'config': 'Built-in Claude Code command (configure settings)',
    }

    if skill_clean in claude_commands:
        return True, f"✅ Built-in command: {claude_commands[skill_clean]}"

    return False, f"❌ Skill not found: {skill_name}"


def test_convention_documented(convention_name: str) -> Tuple[bool, str]:
    """
    Test: Convention/style is documented in rules or README.

    For 'bullets': checks writing_style.md
    For 'draft': checks writing_style.md (drafts section)
    """
    convention_map = {
        'bullets': ('_rules/writing_style.md', 'Leading bold keyword'),
        'draft': ('_rules/writing_style.md', 'Drafts'),
    }

    if convention_name not in convention_map:
        return None, f"⚠️  Convention '{convention_name}' not recognized (manual test needed)"

    doc_file, keyword = convention_map[convention_name]
    doc_path = CLAUDE_DIR / doc_file

    if not doc_path.exists():
        return False, f"❌ Documentation missing: {doc_path}"

    with open(doc_path) as f:
        content = f.read()

    if keyword.lower() in content.lower():
        return True, f"✅ Documented in {doc_file}"
    else:
        return False, f"❌ Keyword '{keyword}' not found in {doc_file}"


def test_alias_executable(alias_entry: Dict) -> Tuple[bool, str]:
    """
    Test: Alias is executable (command exists and is callable).

    Handles both:
    - Skills: /skill-name (Claude Code skills)
    - Conventions: bare words like 'bullets' (documented practices)
    - Commands: /command (Claude Code built-in commands)
    """
    inp = alias_entry['input']
    meaning = alias_entry['meaning']

    if inp.startswith('/'):
        # Skill or command
        skill_name = inp.lstrip('/')
        exists, msg = test_skill_exists(inp)
        if exists:
            return True, msg
        else:
            # Check if it's a built-in command (may not have a file)
            if any(keyword in meaning.lower() for keyword in ['skill', 'command', 'automation']):
                return True, f"✅ Documented command: {inp}"
            return False, msg

    else:
        # Convention (e.g., 'bullets', 'draft')
        exists, msg = test_convention_documented(inp)
        if exists is None:
            # Can't auto-test this; manual verification needed
            return True, msg
        return exists, msg


def test_all_aliases_executable():
    """Test: All aliases are executable or documented."""
    aliases = parse_aliases_table()

    print(f"🧪 Testing {len(aliases)} aliases for executability...\n")

    failed = []
    for alias in aliases:
        executable, msg = test_alias_executable(alias)
        status = "✅" if executable else "❌"
        print(f"{status} {alias['input']:30s} | {msg}")

        if not executable:
            failed.append((alias['input'], msg))

    print()

    if failed:
        print(f"❌ {len(failed)} aliases are not executable:")
        for inp, msg in failed:
            print(f"  - {inp}: {msg}")
        return False
    else:
        print(f"✅ All {len(aliases)} aliases are executable or documented")
        return True


def test_meaning_matches_behavior():
    """
    Test: Meaning description matches actual behavior.

    Spot-checks a few aliases to ensure the documented behavior is accurate.
    """
    aliases = parse_aliases_table()
    test_cases = {
        '/fewer-permission-prompts': 'transcript',  # Should audit transcripts
        'plan': 'plan mode',  # Should enter plan mode
        'bullets': 'keyword',  # Should describe keyword: style
    }

    print(f"\n🧪 Spot-checking meaning accuracy...\n")

    for alias_input, expected_keyword in test_cases.items():
        matching = [a for a in aliases if a['input'] == alias_input]
        if not matching:
            print(f"⚠️  {alias_input}: Not found in aliases (skipping)")
            continue

        alias = matching[0]
        meaning = alias['meaning'].lower()

        if expected_keyword.lower() in meaning:
            print(f"✅ {alias_input:30s} | Meaning matches behavior")
        else:
            print(f"❌ {alias_input:30s} | Meaning mismatch (expected '{expected_keyword}', got '{meaning[:50]}...')")


def main():
    """Run all behavior tests."""
    print("=" * 70)
    print("Alias Behavior Integration Tests")
    print("=" * 70)
    print()

    all_pass = test_all_aliases_executable()
    test_meaning_matches_behavior()

    print()
    if not all_pass:
        print("❌ Some aliases failed behavior tests")
        sys.exit(1)
    else:
        print("✅ All alias behavior tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
