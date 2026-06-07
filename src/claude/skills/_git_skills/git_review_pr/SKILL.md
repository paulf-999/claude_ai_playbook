---
name: git_review_pr
description: Generate and post a structured Claude review comment on a GitHub PR — covering a high-level summary and a scored review table across code quality, code complexity, testing, security, documentation, and standards compliance.
version: 0.2.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools: Bash, Agent
triggers:
  explicit:
    - /git_review_pr
    - /git_review_pr <number>
  contextual:
    - user asks to review a PR or post a Claude review
    - auto-triggered at end of /create_pr when user opts in
not_for:
  - creating a PR — use /create_pr instead
  - general code review not tied to a GitHub PR
output:
  type: mixed
  confirmation_required: true
---

## Scope gate

This skill is at **draft** maturity — happy path only.

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## Pre-check

Run `gh auth status`. If it fails, stop and tell the user:

> "This skill requires the `gh` CLI authenticated to GitHub. Run `gh auth login` and try again."

---

## Phase 1 — Identify the PR

See [phase1.md](phase1.md) — identifies the PR from a passed argument or the current branch.

---

## Phase 2 — Fetch PR data

See [phase2.md](phase2.md) — fetches diff, metadata, repo URL, and changed file paths in parallel.

---

## Phase 3 — Analyse

Use the Agent tool with `subagent_type: code_reviewer`. Pass it:
- The PR `<number>` so it can populate the header block
- The PR title, description, and metadata (author, files changed, additions/deletions)
- The full diff (or truncated diff with a note)
- The list of file paths changed in the PR
- The `repo_url` and `headRefName` so it can construct file links
- The output format and scoring guidance from [comment_format.md](comment_format.md)

Instruct the agent to produce **only** the structured output defined in the format section — no preamble, no trailing commentary. The scorecard covers **6 themes**: code quality, code complexity, testing, security, documentation, and standards.

---

## Phase 4 — Format and confirm

Wrap the agent output in no additional envelope — the format is defined in [comment_format.md](comment_format.md).

Show the full formatted comment to the user.

**If the verdict is "Request changes" or "Approve with suggestions"**, prompt:

> "Would you like to address any of these before posting?
>
> 1. \<one-line summary of recommendation 1\>
> 2. \<one-line summary of recommendation 2\>
>
> Reply with numbers (e.g. `1, 2`), `all`, or `n` to skip."

If the user selects recommendations, address each in turn then re-show the updated comment.

Ask: > "Post this as a comment on PR #\<number\>? (y/n)" — if the user says no, stop.
> Note: the amendment prompt is intentionally skipped for Approve verdicts — no Must or Should items means nothing actionable to address before posting.

---

## Phase 5 — Post the comment

Write the comment body to `~/_drafts/pr/review_pr_<number>_<YYYY-MMM-DD>.md`, then post:

```bash
gh pr comment <number> --body-file ~/_drafts/pr/review_pr_<number>_<YYYY-MMM-DD>.md
```

Return the PR URL.

---

> TODO (tactical): handle very large diffs (>500 lines) more gracefully — e.g. summarise by file rather than truncating
> TODO (tactical): support posting as a formal GitHub review (approve/request-changes) via `gh pr review`, not just a comment
> TODO (tactical): add `--dry-run` argument to preview the comment without posting
> TODO (tactical): add guard for empty diff response (e.g. PR opened with no commits yet)
> TODO (tactical): add eval assertion for diff-truncation behaviour (>500 lines) — eval 4 covers the assertion but not the invocation path
