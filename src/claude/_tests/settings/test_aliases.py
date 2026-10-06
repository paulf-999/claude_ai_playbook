# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-06
# Version:           2.2.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the alias table in aliases.md.

Every row needs the four columns filled in, a known status, a unique and
well-formed input, and a substantive meaning. Rule paths a meaning names must
exist, and experimental automation aliases must point to their controls.
Merged in from the old ``rules/test_aliases_behavior.py``: the core aliases stay
documented, at least one is Ready, and every Testing alias names its exit doc.
"""
import re

import pytest

from _shared_paths import ALIASES_FILE, CLAUDE_DIR

COLUMNS = ["Input", "Theme", "Status", "Meaning"]
VALID_STATUSES = {"Ready", "Testing"}
INPUT_PATTERN = r"`/?[a-z][a-z0-9_-]*`"
CONTROLS_DOC = "_rules_lazy_load/automation_controls.md"
# A rule path an alias meaning names, under rules/ or _rules_lazy_load/
RULE_PATH = r"\b_?rules(?:_lazy_load)?/[\w/]+\.md"


def parse_aliases(content: str) -> list[dict[str, str]]:
    """Parse the alias table into one dict per row.

    :param content: Text of aliases.md.
    :type content: str
    :return: Rows keyed by lowercase column name.
    :rtype: list[dict[str, str]]
    :raises ValueError: When there's no table, the header is wrong or a row doesn't have four cells.
    """
    table = [line for line in content.splitlines() if line.strip().startswith("|")]
    if len(table) < 3:
        raise ValueError("aliases.md needs a table with a header, a separator and at least one row")
    header = [cell.strip() for cell in table[0].strip().strip("|").split("|")]
    if header != COLUMNS:
        raise ValueError(f"alias table header is {header}, expected {COLUMNS}")
    rows = []
    for line in table[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        # A wrong cell count means a broken row, which must fail rather than vanish
        if len(cells) != len(COLUMNS):
            raise ValueError(f"alias row has {len(cells)} cells, expected {len(COLUMNS)}: {line}")
        rows.append(dict(zip([c.lower() for c in COLUMNS], cells)))
    return rows


def load_aliases() -> list[dict[str, str]]:
    """Parse the real aliases.md.

    :return: Rows keyed by lowercase column name.
    :rtype: list[dict[str, str]]
    """
    return parse_aliases(ALIASES_FILE.read_text())


def test_table_parses_with_rows():
    """The real table parses and has at least one alias."""
    aliases = load_aliases()
    assert aliases, "aliases.md has no alias rows"


def test_required_fields():
    """Each alias has all four fields filled in."""
    for alias in load_aliases():
        empty = [column for column, value in alias.items() if not value]
        assert not empty, f"{alias['input'] or 'a row'}: empty {empty} — fill in every column"


def test_valid_status():
    """Status is Ready or Testing."""
    for alias in load_aliases():
        assert alias["status"] in VALID_STATUSES, (
            f"{alias['input']}: status '{alias['status']}' not in {VALID_STATUSES}"
        )


def test_no_duplicate_inputs():
    """No input appears twice."""
    inputs = [alias["input"] for alias in load_aliases()]
    duplicates = sorted({i for i in inputs if inputs.count(i) > 1})
    assert not duplicates, f"Duplicate alias inputs: {duplicates}"


def test_meaning_is_substantive():
    """Each meaning is more than a few characters."""
    for alias in load_aliases():
        assert len(alias["meaning"]) > 10, f"{alias['input']}: meaning too brief ('{alias['meaning']}')"


def test_input_format():
    """Each input is a backticked lowercase word or /command."""
    for alias in load_aliases():
        assert re.fullmatch(INPUT_PATTERN, alias["input"]), (
            f"{alias['input']}: expected `word` or `/command` in lowercase, matching {INPUT_PATTERN}"
        )


def test_referenced_rule_paths_exist():
    """Every rule path a meaning names exists, so links can't rot."""
    paths = {path for alias in load_aliases() for path in re.findall(RULE_PATH, alias["meaning"])}
    assert paths, "expected at least one meaning to name a rules/ or _rules_lazy_load/ path"
    missing = sorted(path for path in paths if not (CLAUDE_DIR / path).is_file())
    assert not missing, f"aliases.md names rule files that don't exist: {missing}"


