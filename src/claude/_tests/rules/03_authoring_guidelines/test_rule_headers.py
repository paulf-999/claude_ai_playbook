# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-02
# Version:           1.3.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the rule-only ``applies_to``, ``miss_cost`` and ``loading`` headers defined in _claude_config_metadata.md.

Every always-on entry-point rule (the top-level files in tiers 01–04) declares which
sessions need it, as comma-separated globs or ``*`` alone, on the line after ``updated``.
Every entry-point rule, always-on or lazy, declares what a miss costs. A lazy rule whose
miss is ``high`` must load mechanically — through ``paths:`` or a hook — never on recall alone.
``make audit_rule_usage`` reads both headers, so a missing or malformed value skews the report.
Every entry point also says how it loads and why, and the mode must match its folder.
"""
import re
from pathlib import Path

from _shared_paths import HOOKS_DIR, RULES_DIR

ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_claude_reference")
LAZY_TIER = "05_lazy_load"
APPLIES_TO = re.compile(r"^<!-- applies_to: (.+) -->$", re.M)
MISS_COST = re.compile(r"^<!-- miss_cost: (high|medium|low) — \S.* -->$")
MISS_COST_PREFIX = "<!-- miss_cost:"
HEADER_PREFIX = "<!-- applies_to:"
EVERY_SESSION = "*"
# paths: frontmatter (up to 4) + version, created, updated, applies_to, miss_cost, loading
HEADER_LINES = 11
LOADING = re.compile(r"^<!-- loading: (always-on|path-scoped|lazy) — \S.* -->$")
LOADING_PREFIX = "<!-- loading:"
GLOB = re.compile(r"^[A-Za-z0-9_.*/\-{}?\[\]]+$")
HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"

VALID = "<!-- version: 1.0.0 -->\n<!-- created: 2026-10-01 -->\n<!-- updated: 2026-10-01 -->\n"


def applies_to_errors(content: str) -> list[str]:
    """Return problems with a rule's ``applies_to`` header; empty when it is valid.

    :param content: Rule file text.
    :return: One message per problem.
    """
    found = APPLIES_TO.findall(content)
    if not found:
        return ["no applies_to header"]
    if len(found) > 1:
        return ["more than one applies_to header"]
    lines = content.splitlines()
    position = next(i for i, line in enumerate(lines) if line.startswith(HEADER_PREFIX))
    if position == 0 or not lines[position - 1].startswith("<!-- updated:"):
        return ["applies_to must sit on the line straight after updated"]
    globs = [g.strip() for g in found[0].split(",")]
    if EVERY_SESSION in globs and len(globs) > 1:
        return ["* means every session, so it can't be mixed with other globs"]
    bad = [g for g in globs if not GLOB.match(g)]
    return [f"not a glob: {g!r}" for g in bad]


def has_header(content: str) -> bool:
    """Tell whether a file carries applies_to in its header block, not just in its body.

    :param content: File text.
    :return: True when one of the first ``HEADER_LINES`` lines is an applies_to line.
    """
    return any(line.startswith(HEADER_PREFIX) for line in content.splitlines()[:HEADER_LINES])


def always_on_entry_points() -> list[Path]:
    """List the top-level rule files in tiers 01–04.

    :return: Paths of the always-on entry-point rules.
    """
    return sorted(p for tier in ALWAYS_ON_TIERS for p in (RULES_DIR / tier).glob("*.md") if p.name != "README.md")


# --- Parser: accepted ---

def test_single_glob_accepted():
    """One glob on the line after updated is valid."""
    assert applies_to_errors(f"{VALID}<!-- applies_to: **/*.py -->\n# 🐍 Rule\n") == []


def test_several_globs_accepted():
    """Comma-separated globs are valid, with or without spaces after the commas."""
    assert applies_to_errors(f"{VALID}<!-- applies_to: **/_rules/**, **/CLAUDE.md -->\n") == []
    assert applies_to_errors(f"{VALID}<!-- applies_to: **/*.py,**/*.sh -->\n") == []


def test_every_session_accepted():
    """``*`` alone means the rule applies to every session."""
    assert applies_to_errors(f"{VALID}<!-- applies_to: * -->\n") == []


# --- Parser: rejected ---

def test_missing_header_rejected():
    """A rule with no applies_to line is reported."""
    assert applies_to_errors(f"{VALID}# 🐍 Rule\n") == ["no applies_to header"]


def test_duplicate_header_rejected():
    """Two applies_to lines are ambiguous."""
    content = f"{VALID}<!-- applies_to: * -->\n<!-- applies_to: **/*.py -->\n"
    assert applies_to_errors(content) == ["more than one applies_to header"]


def test_misplaced_header_rejected():
    """applies_to below the H1 isn't part of the header block."""
    errors = applies_to_errors(f"{VALID}# 🐍 Rule\n<!-- applies_to: * -->\n")
    assert errors == ["applies_to must sit on the line straight after updated"], errors


