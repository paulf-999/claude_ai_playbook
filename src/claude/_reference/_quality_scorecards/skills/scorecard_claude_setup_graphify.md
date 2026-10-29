# Quality Scorecard — claude_setup_graphify

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-29

**Overall score:** 6.1/10

**Recommended improvements:**
- Fix the writable pre-check so it works on a fresh repo: `touch graphify-out/.test` fails until `graphify-out/` exists.
- Check `.gitignore` for an existing `graphify-out/` entry before appending, instead of only checking after the append.
- Make the re-run guidance agree in one place, either duplicate detection or "remove the old section first".
- Build out `--dry-run`, `--skip-extract` and `--state`, or remove them.
- Set `confirmation_required: true` in the contract so it matches SKILL.md's "wait for a yes".
- Add adversarial evals for path traversal, a symlinked `.gitignore`, running as root, the user declining the data prompt, and running twice.
- Set `tested` / `test_coverage_level` to match what actually runs until #463 adds an eval runner.
- Treat repo docs, and the graph built from them, as untrusted data, and either wire the `_security.md` safeguards into the phases or cut them.
- Replace the hardcoded `~/.claude/skills/graphify/` path, and the GNU-only `stat -c`, with portable forms.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | Five clear phases, with detail in `reference/`. Two problems: `_implementation.md` L34 points flags to "see SKILL.md for details", but SKILL.md has none. Phase 4 (L22) says only "Add Graphify section to CLAUDE.md" and never says what goes in it or how duplicates are handled. |
| **Complexity** | 4/10 | 2026-10-29 | Raw 6: Concepts 2 (pre-flight, install, extract, file config, verify), Scope 2 (repo root plus the `/graphify` skill that `graphify install --platform claude` installs), Dependencies 1 (graphifyy, with its LLM backends optional), Prerequisites 1 (Python, pip, git). This is within the Strategic limit of 8 but sits below the raw-5 anchor. |
| **Test Coverage** | 6/10 | 2026-10-27 | 12 prose evals, the bare Strategic count, plus one not_for case. Nothing runs them (SKILL.md L59, #463), so the cap is 7. Strategic also needs adversarial inputs and there are none: no traversal, symlink, root, declined-prompt or re-run eval. `add_gitignore_entry` expects only `[.gitignore updated]`, with no duplicate check. |
| **Code Quality** | 6/10 | 2026-10-27 | `_implementation.md` L8's writable check `touch graphify-out/.test` fails before the folder exists. L19 appends to `.gitignore` before the duplicate check on L20. `_security.md` L51 uses `stat -c '%A'`, which fails on macOS. The Python check `grep -E "3\.[89]\|3\.1[0-9]"` misses 3.20 and later. Every phase does have a verify step and a recovery hint. |
| **Security** | 6/10 | 2026-10-29 | Good: there is a confirm step before data leaves the machine (SKILL.md L20), plus the pinned install, the no-root rule and repo-root confinement. Weak: the contract has `confirmation_required: false` (L24), which contradicts that confirm step. Repo docs that get an LLM pass, and the graph built from them, are never treated as untrusted data. `_security.md`'s backups, checksums, umask and symlink checks are not wired into any phase. |
| **Documentation** | 7/10 | 2026-10-27 | Troubleshooting, FAQ, examples and known gaps are all there. But FAQ L53 documents `--state`, which nothing implements. FAQ L62 ("Duplicate detection prevents corruption") and `_troubleshooting.md` L75 contradict `_troubleshooting.md` L47 ("Remove old section before re-running"). The "50–90%" savings figure (L50) has no source. |
| **Standards Compliance** | 7/10 | 2026-10-29 | Naming, contract fields, not_for, `tests/README.md`, emoji headings and the maturity line all pass. Gates missed: hardcoded `~/.claude/skills/graphify/` (`_troubleshooting.md` L59, which `portable_paths.md` forbids). Strategic eval coverage has no adversarial cases. Frontmatter `tested: true` / `comprehensive` (L8–9) overstates evals that nothing runs. The body is about 62 lines outside Instructions, against a limit of 60. |
| **Overall** | **6.1/10** | 2026-10-29 | The phased setup and data-sharing prompt are sound, but the pre-check bug, contradictory re-run guidance, unbuilt flags and unrun, non-adversarial evals fall short of the claimed strategic maturity. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_setup_graphify/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_setup_graphify/tests/evals.yaml` — Test Coverage dimension