def test_testing_automation_aliases_reference_controls():
    """Experimental automation aliases point to their controls doc."""
    testing = [a for a in load_aliases() if a["theme"] == "Automation" and a["status"] == "Testing"]
    assert testing, "expected at least one Automation alias in Testing"
    for alias in testing:
        assert CONTROLS_DOC in alias["meaning"], f"{alias['input']}: Testing automation alias must name {CONTROLS_DOC}"


def test_controls_note_matches_table():
    """The automation-controls note names exactly the Testing automation aliases."""
    content = ALIASES_FILE.read_text()
    note = content.split("## ", 1)[1] if "## " in content else ""
    named = set(re.findall(r"`(/[a-z][a-z0-9_-]*)`", note))
    testing = {
        a["input"].strip("`") for a in load_aliases() if a["theme"] == "Automation" and a["status"] == "Testing"
    }
    assert named, "expected the note section to name the experimental automation aliases"
    assert named == testing, (
        f"note names {sorted(named)} but the table's Testing automation aliases are {sorted(testing)}"
    )


def test_core_aliases_documented():
    """The core aliases stay in the table."""
    inputs = {alias["input"].strip("`") for alias in load_aliases()}
    missing = sorted({"/fewer-permission-prompts", "/batch", "plan"} - inputs)
    assert not missing, f"core aliases missing from aliases.md: {missing}"


def test_some_alias_is_ready():
    """At least one alias is Ready, so the table isn't all experiments."""
    assert any(alias["status"] == "Ready" for alias in load_aliases()), "no alias is marked Ready"


def test_every_testing_alias_names_its_exit_doc():
    """Every Testing alias points to the rule that says when it graduates."""
    for alias in load_aliases():
        if alias["status"] == "Testing":
            assert re.search(RULE_PATH, alias["meaning"]), (
                f"{alias['input']} is Testing but names no rule with its exit criteria"
            )


def test_plan_alias_enters_plan_mode():
    """The plan alias says it enters plan mode."""
    plan = next((a for a in load_aliases() if a["input"] == "`plan`"), None)
    assert plan, "the plan alias is missing"
    assert "plan mode" in plan["meaning"].lower(), f"plan alias meaning should mention plan mode: {plan['meaning']}"


def test_parser_rejects_missing_table():
    """Text with no table is an error, not an empty list."""
    with pytest.raises(ValueError, match="needs a table"):
        parse_aliases("# Aliases\n\nNo table here.\n")


def test_parser_rejects_wrong_header():
    """A table with the wrong columns is an error."""
    content = "| Input | Meaning |\n|---|---|\n| `x` | does x |\n"
    with pytest.raises(ValueError, match="header"):
        parse_aliases(content)


def test_parser_rejects_short_row():
    """A row with a missing cell fails instead of being dropped."""
    content = "| Input | Theme | Status | Meaning |\n|---|---|---|---|\n| `x` | Theme | Ready |\n"
    with pytest.raises(ValueError, match="3 cells") as error:
        parse_aliases(content)
    assert "| `x` | Theme | Ready |" in str(error.value), "the error should quote the broken row so it can be found"


def test_parser_reads_good_row():
    """A well-formed row parses into lowercase keys."""
    content = "| Input | Theme | Status | Meaning |\n|---|---|---|---|\n| `x` | Demo | Ready | Does the x thing |\n"
    rows = parse_aliases(content)
    assert len(rows) == 1, f"expected one row, got {rows}"
    expected = {"input": "`x`", "theme": "Demo", "status": "Ready", "meaning": "Does the x thing"}
    assert rows[0] == expected, f"got {rows[0]}"
