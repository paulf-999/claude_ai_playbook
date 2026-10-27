# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-11
# Date updated:      2026-10-27
# Version:           2.2.0
# Test quality score: 10/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that rule files point at things that exist and agree with the files they repeat.

Rule guidance is instructional, so its wording isn't pinned. What can break silently
is a pointer to a moved file, or two copies of one fact drifting apart, so each test
checks one of those. Merged on 2026-10-11 from seven per-rule test files: writing_style,
_decision_making, _security_guardrails, authoring_rules, _artefact_proposal_gates,
claude_operational_efficiency and git. Also checks every ``make`` target a rule names exists.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from _shared_paths import (
    CLAUDE_DIR,
    HOOKS_DIR,
    LAZY_RULES_DIR,
    RULES_DIR,
    SETTINGS_FILE,
    SKILLS_DIR,
    resolve_config_path,
)

BEHAVIOUR_DIR = RULES_DIR / "02_claude_standards" / "behaviour"
RULE_TIERS = (
    "01_essentials", "02_claude_standards", "03_authoring_guidelines", "02_claude_standards/path_scoped_rules",
)

# ── writing_style.md ─────────────────────────────────────

WRITING_STYLE = RULES_DIR / "01_essentials" / "claude_usage_standards" / "writing_style.md"


# Names writing_style.md uses as made-up examples, not as real files
WRITING_STYLE_EXAMPLE_NAMES = {"behavior.md", "claude_code_automation_commands.md"}


def test_writing_style_names_real_files():
    """Every file writing_style.md names exists, apart from its deliberate made-up examples."""
    names = set(re.findall(r"`([A-Za-z_][\w.]*\.(?:py|md))`", WRITING_STYLE.read_text()))
    assert names, "writing_style.md should name some files"
    missing = sorted(name for name in names - WRITING_STYLE_EXAMPLE_NAMES if not any(CLAUDE_DIR.rglob(name)))
    assert not missing, f"writing_style.md names missing files — fix the name or list it as an example: {missing}"


def test_writing_style_points_to_its_multifile_child():
    """writing_style.md names its multifile-organisation child, and the child exists."""
    child = WRITING_STYLE.parent / "multifile_document_organisation.md"
    assert "/claude_usage_standards/multifile_document_organisation.md" in WRITING_STYLE.read_text(), (
        "writing_style.md no longer names its multifile child"
    )
    assert child.is_file(), f"the named child is missing: {child}"


# ── _security_guardrails.md ──────────────────────────────

GUARDRAILS = RULES_DIR / "02_claude_standards" / "security" / "_security_guardrails.md"


def too_broad() -> list[str]:
    """List the wildcard permissions the guardrails name as too broad, such as ``Bash(git:*)``."""
    line = next(
        (x for x in GUARDRAILS.read_text().splitlines() if "Never recommend wildcards for destructive commands" in x),
        "",
    )
    return re.findall(r"`(Bash\([^`]+\))`", line)


def test_guardrails_name_the_destructive_wildcards():
    """The guardrails name the wildcards they forbid, so the settings check can't pass on an empty list."""
    broad = too_broad()
    assert "Bash(git:*)" in broad, f"the guardrails should name Bash(git:*) as too broad, found {broad}"
    assert "Bash(rm -rf:*)" in broad, (  # wording-check: list the settings check uses
        f"the guardrails should name Bash(rm -rf:*) as too broad, found {broad}"
    )


def test_settings_allow_none_of_the_forbidden_wildcards():
    """settings.json allows none of the wildcards the guardrails call too broad."""
    allow = set(json.loads(SETTINGS_FILE.read_text())["permissions"]["allow"])
    broken = sorted(allow & set(too_broad()))
    assert not broken, f"settings.json allows {broken}, which the security guardrails forbid"


# ── authoring_rules.md ───────────────────────────────────

AUTHORING_RULES = RULES_DIR / "03_authoring_guidelines" / "authoring_rules.md"


def test_authoring_rules_template_exists():
    """The rule template the guide names exists."""
    assert "_templates/rule.md.template" in AUTHORING_RULES.read_text(), "the guide no longer names the rule template"
    assert (CLAUDE_DIR / "_templates" / "rule.md.template").is_file(), "_templates/rule.md.template is missing"


