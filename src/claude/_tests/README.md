# 🧪 Tests

**Purpose:** Check that every part of the Claude config (rules, skills, agents, hooks, settings and scripts) is well formed and behaves as intended, so a broken change fails here before it reaches a live session.

## 🎯 Summary

- **One suite:** run everything at once with `pytest`, and it checks whichever config `CLAUDE_CONFIG_DIR` points at.
- **Named after what they test:** each folder is named exactly after the config folder it checks, including `_reference/`; only `_docs/`, `_helpers/`, `_root_files/` and `_shared_checks/` match no config folder, which their underscore-led names keep apart.
- **`_helpers/` is the shared engine:** it holds the helpers every other folder imports, and no tests.
- **`_shared_checks/` proves the shared checks:** it holds the tests for the checks every artefact type shares, and the scan that runs them over the whole config.
- **Per-folder detail:** each folder's README lists its tests, with Quality, Created, Updated and Version copied from each test's own metadata header.

## ▶️ Running the tests

```bash
# Playbook repo: from the repo root, where pytest.ini adds coverage and the install tests
CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest

# Live config: from the config folder
cd ~/.claude && python3 -m pytest _tests
```

- **Why set `CLAUDE_CONFIG_DIR`:** without it, the suite may check your live config instead of the repo.

## 🗂️ What each folder tests

| Folder | What it tests | What it checks |
|---|---|---|
| [`_docs/`](_docs/README.md) | The repo's own docs, not the config | Local links in the repo's `README.md` and `docs/` |
| [`_helpers/`](_helpers/README.md) | None, it's shared infrastructure | Helpers used across the suite |
| [`_root_files/`](_root_files/README.md) | Single files at the config root | `settings.json` permissions and `aliases.md` entries |
| [`_shared_checks/`](_shared_checks/README.md) | Checks every artefact type shares | File naming and structure, rule loading, the shared metadata-header format and the Python version check |
| [`_reference/`](_reference/README.md) | Quality scorecards in `_reference/_quality_scorecards/` | Every artefact has a scorecard, and its dates are valid |
| [`agents/`](agents/README.md) | Sub-agents | Agent headers and triggers |
| [`hooks/`](hooks/README.md) | Hooks | Hook headers, registration and each hook's behaviour |
| [`rules/`](rules/README.md) | Rules | Rule structure, loading, headers and cross-references, by tier |
| [`scripts/`](scripts/README.md) | Maintenance scripts | Each script's behaviour and naming |
| [`skills/`](skills/README.md) | Skills | Skill structure, headers, references and each skill's own scripts |

## 🧩 Why `_helpers/` and `_shared_checks/` exist

Most folders map to one config folder, but some code and checks belong to none of them.

- **Shared helpers:** path resolution, the file-structure scanner and the metadata-header validator are used by tests in several folders, so they live in one place.
- **Shared checks:** checks like "every file is named correctly" apply to every artefact type, so their tests live in `_shared_checks/` rather than beside any one artefact's tests.
- **How tests find it:** `conftest.py` puts `_helpers/` on `sys.path`, so tests import helpers by name, e.g. `from _shared_paths import CLAUDE_DIR`.
- **Why the `_` prefix:** it marks the folder as infrastructure rather than an artefact type, and sorts it first.
- **Its helpers:** listed in [`_helpers/README.md`](_helpers/README.md).

---

## 📐 When to add a test

- **Enforcement hooks:** adding or changing one needs a matching test, per `rules/02_claude_standards/behaviour/_how_to_approach.md`.
- **Instructional rules:** files Claude reads but no hook enforces need no test of their own, because `test_rules_structure.py` covers their structure.
