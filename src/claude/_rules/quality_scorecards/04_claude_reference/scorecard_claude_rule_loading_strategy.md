# Quality Scorecard — claude_rule_loading_strategy.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-29

**Overall score:** 6.4/10

**Recommended improvements:**
- Extend `test_rules_structure.py`'s emoji check to cover all `##` subheadings, not just the H1, so this class of gap is caught mechanically.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 6/10 | • 📋 **Principle is clear:** "lazy-load by default" is stated plainly<br>• 🚩 **Self-undermining:** claims to be the "Source of Truth" for the tier system, but its own "Filesystem structure" list is incomplete (see Currency) |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 3 concepts (source of truth, when-adding-a-rule, tier classification), 1 child |
| **Evidence of Need** | 8/10 | • 🔗 **Load-bearing:** directly referenced by `authoring_rules.md`'s checklist as the place to check for the full rule list and always-on/lazy-load placement |
| **Token Cost Justification** | 8/10 | • 🎯 **Scope:** Tier 4, always-on — moderate session relevance, foundational for rule-placement decisions specifically |
| **Structural Compliance** | 4/10 | • 🚩 **Missing emoji headings:** confirmed via `grep "^## "` — 4 of 5 `##` headings ("Source of Truth", "When Adding a Rule", "Tier Classification", "Related References") have no emoji, violating `writing_style.md`'s "use on all major headings" rule; only the H1 does |
| **Currency** | 5/10 | • 🐛 **Incomplete tier list:** the "Filesystem structure" section (lines 14–18) lists `01_essentials/`, `02_claude_standards/`, `04_claude_reference/`, `05_lazy_load/` — but omits `03_authoring_guidelines/`, which is a real, current tier |
| **Test Coverage** | 7/10 | • 🧪 **No file literally named for this rule**, but `test_always_on_reachability.py` (11 functions) directly mechanizes the reachability principle it documents, and `test_lazy_load_coverage.py` (2 functions) covers the lazy-load side |
| **Overall** | **6.4/10** | • 💪 **Strength:** the underlying reachability mechanism is well-tested even without a rule-specific test<br>• ⚠️ **Gap:** the two lowest scores in this survey — missing subheading emoji and an incomplete tier list, in the one file whose job is being the tier reference |

## 🔗 Related files

- `src/claude/_rules/04_claude_reference/claude_rule_loading_strategy.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Test Coverage dimension
- `src/claude/_tests/rules/05_lazy_load/test_lazy_load_coverage.py` — Test Coverage dimension
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension (the emoji-heading rule being violated)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Missing subheading emoji:** 4 of 5 `##` headings in this file have no emoji prefix, violating `writing_style.md`'s "use on all major headings" rule. `test_h1_heading_has_emoji()` in `test_rules_structure.py` only checks the H1, so this currently passes the test suite undetected.
- 🐛 **Incomplete tier list:** the "Filesystem structure" section omits `03_authoring_guidelines/` from its list of current tiers, despite that tier existing and being actively used (`authoring_agents.md`, `authoring_rules.md`, `authoring_skills.md` all live there).
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