def test_authoring_rules_tiers_exist():
    """Each tier the guide offers is a real folder."""
    text = AUTHORING_RULES.read_text()
    missing = [t for t in RULE_TIERS if f"`{t}/`" not in text or not (RULES_DIR / t).is_dir()]
    assert not missing, f"tiers missing from the guide or from rules/: {missing}"


def test_authoring_rules_scorecard_readme_exists():
    """The scorecard README the guide points to exists."""
    readme = CLAUDE_DIR / "_reference" / "_quality_scorecards" / "rules" / "README.md"
    assert readme.is_file(), f"the guide points to a scorecard template that's gone: {readme}"


def test_authoring_rules_on_demand_children_exist():
    """Every on-demand child the guide names exists."""
    paths = re.findall(r"\*\*Read on demand:\*\* `~/[^/]+/([^`]+)`", AUTHORING_RULES.read_text())
    assert len(paths) == 3, f"expected the common-mistakes, hard-gates and rule-lifecycle pointers, found {paths}"
    missing = [p for p in paths if not resolve_config_path(CLAUDE_DIR, p).is_file()]
    assert not missing, f"Read-on-demand pointers to missing files: {missing}"


def test_authoring_rules_structure_test_exists():
    """The structural test every rule must pass is where the guide says."""
    assert "test_rules_structure.py" in AUTHORING_RULES.read_text(), "the guide no longer names test_rules_structure.py"
    assert (CLAUDE_DIR / "_tests" / "rules" / "test_rules_structure.py").is_file(), "test_rules_structure.py is gone"


# ── _artefact_proposal_gates.md ──────────────────────────

GATES = BEHAVIOUR_DIR / "_artefact_proposal_gates.md"
GATES_PARENT = RULES_DIR / "02_claude_standards" / "behaviour.md"
SKILL_DOMAINS = RULES_DIR / "03_authoring_guidelines" / "authoring_skills" / "skill_domains.yaml"
GATE_HEADINGS = ["### Gate 1️⃣: Naming", "### Gate 2️⃣: Placement", "### Gate 3️⃣: Duplication"]
GATE_TIERS = {tier: RULES_DIR / tier for tier in RULE_TIERS} | {"_rules_lazy_load": LAZY_RULES_DIR}


def gate_section(content: str, number: int) -> str:
    """Return one gate's text, from its heading to the next ``---``, or ``""`` if the heading is missing."""
    start = content.find(GATE_HEADINGS[number - 1])
    if start == -1:
        return ""
    end = content.find("\n---", start)
    return content[start:] if end == -1 else content[start:end]


def referenced_rule_files(section: str) -> list[Path]:
    """Resolve every file a gate's **Reference:** line names, parent first, then its ``_child.md`` names."""
    match = re.search(r"\*\*Reference:\*\* `~/[^/`]+/((?:rules|_rules_lazy_load)/[^`]+)\.md`(.*)", section)
    if not match:
        return []
    parent = CLAUDE_DIR / f"{match.group(1)}.md"
    children = re.findall(r"`(_[a-z_]+\.md)`", match.group(2))
    return [parent] + [parent.with_suffix("") / child for child in children]


def test_gates_parent_points_to_the_rule():
    """behaviour.md names where the gates load from, and the gates have no paths: frontmatter."""
    assert "`rules/02_claude_standards/behaviour/_artefact_proposal_gates.md`" in GATES_PARENT.read_text(), (
        "behaviour.md lost its pointer to _artefact_proposal_gates.md"
    )
    assert not GATES.read_text().startswith("---"), "the gates must load every session — remove the frontmatter"


def test_gates_naming_examples_exist():
    """Every skill, hook and agent Gate 1 uses as an example is real."""
    section = gate_section(GATES.read_text(), 1)
    skills = {path.parent.name for path in SKILLS_DIR.rglob("SKILL.md")}
    for skill in ("confluence_create_page", "jira_create"):
        assert f"`{skill}`" in section, f"Gate 1 no longer uses {skill} as an example — update this test"
        assert skill in skills, f"Gate 1 example skill {skill} doesn't exist under skills/"
    assert (HOOKS_DIR / "hook_enforcement_naming_convention.sh").is_file(), "Gate 1 example hook no longer exists"
    agent = CLAUDE_DIR / "agents" / "core" / "technical_writer" / "AGENT.md"
    assert agent.is_file(), "Gate 1 example agent no longer exists"


