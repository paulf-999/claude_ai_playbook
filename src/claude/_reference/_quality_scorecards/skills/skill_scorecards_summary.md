# 📊 Skill Scorecards Summary

**Purpose:** One-glance rollup of every skill scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Skills | 8 | 6.6/10 | 2026-10-29 | • 💪 **Strongest:** `git_review_pr` (7.6/10)<br>• ⚠️ **Weakest:** `git_create_pr` (6.0/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`git_create_pr`:** add adversarial and secret-leak evals, and escape a user-typed PR title before it reaches the shell | • 🔻 **Score:** 6.0/10, below what its strategic level expects | `scorecard_git_create_pr.md` |
| 2 | • 🔧 **`claude_setup_graphify`:** fix the writable pre-check, which fails on a fresh repo, and set `confirmation_required: true` | • 🔻 **Score:** 6.1/10, below what its strategic level expects | `scorecard_claude_setup_graphify.md` |
| 3 | • 🔧 **`claude_review_config`:** fix the wrong grade in the worked example and document the error cases its evals expect | • 🔻 **Score:** 6.1/10 | `scorecard_claude_review_config.md` |
| 4 | • 🔧 **`claude_kaizen`:** cut its scope, since raw complexity 8 is over the tactical cap of 6 | • 🔻 **Score:** 6.4/10 | `scorecard_claude_kaizen.md` |
| 5 | • 🔧 **`jira_create`:** drop Epic from the valid issue types and settle the story-point upper limit | • 🔻 **Score:** 6.4/10 | `scorecard_jira_create.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_git_review_pr.md` | 7.6/10 | 2026-10-26 | • Add a runner for `tests/evals.yaml` (#387), so Test Coverage can rise above the cap for unrun scenarios<br>• Add scenarios for the 4 untested "not for" hand-offs: creating a PR, a formal review, editing the PR's code and a bug hunt<br>• Lower complexity further, for example by moving the update-earlier-review branch or the large-diff budget into helpers<br>• Record use-frequency evidence for the strategic claim, which `_core_standards.md` asks for |
| `scorecard_claude_capture_session_prompts.md` | 7.4/10 | 2026-10-29 | • Use one minimum Python version everywhere: the script needs 3.10 (`capture_session_prompts.py` line 16), but SKILL.md line 17, contract line 59 and `_error_recovery.md` line 12 all say 3.9<br>• Catch the `ValueError` from `strptime` (script line 86) and print a clear message, so a bad `--date` doesn't end in a traceback<br>• Make the evals match the script: `capture_default_date` expects a `Timestamp` header, but the script writes `# | Hour | Min`<br>• Add a runner for the evals, or at least for the `cross_session_aggregation_out_of_scope` "not for" case |
| `scorecard_confluence_create_page.md` | 6.9/10 | 2026-10-29 | • Add a runner or pytest that executes `tests/evals.yaml`, or set `tested: false` and lower `test_coverage_level` until one exists<br>• Delete `reference/_confluence_page_formatting.md` or make it the one source, since it repeats `reference/common/_common_header.md` and `_common_formatting.md`, and SKILL.md links to one copy while the patterns read the other<br>• Change `_error_recovery.md`'s "Try again: transient errors are common" so it says what `_troubleshooting.md` says: check the parent page for a new draft before retrying, so a retry doesn't create a duplicate<br>• Remove `mcp__atlassian__updateConfluencePage` from the SKILL.md `tools:` list, since the contract marks page updates as `not_for` |
| `scorecard_claude_kaizen.md` | 6.4/10 | 2026-10-29 | • Add a runner or pytest that runs the 8 scenarios in `tests/evals.yaml` (#463), so Test Coverage can go above the cap of 7 for unrun evals<br>• Cut the scope or split the skill: its raw complexity is about 8, over the tactical limit of 6, and no complexity score is recorded anywhere<br>• Move `evals/` (the runner plus the seed YAML) into an allowed layout, such as `runner.py` at skill root and seeds under `reference/`, or record why it's an exception<br>• Add the missing pieces to the workflow: a check for duplicate rules (Purpose promises "keep rule set DRY"), how to create `candidates.md` when it doesn't exist, and how to make the config copy for the after-run |
| `scorecard_jira_create.md` | 6.4/10 | 2026-10-29 | • Drop Epic from the valid issue types in `_field_constraints.md` and `_error_handling.md`, because `not_for` and Best For both say the skill can't create epics<br>• Settle the story-points limit: `_field_constraints.md` gives "Valid range: 0.5 to 100" and also "no upper limit enforced"<br>• Set `tested: false` until a runner or a pytest runs `tests/evals.yaml`, because nothing under `_tests/skills/` covers `jira_create`<br>• Change `test_coverage_level: comprehensive` to `basic` or add the missing security case, and remove the contract note "error handling incomplete" that `_error_handling.md` no longer supports |
| `scorecard_claude_review_config.md` | 6.1/10 | 2026-10-29 | • Fix the grade in SKILL.md's Example Usage: 7.7/10 should be B, not B+, under `reference/_scoring_guide.md` (7.5–7.9 = B)<br>• Add an error-handling section to `reference/_implementation.md` for a missing `rules/` folder and malformed YAML, so the two error evals test documented behaviour<br>• Renumber the evals to match `_implementation.md`, where Phase 3 is the report and Phase 4 is offering fixes<br>• Make the MoSCoW scope match: `phase2_moscow_table` expects "Must/Should only", but `_implementation.md` lists Must, Should, Could and Won't |
| `scorecard_claude_setup_graphify.md` | 6.1/10 | 2026-10-29 | • Fix the writable pre-check so it works on a fresh repo: `touch graphify-out/.test` fails until `graphify-out/` exists<br>• Check `.gitignore` for an existing `graphify-out/` entry before appending, instead of only checking after the append<br>• Make the re-run guidance agree in one place, either duplicate detection or "remove the old section first"<br>• Build out `--dry-run`, `--skip-extract` and `--state`, or remove them |
| `scorecard_git_create_pr.md` | 6.0/10 | 2026-10-29 | • Add a runner or pytest that runs `tests/evals.yaml`, or score the skill as unrun until one exists<br>• Add adversarial and secret-leak evals (a custom title containing `$(...)` or quotes, and an untracked `.env` in the changed files) to reach strategic coverage<br>• Add an eval for the "complex merge conflict" not_for case<br>• Validate or shell-escape a user-typed custom PR title before it goes into `--title "<pr title>"`, and check it against the 70-character, no-filename title rules |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
