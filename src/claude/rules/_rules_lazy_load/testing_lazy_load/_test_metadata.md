<!-- version: 2.0.6 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-11 -->
# 📊 Test Metadata Standard

**Purpose:** Track test quality, creation date, and maintenance status via structured metadata headers. Enable quick assessment of test staleness and coverage before running or updating.

---

## 📋 Contents

- [Format](#-format)
- [Quality Scoring](#-quality-scoring-1-10)
- [Minimum for New Tests](#-minimum-for-new-tests)
- [Complexity Scoring](#-complexity-scoring) — reward simplicity; quality and complexity are independent minimums (see `_test_metadata_complexity_scoring.md`)
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

**Python style compliant:** `Yes` only if the file follows every rule in `~/.claude/rules/02_claude_standards/path_scoped_rules/style_guide_standards/python.md` (f-strings only, reST docstrings, no bare `except`, `pathlib.Path` not `os.path`, etc.) — check before setting; don't assume.

---

## 🎯 Quality Scoring (1–10)

Quality is scored from what a file's tests catch and how clearly they report it, never from how many tests it has.

| Check | Points | What earns them |
|---|---|---|
| 💬 **Failure messages** | 0–4 | The share of `assert` statements that carry a message, times 4 |
| 📝 **Docstrings** | 0–3 | The share of test functions with a docstring, times 3 |
| 🔎 **Non-vacuous scan** | 2 | At least one assert proves a scan of the real config found something: `assert len(x) >= n`, `assert any(...)` or `assert found, "..."`; a file that scans nothing real earns these automatically |
| 🧪 **Proven to fail** | 1 | At least one test feeds bad input and is named for what it catches, e.g. `..._is_flagged` or `..._rejected` |

- **Score:** the rounded sum of the four checks, so a file of 3 clear tests can score 10.
- **Computed, not judged:** `test_test_quality_score.py` works the score out from the file and fails when the header disagrees.
- **Why:** counting tests rewarded padding, which helped the suite pass 1,000 tests by 2026-10-11.

---

## 🎯 Minimum for new tests

- **Minimums:** every test file must score quality ≥7/10 and complexity score ≥7/10, keeping to one concept with minimal dependencies and fixtures.
- **Style:** every test must also set `Python style compliant: Yes`.
- **Write only what's needed:** one test that proves a checker can fail is enough, so don't add near-identical cases to raise a score.
- **Enforced:** `test_test_score_floor.py` fails any test file below quality 7, complexity 7 or style Yes.
  - **Note:** `test_test_quality_score.py` checks that each quality score matches what its file earns.
- **Can't meet complexity?** split the test by concept rather than letting complexity slide — see `_test_metadata_complexity_scoring.md`.

---

## 🧮 Complexity Scoring

- **Read on demand:** [`~/.claude/_rules_lazy_load/testing_lazy_load/_test_metadata_complexity_scoring.md`](_test_metadata_complexity_scoring.md) — when scoring a test's complexity.

---

## ⚙️ Maintenance

- **File modified:** set `Date updated:` to today.
- **Test refactored:** re-score quality and complexity if coverage changed.
- **Feature deprecated:** mark quality 1–2 and note the reason in a comment.
- **Never:** change `Date created:`, copy another test's header, or leave `Date updated: [placeholder]` on a modified file.
- **Read on demand:** [`~/.claude/_rules_lazy_load/testing_lazy_load/_test_metadata_audit.md`](_test_metadata_audit.md) — quarterly audit, archival workflow and a worked example.
