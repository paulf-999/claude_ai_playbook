# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# Date created:      2026-08-28
# Version:           2.0.0
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Content-regression tests for behaviour/_artefact_proposal_gates.md.

Goal: catch silent loss or drift of the three proposal gates (naming,
placement, duplication), their order, and the files and examples they
point to. Every check reads the real rule or a file it names, so the suite
fails if the rule is deleted, trimmed, or left pointing at moved files.
"""
import re

from _shared_paths import CLAUDE_DIR, HOOKS_DIR, RULES_DIR, SKILLS_DIR

RULE_FILE = RULES_DIR / "02_claude_standards" / "behaviour" / "_artefact_proposal_gates.md"
PARENT_FILE = RULES_DIR / "02_claude_standards" / "behaviour.md"
SKILL_DOMAINS = RULES_DIR / "03_authoring_guidelines" / "authoring_skills" / "skill_domains.yaml"

GATE_HEADINGS = ["### Gate 1️⃣: Naming", "### Gate 2️⃣: Placement", "### Gate 3️⃣: Duplication"]
TIERS = ["01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_claude_reference", "05_lazy_load"]


def gate_section(content: str, number: int) -> str:
    """Return the text of one gate, from its heading to the next ``---`` rule.

    :param content: Full text of the rule file.
    :type content: str
    :param number: Gate number, 1 to 3.
    :type number: int
    :return: The gate's section, or an empty string if the heading is missing.
    :rtype: str
    """
    start = content.find(GATE_HEADINGS[number - 1])
    if start == -1:
        return ""
    end = content.find("\n---", start)
    return content[start:] if end == -1 else content[start:end]


def referenced_rule_files(section: str) -> list:
    """Resolve every file a gate's **Reference:** line names to a real path.

    The parent is written as ``~/<config_dir>/_rules/...md`` (any config
    directory name, per portable_paths.md); its children are bare
    ``_child.md`` names living in a folder named after the parent.

    :param section: One gate's text, from :func:`gate_section`.
    :type section: str
    :return: Paths of the parent and each named child.
    :rtype: list
    """
    match = re.search(r"\*\*Reference:\*\* `~/[^/`]+/(_rules/[^`]+)\.md`(.*)", section)
    if not match:
        return []
    parent = CLAUDE_DIR / f"{match.group(1)}.md"
    children = re.findall(r"`(_[a-z_]+\.md)`", match.group(2))
    return [parent] + [parent.with_suffix("") / child for child in children]


def test_rule_file_exists():
    """The rule lives where behaviour.md and this test expect it."""
    assert RULE_FILE.is_file(), f"Missing {RULE_FILE} — restore it or update RULE_FILE and behaviour.md's import"


def test_parent_imports_the_rule():
    """behaviour.md imports the rule, so it is loaded every session."""
    parent = PARENT_FILE.read_text()
    import_line = r"^@~/[^/]+/_rules/02_claude_standards/behaviour/_artefact_proposal_gates\.md$"
    assert re.search(import_line, parent, re.MULTILINE), (
        "behaviour.md must @import _artefact_proposal_gates.md, or the gates are never loaded"
    )


def test_three_gates_appear_in_order():
    """Naming, placement and duplication headings all exist, in that order."""
    content = RULE_FILE.read_text()
    positions = [content.find(heading) for heading in GATE_HEADINGS]
    assert -1 not in positions, f"Missing gate heading(s): {[h for h, p in zip(GATE_HEADINGS, positions) if p == -1]}"
    assert positions == sorted(positions), "Gates must appear in order: naming → placement → duplication"


def test_every_gate_has_check_reference_and_action():
    """Each gate states what it checks, where the standard lives, and what to do."""
    content = RULE_FILE.read_text()
    for number in (1, 2, 3):
        section = gate_section(content, number)
        for label in ("**Check:**", "**Reference:**", "**Action:**"):
            assert label in section, f"Gate {number} is missing its {label} line"


def test_naming_gate_covers_every_artefact_type():
    """Gate 1 gives a naming rule for skills, rules, hooks, agents and processes."""
    section = gate_section(RULE_FILE.read_text(), 1)
    for artefact in ("**Skills:**", "**Rules:**", "**Hooks:**", "**Agents:**", "**Processes:**"):
        assert artefact in section, f"Gate 1 no longer names a pattern for {artefact.strip('*:')}"


def test_naming_gate_keeps_its_patterns():
    """Gate 1's patterns match the naming standard's own patterns."""
    section = gate_section(RULE_FILE.read_text(), 1)
    for pattern in ("`<domain>_<action>`", "`hook_<type>_<domain>.sh`", "`agents/<group>/<name>/AGENT.md`"):
        assert pattern in section, f"Gate 1 lost the {pattern} pattern"


def test_naming_gate_examples_exist():
    """Every skill, hook and agent Gate 1 uses as an example is real."""
    section = gate_section(RULE_FILE.read_text(), 1)
    skills = {path.parent.name for path in SKILLS_DIR.rglob("SKILL.md")}
    for skill in ("confluence_create_page", "jira_create"):
        assert f"`{skill}`" in section, f"Gate 1 no longer uses {skill} as an example — update this test"
        assert skill in skills, f"Gate 1 example skill {skill} doesn't exist under skills/"
    assert (HOOKS_DIR / "hook_enforcement_naming_convention.sh").is_file(), "Gate 1 example hook no longer exists"
    agent = CLAUDE_DIR / "agents" / "core" / "technical_writer" / "AGENT.md"
    assert agent.is_file(), "Gate 1 example agent no longer exists"


def test_naming_gate_example_domains_are_registered():
    """The skill domains Gate 1 relies on are listed in skill_domains.yaml."""
    domains = set(re.findall(r"^\s*- id: ([a-z_]+)$", SKILL_DOMAINS.read_text(), re.MULTILINE))
    for domain in ("confluence", "jira"):
        assert domain in domains, (
            f"Domain '{domain}' is missing from skill_domains.yaml, which Gate 1 tells Claude to check"
        )


def test_placement_gate_names_every_tier():
    """Gate 2 lists all five rule tiers, and each one exists."""
    section = gate_section(RULE_FILE.read_text(), 2)
    for tier in TIERS:
        assert f"**{tier}/**" in section, f"Gate 2 no longer lists the {tier}/ tier"
        assert (RULES_DIR / tier).is_dir(), f"Gate 2 lists {tier}/, but _rules/{tier}/ doesn't exist"


def test_reference_files_exist():
    """Every file a gate's Reference line points to exists."""
    content = RULE_FILE.read_text()
    for number in (1, 2, 3):
        paths = referenced_rule_files(gate_section(content, number))
        assert paths, f"Gate {number}'s Reference line no longer names a ~/<config>/_rules/ file"
        for path in paths:
            assert path.is_file(), f"Gate {number} points to {path}, which doesn't exist — update the Reference line"


