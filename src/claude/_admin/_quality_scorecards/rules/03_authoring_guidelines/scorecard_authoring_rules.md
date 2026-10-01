# Quality Scorecard — authoring_rules.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-30

**Overall score:** 7.9/10

**Recommended improvements:**
- Extend `test_authoring_rules.py` to check the checklist's tier names against the actual directory structure, so tier-name drift is caught mechanically.
- Add content-regression checks for the two children, so the recorded mistakes and gates can't be lost silently in a later edit.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-29 | • 📋 **Clear flow:** 5-question checklist, 5-step creation process, quality gates, then mistakes and a tick-box checklist<br>• ✅ **Tier names current:** step 5 lists the real `01_essentials/`–`05_lazy_load/` directories |
| **Complexity** | 6/10 | 2026-09-29 | • 🧮 **Raw complexity 4:** one directory (parent plus 2 children), ~6 concepts (checklist, creation steps, quality gates, metadata, mistakes, hard gates) |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Heavily used:** its process and gates were followed repeatedly while building the scorecard and metadata conventions<br>• 🧾 **Mistakes are real:** every entry in `_common_mistakes.md` cites a recorded incident or PR |
| **Token Cost Justification** | 8/10 | 2026-09-29 | • 🎯 **Scope:** Tier 3, always-on — governs how every future rule gets created<br>• ⚖️ **Cost trimmed:** the two children moved to `authoring_rules/_lazy_load/` and load on demand |
| **Structural Compliance** | 9/10 | 2026-09-29 | • ✅ **Compliant:** metadata header, emoji H1, Purpose statement, trailing newline and Related section in all three files<br>• 🔗 **Children wired:** both are named in `**Read on demand:**` pointers and exempt from the orphan scan |
| **Currency** | 9/10 | 2026-09-29 | • ✅ **Matches the current config:** tier names, metadata standard and reachability test all reflect today's structure |
| **Test Coverage** | 6/10 | 2026-09-28 | • 🧪 **Direct test exists:** `test_authoring_rules.py`, 5 functions, now checking the two new sections<br>• ⚠️ **Structural only:** checks that sections and patterns exist, not that their content is correct |
| **Overall** | **7.9/10** | 2026-09-29 | • 💪 **Strength:** actively followed process, now with evidence-based mistakes and a finishing checklist<br>• ⚠️ **Gap:** tests remain structural, so content drift isn't caught |

## 🔗 Related files

- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — the rule being scored
- `src/claude/_rules/03_authoring_guidelines/authoring_rules/_lazy_load/_common_mistakes.md` — child, scored as part of this rule
- `src/claude/_rules/03_authoring_guidelines/authoring_rules/_lazy_load/_hard_gates_checklist.md` — child, scored as part of this rule
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_rules.py` — Test Coverage dimension
