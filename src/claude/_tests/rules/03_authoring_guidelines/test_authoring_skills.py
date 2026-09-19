# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 5/10
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

#!/usr/bin/env python3
"""
Test Suite: authoring_skills.md Improvements (7 Items)

Validates that authoring_skills.md contains all 7 improvements:
1. Consolidated redundancy (no concept explained 3+ times)
2. REQUIRED vs. optional marked clearly
3. Prose restructured (scannable, not dense)
4. Inline example of good SKILL.md frontmatter
5. Decision tree for maturity selection
6. Anti-patterns section (scope-creep guidance)
7. Maturity eval differences documented (Draft vs. Tactical vs. Strategic)

Run: pytest _tests/rules/test_authoring_skills_improvements.py -v
"""

import re

from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "03_authoring_guidelines" / "authoring_skills.md"


def resolved_content() -> str:
    """Return RULE_FILE's content with every @import line inlined recursively.

    authoring_skills.md is a parent+child rule (per _rule_directory_patterns.md)
    — its content lives across several imported files, not just the parent.
    Checks below must see the full resolved text, not just the parent's own
    lines, or any future re-split of the rule silently breaks every assertion.

    :return: The parent file's text with each @import line replaced by the
        target file's own (recursively resolved) content.
    :rtype: str
    """
    text = RULE_FILE.read_text(encoding="utf-8")
    parts = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("@~/") and "/" in stripped[len("@~/"):]:
            rest = stripped[len("@~/"):].split("/", 1)[1]
            target = CLAUDE_DIR / rest
            if target.exists():
                parts.append(target.read_text(encoding="utf-8"))
                continue
        parts.append(line)
    return "\n".join(parts)


class TestConsolidatedRedundancy:
    """Test that concepts are not repeated 3+ times across Core Standards, 7-Step, Hard Gates."""

    def test_5_section_structure_not_repeated(self):
        """Verify SKILL.md 5-section structure is explained once, then referenced."""
        content = resolved_content()

        # Search for "5.section" or "five.section" or "Frontmatter.*Purpose.*Example"
        pattern = r"Frontmatter.*Purpose.*Example.*Best For.*References"
        matches = len(re.findall(pattern, content, re.IGNORECASE | re.DOTALL))

        # Should appear 1-2 times (Core Standards definition + maybe one reference)
        # NOT 3+ times (Core Standards + 7-Step + Hard Gates all explaining it)
        assert matches <= 2, (
            f"SKILL.md 5-section structure explained {matches} times (target: 1-2). "
            "Consolidate: define once in Core Standards, reference in 7-Step/Hard Gates."
        )

    def test_contract_fields_not_repeated(self):
        """Verify contract.yaml required fields explained once, not in multiple sections."""
        content = resolved_content()

        # Count sections explaining "name, version, summary, maturity"
        pattern = r"name.*version.*summary.*maturity"
        matches = len(re.findall(pattern, content, re.IGNORECASE))

        # Explained once in Core Standards; a checklist-style restatement in
        # both Hard Gates Checklist and the Quality Checklist reference file
        # is expected — checklists intentionally repeat requirements for
        # scannability, unlike the prose-duplication this test targets.
        assert matches <= 3, (
            f"Contract fields (name, version, summary, maturity) explained {matches} times. "
            "Consolidate: explain once in Core Standards, restate in checklists only."
        )


