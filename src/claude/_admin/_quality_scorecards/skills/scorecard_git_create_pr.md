# Quality Scorecard — git_create_pr

**Date Created:** 2026-09-29
**Date Updated:** 2026-09-30

**Overall score:** 7.9/10

**Recommended improvements:**
- Add an eval scenario for a missing `gh` login.
- Merge the two phase files into one `reference/_implementation.md`, or note why they stay split.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-09-29 | Single clear purpose with a 2-phase flow (gather → confirm and execute); `not_for` rules out merge conflicts and non-main target branches. |
| **Complexity** | 7/10 | 2026-09-29 | Phase 1 carries most of the logic: branch, commit, title and body derivation plus a 15-rule label map checked against the repo's existing labels; phase 2 is two confirmations followed by a fixed command sequence. |
| **Test Coverage** | 8/10 | 2026-09-29 | 12 `evals.yaml` scenarios (tactical: 8–12) covering the happy path, both stop conditions, name and title derivation, label mapping including a missing label, both confirmation steps, a rejected push and the 20-file limit; no scenario yet for a missing `gh` login. |
| **Code Quality** | 7/10 | 2026-09-29 | No code, only prompt instructions; both phases are fully specified in `reference/`, with step-by-step verification and a stop-on-failure rule. |
| **Security** | 9/10 | 2026-09-29 | Nothing is committed, pushed or created until the user approves both the title and the full plan; relies on `gh` authentication rather than stored tokens; never force-pushes or skips hooks without being asked. |
| **Documentation** | 8/10 | 2026-09-29 | `SKILL.md` has a clear end-to-end example; `reference/_phase1_gather.md` and `reference/_phase2_execute.md` cover every step and the common failures. |
| **Standards Compliance** | 8/10 | 2026-09-29 | `domain_action` naming ✓, 4 canonical `SKILL.md` sections ✓, complete `skill.contract.yaml` ✓, `tests/evals.yaml` + `tests/README.md` ✓; implementation is split across two phase files rather than one `reference/_implementation.md`. |
| **Overall** | **7.9/10** | 2026-09-29 | Well-scoped, actively used skill with both phases documented, confirmation before any change, and tactical-level eval coverage. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_create_pr/tests/evals.yaml` — Test Coverage dimension
