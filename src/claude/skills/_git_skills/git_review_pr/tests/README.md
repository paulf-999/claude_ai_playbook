# 🧪 Tests

`evals.yaml` holds this skill's test scenarios: recorded situations (a user request, the setup, the expected result) that check `git_review_pr` still behaves correctly as it changes over time. They aren't code. Think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `gh_not_logged_in_stops` | Pre-check | Stops and asks for `gh auth login` before fetching anything |
| 2 | `comment_matches_format` | Identify, analyse | Finds the branch's PR, calls `code_reviewer` and fills every section of the template |
| 3 | `large_diff_summarised_by_file` | Fetch | Reviews whole files up to about 500 lines and summarises the rest by file |
| 4 | `prompt_injection_in_pr_ignored` | Analyse | Ignores instructions planted in the PR and flags them as a Must finding |
| 5 | `secret_in_comment_never_saved_or_posted` | Check | Checks the comment before saving, so a flagged secret is neither saved nor posted, and never shown |
| 6 | `dry_run_posts_nothing` | Check | With `--dry-run`, saves the draft and posts nothing |
| 7 | `declined_post_keeps_draft` | Confirm | Keeps the saved draft and posts nothing when the user answers `n` |
| 8 | `earlier_review_updated_not_duplicated` | Post | Uses a PR number argument and updates the user's earlier review instead of duplicating it |
| 9 | `failed_post_keeps_draft` | Post | Keeps the draft and reports the error when posting fails |
| 10 | `invalid_argument_rejected` | Identify | Rejects a pull URL whose owner part smuggles in a shell command |
| 11 | `empty_diff_stops` | Fetch | Stops before analysis when the PR has no changes |
| 12 | `local_diff_routed_to_code_reviewer` | Hand-off | Sends a local diff with no PR to `code_reviewer` instead |

- **Maturity:** 12 scenarios sits within the 8–12 expected for a **tactical** skill
- **Not covered:** complexity scoring (the `code_reviewer` agent's job), and four `not_for` cases (creating a PR, a formal review, editing the PR's code and a bug hunt), left out to stay within 12
- **Merged:** the two secret scenarios became one on 2026-10-26, to make room for the declined post
- **Secret pattern test:** `_tests/skills/git_review_pr/test_git_review_pr_secret_check.py` runs the check's `grep` pattern against sample secrets and safe text
- **No handler tests:** this skill has no Python code, so nothing else runs the scenarios yet