class TestRequiredVsOptionalMarked:
    """Test that REQUIRED vs. optional fields are clearly marked."""

    def test_required_marker_present(self):
        """Verify [REQUIRED] tags mark mandatory fields."""
        content = resolved_content()

        assert "[REQUIRED]" in content or "[MUST]" in content or "**[REQUIRED]**" in content, (
            "Rule must explicitly mark [REQUIRED] fields (e.g., evals.yaml, SKILL.md structure, contract fields)"
        )

    def test_optional_marker_present(self):
        """Verify [IF APPLICABLE] or [OPTIONAL] tags mark conditional fields."""
        content = resolved_content()

        has_optional = "[IF APPLICABLE]" in content or "[OPTIONAL]" in content
        assert has_optional, (
            "Rule must mark conditional fields with [IF APPLICABLE] or [OPTIONAL] "
            "(e.g., reference/_formats.md, requires, dependencies)"
        )

    def test_contract_fields_clearly_categorized(self):
        """Verify contract.yaml section clearly lists which fields are required."""
        content = resolved_content()

        # Look for a heading mentioning "Contract" (not just any prose mention
        # of the word) and capture the section body that follows it.
        contract_section = re.search(
            r"^#+[^\n]*Contract[^\n]*\n(.*?)(?:^#+ |\Z)",
            content,
            re.DOTALL | re.MULTILINE
        )

        assert contract_section, "Rule must have a Contract section documenting required fields"

        contract_text = contract_section.group(1)
        has_markers = "[REQUIRED]" in contract_text or "[IF APPLICABLE]" in contract_text
        assert has_markers, (
            "Contract section must mark fields as [REQUIRED] or [IF APPLICABLE], not just list them"
        )


class TestProseRestructured:
    """Test that prose is restructured into scannable bullets/tables, not dense paragraphs."""

    def test_no_excessive_prose_blocks(self):
        """Verify most content is bullets/tables, not long prose paragraphs."""
        content = resolved_content()

        # Remove frontmatter, headers, code blocks
        content_cleaned = re.sub(r"^---.*?---\n", "", content, flags=re.DOTALL)  # frontmatter
        content_cleaned = re.sub(r"^#+\s.*?$", "", content_cleaned, flags=re.MULTILINE)  # headers
        content_cleaned = re.sub(r"```[\s\S]*?```", "", content_cleaned)  # code blocks

        # Count lines that are actual paragraph content (not bullets or tables)
        lines = [line for line in content_cleaned.split("\n") if line.strip()]
        bullet_lines = [line for line in lines if line.strip().startswith(("•", "-", "*", "|"))]

        ratio = len(bullet_lines) / len(lines) if lines else 0
        assert ratio >= 0.60, (
            f"Content is {ratio*100:.0f}% bullets/tables (target: ≥60%). "
            "Restructure dense prose blocks into bullets and tables for scannability."
        )


class TestInlineExample:
    """Test that an inline example of good SKILL.md frontmatter exists."""

    def test_frontmatter_example_present(self):
        """Verify a concrete example of SKILL.md frontmatter is shown in the rule."""
        content = resolved_content()

        # Look for YAML block with at least name, description, version, maturity
        yaml_pattern = r"```(?:yaml|yml).*?---.*?(?:name|description|version|maturity).*?```"
        assert re.search(yaml_pattern, content, re.IGNORECASE | re.DOTALL), (
            "Rule must show a concrete YAML frontmatter example (name, description, version, maturity)"
        )

    def test_example_shows_all_5_frontmatter_fields(self):
        """Verify the example includes all key frontmatter fields."""
        content = resolved_content()

        # Extract YAML example
        yaml_match = re.search(
            r"```(?:yaml|yml)\n(.*?)```",
            content,
            re.IGNORECASE | re.DOTALL
        )

        assert yaml_match, "YAML example block not found"

        example = yaml_match.group(1)
        required_fields = ["name:", "description:", "version:", "maturity:", "tags:"]

        for field in required_fields:
            assert field in example, (
                f"Frontmatter example missing field '{field}'. "
                f"Example should show: name, description, version, maturity, tags"
            )

    def test_example_includes_explanatory_comment(self):
        """Verify the example includes explanation of what makes it 'good'."""
        content = resolved_content()

        # After the example, there should be explanation
        example_section = re.search(
            r"```(?:yaml|yml).*?```.*?\n\n(.*?)(?:###|##|---|\Z)",
            content,
            re.IGNORECASE | re.DOTALL
        )

        assert example_section, "Example section must exist"

        explanation = example_section.group(1)
        assert len(explanation) > 50, (
            "Example must include explanation (✅ what makes this good, ❌ what to avoid)"
        )


