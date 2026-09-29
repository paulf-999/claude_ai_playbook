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
<!-- version: 1.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-29 -->

## 🎯 Purpose

Automate the full PR creation workflow with minimal user intervention:
- **Branch creation** — derive and create feature/hotfix branch from user input
- **Commits** — stage, compose, and push changes with Conventional Commits format
- **PR opening** — populate title, body, labels, and create PR on GitHub
- **Confirmation** — preview before creation; allow title/body edits or manual cleanup

## 💡 Example Usage

```
$ /git_create_pr add user authentication
[Phase 1] Deriving branch name: feature/add_user_authentication
          Commit message: feat: add user authentication
          PR title: feat: add user authentication

[Phase 2] Executing...
          ✓ Branch created
          ✓ Changes committed
          ✓ Pushed to origin

[Phase 3] PR ready to create
          Happy with title/body? (y/e/n): y

PR #1234 created: https://github.com/org/repo/pull/1234
```

## ✨ Best For

Routine feature/hotfix PRs. Faster than manual git workflow; enforces Conventional Commits automatically; minimal setup required.

## 📚 References

- `reference/_phase1_gather.md` — gather-info logic, branch/commit/PR-title/PR-body derivation, and label mapping
- `tests/evals.yaml` — 11 test scenarios covering every phase, both confirmation answers and the 20-file limit
- `scorecard_git_create_pr.md` — 7-dimension quality scorecard
