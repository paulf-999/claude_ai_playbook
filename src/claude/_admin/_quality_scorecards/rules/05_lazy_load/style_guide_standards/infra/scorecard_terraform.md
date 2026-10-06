# Quality Scorecard — terraform.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.7/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Clear principles:** environment separation, module reuse, config-driven, validation-first, infra-only scope — each stated concretely |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** router to 4 children plus 5 short principles, single file, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Concrete:** names real environments (`dev`, `uat`, `cicd`, `prod`, `global`) and a specific scope (Snowflake infra only, not application logic) |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found, no orphaned duplicate |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.7/10** | 2026-10-01 | • 💪 **Strength:** concrete, well-scoped principles, no orphaned duplicate<br>• ⚠️ **Gap:** Clarity (8/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/04_path_scoped/style_guide_standards/infra/terraform.md` — the rule being scored
