# 📊 Agent Scorecards Summary

**Purpose:** One-glance rollup of every agent scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Agents | 3 | 7.7/10 | 2026-10-26 | • 💪 **Strongest:** `code_reviewer` (8.0/10)<br>• ⚠️ **Weakest:** `technical_writer` (7.3/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`technical_writer`:** resolve the Confluence job it shares with `confluence_create_page`, and record real uses | • 🔻 **Score:** 7.3/10 | `scorecard_technical_writer.md` |
| 2 | • 🔧 **`quality_scorecard_reviewer`:** update its stale maturity evidence and add a run block to `scores_below_nine_quote_evidence` | • 🔻 **Score:** 7.9/10 | `scorecard_quality_scorecard_reviewer.md` |
| 3 | • 🔧 **`code_reviewer`:** tighten the three eval checks that are weaker than their assertions | • 🔻 **Score:** 8.0/10 | `scorecard_code_reviewer.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_code_reviewer.md` | 8.0/10 | 2026-10-26 | • Make `clean_change_approved` check for a plain Approve with no Must or Should items, not just the word "approve"<br>• Make `declines_to_edit_or_post` check that the agent declines to edit, not only that it names `git_review_pr`<br>• Catch alignment findings in `skips_linter_style` even when they lack a bold severity label<br>• Add the "bug hunt goes to `/code-review`" boundary and a "review this PR" trigger to the description |
| `scorecard_quality_scorecard_reviewer.md` | 7.9/10 | 2026-10-26 | • Name in the description when not to use it (hooks, tests, PR diffs, whole-config audits)<br>• Name what owns the hook and test scorecard flow on line 31<br>• Add a run block to `scores_below_nine_quote_evidence`, which needs no full session<br>• Update the stale maturity evidence on lines 53–54 and `tested: false` now that 4 evals run |
| `scorecard_technical_writer.md` | 7.3/10 | 2026-10-26 | • Resolve line 3's hand-off of Confluence pages to `confluence_create_page` against lines 25 and 30, which say the agent drafts them<br>• Record real uses, or lower the Tactical maturity on line 4 until usage exists<br>• Give the boundaries on line 52 a reason, and say how audience rewrites differ from editing existing docs<br>• Check the draft path and "no draft written" assertions, which the run blocks don't cover |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
