# 03_authoring_guidelines/

Meta-guidance for authoring and maintaining Claude config artifacts — rules that guide the creation and maintenance of rules, skills, agents, hooks, and other foundational artifacts.

## 📋 Contents

| File | Purpose | Type |
|------|---------|------|
| **authoring_rules.md** | Standards for rule creation: naming, structure, directory placement, testing, scope boundaries; children in `authoring_rules/` cover common mistakes and a hard-gates checklist | Instructional |
| **authoring_skills.md** | Standards for skill creation: naming, contract fields, structure, complexity scoring, testing, maturity levels | Instructional |

## 🎯 Why authoring_guidelines?

These rules guide the creation of other rules, skills, agents, and artifacts. They establish:
- **Consistent structure** across all config artifacts
- **Quality gates** before artifacts are proposed or finalized
- **Testing requirements** for enforcement artifacts
- **Maturity frameworks** for evaluating completeness and stability
- **Scope boundaries** to prevent feature creep and bloat

---

## 📐 Structure & Maturity

Authoring guidelines follow a **progressive maturity model**:

| Level | Artifact Status | Characteristics |
|-------|---|---|
| **Draft** | Speculative or one-time use | New concept; 5–8 evals; explores design space |
| **Tactical** | Battle-tested, recurring use | Solves real, recurring problem; 8–12 evals; used in 5+ sessions |
| **Strategic** | Core workflow, stable | Production-ready; 12+ evals; clear scope; <1 update/year |

---

## 🔗 Related

- **`01_essentials/`** — Foundational rules applied every session (guiding principles, behaviour, security, testing)
- **`02_claude_standards/`** — Quality gates and operational standards (behaviour, git, testing, security guardrails)
- **`04_claude_reference/`** — System knowledge and reference docs (design patterns, efficiency, MCP trust model)
- **`05_lazy_load/`** — Domain-specific rules (SQL, Airflow, Terraform, etc.); loaded on-demand only

---

---

## 🔗 Related rules

Parent, sibling and dependency links for each file in this tier — kept here, not in the file, because READMEs aren't `@import`ed (#121).

### `_claude_config_metadata.md`

- `authoring_rules.md` — imports this file; rule template at `~/.claude/_templates/RULE.md.template`
- `authoring_skills.md`, `05_lazy_load/authoring_agents.md` — apply the placement above
- `_complexity_scoring.md` — sibling shared standard, same "define once" pattern

### `_complexity_scoring.md`

- `authoring_skills.md` — skill maturity gates and quality scorecard, applying the raw sum and inverted score respectively
- `05_lazy_load/authoring_agents.md` — agent maturity gates, same raw-sum convention as skills
- `testing.md` — test complexity scoring, applying the inverted score
- `authoring_rules.md` — rule authoring; no complexity gate defined yet
- `authoring_skills/_hard_gates_checklist.md` and equivalents — where a domain's specific gate thresholds live once defined

### `authoring_rules/_common_mistakes.md`

- Parent: `authoring_rules.md` — pre-creation checklist, creation steps and quality gates
- Sibling: `_hard_gates_checklist.md` — the tick-box check to run before finishing a rule

### `authoring_rules/_hard_gates_checklist.md`

- Parent: `authoring_rules.md` — pre-creation checklist, creation steps and quality gates
- Sibling: `_common_mistakes.md` — the mistakes these gates are designed to catch

### `authoring_rules.md`

**Naming & placement:**
- `naming_standards.md` — self-describing, unambiguous naming principles; see children for directory structure and object patterns
- `~/.claude/_rules/04_claude_reference/claude_rule_loading_strategy.md` — full rule list; duplication detection + always-on vs. lazy-load placement

**Authoring & testing:**
- `~/.claude/_templates/RULE.md.template` — two templates (principle-based vs. constraint-based)
- `testing.md` — when tests are required; enforcement rules always need tests
- `_complexity_scoring.md` (sibling file) — shared complexity formula; no maturity/complexity gate is defined for rules yet, but reference this rather than inventing a new formula if one is added
- `_rules/quality_scorecards/README.md` — quality scorecard template and per-dimension criteria for rules

**Principles & maintenance:**
- `guiding_principles.md` — intentionality principle; evidence-gathering methods; review cadence (reset every ~6 months per Boris Cherny)
- `behaviour.md` — includes decision-making as child file (_decision_making.md); when to present options vs. decide unilaterally

### `authoring_skills/_core_standards.md`

- Parent: `authoring_skills.md` — child index and file organisation
- Sibling: `_trigger_design.md` — trigger phrase design

### `authoring_skills/_hard_gates_checklist.md`

- Parent: `authoring_skills.md` — child index and file organisation
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields, maturity levels

### `authoring_skills/_no_orphaned_files.md`

- Parent: `authoring_skills.md` — child index and file organisation
- `guiding_principles.md` — "Reversible by design" and "no speculative work" — the same reasoning this rule mechanizes for skill files specifically

### `authoring_skills/_scope_and_maintenance.md`

- Parent: `authoring_skills.md` — child index and file organisation

### `authoring_skills/_trigger_design.md`

- Parent: `authoring_skills.md` — child index and file organisation
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields, maturity levels
- Sibling: `_hard_gates_checklist.md` — evals.yaml, scorecard and reference-file requirements

### `authoring_skills.md`

- **naming_standards.md** — Foundational naming principles; skill naming patterns in child file
- **testing.md** — Skill testing requirements by maturity level
- **authoring_rules.md** — General rule authoring process (complementary to skill authoring)
- **_complexity_scoring.md** (sibling file) — shared complexity formula this file's maturity gates and quality-scorecard dimension both draw from
