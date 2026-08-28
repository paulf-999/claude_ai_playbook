# 🌿 Rules — Git

**Purpose:** Establish best practices for git workflow, commits, branch management, and pull requests to maintain clean history, safe operations, and clear communication.

## 📋 Contents

- [Safe Git Patterns](#-safe-git-patterns) — `_safe_patterns.md`
- [Commits](#-commits) — `_commits.md`
- [Complex Git Operations](#-complex-git-operations)
- [Protected Branches](#-protected-branches)
- [Branch Naming](#-branch-naming)
- [Pull Requests](#-pull-requests)

---

## 🔒 Safe Git Patterns

@~/.claude/_rules/02_claude_standards/git/_safe_patterns.md

---

## 📝 Commits

@~/.claude/_rules/02_claude_standards/git/_commits.md

---

## 🧩 Complex Git Operations

- **Flag before acting:** before reaching for `git stash`, `git reset --soft`/`--hard`, or reconciling changes across several branches, pause and state plainly that the operation is getting complex — propose the simplest alternative before executing.
- **Simplest over proper:** prefer the simplest correct option over the most "proper" one — e.g. redoing a small edit directly on a second branch is often simpler and safer than juggling a stash across branch switches.
- **Never silently resolve a stash:** if a stash is created mid-task, surface what it contains and why to the user — do not drop or pop it unilaterally.

---

## 🔒 Protected Branches

- **Never commit to main:** `main` is the long-lived production branch — all work goes through short-lived `feature/`, `hotfix/`, or `release/` branches merged via PR.

---

## 🏷️ Branch Naming

- **Prefix:** `feature/` for new features, `hotfix/` for urgent fixes, `release/` for bulk changes spanning 20+ files
- **Characters:** lowercase only, letters/numbers/underscores — no hyphens, spaces, or special characters
- **Pattern:** `^(feature|hotfix|release)/[a-z0-9_]+$`
- **Examples:** `feature/add_pr_template`, `hotfix/fix_commitlint`, `release/new_col_all_int_dim_merchant_models`

---

## 📋 Pull Requests

- **Use gh CLI:** use the `gh` CLI for all GitHub PR operations — do not attempt GitHub MCP tools without first confirming access is available.
- **PR template required:** always use `.github/pull_request_template.md` as the PR body — read the file before raising any PR, never substitute a custom format.
- **Edit in scope:** when editing an existing PR description, only modify the sections explicitly specified.
- **Size limit:** PRs must contain fewer than 20 files — split if needed.
  - **Note:** if a change genuinely cannot be split, use a `release/` branch and ensure the PR applies the same type of change consistently.
- **Title format:** Conventional Commits — `type(scope): description`; description must be non-technical, written for a mixed audience.
- **Summary:** 1 sentence, 2 at most — non-technical, no code references or implementation detail.
- **Breaking changes:** flag explicitly and describe the rollout impact.
- **No conflict markers:** files must not contain merge conflict markers.

---

## 🔗 Related Rules

- `testing.md` — test requirements and design patterns
- `behaviour.md` — safe action defaults and decision-making
