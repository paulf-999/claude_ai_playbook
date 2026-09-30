# Quality Scorecard — terraform.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Add a dedicated structural test for this file and its 4 children.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 8/10 | • 📋 **Clear principles:** environment separation, module reuse, config-driven, validation-first, infra-only scope — each stated concretely |
| **Complexity** | 9/10 | • 🧮 **Raw complexity 1:** router to 4 children plus 5 short principles, single file, no dependencies |
| **Evidence of Need** | 8/10 | • 🔗 **Concrete:** names real environments (`dev`, `uat`, `cicd`, `prod`, `global`) and a specific scope (Snowflake infra only, not application logic) |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | • 🔍 **Check:** no stale references found, no orphaned duplicate |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **7.0/10** | • 💪 **Strength:** concrete, well-scoped principles, no orphaned duplicate<br>• ⚠️ **Gap:** missing Purpose statement, zero test coverage |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/infra/terraform.md` — the rule being scored
