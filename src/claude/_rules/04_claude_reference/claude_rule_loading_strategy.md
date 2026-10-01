<!-- version: 1.2.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-01 -->
<!-- applies_to: **/_rules/**, **/CLAUDE.md -->
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
| `04_claude_reference/` | How Claude Code and this config work (efficiency, delegation, turn budgets, external system access) — used during tool use and config decisions | `claude_operational_efficiency.md` | Wasted context and turns, wrong tool choices | Always-on; some files are lazy-load candidates |
| `05_lazy_load/` | Domain-specific style guides and niche tools (SQL, Airflow, dbt, Terraform) for real, recurring problems in one domain | `style_guide_standards/sql.md` | Nothing outside that domain — that's why it isn't imported | On demand; never imported |

- **Source of truth:** each tier's directory is the current list of its rules, and `CLAUDE.md` shows what is actually imported — the examples above are illustrative only.
- **Placement rationale:** each rule's `Purpose` statement explains why it sits in its tier.
- **Per-parent `_lazy_load/`:** an always-on parent may keep bulky children beside it in `<parent>/_lazy_load/` — never imported, named in the parent's `**Read on demand:**` pointers (e.g. `authoring_skills/_lazy_load/`).

---

## ⚖️ Always-on or lazy-load?

**Always-on (tiers 01–04) when the rule is:**
- **Safety-critical:** e.g. behaviour, guiding principles
- **A quality gate:** e.g. testing, security
- **Needed in most sessions:** more than 70%
- **Foundational for all work:** e.g. naming, writing style

**Lazy-load (`05_lazy_load/`) when the rule is:**
- **Domain-specific:** e.g. style guides for SQL, Airflow, dbt
- **Needed in fewer than 70% of sessions**
- **Tied to a clear trigger:** a command, a tool, a file type
- **Safe to omit:** no safety cost in sessions that don't need it

---

## ➕ When adding a rule

1. Read `CLAUDE.md` to see what's currently imported.
2. Check the tier directories to see what already lives where.
3. Assess: does this rule apply to more than 70% of sessions? Is it blocking or safety-critical?
4. Decide placement with human judgment (session coverage, criticality, size) — not a flowchart.

If unsure, lazy-load it. Always-on rules are the exception, not the default.
