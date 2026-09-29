# Quality Scorecard — git_create_pr

**Date Created:** 2026-09-29
**Date Updated:** 2026-09-29

| Dimension | Score | Notes |
|---|---|---|
| **Design** | 8/10 | Single clear purpose with a 3-phase flow (gather → commit and push → confirm and create); `not_for` rules out merge conflicts and non-main target branches. |
| **Complexity** | 7/10 | Phase 1 carries most of the logic: branch, commit, title and body derivation plus a 15-rule label map; phases 2 and 3 are thin wrappers around `git` and `gh`. |
| **Test Coverage** | 7/10 | 11 `evals.yaml` scenarios (tactical: 8–12) covering the happy path, both stop conditions, name and title derivation, label mapping, both confirmation branches and the 20-file limit; no scenarios yet for push failures or `gh` authentication errors. |
| **Code Quality** | 6/10 | No code, only prompt instructions; phase 1 is fully specified in `reference/_phase1_gather.md`, but phases 2 and 3 are only described in `SKILL.md`, with no documented error handling for failed pushes. |
| **Security** | 8/10 | Relies on `gh` authentication rather than stored tokens; confirmation is required before the PR is created; stages all changed files by default, which could pick up unintended files. |
| **Documentation** | 6/10 | `SKILL.md` has a clear end-to-end example; phase 1 reference is thorough; there is no reference doc for phases 2 and 3 or for error recovery. |
| **Standards Compliance** | 8/10 | `domain_action` naming ✓, 4 canonical `SKILL.md` sections ✓, complete `skill.contract.yaml` ✓, `tests/evals.yaml` + `tests/README.md` ✓; `reference/_implementation.md` is missing, with phase 1 in `reference/_phase1_gather.md` instead. |
| **Overall** | **7.1/10** | Well-scoped, actively used skill with strong phase 1 guidance and now tactical-level eval coverage; phases 2–3 and error recovery are under-documented. |