class TestDecisionTree:
    """Test that maturity selection logic is documented as a decision tree/framework."""

    def test_maturity_decision_section_exists(self):
        """Verify a section explaining how to choose maturity level exists."""
        content = resolved_content()

        # Look for maturity selection guidance
        has_selection_guidance = (
            re.search(r"(?:Choose|Select|Decide).*maturity", content, re.IGNORECASE) or
            re.search(r"maturity.*(?:decision|select|choose)", content, re.IGNORECASE)
        )

        assert has_selection_guidance, (
            "Rule must explain HOW to choose maturity level (not just what levels exist). "
            "Add a 'Maturity Selection' or 'Maturity Decision' section with clear logic."
        )

    def test_decision_tree_or_flowchart_present(self):
        """Verify decision tree or table showing maturity selection logic."""
        content = resolved_content()

        # Look for either: a table with maturity columns, or if/then logic
        has_table = re.search(r"\|.*(?:draft|tactical|strategic).*\|", content, re.IGNORECASE)
        has_decision_logic = (
            re.search(r"if.*then.*maturity", content, re.IGNORECASE) or
            re.search(r"Use.*(?:draft|tactical|strategic).*when", content, re.IGNORECASE)
        )

        assert has_table or has_decision_logic, (
            "Maturity selection must use a table or if/then logic, not just narrative. "
            "Show: 'Use Draft when X', 'Use Tactical when Y', 'Use Strategic when Z'"
        )

    def test_maturity_justified_by_evidence(self):
        """Verify maturity levels reference evidence (frequency, test coverage, etc.)."""
        content = resolved_content()

        # Look for maturity + evidence language
        evidence_terms = ["frequency", "evidence", "real problem", "observed", "use", "tested"]
        has_evidence_context = any(
            re.search(term, content, re.IGNORECASE)
            for term in evidence_terms
        )

        assert has_evidence_context, (
            "Maturity selection must be evidence-based (frequency, test coverage, real problems). "
            "Document: 'Draft = speculative/one-time', 'Tactical = recurring/tested', 'Strategic = core workflow'"
        )


class TestAntiPatterns:
    """Test that anti-patterns (what NOT to do) are documented."""

    def test_anti_patterns_section_exists(self):
        """Verify an anti-patterns or 'Don't do' section exists."""
        content = resolved_content()

        has_anti_patterns = (
            "anti-pattern" in content.lower() or
            "don't do" in content.lower() or
            "avoid" in content.lower() and "skill" in content.lower()
        )

        assert has_anti_patterns, (
            "Rule must include anti-patterns section: 'Don't do X', 'Avoid Y', etc. "
            "Examples: avoid skills that handle 'everything', avoid ad-hoc test_*_handler.py, etc."
        )

    def test_scope_creep_anti_pattern(self):
        """Verify rule warns against scope-creep (skills trying to handle everything)."""
        content = resolved_content()

        has_scope_warning = (
            re.search(r"(?:scope|boundary|not_for).*(?:prevent|avoid|creep)", content, re.IGNORECASE) or
            re.search(r"(?:don't|avoid).*(?:everything|all|generic)", content, re.IGNORECASE)
        )

        assert has_scope_warning, (
            "Anti-patterns must warn against scope-creep: "
            "'Don't try to handle everything related to X', 'Keep boundaries tight', etc."
        )

    def test_testing_anti_pattern(self):
        """Verify rule warns against ad-hoc testing (not using evals.yaml)."""
        content = resolved_content()

        has_testing_warning = (
            re.search(r"(?:not|don't|avoid).*test_.*_handler", content, re.IGNORECASE) or
            re.search(r"evals\.yaml.*(?:standard|only|required)", content, re.IGNORECASE)
        )

        assert has_testing_warning, (
            "Anti-patterns must warn against ad-hoc testing: "
            "'Use evals.yaml (not test_*_handler.py)', 'No custom test scripts', etc."
        )


