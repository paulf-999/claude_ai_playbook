# Quality Scorecard — git_create_pr

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-29

**Overall score:** 6.0/10

**Recommended improvements:**
- Add a runner or pytest that runs `tests/evals.yaml`, or score the skill as unrun until one exists.
- Add adversarial and secret-leak evals (a custom title containing `$(...)` or quotes, and an untracked `.env` in the changed files) to reach strategic coverage.
- Add an eval for the "complex merge conflict" not_for case.
- Validate or shell-escape a user-typed custom PR title before it goes into `--title "<pr title>"`, and check it against the 70-character, no-filename title rules.
- Replace the default "All changed/untracked files unless context suggests otherwise" with an explicit list of files the user confirms, and flag likely secret files.
- Replace the literal `~/.claude/_rules_lazy_load/org.md` in `_phase1_gather.md` with a path that doesn't hardcode the config directory.
- Fix `tests/README.md`, which calls 12 scenarios "the 8–12 expected for a **tactical** skill" while SKILL.md and the contract say `strategic`, or move the skill back to tactical.
- Cut the raw complexity (currently 8, the strategic ceiling), for example by moving label mapping into its own reference file or making it optional.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-29 | The phase map is clear, with a separate title confirm (2a) and plan confirm (2b), and the detail lives in `reference/`. Phase 1 does two jobs, gathering state and deriving six outputs. Its staging default, "All changed/untracked files unless context suggests otherwise", is vague. `SKILL.md` also adds a `## ⚠️ Known gaps` section that the template doesn't have. |
| **Complexity** | 2/10 | 2026-10-29 | Raw complexity is 8: Concepts 3 (gather, branch/commit/title derivation, subagent body, label mapping plus existence check, two confirms, execution, error recovery), Scope 2 (stages across any folder, plus `.github/`), Dependencies 2 (`git`, `gh`) and Prerequisites 1 (gh auth, PR template, origin remote). That is exactly the strategic cap of ≤8, so it has no headroom. |
| **Test Coverage** | 6/10 | 2026-10-27 | There are 12 evals, which meets the strategic count, but nothing runs them. SKILL.md says "nothing runs `tests/evals.yaml` yet", so the unrun-evals cap of 7 applies. The score drops below 7 because strategic coverage needs adversarial inputs, and SKILL.md admits "it has no adversarial or secret-leak cases". The "complex merge conflict scenarios" not_for case also has no eval. Only `non-main branch PRs` is covered, by eval 4. |
| **Code Quality** | 7/10 | 2026-10-27 | The execution rules are sound: verify each step, stop on failure, heredoc commit, `--body-file`, no `--no-verify`. The error-recovery table is good too. However, a custom title ("Anything else: treat the reply as the custom title") gets none of the title-format checks. The "`gh` not logged in" row also overlaps with the pre-check that already stops on `gh auth status`. |
| **Security** | 7/10 | 2026-10-27 | There are two confirm steps, and the contract sets `confirmation_required: true`. Force-push and `--no-verify` are forbidden. Untrusted input is not handled as data, though. A user-typed title goes inside a double-quoted `--title "<pr title>"` with no escaping, and the default stages all untracked files with no check for secrets. This matches the ~7 anchor. |
| **Documentation** | 7/10 | 2026-10-27 | SKILL.md has a clear purpose and a realistic example, and its known gaps come with workarounds. `tests/README.md` contradicts the maturity ("tactical skill" vs `maturity: strategic`). The Purpose says "minimal user intervention" even though the flow has two mandatory confirmations. The contract `summary` says "from staged changes", but the skill stages changed and untracked files itself. |
| **Standards Compliance** | 6/10 | 2026-10-27 | These gates are met: naming, contract fields and version match (2.0.0), frontmatter, metadata header, Instructions section, length ≤60, emoji headings, `tests/` layout, README and `_implementation.md`. These gates are missed: (1) coverage doesn't match strategic, with no adversarial or security evals; (2) no hardcoded paths, since `_phase1_gather.md` line 41 names `~/.claude/_rules_lazy_load/org.md`; (3) user input validated before a shell command, which the custom title isn't. The strategic claim of "core, frequently used" also has no recorded usage evidence. |
| **Overall** | **6.0/10** | 2026-10-29 | The workflow is well structured and safely gated, but it is held back by unrun evals with no adversarial cases, unescaped user input in the shell command, a hardcoded config path, and complexity at the strategic ceiling. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_create_pr/tests/evals.yaml` — Test Coverage dimension
