<!-- version: 2.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 📍 Test File Organisation

**Purpose:** Where tests live and how to name them.

---

- **Default location:** `_tests/<domain>/test_<feature>[_<aspect>].py`, mirroring the domain of the code under test.
- **Colocate instead:** when a test covers one artefact and its maintainer is the audience — e.g. a skill's `tests/evals.yaml`.
- **Centralise:** when a test sweeps many artefacts or shares fixtures — e.g. `test_no_orphaned_skill_files.py`.
- **Pytest files stay central:** moving a `.py` test changes shared `pytest.ini` collection config, so check the runner still finds it before colocating one.
- **Mirror the target filename:** a structural test for one rule or `hooks/` file is named after it — `git.md` → `test_git.py`, `_decision_making.md` → `test_decision_making.py`.
  - **No tier in the name:** the test's subdirectory (e.g. `_tests/rules/02_claude_standards/`) already carries it.
  - **No single target:** name it for what it validates — e.g. `test_lazy_load_coverage.py`.
- **One goal per test function:** its name says what it validates.
