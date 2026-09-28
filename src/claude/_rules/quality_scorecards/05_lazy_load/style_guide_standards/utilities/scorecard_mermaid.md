# Quality Scorecard — mermaid.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Add a dedicated structural test for this file and its 2 children.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 6/10 | • 📋 **Bare routing:** a 2-item child list with a one-line scope statement, no inline principles or examples of its own |
| **Complexity** | 10/10 | • 🧮 **Raw complexity 0:** a pure 2-item router, single file, no dependencies — as simple as a rule file gets |
| **Evidence of Need** | 6/10 | • 🔗 **Somewhat concrete:** names a real usage scope (skill `flow.md` files, role READMEs), but nothing beyond that |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji headers, Contents section |
| **Currency** | 9/10 | • 🔍 **Check:** no stale references found, no orphaned duplicate |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **6.5/10** | • 💪 **Strength:** simple, no orphaned duplicate, states a real usage scope<br>• ⚠️ **Gap:** thin content, missing Purpose statement, zero test coverage |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/utilities/mermaid.md` — the rule being scored
