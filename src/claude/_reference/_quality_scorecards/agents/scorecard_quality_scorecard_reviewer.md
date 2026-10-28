# Quality Scorecard — quality_scorecard_reviewer

**Date Created:** 2026-10-22
**Date Updated:** 2026-10-28

**Overall score:** 8.1/10

**Recommended improvements:**
- Fix the failing `declines_to_edit_or_score_hooks` eval, either by changing the agent's hook refusal or by widening the eval's `must_match` regex, so that every "not for" case passes when it runs.
- Add a `run` block to `scores_below_nine_quote_evidence`, since it needs no full session and so shouldn't be skipped.
- Add `git_review_pr` to the "Not for" PR-diff bullet beside `code_reviewer`.
- Put the "not for" boundary (hooks, tests, PR diffs, config audits) in the frontmatter `description`, so the description alone says when not to use the agent.
- Replace "with no recorded runs yet" in Maturity Justification with the recorded run count from `score_history.csv`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-26 | • 💪 **Description:** says what it does, when to use it ("Use when asked to score, re-score or independently review…") and that it is read-only<br>• ⚠️ **No when-not:** the AGENT.md `description` (line 3) leaves out the hooks, tests, PR-diff and config-audit exclusions, which appear only in the body (lines 31–32), so it misses the ~9 anchor |
| **Scope Boundaries** | 8/10 | 2026-10-26 | • 💪 **Fenced mostly:** names hooks/tests, `code_reviewer` and `claude_review_config` in "Not for"<br>• ⚠️ **Missed neighbour:** `git_review_pr` also reviews PR diffs, and evals.yaml `pr_review_goes_to_code_reviewer` expects "code_reviewer or git_review_pr", but AGENT.md line 32 names only `code_reviewer` |
| **Complexity** | 7/10 | 2026-10-26 | • 🧮 **Raw 3:** Concepts 1 (one scoring job with a few rules), Scope 2 (reads the artefact plus `_reference/_quality_scorecards/`, `_templates/scorecard/` and `_rules_lazy_load/` rubric files), Dependencies 0, Prerequisites 0<br>• ⚠️ **Anchor:** matches the ~7 row, "one job that reads across several folders" |
| **Evidence of Need** | 9/10 | 2026-10-28 | • 📈 **Recurring:** `score_history.csv` holds 76 rows with reviewer `quality_scorecard_reviewer`, a recorded use across many artefacts<br>• ⚠️ **Stale claim:** AGENT.md line 53 still says "no recorded runs yet" (counted under Structural Compliance) |
| **Test Coverage** | 7/10 | 2026-10-28 | • 📊 **Right count:** 7 evals, within the draft range of 5–8, covering triggering, output, anchoring and both "not for" cases<br>• ⚠️ **Pass rate 75%:** `audit_agent_evals.py` passed 3 of 4 runnable evals (2026-10-28), and the anchors cap 75–89% at 8 or below<br>• ⚠️ **Not-for case fails:** the failing eval, `declines_to_edit_or_score_hooks`, is itself a "not for" case, so the ~9 anchor ("including the 'not for' cases") isn't met<br>• ⚠️ **Avoidable skip:** `scores_below_nine_quote_evidence` has no `run` block, even though it needs no full session |
| **Structural Compliance** | 8/10 | 2026-10-26 | • 💪 **Gates met:** full frontmatter (name, description, maturity, triggers, tools, model, isolation), metadata header straight after it, every required section, 61 lines and 6 principles<br>• 💪 **Evals complete:** each eval has name, description, input, setup and expected_output<br>• ⚠️ **Maturity evidence stale:** the hard gate "Maturity justified with evidence" is undercut by line 53, "no recorded runs yet", which the history CSV contradicts |
| **Tool Safety** | 10/10 | 2026-10-28 | • 🔒 **Least privilege:** `tools: Read, Grep, Glob` only, with no Write, Edit or Bash, which suits a read-only reviewer<br>• 💪 **Isolation:** `isolation: none` is appropriate, because the agent can't write files |
| **Overall** | **8.1/10** | 2026-10-28 | • 💪 **Strength:** tightly scoped read-only tools, a clear purpose and heavy recorded use<br>• ⚠️ **Gap:** a failing "not for" eval, one avoidable skipped eval, a near neighbour missing from "Not for", and a stale maturity line<br>• 🔁 **Self-scored:** this agent scored itself, so a cross-check by a different reviewer would strengthen the result |

## 🔗 Related files

- `src/claude/agents/core/quality_scorecard_reviewer/AGENT.md` — the artefact being scored
- `src/claude/agents/core/quality_scorecard_reviewer/evals.yaml` — Test Coverage, Scope Boundaries
- `src/claude/_reference/_quality_scorecards/score_history.csv` — Evidence of Need, Structural Compliance
- `src/claude/scripts/_audit_scripts/audit_agent_evals.py` — Test Coverage (run pass rate)
- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — Scope Boundaries (near neighbour missing from "Not for")
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/_reference/_quality_scorecards/scoring_anchors.md` — anchors for every dimension
