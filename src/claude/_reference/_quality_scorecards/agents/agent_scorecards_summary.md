# 📊 Agent Scorecards Summary

**Purpose:** One-glance rollup of every agent scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Agents | 3 | 7.4/10 | 2026-10-28 | • 💪 **Strongest:** `quality_scorecard_reviewer` (8.1/10)<br>• ⚠️ **Weakest:** `technical_writer` (6.3/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`technical_writer`:** decide whether it drafts Confluence pages, and fix or explain its 4 failing evals | • 🔻 **Score:** 6.3/10 | `scorecard_technical_writer.md` |
| 2 | • 🔧 **`code_reviewer`:** find out why `findings_have_fixes` fails, then fix the agent or the eval | • 🔻 **Score:** 7.9/10 | `scorecard_code_reviewer.md` |
| 3 | • 🔧 **`quality_scorecard_reviewer`:** fix the failing `declines_to_edit_or_score_hooks` eval and update its stale maturity evidence | • 🔻 **Score:** 8.1/10 | `scorecard_quality_scorecard_reviewer.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_quality_scorecard_reviewer.md` | 8.1/10 | 2026-10-28 | • Fix the failing `declines_to_edit_or_score_hooks` eval, either by changing the agent's hook refusal or by widening the eval's `must_match` regex, so that every "not for" case passes when it runs<br>• Add a `run` block to `scores_below_nine_quote_evidence`, since it needs no full session and so shouldn't be skipped<br>• Add `git_review_pr` to the "Not for" PR-diff bullet beside `code_reviewer`<br>• Put the "not for" boundary (hooks, tests, PR diffs, config audits) in the frontmatter `description`, so the description alone says when not to use the agent |
| `scorecard_code_reviewer.md` | 7.9/10 | 2026-10-28 | • Find out why `findings_have_fixes` fails, then fix the agent or loosen the eval's narrow `for item in items:` regex, and record which it was<br>• Add `quality_scorecard_reviewer` and `claude_review_config` to "When to use" as "Not for" lines, so every near neighbour is named<br>• Add a usage record (dated rows or linked PRs) beyond the single 2026-10-05 use<br>• Add "review this PR" and "score this PR" to `triggers:`, since the routing eval's own prompt uses that wording |
| `scorecard_technical_writer.md` | 6.3/10 | 2026-10-28 | • Decide whether this agent drafts Confluence pages, then make the description, "When to use", triggers and evals all say the same thing<br>• If Confluence drafting stays, add `confluence_create_page`'s own drafting to "Not for", or remove Confluence pages from the agent<br>• Add triggers for common phrasings such as "write a PR description" and "write the PR body"<br>• Record real uses, for example usage rows or dated PRs drafted by the agent, or step maturity down to draft as line 59 says to |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
