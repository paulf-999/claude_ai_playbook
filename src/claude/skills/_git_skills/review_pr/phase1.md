## Phase 1 — Identify the PR

If `$ARGUMENTS` is a number (e.g. `/review_pr 42`), use it as the PR number.

Otherwise, run:

```bash
gh pr view --json number,title,url
```

If no PR is found for the current branch, stop and tell the user:

> "No open PR found for this branch. Either pass a PR number (e.g. `/review_pr 42`) or create a PR first."
