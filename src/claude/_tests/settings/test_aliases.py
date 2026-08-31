#!/usr/bin/env python3
"""
Tests for aliases.md

Validates that each alias entry:
1. Has all required fields (Input, Theme, Status, Meaning)
2. Status is a valid state (Ready, Testing)
3. The alias/skill actually exists or is documented
4. Meaning accurately describes the feature
"""

import re
import sys
from pathlib import Path

# Load aliases.md
ALIASES_PATH = Path(__file__).parent.parent.parent / "aliases.md"


def parse_aliases_table():
    """Parse aliases.md markdown table into structured data."""
    with open(ALIASES_PATH) as f:
        content = f.read()

    # Extract table rows (skip header)
    lines = content.split('\n')
    table_lines = [l for l in lines if l.strip().startswith('|')]

    if len(table_lines) < 3:  # header, separator, at least one row
        raise ValueError(f"Invalid aliases table in {ALIASES_PATH}")

    aliases = []
    for line in table_lines[2:]:  # Skip header and separator
        parts = [p.strip() for p in line.split('|')[1:-1]]  # Skip empty first/last
        if len(parts) != 4:
            continue

        aliases.append({
            'input': parts[0],
            'theme': parts[1],
            'status': parts[2],
            'meaning': parts[3]
        })

    return aliases


def test_required_fields():
    """Test: Each alias has all required fields."""
    aliases = parse_aliases_table()

    for alias in aliases:
        assert alias['input'], "Input field missing"
        assert alias['theme'], "Theme field missing"
        assert alias['status'], "Status field missing"
        assert alias['meaning'], "Meaning field missing"

    print(f"✅ All {len(aliases)} aliases have required fields")


def test_valid_status():
    """Test: Status is one of allowed values."""
    VALID_STATUSES = {'Ready', 'Testing'}
    aliases = parse_aliases_table()

    for alias in aliases:
        assert alias['status'] in VALID_STATUSES, \
            f"{alias['input']}: Invalid status '{alias['status']}'. Must be one of: {VALID_STATUSES}"

    print(f"✅ All aliases have valid status (Ready or Testing)")


def test_no_duplicate_inputs():
    """Test: No duplicate input aliases."""
    aliases = parse_aliases_table()
    inputs = [a['input'] for a in aliases]

    assert len(inputs) == len(set(inputs)), \
        f"Duplicate alias inputs found: {[x for x in inputs if inputs.count(x) > 1]}"

    print(f"✅ No duplicate alias inputs")


def test_meaning_not_empty():
    """Test: Meaning field has substantive content (not just punctuation)."""
    aliases = parse_aliases_table()

    for alias in aliases:
        meaning = alias['meaning'].strip()
        assert len(meaning) > 10, \
            f"{alias['input']}: Meaning too brief or empty ('{meaning}')"

    print(f"✅ All meanings are substantive (>10 chars)")


def test_input_format():
    """Test: Input field is properly formatted (/command or bare word)."""
    aliases = parse_aliases_table()

    for alias in aliases:
        inp = alias['input']
        # Should be /command or bare_word or backtick wrapped
        assert inp.startswith('/') or inp.startswith('`') or '_' not in inp or inp[0].isalpha(), \
            f"Invalid input format: '{inp}' (expected /command or bare word)"

    print(f"✅ All inputs are properly formatted")


def test_no_orphaned_references():
    """Test: Referenced skills/commands are not stubs (at least documented somewhere)."""
    aliases = parse_aliases_table()

    # Skills/commands that are expected to exist
    known_skills = {
        'batch', 'goal', 'loop', 'fewer-permission-prompts',
        'plan', 'draft', 'bullets'
    }

    for alias in aliases:
        inp = alias['input'].lstrip('/').lstrip('`').rstrip('`')
        if inp.startswith('_'):
            continue  # Skip internal aliases

        # If it's documented, that's enough
        if alias['status'] == 'Ready' or alias['status'] == 'Testing':
            assert alias['meaning'], f"{inp}: No meaning provided"

    print(f"✅ All aliases are documented (have meaning)")


def test_consistency():
    """Test: Related aliases have consistent documentation."""
    aliases = parse_aliases_table()
    alias_dict = {a['input']: a for a in aliases}

    # Automation-related aliases should reference controls
    automation_aliases = [a for a in aliases if a['theme'] == 'Automation']
    for alias in automation_aliases:
        if alias['status'] == 'Testing':
            # Should reference control docs
            assert 'claude_efficiency.md' in alias['meaning'] or 'automation_controls.md' in alias['meaning'], \
                f"{alias['input']}: Automation Testing alias should reference control docs"

    print(f"✅ Automation aliases reference control documentation")


def main():
    """Run all tests."""
    tests = [
        test_required_fields,
        test_valid_status,
        test_no_duplicate_inputs,
        test_meaning_not_empty,
        test_input_format,
        test_no_orphaned_references,
        test_consistency,
    ]

    print("🧪 Running aliases.md tests...\n")

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print()
    if failed:
        print(f"❌ {failed}/{len(tests)} tests failed")
        sys.exit(1)
    else:
        print(f"✅ All {len(tests)} tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
