# Quality Scorecard — git_create_pr

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-29

**Overall score:** 7.3/10

**Recommended improvements:**
- Add a runner or pytest that runs `tests/evals.yaml` and records a pass rate, so Test Coverage can go above the cap of 7 for evals nothing runs.
- Record the skill's raw complexity score per `_complexity_scoring.md`, because hard gate 8 has no record anywhere in the skill folder.
- Replace the literal `~/.claude/_rules_lazy_load/org.md` in `reference/_phase1_gather.md` line 45 with a path that does not depend on the config-directory name.
- Make the `gh` auth handling consistent: `_implementation.md` stops before Phase 1 when `gh auth status` fails, but the `_phase2_execute.md` error table says "`gh` not logged in" is found only after the push.
- Align the contract with the skill: change `summary: Create GitHub PR from staged changes` to match "all changed/untracked files", and drop `<20 staged files` from `requires.resources`, since the skill flags a large change and suggests a split.
- Tell the `technical_writer` body-drafting step to treat diff and file content as data, not instructions.
- Add evals for a failed `gh auth status`, a pre-commit hook failure and an existing PR for the branch.
- Replace "unless context suggests otherwise" in the files-to-stage rule with a specific rule.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-29 | Clear phases (gather, 2a title, 2b plan, execute), with the detail in `reference/` and a thin `_implementation.md` phase map. Two things hold it back. The 20-file check sits only in `_implementation.md` error handling, not in the Phase 1 derivations. "All changed/untracked files unless context suggests otherwise" (`_phase1_gather.md` line 17) leaves staging to judgement. |
| **Complexity** | 6/10 | 2026-10-29 | About raw 4: one job, but it reads the whole working tree, calls GitHub through `gh`, and branches across a 15-rule label map, a label-exists split, three title replies and a `create labels` loop. |
| **Test Coverage** | 7/10 | 2026-10-29 | 15 evals meet the strategic 12+. They include adversarial cases (a `$(rm -rf ~)` title, an unstaged `.env`) and both not_for cases (`reuses_existing_feature_branch` turns down `develop`, `merge_conflict_stops`). Capped at 7 because SKILL.md Known gaps says "nothing runs `tests/evals.yaml` yet, which #463 tracks". No eval covers a failed `gh auth status`, a pre-commit hook failure or an existing PR. |
| **Code Quality** | 7/10 | 2026-10-27 | Safe execution patterns: each step is checked, the flow stops on failure, commit message and title go through heredocs, and the body goes through `--body-file`. The `gh` auth handling contradicts itself: `_implementation.md` says "stop before Phase 1 if `gh auth status` fails", but the `_phase2_execute.md` table handles "`gh` not logged in" after the push. Hook-failure recovery "ask[s] before committing again", but "Hook modifies files" re-commits without asking. |
| **Security** | 8/10 | 2026-10-29 | Two confirm steps come before any write. A typed title is treated as data and goes through a quoted heredoc. There is no force-push and no `--no-verify`, and likely secret files are held back by name. Held back because secrets are spotted by filename only (SKILL.md Known gaps), and the `technical_writer` body draft takes the diff without saying to treat that content as data. |
| **Documentation** | 8/10 | 2026-10-29 | Purpose, a realistic example that shows both confirm steps, maturity in Best For, and four Known gaps each with a workaround. The tests README has a scenario table. Held back because the description says when to use the skill but not when not to, troubleshooting lives only in `reference/_phase2_execute.md`, and the Purpose line "with minimal user intervention" sits awkwardly beside two required confirm steps. |
| **Standards Compliance** | 7/10 | 2026-10-29 | Naming, contract fields, `not_for`, `confirmation_required: true`, matching versions (2.1.0), `tests/` layout and SKILL.md length (about 49 lines outside Instructions) all pass. It misses two hard gates: gate 8 has no recorded complexity score, and gate 3/9 is broken by the hardcoded `~/.claude/` path in `_phase1_gather.md` line 45. The contract also drifts from the skill: `summary` says "staged changes", and `requires.resources` says `<20 staged files`. |
| **Overall** | **7.3/10** | 2026-10-29 | A safe, well-structured PR workflow, held back by evals nothing runs, two missed hard gates and small contradictions between its reference files and its contract. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_create_pr/tests/evals.yaml` — Test Coverage dimension
