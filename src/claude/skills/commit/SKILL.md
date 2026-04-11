---
name: commit
description: Stage files and create a conventional commit — review diff, draft message, confirm, and commit.
version: 1.0.0
maturity: tactical
tags:
  criticality: must
  status: active
  tested: false
tools: Bash
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are executing a git commit workflow. Follow every step in order. After each git-mutating step, confirm it succeeded before continuing. If any step fails, stop and report the error.

---

## ⚠️ Pre-check — verify required tools

Before doing anything else, confirm Bash is available by running `git status`. If the command fails or Bash is not accessible, stop immediately and tell the user:

> "This skill requires Bash access to run git commands. Please ensure the Bash tool is permitted for this session and try again."

Do not proceed without Bash.

---

## 🔍 Step 1 — Check working state

Run `git status` to see what has changed. If the working tree is clean, stop and tell the user.

---

## 📦 Step 2 — Stage files

Run `git diff` to show unstaged changes so the user can see what has changed. Then show the list of changed/untracked files from `git status`.

Stage specific files by name — never use `git add -A` or `git add .` without review. Ask the user to confirm which files to stage, or stage all changed files if they instruct you to.

---

## 📝 Step 3 — Generate and confirm commit message

Analyse the staged diff (`git diff --cached`) and draft a commit message following Conventional Commits:

Format: `type(scope): imperative description`
- `type`: one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`
- `scope`: the affected area (e.g. `dbt`, `makefile`, `pre-commit`, `aws`)
- Description: lowercase, imperative mood, no trailing period
- Examples: `feat(pre-commit): add ruff`, `fix(dbt): correct model reference`

Show the draft message to the user and wait for approval or edits before committing.

Once approved, run:
```
git commit -m "$(cat <<'EOF'
<approved message>
EOF
)"
```

If pre-commit hooks fail, report the failure clearly. Do not retry with `--no-verify` unless the user explicitly instructs it.
