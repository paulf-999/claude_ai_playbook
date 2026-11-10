# 🛠️ git_create_pr — Implementation

**Purpose:** Map the skill's two phases to the files that hold their detail, so Claude knows what to read and in what order.

## 🔄 Phases

| Phase | What happens | Detail |
|---|---|---|
| **1 — Gather** | Read-only checks, then derive the branch, files to stage, commit message, PR title, body and labels | `_phase1_gather.md` |
| **2 — Confirm** | Show the title, every command, the commit message and the full PR body in one prompt, then wait for a yes before branching, committing or pushing | `_phase2_execute.md` → Confirm |
| **2 — Execute** | Create the branch, stage files by name, commit, push and open the PR with `gh pr create` | `_phase2_execute.md` → Execution rules |

## 🚨 Error handling

- **Missing prerequisite:** stop before Phase 1 if `gh auth status` fails or `.github/pull_request_template.md` is missing.
- **Nothing to commit:** stop in Phase 1 when the working tree is clean.
- **Rejected push or failed `gh` call:** follow `_phase2_execute.md` → Error recovery, which never force-pushes.
- **20 or more files:** flag it and suggest a split before Phase 2.
