# Quality Scorecard — datetime.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** exact formats with examples, an explicit applies-to/does-not-apply split, a documented exception with reasoning |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** single self-contained file, no children, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Concrete:** the draft-filename exception (`YYYY-MMM-DD`) is specific and reasoned, not generic advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strength:** the clearest applies-to/exception structure in this survey<br>• ⚠️ **Gap:** Evidence of Need (8/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/_rules_lazy_load/style_guide_standards/utilities/datetime.md` — the rule being scored
