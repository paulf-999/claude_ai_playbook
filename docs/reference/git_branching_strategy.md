# 🌿 Git Branching Strategy

This repository uses a simplified branching strategy, with branch naming enforced via a [pre-commit hook](../src/sh/pre_commit_hooks/git_validate_branch_name.sh).

---

## 🌱 Branch Types

| Branch     | Purpose                                                                 |
|------------|-------------------------------------------------------------------------|
| `main`     | 🏠 Long-lived branch containing production-ready code.                     |
| `feature/` | ✨ Short-lived branches for new features. Branch from `main`, merge back into `main`. |
| `hotfix/`  | 🔥 Short-lived branches for urgent fixes to production. Branch from `main`, merge back into `main`. |
| `release/` | 📦 Used for bulk PRs spanning 20+ files (e.g., formatting or linting passes across many models). Must apply the same type of change consistently and be tied to a significant release. |

---

## 📝 Naming Rules

- Allowed prefixes are `feature/`, `hotfix/`, or `release/`.
- The suffix must be lowercase, containing only letters, numbers, and underscores (`a–z`, `0–9`, `_`).
- Hyphens, spaces, and special characters are not permitted.

Regex pattern:

```bash
^(feature|hotfix|release)/[a-z0-9_]+$
```

---

## ✅ Examples

| ✅ Allowed                                        | ❌ Not allowed                    | Reason                        |
|---------------------------------------------------|----------------------------------|-------------------------------|
| `feature/add_pr_template`                         | `feature/add-pr-template`        | Hyphen not allowed            |
| `feature/add_pr_123`                              | `feature/Add_PR`                 | Uppercase not allowed         |
| `hotfix/fix_commitlint`                           | `hotfix/fix commitlint`          | Spaces not allowed            |
| `hotfix/issue_42`                                 | `feature/feature_with$symbol`    | Special characters not allowed |
| `release/new_col_all_int_dim_merchant_models`     | `release/New-Column-Changes`     | Uppercase and hyphens not allowed |

The script [`git_validate_branch_name.sh`](../src/sh/pre_commit_hooks/git_validate_branch_name.sh) enforces these rules — a commit on a non-conforming branch will be rejected with a descriptive error message.