def test_naming_and_placement_recommend_directly():
    """Gates 1 and 2 recommend the fix outright instead of offering options."""
    content = RULE_FILE.read_text()
    assert "recommend the corrected name directly" in gate_section(content, 1), (
        "Gate 1 must recommend the corrected name directly"
    )
    assert "recommend the correct directory directly" in gate_section(content, 2), (
        "Gate 2 must recommend the correct directory directly"
    )


def test_duplication_gate_offers_integration():
    """Gate 3 offers extending the existing artefact as an alternative to a new one."""
    section = gate_section(RULE_FILE.read_text(), 3)
    assert "extend existing artefact vs. create new one" in section, (
        "Gate 3 must offer extend-existing vs. create-new options"
    )


def test_gate_sequence_runs_in_order():
    """The sequence block asks the three questions in order and ends in 'safe to proceed'."""
    content = RULE_FILE.read_text()
    questions = [
        "1. Does naming follow convention?",
        "2. Is placement correct for artefact type?",
        "3. Does similar artefact already exist?",
    ]
    positions = [content.find(question) for question in questions]
    assert -1 not in positions, "The Gate Sequence block lost one of its three questions"
    assert positions == sorted(positions), "The Gate Sequence questions are out of order"
    assert "Safe to proceed with proposal" in content, (
        "The Gate Sequence no longer ends in 'Safe to proceed with proposal'"
    )


def test_options_only_in_listed_scenarios():
    """Options are limited to one named scenario per gate, with 'Otherwise' as the default."""
    content = RULE_FILE.read_text()
    assert "Present options *only* in these scenarios" in content, (
        "The 'only in these scenarios' limit on options was lost"
    )
    for gate in ("**Gate 1 (Naming):**", "**Gate 2 (Placement):**", "**Gate 3 (Duplication):**"):
        assert gate in content, f"When to Present Options lost its {gate} scenario"
    assert "**Otherwise:**" in content, "When to Present Options lost its 'Otherwise' default"


def test_contents_matches_headings():
    """Every Contents link has a matching ## heading."""
    content = RULE_FILE.read_text()
    for title in ("The Three Gates", "Gate Sequence", "When to Present Options"):
        assert f"[{title}]" in content, f"Contents is missing a link to '{title}'"
        assert re.search(rf"^## \S+ {title}$", content, re.MULTILINE), f"'{title}' is in Contents but has no ## heading"


def test_section_helper_flags_missing_gate():
    """Synthetic bad case: a rule with a gate removed yields an empty section."""
    trimmed = RULE_FILE.read_text().replace(GATE_HEADINGS[1], "### Placement (renamed)")
    assert gate_section(trimmed, 2) == "", "gate_section must return '' when a gate heading is missing"
    assert gate_section(trimmed, 1), "gate_section must still find the untouched gates"


def test_reference_helper_flags_missing_reference():
    """Synthetic bad case: a gate with no Reference line resolves to no files."""
    assert referenced_rule_files("### Gate 1️⃣: Naming\n**Check:** something\n") == [], \
        "referenced_rule_files must return [] when there is no Reference line"
