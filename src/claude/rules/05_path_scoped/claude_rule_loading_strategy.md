---
paths:
  - "**/rules/**"
  - "**/_rules_lazy_load/**"
  - "**/CLAUDE.md"
---
<!-- version: 3.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: low — a rule lands in the wrong tier, which is easy to move -->
<!-- loading: path-scoped — only needed when placing or moving a rule, so it loads when rule files or CLAUDE.md are open -->
# 📋 Rules Loading Strategy

**Purpose:** Decide which folder a rule belongs in — and so whether it loads every session, with matching files, or only on demand.

**Principle:** Lazy-load by default. Always-on rules must block or apply everywhere.

Claude Code loads every `.md` under `rules/` on its own, so every always-on file adds its full size to every session — measured tier sizes are in `_rules_lazy_load/_tier_readmes/00_rules_overview.md`. Only rules that justify this cost stay always-on.

---

## 📁 The six rule folders

| Tier | What belongs there | Example | If it's missing | Loading |
|---|---|---|---|---|
| `01_essentials/` | Foundational decision-making principles and user-facing conventions (naming, writing style, response standards) that apply to every task | `guiding_principles.md` | Confused user experience, quality decay, violated conventions | Always-on |
| `02_claude_standards/` | Blocking quality gates and safe operational conduct (testing, security, git, portable paths) that gate new features, rules and abstractions | `behaviour.md` | Quality decay, security vulnerabilities, scope creep, safety regression | Always-on |
| `03_authoring_guidelines/` | Standards for authoring the config's own rules, skills and agents — used whenever an artefact is being created | `authoring_rules.md` | Inconsistent artefact structure, scope creep, missing tests | Always-on |
| `04_claude_reference/` | How Claude Code and this config work (efficiency, delegation, turn budgets, external system access) — used during tool use and config decisions | `claude_operational_efficiency.md` | Wasted context and turns, wrong tool choices | Always-on |
| `05_path_scoped/` | Domain-specific rules tied to one file type (SQL, Airflow, dbt, Terraform, testing) through `paths:` frontmatter | `style_guide_standards/sql.md` | Nothing outside that domain — that's why it loads only with matching files | Path-scoped; loads when a matching file is open |
| `_rules_lazy_load/` | Niche tools, discretionary rules and bulky children, beside `rules/` rather than inside it | `turn_budgets.md` | Nothing until Claude follows a pointer to it | On demand; never loaded automatically |

- **Source of truth:** each folder is the current list of its rules — the examples above are illustrative only.
- **Folder sets the mode:** tiers 01–04 load every session, unless a rule there has `paths:` (e.g. `authoring_agents.md`), and nothing under `rules/` is `@import`ed.
- **Placement rationale:** each rule's `Purpose` statement explains why it sits in its tier.
- **On-demand children:** an always-on parent keeps bulky children in `_rules_lazy_load/<parent>/`, named in its `**Read on demand:**` pointers (e.g. `_rules_lazy_load/authoring_skills/`).

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

## 🎯 When `paths:` fits

A rule under `rules/` with `paths:` frontmatter loads whenever Claude reads a matching file — the most reliable lazy trigger.

- **Clear file type:** the rule is about one kind of file, for example `**/*.sql` or `**/agents/**`.
- **Read before write:** Claude reads a matching file before editing it, so the trigger fires in time.
- **New-file gap:** creating the first file of its kind reads nothing, so keep a `**Read on demand:**` pointer in an always-on rule for that case.
- **Backstop for high cost:** a high miss cost also needs a hook or test that catches the mistake, such as the naming-convention hook.
- **Not for every-session rules:** a rule about how Claude works, rather than which file it touches, stays always-on.
- **Proven:** `test_path_scoped_rules_live.py` shows in a real session that a `paths:` rule loads with a matching file and not otherwise.
- **Stays pointer-based:** a rule with no file type of its own, such as delegation, MCP trust or date formats — its `load:` reason names the pointer.

---

## 🚩 Audit flags

- **Promote:** a lazy rule with `miss_cost: high` that the report shows missed — add a trigger or move it to tiers 01–04.
- **Demote:** an always-on rule with `miss_cost: low` applied in under half of sessions — move it to `05_path_scoped/` with `paths:`, or to `_rules_lazy_load/`.
- **Stale:** a rule with no use for 90 days, per `rule_usage_history.csv` — archive it or refresh its evidence.
- **Not enough data:** fewer than 10 applied sessions — no decision yet.
- **Cut-offs:** 10 sessions, half and 90 days are first guesses in `audit_rule_usage.py`, reviewed after 3 reports.

---

## ➕ When adding a rule

1. Check the `rules/` tier folders and `_rules_lazy_load/` to see what already lives where.
2. Give the rule `applies_to` and `miss_cost` headers, per `_claude_config_metadata.md`.
3. Run `make audit_rule_usage` and compare the closest existing rules' applied % and misses.
4. Place it with the table above, judging on criticality and size where the numbers don't decide.

If unsure, lazy-load it. Always-on rules are the exception, not the default.
