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
<!-- version: 1.4.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** run `gh auth status` and confirm `.github/pull_request_template.md` exists, and stop and tell the user if either fails.
- **Read first:** read `reference/_phase1_gather.md`, then `reference/_phase2_execute.md` before running any git command.
- **Always:** confirm the PR title, then the full plan, before creating a branch, committing or pushing.
- **Always:** stage files by name, and draft the PR body from the repo template using `subagent_type: technical_writer`.
- **Never:** commit to `main`, force-push, or use `--no-verify` unless the user explicitly asks.
- **Never:** open a PR of 20 or more files without flagging it and suggesting a split.

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

Routine feature and hotfix PRs, faster than the manual git workflow and with Conventional Commits enforced. Currently at the **tactical** stage — main path, both confirmation steps and push errors are covered, but not merge conflicts or non-main base branches.

## 📚 References

- `reference/_phase1_gather.md` — gather-info logic, branch/commit/PR-title/PR-body derivation, label mapping and the label-exists check
- `reference/_phase2_execute.md` — title and plan confirmation, execution rules and error recovery
- `tests/evals.yaml` — 12 test scenarios covering every phase, both confirmation steps, a rejected push and the 20-file limit
- `_admin/_quality_scorecards/skills/scorecard_git_create_pr.md` — 7-dimension quality scorecard
