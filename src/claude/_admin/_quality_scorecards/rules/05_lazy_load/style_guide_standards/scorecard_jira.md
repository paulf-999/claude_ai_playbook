# Quality Scorecard — jira.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Delete or reconcile the orphaned duplicate `jira/jira.md`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-09-28 | • 📋 **Clear but thin:** 4 one-line principles, no why/how/test depth or examples, unlike `airflow.md`/`dbt.md` |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** router to 5 children plus one short principles section, single file, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Concrete:** the `dm-claude-created` label convention is specific and operational, not generic advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 6/10 | 2026-09-28 | • 🐛 **Orphaned duplicate:** `jira/jira.md` is a near-identical, unreferenced copy of this file (confirmed via `diff` — only the relative link paths differ, as expected for its own location) |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.0/10** | 2026-10-01 | • 💪 **Strength:** concrete, specific labeling convention<br>• ⚠️ **Gap:** Currency (6/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/jira.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/jira/jira.md` — Currency dimension (the orphaned duplicate)
- `src/claude/_tests/skills/jira_create/test_jira_create_handler.py` — Test Coverage dimension (a different artifact, not this rule)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/jira/jira.md` is a near-identical copy of this parent file, differing only in its relative link paths — confirmed unreferenced anywhere in the repo via grep.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
