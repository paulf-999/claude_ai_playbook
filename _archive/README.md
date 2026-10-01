# 🗄️ Archive

**Purpose:** Keep retired config files out of the installed config while leaving them easy to find and restore.

- **Layout:** each file keeps its original repo path under `_archive/`, e.g. `_archive/src/claude/_rules/...`.
- **Not installed:** `make install` copies only `src/claude/`, so nothing here reaches `~/.claude/`.
- **Not tested:** the test suite and the usage audit don't scan this folder.
- **Restore:** `git mv` the file back to the path under `_archive/`.

## 📋 Archived files

| File | Archived | Why |
|---|---|---|
| `src/claude/_rules/05_lazy_load/environment_setup/ohmyzsh_setup.md` | 2026-10-01 | Nothing pointed to it and it had no trigger, so it loaded in 0 of 115 measured sessions |
| `src/claude/_admin/_quality_scorecards/rules/05_lazy_load/environment_setup/scorecard_ohmyzsh_setup.md` | 2026-10-01 | Its scorecard, archived with it |