def test_star_mixed_with_globs_rejected():
    """``*`` with other globs is contradictory."""
    errors = applies_to_errors(f"{VALID}<!-- applies_to: *, **/*.py -->\n")
    assert errors == ["* means every session, so it can't be mixed with other globs"], errors


def test_prose_instead_of_glob_rejected():
    """Words with spaces aren't globs."""
    errors = applies_to_errors(f"{VALID}<!-- applies_to: python files -->\n")
    assert errors == ["not a glob: 'python files'"], errors


def test_empty_entry_rejected():
    """A trailing comma leaves an empty glob."""
    errors = applies_to_errors(f"{VALID}<!-- applies_to: **/*.py, -->\n")
    assert errors == ["not a glob: ''"], errors


# --- Real rules ---

def test_always_on_tiers_have_entry_points():
    """The scan finds the always-on rules, so an empty result can't pass silently."""
    entry_points = always_on_entry_points()
    assert len(entry_points) >= 10, f"expected at least 10 always-on entry points, found {len(entry_points)}"
    assert all(p.parent.name in ALWAYS_ON_TIERS for p in entry_points), "scan left tiers 01–04"


def test_every_always_on_entry_point_declares_applies_to():
    """Each always-on entry point carries a valid applies_to header."""
    problems = {p.relative_to(RULES_DIR).as_posix(): applies_to_errors(p.read_text()) for p in always_on_entry_points()}
    problems = {path: errors for path, errors in problems.items() if errors}
    assert not problems, f"applies_to problems {HINT}:\n  " + "\n  ".join(f"{k}: {v}" for k, v in problems.items())


def test_children_do_not_declare_applies_to():
    """Child files inherit from their parent, so only entry points carry the header."""
    children = [
        p for tier in ALWAYS_ON_TIERS for p in (RULES_DIR / tier).rglob("_*.md") if has_header(p.read_text())
    ]
    assert not children, f"child files with applies_to {HINT}: {children}"


def test_header_example_in_the_body_is_not_a_header():
    """An applies_to example deep in a file's body isn't treated as a header, but one on line 4 is."""
    body = f"{VALID}# 🗂️ Child\n" + "text\n" * HEADER_LINES + "<!-- applies_to: * -->\n"
    assert not has_header(body), "an example in the body was taken for a header"
    assert has_header(f"{VALID}<!-- applies_to: * -->\n"), "a real header on line 4 was missed"


# --- miss_cost ---

def miss_cost_errors(content: str) -> list[str]:
    """Return problems with a rule's ``miss_cost`` header; empty when it is valid.

    :param content: Rule file text.
    :return: One message per problem.
    """
    lines = content.splitlines()
    found = [i for i, line in enumerate(lines) if line.startswith(MISS_COST_PREFIX)]
    if not found:
        return ["no miss_cost header"]
    if len(found) > 1:
        return ["more than one miss_cost header"]
    position = found[0]
    above = lines[position - 1] if position else ""
    if not above.startswith(("<!-- updated:", HEADER_PREFIX)):
        return ["miss_cost must sit straight after updated or applies_to"]
    if not MISS_COST.match(lines[position]):
        return ["miss_cost must be high, medium or low, then ' — ' and a reason"]
    return []


def miss_cost_of(content: str) -> str:
    """Return a rule's miss cost level, or an empty string when it has none.

    :param content: Rule file text.
    :return: ``high``, ``medium``, ``low`` or ``""``.
    """
    match = next((MISS_COST.match(line) for line in content.splitlines() if MISS_COST.match(line)), None)
    return match.group(1) if match else ""


