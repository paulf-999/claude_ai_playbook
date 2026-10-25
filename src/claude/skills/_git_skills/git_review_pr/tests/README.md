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
| 9 | `invalid_argument_rejected` | Pre-check | Rejects anything but a PR number or pull URL before it reaches a shell command |
| 10 | `empty_diff_stops` | Fetch | Stops before analysis when the PR has no changes |
| 11 | `secret_never_saved_to_drafts` | Confirm | Checks the comment before saving, so a flagged secret never reaches `_drafts/` |
| 12 | `local_diff_routed_to_code_reviewer` | Hand-off | Sends a local diff with no PR to `code_reviewer` instead |

- **Maturity:** 12 scenarios sits within the 8–12 expected for a **tactical** skill
- **Not covered:** complexity scoring (the `code_reviewer` agent's job) and a declined post
- **Secret pattern test:** `_tests/skills/git_review_pr/test_git_review_pr_secret_check.py` runs the check's `grep` pattern against sample secrets and safe text
- **No handler tests:** this skill has no Python code, so nothing else runs the scenarios yet
