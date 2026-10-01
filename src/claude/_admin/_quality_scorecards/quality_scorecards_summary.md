# 📊 Quality Scorecards Summary

**Purpose:** One-glance rollup across every artefact type, showing where quality is weakest and what to fix first, without opening the five per-type summaries.

---

## 📋 Scores by type

- **Overall:** the mean of every scorecard's Overall score for that type.
- **Strongest and weakest:** the highest- and lowest-scoring file of that type, by Overall score.
- **Date Updated:** the latest `Date Updated` among that type's scorecards.
- **Rules split:** always-on rules (tiers 01–04 and `aliases.md`) load in every session, so they rank above lazy-load rules, which load only on demand.

| Type | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Tests | 51 | 8.9/10 | 2026-10-01 | • 💪 **Strongest:** 3 files tied at 9.6/10, including `test_latency_optimisation.py`<br>• ⚠️ **Weakest:** `test_confluence_create_page_timeout.py` (6.9/10) |
| Skills | 7 | 8.4/10 | 2026-09-30 | • 💪 **Strongest:** `claude_setup_graphify` (9.9/10)<br>• ⚠️ **Weakest:** `claude_kaizen` (6.1/10) |
| Rules — always-on | 16 | 8.2/10 | 2026-10-01 | • 💪 **Strongest:** `portable_paths.md` (9.4/10)<br>• ⚠️ **Weakest:** `claude_operational_efficiency.md` (7.1/10) |
| Rules — lazy-load | 17 | 8.4/10 | 2026-10-01 | • 💪 **Strongest:** `latency_optimisation.md` (9.2/10)<br>• ⚠️ **Weakest:** `makefile.md` (6.8/10) |
| Hooks | 0 | — | — | • ⚠️ **Gap:** no hooks are scored yet |
| Agents | 0 | — | — | • ⚠️ **Gap:** no agents are scored yet |

---

## 🚀 Recommended next actions

Ranked by impact, highest first, with lazy-load rule actions last because those rules load only on demand.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🆕 **Unscored hooks and agents:** write the first scorecards for hooks and agents | • 🙈 **Blind spot:** two of the five types have no quality signal at all | `hooks/hook_scorecards_summary.md`<br>`agents/agent_scorecards_summary.md` |
| 2 | • 🔧 **Lowest skill score:** replace `claude_kaizen`'s placeholder eval runner | • 🔻 **Bottom of the table:** at 6.1/10 it is the lowest-scoring skill | `skills/skill_scorecards_summary.md` |
| 3 | • ✂️ **Test complexity:** split the two `confluence_create_page` tests first, then the other 3 tests whose complexity score is below 7 | • 📉 **Lowest scores:** those two tests score 4/10 for complexity, the lowest of the 5 below the ≥7 floor | `tests/test_scorecards_summary.md` |
| 4 | • 💬 **Failure messages:** add assertion failure messages to `test_jira_create_handler.py` and `test_confluence_create_page_timeout.py` first, then `test_confluence_create_page_handler.py` | • 🔍 **Lowest scores:** the first two have failure messages on 0% of assertions, and the third on 1% | `tests/test_scorecards_summary.md` |
| 5 | • 🔧 **Lowest lazy-load rule score:** fix or remove `makefile.md`'s broken templates reference, then add inline principles | • 🔻 **Bottom of the table:** at 6.8/10 it is the lowest-scoring lazy-load rule | `rules/rule_scorecards_summary.md` |

---

## 📄 All summaries

| Summary | Scored | Overall | Date Updated |
|---|---|---|---|
| `tests/test_scorecards_summary.md` | 51 | 8.9/10 | 2026-10-01 |
| `skills/skill_scorecards_summary.md` | 7 | 8.4/10 | 2026-09-30 |
| `rules/rule_scorecards_summary.md` | 33 | 8.3/10 | 2026-10-01 |
| `hooks/hook_scorecards_summary.md` | 0 | — | — |
| `agents/agent_scorecards_summary.md` | 0 | — | — |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever any per-type summary changes.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files whenever a scorecard is re-scored.
- **Bump dates:** set a type's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its source summary no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
