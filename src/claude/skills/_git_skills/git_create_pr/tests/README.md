# 🧪 Tests

`evals.yaml` holds this skill's test scenarios: recorded situations (a user request, the setup, the expected result) that check `git_create_pr` still behaves correctly as it changes over time. They aren't code. Think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_feature_pr` | Full flow | Reads the template, derives names, confirms title and plan, then creates the PR and reports its link |
| 2 | `missing_pr_template_stops` | Gather | Stops and asks for a PR template instead of inventing a body |
| 3 | `clean_working_tree_stops` | Gather | Stops when there's nothing to commit |
| 4 | `reuses_existing_feature_branch` | Derive | Keeps the current feature branch, and turns down a base branch other than `main` (a not_for case) |
| 5 | `branch_name_derived_in_snake_case` | Derive | Turns messy arguments into a valid lowercase, underscore-only branch name |
| 6 | `pr_title_plain_english_no_filenames` | Derive | PR title is plain English, 70 characters or fewer, with no filenames |
| 7 | `labels_mapped_and_missing_ones_skipped` | Labels | Applies `claude-skill` from the path, and skips and reports `hotfix` when the repo lacks it |
| 8 | `docs_only_change_labelled_documentation` | Labels | A docs-only change gets the `docs` type and `documentation` label |
| 9 | `user_requests_title_alternatives` | Confirm | Offers alternative titles and uses the one picked, running nothing until the plan is approved |
| 10 | `user_declines_plan` | Confirm | Declining the plan leaves no branch, commit, push or PR behind |
| 11 | `too_many_changed_files` | Edge case | Flags a change of 20 or more files and suggests splitting it |
| 12 | `push_rejected_stops` | Error recovery | A rejected push stops the flow without force-pushing or creating the PR |
| 13 | `custom_title_with_shell_syntax_is_data` | Security | A typed title with `$(...)` is checked against the title rules and never runs |
| 14 | `likely_secret_file_not_staged` | Security | An untracked `.env` is left out of the commit and listed under "Not staged" |
| 15 | `merge_conflict_stops` | Not for | Unmerged paths stop the skill before anything is staged |

- **Maturity:** 15 scenarios, including adversarial and security cases, meets the 12+ expected for a **strategic** skill
- **No handler tests:** this skill has no Python code, so there's no pytest suite. `evals.yaml` is its only test
