# 📝 Commits

**Purpose:** Establish commit boundaries, formatting, and staging discipline to maintain clean history and safe operations.

---

## 📝 Commits

- **Commit at a logical boundary, not on every edit:** during interactive work, hold changes and commit once the task is done.
  - **Mid-iteration:** treat follow-ups, questions, or refinement as a signal the work is still in flight — don't commit or push.
  - **Done means:** a terminal state *and* relevant automated checks pass.
    - **Let the hook gate it:** rely on `pre-commit` rather than pre-running everything each time.
    - **Missing check:** if nothing covers the change, surface the gap and propose a test (see `testing.md` / `behaviour.md`) before committing.
  - **Permission to commit:** an explicit "commit"/"push", a task that names committing as its endpoint, or reaching done in non-interactive mode (`/goal`, `/loop`, auto).
  - **Push timing:** feature-branch pushes within an approved task need no extra confirmation (per `behaviour.md`) — batch to the boundary, not one per micro-commit.
- **Format:** `type(scope): imperative description` (Conventional Commits)
  - `type`: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, etc.
  - `scope`: the affected area (e.g., `dbt`, `pre-commit`, `makefile`)
  - Description: lowercase, imperative, no trailing period
  - Examples: `feat(pre-commit): add ruff`, `fix(dbt): correct model reference`
- **No-verify:** only use `--no-verify` when explicitly instructed — not by default.
- **Stage by name:** stage specific files by name — never `git add -A` or `git add .` without review.
- **Confirm branch:** run `git branch --show-current` before staging and confirm it matches the expected branch.
  - **Note:** if it does not match, stop and alert the user — do not stage or commit until confirmed.
- **After stash/switch:** run `git diff --name-only origin/<branch>` before staging — only stage files that belong to the current task.
- **Logical commits:** group related changes into a single commit — one commit per logical change, not one per file.
- **Heredoc messages:** always pass commit messages via heredoc to preserve formatting.

---

## 🔗 Related

- Parent: `git.md` — safe patterns, branch naming, pull requests, complex operations
