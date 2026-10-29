# Quality Scorecard — claude_setup_graphify

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-29

**Overall score:** 6.4/10

**Recommended improvements:**
- Define `--dry-run`, `--skip-extract` and `--state` in SKILL.md or `_implementation.md`, or delete them and the FAQ answer about `--state`.
- Point the writable fix in the troubleshooting quick links and the `validate_writable_directory` eval at the repo root (`[ -w . ]`), not `graphify-out/`.
- Say what Phase 4 does when CLAUDE.md doesn't exist, since the contract lists `Edit` but not `Write`.
- Either build the controls `_security.md` lists (umask, `chmod 600`, backup and rollback, checksums, ownership check) into the phases, or mark them as advice.
- Delete the claim that concurrent runs are safe, or back it, because grep-then-append isn't atomic.
- Install with `python3 -m pip` so the package goes to the same interpreter the pre-check tested.
- Add a runner for `tests/evals.yaml` (#463), plus evals for the flags and for a missing CLAUDE.md.
- Back the `strategic` maturity with recorded usage, or lower it to `tactical`.
- Swap the hardcoded `~/.claude/skills/graphify/` in `_troubleshooting.md` for a path built from the config directory.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | The phases are clear and linear, with must-follow steps in SKILL.md and the detail in `reference/`. Two gaps: `_implementation.md` L38 has "Utility flags (see SKILL.md for details)" but SKILL.md never defines them, and Phase 4 (L26) doesn't say what happens when there's no CLAUDE.md. |
| **Complexity** | 5/10 | 2026-10-29 | Raw sum 5: Concepts 2 (validate, install, extract with consent, edit repo files, verify), Scope 1 (repo root), Dependencies 1 (graphifyy), Prerequisites 1 (Python, pip, network, git). This is within the strategic limit of 8 and matches the ~5 anchor. |
| **Test Coverage** | 6/10 | 2026-10-27 | There are 17 prose evals, including adversarial cases and a not_for case. Nothing runs them (SKILL.md L60), so the cap of 7 applies. Below the cap: `validate_writable_directory` sets up "graphify-out/ writable, then read-only" (evals L23), but the pre-check tests the repo root. No eval covers the three flags or a missing CLAUDE.md, and `add_gitignore_entry` and `update_claude_md` each expect one thin result. |
| **Code Quality** | 6/10 | 2026-10-27 | The Phase 3 and 4 appends are idempotent and the symlink and root checks are quoted. But the pre-check runs `python3` while Phase 1 runs bare `pip`, which can install to a different interpreter. The FAQ says "safe for concurrent runs. Duplicate detection prevents corruption" (L66), but grep-then-append can race. The writable quick link says "Check: `ls -ld graphify-out/`" (L71), which contradicts the `[ -w . ]` check (L11). |
| **Security** | 7/10 | 2026-10-29 | Strong core: the version is pinned, there is an Always/On-a-no data-sharing confirm step, root is refused, symlinked targets are refused and writes are bounded by `git rev-parse --show-toplevel`. However, `_security.md` lists controls that no phase carries out: `umask 0077`, `chmod 600 graph.json` (L20–21), pre-backup and atomic rollback (L33–34), md5sum checksums (L47), `.git` ownership (L29). It also never says to treat repo content passed to the LLM pass as data rather than instructions. |
| **Documentation** | 7/10 | 2026-10-27 | SKILL.md, the example, Known gaps, troubleshooting and FAQ are all present and readable. Inaccurate in places: the FAQ says "`/claude_setup_graphify --state` shows completion for all 5 phases" (L57) with nothing behind it, and the "see SKILL.md for details" pointer goes nowhere. `_implementation.md` L19 asks for a yes only "before extracting a work repo", while SKILL.md L20 says always. |
| **Standards Compliance** | 7/10 | 2026-10-29 | Naming, the six-section structure, the version match (2.1.0), `tests/README.md` and the eval count all pass. Gaps: `_troubleshooting.md` L59 hardcodes `~/.claude/skills/graphify/` (portable paths), and the contract puts tools under `dependencies.tools` instead of `requires.tools`. `maturity: strategic` needs "20+/month or always-on" in `_core_standards.md`, but the skill is `criticality: could`, a "one-time setup per repo" (SKILL.md L52), and no file records its use. |
| **Overall** | **6.4/10** | 2026-10-29 | A well-shaped setup skill with real safeguards, held back by unrun evals, flags and security controls that are claimed but never defined, and a strategic maturity that no recorded use supports. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_setup_graphify/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_setup_graphify/tests/evals.yaml` — Test Coverage dimension
