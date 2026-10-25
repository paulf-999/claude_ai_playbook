# 📊 Quality Scorecards Summary

**Purpose:** One-glance rollup across every artefact type, showing where quality is weakest and what to fix first, without opening the five per-type summaries.

---

## 📋 Scores by type

- **Overall:** the mean of every scorecard's Overall score for that type.
- **Strongest and weakest:** the highest- and lowest-scoring file of that type, by Overall score.
- **Date Updated:** the latest `Date Updated` among that type's scorecards.
- **Rules split:** always-on rules (tiers 01–03 and `aliases.md`) load in every session, so they rank above lazy-load rules, which load only on demand.

| Type | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Tests | 60 | 9.1/10 | 2026-10-11 | • 💪 **Strongest:** 2 files tied at 9.6/10, including `test_rule_reachability.py`<br>• ⚠️ **Weakest:** `test_capture_session_prompts.py` (8.1/10) |
| Skills | 8 | 8.2/10 | 2026-10-25 | • 💪 **Strongest:** `claude_review_config` (9.4/10)<br>• ⚠️ **Weakest:** `git_review_pr` (7.1/10) |
| Rules — always-on | 19 | 7.0/10 | 2026-10-25 | • 💪 **Strongest:** `claude_working_practices.md` (7.9/10)<br>• ⚠️ **Weakest:** `claude_operational_efficiency.md` (5.9/10) |
| Rules — lazy-load | 12 | 6.3/10 | 2026-10-25 | • 💪 **Strongest:** `latency_optimisation.md` (7.0/10)<br>• ⚠️ **Weakest:** `dbt.md` (5.5/10) |
| Hooks | 5 | 8.5/10 | 2026-10-02 | • 💪 **Strongest:** `hook_enforcement_mcp_stale_settings.sh` (9.0/10)<br>• ⚠️ **Weakest:** `hook_style_guide_response_standards_checker.sh` (8.0/10) |
| Agents | 3 | 8.5/10 | 2026-10-22 | • 💪 **Strongest:** `code_reviewer` (8.9/10)<br>• ⚠️ **Weakest:** `technical_writer` (8.1/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first, with lazy-load rule actions last because those rules load only on demand.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **Lowest always-on rule score:** add or stop naming the `make disable_mcp` target in `claude_operational_efficiency.md`'s children | • 🔻 **Bottom of the table:** at 5.9/10 it is the lowest-scoring always-on rule | `rules/rule_scorecards_summary.md` |
| 2 | • 📅 **Reserved hook:** set a date to wire in or remove `hook_style_guide_response_standards_checker.sh` | • 🔻 **Weakest hook:** at 8.0/10 it is the lowest-scoring hook | `hooks/hook_scorecards_summary.md` |
| 3 | • 🔧 **Lowest skill score:** add scenarios for the 4 untested "not for" cases and a declined post to `tests/evals.yaml` (`git_review_pr`) | • 🔻 **Bottom of the table:** at 7.1/10 it is the lowest-scoring skill | `skills/skill_scorecards_summary.md` |
| 4 | • 🔧 **Lowest lazy-load rule score:** make `dbt.md`'s layers, prefixes and commands match its children, and replace the non-existent `dbt lineage` | • 🔻 **Bottom of the table:** at 5.5/10 it is the lowest-scoring lazy-load rule | `rules/rule_scorecards_summary.md` |

---

## 📄 All summaries

| Summary | Scored | Overall | Date Updated |
|---|---|---|---|
| `tests/test_scorecards_summary.md` | 60 | 9.1/10 | 2026-10-11 |
| `skills/skill_scorecards_summary.md` | 8 | 8.2/10 | 2026-10-22 |
| `rules/rule_scorecards_summary.md` | 31 | 6.7/10 | 2026-10-25 |
| `hooks/hook_scorecards_summary.md` | 5 | 8.5/10 | 2026-10-02 |
| `agents/agent_scorecards_summary.md` | 3 | 8.5/10 | 2026-10-22 |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever any per-type summary changes.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files whenever a scorecard is re-scored.
- **Bump dates:** set a type's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its source summary no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
