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

[Phase 2] Plan Review

Title: feat: add user authentication
Source branch: feature/add_user_authentication
Target branch: main
Files changed: 3 files (+45 insertions, -12 deletions)

Confirm (y) · Edit (e) · Cancel (n): y

[Phase 3] Creating PR...
          ✓ Branch created
          ✓ Changes committed
          ✓ Pushed to origin
          ✓ PR created

PR #1234 created and verified: https://github.com/org/repo/pull/1234
```

**Best for:** Routine feature/hotfix PRs. Full workflow automation — branch creation, conventional commit, PR with validated title/labels — in one command.

**Special Note — Response Standards Waiver:**
- This skill uses custom interactive output format (multi-turn workflow with confirmation points)
- Free-form prompts are incompatible with standard Claude response formatting requirements
- The response standards rule makes an exception for this skill to preserve interactive capability

---

## Scope gate

This skill is at **tactical** maturity. Work through phases in order with light error handling.

---

## ⚠️ Pre-check

Before proceeding, run `git status` to confirm Bash is available. If it fails, stop and tell the user Bash access is required.

---

## 🔍 Phase 1 — Gather information

See `reference/_git_pr_formatting_conventions.md` — branch naming, commit message format, PR title/body standards, and label derivation.

---

## 🚀 Phase 2 — Execute

Create the branch, stage files, commit, push, and open PR on GitHub. Do not proceed if diff exceeds 20 files.

---

## ✅ Phase 3 — Verify

Run `gh pr view <number> --json title,labels` and verify:
1. **Labels:** non-empty array (add if needed)
2. **Title:** matches `^(feat|fix|chore|docs|refactor|test|ci)(\([^)]+\))?: [a-z]`
3. **Cleanliness:** no file extensions, path separators, or backticks

Report PR URL and ask if user wants to run follow-up skills (`/git_review_pr` or `/git_notify_pr`).

---

**For detailed specifications, see:**
- `reference/_git_pr_formatting_conventions.md` — Branch naming, commit format, PR title/body standards
- `reference/_implementation.md` — Error handling, tool references
- `reference/_format_standards.md` — Conventional Commits, branch naming, and PR formatting standards
- `reference/_testing_section_template.md` — How to populate testing section with evidence
- `reference/_quality_scorecard.md` — Quality assessment
