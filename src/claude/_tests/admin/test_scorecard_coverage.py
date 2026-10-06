# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Every hook, agent and skill has a scorecard on its folder's dimensions, and the summaries add up.

Each scorecard's Overall must be the mean of its dimension rows, its Recommended improvements must
appear exactly when Overall is below 8.5, and each summary's Scored count and Overall must match
the scorecards they roll up.
"""
import re

from _shared_paths import CLAUDE_DIR

CARDS = CLAUDE_DIR / "_admin" / "_quality_scorecards"
HOOK_NAMES = sorted(p.stem for p in (CLAUDE_DIR / "hooks").glob("hook_*.sh"))
AGENT_NAMES = sorted(p.parent.name for p in (CLAUDE_DIR / "agents").rglob("AGENT.md"))
SKILL_NAMES = sorted(
    p.parent.name for p in (CLAUDE_DIR / "skills").rglob("SKILL.md")
    if not any(part.startswith(".") for part in p.relative_to(CLAUDE_DIR / "skills").parts)
)
KINDS = {
    "hooks": (HOOK_NAMES, "hook_scorecards_summary.md", "Hooks"),
    "agents": (AGENT_NAMES, "agent_scorecards_summary.md", "Agents"),
    "skills": (SKILL_NAMES, "skill_scorecards_summary.md", "Skills"),
}
# Skills keep their dimensions in the scorecard template rather than a folder README
SKILL_TEMPLATE = CLAUDE_DIR / "_templates" / "skills" / "_quality_scorecard_template.md"
TEMPLATE_DIM = re.compile(r"^\| \*\*([^*]+)\*\* \| X/10 \|", re.M)
DIM_ROW = re.compile(r"^\| \*\*([^*]+)\*\* \| (\d+)/10 \|", re.M)
OVERALL_ROW = re.compile(r"^\| \*\*Overall\*\* \| \*\*([\d.]+)/10\*\* \|", re.M)
HEADER_SCORE = re.compile(r"^\*\*Overall score:\*\* ([\d.]+)/10$", re.M)
README_DIM = re.compile(r"^\| \*\*([^*]+)\*\* \| [^|]+ \| [^|]+ \|$", re.M)
FIX_THRESHOLD = 8.5


def dimensions(readme_text):
    """Return the dimension names a folder README defines, in order."""
    return README_DIM.findall(readme_text)


def template_dimensions(template_text):
    """Return the dimension names a scorecard template defines, in order, without Overall."""
    return [name for name in TEMPLATE_DIM.findall(template_text) if name != "Overall"]


def folder_dimensions(folder):
    """Return a folder's dimensions from its README, or from the skill template for skills."""
    readme = CARDS / folder / "README.md"
    return dimensions(readme.read_text()) if readme.is_file() else template_dimensions(SKILL_TEMPLATE.read_text())


def card_scores(text):
    """Return (dimension rows, table overall, header overall) parsed from a scorecard."""
    rows = [(name, int(score)) for name, score in DIM_ROW.findall(text) if name != "Overall"]
    table = OVERALL_ROW.search(text)
    header = HEADER_SCORE.search(text)
    return rows, float(table.group(1)) if table else None, float(header.group(1)) if header else None


def mean(values):
    """Average to one decimal place, the way scorecards round."""
    return round(sum(values) / len(values), 1)


def summary_row(text, group):
    """Return (scored, overall) from a summary's row for a group, or None."""
    match = re.search(rf"^\| {re.escape(group)} \| (\d+) \| ([\d.]+)/10 \|", text, re.M)
    return (int(match.group(1)), float(match.group(2))) if match else None


SAMPLE = """**Overall score:** 8.5/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-01 | • a |
| **Cost** | 9/10 | 2026-10-01 | • b |
| **Overall** | **8.5/10** | 2026-10-01 | • c |
"""


# ── parsing ──────────────────────────────────────────────────────────────────


def test_scorecard_rows_and_overalls_are_read():
    """Dimension rows, the table Overall and the header Overall are all parsed."""
    rows, table, header = card_scores(SAMPLE)
    assert rows == [("Clarity", 8), ("Cost", 9)], rows
    assert (table, header) == (8.5, 8.5), (table, header)


