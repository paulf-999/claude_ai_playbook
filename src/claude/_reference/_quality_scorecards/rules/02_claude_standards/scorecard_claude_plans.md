# Quality Scorecard — claude_plans.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 8.0/10

**Recommended improvements:**
- Record a dated incident or issue in which phases ran without approval, to back the rule's need.
- Add a "✅ Right" example beside the existing "❌ Wrong: No gate, silent progress" case.
- Swap "or similar" in step 2 for the exact approval wording the rule wants.
- Make step 3 match step 5, so a reply with feedback counts as a valid answer and the gate isn't only yes or no.
- Split the long "Tightly coupled" skip bullet so the plan-mode caveat is its own child bullet.
- Add a content-regression test for the parent's own rules (the 3-phase threshold, the skip conditions and the three required report parts).

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-27 | • 🎯 **Clear trigger:** "3+ phases", "sequential, not parallel" and the skip list make it plain when to gate.<br>• ⚠️ **Loose wording:** step 2's "Ready to proceed to Phase X?" or similar leaves the approval wording open.<br>• ⚠️ **Yes/no versus feedback:** step 3's "(yes/no)" clashes with step 5's "On "no" or feedback".<br>• ⚠️ **One-sided example:** the `## 📚 Example` section shows only the wrong case. |
| **Complexity** | 9/10 | 2026-10-27 | • 🧮 **Raw complexity 1:** Concepts 1 (the gate, when to apply or skip, and the report format), Scope 0 (one file, with the children loading on their own), Dependencies 0, Prerequisites 0. |
| **Evidence of Need** | 5/10 | 2026-10-27 | • ❓ **No recorded incident:** the only example is hypothetical ("User plans 3-phase work... User discovers Phase 2 approach was misaligned").<br>• ⚠️ **Not inherited:** the dated 2026-09-19 incident in `_plan_mode_phase_gates.md` is about a wrong Write path, not a missed phase gate. |
| **Token Cost Justification** | 8/10 | 2026-10-27 | • ✅ **Header set:** `applies_to: *` and `loading: always-on`, with a reason ("any task can grow into multi-phase work").<br>• ⚖️ **Arguable coverage:** only multi-phase sessions need it, but it is short (81 lines) and its `miss_cost` is medium. |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Within limits:** 81 lines, a complete metadata header, emoji on H1 and H2, a Purpose line, and no Related section.<br>• ✅ **Contents optional:** no Contents section, which `test_rules_structure.py` allows.<br>• ⚠️ **Style slip:** line 31 crams the skip condition and the plan-mode caveat into one bullet joined by an em dash.<br>• ⚠️ **Style slip:** the line 17 `**Why:**` paragraph has two sentences. |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **Paths exist:** `claude_response_standards.md`, `claude_plans/_plan_mode_phase_gates.md` and `claude_plans/_plan_file_format.md` all exist at commit 1705887.<br>• ✅ **Consistent:** the plan-mode caveat on line 31 matches the child's "unless the user explicitly waives gates". |
| **Test Coverage** | 9/10 | 2026-10-25 | • ✅ **Structural:** covered by `test_rules_structure.py` and `test_rule_headers.py`.<br>• ✅ **No incident in the parent:** so the rubric asks for no content-regression test.<br>• ⚠️ **Not run in this review:** the reviewer can only read files, so the pass result comes from coverage, not a fresh run.<br>• ⚠️ **Child-only test:** `test_plan_mode_phase_gates.py` checks only the child. |
| **Overall** | **8.0/10** | 2026-10-27 | • 💪 **Tight and current:** a short, single-concept rule whose references all resolve.<br>• ⚠️ **Need unproven:** no dated incident backs the parent rule. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans/_plan_mode_phase_gates.md` — Evidence of Need, Currency, Test Coverage
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans/_plan_file_format.md` — Currency
- `src/claude/rules/01_essentials/claude_response_standards.md` — Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance, Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Token Cost Justification, Test Coverage
- `src/claude/_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` — Test Coverage
