# Quality Scorecard — datetime.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Add a dedicated structural test for this file.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** exact formats with examples, an explicit applies-to/does-not-apply split, a documented exception with reasoning |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** single self-contained file, no children, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Concrete:** the draft-filename exception (`YYYY-MMM-DD`) is specific and reasoned, not generic advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | 2026-09-28 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found |
| **Test Coverage** | 2/10 | 2026-09-28 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **7.3/10** | 2026-09-28 | • 💪 **Strength:** the clearest applies-to/exception structure in this survey<br>• ⚠️ **Gap:** missing Purpose statement, zero test coverage |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/utilities/datetime.md` — the rule being scored
