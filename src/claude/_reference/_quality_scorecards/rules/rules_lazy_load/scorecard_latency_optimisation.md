# Quality Scorecard — latency_optimisation.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Record evidence of need, such as a dated slow or costly run
- Replace the per-model catalogue on lines 39–44 with a pointer to the current model docs
- Split the prose on lines 14, 30 and 43 into one-sentence bullets, and drop the stray `---` on line 76

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear levers:** the effort table (lines 32–37) and the "how to apply" bullets (lines 51–61) are specific enough to act on.<br>• ⚠️ **Overstated opener:** line 14 says "Premature optimisation wastes context and ruins response quality", which overstates the case and runs three sentences of prose together.<br>• ⚠️ **Vague row:** line 35's `medium` row ("when `high` is slower than needed and quality still holds") doesn't say how to judge that. |
| **Complexity** | 7/10 | 2026-10-25 | • 🧮 **Raw complexity 3:** Concepts 2 (when to optimise, effort, temperature, related parameters, measure-first) + Scope 0 (single file) + Dependencies 1 (Claude API) + Prerequisites 0. This matches the ~7 anchor. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No incident:** the rule records no dated incident, issue or usage, so the need rests on the general statement at line 14.<br>• ⚠️ **Gate missed:** `_hard_gates_checklist.md` line 26 ("Evidence of need is recorded") isn't met by anything in the file. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Header and shape:** the metadata header (lines 1–3), `miss_cost`/`loading` (lines 4–5), the emoji H1, Purpose (line 8) and the 77-line length all pass.<br>• ⚠️ **Prose paragraphs:** lines 14, 30 and 43 put several sentences in bold-led prose, not one sentence per bullet.<br>• ⚠️ **Loose ends:** the file ends on a stray `---` at line 76, and the measure-first steps (lines 69–72) have no closing punctuation, unlike the rest of the file. |
| **Currency** | 7/10 | 2026-10-25 | • 🔍 **No dead paths:** the rule names no files or commands that could go stale.<br>• ⚠️ **Model catalogue:** lines 39–40 and 43–44 list per-model defaults and `temperature` behaviour (Opus 5.5, Opus 5, Opus 4.8, Fable 5/5.1, Sonnet 5/5.5, and so on). That is the kind of exhaustive list that rots silently, and none of the allowed inputs can confirm it (`updated` at line 3 is 2026-10-02). |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Reachability runs:** `_tests/rules/rules_lazy_load/test_lazy_load_triggers.py` line 260 pins its pointer trigger, and `_tests/rules/rules_lazy_load/test_lazy_load_coverage.py` line 147 lists it as an entry point.<br>• ✅ **No incident to pin:** the rule records no incident, so no content-regression test is warranted.<br>• ⚠️ **Unconfirmed structural pass:** `test_rules_structure.py` was outside the allowed inputs, so I couldn't confirm a passing structural run for this file. |
| **Overall** | **7.0/10** | 2026-10-25 | • 💪 **Actionable:** a focused single-file rule with a clear effort table and a measure-before-optimising step.<br>• ⚠️ **Unbacked need:** no recorded evidence of need.<br>• ⚠️ **Rotting list:** the per-model catalogue at lines 39–44 is likely to drift. |

## 🔗 Related files

- `src/claude/rules/_rules_lazy_load/claude_config/claude_cost/latency_optimisation.md` — the rule being scored
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage dimension
