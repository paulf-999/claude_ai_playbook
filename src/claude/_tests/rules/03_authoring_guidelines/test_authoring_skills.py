# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-16
# Date updated:      2026-10-02
# Version:           4.1.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests what authoring_skills.md says every skill must contain.

Covers the SKILL.md structure, the good-frontmatter example, the contract's required
fields and trigger design, read from the parent rule and every child it points to.
Where the rule states something twice — the contract fields in the core standards and
in the hard-gates checklist — the two must agree. The old checks matched words such
as "use" that any text contains, so they could never fail.
``test_authoring_skills_maturity.py`` covers maturity, scope and maintenance.
"""
from __future__ import annotations

import re

from _resolved_rule import child_paths, resolved_content
from _shared_paths import RULES_DIR

RULE_FILE = RULES_DIR / "03_authoring_guidelines" / "authoring_skills.md"
CHECKLIST = RULES_DIR / "03_authoring_guidelines" / "authoring_skills" / "_lazy_load" / "_hard_gates_checklist.md"
SECTIONS = ["Frontmatter", "Instructions for Claude", "Purpose", "Example Usage", "Best For", "References"]
CONTRACT_FIELDS = ["`name`, `version`, `summary`, `maturity`", "`dispatch.triggers`", "`dispatch.not_for`", "`output`"]
MATURITY_LEVELS = {"draft", "tactical", "strategic"}


def content() -> str:
    """Read authoring_skills.md with every child inlined.

    :return: The full resolved rule text.
    :rtype: str
    """
    return resolved_content(RULE_FILE)


def frontmatter_example() -> str:
    """Return the YAML block of the 'Good SKILL.md Frontmatter' example.

    :return: The example's fenced text, frontmatter and metadata header.
    :rtype: str
    """
    after = content().split("**Example: Good SKILL.md Frontmatter**", 1)[1]
    return after.split("```yaml", 1)[1].split("```", 1)[0]


def test_children_resolve():
    """Every child the rule points to exists and is inlined."""
    children = child_paths(RULE_FILE)
    assert len(children) >= 5, f"expected the five on-demand children, found {children}"
    missing = [str(c) for c in children if not c.is_file()]
    assert not missing, f"authoring_skills.md points to missing files: {missing}"
    assert "**Read on demand:**" not in content(), "a pointer was left unresolved"


def test_skill_md_has_six_sections_in_order():
    """SKILL.md's six sections are listed in the canonical order."""
    found = re.findall(r"^\d\. \*\*([^*]+)\*\* —", content(), re.M)
    assert found[:6] == SECTIONS, f"SKILL.md sections changed: {found[:6]}"


def test_skill_md_stays_short():
    """SKILL.md is meant to be about 60 lines plus its instructions, with detail in reference/."""
    target = "6-section canonical structure, ~60 lines plus the instructions section"
    assert target in content(), "the ~60-line target is missing"


def test_example_name_follows_pattern():
    """The example skill name follows the <domain>_<action> pattern it teaches."""
    name = re.search(r"^name: (\S+)$", frontmatter_example(), re.M)
    assert name, "the example has no name field"
    assert re.fullmatch(r"[a-z]+_[a-z_]+", name.group(1)), f"example name {name.group(1)} breaks <domain>_<action>"


def test_example_maturity_is_a_real_level():
    """The example's maturity is one of the three levels the rule defines."""
    maturity = re.search(r"^maturity: (\S+)$", frontmatter_example(), re.M)
    assert maturity and maturity.group(1) in MATURITY_LEVELS, f"example maturity must be one of {MATURITY_LEVELS}"


def test_example_has_frontmatter_fields_and_header():
    """The example carries name, description, maturity and tags, then the 3-line metadata header."""
    example = frontmatter_example()
    missing = [f for f in ("name:", "description:", "maturity:", "tags:") if f"\n{f}" not in example]
    assert not missing, f"example frontmatter is missing {missing}"
    header = re.findall(r"^<!-- (version|created|updated): ", example, re.M)
    assert header == ["version", "created", "updated"], f"example metadata header is wrong: {header}"


def test_contract_required_fields():
    """The contract section lists every required field."""
    section = content().split("## 📜 Contract Requirements [REQUIRED]", 1)[1].split("[IF APPLICABLE]", 1)[0]
    missing = [f for f in CONTRACT_FIELDS if f not in section]
    assert not missing, f"contract requirements no longer list {missing}"


def test_checklist_matches_contract_fields():
    """The hard-gates checklist asks for the same contract fields the core standards require."""
    checklist = CHECKLIST.read_text()
    assert "name, version, summary, maturity all defined" in checklist, "checklist lost the core contract fields"
    for field in ("dispatch.triggers documented", "dispatch.not_for documented", "output (type, confirmation_required"):
        assert field in checklist, f"checklist no longer asks for {field!r}"


def test_not_for_is_most_important():
    """The checklist marks not_for as the most important contract field."""
    assert "specific and not empty (scope boundaries; MOST IMPORTANT)" in CHECKLIST.read_text(), "not_for emphasis lost"


def test_trigger_design_prefers_explicit_triggers():
    """Explicit triggers drive auto-invocation, and phrase lists should be exhaustive."""
    assert "**Explicit triggers drive auto-invocation.**" in content(), "the explicit-trigger rule is missing"
    exhaustive = "**Be exhaustive:** a false positive costs less than a missed invocation."
    assert exhaustive in content(), "the be-exhaustive rule is missing"


def test_trigger_design_warns_against_generic_phrases():
    """Triggers that are too generic, such as 'help', are called out."""
    assert '**Not too generic:** "help" or "please" alone' in content(), "the too-generic warning is missing"
