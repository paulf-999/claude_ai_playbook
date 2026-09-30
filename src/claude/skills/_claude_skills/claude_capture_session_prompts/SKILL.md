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
<!-- version: 0.2.1 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-09-30 -->

## 🎯 Purpose

Capture session activity from `history.jsonl` into a structured markdown table:
- **Date-filtered capture** — Extract prompts from a specific date (default: today, local time)
- **Heuristic categorization** — Classify by theme, status, subject, priority (MoSCoW)
- **Structured markdown** — Output table with summary statistics for review and planning
- **Manual refinement workflow** — Edit categories post-generation for accuracy

## 💡 Example Usage

**Run:** `python3 "${CLAUDE_SKILL_DIR}/capture_session_prompts.py" [--date YYYY-MM-DD]` — Claude Code expands `${CLAUDE_SKILL_DIR}` to this skill's folder.

```
$ /claude_capture_session_prompts

Capturing prompts for 2026-08-26 (local time)...

✅ Capture complete
   - Prompts found: 8
   - Themes: Rules (2), Skills (2), Process (1), Planning (1), Other (2)
   - Status: Done (3), Pending (4), Clarifying (1)

📄 Output saved to: ~/_sessions/2026_08_26_claude_prompts.md

Next: Review table for accuracy, adjust categorization, use for planning.
```

**Generated table sample:**

| Timestamp | Theme | Subject | Status | Proposed Action | Closure | MoSCoW | Prompt |
|---|---|---|---|---|---|---|---|
| 09:15 | Rules | Guiding principles | ✅ Done | Review usage evidence | Updated guiding_principles.md | Must | Review guiding principles... |
| 13:45 | Planning | Sprint items | ⏳ Pending | Plan next sprint | TODO added | Should | What should be next sprint focus... |

---

## ✨ Best For

Capturing end-of-session activity for review, planning, and auditing. Generates a structured table that identifies pending work and priorities for next session.

**Caveats:** Heuristics are keyword-based; manual refinement expected. One date at a time (no cross-session aggregation in v0.1). Python 3.9+ required.

**Special Note — Response Standards Waiver:**
- **Exemption:** `_rules/05_lazy_load/response_standards_enforcement.md` exempts skill invocation output from the response standards.
- **Declared:** the contract sets `waives_response_standards: true`, so this skill's capture report keeps its own format.

## 📚 References

**Workflow & Implementation:**
- `capture_session_prompts.py` — the script this skill runs (reads history, writes the table)
- `reference/_implementation.md` — 3-phase workflow (capture → review → plan)
- `tests/evals.yaml` — 6 test scenarios covering all phases
- `_tests/skills/claude_capture_session_prompts/` — pytest coverage for the script

**Quality & Design:**
- `_admin/_quality_scorecards/skills/scorecard_claude_capture_session_prompts.md` — Quality assessment and Draft maturity justification
- `reference/_error_recovery.md` — Troubleshooting common issues
- `reference/_examples.md` — Usage examples (daily capture, historical review, refinement)
