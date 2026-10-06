# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""No agent trigger competes with a skill for the same request.

On 2026-10-01 the technical_writer agent's "create confluence page" trigger clashed with the
confluence_create_page skill, so two artefacts answered one request. A trigger clashes when every
meaningful word in it appears in a skill's description, which is what Claude Code matches skills on.
"""
import re

from _shared_paths import CLAUDE_DIR

STOP_WORDS = {"a", "an", "the", "or", "and", "to", "of", "for", "with", "new", "my", "your"}
WORD = re.compile(r"[a-z0-9]+")


def frontmatter(text):
    """Return the YAML frontmatter block of a markdown file, or an empty string."""
    return text.split("\n---", 1)[0] if text.startswith("---\n") else ""


def triggers(agent_text):
    """Return an agent's trigger phrases, skipping slash commands."""
    block = re.search(r"^triggers:\n((?:  - .*\n)+)", frontmatter(agent_text) + "\n", re.M)
    items = re.findall(r'^  - "?([^"\n]+)"?$', block.group(1), re.M) if block else []
    return [item for item in items if not item.startswith("/")]


def description(skill_text):
    """Return a skill's frontmatter description, lower-cased."""
    match = re.search(r"^description: (.+)$", frontmatter(skill_text), re.M)
    return match.group(1).lower() if match else ""


def meaningful_words(phrase):
    """Return a phrase's words, lower-cased, without stop words."""
    return {w for w in WORD.findall(phrase.lower()) if w not in STOP_WORDS}


def clashes(trigger, skill_description):
    """Tell whether every meaningful word of a trigger appears in a skill's description."""
    words = meaningful_words(trigger)
    return bool(words) and words <= set(WORD.findall(skill_description))


def agent_files():
    """List every agent definition in the config."""
    return sorted((CLAUDE_DIR / "agents").rglob("AGENT.md"))


def skill_files():
    """List every skill definition in the config, skipping templates."""
    return sorted(p for p in (CLAUDE_DIR / "skills").rglob("SKILL.md") if "template" not in str(p).lower())


# ── the checks ───────────────────────────────────────────────────────────────


def test_triggers_are_read_without_slash_commands():
    """Quoted and unquoted triggers are read, and /commands are skipped."""
    text = '---\nname: a\ntriggers:\n  - /a\n  - "draft pr body"\n  - write notes\nmodel: x\n---\n# A\n'
    assert triggers(text) == ["draft pr body", "write notes"]


def test_no_triggers_gives_an_empty_list():
    """An agent without a triggers block has nothing to clash."""
    assert triggers("---\nname: a\n---\n# A\n") == []


def test_description_is_read_lower_cased():
    """A skill's description is read from frontmatter only."""
    assert description("---\nname: s\ndescription: Create a Page\n---\ndescription: body\n") == "create a page"


def test_stop_words_are_ignored():
    """Joining words don't count towards a clash."""
    assert meaningful_words("Create a new Confluence page") == {"create", "confluence", "page"}


def test_the_original_clash_is_caught():
    """The 2026-10-01 trigger clashes with the Confluence skill's description."""
    skill = "create, add, write or publish a confluence page from the general_page template"
    assert clashes("create confluence page", skill)
    assert clashes("write confluence page", skill)


def test_partial_overlap_is_not_a_clash():
    """Sharing some words isn't a clash, for example "draft pr body" against a PR-creating skill."""
    assert not clashes("draft pr body", "create github pr with staged changes, commit message, and pr body")


def test_agents_and_skills_are_found():
    """The scan finds agents and skills, or the clash check would pass vacuously."""
    assert agent_files(), "no agents found"
    assert len(skill_files()) >= 5, f"expected at least 5 skills, found {len(skill_files())}"


def test_no_agent_trigger_clashes_with_a_skill():
    """No agent trigger is fully covered by any skill's description."""
    found = []
    for agent in agent_files():
        for trigger in triggers(agent.read_text()):
            for skill in skill_files():
                if clashes(trigger, description(skill.read_text())):
                    found.append(f"{agent.parent.name} '{trigger}' vs {skill.parent.name}")
    assert not found, f"agent triggers that clash with a skill — drop the trigger or hand off to the skill: {found}"


def test_technical_writer_hands_confluence_pages_to_the_skill():
    """The technical writer sends direct Confluence requests to confluence_create_page, and needs no MCP."""
    text = (CLAUDE_DIR / "agents" / "core" / "technical_writer" / "AGENT.md").read_text()
    assert "use the confluence_create_page skill" in frontmatter(text), "the description lost its hand-off"
    assert "GitHub MCP" not in text, "the stale GitHub MCP requirement came back"
