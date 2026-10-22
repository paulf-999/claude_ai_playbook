# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates the health signals audit_claude_component.py raises for tagged components.

Each test feeds the audit one piece of frontmatter, or one unreadable file, and
checks the signal it reports — so a broken signal shows up as a named failure
rather than a quietly empty report section.
"""
from __future__ import annotations

import importlib.util
from datetime import date, timedelta

import pytest

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "scripts" / "_audit_scripts" / "audit_claude_component.py"
BROKEN_FRONTMATTER = "---\nname: [unclosed\nmaturity: draft\n---\n# Broken\n"


def load_audit():
    """Import the audit script as a module."""
    spec = importlib.util.spec_from_file_location("audit_claude_component", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = load_audit()


def health(metadata: dict, known_names: set[str] | None = None) -> dict:
    """Return only the signals the audit raised for this frontmatter."""
    signals = audit.check_health(metadata, known_names or set())
    return {key: detail for key, detail in signals.items() if detail is not None}


def test_dormant_critical_component_is_flagged():
    """A must-have component marked dormant raises DORMANT."""
    signals = health({"tags": {"status": "dormant", "criticality": "must"}, "last-reviewed": date.today()})
    assert set(signals) == {"DORMANT"}, f"expected only DORMANT, got {signals}"


def test_deprecated_component_is_flagged_without_criticality():
    """A deprecated component raises DEPRECATED and says its criticality is unset."""
    signals = health({"tags": {"status": "deprecated"}})
    assert signals == {"DEPRECATED": "[criticality: unset]"}, f"expected only DEPRECATED, got {signals}"


@pytest.mark.parametrize("tested", [False, "false", "FALSE"])
def test_untested_critical_component_is_flagged(tested):
    """tested: false raises UNTESTED, whether YAML gives a bool or a string."""
    signals = health({"tags": {"tested": tested, "criticality": "should"}, "last-reviewed": date.today()})
    assert set(signals) == {"UNTESTED"}, f"expected only UNTESTED for tested={tested!r}, got {signals}"


def test_unrecognised_tested_value_is_ignored():
    """A tested value that isn't a boolean raises nothing rather than guessing."""
    signals = health({"tags": {"tested": "maybe", "criticality": "must"}, "last-reviewed": date.today()})
    assert signals == {}, f"an unrecognised tested value should raise nothing, got {signals}"


def test_old_review_date_is_stale():
    """A review date older than the staleness window raises STALE with its age."""
    reviewed = date.today() - timedelta(days=audit.STALENESS_WARN_DAYS + 1)
    signals = health({"last-reviewed": reviewed})
    assert set(signals) == {"STALE"}, f"expected only STALE, got {signals}"
    assert f"{audit.STALENESS_WARN_DAYS + 1}d ago" in signals["STALE"], signals["STALE"]


def test_recent_review_date_as_text_is_not_stale():
    """A recent review date written as text parses and raises nothing."""
    signals = health({"last-reviewed": date.today().isoformat()})
    assert signals == {}, f"a recent review should raise nothing, got {signals}"


def test_unparseable_review_date_is_reported():
    """A review date that isn't a date is reported as STALE with the bad value."""
    signals = health({"last-reviewed": "last spring"})
    assert signals == {"STALE": "[last-reviewed: unparseable value 'last spring']"}, signals


def test_unknown_dependency_is_flagged():
    """depends-on naming a component that doesn't exist raises BROKEN_DEP for that name only."""
    signals = health({"depends-on": ["known", "ghost"]}, known_names={"known"})
    assert signals == {"BROKEN_DEP": "[unknown: ghost]"}, f"expected only the unknown name, got {signals}"


def test_known_dependencies_raise_nothing():
    """depends-on naming only real components raises nothing."""
    assert health({"depends-on": ["known"]}, known_names={"known"}) == {}


def test_unreadable_frontmatter_counts_as_untagged(tmp_path):
    """A component whose frontmatter won't parse is counted as untagged, not skipped or crashed on."""
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "broken.md").write_text(BROKEN_FRONTMATTER)
    tagged, untagged = audit.find_all_components(tmp_path)
    assert (tagged, [p.name for p in untagged]) == ([], ["broken.md"]), (tagged, untagged)


def test_unreadable_file_adds_no_known_name(tmp_path):
    """A tagged file that can't be re-read adds no name to the depends-on lookup."""
    broken = tmp_path / "broken.md"
    broken.write_text(BROKEN_FRONTMATTER)
    assert audit._collect_names([broken]) == set()


def test_report_skips_a_tagged_file_it_cant_reread(tmp_path, monkeypatch, capsys):
    """If a tagged file breaks before the health pass, the report skips it instead of crashing."""
    broken = tmp_path / "skills" / "broken.md"
    broken.parent.mkdir()
    broken.write_text(BROKEN_FRONTMATTER)
    monkeypatch.setattr(audit, "find_all_components", lambda root: ([broken], []))
    audit.build_report(tmp_path)
    assert "Health signals: 0" in capsys.readouterr().out, "the unreadable file should add no signals"


def test_paths_outside_root_fall_back(tmp_path):
    """A path outside the scan root shows in full, and groups under 'other'."""
    outside = tmp_path.parent / "elsewhere.md"
    root = tmp_path / "claude"
    assert audit._rel(outside, root / "skills") == str(outside)
    assert audit._top_dir(outside, root) == "other"
