---
name: git_create_pr
description: Create GitHub PR with staged changes, commit message, and PR body
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
  test_coverage_level: comprehensive
---

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

**Best for:** Routine feature/hotfix PRs. Faster than manual git workflow; enforces Conventional Commits automatically; minimal setup required.

---

**For detailed specifications, see:**
- `reference/_implementation.md` — Phase 1/2/3 logic, error handling, validation
- `reference/_formats.md` — Conventional Commits rules, branch naming, PR formatting
- `reference/_quality_scorecard.md` — Quality assessment and design rationale
