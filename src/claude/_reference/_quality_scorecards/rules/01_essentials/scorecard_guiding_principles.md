# Quality Scorecard — guiding_principles.md

**Date Created:** 2026-09-21
**Date Updated:** 2026-10-27

**Overall score:** 7.3/10

**Recommended improvements:**
- Use one unit (minutes or money) in the Automation ROI threshold, and write the line 22 example as a full worked comparison.
- Record at least one dated incident or usage-evidence entry for a principle, such as a pruned import or a removed hook, so the rule's need rests on a file.
- Path-scope the rule, or correct line 6's claim that path-scoping saves nothing, since the rule also loads in sessions outside the config.
- Confirm that `/doctor prompt-audit` exists and cite where, or replace it with a command that does.
- Delete line 11, which repeats the Purpose line.
- Add a content check for the "under 200 lines" and "110-line" size targets, or record a passing `test_rules_structure.py` run.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear principles:** each row's name, description and "How to apply" read the same to any reader.<br>• ⚠️ **Mixed units:** line 22's "if manual time per month < automation setup + monthly API cost" compares minutes with money.<br>• ⚠️ **Cryptic example:** line 22's "manual 10 min < Claude 2 min + $5" doesn't say which way the decision goes.<br>• ⚠️ **Vague trigger:** line 15's "Imports: only when directly referenced" doesn't say who references the import or how. |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** Concepts 3 (11 principles) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Broad bundle:** 11 principles in one table, matching the ~7 anchor ("one job that reads across several folders") more than the ~9 one. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **No dated incident:** unlike `portable_paths.md`, the rule records no incident, issue or usage row for any principle.<br>• 🔗 **External backing:** the size target and "context, not enforcement" points cite the Claude Code memory docs (lines 17 and 18).<br>• 🔗 **Relied on:** the rule rubric's Evidence and Currency dimensions are defined from this rule's principles (`rules/README.md` lines 75 and 87). |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • 🎯 **Header set:** lines 4–6 give `applies_to`, `miss_cost` and a loading reason.<br>• ⚠️ **Loads beyond its scope:** `applies_to` is `**/claude/**, **/.claude/**`, but the rule sits always-on in `rules/01_essentials/`, so it also loads in projects outside the config.<br>• ⚠️ **Overstated reason:** line 6's "path-scoping would save nothing" holds only for sessions inside the config. |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Within limits:** 25 lines, a metadata header, an emoji H1, a Purpose line and bold-keyword cell bullets.<br>• ⚠️ **Redundant line:** line 11 repeats the Purpose line, against `writing_style.md`'s brevity rule.<br>• ⚠️ **No recorded run:** no input records `test_rules_structure.py` or the header tests passing on this commit. |
| **Currency** | 8/10 | 2026-10-27 | • ✅ **Pointer resolves:** line 19's `_rules_lazy_load/claude_config/usage_evidence.md` exists.<br>• ✅ **Limits agree:** line 17's 110-line rule-file limit matches `_hard_gates_checklist.md` line 24.<br>• ⚠️ **Unconfirmed command:** no file in the repo defines or documents `/doctor prompt-audit` (line 17). |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Runnable test:** `test_guiding_principles.py` checks CLAUDE.md's imports against three principles: lazy-load, explicit and context efficiency.<br>• ✅ **No regression test needed:** the rule documents no incident, so the rubric asks only for structural coverage.<br>• ⚠️ **Partial content coverage:** the other eight principles get only structural checks, and no input records a pass rate. |
| **Overall** | **7.3/10** | 2026-10-27 | • 💪 **Strength:** a short, scannable, foundational table that the rubric itself builds on, with a real pytest behind three principles.<br>• ⚠️ **Gap:** no recorded evidence of need, a muddled ROI threshold and wider loading than its `applies_to`. |

## 🔗 Related files

- `src/claude/rules/01_essentials/guiding_principles.md` — the rule being scored
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/rules/_rules_lazy_load/claude_config/usage_evidence.md` — Currency
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_hard_gates_checklist.md` — Currency
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance
- `src/claude/_reference/_quality_scorecards/rules/README.md` — Evidence of Need
- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — Evidence of Need (the comparison anchor)
- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance and Test Coverage
