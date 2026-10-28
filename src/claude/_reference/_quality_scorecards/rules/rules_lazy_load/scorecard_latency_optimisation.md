# Quality Scorecard — latency_optimisation.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 6.8/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Record evidence of need, such as a dated run where a slow or costly API call blocked the work.
- Swap the per-model list on lines 39–44 for a pointer to the current model docs, so model changes don't make the rule wrong.
- Split lines 14, 30 and 43 into one-sentence bullets.
- Remove the stray `---` on line 76 and check the file ends with exactly one newline.
- Add this rule to `test_lazy_load_rule_structure.py`'s `RULES` dict, so its Purpose line and headings are tested.
- Move the Batch API "half price" reason on line 22 into a cost point, or reword line 14, so the latency guidance and the cost guidance don't get mixed up.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear levers:** the effort table (lines 32–37), the "Appropriate / Not appropriate" lists and the four-step measure-first check are all clear and easy to act on.<br>• ⚠️ **Overstated:** line 14 says premature optimisation "ruins response quality", which is stronger than the rest of the rule backs up.<br>• ⚠️ **Mixed aims:** line 22 rules out batch work on price ("half price anyway") inside a section about when latency matters, so latency and cost guidance blur together. |
| **Complexity** | 7/10 | 2026-10-25 | • 🧮 **Raw complexity 3:** Concepts 2 (when it applies, effort, temperature, related parameters, measure first) + Scope 0 (one file) + Dependencies 1 (the Claude API) + Prerequisites 0. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • 📊 **Loaded, never applied:** `docs/audits/rule_usage_sessions.csv` shows it loaded in 3 sessions (2026-09-19, 2026-09-29, 2026-10-01) with `applied=0` each time.<br>• ⚠️ **No incident:** no file records a dated slow or costly run that this rule fixed. |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Lazy:** it lives in `_rules_lazy_load/` and loads only through the "Read on demand" pointer in `claude_operational_efficiency.md` line 29, so it's left out of the average. |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Within limits:** 77 lines, a metadata header with `miss_cost` and `loading`, an emoji H1 and H2s, and a Purpose line.<br>• ⚠️ **Multi-sentence prose:** line 14 has three sentences, line 30 has two, and line 43 has two.<br>• ⚠️ **Stray rule line:** line 76 is a trailing `---` with no section after it.<br>• ⚠️ **Possible extra newline:** a blank line 77 shows after it, and `test_files_end_with_single_newline` doesn't scan `_rules_lazy_load/`, so no test would catch it. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **No stale paths:** the rule names no config files or commands that could have moved.<br>• ⚠️ **Model list:** lines 39–44 list effort defaults and `temperature` behaviour model by model (Opus 5.5, Fable 5/5.1, Sonnet 5.5 and others), which no repo file confirms and which goes stale, against "False truth rots silently". |
| **Test Coverage** | 7/10 | 2026-10-27 | • 🧪 **Trigger pinned:** `test_triggers_added_on_2026_10_01_stay` requires the pointer to remain, and `test_lazy_load_coverage.py` lists it as an entry point.<br>• 🧪 **Header and context checks:** `test_rule_headers.py` checks `miss_cost` and `loading`, and the Contents and Related checks in `test_rules_structure.py` include it.<br>• ⚠️ **Core checks skip it:** the line-limit, single-newline and H1 tests use `native_rule_files()`, which leaves out `_rules_lazy_load/`.<br>• ⚠️ **Not tracked:** this rule isn't in `test_lazy_load_rule_structure.py`'s `RULES` dict, so its Purpose line and headings aren't tested. |
| **Overall** | **6.8/10** | 2026-10-27 | • 💪 **Practical and lazy:** short, actionable effort guidance with a measure-first check, loaded only when needed.<br>• ⚠️ **Weak evidence:** no recorded need, a per-model list that will go stale, and structural checks that skip this file. |

## 🔗 Related files

- `src/claude/rules/_rules_lazy_load/claude_config/claude_cost/latency_optimisation.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — Token Cost Justification (holds the pointer)
- `docs/audits/rule_usage_sessions.csv` — Evidence of Need
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance, Test Coverage
- `src/claude/_tests/_helpers/_shared_paths.py` — Test Coverage (`native_rule_files()` leaves out the lazy folder)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_triggers.py` — Test Coverage
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_coverage.py` — Test Coverage
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Test Coverage
