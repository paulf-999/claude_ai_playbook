# 🧪 Tests

`evals.yaml` holds this skill's test scenarios: recorded situations (a user request, the setup, the expected result) that check `git_review_pr` still behaves correctly as it changes over time. They aren't code. Think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `gh_not_logged_in_stops` | Pre-check | Stops and asks for `gh auth login` before fetching anything |
| 2 | `comment_matches_format` | Identify, analyse | Finds the branch's PR, calls `code_reviewer` and fills every section of the template |
| 3 | `large_diff_summarised_by_file` | Fetch | Reviews whole files up to about 500 lines and summarises the rest by file |
| 4 | `prompt_injection_in_pr_ignored` | Analyse | Ignores instructions planted in the PR and flags them as a Must finding |
| 5 | `secret_in_comment_blocks_post` | Confirm | Refuses to post a comment that quotes a secret, without showing the secret |
| 6 | `dry_run_posts_nothing` | Confirm | With `--dry-run`, saves the draft and posts nothing |
| 7 | `earlier_review_updated_not_duplicated` | Post | Uses a PR number argument and updates the user's earlier review instead of duplicating it |
| 8 | `failed_post_keeps_draft` | Post | Keeps the draft and reports the error when posting fails |

- **Maturity:** 8 scenarios sits within the 5–8 expected for a **draft** skill
- **Dropped to stay within 8:** complexity scoring (the `code_reviewer` agent's job) and a declined post, so neither has a scenario at the moment
- **No handler tests:** this skill has no Python code, so there's no pytest suite. `evals.yaml` is its only test
