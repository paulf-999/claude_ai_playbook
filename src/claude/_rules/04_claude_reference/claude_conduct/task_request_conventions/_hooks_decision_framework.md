# 🪝 Hooks Decision Framework

**Purpose:** Behavioral guardrail for hook proposals — prevents low-ROI hooks by providing clear ROI criteria before suggesting any automation.

Claude reads this whenever considering: "Should I propose a hook?", "This would be better as automation", "Let me add this feature."

---

## 🎯 Core principle

**Default to "no hook" unless ROI is clear.** Hooks are expensive; their cost must be justified by frequency and measurable impact. This framework prevents repeating the 2026-08-07 incident, when 5 low-ROI hooks were proposed and later removed at user cost.

---

## 💰 True cost breakdown

Don't count only "execution time." Hooks accumulate hidden costs:

- **Baseline context:** settings.json grows with each registration — cost is paid even when hook doesn't fire
- **Maintenance surface:** hook script + test file + registration entry + updates when Claude Code changes
- **Failure risk:** hook fails silently or blocks a workflow; user must diagnose and remove
- **Cognitive overhead:** user must know the hook exists, understand what it does, debug if broken
- **Audit burden:** quarterly reviews to verify ROI still holds; eventual removal if not

---

## 🔍 Decision framework

Before proposing a hook, answer these questions in order:

| Question | Evaluation |
|----------|-----------|
| **1. Real or speculative?** | Is this a recurring, observed problem or a hypothetical "might be useful"? Reject speculation. |
| **2. Frequency?** | How many times per month would this hook trigger? <5/month = likely not ROI-positive. |
| **3. Manual cost?** | Without automation, how much user time per month? (in minutes or hours) |
| **4. Setup + maintenance?** | Estimate hours: script + test + registration + 2 years maintenance. |
| **5. ROI threshold?** | Does manual cost × frequency > setup + maintenance by 3x+? |

**Decision tree:**
- ❌ **Stop proposing if:** frequency <5/month, manual cost <30 min/month, setup >4 hours, or simpler alternative exists
- ✅ **Proceed if:** frequency >8/month, manual cost >1 hour/month, setup <3 hours, AND no simpler alternative

---

## 📊 ROI formula

```
Manual effort per month (hours) = (manual_time_per_trigger_min ÷ 60) × frequency_per_month

Setup + maintenance cost (hours) = initial_setup_hours + (maintenance_per_month_hours × 24_months)

ROI threshold: Manual effort > (Setup + maintenance) × 3
```

**Example — ROI-positive:**
- Manual: 5 min/trigger × 15/month = 1.25 hrs/month
- Setup: 2 hrs, maintenance: 0.25 hrs/month = 8 hrs over 2 years
- ROI: 1.25 × 24 = 30 > 8 × 3 = 24 ✅ **Proceed**

**Example — ROI-negative:**
- Manual: 2 min/trigger × 3/month = 0.1 hrs/month
- Setup: 3 hrs, maintenance: 0.1 hrs/month = 5.4 hrs over 2 years
- ROI: 0.1 × 24 = 2.4 < 5.4 × 3 = 16.2 ❌ **Don't propose**

---

## 🚩 Red flags (stop proposing)

Do not propose the hook if any of these apply:

- ❌ **"Might be useful someday"** — no real problem observed yet
- ❌ **"Could save time if..."** — hypothetical benefit, not proven
- ❌ **"Just saw this pattern once"** — insufficient frequency data
- ❌ **Simpler alternative exists** — a rule, manual check, or code review would do
- ❌ **Frequency <5/month** — likely not ROI-positive; keep manual
- ❌ **Setup time >4 hours** — maintenance burden outweighs benefit

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

**enforcement_writing_style.sh** (active):
- Real problem: many sessions produce output violating writing style
- Frequency: ~40+ times/month across all sessions
- Manual alternative: user would review, ask Claude to rewrite (~15 min/violation)
- ROI: Positive; hook saves ~10 hours/month; setup cost recouped in weeks

---

## 🧪 Testing & registration requirements

Before proposing, confirm:

- **Test exists:** Every hook needs a test — see `_rules/01_essentials/testing.md`
- **Naming:** Use `hook_<type>_<domain>.sh` format — see `_rules/01_essentials/conventions/naming_standards.md`
- **Registration:** Hook declared in settings.json with explicit event matcher
- **No wildcards:** Register specific events, not broad matchers

---

## 📋 Audit cadence

After a hook is created:

- **Monthly:** Does this hook still solve the problem it was designed for?
- **Quarterly:** Deep review — is ROI still positive? Are users benefiting?
- **Remove if:** Frequency has dropped, ROI no longer holds, or maintenance cost has grown

---

## 🔗 Related rules

- `_rules/02_claude_standards/behaviour.md` → "Before proposing" section (hook risk flags)
- `_rules/01_essentials/guiding_principles.md` → "Intentionality gates everything" + "Automation ROI"
- `_rules/01_essentials/conventions/naming_standards.md` → Hook naming convention
- `_rules/01_essentials/testing.md` → Hook test requirements
- Parent: `task_request_conventions.md` — Behavioral conventions for user request patterns

---

**Read this before proposing any automation feature.**
