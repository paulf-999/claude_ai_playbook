# 📊 Skill Scorecards Summary

**Purpose:** One-glance rollup of every skill scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Skills | 8 | 8.2/10 | 2026-10-25 | • 💪 **Strongest:** `claude_review_config` (9.4/10)<br>• ⚠️ **Weakest:** `git_review_pr` (7.1/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`git_review_pr`:** add scenarios for the 4 untested "not for" cases and a declined post to `tests/evals.yaml` | • 🔻 **Score:** 7.1/10 | `scorecard_git_review_pr.md` |
| 2 | • 🔧 **`jira_create`:** add adversarial-input and assignee-validation scenarios to `tests/evals.yaml` | • 🔻 **Score:** 7.7/10 | `scorecard_jira_create.md` |
| 3 | • 🔧 **`claude_kaizen`:** record one real promotion end to end, since the evals cover the runner but not a full skill run | • 🔻 **Score:** 7.9/10 | `scorecard_claude_kaizen.md` |
| 4 | • 🔧 **`confluence_create_page`:** add adversarial-input scenarios to `tests/evals.yaml` | • 🔻 **Score:** 8.1/10 | `scorecard_confluence_create_page.md` |
| 5 | • 🔧 **`git_create_pr`:** add an eval scenario for a missing `gh` login | • 🔻 **Score:** 8.1/10 | `scorecard_git_create_pr.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_claude_review_config.md` | 9.4/10 | 2026-10-06 | — (≥8.5) |
| `scorecard_claude_capture_session_prompts.md` | 9.0/10 | 2026-10-06 | — (≥8.5) |
| `scorecard_claude_setup_graphify.md` | 8.4/10 | 2026-10-06 | • Bring the evals within the tactical range of 8–12, or justify strategic maturity |
| `scorecard_confluence_create_page.md` | 8.1/10 | 2026-09-19 | • Add adversarial-input scenarios to `tests/evals.yaml`<br>• Add retry logic for transient MCP failures in `phase_3_publish_page`<br>• Add a short FAQ section to the documentation |
| `scorecard_git_create_pr.md` | 8.1/10 | 2026-10-06 | • Add an eval scenario for a missing `gh` login<br>• Merge the two phase files into one `reference/_implementation.md`, or note why they stay split |
| `scorecard_claude_kaizen.md` | 7.9/10 | 2026-10-06 | • Record one real promotion end to end, since the evals cover the runner but not a full skill run |
| `scorecard_jira_create.md` | 7.7/10 | 2026-10-06 | • Add adversarial-input and assignee-validation scenarios to `tests/evals.yaml`<br>• Add retry logic for transient MCP failures in `phase_3_create_ticket`<br>• Add a short FAQ section to the documentation |
| `scorecard_git_review_pr.md` | 7.1/10 | 2026-10-25 | • Add scenarios for the 4 untested "not for" cases and a declined post<br>• Write the exact accepted-argument pattern into Phase 1<br>• Resolve the drafts path from the config directory<br>• Bring raw complexity below the tactical limit of 6 |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
