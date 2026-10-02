# 📊 Hook Scorecards Summary

**Purpose:** One-glance rollup of every hook scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Hooks | 5 | 8.5/10 | 2026-10-02 | • 💪 **Strongest:** `hook_enforcement_mcp_stale_settings.sh` (9.0/10)<br>• ⚠️ **Weakest:** `hook_style_guide_response_standards.sh` (8.0/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 📅 **Reserved hook:** set a date to wire in or remove `hook_style_guide_response_standards.sh` | • 💤 **Unused:** it has been reserved since it was added | `scorecard_hook_style_guide_response_standards.md` |
| 2 | • 🧪 **Validator check:** test the naming validator's `--check` mode directly | • 🤫 **Fails open:** a broken validator would switch the hook off silently | `scorecard_hook_enforcement_naming_convention.md` |
| 3 | • 📌 **First hit:** record the first real catch of `hook_enforcement_markdown_location.sh`, or retire it after 90 days | • 📭 **No evidence yet:** it has only run since 2026-10-01 | `scorecard_hook_enforcement_markdown_location.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_hook_enforcement_mcp_stale_settings.md` | 9.0/10 | 2026-10-02 | — (≥8.5) |
| `scorecard_hook_style_guide_response_standards_inject.md` | 8.6/10 | 2026-10-02 | — (≥8.5) |
| `scorecard_hook_enforcement_naming_convention.md` | 8.4/10 | 2026-10-02 | • Test the validator's `--check` mode directly. |
| `scorecard_hook_enforcement_markdown_location.md` | 8.4/10 | 2026-10-02 | • Record its first real hit, or retire it after 90 days. |
| `scorecard_hook_style_guide_response_standards.md` | 8.0/10 | 2026-10-02 | • Set a date to wire in or remove the reserved hook. |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
