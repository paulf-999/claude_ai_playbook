---
paths:
  - "**/_rules/**"
  - "**/CLAUDE.md"
---
<!-- version: 2.1.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-02 -->
<!-- miss_cost: low — a rule lands in the wrong tier, which is easy to move -->
<!-- loading: path-scoped — only needed when placing or moving a rule, so it loads when _rules/ files or CLAUDE.md are open -->
# 📋 Rules Loading Strategy

**Purpose:** Decide which of the five tiers a rule belongs in — and so whether it loads every session or only on demand.

**Principle:** Lazy-load by default. Always-on rules must block or apply everywhere.

Every import adds the imported file's full size to every session — measured tier sizes are in `_rules/README.md`. Only rules that justify this cost stay always-on.

---

## 📁 The five tiers

| Tier | What belongs there | Example | If it's missing | Loading |
|---|---|---|---|---|
| `01_essentials/` | Foundational decision-making principles and user-facing conventions (naming, writing style, response standards) that apply to every task | `guiding_principles.md` | Confused user experience, quality decay, violated conventions | Always-on |
| `02_claude_standards/` | Blocking quality gates and safe operational conduct (testing, security, git, portable paths) that gate new features, rules and abstractions | `behaviour.md` | Quality decay, security vulnerabilities, scope creep, safety regression | Always-on |
| `03_authoring_guidelines/` | Standards for authoring the config's own rules, skills and agents — used whenever an artefact is being created | `authoring_rules.md` | Inconsistent artefact structure, scope creep, missing tests | Always-on |
| `04_claude_reference/` | How Claude Code and this config work (efficiency, delegation, turn budgets, external system access) — used during tool use and config decisions | `claude_operational_efficiency.md` | Wasted context and turns, wrong tool choices | Always-on |
| `05_lazy_load/` | Domain-specific style guides and niche tools (SQL, Airflow, dbt, Terraform) for real, recurring problems in one domain | `style_guide_standards/sql.md` | Nothing outside that domain — that's why it isn't imported | On demand; never imported |

- **Source of truth:** each tier's directory is the current list of its rules, and `CLAUDE.md` shows what is actually imported — the examples above are illustrative only.
- **Placement rationale:** each rule's `Purpose` statement explains why it sits in its tier.
- **Per-parent `_lazy_load/`:** an always-on parent may keep bulky children beside it in `<parent>/_lazy_load/` — never imported, named in the parent's `**Read on demand:**` pointers (e.g. `authoring_skills/_lazy_load/`).

---

## ⚖️ Always-on or lazy-load?

Decide from two numbers per rule, both in `_admin/_audits/audit_rule_usage.md`:

- **Applied %:** the share of sessions matching the rule's `applies_to` globs, measured by `make audit_rule_usage`.
- **Miss cost:** what breaks when the rule applies but isn't loaded, from its `miss_cost` header.

| Miss cost | Applied in half of sessions or more | Applied in fewer |
|---|---|---|
| **High** | Always-on | Lazy only with `paths:` or a hook that loads it, otherwise always-on |
| **Medium** | Always-on | Lazy, with a trigger where one exists |
| **Low** | Always-on only if small | Lazy |

- **Domain style guides:** SQL, Airflow, dbt and similar guides are lazy, triggered by `paths:` on their file type.
- **Pointers aren't triggers:** a `**Read on demand:**` pointer works only if Claude remembers it, so it never counts for a high-cost rule.

---

## 🚩 Audit flags

- **Promote:** a lazy rule with `miss_cost: high` that the report shows missed — add a trigger or move it to tiers 01–04.
- **Demote:** an always-on rule with `miss_cost: low` applied in under half of sessions — move it to `05_lazy_load/` or a per-parent `_lazy_load/`.
- **Stale:** a rule with no use for 90 days, per `rule_usage_history.csv` — archive it or refresh its evidence.
- **Not enough data:** fewer than 10 applied sessions — no decision yet.
- **Cut-offs:** 10 sessions, half and 90 days are first guesses in `audit_rule_usage.py`, reviewed after 3 reports.

---

## ➕ When adding a rule

1. Read `CLAUDE.md` to see what's currently imported.
2. Check the tier directories to see what already lives where.
3. Give the rule `applies_to` and `miss_cost` headers, per `_claude_config_metadata.md`.
4. Run `make audit_rule_usage` and compare the closest existing rules' applied % and misses.
5. Place it with the table above, judging on criticality and size where the numbers don't decide.

If unsure, lazy-load it. Always-on rules are the exception, not the default.
