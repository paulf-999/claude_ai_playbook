# Quality Scorecard — claude_rule_loading_strategy.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Change line 71's `load:` to the real field name, `loading:`
- Update `HEADER_LINES` in `test_claude_rule_loading_strategy.py` lines 30–31 to the current 12-line header
- Record evidence of need for the placement rules
- Split the multi-sentence lines 17, 19 and 92, and give the numbered steps bold keywords

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🎯 **Decision table:** the miss-cost by applied-% grid (lines 47–51) gives one answer per cell, so two readers will place a rule the same way.<br>• ⚠️ **Wrong field name:** line 71 says "its `load:` reason names the pointer", but the header field is `loading:` (line 12 of the same file), so a reader may look for a field that doesn't exist.<br>• ⚠️ **Tier overlap:** line 34 says "tiers 01–03 load every session", yet the path-scoped folder sits inside `02_claude_standards/` (line 29), and only the `paths:` clause explains the exception. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (tier table, load decision grid, `paths:` fit, audit flags, adding steps) + Scope 2 (`rules/`, `_rules_lazy_load/` and `_reference/_style_guide_standards/`, lines 31 and 54) + Dependencies 0 (`make audit_rule_usage` is the config's own script) + Prerequisites 0.<br>• ⚠️ **Five jobs in one file:** lines 75–81 (audit flags) and 85–92 (adding steps) sit on top of the placement guidance, which pushes the Concepts count up. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ❓ **No incident recorded:** lines 17–19 state the per-session cost but give no dated incident or misplacement that the rule fixed.<br>• 🔗 **Uses measured data:** lines 42–45 base the decision on `docs/audits/audit_rule_usage.md`, which exists, but the rule records no result from it. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — path-scoped rule in `path_scoped_rules/`, so the rubric leaves this out of the average<br>• 🔍 **Reviewer note:** `paths:` on lines 2–6 loads it only with rule, lazy-rule, style-guide or `CLAUDE.md` files, which the reviewer would have scored 9/10. |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Header and length:** metadata comments on lines 8–12, emoji H1, Purpose line, about 80 body lines and no Related section.<br>• ⚠️ **Multi-sentence lines:** line 17 (`**Principle:**` has two sentences), line 19 and line 92 are each more than one sentence.<br>• ⚠️ **Steps lack keywords:** the numbered steps on lines 87–90 don't start with a bold keyword. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Paths exist:** `test_rule_headers.py` (with `test_high_cost_lazy_rules_load_mechanically`), `test_path_scoped_rules_live.py`, `audit_rule_usage.py`, `rule_usage_history.csv`, `docs/audits/audit_rule_usage.md`, `authoring_agents.md`, `_claude_config_metadata.md` and `latency_optimisation.md` all exist today.<br>• 🍂 **One stale reference:** line 71 names a `load:` field, but the metadata standard and this file's own line 12 use `loading:`. |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Drift test runs:** `src/claude/_tests/rules/02_claude_standards/test_claude_rule_loading_strategy.py` checks the five-row table against the folders on disk, plus tier order, example files, loading claims, the on-demand pointer, line limit and trailing newline. No incident is recorded, so no content-regression test is needed.<br>• ⚠️ **Header count out of date:** that test's lines 30–31 set `HEADER_LINES = 9` ("5 lines + version, created, updated, miss_cost"), but the rule now has a 7-line frontmatter plus 5 comment lines (12 in total, including `loading:`). The line-limit check still passes, but its maths is wrong.<br>• ⚠️ **Gaps:** nothing checks the test and script names on lines 56, 70 and 81 or the field name on line 71. I did not run the test. |
| **Overall** | **7.0/10** | 2026-10-25 | • 💪 **Strengths:** a decisive placement grid, path-scoped loading, and a drift test tied to the real folders.<br>• ⚠️ **Gaps:** the stale `load:` field name (line 71), no recorded incident, multi-sentence lines (17, 19, 92), and an out-of-date header count in the test. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Test Coverage dimension
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_coverage.py` — Test Coverage dimension
- `src/claude/_tests/rules/02_claude_standards/test_claude_rule_loading_strategy.py` — Test Coverage dimension (dedicated test)
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance dimension (H2 emoji check)
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension (the emoji-heading rule being violated)

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** all `##` headings now carry an emoji (v1.2.0, 2026-09-30), and `test_h2_headings_have_emoji()` now enforces it for every rule.
- ✅ **Resolved:** the tier list now covers all five tiers, including `03_authoring_guidelines/`.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
