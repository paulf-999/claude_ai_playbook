<!-- version: 1.1.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-10-01 -->
# 🧮 Test Complexity Scoring (0–10)

**Purpose:** Apply the config's shared complexity formula to tests — reward genuinely simple tests, and make "simple" and "thorough" achievable together rather than in tension.

---

## 📐 The formula

@~/.claude/_rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md

Tests use the *inverted score* defined above: **complexity score = 10 − raw sum**, so a higher number means a simpler test — one concept, one file, no external dependencies, no fixtures scores 10; a sprawling, multi-directory, multi-dependency test scores near 0.

**Example:** `test_portable_paths_python.py` scans one directory (Scope 1), verifies 3 distinct patterns — `.expanduser()`, home-dir constants, import prefixes (Concepts 1), uses no external tools (Dependencies 0), needs no fixtures (Prerequisites 0) → raw complexity 2 → **complexity score 8**.

---

## 📏 Scope for tests

Count top-level folders of the config, not every subfolder a recursive scan passes through.

| Scope | What the test reads |
|---|---|
| **0** | One file, or only temp files the test builds itself |
| **1** | One top-level folder, however deep — e.g. all of `_rules/`, `hooks/` or `_tests/` |
| **2** | Two or more top-level folders, or root files such as `CLAUDE.md` plus a folder |
| **3** | The whole config directory |

- **Why:** a scan of one tree is one place to look, so scoring each subfolder separately pushed simple scans into needless splits (found 2026-10-01).
- **Dependencies:** a test's own helper module (e.g. `_rule_reachability.py`) is the code under test, not a dependency.

---

## 🎯 Quality and complexity are independent, not opposed

Assertion/function *count* (what the quality score measures) and structural complexity (Concepts/Scope/Dependencies/Prerequisites) are different axes. A test can run 20 assertions against a single file with no dependencies and still score complexity 8–10 — thoroughness doesn't require sprawl.

**New tests must reach quality ≥9 AND complexity score ≥7** (raw sum ≤3): write as many assertions and test functions as the artifact genuinely needs, but keep the test structurally simple — one concept, one file, minimal dependencies and fixtures. If hitting quality ≥9 seems to require raw complexity above 3, that's a signal to split the test, not to let complexity slide.

**Don't pad complexity to hit a number.** A single-file content-regression check (see `_concurrent_sessions.md`'s test) is *supposed* to be simple — its natural complexity score is already 8–10. Inflating its scope or dependencies just to move the number is the exact anti-pattern this scoring exists to catch.
