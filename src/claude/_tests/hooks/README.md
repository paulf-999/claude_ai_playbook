# 🧪 `hooks/` tests

**Purpose:** Tests for Claude Code hook scripts in `~/.claude/hooks/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_hook_metadata_header.py` | Every hook script carries a valid metadata header on lines 2–4, after its shebang | 9/10 | 2026-09-29 | 2026-10-17 | 2.0.2 |
| `test_hook_registry_utils.py` | `settings.json` hook registry — known events, command hooks, no duplicates, every referenced hook file exists, and every hook file is registered or listed in `RESERVED_HOOKS` | 8/10 | 2026-08-28 | 2026-10-11 | 2.3.4 |

**Utility (not a scored test):** `hook_test_utils.py` — shared `run_hook()` helper, pipes a JSON payload to a hook and returns the result.

## 📁 `enforcement/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_enforcement_mcp_stale_settings.py` | `hook_enforcement_mcp_stale_settings.sh` — warns once when the disabled MCP servers change mid-session | 10/10 | 2026-09-18 | 2026-10-11 | 2.0.4 |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — denies new config files whose names break the compliance checks, and lets everything else through | 10/10 | 2026-08-28 | 2026-10-11 | 2.1.2 |
| `test_enforcement_markdown_location.py` | `hook_enforcement_markdown_location.sh` — flags stray markdown at the config root and badly named `_reference/` files, using the real stdin payload | 10/10 | 2026-08-28 | 2026-10-11 | 3.1.2 |

## 📁 `response_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_style_guide_response_standards_checker_flags.py` | `hook_style_guide_response_standards_checker.sh` (reserved) — flags a missing Summary, offer line or timing footer, and text after the footer | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.2 |
| `test_style_guide_response_standards_checker_waivers.py` | `hook_style_guide_response_standards_checker.sh` (reserved) — skips short answers, skill output, code blocks, errors and plan-mode output | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.2 |
| `test_style_guide_response_standards_reminder.py` | `hook_style_guide_response_standards_reminder.sh` — per-turn salience injection, timestamp, waiver handling | 10/10 | 2026-09-07 | 2026-10-11 | 2.1.2 |

[← All tests](../README.md)
