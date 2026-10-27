# Quality Scorecard — claude_capture_session_prompts

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-27

**Overall score:** 7.0/10

**Recommended improvements:**
- Make the column list in `evals.yaml` (`capture_default_date`), `reference/_implementation.md` and `reference/_examples.md` match the script's real columns
- Make the Python minimum the same everywhere, since the script needs 3.10 but SKILL.md, the contract and `_error_recovery.md` say 3.9
- Fix the `_implementation.md` pointer to a "**Run:** command in SKILL.md → Example Usage" that doesn't exist
- Add evals for the `not_for` cases and the secret-masking path, and give each eval a `run` block or a pytest case
- Stop the script silently overwriting an existing `~/_sessions/YYYY_MM_DD_claude_prompts.md`, which loses Phase 2 edits
- Catch a bad `--date` value with a clear message instead of a `ValueError` traceback
- Add `returns` to the contract's `output`, and put trigger phrases in the SKILL.md `description`
- Narrow the `summarize this session` trigger, and lower `test_coverage_level: comprehensive` to match 6 unrun evals

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-27 | • ✅ **Clear phases:** the script builds the table instead of Claude, and the detail lives in `reference/`<br>• 🕳️ **Gap:** `_implementation.md` Phase 1 points to a Run command in Example Usage that doesn't exist |
| **Complexity** | 6/10 | 2026-10-27 | • 🧮 **Raw complexity 4:** Concepts 2, Scope 1, Dependencies 1 (`history.jsonl` and Python), Prerequisites 0, at the draft limit of 4<br>• 🔀 **Branching:** `determine_status` is a 7-branch chain where order matters |
| **Test Coverage** | 7/10 | 2026-10-27 | • 📊 **Draft count:** 6 evals, and 22 pytest tests run the script, including masking and the end-to-end report<br>• 🕳️ **Gaps:** the evals are prose with no `run` block and no `not_for` case<br>• ⚠️ **Stale:** eval 1 expects a "Timestamp" header the script never writes |
| **Code Quality** | 7/10 | 2026-10-27 | • ✅ **Solid:** typed, documented, skips malformed JSON lines and escapes pipes<br>• ⚠️ **Gaps:** `write_text` overwrites an existing report, and an invalid `--date` ends in a traceback<br>• ⚠️ **Mismatch:** the 3.10 check contradicts the documented 3.9 |
| **Security** | 8/10 | 2026-10-27 | • 🛡️ **Masked:** secrets are masked in `build_row` before any field is built, with an end-to-end test<br>• ✅ **Local:** never pastes raw history lines, never edits `history.jsonl`, posts nothing externally<br>• ⚠️ **Limits:** masking knows fixed patterns only, and the overwrite needs no confirmation |
| **Documentation** | 6/10 | 2026-10-27 | • ✅ **Clear:** SKILL.md and the error-recovery table<br>• 🍂 **Stale:** `_examples.md` shows a Timestamp column, MoSCoW on Done rows and a "By MoSCoW" summary the script doesn't produce<br>• ⚠️ **Drift:** `_implementation.md` lists the wrong columns, and the Python version differs between files |
| **Standards Compliance** | 7/10 | 2026-10-27 | • ✅ **Met:** naming, `tests/` layout, a 0.4.1 header matching the contract, `not_for` and length<br>• ❌ **Missed:** no `returns` in the contract `output`, and few trigger phrases in the `description`<br>• ⚠️ **Overstated:** `test_coverage_level: comprehensive` for 6 unrun evals |
| **Overall** | **7.0/10** | 2026-10-27 | A sound, well-tested script that masks secrets, held back by reference docs and evals that no longer match its output, and by unrun evals with no `not_for` case. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_capture_session_prompts/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_capture_session_prompts/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored blind by `quality_scorecard_reviewer`
