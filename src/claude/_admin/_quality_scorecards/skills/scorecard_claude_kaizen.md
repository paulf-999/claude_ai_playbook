# Quality Scorecard — claude_kaizen

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-02

**Overall score:** 7.1/10

**Recommended improvements:**
- Add a `reference/_implementation.md` covering the audit and promotion logic, including the promotion threshold.
- Confirm the `regression_blocks_promotion` eval now passes against the real runner.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-02 | Clear loop (audit → promote → validate → propose) with diff-only output and explicit `not_for` limits; the "promote with proof" step now runs real evals against the rules under test. |
| **Complexity** | 5/10 | 2026-09-29 | Several moving parts: error-log audit, candidate counting, rule and eval drafting, before/after runs and staleness checks, plus a Python runner and a dataset. |
| **Test Coverage** | 7/10 | 2026-10-02 | 7 `evals.yaml` scenarios (draft: 5–8) covering promotion, the one-off threshold, a declined diff, regressions, stale rules, a missing error log and out-of-scope requests, plus `test_claude_kaizen_runner.py` (14 cases) for the runner itself. |
| **Code Quality** | 8/10 | 2026-10-02 | `evals/runner.py` sends each prompt to `claude -p` with no tools in a throwaway folder, checks `must_match` / `must_not_match` regexes, and fails a case with a reason when the CLI is missing, times out or errors. |
| **Security** | 8/10 | 2026-09-29 | Never auto-applies changes; every rule arrives as a diff for review; no secrets or external services involved. |
| **Documentation** | 6/10 | 2026-09-29 | `SKILL.md` has a clear step-by-step example and scope limits; there is no reference doc for the audit or promotion logic, and the promotion threshold is only shown by example. |
| **Standards Compliance** | 8/10 | 2026-09-29 | `domain_action` naming ✓, 4 canonical `SKILL.md` sections ✓, complete `skill.contract.yaml` ✓, `tests/evals.yaml` + `tests/README.md` ✓, roadmap kept in `reference/` ✓; no `reference/_implementation.md`. |
| **Overall** | **7.1/10** | 2026-10-02 | Well-bounded draft skill with safe diff-only output and a real eval runner; held back by its many moving parts and the missing implementation reference. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_kaizen/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_kaizen/tests/evals.yaml` — Test Coverage dimension
