# 🔀 Concurrent Sessions — Shared Working Tree Safety

**Purpose:** Prevent one Claude Code session from silently absorbing or corrupting another session's uncommitted work when both operate on the same git working tree at once.

---

## 📅 Real incident (2026-09-21)

While building several PRs in one session, another Claude Code session was concurrently working in the *same* working tree. The git index accumulated a mix of both sessions' staged content. A `git commit` for an unrelated PR nearly included three files from the other session (`confluence_create_page_handler.py`, `jira_create_handler.py`, `_confluence_page_formatting.md`) before this was caught. Later, a `git stash pop` produced a merge conflict against the other session's concurrent edits, and a pre-commit hook failure turned out to be caused by an orphaned file the other session had left mid-rename — not a defect in the change being committed.

---

## 🔍 Detect early, don't assume

- **Unfamiliar staged/unstaged content:** if `git status` shows files you didn't touch, stop and ask whose they are — don't assume they're safe to include or safe to discard.
- **Shifting state between checks:** if `git status` shows *more* changes on a second look than the first, another process is actively writing to this working tree — say so explicitly before continuing.
- **Investigate before deleting or overwriting:** per `behaviour.md`, unfamiliar state is a signal to look closer, not a green light.

## 🧹 Never blind-stage

- **Stage by explicit filename only:** never `git add -A` or `git add .` (already required by `_commits.md`) — this is the single control that prevents contamination.
- **Re-verify column-by-column before committing:** `git status --short`'s first column is staged, second is unstaged (`M ` vs ` M`) — misreading this is an easy, real mistake; check every line, not just the filenames.
- **Reset before each separate commit:** when building multiple unrelated commits/PRs from one working tree, run `git reset` (unstages only, never touches file content) before staging each one's specific files — don't assume the index is clean just because you didn't add anything new.

## 🗄️ Stash operations compound the risk

- **`git stash pop` can conflict with concurrent edits:** treat any pop that reports a conflict as a signal to inspect carefully, not to accept either side blindly.
- **Re-run `git status` after every stash operation:** confirm the staged/unstaged split still matches what you intend before proceeding.
- **Never drop a stash you didn't create:** if `git stash list` shows an entry from another branch or session, leave it — per `git.md`'s existing stash rule.

## 🪝 Pre-commit hook isolation can mask the real cause

- **A hook failure may come from someone else's uncommitted content:** pre-commit's stash-based isolation still includes untracked files already on disk (e.g. from another session's incomplete work) unless explicitly excluded.
- **Replicate the isolation manually before assuming your change is broken:** `git stash push --keep-index --include-untracked` then re-run the failing check — if it passes in isolation but fails via the real hook, the difference (often an untracked file) is the actual cause.

## 🌳 Prefer a worktree when overlap is likely

- **If you know another session is or will be active on this repo, suggest `git worktree`:** a separate worktree gives each session its own working directory and index, eliminating this entire class of problem.
- **This applies to your own sub-agents too:** when spawning agents that will touch git state, prefer `isolation: "worktree"` over sharing the current working tree.

---

## 🔗 Related

- Parent: `git.md` — git workflow, commits, branch naming, pull requests
- Sibling: `_safe_patterns.md` — hook-execution risk in untrusted repos
- Sibling: `_commits.md` — stage-by-name, branch confirmation, logical commits
- `behaviour.md` — investigate unfamiliar state before overwriting or deleting
