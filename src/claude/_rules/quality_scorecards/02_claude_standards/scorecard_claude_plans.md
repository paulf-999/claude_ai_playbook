# Quality Scorecard — claude_plans.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.6/10

**Recommended improvements:**
- Add a "Right" example alongside the existing "Wrong" example in the Example section, per the heading's implied pairing.
- Add a Contents section, matching the sibling files in this tier (`behaviour.md`, `git.md`, `testing.md`).
- Add a dedicated test for the `_plan_file_format.md` child and the parent's own inline "How to apply" format.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 7/10 | • 📋 **Core principle is crisp:** "pause after each phase" with a clear format template<br>• 🔍 **Asymmetric example:** "Example" section (line 78) shows only a "Wrong" case, no matching "Right" case despite the pairing implied by the heading |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** ~4 concepts (core principle, when-to-apply, how-to-apply, anti-patterns) plus 2 children |
| **Evidence of Need** | 8/10 | • 🔗 **Followed in practice:** this very session's multi-phase scorecard work used explicit phase-gate confirmations matching this rule's format<br>• 📉 **No in-file incident:** doesn't cite a specific past failure |
| **Token Cost Justification** | 9/10 | • 🎯 **Scope:** Tier 2, always-on — governs delivery of all multi-step and plan-mode work |
| **Structural Compliance** | 7/10 | • ✅ **Compliant:** emoji headers, Purpose statement, trailing newline<br>• ❌ **Gap:** no Contents section, unlike sibling files in the same tier (`behaviour.md`, `git.md`, `testing.md` all have one) |
| **Currency** | 8/10 | • 🔍 **Check:** format described matches actual phase-gate behavior observed this session<br>• ✅ **Result:** no stale references found |
| **Test Coverage** | 7/10 | • 🧪 **Partial:** `test_plan_mode_phase_gates.py` covers the `_plan_mode_phase_gates.md` child directly<br>• ⚠️ **Untested:** `_plan_file_format.md` child and the parent's own inline "How to apply" format have no dedicated test |
| **Overall** | **7.6/10** | • 💪 **Strength:** genuinely followed, not just documented<br>• ⚠️ **Gap:** missing Contents section and an asymmetric example |

## 🔗 Related files

- `src/claude/_rules/02_claude_standards/claude_plans.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` — Test Coverage dimension
- `src/claude/_rules/02_claude_standards/claude_plans/_plan_file_format.md` — Test Coverage dimension (untested child)
