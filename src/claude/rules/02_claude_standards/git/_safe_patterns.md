<!-- version: 2.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-25 -->
# 🔒 Safe Git Patterns

**Purpose:** Keep git from running code planted in an untrusted repository, and keep git commands from changing the shell's working directory.

---

## ⚠️ Untrusted repositories

- **Hooks run either way:** git runs a repository's `.git/hooks/` scripts whether you `cd` into it or use `git -C`, so `git -C` is not a safety control.
- **Config can run code too:** a repository's own `.git/config` can set options such as `core.fsmonitor` or `core.pager` that run commands, even for a read-only command like `git status`.
- **Default:** don't run git in a repository that you didn't create or clone from a trusted source.
- **If you must:** ask first, then turn off hooks, the file monitor and the pager for that command with `git --no-pager -c core.hooksPath=/dev/null -c core.fsmonitor=false -C <repo> <command>`.

## 📍 Use `git -C`, not `cd && git`

- **Rule:** write `git -C /path/to/repo <command>` instead of `cd /path/to/repo && git <command>`.
- **Why:** the shell's working directory stays where it was, so later commands don't run in the wrong folder.
- ❌ `cd /repo && git status`
- ✅ `git -C /repo status`
- **Scope:** this applies to every git command, and destructive ones such as `reset --hard` and `push --force` still need confirmation under `git.md`.
