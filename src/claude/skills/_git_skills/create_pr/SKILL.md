---
name: create_pr
description: Full PR workflow — create branch, stage files, commit, push, and open a GitHub PR following team conventions.
version: 1.3.0
maturity: tactical
tags:
  criticality: must
  status: active
  tested: false
tools: Bash, Read, Glob, Agent
triggers:
  explicit:
    - /create_pr
    - /create_mr
  contextual:
    - user asks to create, raise, or open a PR or MR
not_for:
  - reviewing a PR — use /review_pr instead
  - posting a Teams notification — use /notify_pr instead
output:
  type: mixed
  confirmation_required: true
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are executing a full PR workflow. Work through the phases below in order.

## ⚠️ Pre-check — verify required tools

Before doing anything else, confirm Bash is available by running `git status`. If the command fails or Bash is not accessible, stop immediately and tell the user:

> "This skill requires Bash access to run git commands. Please ensure the Bash tool is permitted for this session and try again."

Do not proceed without Bash.

---

## 🔍 Phase 1 — Gather information (read-only, no prompting)

See [phase1.md](phase1.md) — repo state inspection, branch naming, commit message, PR body, and label derivation.

---

## 🚀 Phase 2 — Present the plan and execute

See [phase2.md](phase2.md) — title confirmation, full plan presentation, and sequential git/gh execution.

---

## ✅ Phase 3 — Verify

After the PR is created, run:

```bash
gh pr view <number> --json title,labels
```

Assert each of the following — report any failure as a warning and correct it before finishing:

1. **Label**: `labels` array is non-empty. If empty, apply the correct label now: `gh pr edit <number> --add-label "<label>"`.
2. **Title format**: title matches `^(feat|fix|chore|docs|refactor|test|ci|perf|style|build|revert)(\([^)]+\))?: [a-z]` — starts with a conventional commits type, followed by an optional `(scope)`, then `: ` and a lowercase description.
3. **Title cleanliness**: title does not contain file extensions (`.json`, `.py`, `.sql`, `.yml`, `.md`, `.sh`, `.tf`), path separators (`/`), or backticks.

If all checks pass, return the PR URL and report:

> "PR #<number> created and verified."

Then ask the user:

> "Would you like me to run any of the following on this PR?
> - **(r)** Post a Claude code review comment (`/review_pr`)
> - **(n)** Send a Teams notification (`/notify_pr`)
>
> Reply with any combination — 'r', 'n', 'both', or 'neither'."

Based on the response, launch the relevant skills using the `Agent` tool. If both are requested, launch them as parallel sub-agents in a single message:

- **`review_pr`**: read `~/.claude/skills/_git_skills/review_pr/SKILL.md` and execute all phases for the newly-created PR number
- **`notify_pr`**: read `~/.claude/skills/_git_skills/notify_pr/SKILL.md` and execute it for the newly-created PR number
