# 📊 Test Metadata Standard

**Purpose:** Track test quality, creation date, and maintenance status via structured metadata headers. Enable quick assessment of test staleness and coverage before running or updating.

---

## 📋 Contents

- [Format](#-format)
- [Quality Scoring](#-quality-scoring-1-10)
- [New Tests Must Score ≥9/10](#-new-tests-must-score-910)
- [Complexity Scoring](#-complexity-scoring) — reward simplicity; quality and complexity are independent floors, not a cap (see `_test_metadata_complexity_scoring.md`)
- [Maintenance](#-maintenance) — gates, quarterly audit, protocol (see `_test_metadata_maintenance.md`)

---

## 📝 Format

Every test file in `~/.claude/_tests/` must open with this metadata header:

```python
# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: X/10
# Test complexity score: Y/10
# Python style compliant: Yes/No
# Date created:      YYYY-MM-DD
# Version:           1.0.0
# Date updated:      [placeholder] or YYYY-MM-DD
# ─────────────────────────────────────────────────────────
```

**Placement:** Line 1–7, before any docstring or code.

**Python style compliant:** `Yes` only if the file follows every rule in `~/.claude/_rules/05_lazy_load/style_guide_standards/python.md` (f-strings only, reST docstrings, no bare `except`, `pathlib.Path` not `os.path`, etc.) — check before setting; don't assume.

---

## 🎯 Quality Scoring (1–10)

| Score | Meaning | Indicators |
|-------|---------|-----------|
| **9–10** | Excellent | 15+ assertions, 10+ test functions, comprehensive, <200 lines, maintained quarterly |
| **7–8** | Good | 10–14 assertions, 8+ test functions, main scenarios, maintainable complexity |
| **5–6** | Adequate | 5–9 assertions, 4–7 test functions, works, has coverage gaps, occasional maintenance |
| **3–4** | Poor | <5 assertions, <4 test functions, brittle, stale references, needs refactoring |
| **1–2** | Broken | Failing tests, removed feature references, unmaintained 3+ months, archive candidate |

**Scoring rule:** Count assertions and test functions as primary indicators. Adjust ±1 for clarity (docstring, maintainability), complexity (lines), or staleness (deprecated refs).

---

## 🎯 New tests must score ≥9/10

**Any test Claude writes from now on must be built to reach quality ≥9/10 AND complexity score ≥7/10** — not scored honestly after the fact at whatever level it lands. Design for 15+ assertions and 10+ test functions up front (quality), while keeping the test to one concept and one file with minimal dependencies/fixtures (complexity) — see `_test_metadata_complexity_scoring.md` for why these don't trade off against each other. A test that only reaches 5/10 or 6/10 quality wasn't finished; a test padded with unnecessary scope/dependencies just to look thorough missed the point.

**Existing tests keep their current score** — this floor applies going forward, not retroactively. A 6/10 test written before this rule existed isn't a violation; a new 6/10 test is.

---

## 🧮 Complexity Scoring

@~/.claude/_rules/02_claude_standards/testing/_test_metadata_complexity_scoring.md

---

## ⚙️ Maintenance

@~/.claude/_rules/02_claude_standards/testing/_test_metadata_maintenance.md

---

## 🔗 Related Rules

- Parent: `testing.md` — When tests are required; test design pattern and gates
- `claude_plans.md` — Gate testing before merging
- `~/.claude/_tests/` — Location of all test files and metadata headers
