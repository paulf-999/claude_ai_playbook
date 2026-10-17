# 🧪 Tests

**Purpose:** Check that every part of the Claude config (rules, skills, agents, hooks, settings and scripts) is well formed and behaves as intended, so a broken change fails here before it reaches a live session.

## 🎯 Summary

- **One suite:** run everything at once with `pytest`, and it checks whichever config `CLAUDE_CONFIG_DIR` points at.
- **Named after what they test:** each folder is named after the config folder or files it checks, apart from `_core/`.
- **Repo-only tests:** checks on the repo itself, like its docs links, live in [repo-root `tests/`](../../../tests/docs/README.md) so they never install.
- **`_core/` is the shared engine:** it holds the helpers every other folder imports and the few tests that span the whole config.
- **Per-folder detail:** each folder's README lists its tests, with Quality, Created, Updated and Version copied from each test's own metadata header.

## ▶️ Running the tests

```bash
# Playbook repo: from the repo root, where pytest.ini adds coverage and the install tests
CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest src/claude/_tests

# Live config: from the config folder
cd ~/.claude && python3 -m pytest _tests
```

- **Why set `CLAUDE_CONFIG_DIR`:** without it, the suite may check your live config instead of the repo.

## 🗂️ What each folder tests

| Folder | What it tests | What it checks |
|---|---|---|
| [`_core/`](_core/README.md) | None, it's shared infrastructure | Helpers used across the suite, plus whole-config checks like file naming |
| [`_reference/`](_reference/README.md) | Quality scorecards in `_reference/_quality_scorecards/` | Every artefact has a scorecard, and its dates are valid |
| [`agents/`](agents/README.md) | Sub-agents | Agent headers and triggers |
| [`hooks/`](hooks/README.md) | Hooks | Hook headers, registration and each hook's behaviour |
| [`rules/`](rules/README.md) | Rules | Rule structure, loading, headers and cross-references, by tier |
| [`root_files/`](root_files/README.md) | Single files at the config root | `settings.json` permissions and `aliases.md` entries |
| [`scripts/`](scripts/README.md) | Maintenance scripts | Each script's behaviour and naming |
| [`skills/`](skills/README.md) | Skills | Skill structure, headers, references and each skill's own scripts |

## 🧩 Why `_core/` exists

Every other folder maps to one kind of artefact, but some code and checks belong to none of them.

- **Shared helpers:** path resolution, the file-structure scanner and the metadata-header validator are used by tests in several folders, so they live in one place.
- **Whole-config tests:** checks like "every file in the config is named correctly" cover all artefacts at once, so they sit beside the helpers they use.
- **How tests find it:** `conftest.py` puts `_core/` on `sys.path`, so tests import helpers by name, e.g. `from _shared_paths import CLAUDE_DIR`.
- **Why the `_` prefix:** it marks the folder as infrastructure rather than an artefact type, and sorts it first.
- **Its helpers:** listed in [`_core/README.md`](_core/README.md).

---

## 📐 When to add a test

- **Enforcement hooks:** adding or changing one needs a matching test, per `rules/02_claude_standards/behaviour.md`.
- **Instructional rules:** files Claude reads but no hook enforces need no test of their own, because `test_rules_structure.py` covers their structure.
