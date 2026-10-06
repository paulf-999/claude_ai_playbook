---
name: claude_kaizen
description: Self-improving loop—audit recent corrections for recurring patterns, promote verified ones into rules with proof (evals), prune stale rules. Run at session start after repeating a correction, or manually via /claude_kaizen. Always outputs diffs for review, never auto-applies.
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
  disable_model_invocation: false
---
<!-- version: 0.6.0 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** confirm `~/claude/_errors/` exists and holds logs, and if not, say so and stop without proposing any rule.
- **Read first:** read `reference/_implementation.md` for the audit, promote, validate and prune phases.
- **Always:** show every rule and eval case as a diff with before/after results, and wait for an explicit yes before writing to `_rules_lazy_load/learned/`.
- **Always:** tell the user that `evals/runner.py` makes one Claude call per case before running it.
- **Never:** promote a pattern seen fewer than 2 times, or one whose after-run shows a regression.
- **Never:** delete or edit a stale rule, which only gets flagged for re-validation.

## 🎯 Purpose

Self-improving development loop: capture recurring mistakes, promote only verified ones into rules, keep rule set DRY and fresh.

- **Audit friction:** Scan recent error logs for patterns
- **Promote with proof:** Only rules passing evals get added
- **Diff-only output:** Every change is reviewable, never auto-applied
- **Continuous pruning:** Flag stale rules for re-validation

## 💡 Example Usage

**Scenario:** You fix the same bug (e.g., missing input validation) twice in one week.

1. Run `/claude_kaizen` (manually or auto-triggered at session start)
2. Skill audits `~/claude/_errors/` and finds 2 occurrences of the same mistake
3. Candidate is already in `_rules_lazy_load/learned/candidates.md` with count = 2
4. Meets promotion threshold; skill drafts a rule + eval case
5. Runs full test suite (before/after) to catch regressions
6. Outputs a **diff proposal** showing the new rule, eval case, and test results
7. You review the diff, approve, and it's written to `_rules_lazy_load/learned/`

## ✨ Best For

Currently at the **draft** stage — one repo at a time, with no SessionStart trigger or cross-repo promotion yet.

- **Recurring mistakes** — Patterns that appear 2+ times across sessions
- **Rule validation** — Every promoted rule ships with an eval that proves it works
- **Staleness audits** — Flags rules older than 6 months for re-validation
- **Cross-repo learning** — Tracks which repos have promoted similar rules (v2 feature)

**When NOT to use:**
- One-off mistakes (not promoted until they recur)
- Manual rule authoring (use `authoring_rules.md` instead)
- Batch rule creation (this audits and promotes one pattern at a time)

**Output format:** the contract sets `waives_response_standards: true`, so the audit keeps its own step-by-step format.

## 📚 References

- `evals/runner.py` — asks headless Claude (`claude -p`, no tools) each eval prompt against the rules under test and checks the reply with `must_match` / `must_not_match` regexes; one Claude call per case
- `evals/claude_ai_playbook.yaml` — seed eval cases proving each promoted rule works
- `<config-dir>/_rules_lazy_load/learned/` — Auto-promoted rules with validation dates, where `<config-dir>` is `$CLAUDE_CONFIG_DIR` (or `~/.claude` when it's unset)
- `reference/_implementation.md` — audit, promote, validate and prune phases
- `reference/_roadmap.md` — planned v2 enhancements
- `tests/evals.yaml` — 7 test scenarios covering promotion, validation, pruning and scope
- `_admin/_quality_scorecards/skills/scorecard_claude_kaizen.md` — 7-dimension quality scorecard
