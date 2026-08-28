# 🧪 Tests

Tests verify that enforcement hooks and rule files behave as intended.
Run from within each subdirectory using `pytest`.

```bash
cd ~/.claude/_tests/hooks && pytest -v
cd ~/.claude/_tests/rules && pytest -v
```

---

## 📁 Subdirectories

### `hooks/`

Tests for Claude Code hook scripts in `~/.claude/hooks/`.

| File | What it tests |
|---|---|
| `hook_test_utils.py` | Shared `run_hook()` utility — pipes a JSON payload to a hook and returns the result |
| `test_style_guides.py` | All `hook_style_guide_*.sh` hooks — parametrized; tests trigger paths, non-trigger paths, and wrong-tool pass-through |
| `test_style_guide_dispatch.py` | `hook_style_guide_dispatch.sh` — routing, no-match silence, and multi-guide aggregation |
| `test_writing_style_rule.py` | `hook_style_guide_writing.sh` — injects writing_style.md for `_rules/` edits |
| `test_enforcement_autotest.py` | `hook_enforcement_autotest.sh` — blocks when test suite fails; uses fake `python3` binary to avoid recursive pytest |
| `test_enforcement_dir_structure.py` | `hook_enforcement_dir_structure.sh` — injects dir structure rules for `mkdir` under `~/.claude/` |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — blocks new files under `~/.claude/` |
| `test_enforcement_subagent_reads.py` | `hook_enforcement_subagent_reads.sh` — injects sub-agent reminder for unscoped external reads |
| `test_enforcement_task_tracking.py` | `hook_enforcement_task_tracking.sh` — injects TaskCreate reminder for multi-step prompts |
| `test_hook_registry.py` | `settings.json` hook registry — every referenced hook file must exist on disk |

### `rules/`

Tests for structural properties and behavioral compliance of files in `~/.claude/_rules/`.

| File | What it tests |
|---|---|
| `test_rules_structure.py` | File quality across all `_rules/` files — line limits, trailing newlines, expected file set |
| `test_lazy_load_coverage.py` | Every `lazy_load/` file is reachable from at least one hook (direct or via a parent index file) |
| `test_guiding_principles.py` | Enforcement of lazy-load defaults and intentionality gates — no lazy_load/ imports in CLAUDE.md, all imports documented |
| `test_aliases_behavior.py` | Aliases are documented, properly formatted, and validated as functional (spot-check representative aliases) |
| `test_testing_rule_compliance.py` | Self-consistency check: enforcement hooks have tests, and testing.md documents the enforcement pattern |

---

## 📐 When to add a test

Per `_rules/behaviour.md` — adding or modifying an **enforcement hook** requires a corresponding test.
Instructional rules (files Claude reads but no mechanical hook fires) do not require tests; structural quality is covered by `test_rules_structure.py`.
