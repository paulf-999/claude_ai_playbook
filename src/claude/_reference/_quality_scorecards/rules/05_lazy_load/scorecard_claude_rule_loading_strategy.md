# Quality Scorecard — claude_rule_loading_strategy.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 📋 **Rewritten:** v2.0.0 replaces the unmeasurable 70% threshold with a placement table driven by the audit's applied % and each rule's `miss_cost` |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 2 (tiers, placement table, audit flags, adding a rule) + Scope 0 + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Load-bearing:** referenced by `authoring_rules.md`'s checklist for rule placement<br>• 📊 **Measured:** its placement inputs now come from `make audit_rule_usage` |
| **Token Cost Justification** | 9/10 | 2026-10-01 | • 🎯 **Lazy since v2.1.0:** `paths:` loads it only when a `_rules/` file or `CLAUDE.md` is read, saving ≈1.1k tokens in the 70% of sessions that never touch rules |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** every `##` heading now has an emoji, now enforced by `test_h2_headings_have_emoji()`<br>• ✅ **Compliant:** metadata header with `applies_to` and `miss_cost`, Purpose statement, 70 lines |
| **Currency** | 9/10 | 2026-10-01 | • ✅ **Fixed:** the tier table lists all five tiers, including `03_authoring_guidelines/`, and points to the tier folders as the source of truth |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_claude_rule_loading_strategy.py` (16 functions) checks the tier table against the real folders and CLAUDE.md imports, and that the 70% threshold stays gone<br>• ✅ **Generic checks:** passes `test_rules_structure.py`, including the new H2 emoji check |
| **Overall** | **8.9/10** | 2026-10-01 | • 💪 **Strength:** a clear five-tier table, now checked against the real folders by a dedicated test<br>• ⚠️ **Gap:** Complexity (8/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/04_path_scoped/claude_rule_loading_strategy.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Test Coverage dimension
- `src/claude/_tests/rules/05_lazy_load/test_lazy_load_coverage.py` — Test Coverage dimension
- `src/claude/_tests/rules/05_lazy_load/test_claude_rule_loading_strategy.py` — Test Coverage dimension (dedicated test)
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance dimension (H2 emoji check)
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension (the emoji-heading rule being violated)

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** all `##` headings now carry an emoji (v1.2.0, 2026-09-30), and `test_h2_headings_have_emoji()` now enforces it for every rule.
- ✅ **Resolved:** the tier list now covers all five tiers, including `03_authoring_guidelines/`.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
