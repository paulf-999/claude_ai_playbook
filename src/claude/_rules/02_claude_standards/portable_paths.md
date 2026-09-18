# 🌍 Portable Paths

**Purpose:** Prevent hooks and tests from hardcoding a specific machine's filesystem layout — the Claude config directory is not always at the OS default location, and code that assumes it is breaks silently elsewhere.

---

## 🎯 Core principle

**Never hardcode an absolute path, username, or literal `~/.claude`/`~/claude` reference.** Always resolve the config directory dynamically — from `CLAUDE_CONFIG_DIR` in Python, or from the script's own location in shell. A hook or test that works on one machine and silently breaks on another has failed its job.

**Why:** This config is deliberately deployed at non-default locations (`~/claude`, no dot, on this account's live machine; a repo checkout under test in the playbook). Code that hardcodes `~/.claude/...` or another machine's username passes locally and fails everywhere else — and fails silently, since shell `source ... || true` and Python's bare `except` patterns both swallow the resulting error.

---

## 🐛 Real incidents (evidence, not hypothetical)

Found in one session (2026-09-17), all three shipped without failing until tested on a second machine:

- **Test files:** `test_response_standards_hook.py` / `_inject.py` hardcoded `/home/paul/.claude/hooks/...` — a different user's home directory from a different machine entirely.
- **Test-harness bug:** `test_rules_structure.py`'s import-reachability check used `Path(...).expanduser()`, resolving `~` against the real `$HOME` instead of substituting `CLAUDE_CONFIG_DIR` — always failed off the one machine it was written on.
- **Hook scripts:** `hook_enforcement_dir_structure.sh` / `_naming_convention.sh` hardcoded `source ~/.claude/_templates/utils/shell_utils.sh` — on a machine where the config lives at `~/claude` (no dot), `~/.claude/` exists (Claude Code's own state dir, `ide`/`projects`) but has no `_templates/`, so the hook always failed.
- **This rule's own test, written minutes later (2026-09-18):** `test_always_on_reachability.py`'s import parser recognized only the literal string `"@~/.claude/"` — would have silently found zero imports and reported every file orphaned had it been ported to live's `~/claude/`-convention config unmodified.

---

## ✅ How to apply

**Python (tests, scripts):**
- **Resolve via `CLAUDE_DIR`:** import `from _claude_dir import CLAUDE_DIR` and build paths as `CLAUDE_DIR / "hooks" / "x.sh"` — never `Path("~/.claude/hooks/x.sh").expanduser()`.
- **Never hardcode a username or absolute path:** no `/home/<name>/...`, no `/Users/<name>/...` as a literal string used for real path resolution.
- **`.expanduser()` is reserved for `_claude_dir.py` itself** — that's the one file whose job is turning `~` into a real path; nowhere else should call it.
- **Never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines** — the config-dir name varies. Detect any `@~/<name>/` prefix generically and strip through the first two path segments; don't match on one literal convention.

**Shell (hooks):**
- **Resolve relative to the script's own location:** `CLAUDE_ROOT_DIR="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"`, then reference `"${CLAUDE_ROOT_DIR}/_rules/..."` — never `~/.claude/...` or `~/claude/...` as a literal string.
- **Guard clauses too:** a check like `[[ "$FILE_PATH" != *".claude/"* ]]` is the same anti-pattern — compare against the resolved `CLAUDE_ROOT_DIR`, not a hardcoded substring.

**Both:** test data (example strings inside a fixture payload, illustrative comments) is not a violation — this rule is about paths actually used for file I/O or process execution, not text a test happens to contain.

---

## 🔗 Related rules

- `testing.md` — every hook and script needs a test; this rule is part of what "correct" looks like
- `authoring_rules.md` / `authoring_skills.md` — apply this when writing any new hook, test, or script
