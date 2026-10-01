# Quality Scorecard — ansible.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.8/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Excellent:** a full repo-structure diagram, a naming-convention table with real examples, and explicit FQCN/linting requirements |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** router to 4 children plus repo structure, naming, and linting sections, single file, no dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Very concrete:** real inventory-scope naming, specific `ansible-lint` skip rules, an explicit exclusion note for `secrets_and_inventory.md` |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found, no orphaned duplicate (unlike `airflow`/`dbt`/`jira`/`sql`/`python`) |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.8/10** | 2026-10-01 | • 💪 **Strength:** the most concrete repo-structure documentation in this survey, no orphaned duplicate<br>• ⚠️ **Gap:** Complexity (8/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/infra/ansible.md` — the rule being scored
