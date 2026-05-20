## Phase 2 — Fetch PR data

Run these three commands in parallel:

```bash
gh pr view <number> --json number,title,body,author,additions,deletions,changedFiles,baseRefName,headRefName,url
gh pr diff <number>
gh repo view --json url
```

If the diff exceeds 500 lines, truncate to the first 500 lines and note this in the review comment with: *"Note: diff truncated to 500 lines — review covers visible changes only."*

From the results, extract:
- `headRefName` — the feature branch name (used to construct file links)
- `repo_url` — the base repo URL (e.g. `https://github.com/org/repo`)
- File paths changed in the diff — collect these for link construction

File links take the form: `{repo_url}/blob/{headRefName}/{filepath}`
