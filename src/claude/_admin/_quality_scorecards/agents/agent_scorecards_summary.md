# 📊 Agent Scorecards Summary

**Purpose:** One-glance rollup of every agent scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Agents | 0 | — | — | • ⚠️ **Gap:** no agents are scored yet |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🆕 **First scorecards:** score the first agents | • 🙈 **Blind spot:** no agent has a quality signal yet | `README.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| — | — | — | • ⚠️ **Gap:** no agents are scored yet |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
