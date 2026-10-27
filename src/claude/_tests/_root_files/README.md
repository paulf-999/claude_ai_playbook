# 🧪 `_root_files/` tests

**Purpose:** Tests for single files at the config root: `settings.json` and `aliases.md`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_aliases.py` | Each `aliases.md` entry is complete, well formed and unique, its links and controls note stay in sync, core aliases stay documented, and the file has a metadata header | 10/10 | 2026-08-28 | 2026-10-25 | 2.3.0 |
| `test_settings.py` | `settings.json` permission structure, security denies, no broad destructive allows, no auto-approved GitHub or branch writes while reads stay prompt-free, and no real secrets | 9/10 | 2026-08-28 | 2026-10-27 | 1.5.0 |

[← All tests](../README.md)
