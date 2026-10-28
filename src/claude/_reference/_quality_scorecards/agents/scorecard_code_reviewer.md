# Quality Scorecard — code_reviewer

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-28

**Overall score:** 7.9/10

**Recommended improvements:**
- Find out why `findings_have_fixes` fails, then fix the agent or loosen the eval's narrow `for item in items:` regex, and record which it was.
- Add `quality_scorecard_reviewer` and `claude_review_config` to "When to use" as "Not for" lines, so every near neighbour is named.
- Add a usage record (dated rows or linked PRs) beyond the single 2026-10-05 use.
- Add "review this PR" and "score this PR" to `triggers:`, since the routing eval's own prompt uses that wording.
- Count the concepts in Role & Principles down, or group them, so the agent stays at raw complexity 3 or below as it grows.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-26 | • 🎯 **Description:** says what it does, when to use it and that it is read-only<br>• 🔍 **Trigger gap:** `triggers:` has "review this diff", "review my changes", "score this diff" and "code review", but no PR phrasing, even though eval `natural_phrase_selects_agent` routes on "score this PR" |
| **Scope Boundaries** | 8/10 | 2026-10-26 | • ✅ **Fenced against the closest neighbours:** "Not for" names `git_review_pr` (posting) and the built-in `/code-review` (bug hunt)<br>• ⚠️ **Unnamed neighbours:** `quality_scorecard_reviewer` (it also "scores", which overlaps the "score this diff" trigger) and `claude_review_config` are not named<br>• 📝 **Partial:** the constraint says only "whole-repo audits are a separate job", without naming the skill that does them |
| **Complexity** | 7/10 | 2026-10-26 | • 🧮 **Raw 3:** one job (Concepts 1), reads the diff plus repo rules and style guides across folders (Scope 2), no external services (Dependencies 0), no fixtures (Prerequisites 0)<br>• ⚠️ **Many rules:** six principles plus three "Does NOT" constraints, close to the next concept band |
| **Evidence of Need** | 7/10 | 2026-10-26 | • ✅ **One real use:** "reviewing an infrastructure PR through `git_review_pr` on 2026-10-05" (Maturity Justification, line 57)<br>• ⚠️ **No repeat record:** no usage log or later dated uses, and the only record is the agent's own claim |
| **Test Coverage** | 7/10 | 2026-10-28 | • 📊 **Count:** 8 evals, the top of the draft range (5–8), covering triggering, verdicts, template, fixes, linter skip and both "not for" cases<br>• ✅ **Runs:** 6 of the 8 have `run` blocks, and the 2 routing evals skipped need a full session<br>• ⚠️ **Pass rate 83% (5/6):** `findings_have_fixes` fails, and nothing explains it, so the anchor caps this at 8<br>• ⚠️ **Below the cap:** that eval tests the headline "Specific and fixable" principle, and its `must_match` needs a line starting with exactly `for item in items:` or one of two variants, so the failure may be in the regex or in the agent |
| **Structural Compliance** | 9/10 | 2026-10-28 | • ✅ **Hard gates pass:** full frontmatter (name, description, maturity, triggers, tools, model, isolation), metadata header right after it, five sections plus Maturity Justification, 6 principles, a reason given for each constraint<br>• 📏 **Minor:** the description is three sentences, while `_core_standards.md` asks for one, and the file is 65 lines against the ~40–60 target |
| **Tool Safety** | 9/10 | 2026-10-28 | • 🔒 **Least privilege:** `tools: Read, Grep, Glob`, with no Bash, Write or MCP<br>• ✅ **Isolation:** `isolation: none` is justified because "it never writes files" |
| **Overall** | **7.9/10** | 2026-10-28 | • 💪 **Strength:** a tightly scoped, read-only reviewer with runnable evals that include the secret-echo and refusal cases<br>• ⚠️ **Gap:** one unexplained eval failure on its core principle, a single recorded use, and two near neighbours left out of "Not for" |

## 🔗 Related files

- `src/claude/agents/core/code_reviewer/AGENT.md` — the artefact being scored
- `src/claude/agents/core/code_reviewer/evals.yaml` — Test Coverage (`findings_have_fixes`, `natural_phrase_selects_agent`)
- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — Scope Boundaries and Evidence of Need (the caller)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_core_standards.md` — Structural Compliance (one-sentence description, draft eval count)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/_reference/_quality_scorecards/scoring_anchors.md` — run pass-rate bands for Test Coverage
