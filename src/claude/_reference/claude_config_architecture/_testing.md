---
created: 2025-11-15
last_modified: 2026-09-29
---

# 🧪 Testing Strategy

How the Claude config's pytest suite is organised, and where a new test belongs.

This page explains the layout, not the inventory — `_tests/README.md` lists every test file with its quality score and dates, so check there for what currently exists.

---

## 🧱 Test layers

| Layer | What it catches | Where it lives |
|---|---|---|
| **Structure** | Format and layout drift across many files at once | `_tests/rules/test_rules_structure.py`, `_tests/test_file_structure_compliance.py` |
| **Reachability** | Always-on files that are never imported, and lazy-load files nothing links to | `_tests/rules/02_claude_standards/test_always_on_reachability.py`, `_tests/rules/05_lazy_load/test_lazy_load_coverage.py` |
| **Metadata** | Missing or malformed version/created/updated headers | `test_claude_config_metadata.py`, `test_hook_metadata_header.py`, `test_agent_metadata_header.py`, `test_skill_metadata_header.py` |
| **Rule content** | Silent loss of a rule's key guidance in a later edit | `_tests/rules/<tier>/test_<rule>.py` |
| **Hooks** | Hooks registered in `settings.json` that are missing, or that stop behaving as documented | `_tests/hooks/` |
| **Skills** | Skills that break the authoring standard or carry orphaned files | `_tests/skills/` |
| **Settings** | Unsafe permissions or secrets in `settings.json`, and aliases that don't work | `_tests/settings/`, `_tests/rules/test_aliases_behavior.py` |

---

## 📏 Structure and reachability

- **Rule format:** `test_rules_structure.py` checks line limits, H1 and H2 emoji headings and trailing newlines.
- **Rule layout:** `test_rules_structure_layout.py` checks where rule files live, that every `@import` resolves, and that `CLAUDE.md` imports tiers in order.
- **Context budget:** the same file fails on a `## Related` section outside a README, or a Contents section on a file with fewer than 3 real headings.
- **Naming and placement:** `test_file_structure_compliance.py` checks snake_case names, underscore prefixes and where directories sit.
- **Reachability:** `test_always_on_reachability.py` fails if a file under `rules/` would load wrongly — a README, `_lazy_load/` folder, `@import` or unscoped `04_path_scoped/` file — or a Read-on-demand pointer leads nowhere.

---

## 🧩 Rule, hook and skill tests

- **Rule content tests:** mirror the target filename and tier folder (e.g. `git/_concurrent_sessions.md` → `_tests/rules/02_claude_standards/test_concurrent_sessions.py`) — see `testing.md` for the naming rule.
- **Hook tests:** grouped by hook type under `_tests/hooks/` (`enforcement/`, `response_standards/`, `session_start/`), plus a registry check that every hook `settings.json` references exists.
- **Skill tests:** `_tests/skills/` holds cross-skill checks and handler tests, while each skill's `evals.yaml` lives in that skill's own `tests/` folder — see `authoring_skills.md`.

---

## ▶️ Running the suite

- **Live config:** run `pytest` from the config root — its `pytest.ini` sets `testpaths = _tests`.
- **Playbook repo:** run `pytest` from the repo root with `CLAUDE_CONFIG_DIR` pointing at `src/claude/`.
- **Paths:** tests resolve the config directory through `_tests/_shared_paths.py`, never a hardcoded home path — see `portable_paths.md`.

---

## ➕ Adding a test

- **Where:** `_tests/<domain>/test_<feature>.py`, following the colocate-vs-centralise guidance in `testing.md`.
- **Header and floors:** every new test carries the metadata header and must reach quality ≥9 and complexity score ≥7 — see `testing.md`'s Test Metadata Standard.
- **Inventory:** add the new file to `_tests/README.md`.
