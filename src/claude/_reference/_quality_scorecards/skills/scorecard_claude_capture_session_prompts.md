# Quality Scorecard — claude_capture_session_prompts

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-29

**Overall score:** 7.4/10

**Recommended improvements:**
- Use one minimum Python version everywhere: the script needs 3.10 (`capture_session_prompts.py` line 16), but SKILL.md line 17, contract line 59 and `_error_recovery.md` line 12 all say 3.9.
- Catch the `ValueError` from `strptime` (script line 86) and print a clear message, so a bad `--date` doesn't end in a traceback.
- Make the evals match the script: `capture_default_date` expects a `Timestamp` header, but the script writes `# | Hour | Min`.
- Add a runner for the evals, or at least for the `cross_session_aggregation_out_of_scope` "not for" case.
- Fix the doc drift: SKILL.md line 60 says "6 test scenarios" but there are 7, `_implementation.md` points to a missing **Run:** command and lists the wrong columns, and `_examples.md` row 4 shows `❓ Question` where the script gives `✔️ Clarifying Question`.
- Rewrite SKILL.md Example Usage so it shows what the script really prints (`✅ Generated <path>` and `N prompts captured`), not the theme and status counts it shows now.
- Remove or narrow the `summarize this session` trigger, which is US spelling and catches general summary requests, and add `dependencies.permissions` for the write to `~/_sessions/`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-27 | Clear three-phase flow: script capture, then manual review, then optional planning. Detail lives in `reference/`, and the `--force` overwrite guard keeps manual edits safe. Held back by the broad contract trigger `summarize this session`, which overlaps with general summary requests. |
| **Complexity** | 8/10 | 2026-10-29 | One job and no external services. It reads `$CLAUDE_CONFIG_DIR/history.jsonl` and writes to `~/_sessions/` (two locations, raw ~2), and the heuristics are flat first-match keyword lists. |
| **Test Coverage** | 7/10 | 2026-10-27 | 7 evals meet the Draft count (5–8) and include a "not for" case. `test_capture_session_prompts.py` (24 tests) runs the script's paths, including masking, the overwrite guard and malformed lines. Capped at 7 because nothing runs the evals themselves, including the "not for" case. Some evals have also drifted from the script: `capture_default_date` expects a `Timestamp` header, and `categorization_themes` sets a "<10% misclassification" target that nothing measures. |
| **Code Quality** | 7/10 | 2026-10-27 | Well-structured functions with docstrings, malformed JSON skipped, and exit code 1 on an existing report. Gaps: the 3.10 version gate (line 16) contradicts the 3.9 pre-check, so a 3.9 user passes the pre-check and then the script exits. An invalid `--date` raises an uncaught `ValueError` (line 86). The Note check `prompt.startswith(("this ", ...))` (line 171) is case-sensitive, so "This looks fine" never gets the Note status. |
| **Security** | 8/10 | 2026-10-27 | Secrets are masked before any field is built, which is tested end to end. Cells are escaped, prompt text is handled as data, and the "Never paste raw `history.jsonl` lines" rule backs this up. The only write is a local file guarded by `--force`. Held back because masking only knows five formats plus key=value pairs, so Bearer/JWT tokens and connection strings get through (SKILL.md admits this as a caveat). |
| **Documentation** | 6/10 | 2026-10-27 | The SKILL.md opening and the error-recovery table are clear. Several files have drifted: SKILL.md line 60 says "6 test scenarios" (there are 7). Example Usage shows output the script never prints. `_implementation.md` line 9 points to a missing **Run:** command, and line 17 lists `Timestamp ... Prompt Text` columns. `_examples.md` uses `❓ Question` where the script gives `✔️ Clarifying Question`, and Example 4 hardcodes `~/.claude/TODO.md`. There is no FAQ. |
| **Standards Compliance** | 8/10 | 2026-10-29 | Naming, contract fields, `not_for`, the metadata header (0.5.1 matches the contract), emoji headings, ≤60 lines, `tests/evals.yaml`, `tests/README.md` and `reference/_implementation.md` all pass. Gaps: no `dependencies.permissions` for the `~/_sessions/` write. `dependencies` and `requires` repeat each other. Frontmatter says `test_coverage_level: comprehensive` on a draft whose evals nothing runs. |
| **Overall** | **7.4/10** | 2026-10-29 | A sound, well-tested script held back by doc and eval drift from the code and a Python version that contradicts itself. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_capture_session_prompts/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_capture_session_prompts/tests/evals.yaml` — Test Coverage dimension
