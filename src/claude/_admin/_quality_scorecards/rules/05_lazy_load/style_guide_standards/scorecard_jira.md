# Quality Scorecard — jira.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.5/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-09-28 | • 📋 **Clear but thin:** 4 one-line principles, no why/how/test depth or examples, unlike `airflow.md`/`dbt.md` |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** router to 5 children plus one short principles section, single file, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Concrete:** the `dm-claude-created` label convention is specific and operational, not generic advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 9/10 | 2026-10-01 | • ✅ **Resolved:** the orphaned duplicate `jira/jira.md` was deleted in #90 (confirmed 2026-10-01)<br>• 🔍 **Check:** no stale references remain |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.5/10** | 2026-10-01 | • 💪 **Strength:** concrete, specific labeling convention<br>• ⚠️ **Gap:** Clarity (7/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/jira.md` — the rule being scored
- `src/claude/_tests/skills/jira_create/test_jira_create_handler.py` — Test Coverage dimension (a different artifact, not this rule)

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/jira/jira.md` was deleted in #90, confirmed absent on 2026-10-01.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
