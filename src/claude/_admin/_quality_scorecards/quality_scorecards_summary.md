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
| Tests | 64 | 9.1/10 | 2026-10-06 | • 💪 **Strongest:** 3 files tied at 9.6/10, including `test_latency_optimisation.py`<br>• ⚠️ **Weakest:** `test_jira_create_handler.py` (7.9/10) |
| Skills | 8 | 8.4/10 | 2026-10-06 | • 💪 **Strongest:** `claude_review_config` (9.4/10)<br>• ⚠️ **Weakest:** `jira_create` (7.6/10) |
| Rules — always-on | 14 | 8.3/10 | 2026-10-01 | • 💪 **Strongest:** `portable_paths.md` (9.4/10)<br>• ⚠️ **Weakest:** `claude_operational_efficiency.md` (7.1/10) |
| Rules — lazy-load | 17 | 8.3/10 | 2026-10-01 | • 💪 **Strongest:** `latency_optimisation.md` (9.2/10)<br>• ⚠️ **Weakest:** `makefile.md` (6.8/10) |
| Hooks | 5 | 8.5/10 | 2026-10-02 | • 💪 **Strongest:** `hook_enforcement_mcp_stale_settings.sh` (9.0/10)<br>• ⚠️ **Weakest:** `hook_style_guide_response_standards.sh` (8.0/10) |
| Agents | 2 | 8.5/10 | 2026-10-05 | • 💪 **Strongest:** `code_reviewer` (8.9/10)<br>• ⚠️ **Weakest:** `technical_writer` (8.1/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first, with lazy-load rule actions last because those rules load only on demand.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 📅 **Reserved hook:** set a date to wire in or remove `hook_style_guide_response_standards.sh` | • 🔻 **Weakest hook:** at 8.0/10 it is the lowest-scoring hook | `hooks/hook_scorecards_summary.md` |
| 2 | • 🔧 **Lowest skill score:** add adversarial-input and assignee-validation scenarios to `tests/evals.yaml` (`jira_create`) | • 🔻 **Bottom of the table:** at 7.6/10 it is the lowest-scoring skill | `skills/skill_scorecards_summary.md` |
| 3 | • 💬 **Failure messages:** add assertion failure messages to `test_jira_create_handler.py`, then the two confluence handler tests (`_handler.py` and `_phases.py`) | • 🔍 **Lowest scores:** `test_jira_create_handler.py` and `_phases.py` have failure messages on 0% of assertions, and `_handler.py` on 3% | `tests/test_scorecards_summary.md` |
| 4 | • 🔧 **Lowest lazy-load rule score:** fix or remove `makefile.md`'s broken templates reference, then add inline principles | • 🔻 **Bottom of the table:** at 6.8/10 it is the lowest-scoring lazy-load rule | `rules/rule_scorecards_summary.md` |

---

## 📄 All summaries

| Summary | Scored | Overall | Date Updated |
|---|---|---|---|
| `tests/test_scorecards_summary.md` | 64 | 9.1/10 | 2026-10-06 |
| `skills/skill_scorecards_summary.md` | 8 | 8.4/10 | 2026-10-06 |
| `rules/rule_scorecards_summary.md` | 31 | 8.3/10 | 2026-10-01 |
| `hooks/hook_scorecards_summary.md` | 5 | 8.5/10 | 2026-10-02 |
| `agents/agent_scorecards_summary.md` | 2 | 8.5/10 | 2026-10-05 |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever any per-type summary changes.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files whenever a scorecard is re-scored.
- **Bump dates:** set a type's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its source summary no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
