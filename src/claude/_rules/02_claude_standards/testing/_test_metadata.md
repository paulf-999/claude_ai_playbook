<!-- version: 2.0.0 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-01 -->
# 📊 Test Metadata Standard

**Purpose:** Track test quality, creation date, and maintenance status via structured metadata headers. Enable quick assessment of test staleness and coverage before running or updating.

---

## 📋 Contents

- [Format](#-format)
- [Quality Scoring](#-quality-scoring-1-10)
- [New Tests Must Score ≥9/10](#-new-tests-must-score-910)
- [Complexity Scoring](#-complexity-scoring) — reward simplicity; quality and complexity are independent floors, not a cap (see `_test_metadata_complexity_scoring.md`)
- [Maintenance](#-maintenance) — when to update the header

---

## 📝 Format

Every test file in `~/.claude/_tests/` must open with this metadata header:

```python
# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      YYYY-MM-DD
# Date updated:      YYYY-MM-DD
# Version:           X.Y.Z
# Test quality score: X/10
# Test complexity score: Y/10
# Python style compliant: Yes/No
# ─────────────────────────────────────────────────────────
```

**Placement:** Lines 1–9, before any docstring or code.

**Order:** the six fields appear in exactly this order — dates, then version, then scores — and `test_test_metadata.py` enforces it.

**Every field is mandatory:** a new file sets `Date updated:` to the same day as `Date created:`, never `[placeholder]`.

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

**Style counts too:** a new test must also set `Python style compliant: Yes`.

**Enforced:** `test_test_score_floor.py` fails any test file below quality 9, complexity 7 or style Yes.
- **No exemptions:** every test met the minimum on 2026-10-01, so the old exemption list is gone and the rule applies to every test.
- **Can't meet it?** split the test by concept rather than padding it — see `_test_metadata_complexity_scoring.md`.

---

## 🧮 Complexity Scoring

@~/.claude/_rules/02_claude_standards/testing/_test_metadata_complexity_scoring.md

---

## ⚙️ Maintenance

- **File modified:** set `Date updated:` to today.
- **Test refactored:** re-score quality and complexity if coverage changed.
- **Feature deprecated:** mark quality 1–2 and note the reason in a comment.
- **Never:** change `Date created:`, copy another test's header, or leave `Date updated: [placeholder]` on a modified file.
- **Read on demand:** `~/.claude/_rules/05_lazy_load/testing_guidance.md` — quarterly audit, archival workflow and a worked example.