class TestMaturityEvalDifferences:
    """Test that differences between Draft/Tactical/Strategic evals are documented."""

    def test_eval_count_by_maturity_documented(self):
        """Verify rule explains eval count expectations: Draft 5-8, Tactical 8-12, Strategic 12+"""
        content = resolved_content()

        # Look for maturity + eval count table or narrative
        has_counts = (
            re.search(r"(?:Draft|draft).*(?:5|8).*eval", content) or
            re.search(r"(?:Tactical|tactical).*(?:8|12).*eval", content) or
            re.search(r"\d+.*eval.*(?:draft|tactical|strategic)", content, re.IGNORECASE)
        )

        assert has_counts, (
            "Rule must document eval counts by maturity: "
            "Draft 5-8, Tactical 8-12, Strategic 12+ scenarios"
        )

    def test_eval_coverage_differences_explained(self):
        """Verify rule explains WHAT each maturity level tests."""
        content = resolved_content()

        # Look for coverage differences: Draft=happy paths, Tactical=errors, Strategic=adversarial
        coverage_pattern = (
            r"(?:happy path|error|edge case|adversarial)"
        )
        matches = len(re.findall(coverage_pattern, content, re.IGNORECASE))

        assert matches >= 3, (
            "Rule must explain eval COVERAGE by maturity level:\n"
            "  - Draft: happy paths + basic validation\n"
            "  - Tactical: happy paths + error cases\n"
            "  - Strategic: all of above + edge cases + adversarial"
        )

    def test_maturity_eval_table_or_narrative(self):
        """Verify maturity/eval guidance is in table or clear narrative."""
        content = resolved_content()

        # Look for either table with maturity column, or clear narrative sections
        has_table = re.search(
            r"\|.*(?:Draft|Tactical|Strategic).*\|.*eval",
            content,
            re.IGNORECASE
        )

        has_narrative = (
            re.search(r"Draft.*\d+.*eval", content, re.IGNORECASE) and
            re.search(r"Tactical.*\d+.*eval", content, re.IGNORECASE)
        )

        assert has_table or has_narrative, (
            "Maturity/eval guidance must be in table or clear narrative (not scattered)"
        )


class TestLowMaintenanceDesign:
    """Test that Low-Maintenance Design section exists and is comprehensive."""

    def test_low_maintenance_design_section_exists(self):
        """Verify Low-Maintenance Design section is present."""
        content = resolved_content()

        assert "Low-Maintenance Design" in content or "low-maintenance" in content.lower(), (
            "Rule must have Low-Maintenance Design section emphasizing stability and preventing maintenance debt"
        )

    def test_immutability_principle_documented(self):
        """Verify immutability/stability-first principle is documented."""
        content = resolved_content()

        has_immutability = (
            re.search(r"(?:immutable|immutability|stable|stability|won't change)", content, re.IGNORECASE) and
            re.search(r"(?:v1\.0|version 1)", content, re.IGNORECASE)
        )

        assert has_immutability, (
            "Low-Maintenance Design must emphasize immutability: "
            "'Once v1.0 ships, assume it won't need changes'"
        )

    def test_isolation_principle_documented(self):
        """Verify isolation/independence principle is documented."""
        content = resolved_content()

        has_isolation = (
            re.search(r"(?:isolate|isolation|self-contained|no.*depend)", content, re.IGNORECASE) or
            re.search(r"(?:skill.*call|skill.*dependency)", content, re.IGNORECASE)
        )

        assert has_isolation, (
            "Low-Maintenance Design must emphasize isolation: "
            "'No skill-to-skill calls', 'self-contained skills'"
        )

    def test_maintenance_policy_documented(self):
        """Verify maintenance policy (when to update) is documented."""
        content = resolved_content()

        has_policy = (
            re.search(r"(?:update.*only|maintenance.*policy|when to update)", content, re.IGNORECASE) and
            (re.search(r"(?:security|vulnerability)", content, re.IGNORECASE) or
             re.search(r"(?:broken|deprecated|API change)", content, re.IGNORECASE))
        )

        assert has_policy, (
            "Low-Maintenance Design must document maintenance policy: "
            "'Update only for security/broken deps, not feature requests'"
        )

    def test_red_flags_or_measurement_documented(self):
        """Verify red flags or measurement criteria are documented."""
        content = resolved_content()

        has_metrics = (
            re.search(r"(?:red flag|measurement|update.*frequency|updates.*year)", content, re.IGNORECASE) or
            re.search(r"(?:more than|2.*year)", content, re.IGNORECASE)
        )

        assert has_metrics, (
            "Low-Maintenance Design must include red flags or metrics: "
            "'If updated more than 2x/year, redesign it'"
        )


