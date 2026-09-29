<!-- version: 1.1.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# 📁 Tier Definitions

**Purpose:** Define each of the 5 directory tiers — what belongs there, why, and its loading strategy.

**Note:** each tier's directory is the current list of its rules — the single example per tier below is illustrative only.

---

## 📁 Tier 1: `01_essentials/` — User-Facing & Foundational

**Definition:** Foundational decision-making principles and user-facing conventions that apply to every session and every user contribution.

**Characteristics:**
- Foundational principles governing all decisions (intentionality, explicitness, context efficiency)
- User-facing conventions (naming, writing style, response standards)
- Applies to every session and every task
- Cost of omission: confused user experience, quality decay, or violated conventions
- **Example:** `guiding_principles.md` — foundational meta-principles: intentionality, explicitness, context efficiency

**Loading:** Always-on (imported in CLAUDE.md) — foundational to every session.

## ⚙️ Tier 2: `02_claude_standards/` — Blocking Standards & Enforcement

**Definition:** Rules that enforce quality gates, operational standards, secure coding practices, and structural standards. Blocking rules for code quality, system stability, and safe operational conduct.

**Characteristics:**
- Blocking operational standards (safe conduct, decision-making, preventing unsafe actions)
- Mechanical enforcement rules (testing, security, naming validation, portable paths)
- Gates new features, rules, and abstractions
- High cost of violation: quality decay, security vulnerabilities, scope creep, **safety regression**
- **Example:** `behaviour.md` — safety-critical operational conduct (ask before risky operations, investigate state before deletion)

**Loading:** Always-on — blocking rules must apply universally to enforce standards and ensure safe conduct.

## 🛠️ Tier 3: `03_authoring_guidelines/` — Meta-Guidance for Creating Artifacts

**Definition:** Standards for authoring the config's own artifacts — rules, skills, and agents.

**Characteristics:**
- User-facing standards for creating new rules, skills, and agents
- Applies whenever a new artifact is being authored, not every session's task work
- Cost of omission: inconsistent artifact structure, scope creep, missing test coverage
- **Example:** `authoring_rules.md` — rule creation checklist, directory placement, testing requirements

**Loading:** Always-on — authoring standards must be consistently applied whenever new artifacts are created.

## 📚 Tier 4: `04_claude_reference/` — System Knowledge & Platform Guidance

**Definition:** Meta-knowledge about how Claude Code and the config system work. Reference material for operational decisions, architectural understanding, and platform-specific behavior.

**Characteristics:**
- Technical/meta-knowledge about Claude Code operation (efficiency, delegation, turn budgets)
- Platform-specific guidance (how to use tools, when to load rules, external system access)
- Applies during specific activities (tool use, config decisions)
- **Example:** `claude_operational_efficiency.md` — token efficiency, sub-agent constraints, delegation

**Loading:** Mostly always-on (high session coverage for efficiency guidance), but some are lazy-load candidates.

## 🎯 Tier 5: `05_lazy_load/` — Domain-Specific & Niche

**Definition:** Domain-specific style guides, tools, and specialized guidance. Loaded on-demand only when actively needed.

**Characteristics:**
- Solves real, recurring problems in specific domains (SQL, Airflow, dbt, Terraform, etc.)
- Not applicable to every session — only when working in that domain
- Reduces baseline token cost by lazy-loading
- **Example:** `style_guide_standards/sql.md` — SQL formatting and SQLFluff standards

**Loading:** Lazy-loaded (in `_rules/05_lazy_load/`) — loaded on-demand only when actively needed. Never imported in baseline CLAUDE.md.

---

## 🔗 Related

- Parent: `_claude_rule_classification.md` — distribution summary and loading decision framework