def test_gates_example_domains_are_registered():
    """The skill domains Gate 1 relies on are listed in skill_domains.yaml."""
    domains = set(re.findall(r"^\s*- id: ([a-z_]+)$", SKILL_DOMAINS.read_text(), re.MULTILINE))
    for domain in ("confluence", "jira"):
        assert domain in domains, (
            f"Domain '{domain}' is missing from skill_domains.yaml, which Gate 1 tells Claude to check"
        )


def test_gates_placement_names_every_tier():
    """Gate 2 lists all five rule folders, and each one exists."""
    section = gate_section(GATES.read_text(), 2)
    for tier, folder in GATE_TIERS.items():
        assert f"**{tier}/**" in section, f"Gate 2 no longer lists the {tier}/ tier"
        assert folder.is_dir(), f"Gate 2 lists {tier}/, but {folder} doesn't exist"


def test_gates_reference_files_exist():
    """Every file a gate's Reference line points to exists."""
    content = GATES.read_text()
    for number in (1, 2, 3):
        paths = referenced_rule_files(gate_section(content, number))
        assert paths, f"Gate {number}'s Reference line no longer names a ~/<config>/rules/ or _rules_lazy_load/ file"
        for path in paths:
            assert path.is_file(), f"Gate {number} points to {path}, which doesn't exist — update the Reference line"


def test_gate_section_flags_a_missing_gate():
    """Synthetic bad case: a rule with a gate removed yields an empty section."""
    trimmed = GATES.read_text().replace(GATE_HEADINGS[1], "### Placement (renamed)")
    assert gate_section(trimmed, 2) == "", "gate_section must return '' when a gate heading is missing"
    assert gate_section(trimmed, 1), "gate_section must still find the untouched gates"


def test_reference_helper_flags_a_missing_reference():
    """Synthetic bad case: a gate with no Reference line resolves to no files."""
    assert referenced_rule_files("### Gate 1️⃣: Naming\n**Check:** something\n") == [], (
        "referenced_rule_files must return [] when there is no Reference line"
    )


# ── claude_operational_efficiency.md ─────────────────────

EFFICIENCY_DIR = RULES_DIR / "02_claude_standards" / "claude_working_practices"
EFFICIENCY = EFFICIENCY_DIR / "claude_operational_efficiency.md"
EFFICIENCY_CHILDREN = EFFICIENCY_DIR / "claude_operational_efficiency"
LOADS_ON_ITS_OWN = re.compile(r"^- \*\*Loads on its own from:\*\* `rules/(\S+)`$", re.MULTILINE)


def efficiency_children() -> list[str]:
    """Return every child the efficiency rule says loads on its own, relative to ``rules/``."""
    return LOADS_ON_ITS_OWN.findall(EFFICIENCY.read_text())


def test_efficiency_children_resolve_inside_their_folder():
    """Every child the efficiency rule names exists inside its own subfolder."""
    assert EFFICIENCY_CHILDREN.is_dir(), f"Child folder missing: {EFFICIENCY_CHILDREN}"
    for path in efficiency_children():
        target = RULES_DIR / path
        assert target.is_file(), f"child pointer does not resolve: {path}"
        assert target.parent == EFFICIENCY_CHILDREN, f"child pointer {path} points outside {EFFICIENCY_CHILDREN.name}/"


def test_efficiency_has_no_orphaned_children():
    """Every ``.md`` file in the child folder is named by the parent."""
    named = {path.rsplit("/", 1)[-1] for path in efficiency_children()}
    orphans = {child.name for child in EFFICIENCY_CHILDREN.glob("*.md")} - named
    assert not orphans, f"Children never named by the parent (silently unreachable): {sorted(orphans)}"


def test_efficiency_contents_match_headings():
    """Every Contents entry in the efficiency rule names a real ``##`` heading."""
    text = EFFICIENCY.read_text()
    entries = re.findall(r"^- \[([^\]]+)\]\(#", text, re.MULTILINE)
    headings = [re.sub(r"^[^\w]+", "", h).strip() for h in re.findall(r"^## (.+)$", text, re.MULTILINE)]
    assert entries, "Contents section has no entries"
    missing = [entry for entry in entries if entry not in headings]
    assert not missing, f"Contents entries with no matching ## heading: {missing}"