def has_mechanical_trigger(rel: str, content: str, hook_texts: list[str]) -> bool:
    """Tell whether a lazy rule loads without Claude having to remember it.

    :param rel: Rule path relative to ``_rules``.
    :param content: Rule file text.
    :param hook_texts: Text of every hook script.
    :return: True with ``paths:`` frontmatter or a hook that names the rule.
    """
    frontmatter = content.split("\n---", 1)[0] if content.startswith("---\n") else ""
    return "paths:" in frontmatter or any(rel in text for text in hook_texts)


def lazy_entry_points() -> list[Path]:
    """List the lazy rules that stand alone rather than belonging to a parent topic.

    :return: Paths of the lazy entry-point rules.
    """
    tier = RULES_DIR / LAZY_TIER
    found = []
    for path in sorted(tier.rglob("*.md")):
        if path.name == "README.md" or path.name.startswith("_") or "_lazy_load" in path.parts:
            continue
        parents = [p for p in path.parents if p != tier and tier in p.parents]
        if not any(p.with_suffix(".md").is_file() for p in parents):
            found.append(path)
    return found


def test_miss_cost_after_updated_accepted():
    """A miss_cost line straight after updated, as on a lazy rule, is valid."""
    assert miss_cost_errors(f"{VALID}<!-- miss_cost: low — style drift -->\n") == []


def test_miss_cost_after_applies_to_accepted():
    """A miss_cost line straight after applies_to, as on an always-on rule, is valid."""
    assert miss_cost_errors(f"{VALID}<!-- applies_to: * -->\n<!-- miss_cost: high — leaks secrets -->\n") == []


def test_miss_cost_problems_rejected():
    """Missing, duplicate, misplaced, unknown-level and reasonless headers are each reported."""
    assert miss_cost_errors(VALID) == ["no miss_cost header"]
    twice = f"{VALID}<!-- miss_cost: low — a -->\n<!-- miss_cost: low — b -->\n"
    assert miss_cost_errors(twice) == ["more than one miss_cost header"]
    assert miss_cost_errors(f"{VALID}# 🐍 Rule\n<!-- miss_cost: low — a -->\n") == [
        "miss_cost must sit straight after updated or applies_to"]
    bad_format = ["miss_cost must be high, medium or low, then ' — ' and a reason"]
    assert miss_cost_errors(f"{VALID}<!-- miss_cost: severe — a -->\n") == bad_format
    assert miss_cost_errors(f"{VALID}<!-- miss_cost: low -->\n") == bad_format


def test_trigger_detection():
    """paths: frontmatter or a hook naming the rule counts as a trigger, and a pointer alone doesn't."""
    rel = "05_lazy_load/x.md"
    assert has_mechanical_trigger(rel, '---\npaths:\n  - "**/*.sql"\n---\n# X\n', [])
    assert has_mechanical_trigger(rel, "# X\n", [f'cat "$ROOT/_rules/{rel}"'])
    assert not has_mechanical_trigger(rel, "# X\n", ["echo unrelated"]), "a rule nothing loads has no trigger"


def test_lazy_tier_has_entry_points():
    """The lazy scan finds rules, and skips children of a parent topic."""
    names = [p.name for p in lazy_entry_points()]
    assert len(names) >= 15, f"expected at least 15 lazy entry points, found {len(names)}"
    assert "formatting.md" not in names, "sql/formatting.md is a child of sql.md, not an entry point"


def test_every_entry_point_declares_miss_cost():
    """Each always-on and lazy entry point carries a valid miss_cost header."""
    problems = {
        p.relative_to(RULES_DIR).as_posix(): miss_cost_errors(p.read_text())
        for p in always_on_entry_points() + lazy_entry_points()
    }
    problems = {path: errors for path, errors in problems.items() if errors}
    assert not problems, f"miss_cost problems {HINT}:\n  " + "\n  ".join(f"{k}: {v}" for k, v in problems.items())


def test_high_cost_lazy_rules_load_mechanically():
    """A lazy rule that is costly to miss must have paths: or a hook, not rely on Claude remembering it."""
    hook_texts = [h.read_text() for h in HOOKS_DIR.glob("*.sh")]
    untriggered = [
        p.relative_to(RULES_DIR).as_posix() for p in lazy_entry_points()
        if miss_cost_of(p.read_text()) == "high"
        and not has_mechanical_trigger(p.relative_to(RULES_DIR).as_posix(), p.read_text(), hook_texts)
    ]
    assert not untriggered, (
        f"high miss_cost lazy rules with no trigger: {untriggered} — add paths: frontmatter, "
        f"a hook that loads it, or move it to an always-on tier {HINT}"
    )


