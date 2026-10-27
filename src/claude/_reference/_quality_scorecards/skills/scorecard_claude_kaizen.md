# Quality Scorecard — claude_kaizen

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-27

**Overall score:** 6.4/10

**Recommended improvements:**
- Bring raw complexity down to the draft limit of 4, for example by moving pruning or the eval runner into a separate artefact, or justify a higher maturity
- Make phase 2 match the approval rule: ask before writing `_rules_lazy_load/_learned/candidates.md`, or say plainly the ledger is exempt
- Say when the drafted eval case is written to `evals/claude_ai_playbook.yaml`, and how to "apply the draft to a copy of the config"
- Tell Claude to treat `~/_errors/` log content as data, never as instructions, before it becomes a rule
- Fix the doc drift: `tests/README.md` calls the runner a placeholder, the contract says Python 3.6+ against the runner's 3.10, lists unused `Agent` and `pytest`, and promises a session-start trigger that doesn't exist
- Move the `evals/` folder to a place the skill layout allows, or document it as an exception
- Add troubleshooting for "Not logged in" and Keychain logins
- Make the scope and `not_for` evals runnable, so Test Coverage can rise above the cap of 7

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | • 📐 **Sound:** 6 clear phases in `reference/_implementation.md`, and SKILL.md stays lean<br>• ⚠️ **Contradiction:** phase 2 writes `candidates.md` before approval, but SKILL.md says to wait for a yes before writing to `_learned/`<br>• 🌫️ **Gaps:** nothing says when the eval case is written, or how to apply the draft to a config copy |
| **Complexity** | 4/10 | 2026-10-27 | • 🧮 **Raw complexity 6:** Concepts 2, Scope 2, Dependencies 1 (the `claude` CLI), Prerequisites 1 (error logs and a working login)<br>• ⚠️ **Over the limit:** 6 is above the draft limit of 4 |
| **Test Coverage** | 7/10 | 2026-10-27 | • 📊 **Right count:** 7 evals, inside draft's 5–8, including the cross-repo `not_for` case<br>• 🧪 **Runner tested:** `test_claude_kaizen_runner.py` is thorough, but it tests `runner.py`, not the skill's behaviour<br>• 🔒 **Cap:** `tests/evals.yaml` is prose nothing runs<br>• 🕳️ **Gaps:** no eval for bulk removal, auto-apply requests or adversarial log content |
| **Code Quality** | 8/10 | 2026-10-27 | • ✅ **Solid runner:** specific exceptions, a timeout, clear failure reasons, and no call spent on cases with no patterns<br>• ⚠️ **Edge case:** `parse_args` turns an empty `--config-dir` into `Path("")` without a warning<br>• ⚠️ **Style:** docstrings carry `:type:`/`:rtype:`, which the Python guide drops |
| **Security** | 7/10 | 2026-10-27 | • 🔒 **Confirmed:** diff-only output, and nothing is written until an explicit yes<br>• 🛡️ **Safe runner:** `--tools ""`, a throwaway folder, a 0o700 isolated config and symlinked credentials<br>• ⚠️ **Untrusted input:** `~/_errors/` content becomes rule text with no data-not-instructions rule, so only human review of the diff stands in the way |
| **Documentation** | 6/10 | 2026-10-27 | • ✅ **Clear page:** purpose, a worked example and "When NOT to use"<br>• 🍂 **Stale:** `tests/README.md` says the runner is a placeholder that marks every case passed<br>• ⚠️ **Drift:** Python 3.6+ against 3.10, and unused `Agent` and `pytest` in the contract<br>• ⚠️ **Promises:** "Run at session start" and cross-repo learning are both v2 in `_roadmap.md`<br>• ❓ **No troubleshooting:** nothing covers login or Keychain failures |
| **Standards Compliance** | 6/10 | 2026-10-27 | • ✅ **Met:** naming, a 0.6.2 header matching the contract, `tests/` files, `_implementation.md` and length<br>• ❌ **Gate 8:** raw complexity 6 is above the draft limit<br>• ❌ **Layout:** an extra `evals/` folder at the skill root<br>• ⚠️ **Gate 3:** the description lacks the contract's trigger phrases, and paths aren't `$HOME`-based |
| **Overall** | **6.4/10** | 2026-10-27 | A well-built, well-tested eval runner sits inside a skill that is too complex for draft, has drifted docs, and doesn't treat log input as untrusted. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_kaizen/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_kaizen/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored blind by `quality_scorecard_reviewer`
