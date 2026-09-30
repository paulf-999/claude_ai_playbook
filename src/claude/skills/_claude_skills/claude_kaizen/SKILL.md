---
name: claude_kaizen
description: Self-improving loop—audit recent corrections for recurring patterns, promote verified ones into rules with proof (evals), prune stale rules. Run at session start after repeating a correction, or manually via /claude_kaizen. Always outputs diffs for review, never auto-applies.
maturity: draft
tags:
  status: active
  tested: true
  disable_model_invocation: false
---
<!-- version: 0.2.1 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-09-30 -->

## 🎯 Purpose

Self-improving development loop: capture recurring mistakes, promote only verified ones into rules, keep rule set DRY and fresh.

- **Audit friction:** Scan recent error logs for patterns
- **Promote with proof:** Only rules passing evals get added
- **Diff-only output:** Every change is reviewable, never auto-applied
- **Continuous pruning:** Flag stale rules for re-validation

## 💡 Example Usage

**Scenario:** You fix the same bug (e.g., missing input validation) twice in one week.

1. Run `/claude_kaizen` (manually or auto-triggered at session start)
2. Skill audits `~/_errors/` and finds 2 occurrences of the same mistake
3. Candidate is already in `_rules/learned/candidates.md` with count = 2
4. Meets promotion threshold; skill drafts a rule + eval case
5. Runs full test suite (before/after) to catch regressions
6. Outputs a **diff proposal** showing the new rule, eval case, and test results
7. You review the diff, approve, and it's written to `_rules/learned/`

## ✨ Best For

- **Recurring mistakes** — Patterns that appear 2+ times across sessions
- **Rule validation** — Every promoted rule ships with an eval that proves it works
- **Staleness audits** — Flags rules older than 6 months for re-validation
- **Cross-repo learning** — Tracks which repos have promoted similar rules (v2 feature)

**When NOT to use:**
- One-off mistakes (not promoted until they recur)
- Manual rule authoring (use `authoring_rules.md` instead)
- Batch rule creation (this audits and promotes one pattern at a time)

**Special Note — Response Standards Waiver:**
- This skill uses custom interactive output format (multi-phase audit → promote → validate workflow)
- Free-form prompts are incompatible with standard Claude response formatting requirements
- The response standards rule makes an exception for this skill to preserve interactive capability

## 📚 References

- `evals/runner.py` — scores eval cases before and after a proposed rule change
- `evals/dmt-scripts-claude_ai_playbook.yaml` — seed eval cases proving each promoted rule works
- `~/.claude/_rules/learned/` — Auto-promoted rules with validation dates
- `reference/_roadmap.md` — planned v2 enhancements
- `tests/evals.yaml` — 7 test scenarios covering promotion, validation, pruning and scope
- `_admin/_quality_scorecards/skills/scorecard_claude_kaizen.md` — 7-dimension quality scorecard