# --- loading ---

def loading_errors(content: str, expected: str) -> list[str]:
    """Return problems with a rule's ``loading`` header; empty when it is valid.

    :param content: Rule file text.
    :param expected: The mode the rule's folder and frontmatter imply.
    :return: One message per problem.
    """
    lines = content.splitlines()
    found = [i for i, line in enumerate(lines) if line.startswith(LOADING_PREFIX)]
    if not found:
        return ["no loading header"]
    if len(found) > 1:
        return ["more than one loading header"]
    position = found[0]
    if not position or not lines[position - 1].startswith(MISS_COST_PREFIX):
        return ["loading must sit straight after miss_cost"]
    match = LOADING.match(lines[position])
    if not match:
        return ["loading must be always-on, path-scoped or lazy, then ' — ' and a reason"]
    if match.group(1) != expected:
        return [f"loading says {match.group(1)} but the rule is {expected}"]
    return []


def expected_loading(path, content: str) -> str:
    """Return the loading mode a rule's location and frontmatter imply.

    :param path: Rule file path.
    :param content: Rule file text.
    :return: ``always-on``, ``path-scoped`` or ``lazy``.
    """
    if path.relative_to(RULES_DIR).parts[0] in ALWAYS_ON_TIERS:
        return "always-on"
    frontmatter = content.split("\n---", 1)[0] if content.startswith("---\n") else ""
    return "path-scoped" if "paths:" in frontmatter else "lazy"


LOADING_LINE = "<!-- miss_cost: low — a -->\n<!-- loading: {} — a reason -->\n"


def test_loading_after_miss_cost_accepted():
    """Each mode is valid when it matches the rule and sits straight after miss_cost."""
    for mode in ("always-on", "path-scoped", "lazy"):
        assert loading_errors(VALID + LOADING_LINE.format(mode), mode) == [], f"{mode} was rejected"


def test_loading_problems_rejected():
    """Missing, duplicate, misplaced, unknown, reasonless and mismatched headers are each reported."""
    miss = "<!-- miss_cost: low — a -->\n"
    assert loading_errors(VALID + miss, "lazy") == ["no loading header"]
    twice = VALID + LOADING_LINE.format("lazy") + "<!-- loading: lazy — b -->\n"
    assert loading_errors(twice, "lazy") == ["more than one loading header"]
    assert loading_errors(VALID + "<!-- loading: lazy — a -->\n", "lazy") == [
        "loading must sit straight after miss_cost"]
    bad_format = ["loading must be always-on, path-scoped or lazy, then ' — ' and a reason"]
    assert loading_errors(VALID + miss + "<!-- loading: sometimes — a -->\n", "lazy") == bad_format
    assert loading_errors(VALID + miss + "<!-- loading: lazy -->\n", "lazy") == bad_format
    assert loading_errors(VALID + LOADING_LINE.format("lazy"), "always-on") == [
        "loading says lazy but the rule is always-on"]


def test_expected_loading_follows_folder_and_frontmatter():
    """Tiers 01–04 are always-on, and lazy rules are path-scoped only with paths: frontmatter."""
    lazy = RULES_DIR / LAZY_TIER / "x.md"
    assert expected_loading(RULES_DIR / "02_claude_standards" / "x.md", "# X\n") == "always-on"
    assert expected_loading(lazy, '---\npaths:\n  - "**/*.sql"\n---\n# X\n') == "path-scoped"
    assert expected_loading(lazy, "# X\n") == "lazy"


def test_every_entry_point_declares_loading():
    """Each always-on and lazy entry point says how it loads and why, matching its folder and frontmatter."""
    problems = {
        p.relative_to(RULES_DIR).as_posix(): loading_errors(p.read_text(), expected_loading(p, p.read_text()))
        for p in always_on_entry_points() + lazy_entry_points()
    }
    problems = {path: errors for path, errors in problems.items() if errors}
    assert not problems, f"loading problems {HINT}:\n  " + "\n  ".join(f"{k}: {v}" for k, v in problems.items())
