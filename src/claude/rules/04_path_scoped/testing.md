---
paths:
  - "**/*.py"
  - "**/*.sh"
  - "**/*.sql"
  - "**/_tests/**"
---
<!-- version: 1.5.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-10 -->
<!-- miss_cost: medium — untested code the user catches in review -->
<!-- loading: path-scoped — only matters when writing code, so it loads when a Python, shell or SQL file is open -->
# 🧪 Testing

**Purpose:** Every new code artifact needs a test to prevent regressions and validate intended behavior.

**Rule of thumb:** if you added code, write a test.

---

## ✅ When Tests Are Required

- **🆕 New features:** CLI commands, config settings, skills and hooks all need tests.
- **🧩 New abstractions:** functions, classes, utilities and rule files need tests.
- **🔧 Breaking changes:** changed behaviour needs updated tests.
- **🐛 Bug fixes:** include a regression test so the bug can't recur.
- **📄 Instructional content:** READMEs and docs need no behaviour test, since following a rule can't be graded without a live-session eval harness.
  - **Note:** `test_rules_structure.py` already checks every rule's file quality.
- **🧷 Content-regression test:** when a rule records a real incident or hard-won lesson, assert its key phrases survive, as `test_git.py` does.
  - **Why:** it catches silent loss of the text in a later edit or merge, so reserve it for content that would be costly to lose.

---

## 🎯 Test Goals (What to Validate)

Define the goal before writing the test, because tests validate *intended behavior*, not just "the code runs."

- **Specific:** "accurate sentiment classification", not "good performance".
- **Measurable:** quantifiable metrics (F1, accuracy) or well-defined qualitative scales.
- **Achievable:** based on benchmarks and your real requirements.
- **Relevant:** aligned with the application's real purpose, not hypothetical edge cases.
- **LLM-facing code:** cover ambiguous inputs, mixed signals (sarcasm), adversarial prompts and malformed text.

| Goal | Example | Purpose |
|---|---|---|
| **Structure** | `test_aliases.py` | Config file structure and required fields are valid |
| **Behavior** | `test_aliases_behavior.py` | Feature works as documented |
| **Principles** | `test_settings.py` | Change aligns with guiding principles |
| **Integration** | Skill runs end-to-end | Feature integrates with the rest of the system |
| **Regression** | Bug fix test | Bug won't silently reappear |
| **Consistency** | Style guide hooks | Standards enforced, with no exceptions |

---

## 🧱 Test Layers

`_tests/README.md` lists every test file with its scores, so this table shows the layout, not the inventory.

| Layer | What it catches | Where it lives |
|---|---|---|
| **Structure** | Format and layout drift across many files | `test_rules_structure.py`, `test_rules_structure_layout.py`, `test_file_structure_compliance.py` |
| **Reachability** | Misplaced files under `rules/`, dead pointers and unlinked lazy files | `test_always_on_reachability.py`, `test_lazy_load_coverage.py` |
| **Metadata** | Missing or malformed version/created/updated headers | `test_claude_config_metadata.py` and the hook, agent and skill header tests |
| **Rule content** | Silent loss of a rule's key guidance | `_tests/rules/<tier>/test_<rule>.py`, mirroring the rule's filename |
| **Hooks** | Registered hooks that are missing or stop behaving as documented | `_tests/hooks/`, grouped by hook type |
| **Skills** | Skills that break the authoring standard or carry orphaned files | `_tests/skills/`, plus each skill's own `tests/evals.yaml` |
| **Settings** | Unsafe permissions, secrets and broken aliases | `_tests/settings/`, `test_aliases_behavior.py` |

---

## ✍️ Writing a Test

- **Read on demand:** [`~/.claude/_rules_lazy_load/testing/_testing_design_pattern.md`](../_rules_lazy_load/testing/_testing_design_pattern.md) — before writing a new test: state the goal, test behaviour, write assertion messages, spot-check.
- **Read on demand:** [`~/.claude/_rules_lazy_load/testing/_testing_anti_patterns.md`](../_rules_lazy_load/testing/_testing_anti_patterns.md) — before writing a new test: empty, over-mocked, fragile, slow and unclear tests to avoid.
- **Read on demand:** [`~/.claude/_rules_lazy_load/testing/_testing_file_organization.md`](../_rules_lazy_load/testing/_testing_file_organization.md) — before creating a test file: where it lives and how to name it.
- **Read on demand:** [`~/.claude/_rules_lazy_load/testing/_test_metadata.md`](../_rules_lazy_load/testing/_test_metadata.md) — before writing or editing a test: the required header, and the quality ≥9 and complexity ≥7 floor that `test_test_score_floor.py` enforces.
- **Read on demand:** [`~/.claude/_rules_lazy_load/testing/_test_metadata_audit.md`](../_rules_lazy_load/testing/_test_metadata_audit.md) — when auditing tests: the quarterly audit, worked example and archival workflow.
- **Inventory:** add each new test file to `_tests/README.md`.

---

## 🔄 Running and Maintaining

- **Live config:** run `pytest` from the config root, where `pytest.ini` sets `testpaths = _tests`.
- **Playbook repo:** run `pytest` from the repo root with `CLAUDE_CONFIG_DIR` pointing at `src/claude/`.
- **Paths:** resolve the config directory through `_tests/_shared_paths.py`, never a hardcoded home path, per `portable_paths.md`.
- **Update tests with code:** change a test in the same commit as the behaviour it covers.
- **Delete dead tests:** remove a feature's tests when the feature is removed.
