<!-- version: 1.1.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-10-02 -->
# 📅 Hooks ROI — Precedent & Examples

**Purpose:** The real incidents behind the hooks decision framework — one negative (5 low-ROI hooks removed), one positive and one corrected claim — grounding the framework in evidence, not theory.

---

## 📅 Precedent: 2026-08-07 hook removal

**What happened:** 5 hooks were proposed without ROI evaluation:
- `enforcement_task_tracking.sh`
- `enforcement_naming_convention.sh`
- `enforcement_dir_structure.sh`
- `enforcement_subagent_reads.sh`
- `style_guide_dispatch.sh`

**Cost:** 5000+ tokens/session baseline, zero observed value.

**Outcome:** All removed; user spent time auditing and removing low-value automation.

**Lesson:** Without explicit ROI criteria, automation becomes silent debt.

---

## ✅ Success example

**hook_enforcement_mcp_stale_settings.sh** (active):
- **Real problem:** an MCP server toggled mid-session doesn't change until restart, and tool calls can hang for 2–6 minutes meanwhile (`_mcp_server_toggling.md`).
- **Evidence:** on 2026-10-01 a server disabled mid-session kept working until restart.
- **Cost:** about 0.03s per prompt, and silent unless the server list has changed.
- **ROI:** positive, because one avoided hang outweighs months of near-zero running cost.
- **Frequency:** not measured — the case rests on the incident and the low cost, not on a count.

---

## ⚠️ Correction: claimed ROI with no data

**hook_enforcement_markdown_location.sh** was listed here as the success example, at "~40+ times/month" and "~10 hours/month saved".
- **What was wrong:** the hook never ran until the 2026-10-01 fix in #195, so those figures couldn't have been measured.
- **Lesson:** record a hook's real hits before claiming ROI, and write "not measured" rather than an estimate.
