# Quality Scorecard — ansible.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Add a dedicated structural test for this file and its 4 children.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Excellent:** a full repo-structure diagram, a naming-convention table with real examples, and explicit FQCN/linting requirements |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** router to 4 children plus repo structure, naming, and linting sections, single file, no dependencies |
| **Evidence of Need** | 9/10 | • 🔗 **Very concrete:** real inventory-scope naming, specific `ansible-lint` skip rules, an explicit exclusion note for `secrets_and_inventory.md` |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | • 🔍 **Check:** no stale references found, no orphaned duplicate (unlike `airflow`/`dbt`/`jira`/`sql`/`python`) |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **7.2/10** | • 💪 **Strength:** the most concrete repo-structure documentation in this survey, no orphaned duplicate<br>• ⚠️ **Gap:** missing Purpose statement, zero test coverage |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/infra/ansible.md` — the rule being scored
