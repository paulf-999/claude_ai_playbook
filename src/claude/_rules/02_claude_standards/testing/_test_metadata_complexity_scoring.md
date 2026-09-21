# 🧮 Test Complexity Scoring (0–10)

**Purpose:** Apply the config's shared complexity formula to tests — reward genuinely simple tests, and make "simple" and "thorough" achievable together rather than in tension.

---

## 📐 The formula

@~/.claude/_rules/03_authoring_guidelines/_complexity_scoring.md

Tests use the *inverted score* defined above: **complexity score = 10 − raw sum**, so a higher number means a simpler test — one concept, one file, no external dependencies, no fixtures scores 10; a sprawling, multi-directory, multi-dependency test scores near 0.

**Example:** `test_portable_paths.md`'s test scans 2 directories (Scope 1), verifies 3 distinct patterns — hardcoded source, `.expanduser()`, home-dir constants (Concepts 1), uses no external tools (Dependencies 0), needs no fixtures (Prerequisites 0) → raw complexity 2 → **complexity score 8**.

---

## 🎯 Quality and complexity are independent, not opposed

Assertion/function *count* (what the quality score measures) and structural complexity (Concepts/Scope/Dependencies/Prerequisites) are different axes. A test can run 20 assertions against a single file with no dependencies and still score complexity 8–10 — thoroughness doesn't require sprawl.

**New tests must reach quality ≥9 AND complexity score ≥7** (raw sum ≤3): write as many assertions and test functions as the artifact genuinely needs, but keep the test structurally simple — one concept, one file, minimal dependencies and fixtures. If hitting quality ≥9 seems to require raw complexity above 3, that's a signal to split the test, not to let complexity slide.

**Don't pad complexity to hit a number.** A single-file content-regression check (see `_concurrent_sessions.md`'s test) is *supposed* to be simple — its natural complexity score is already 8–10. Inflating its scope or dependencies just to move the number is the exact anti-pattern this scoring exists to catch.

---

## 🔗 Related

- Parent: `_test_metadata.md` — the quality-score rubric this complements
- `_complexity_scoring.md` (in `03_authoring_guidelines/`) — the shared formula this file applies
