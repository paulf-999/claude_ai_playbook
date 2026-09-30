# Quality Scorecard — jira.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Delete or reconcile the orphaned duplicate `jira/jira.md`.
- Add a dedicated structural test for this rule file — the existing `jira_create` skill tests cover a different artifact (the skill handler), not this style guide.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 7/10 | • 📋 **Clear but thin:** 4 one-line principles, no why/how/test depth or examples, unlike `airflow.md`/`dbt.md` |
| **Complexity** | 9/10 | • 🧮 **Raw complexity 1:** router to 5 children plus one short principles section, single file, no dependencies |
| **Evidence of Need** | 8/10 | • 🔗 **Concrete:** the `dm-claude-created` label convention is specific and operational, not generic advice |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji headers, Contents section, well within line limit |
| **Currency** | 6/10 | • 🐛 **Orphaned duplicate:** `jira/jira.md` is a near-identical, unreferenced copy of this file (confirmed via `diff` — only the relative link paths differ, as expected for its own location) |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** no structural test for this rule file; `_tests/skills/jira_create/` covers the unrelated `jira_create` skill handler, not this style guide's content |
| **Overall** | **6.3/10** | • 💪 **Strength:** concrete, specific labeling convention<br>• ⚠️ **Gap:** thinnest content of the style guides surveyed, missing Purpose statement, and an orphaned duplicate |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/jira.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/jira/jira.md` — Currency dimension (the orphaned duplicate)
- `src/claude/_tests/skills/jira_create/test_jira_create_handler.py` — Test Coverage dimension (a different artifact, not this rule)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/jira/jira.md` is a near-identical copy of this parent file, differing only in its relative link paths — confirmed unreferenced anywhere in the repo via grep.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
