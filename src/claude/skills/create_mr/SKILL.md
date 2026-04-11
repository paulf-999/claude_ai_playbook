---
name: create_mr
description: Full MR workflow — create branch, stage files, commit, push, and open a GitHub PR following team conventions.
version: 1.0.0
maturity: tactical
tags:
  criticality: must
  status: active
  tested: false
tools: Bash, Read, Glob, Agent
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are executing a full merge request workflow. Work through the two phases below in order.

## ⚠️ Pre-check — verify required tools

Before doing anything else, confirm Bash is available by running `git status`. If the command fails or Bash is not accessible, stop immediately and tell the user:

> "This skill requires Bash access to run git commands. Please ensure the Bash tool is permitted for this session and try again."

Do not proceed without Bash.

---

## 🔍 Phase 1 — Gather information (read-only, no prompting)

Run the following silently to understand the current state:

1. `git status` — identify changed/untracked files and current branch
2. `git diff` — review unstaged changes
3. Check whether `.github/pull_request_template.md` exists — read it if so

If the working tree is clean (nothing to commit), stop and tell the user.

Using what you have gathered:

- **Branch**: If already on a `feature/` or `hotfix/` branch, use it. Otherwise, derive a branch name from $ARGUMENTS (if provided) or propose one based on the changes. `$ARGUMENTS` is the text passed after the skill invocation — e.g. `/create_mr fix login redirect` → use `fix login redirect` as the branch hint. Branch naming pattern: `^(feature|hotfix)/[a-z0-9_]+$`
- **Files to stage**: List all changed/untracked files. Default to staging all of them unless context suggests otherwise.
- **Commit message**: Draft a Conventional Commits message from the diff:
  - Format: `type(scope): imperative description`
  - `type`: one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`
  - `scope`: the affected area (e.g. `dbt`, `makefile`, `pre-commit`, `aws`)
  - Description: lowercase, imperative mood, no trailing period
- **PR body**: Use the `Agent` tool with `subagent_type: technical-writer` to draft the PR body. Pass the agent the full diff, the commit message, and the contents of `.github/pull_request_template.md` (if it exists). Instruct the agent to fill in the summary section with bullet points describing the changes and leave all checkboxes intact. If no template exists, instruct the agent to produce a minimal body with a summary section.

---

## 🚀 Phase 2 — Present the plan and execute

Present the full plan to the user in this format:

```
Here is what I will run:

1. git checkout -b <branch_name>        # (omit if already on feature/hotfix branch)
2. git add <file1> <file2> ...
3. git commit -m "<commit message>"
4. git push -u origin <branch_name>
5. cat <<'EOF' >/tmp/pr_body.md
<full PR body>
EOF
6. gh pr create --title "<commit message>" --body-file /tmp/pr_body.md

PR title: <commit message>

PR body:
---
<full PR body>
---
```

Wait for the user to confirm or request changes before proceeding.

Once confirmed, execute the commands in sequence. After each git-mutating command, verify it succeeded before continuing. If any step fails, stop and report the error — do not skip ahead.

For the commit, use a heredoc to preserve formatting:
```
git commit -m "$(cat <<'EOF'
<commit message>
EOF
)"
```

Write the PR body to `/tmp/pr_body.md` before running `gh pr create`.

If pre-commit hooks fail, report the failure clearly. Do not retry with `--no-verify` unless the user explicitly instructs it.

After the PR is created, return the PR URL.
