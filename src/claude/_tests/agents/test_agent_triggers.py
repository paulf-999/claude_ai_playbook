# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-11
# Version:           2.0.0
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
    skills_dir = CLAUDE_DIR / "skills"
    return sorted(p for p in skills_dir.rglob("SKILL.md") if "template" not in str(p.relative_to(skills_dir)).lower())


# ── the checks ───────────────────────────────────────────────────────────────


def test_triggers_are_read_without_slash_commands():
    """Quoted and unquoted triggers are read, and /commands are skipped."""
    text = '---\nname: a\ntriggers:\n  - /a\n  - "draft pr body"\n  - write notes\nmodel: x\n---\n# A\n'
    assert triggers(text) == ["draft pr body", "write notes"], "both listed triggers should be read"


def test_no_triggers_gives_an_empty_list():
    """An agent without a triggers block has nothing to clash."""
    assert triggers("---\nname: a\n---\n# A\n") == [], "an agent with no triggers list has none"


def test_description_is_read_lower_cased():
    """A skill's description is read from frontmatter only."""
    text = "---\nname: s\ndescription: Create a Page\n---\ndescription: body\n"
    assert description(text) == "create a page", "only the frontmatter description counts, lower-cased"


def test_stop_words_are_ignored():
    """Joining words don't count towards a clash."""
    words = meaningful_words("Create a new Confluence page")
    assert words == {"create", "confluence", "page"}, f"filler words should be dropped, got {words}"


def test_the_original_clash_is_caught():
    """The 2026-10-01 trigger clashes with the Confluence skill's description."""
    skill = "create, add, write or publish a confluence page from the general_page template"
    assert clashes("create confluence page", skill), "a trigger fully covered by the skill should clash"
    assert clashes("write confluence page", skill), "a reworded trigger still covered by the skill should clash"


def test_partial_overlap_is_not_a_clash():
    """Sharing some words isn't a clash, for example "draft pr body" against a PR-creating skill."""
    skill = "create github pr with staged changes, commit message, and pr body"
    assert not clashes("draft pr body", skill), "a trigger with words the skill lacks should not clash"


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
