---
name: claude_capture_session_prompts
description: Capture session prompts from history.jsonl into a structured markdown table for review and planning
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
  test_coverage_level: comprehensive
---

## 🎯 Purpose

Capture session activity from `history.jsonl` into a structured markdown table:
- **Date-filtered capture** — Extract prompts from a specific date (default: today, Dublin time)
- **Heuristic categorization** — Classify by theme, status, subject, priority (MoSCoW)
- **Structured markdown** — Output table with summary statistics for review and planning
- **Manual refinement workflow** — Edit categories post-generation for accuracy

## 💡 Example Usage

```
$ /capture_session_prompts

Capturing prompts for 2026-08-26 (Dublin time)...

✅ Capture complete
   - Prompts found: 8
   - Themes: Rules (2), Skills (2), Process (1), Planning (1), Other (2)
   - Status: Done (3), Pending (4), Clarifying (1)

📄 Output saved to: ~/.claude/sessions/2026-08-26_prompts.md

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

**Caveats:** Heuristics are keyword-based; manual refinement expected. One date at a time (no cross-session aggregation in v0.1). Python 3.6+ required.

**Special Note — Response Standards Waiver:**
- This skill uses custom interactive output format (heuristic categorization workflow)
- Free-form prompts are incompatible with standard Claude response formatting requirements
- The response standards rule makes an exception for this skill to preserve interactive capability

## 📚 References

**Workflow & Implementation:**
- `reference/_implementation.md` — 3-phase workflow (capture → review → plan)
- `evals.yaml` — 6 test scenarios covering all phases

**Quality & Design:**
- `reference/_quality_scorecard.md` — Quality assessment and Draft maturity justification
- `reference/_error_recovery.md` — Troubleshooting common issues
- `reference/_examples.md` — Usage examples (daily capture, historical review, refinement)
