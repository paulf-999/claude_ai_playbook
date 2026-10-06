# 🏗️ Claude Config Architecture & Design Patterns

**Purpose:** Reference guide to your global Claude config's structural and design decisions. Use when understanding how rules fit together — or when deciding where to add features, whether to automate, and how to keep config lean.

---

## 🎯 Design philosophy

The config is built on the principles in `guiding_principles.md` — read that file for the full, current list. These are the ones that most shape its layout:

| Principle | How it shapes config |
|---|---|
| **Lazy-load by default** | Only tiers 01–03 load every session; domain-specific rules live in `_rules_lazy_load/` and are read on demand |
| **Explicit over implicit** | The folder a rule sits in says how it loads — `rules/` tiers 01–03 every session, `paths:` rules with matching files, `_rules_lazy_load/` on demand; no silent automation |
| **Context efficiency** | Always-on size is measured, not estimated; broad imports are questioned in review; unused features are retired |
| **Intentionality** | Features exist because they solve real, recurring problems — not "nice to have" |
| **Reversible by design** | Rules are small, single-purpose; can be commented out or deleted without side effects |
| **Goal-driven design** | Align config to current work goals, ruthlessly prune during 6-month resets; don't build for "all scenarios" |
| **Automation ROI** | Only automate (hooks, skills, commands) when cost is justified by frequency; calculate actual payback period |

---

## 🎯 Two principles in more depth

### Goal-driven design

**Pattern:** Align config to current work goals; ruthlessly prune during 6-month resets.

**Why:** Config designed for "all scenarios" becomes noise and bloat. Every unused rule wastes tokens. Periodic resets are opportunities to re-align to what matters *now*.

**How it works:**
- Every 6 months (per Boris Cherny), archive and reset `~/.claude/`
- During reset: audit every rule — "Have I used this in the last 6 months? Does it serve my current work?"
- Keep only what's actively needed
- Move unused rules to lazy-load or archive

**Gotcha:** Don't mistake "comprehensive" for "good." Lean config beats complete config.

### Automation ROI

**Pattern:** Only automate (hooks, skills, commands) when cost is justified by frequency.

**Why:** Not everything should be automated. A $5 hook that saves 5 min/month costs more than manual work. Automation has hidden costs: development, registration, testing, maintenance.

**How it works:**
1. **Frequency:** How many times/month?
2. **Manual cost:** How long (minutes)?
3. **Automation cost:** Setup time (hours) + monthly API cost ($)
4. **Payback period:** (automation cost) / (frequency × manual time / 60)
5. **Rule:** If payback < 6 months → automate; else → manual

**Example:** Pre-commit hook saves 2 min/month. Setup cost = 1 hour. Payback = 30 months. **Decision: Stay manual.**

**Gotcha:** Automation convenience ≠ automation value. Calculate before you build.

---

## 📂 Directory structure

This page describes the principle, not an inventory — the README in each directory is the current source of truth, so nothing here goes stale when files are added or moved.

| Path | What lives there | Current contents |
|---|---|---|
| `CLAUDE.md` | Entry point; imports memory and aliases | Read the file itself |
| `rules/` | Rules Claude Code loads natively, in tiers `01_essentials/` to `03_authoring_guidelines/` plus `04_path_scoped/` | `_rules_lazy_load/_tier_readmes/00_rules_overview.md` and each tier's README |
| `_rules_lazy_load/` | Rules read on demand, never loaded automatically, plus the tier READMEs | `_rules_lazy_load/README.md` |
| `_reference/` | Background docs like this one — never imported | `_reference/README.md` |
| `_tests/` | pytest suite for rules, hooks, skills and settings | `_tests/README.md` |
| `hooks/`, `skills/`, `agents/`, `_templates/` | Hooks, skills, sub-agents, authoring templates | Each directory's README |

---

## 🔄 What loads when

- **Always-on:** Claude Code loads every `.md` under `rules/` without `paths:` frontmatter — tiers 01–03 and their children; the folders are the current list.
- **With matching files:** rules with `paths:` (mostly `rules/04_path_scoped/`) load when Claude reads a file their globs match.
- **On demand:** `_rules_lazy_load/` and `_reference/` are never imported; Claude reads them when a task needs them.
- **Cost:** measure it rather than estimate it — `_rules_lazy_load/_tier_readmes/00_rules_overview.md` records measured tier sizes, and each always-on file adds its full size to every session.

---

## 🎯 How rules interact

Rules are organized by concern, creating clear separation that simplifies auditing:

| Interaction layer | Key files | Purpose |
|---|---|---|
| **Security** | `behaviour.md` → `security/_security_guardrails.md` → `security.md` | Progressive gates from task approach to code standards |
| **Quality** | `testing.md` + `hook_enforcement_naming_convention.sh` | Naming checked as Claude creates files; tests run in pre-commit and CI |
| **Efficiency** | `_rules_lazy_load/` + `_reference/` | Domain rules and background docs read on demand, keeping the baseline small |

For detailed security architecture, see **[claude_config_architecture/_security.md](claude_config_architecture/_security.md)**.

For testing strategy and coverage, see **[claude_config_architecture/_testing.md](claude_config_architecture/_testing.md)**.

---

## 🔄 Evolution & Maintenance (Goal-Driven Auditing)

Regular maintenance cycles ensure the config stays intentional and focused on current goals:

### Audit Cadence

- **Monthly:** Spot-check — any obviously unused features?
- **Quarterly:** Deep review — search session transcripts for actual usage of each rule
- **Every 6 months:** Full reset (per Boris Cherny) — archive and restart to force intentionality review
  - **During reset:** Audit every rule — "Does this serve my current work?" Archive ruthlessly.
  - **Move to lazy-load:** Any domain-specific rule not immediately relevant
  - **Keep always-on:** Only foundational rules (guiding principles, security, testing)

### Adding a New Rule

Use this decision tree:

1. **Does it apply to EVERY session** (regardless of project type)?
   - **Yes** → Place in the matching always-on tier (`01_essentials/` to `03_authoring_guidelines/`, per `_rules_lazy_load/_tier_readmes/00_rules_overview.md`) and `@import` it from that tier's entry file
   - **No** → Go to step 2

2. **Is it domain-specific** (SQL, dbt, Terraform, etc.)?
   - **Yes** → Place in `_rules_lazy_load/`; list it in that tier's README
   - **No** → Reconsider whether it's needed at all

3. **Will you use this 5+ times/month**?
   - **Yes** → Consider always-on if foundational; else lazy-load with easy reference
   - **No** → Archive or leave out; add when you need it

### Deciding: Automation vs. Manual (Principle C)

Before creating a hook or skill:

1. **What's the task?** Be specific.
2. **How often?** Times/month?
3. **Manual cost?** Minutes to do manually?
4. **Automation cost?** Hours to build + test + register?
5. **Payback period:** Calculate in months. If < 6: automate. Else: stay manual.
