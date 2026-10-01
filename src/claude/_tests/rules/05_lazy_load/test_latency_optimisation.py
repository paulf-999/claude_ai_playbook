# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-17
# Date updated:      2026-10-01
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content tests for _rules/05_lazy_load/latency_optimisation.md.

Guards the file's name and opening, and the guidance it sets: tune latency only
when it's blocking, use effort as the lever, measure first, and revert if quality
drops. It also stops the rule drifting back to temperature advice the API rejects:
current models refuse ``temperature`` and older ones only accept 0 to 1.
"""
from __future__ import annotations

import re

from _shared_paths import RULES_DIR

RULE_FILE = RULES_DIR / "05_lazy_load" / "latency_optimisation.md"


def content() -> str:
    """Read latency_optimisation.md.

    :return: The rule's text.
    :rtype: str
    """
    return RULE_FILE.read_text()


def test_british_file_name():
    """The rule lives at the British spelling, and the old American name is gone."""
    assert RULE_FILE.is_file(), f"expected {RULE_FILE}"
    assert not (RULE_FILE.parent / "latency_optimization.md").exists(), "the old American-spelled file is back"


def test_no_memory_frontmatter():
    """The rule doesn't open with leftover memory-schema frontmatter."""
    assert not content().startswith("---\n"), "rule files open with the metadata header, not YAML frontmatter"


def test_opens_with_metadata_and_emoji_h1():
    """The rule opens with its metadata header comments and then an emoji H1."""
    lines = content().splitlines()
    assert lines[0].startswith("<!-- version: "), f"line 1 should be the version comment, got {lines[0]}"
    first_body = next(line for line in lines if not line.startswith("<!-- "))
    assert re.match(r"# [^\w\s]", first_body), f"the header should be followed by an emoji H1, got {first_body}"


def test_only_when_blocking():
    """Latency tuning is justified only when latency is actually blocking."""
    assert "**only justified when actual latency is blocking the task**" in content(), (
        "the blocking-only rule is missing"
    )


def test_appropriate_and_inappropriate_cases():
    """The rule lists when tuning fits and when it doesn't."""
    assert "**Appropriate cases:**" in content(), "the appropriate-cases list is missing"
    assert "**Not appropriate:**" in content(), "the not-appropriate list is missing"


def test_effort_is_the_lever():
    """Effort is named as the main lever, with a row for each level."""
    assert "## 🎛️ Effort is the main lever" in content(), "the effort section is missing"
    for level in ("`low`", "`medium`", "`high`", "`xhigh` / `max`"):
        assert f"| {level} |" in content(), f"the effort table is missing the {level} row"


def test_effort_default_differs_on_opus_5_5():
    """The rule warns that Claude Opus 5.5 defaults to medium, so effort is set explicitly."""
    assert "Claude Opus 5.5 defaults to `medium`" in content(), "the Opus 5.5 default warning is missing"


def test_temperature_is_not_a_lever():
    """The rule says current models reject temperature."""
    assert "**Temperature is not a lever on current models.**" in content(), "the temperature warning is missing"


def test_no_temperature_above_one():
    """No temperature value above 1 appears, since the API never accepts one."""
    values = [float(v) for v in re.findall(r"temperature\s*[=:]?\s*(\d+(?:\.\d+)?)", content(), re.I)]
    values += [float(v) for v in re.findall(r"\b(\d\.\d)–(\d\.\d)\b", content()) for v in v]
    bad = [v for v in values if v > 1]
    assert not bad, f"the rule gives temperatures above 1, which the API rejects: {bad}"


def test_max_tokens_is_not_for_brevity():
    """A low max_tokens cap is described as truncating, not shortening."""
    assert "a low cap cuts the reply off mid-thought" in content(), "the max_tokens truncation warning is missing"


def test_streaming_is_not_a_speed_fix():
    """Streaming shows output sooner but doesn't finish the reply faster."""
    assert "doesn't make the full reply finish faster" in content(), "the streaming note is missing"


def test_four_measurement_steps():
    """The measure-first section keeps its four steps in order."""
    assert "## 📏 Constraint: measure before optimising" in content(), "the measure-first section is missing"
    section = content().split("## 📏 Constraint: measure before optimising", 1)[1]
    steps = re.findall(r"^\d\. \*\*([^*]+):\*\*", section, re.M)
    assert steps == ["Baseline", "Justify", "Test", "Revert if needed"], f"steps changed: {steps}"


def test_cost_judged_per_completed_task():
    """Cost is judged per completed task, not per request."""
    assert "Judge cost per completed task, not per request" in content(), "the per-task cost rule is missing"