# ── git.md ───────────────────────────────────────────────

GIT_RULES = RULES_DIR / "02_claude_standards" / "git.md"
GIT_CHILDREN = ("_safe_patterns.md", "_commits.md", "_concurrent_sessions.md")


def branch_pattern() -> re.Pattern[str]:
    """Compile the branch-name pattern git.md documents as ``**Pattern:**``."""
    match = re.search(r"\*\*Pattern:\*\* `([^`]+)`", GIT_RULES.read_text())
    assert match, "git.md must document its branch-name regex as **Pattern:** `...`"
    return re.compile(match.group(1))


def test_git_points_to_every_child():
    """git.md names each child it loads beside, so a reader can find them all."""
    text = GIT_RULES.read_text()
    for child in GIT_CHILDREN:
        assert f"**Loads on its own from:** `rules/02_claude_standards/git/{child}`" in text, (
            f"git.md must point to git/{child}"
        )


def test_git_children_exist():
    """Each child git.md points to is on disk."""
    missing = [c for c in GIT_CHILDREN if not (GIT_RULES.parent / "git" / c).is_file()]
    assert not missing, f"git.md points to children that don't exist: {missing}"


def test_git_branch_pattern_accepts_its_examples():
    """Every example branch git.md gives matches its own pattern."""
    examples_line = GIT_RULES.read_text().split("**Examples:**", 1)[1].split("\n")[0]
    examples = re.findall(r"`((?:feature|hotfix|release)/[^`]+)`", examples_line)
    assert len(examples) >= 3, f"expected an example for each prefix, found {examples}"
    bad = [e for e in examples if not branch_pattern().fullmatch(e)]
    assert not bad, f"git.md's own examples break its pattern: {bad}"


def test_git_branch_pattern_rejects_bad_names():
    """Hyphens, capitals, a missing prefix or an unknown prefix all fail git.md's pattern."""
    for name in ("feature/add-pr-template", "feature/AddTemplate", "add_pr_template", "bugfix/x"):
        assert not branch_pattern().fullmatch(name), f"'{name}' should not match the branch pattern"


# ── make targets named in rules ──────────────────────────

REPO_ROOT = CLAUDE_DIR.parent.parent
MAKE_TARGET_REF = re.compile(r"`make ([a-z_]+)")
MAKE_TARGET_DEF = re.compile(r"^([a-z_]+):", re.MULTILINE)


def rule_make_targets() -> set[str]:
    """Return every target named as `` `make <target>` `` in a rule file.

    :return: The target names, e.g. ``{"install", "enable_mcp"}``.
    """
    return {target for path in RULES_DIR.rglob("*.md") for target in MAKE_TARGET_REF.findall(path.read_text())}


def defined_make_targets(root: Path) -> set[str]:
    """Return the targets defined in a repo's root ``Makefile`` and its ``src/make/*.mk`` includes.

    :param root: The repo root holding ``Makefile``.
    :return: The defined target names.
    """
    makefiles = [root / "Makefile", *sorted((root / "src" / "make").glob("*.mk"))]
    return {target for path in makefiles if path.is_file() for target in MAKE_TARGET_DEF.findall(path.read_text())}


def test_rules_name_only_real_make_targets():
    """Every `make <target>` a rule tells the user to run is defined in the repo's makefiles."""
    if not (REPO_ROOT / "Makefile").is_file() or REPO_ROOT / "src" / "claude" != CLAUDE_DIR:
        pytest.skip("no repo Makefile beside this config — a live install has none")
    named = rule_make_targets()
    assert named, "no `make <target>` found in rules — the pattern may be wrong"
    missing = sorted(named - defined_make_targets(REPO_ROOT))
    assert not missing, f"rules name make targets that don't exist: {missing}"


def test_make_target_helpers_flag_a_missing_target(tmp_path: Path):
    """Targets come from the root Makefile and src/make/*.mk, and variables and .PHONY don't count."""
    (tmp_path / "src" / "make").mkdir(parents=True)
    (tmp_path / "Makefile").write_text("SHELL := bash\ninstall:\n\t@echo hi\n.PHONY: install\n")
    (tmp_path / "src" / "make" / "mcp.mk").write_text("enable_mcp:\n\t@echo on\n")
    assert defined_make_targets(tmp_path) == {"install", "enable_mcp"}, "only real targets should be found"
