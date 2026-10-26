# Quality Scorecard — quality_scorecard_reviewer

**Date Created:** 2026-10-22
**Date Updated:** 2026-10-26

**Overall score:** 7.9/10

**Recommended improvements:**
- Name in the description when not to use it (hooks, tests, PR diffs, whole-config audits)
- Name what owns the hook and test scorecard flow on line 31
- Add a run block to `scores_below_nine_quote_evidence`, which needs no full session
- Update the stale maturity evidence on lines 53–54 and `tested: false` now that 4 evals run

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-26 | • 🔍 **Description:** line 3 says what the agent does and when to use it, and lines 10–13 cover natural phrasings<br>• ⚠️ **No "when not":** the exclusions for hooks, tests, PR diffs and whole-config audits appear only in the body (lines 31–32) |
| **Scope Boundaries** | 8/10 | 2026-10-26 | • ✅ **Distinct job:** line 32 names `code_reviewer` and `claude_review_config` as neighbours<br>• ⚠️ **Unnamed owner:** line 31 excludes hooks and tests by pointing to "their own scorecard flow" without naming what owns it |
| **Complexity** | 7/10 | 2026-10-26 | • 🧮 **Raw complexity 3:** one scoring job (Concepts 1), reads the artefact, rubric and anchors across folders (Scope 2), no dependencies or prerequisites, matching the ~7 anchor |
| **Evidence of Need** | 7/10 | 2026-10-26 | • ✅ **Dated origin:** line 53 records "new on 2026-10-22 for issue #381"<br>• ⚠️ **No usage record:** the 2026-10-25/26 eval runs are tests, not real use |
| **Test Coverage** | 8/10 | 2026-10-26 | • 📊 **Runs:** 4 of 7 evals have run blocks, and the clean run on 2026-10-26 passed 4/4 after a first run of 1/4 that failed on faults in the evals<br>• ⚠️ **Not all skips need a session:** `scores_below_nine_quote_evidence` (evals.yaml lines 74–85) could run but has no run block, so the 90% guidance stops at 8<br>• ⚠️ **Prose-only "not for":** the `code_reviewer` hand-off is checked only in prose (line 35) |
| **Structural Compliance** | 8/10 | 2026-10-26 | • ✅ **Hard gates:** complete frontmatter, metadata header (lines 18–20), all 5 sections, 6 principles, 7 evals in the draft range, every eval field present<br>• ⚠️ **Stale maturity evidence:** line 53 says "no recorded runs yet", line 54 omits the 4 running evals, and frontmatter line 8 still says `tested: false`<br>• ⚠️ **Length:** 61 lines, just over the ~40–60 target |
| **Tool Safety** | 9/10 | 2026-10-26 | • 🔒 **Allowlist:** line 14 allows only `Read, Grep, Glob`, which fits a read-only job (line 47)<br>• ✅ **Isolation:** `none` (line 16) is fine because the agent writes no files |
| **Overall** | **7.9/10** | 2026-10-26 | • 💪 **Strength:** a tight read-only allowlist, and evals that now run and pass<br>• ⚠️ **Gap:** stale maturity evidence, one runnable eval left as prose, and no recorded real use |

## 🔗 Related files

- `src/claude/agents/core/quality_scorecard_reviewer/AGENT.md` — the agent being scored
- `src/claude/agents/core/quality_scorecard_reviewer/evals.yaml` — Test Coverage dimension
- `src/claude/agents/core/code_reviewer/AGENT.md` — Scope Boundaries dimension
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
