# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the rule-only ``applies_to`` header defined in _claude_config_metadata.md.

Every always-on entry-point rule (the top-level files in tiers 01–04) declares which
sessions need it, as comma-separated globs or ``*`` alone, on the line after ``updated``.
``make audit_rule_usage`` reads it, so a missing or malformed value skews the report.
"""
import re

from _shared_paths import RULES_DIR

ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_claude_reference")
APPLIES_TO = re.compile(r"^<!-- applies_to: (.+) -->$", re.M)
HEADER_PREFIX = "<!-- applies_to:"
EVERY_SESSION = "*"
HEADER_LINES = 6  # version, created, updated, applies_to, miss_cost, plus paths: frontmatter slack
GLOB = re.compile(r"^[A-Za-z0-9_.*/\-{}?\[\]]+$")
HINT = "— see 03_authoring_guidelines/shared_standards/_claude_config_metadata.md"

VALID = "<!-- version: 1.0.0 -->\n<!-- created: 2026-10-01 -->\n<!-- updated: 2026-10-01 -->\n"


def applies_to_errors(content: str) -> list[str]:
    """Return problems with a rule's ``applies_to`` header; empty when it is valid.

    :param content: Rule file text.
    :type content: str
    :return: One message per problem.
    :rtype: list[str]
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
    :type content: str
    :return: True when one of the first ``HEADER_LINES`` lines is an applies_to line.
    :rtype: bool
    """
    return any(line.startswith(HEADER_PREFIX) for line in content.splitlines()[:HEADER_LINES])


def always_on_entry_points() -> list:
    """List the top-level rule files in tiers 01–04.

    :return: Paths of the always-on entry-point rules.
    :rtype: list
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
