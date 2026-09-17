# 📊 Test Metadata Standard

**Purpose:** Track test quality, creation date, and maintenance status via structured metadata headers. Enable quick assessment of test staleness and coverage before running or updating.

---

## 📋 Contents

- [Format](#-format)
- [Quality Scoring](#-quality-scoring-1-10)
- [Maintenance Gates](#-maintenance-gates)
- [Quarterly Audit Cadence](#-quarterly-audit-cadence)
- [Maintenance Protocol](#-maintenance-protocol)

---

## 📝 Format

Every test file in `~/.claude/_tests/` must open with this metadata header:

```python
# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: X/10
# Date created:      YYYY-MM-DD
# Version:           1.0.0
# Date updated:      [placeholder] or YYYY-MM-DD
# ─────────────────────────────────────────────────────────
```

**Placement:** Line 1–6, before any docstring or code.

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

## ⚙️ Maintenance Gates

### When to update metadata

- **File is modified:** Update `Date updated:` to today's date
- **Test is refactored:** Re-score if coverage improves (e.g., 5/10 → 7/10)
- **Feature deprecated:** Mark quality as 1–2, document reason in comment
- **Quarterly audit:** Review all tests ≤5/10 for relevance and staleness

### Never skip metadata

- ❌ Don't remove or reuse metadata from another test
- ❌ Don't update `Date created:` (frozen once created)
- ❌ Don't leave `Date updated: [placeholder]` if you've modified the file

---

## 📅 Quarterly Audit Cadence

Every 3 months, audit all tests in `~/.claude/_tests/`:

1. **Identify:** Find all files with quality score ≤5
2. **Assess:** Do they test active features? Any stale references?
3. **Update:** Re-score if coverage improved; mark deprecated tests 1–2
4. **Archive:** Move deprecated tests to `~/.claude/_tests/_archived/` with `# Archived: [reason] [date]` comment
5. **Verify:** Run full test suite `pytest ~/.claude/_tests/` — confirm no regressions

---

## 📖 Maintenance Protocol

### Example: Updating a Test

```python
# Before (unchanged)
# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 5/10
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

# After (refactored; +3 assertions, +2 test funcs)
# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 7/10
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      2026-09-20
# ─────────────────────────────────────────────────────────
```

### Metadata Fields Explained

- **Test quality score:** 1–10 rating (frozen until audit or refactor)
- **Date created:** When test was first written (never update)
- **Version:** Semver for test contract; increment on breaking changes
- **Date updated:** When test was last modified; update on any change

### Archival Workflow

When deprecating a test:

1. Move file to `~/.claude/_tests/_archived/`
2. Update metadata: `# Test quality score: 0/10`
3. Add comment: `# Archived: [feature_removed] [date]`
4. Update playbook repo if test is tracked there
5. Remove from any CI/CD that runs the test

---

## 🔗 Related Rules

- `testing.md` — When tests are required; test design pattern and gates
- `behaviour.md` → `_multi_phase_implementation_gates.md` — Gate testing before merging
- `~/.claude/_tests/` — Location of all test files and metadata headers
