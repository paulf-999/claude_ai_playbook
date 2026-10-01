# 🧪 Test Scorecards

**Purpose:** Apply the rule-scorecard discipline to the pytest files in `_tests/` — one scorecard per test file, scored on the same seven-dimension shape rules use, adapted to what makes a test good.

---

## 📁 Location convention

One file per test, mirroring its path under `_tests/`: `_admin/_quality_scorecards/tests/<subpath>/scorecard_<test_file_stem>.md`.

- **Example:** `_tests/rules/02_claude_standards/test_git.py` → `_admin/_quality_scorecards/tests/rules/02_claude_standards/scorecard_test_git.md`
- **Keep the `test_` prefix:** it stops a test scorecard being mistaken for the scorecard of the rule it covers.
- **Never `@import` these files:** they're review records, not content Claude reads while working.
- **Header scores still apply:** every test keeps the quality and complexity scores in its metadata header (see `_rules/02_claude_standards/testing/_test_metadata.md`) — the scorecard explains and extends them, it doesn't replace them.

---

## 📋 Template

This is the test-specific version of the shared `_templates/scorecard.md.template`, with the test dimensions filled in.

```markdown
# Quality Scorecard — <test_file_stem>.py

**Date Created:** YYYY-MM-DD
**Date Updated:** YYYY-MM-DD

**Overall score:** X.X/10

**Recommended improvements:** [omit this line and the bullets below entirely when Overall ≥ 8.5]
- <one imperative action per distinct gap found in the Notes column below>

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | X/10 | YYYY-MM-DD | • 🔍 **<keyword>:** <one point> |
| **Complexity** | X/10 | YYYY-MM-DD | • 🧮 **Raw complexity N:** Concepts+Scope+Dependencies+Prerequisites |
| **Evidence of Need** | X/10 | YYYY-MM-DD | • 🔗 **<keyword>:** <one point> |
| **Coverage** | X/10 | YYYY-MM-DD | • 📊 **<keyword>:** N test functions, N assertions |
| **Structural Compliance** | X/10 | YYYY-MM-DD | • ✅ **<keyword>:** <one point> |
| **Currency** | X/10 | YYYY-MM-DD | • 🔍 **<keyword>:** <one point> |
| **Regression Value** | X/10 | YYYY-MM-DD | • 🛡️ **<keyword>:** <one point> |
| **Overall** | **X.X/10** | YYYY-MM-DD | • 💪 **<keyword>:** [strength]<br>• ⚠️ **<keyword>:** [gap, if any] |

## 🔗 Related files

- `src/claude/_tests/<subpath>/<test_file_stem>.py` — the test being scored
- `<full/repo-relative/path>` — what the test guards, and anything else named in the Notes above
```

- **Notes column:** one point per bullet, joined with `<br>`, each `• <emoji> **<keyword>:** <point>` — same as rule scorecards.
- **Related files:** full repo-relative paths, never bare filenames.
- **Dates:** `Date Created` is frozen once set; `Date Updated` bumps whenever the test is re-scored.
- **Row dates:** a row's `Date Updated` changes only when that row's score changes, and the header `Date Updated` must be on or after the latest row date.

---

## 🎯 Per-dimension criteria

| Dimension | 10 looks like | 1 looks like |
|---|---|---|
| **Clarity** | Module docstring states the goal in one sentence, function names say what they check, assertion messages say how to fix a failure | No goal statement, vague names, bare `assert` with no message |
| **Complexity** | Inverted shared formula (`03_authoring_guidelines/shared_standards/_complexity_scoring.md`): one concept, one file, no dependencies or fixtures | Whole-repo scan, 6+ concepts, several dependencies and complex fixtures |
| **Evidence of Need** | Guards a real rule, hook or skill, or a documented incident | Checks something nothing depends on, or a hypothetical |
| **Coverage** | 10+ test functions and 15+ assertions, including edge cases (the `_test_metadata.md` quality table) | Fewer than 4 functions or 5 assertions |
| **Structural Compliance** | Full metadata header, `Python style compliant: Yes` and true, correct location and name per `_testing_file_organization.md` | Missing or wrong header, style violations, misplaced file |
| **Currency** | Every path and name it checks still exists, header dates and version match the last change | Checks renamed or removed things, stale header |
| **Regression Value** | Would fail if the guarded behaviour broke, and proves its detector works on a synthetic bad case | Would still pass if the guarded thing were deleted or broken |

**Overall:** the average of the seven dimensions, rounded to one decimal place.

---

## 📅 When to score

- **On creation:** every new test gets a scorecard alongside it.
- **On re-score:** when a test's coverage or scope changes, update its scorecard and its header scores together.
- **Summary:** update the test's row in `test_scorecards_summary.md` in the same commit.
