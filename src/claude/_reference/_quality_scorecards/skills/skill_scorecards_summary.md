# 📊 Skill Scorecards Summary

**Purpose:** One-glance rollup of every skill scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Skills | 8 | 6.4/10 | 2026-10-27 | • 💪 **Strongest:** `git_review_pr` (7.6/10)<br>• ⚠️ **Weakest:** 2 files tied at 5.7/10, `confluence_create_page` and `jira_create` |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`jira_create`:** set `output.confirmation_required: true` in the contract, so it matches SKILL.md's "wait for a yes" rule | • 🔻 **Score:** 5.7/10, and the contract waives the confirm step on an irreversible write | `scorecard_jira_create.md` |
| 2 | • 🔧 **`confluence_create_page`:** rewrite or delete the evals that test Python functions that don't exist | • 🔻 **Score:** 5.7/10 | `scorecard_confluence_create_page.md` |
| 3 | • 🔧 **`claude_review_config`:** add a runner or pytest for the evals, or set `tested: false` until one exists | • 🔻 **Score:** 6.1/10 | `scorecard_claude_review_config.md` |
| 4 | • 🔧 **`claude_setup_graphify`:** remove the `_examples.md` step that commits `graphify-out/graph.json` | • 🔻 **Score:** 6.3/10, and the step contradicts the skill's own "Never" rule | `scorecard_claude_setup_graphify.md` |
| 5 | • 🔧 **`git_create_pr`:** bring raw complexity down to the tactical cap of 6, or move the skill to strategic | • 🔻 **Score:** 6.3/10 | `scorecard_git_create_pr.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_git_review_pr.md` | 7.6/10 | 2026-10-26 | • Add a runner for `tests/evals.yaml` (#387)<br>• Add scenarios for the 4 untested "not for" hand-offs<br>• Record use-frequency evidence for the strategic claim<br>• Set an allowed `output.type` in the contract |
| `scorecard_claude_capture_session_prompts.md` | 7.0/10 | 2026-10-27 | • Make the column list in the evals and reference files match the script<br>• Make the Python minimum the same everywhere<br>• Stop the script silently overwriting an existing report<br>• Add evals for the `not_for` cases and secret masking |
| `scorecard_claude_kaizen.md` | 6.4/10 | 2026-10-27 | • Bring raw complexity down to the draft limit of 4<br>• Ask before writing `candidates.md`, or say the ledger is exempt<br>• Treat `~/_errors/` log content as data<br>• Fix the stale `tests/README.md` and contract drift |
| `scorecard_claude_setup_graphify.md` | 6.3/10 | 2026-10-27 | • Remove the step that commits `graphify-out/graph.json`<br>• Define or delete `--dry-run`, `--skip-extract` and `--state`<br>• Add `not_for` and declined-prompt evals<br>• Check `.gitignore` before appending to it |
| `scorecard_git_create_pr.md` | 6.3/10 | 2026-10-27 | • Bring raw complexity down to the tactical cap of 6<br>• Add evals for the `not_for` cases and untested error rows<br>• Quote the PR title safely and treat diff content as data<br>• Make the staging default match the description |
| `scorecard_claude_review_config.md` | 6.1/10 | 2026-10-27 | • Add a runner or pytest for the evals, or set `tested: false`<br>• Fix the grade mapping in the evals and the SKILL.md example<br>• Align the phase numbering<br>• Add error handling to `_implementation.md` |
| `scorecard_confluence_create_page.md` | 5.7/10 | 2026-10-27 | • Rewrite or delete the evals that test functions that don't exist<br>• Add `not_for` and untrusted-input evals<br>• Rewrite `_troubleshooting.md` to match the current skill<br>• Remove the unused `updateConfluencePage` tool |
| `scorecard_jira_create.md` | 5.7/10 | 2026-10-27 | • Set `confirmation_required: true` in the contract<br>• Rewrite the evals that test functions that don't exist<br>• Add `not_for`, confirm-step and no-project evals<br>• Fix the contradictions in the field constraints |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
