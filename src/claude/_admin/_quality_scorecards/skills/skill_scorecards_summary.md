# 📊 Skill Scorecards Summary

**Purpose:** One-glance rollup of every skill scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.
- **Improvements:** skill scorecards have no Recommended improvements section, so each row names its weakest dimension instead.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Skills | 7 | 8.4/10 | 2026-09-30 | • 💪 **Strongest:** `claude_setup_graphify` (9.9/10)<br>• ⚠️ **Weakest:** `claude_kaizen` (6.1/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`claude_kaizen`:** raise Code Quality (3/10), the weakest dimension | • 🔻 **Score:** 6.1/10 | `scorecard_claude_kaizen.md` |
| 2 | • 🔧 **`jira_create`:** raise Test Coverage (6/10), the weakest dimension | • 🔻 **Score:** 7.6/10 | `scorecard_jira_create.md` |
| 3 | • 🔧 **`git_create_pr`:** raise Complexity (7/10), the weakest dimension | • 🔻 **Score:** 7.9/10 | `scorecard_git_create_pr.md` |
| 4 | • 🔧 **`confluence_create_page`:** raise Design (8/10), the weakest dimension | • 🔻 **Score:** 8.1/10 | `scorecard_confluence_create_page.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_claude_setup_graphify.md` | 9.9/10 | 2026-09-07 | — (≥8.5) |
| `scorecard_claude_capture_session_prompts.md` | 9.7/10 | 2026-09-07 | — (≥8.5) |
| `scorecard_claude_review_config.md` | 9.4/10 | 2026-09-07 | — (≥8.5) |
| `scorecard_confluence_create_page.md` | 8.1/10 | 2026-09-19 | • Raise Design (8/10), the weakest dimension |
| `scorecard_git_create_pr.md` | 7.9/10 | 2026-09-30 | • Raise Complexity (7/10), the weakest dimension |
| `scorecard_jira_create.md` | 7.6/10 | 2026-09-19 | • Raise Test Coverage (6/10), the weakest dimension |
| `scorecard_claude_kaizen.md` | 6.1/10 | 2026-09-29 | • Raise Code Quality (3/10), the weakest dimension |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
