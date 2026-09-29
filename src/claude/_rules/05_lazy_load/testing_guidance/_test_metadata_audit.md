<!-- version: 2.0.0 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-09-29 -->
# 📅 Test Metadata Audit

**Purpose:** The quarterly audit, worked update example and archival workflow that keep test metadata headers honest — the per-edit update rules stay always-on in `_test_metadata.md`.

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
# Test complexity score: 3/10
# Python style compliant: Yes
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

# After (refactored; +3 assertions, +2 test funcs)
# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 7/10
# Test complexity score: 4/10
# Python style compliant: Yes
# Date created:      2026-09-16
# Version:           1.0.0
# Date updated:      2026-09-20
# ─────────────────────────────────────────────────────────
```

### Metadata Fields Explained

- **Test quality score:** 1–10 rating (frozen until audit or refactor)
- **Test complexity score:** 0–10 rating per `_test_metadata_complexity_scoring.md` — caps the achievable quality score
- **Python style compliant:** Yes/No against `python.md` — re-check whenever the file is modified
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
