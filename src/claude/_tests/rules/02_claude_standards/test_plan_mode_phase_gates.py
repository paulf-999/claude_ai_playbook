# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-16
# Date updated:      2026-10-28
# Version:           4.0.1
# Test quality score: 9/10
# Test complexity score: 10/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content-regression test for the incident record in plan_mode_phase_gates.md.

Keeps only the persist-to-``_plans/`` section and its 2026-09-19 literal-``~`` incident
note, which ``testing.md`` allows as an incident record.
The rule's other wording is instructional and free to change, so it isn't pinned here.
"""
from _shared_paths import CLAUDE_DIR

GROUP_DIR = CLAUDE_DIR / "rules" / "02_claude_standards" / "claude_working_practices"
RULE_FILE = GROUP_DIR / "plan_mode_phase_gates.md"


def test_keeps_plan_persistence_section():
    """The persist-to-_plans section and its incident note must survive."""
    content = RULE_FILE.read_text()
    assert "## 📁 Persist the plan to `_plans/`" in content, (  # wording-check: incident record
        "Rule lost the persistence section"
    )
    assert "Incident (2026-09-19)" in content, "Rule lost the literal-~ incident note"  # wording-check: incident record
