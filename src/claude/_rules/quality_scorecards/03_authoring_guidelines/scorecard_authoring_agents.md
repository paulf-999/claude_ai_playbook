# Quality Scorecard — authoring_agents.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-30

**Overall score:** 6.9/10

**Recommended improvements:**
- Cite a specific incident or usage evidence justifying this file's always-on, Tier 3 placement.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 8/10 | • 📋 **Good navigation aid:** "Quick Navigation" splits guidance by reader persona (new author, experienced author, reviewer), matching `authoring_skills.md`'s pattern |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** pure router, no inline substantive content, 4 children |
| **Evidence of Need** | 6/10 | • 🔗 **Plausible but unevidenced:** agents are a real feature, but no incident or usage evidence is cited<br>• 📉 **Weaker than its siblings:** unlike `authoring_rules.md`/`authoring_skills.md`, has zero test coverage — a soft signal of lighter real-world use to date |
| **Token Cost Justification** | 7/10 | • 🎯 **Scope:** Tier 3, always-on — plausible, but the total absence of tests makes the always-on cost harder to independently verify as earned |
| **Structural Compliance** | 8/10 | • ✅ **Compliant:** consistent with sibling authoring_*.md files, emoji headers, trailing newline |
| **Currency** | 8/10 | • 🔍 **Check:** no stale references spotted in the parent or its 4 children |
| **Test Coverage** | 3/10 | • 🧪 **Gap:** zero test files exist for `authoring_agents.md` or any of its 4 children<br>• ⚠️ **Inconsistent with siblings:** both `authoring_rules.md` and `authoring_skills.md` have dedicated structural tests; `authoring_agents.md` has none |
| **Overall** | **6.9/10** | • 💪 **Strength:** clear structure, consistent with sibling docs<br>• ⚠️ **Gap:** the only one of the 3 authoring-guideline files with zero test coverage |

## 🔗 Related files

- `src/claude/_rules/03_authoring_guidelines/authoring_agents.md` — the rule being scored
- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — Evidence of Need / Test Coverage dimension (sibling with a dedicated test)
- `src/claude/_rules/03_authoring_guidelines/authoring_skills.md` — Evidence of Need / Test Coverage dimension (sibling with a dedicated test)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **No tests at all:** confirmed via `find src/claude/_tests -iname "*authoring_agents*"` — zero results, and no test references any of its 4 children (`_core_standards.md`, `_decision_tree_and_process.md`, `_scope_and_maturity.md`, `_common_mistakes.md`) by name.
- 🚫 **Inconsistent with siblings:** `test_authoring_rules.py` and `test_authoring_skills.py` both exist for the other two files in the same `03_authoring_guidelines/` tier.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
