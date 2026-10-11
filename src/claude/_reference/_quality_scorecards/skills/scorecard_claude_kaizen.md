# Quality Scorecard — claude_kaizen

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-06

**Overall score:** 7.9/10

**Recommended improvements:**
- Record one real promotion end to end, since the evals cover the runner but not a full skill run.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-02 | Clear loop (audit → promote → validate → propose) with diff-only output and explicit `not_for` limits; the "promote with proof" step now runs real evals against the rules under test. |
| **Complexity** | 5/10 | 2026-09-29 | Several moving parts: error-log audit, candidate counting, rule and eval drafting, before/after runs and staleness checks, plus a Python runner and a dataset. |
| **Test Coverage** | 8/10 | 2026-10-06 | 7 `evals.yaml` scenarios (draft: 5–8) plus 20 runner tests, and on 2026-10-06 the real runner passed both seed cases and caught a deliberate regression (pass before, fail after). |
| **Code Quality** | 9/10 | 2026-10-06 | `evals/runner.py` runs each prompt through `claude -p` with no tools in a private throwaway config that links the rules under test and the existing login, and reports Claude's stdout when stderr is empty. |
| **Security** | 8/10 | 2026-09-29 | Never auto-applies changes; every rule arrives as a diff for review; no secrets or external services involved. |
| **Documentation** | 8/10 | 2026-10-06 | `reference/_implementation.md` now covers all six phases, including the promotion threshold of 2 and the before/after runner commands; `SKILL.md` keeps a clear step-by-step example. |
| **Standards Compliance** | 9/10 | 2026-10-06 | Instructions for Claude before Purpose and off the baseline ✓, maturity justified in Best For ✓, complete contract ✓, `tests/evals.yaml` + `tests/README.md` ✓; 59 lines without the instructions. |
| **Overall** | **7.9/10** | 2026-10-06 | Well-bounded draft skill with safe diff-only output and a proven eval runner that catches regressions; held back mainly by its many moving parts. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_kaizen/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_kaizen/tests/evals.yaml` — Test Coverage dimension