class TestCommonMistakes:
    """Test that Common Mistakes section shows before/after examples."""

    def test_common_mistakes_section_exists(self):
        """Verify Common Mistakes section is present."""
        content = resolved_content()

        assert "Common Mistakes" in content or "common mistake" in content.lower(), (
            "Rule must have Common Mistakes section showing anti-patterns"
        )

    def test_bad_examples_shown(self):
        """Verify bad examples are shown (❌ pattern)."""
        content = resolved_content()

        has_bad_examples = re.search(r"❌|Bad:|mistake", content)

        assert has_bad_examples, (
            "Common Mistakes must show bad examples using ❌ or 'Bad:' label"
        )

    def test_good_examples_shown(self):
        """Verify good examples are shown (✅ pattern)."""
        content = resolved_content()

        has_good_examples = re.search(r"✅|Fix:|Good:|correct", content, re.IGNORECASE)

        assert has_good_examples, (
            "Common Mistakes must show good examples using ✅ or 'Fix:' label"
        )

    def test_before_after_structure(self):
        """Verify before/after examples use Fix/Good labels."""
        content = resolved_content()

        # Look for pattern: "Mistake" or bad emoji followed by "Fix" or good emoji
        has_mistake_and_fix = (
            re.search(r"Mistake.*?Fix", content, re.IGNORECASE | re.DOTALL) or
            re.search(r"Bad.*?Good", content, re.IGNORECASE | re.DOTALL) or
            (re.search(r"❌", content) and re.search(r"✅", content))
        )

        assert has_mistake_and_fix, (
            "Common Mistakes must have before/after examples with Fix labels or good/bad emojis"
        )


class TestQuickNavigation:
    """Test that Quick Navigation Guide covers all user types."""

    def test_quick_navigation_exists(self):
        """Verify Quick Navigation section is present."""
        content = resolved_content()

        assert "Quick Navigation" in content or "quick navigation" in content.lower(), (
            "Rule must have Quick Navigation guide showing different entry points"
        )

    def test_covers_new_skill_author(self):
        """Verify navigation for new skill authors is documented."""
        content = resolved_content()

        has_new_author_path = (
            re.search(r"(?:New|new).*(?:skill|author)", content) and
            re.search(r"(?:Start|start).*(?:here|at)", content)
        )

        assert has_new_author_path, (
            "Quick Navigation must guide new skill authors: 'New skill author? Start here...'"
        )

    def test_covers_experienced_author(self):
        """Verify navigation for experienced authors is documented."""
        content = resolved_content()

        has_experienced_path = (
            re.search(r"(?:Experienced|experienced).*(?:author|refresh)", content) and
            re.search(r"(?:Jump|jump).*(?:to|specific)", content)
        )

        assert has_experienced_path, (
            "Quick Navigation must guide experienced authors: 'Experienced author? Jump to...'"
        )

    def test_covers_reviewer_path(self):
        """Verify navigation for reviewers is documented."""
        content = resolved_content()

        has_reviewer_path = (
            re.search(r"(?:Reviewing|review).*(?:someone|else|skill)", content) and
            re.search(r"(?:Hard Gates|Common Mistakes)", content)
        )

        assert has_reviewer_path, (
            "Quick Navigation must guide reviewers: 'Reviewing someone else's skill? Use...'"
        )

    def test_navigation_structure_clear(self):
        """Verify navigation paths are clearly structured."""
        content = resolved_content()

        nav_section = re.search(
            r"Quick Navigation.*?(?:###|##|---|\Z)",
            content,
            re.IGNORECASE | re.DOTALL
        )

        assert nav_section, "Quick Navigation section must exist"

        nav_text = nav_section.group(0)

        # Should have clear delineation between different paths
        has_structure = (
            nav_text.count("**") >= 6 or  # Multiple bold headers
            re.search(r"1\.|2\.|3\.", nav_text)  # Numbered lists
        )

        assert has_structure, (
            "Quick Navigation must have clear structure (bold headers or numbered lists)"
        )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