def test_mean_rounds_to_one_decimal():
    """The mean matches how scorecards round, for example 8.857 to 8.9."""
    assert mean([9, 8, 8, 9, 9, 10, 9]) == 8.9
    assert mean([7, 7]) == 7.0


def test_readme_dimensions_are_read():
    """A README's dimension table yields names in order, skipping the header row."""
    text = "| Dimension | What | 10 |\n|---|---|---|\n| **Clarity** | a | b |\n| **Cost** | c | d |\n"
    assert dimensions(text) == ["Clarity", "Cost"]


def test_template_dimensions_are_read():
    """A scorecard template's placeholder rows yield dimension names, without Overall."""
    text = "| **Design** | X/10 | YYYY-MM-DD | a |\n| **Security** | X/10 | YYYY-MM-DD | b |\n"
    text += "| **Overall** | **X.X/10** | YYYY-MM-DD | c |\n"
    assert template_dimensions(text) == ["Design", "Security"], template_dimensions(text)


def test_summary_row_is_read():
    """A summary's group row yields its Scored count and Overall."""
    assert summary_row("| Hooks | 5 | 8.5/10 | 2026-10-01 | x |", "Hooks") == (5, 8.5)
    assert summary_row("| Hooks | 0 | — | — | x |", "Hooks") is None


# ── the real scorecards ──────────────────────────────────────────────────────


def test_every_hook_agent_and_skill_has_a_scorecard():
    """Each hook script, agent and skill has its own scorecard."""
    for folder, (names, _, _) in KINDS.items():
        assert names, f"no {folder} found, so this check proves nothing"
        missing = [n for n in names if not (CARDS / folder / f"scorecard_{n}.md").is_file()]
        assert not missing, f"{folder} with no scorecard: {missing}"


def test_scorecards_use_their_folder_dimensions():
    """Each hook, agent and skill scorecard has exactly its folder's 7 dimensions, in order."""
    for folder, (names, _, _) in KINDS.items():
        dims = folder_dimensions(folder)
        assert len(dims) == 7, f"{folder} should define 7 dimensions, found {dims}"
        for name in names:
            rows, _, _ = card_scores((CARDS / folder / f"scorecard_{name}.md").read_text())
            assert [d for d, _ in rows] == dims, f"{name} dimensions {[d for d, _ in rows]} don't match {dims}"


def test_overall_is_the_mean_and_matches_the_header():
    """Each scorecard's Overall is the mean of its rows, and the header repeats it."""
    for folder, (names, _, _) in KINDS.items():
        for name in names:
            rows, table, header = card_scores((CARDS / folder / f"scorecard_{name}.md").read_text())
            assert table == mean([s for _, s in rows]), f"{name}: Overall {table} isn't the mean of its rows"
            assert header == table, f"{name}: header says {header}, table says {table}"


def test_improvements_appear_only_below_the_threshold():
    """Recommended improvements are listed exactly when Overall is below 8.5."""
    for folder, (names, _, _) in KINDS.items():
        for name in names:
            text = (CARDS / folder / f"scorecard_{name}.md").read_text()
            _, table, _ = card_scores(text)
            listed = "**Recommended improvements:**" in text
            assert listed == (table < FIX_THRESHOLD), f"{name}: Overall {table} but improvements listed={listed}"


def test_summaries_add_up():
    """Each type summary's Scored and Overall match its scorecards, and so does the overall summary."""
    overall_text = (CARDS / "quality_scorecards_summary.md").read_text()
    for folder, (names, summary_name, group) in KINDS.items():
        overalls = [card_scores((CARDS / folder / f"scorecard_{n}.md").read_text())[1] for n in names]
        expected = (len(names), mean(overalls))
        assert summary_row((CARDS / folder / summary_name).read_text(), group) == expected, f"{summary_name} is stale"
        assert summary_row(overall_text, group) == expected, f"quality_scorecards_summary.md's {group} row is stale"
