---
name: git_create_pr
description: Create GitHub PR with staged changes, commit message, and PR body
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 1.3.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-30 -->

## 🎯 Purpose

Automate the full PR creation workflow with minimal user intervention:
- **Branch creation** — derive and create feature/hotfix branch from user input
- **Commits** — stage, compose, and push changes with Conventional Commits format
- **PR opening** — populate title, body, labels, and create PR on GitHub
- **Confirmation** — confirm the title, then the full plan, before anything is committed or pushed

## 💡 Example Usage

```
$ /git_create_pr add user authentication
[Phase 1] Deriving branch name: feature/add_user_authentication
          Commit message: feat: add user authentication
          PR title: feat: add user authentication

[Phase 2a] Proposed PR title: feat: add user authentication
           y to confirm · list for alternatives · or type your own: y

[Phase 2b] Here is what I will run: checkout, add, commit, push, gh pr create
           Confirm? y
           ✓ Branch created  ✓ Committed  ✓ Pushed  ✓ PR created

PR #1234 created: https://github.com/org/repo/pull/1234
```

## ✨ Best For

Routine feature/hotfix PRs. Faster than manual git workflow; enforces Conventional Commits automatically; minimal setup required.

## 📚 References

- `reference/_phase1_gather.md` — gather-info logic, branch/commit/PR-title/PR-body derivation, label mapping and the label-exists check
- `reference/_phase2_execute.md` — title and plan confirmation, execution rules and error recovery
- `tests/evals.yaml` — 12 test scenarios covering every phase, both confirmation steps, a rejected push and the 20-file limit
- `scorecard_git_create_pr.md` — 7-dimension quality scorecard
