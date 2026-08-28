# 🔒 Safe Git Patterns

**Purpose:** Protect against git hook execution risks when running commands in untrusted directories.

---

## 🔒 Git hook execution risk

**Pattern:** `cd && git` compound commands — ALWAYS use `git -C` instead

**Risk:** Git hook execution from untrusted repositories.

When `cd /some/repo && git <command>` runs, git executes hooks from that directory's `.git/hooks/`. If redirected to a malicious repository, those hooks execute silently.

**Mitigation:** Always use `git -C /path/to/repo <command>` instead. This runs the git command in the specified directory without changing the shell's working directory, eliminating the hook-execution risk.

**Rule:** Proactively rewrite compound `cd && git` patterns to use `git -C`:
- ❌ `cd /repo && git status`
- ✅ `git -C /repo status`

This applies to all git commands, including destructive ones (`reset --hard`, `push --force`).

---

## 🔗 Related

- Parent: `git.md` — git workflow, commits, branch naming, pull requests
