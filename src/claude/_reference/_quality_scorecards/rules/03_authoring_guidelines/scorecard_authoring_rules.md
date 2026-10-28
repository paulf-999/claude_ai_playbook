# Quality Scorecard — authoring_rules.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.9/10

**Recommended improvements:**
- Point Pre-Creation question 4 at the `rules/` tier folders and `_rules_lazy_load/`, not at a "full rule list" in `claude_rule_loading_strategy.md`.
- Replace "~100–150 tokens/session cost" with a pointer to `make audit_rule_usage`, which measures tier sizes.
- Say in question 2 that a rule in tiers 01–03 with `paths:` frontmatter loads only with matching files, as `authoring_agents.md` does.
- Merge question 2's three-tier list into question 5's five-folder list, so tier placement is described only once.
- Make "Contents only with 3+ headings" say whether a Contents section is required or optional at 3+ headings, and apply that answer to this file.
- Move the rule to `paths:` (it already sets `applies_to: **/rules/**, **/_rules_lazy_load/**`), and keep a `**Read on demand:**` pointer in an always-on rule for new-file sessions.
- Wrap `test_rules_structure.py` in backticks on lines 19 and 65, and remove the blank lines between the two "Loads with config files from" bullets.
- Add a short evidence line that names the incidents the rule prevents (PR #94, PR #97), or point to `_common_mistakes.md` as its evidence.
- Add cross-reference tests for the `claude_rule_loading_strategy.md` and `testing.md` pointers.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear process:** a 5-question checklist, 5 steps and a gates list, each with a bold keyword<br>• ⚠️ **Tiers explained twice:** question 2 (line 21) gives three tiers and question 5 (line 36) gives five, which overlap<br>• ⚠️ **Ambiguous gate:** "add a Contents section only when the rule has 3 or more real `##` headings" (line 61) doesn't say if one is required, and this file has 4 `##` headings and no Contents<br>• ⚠️ **"core safety rules":** the label on line 22 doesn't fit authoring guidance, which is also always-on |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (checklist, creation steps, quality gates, metadata, scorecards) + Scope 2 (rules tiers, `_templates/`, `_reference/`, `_tests/`) + Dependencies 0 + Prerequisites 0 — see `_complexity_scoring.md` |
| **Evidence of Need** | 7/10 | 2026-10-28 | • 🔗 **Evidence in child:** `_common_mistakes.md` records shipped mistakes (PR #94 stale tier names, PR #97 missing headers, 2026-09-17 path incidents)<br>• ⚠️ **None in the rule:** the rule itself names no incident or usage record, and no file records how often it's applied |
| **Token Cost Justification** | 6/10 | 2026-10-25 | • 🎯 **Narrow applies_to:** the header scopes it to `**/rules/**, **/_rules_lazy_load/**` but it loads every session, which the anchor puts between 5 and 7<br>• ⚠️ **Weak reason:** "a new rule can start before any rule file is open" is the new-file gap that `claude_rule_loading_strategy.md` fixes with `paths:` plus a pointer, and `authoring_agents.md` in the same tier already uses `paths:` |
| **Structural Compliance** | 8/10 | 2026-10-28 | • ✅ **Within limits:** 78 lines, metadata header with `applies_to`, `miss_cost` and `loading`, emoji H1 and headers, and a Purpose line<br>• ⚠️ **Style slips:** `test_rules_structure.py` isn't in backticks on lines 19 and 65, line 11 repeats the Purpose as extra prose, and blank lines split the two pointer bullets on lines 69–71 |
| **Currency** | 6/10 | 2026-10-28 | • 🍂 **Stale pointer:** line 32 sends readers to "the full rule list" in `claude_rule_loading_strategy.md`, which now says "each folder is the current list of its rules — the examples above are illustrative only"<br>• 🍂 **Stale cost figure:** "~100–150 tokens/session cost" (line 22) doesn't match a 78-line always-on file, and the strategy rule defers to measured sizes from `make audit_rule_usage`<br>• ⚠️ **Loading drift:** "which Claude Code loads every session" ignores the tier-01–03 `paths:` exception in `claude_rule_loading_strategy.md`<br>• ✅ **Paths exist:** the template, all three on-demand children, both `shared_standards/` files, `authoring_agents.md`, the scorecard README and `test_always_on_reachability.py` are all present |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Covered:** `test_rules_structure.py` and `test_rule_headers.py` check structure and headers, and 5 tests in `test_rule_cross_references.py` cover the template, tiers, scorecard README, on-demand children and structure-test pointer<br>• 🧪 **Agent pointer:** `test_authoring_agents.py` checks the pointer to `authoring_agents.md`<br>• ⚠️ **Gaps:** nothing checks the `claude_rule_loading_strategy.md` or `testing.md` references, and no file records a passing run at c638e09 |
| **Overall** | **6.9/10** | 2026-10-28 | • 💪 **Well tested:** the rule's pointers have their own cross-reference tests, and every named path exists<br>• ⚠️ **Drift:** a stale rule-list pointer and a stale token figure, always-on placement despite a narrow `applies_to`, and tier guidance given twice |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_common_mistakes.md` — Evidence of Need
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_hard_gates_checklist.md` — Currency (pointer target exists)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_rule_lifecycle.md` — Currency (pointer target exists)
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — Currency, Token Cost Justification
- `src/claude/rules/03_authoring_guidelines/authoring_agents.md` — Token Cost Justification, Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — Structural Compliance
- `src/claude/rules/02_claude_standards/path_scoped_rules/testing.md` — Test Coverage
- `src/claude/_templates/rule.md.template` — Currency
- `src/claude/_reference/_quality_scorecards/rules/README.md` — Currency
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage, Structural Compliance
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Test Coverage, Structural Compliance
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Currency, Test Coverage
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_agents.py` — Test Coverage
