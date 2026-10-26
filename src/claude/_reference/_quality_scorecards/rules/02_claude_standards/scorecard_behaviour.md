# Quality Scorecard — behaviour.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.7/10

**Recommended improvements:**
- Move "Other safety patterns" (lines 46–58) under a heading that matches what they cover
- Record evidence of need for the parent and its children
- Fix the multi-sentence bullets and `**X** —` bullets on lines 42, 51 and 66–73
- Add pointer tests for the six children that `test_rule_cross_references.py` doesn't cover

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Misfiled guidance:** `behaviour.md` lines 46–58 put "Other safety patterns" (ask first, investigate, literal direction, plan approval) under "Before claiming completion", so a reader can't tell from the heading what that section covers.<br>• ⚠️ **Mixed signal:** `behaviour.md` line 62 says "Do not proceed without explicit confirmation" for any flagged item, then line 64's engineer test reads as a self-check, so the two lines can be read as different gates.<br>• 🔍 **Option tension:** `_decision_making.md` line 19 ("always present 2–3 options") sits next to `_artefact_proposal_gates.md` line 12 ("proceeds without options"), and only line 23's prerequisite links the two. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (eight distinct concerns: approach, task tiers, completion, proposing, artefact gates, decision-making, disclosure, model choice, session conduct) + Scope 2 (`rules/02_claude_standards/behaviour/` plus `_rules_lazy_load/claude_config/hooks_decision_framework.md` from `behaviour.md` line 68) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Bundled concerns:** `_model_selection_strategy.md` and `_session_conduct.md` are separate jobs that sit under a "safe defaults" parent. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ❓ **No dated incidents:** none of the eight files records an incident, PR or repeated failure, which `_hard_gates_checklist.md` line 26 requires.<br>• 🔗 **Sourced, not observed:** the only provenance is the Boris Cherny source comment at `_how_to_approach.md` line 17 and the `miss_cost: high` header at `behaviour.md` line 5, which state need but don't show it happening. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • ✅ **Justified core:** `behaviour.md` lines 4–6 set `applies_to: *`, `miss_cost: high` and an always-on reason, and the risky-action and confirmation gates apply in every session.<br>• ⚖️ **Passengers:** about 100 parent lines plus seven always-on children load every session, including low-risk material such as `_model_selection_strategy.md` lines 10–13 and `_how_to_approach.md` lines 24–26, which don't need high-miss-cost placement. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and length met:** metadata on lines 1–6, emoji H1, Purpose line, 103 lines with children split out under `behaviour/`.<br>• ⚠️ **Multi-sentence bullets:** `behaviour.md` lines 42 and 51, `_how_to_approach.md` lines 12 and 24.<br>• ⚠️ **No bold-keyword colon:** `behaviour.md` lines 66–73 use `**X** —`, and `_pre_existing_issue_disclosure.md` lines 21–24 and 50–53 have no bold keyword, both breaking `_hard_gates_checklist.md` line 25.<br>• ⚠️ **Redundant line:** `behaviour.md` line 11 repeats the Purpose on line 9. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Pointers resolve:** all seven `behaviour/_*.md` children and `rules/_rules_lazy_load/claude_config/hooks_decision_framework.md` (line 68) exist, and `test_rule_cross_references.py` checks every gate Reference file.<br>• 🔍 **Unverified path:** `_how_to_approach.md` line 20 names `~/_sessions/`, which is outside the config and which I couldn't check from the allowed inputs.<br>• 🔍 **Possible drift:** `_artefact_proposal_gates.md` line 59 calls `claude_rule_loading_strategy.md` a "full rule index table", but I didn't read that file in the allowed inputs, so this is unconfirmed. |
| **Test Coverage** | 7/10 | 2026-10-25 | • 🧪 **Partial targeted tests:** `_tests/rules/test_rule_cross_references.py` lines 150–208 cover only `behaviour.md`'s pointer to `_artefact_proposal_gates.md` and that child's examples and references.<br>• ⚠️ **Other children unchecked:** no test found by Grep checks the other six "Loads on its own from" pointers (`behaviour.md` lines 30, 36, 90, 94, 98, 102) or the `hooks_decision_framework.md` pointer on line 68.<br>• ✅ **No incident test owed:** no file records an incident, so no content-regression test is needed, and I didn't run the structure-test pass. |
| **Overall** | **6.7/10** | 2026-10-25 | • 💪 **Strong safety core:** clear risky-action list, proportional task tiers and a confirm-first rule for every tier.<br>• ⚠️ **Gaps:** no recorded evidence of need, several style slips across the children, and tests that cover one of seven children. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/behaviour.md` — the rule being scored
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
- `src/claude/rules/02_claude_standards/behaviour/_how_to_approach.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/behaviour/_before_acting.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/behaviour/_pre_existing_issue_disclosure.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/behaviour/_model_selection_strategy.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/behaviour/_session_conduct.md` — Test Coverage dimension (untested child)
