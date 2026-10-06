---
name: claude_capture_session_prompts
description: Capture session prompts from history.jsonl into a structured markdown table for review and planning
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 0.4.0 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** confirm `python3 --version` is 3.9 or newer, and stop and tell the user if it isn't.
- **Read first:** read `reference/_implementation.md` for the capture, review and plan phases before running anything.
- **Always:** run `python3 "${CLAUDE_SKILL_DIR}/capture_session_prompts.py" [--date YYYY-MM-DD]`, and never rebuild the table by hand.
- **Always:** write the report to `~/_sessions/YYYY_MM_DD_claude_prompts.md`, with `~` expanded to the absolute home path.
- **Never:** paste raw `history.jsonl` lines into the chat, because they skip the script's secret masking.
- **Never:** edit `history.jsonl`, which Claude Code maintains.

## 🎯 Purpose

Turns a day's prompts from `history.jsonl` into a markdown table for review and planning:
- **Date-filtered capture** — prompts from one date, today by default, in local time.
- **Heuristic categorisation** — theme, status, subject and MoSCoW priority for each prompt.
- **Secret masking** — keys, tokens and password values become `[REDACTED]` before anything is written.
- **Manual refinement** — the table is meant to be edited after it's generated.

## 💡 Example Usage

```
$ /claude_capture_session_prompts

Capturing prompts for 2026-08-26 (local time)...

✅ Capture complete
   - Prompts found: 8
   - Themes: Rules (2), Skills (2), Process (1), Planning (1), Other (2)
   - Status: Done (3), Pending (4), Clarifying (1)

📄 Output saved to: ~/_sessions/2026_08_26_claude_prompts.md
```

## ✨ Best For

Reviewing a session's activity and spotting pending work for the next one. Currently at the **draft** stage — keyword heuristics and one date at a time, with no cross-session aggregation yet.

**Caveats:** expect to refine the categories by hand. Masking is pattern-based, so a secret in an unknown format can still get through. The contract sets `waives_response_standards: true`, so the capture report keeps its own format.

## 📚 References

- `capture_session_prompts.py` — the script this skill runs
- `reference/_implementation.md` — capture, review and plan phases
- `reference/_examples.md` — daily capture, historical review and refinement examples
- `reference/_error_recovery.md` — troubleshooting
- `tests/evals.yaml` — 6 test scenarios, plus pytest in `_tests/skills/claude_capture_session_prompts/`
- `_admin/_quality_scorecards/skills/scorecard_claude_capture_session_prompts.md` — quality scorecard
