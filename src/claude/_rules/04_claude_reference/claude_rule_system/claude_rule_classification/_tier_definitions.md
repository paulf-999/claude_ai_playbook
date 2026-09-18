# 📁 Tier Definitions

**Purpose:** Define each of the 5 directory tiers — what belongs there, why, and its loading strategy.

---

## 📁 Tier 1: `01_essentials/` — User-Facing & Foundational

**Definition:** Foundational decision-making principles and user-facing conventions that apply to every session and every user contribution.

**Characteristics:**
- Foundational principles governing all decisions (intentionality, explicitness, context efficiency)
- User-facing conventions (naming, writing style, response standards)
- Applies to every session and every task
- Cost of omission: confused user experience, quality decay, or violated conventions

**Examples:**
- `guiding_principles.md` — Foundational meta-principles: intentionality, explicitness, context efficiency
- `claude_usage_standards.md` — Entry point for naming, writing style, directory structure conventions
- `claude_response_standards.md` — Expected response format, delivery approach, timing

**Loading:** Always-on (imported in CLAUDE.md) — foundational to every session.

## ⚙️ Tier 2: `02_claude_standards/` — Blocking Standards & Enforcement

**Definition:** Rules that enforce quality gates, operational standards, secure coding practices, and structural standards. Blocking rules for code quality, system stability, and safe operational conduct.

**Characteristics:**
- Blocking operational standards (safe conduct, decision-making, preventing unsafe actions)
- Mechanical enforcement rules (testing, security, naming validation, portable paths)
- Gates new features, rules, and abstractions
- High cost of violation: quality decay, security vulnerabilities, scope creep, **safety regression**

**Examples:**
- `behaviour.md` — Safety-critical operational conduct (ask before risky operations, investigate state before deletion)
- `security.md` — Secure coding guardrails and Claude's conduct (prevent prompt injection, secret exposure)
- `testing.md` — Requires tests for all new features and enforcement rules
- `portable_paths.md` — No hardcoded local-filesystem assumptions in hooks or tests

**Loading:** Always-on — blocking rules must apply universally to enforce standards and ensure safe conduct.

## 🛠️ Tier 3: `03_authoring_guidelines/` — Meta-Guidance for Creating Artifacts

**Definition:** Standards for authoring the config's own artifacts — rules, skills, and agents.

**Characteristics:**
- User-facing standards for creating new rules, skills, and agents
- Applies whenever a new artifact is being authored, not every session's task work
- Cost of omission: inconsistent artifact structure, scope creep, missing test coverage

**Examples:**
- `authoring_rules.md` — Rule creation checklist, directory placement, testing requirements
- `authoring_skills.md` — Skill creation guide, complexity scoring, domain reference
- `authoring_agents.md` — Agent creation process, naming, maturity levels

**Loading:** Always-on — authoring standards must be consistently applied whenever new artifacts are created.

## 📚 Tier 4: `04_claude_reference/` — System Knowledge & Platform Guidance

**Definition:** Meta-knowledge about how Claude Code and the config system work. Reference material for operational decisions, architectural understanding, and platform-specific behavior.

**Characteristics:**
- Technical/meta-knowledge about Claude Code operation (efficiency, git workflow, MCP trust)
- Platform-specific guidance (how to use tools, when to load rules, external system access)
- Applies during specific activities (git work, tool use, config decisions)

**Examples:**
- `claude_operational_efficiency.md` — Token efficiency, sub-agent constraints, delegation
- `git.md` — Git workflow patterns, commit format, branch naming, PR standards
- `claude_rule_loading_strategy.md` — Decision tree for rule placement (always-on vs. lazy-load)
- `mcp_server_toggling.md` — Operational guidance on MCP server toggling

**Loading:** Mostly always-on (high session coverage for git and efficiency guidance), but some are lazy-load candidates.

## 🎯 Tier 5: `05_lazy_load/` — Domain-Specific & Niche

**Definition:** Domain-specific style guides, tools, and specialized guidance. Loaded on-demand only when actively needed.

**Characteristics:**
- Solves real, recurring problems in specific domains (SQL, Airflow, dbt, Terraform, etc.)
- Not applicable to every session — only when working in that domain
- Reduces baseline token cost by lazy-loading

**Examples:**
- `style_guide_standards/sql.md` — SQL formatting and SQLFluff standards
- `style_guide_standards/airflow.md` — Airflow DAG conventions
- `style_guide_standards/dbt.md` — dbt model structure and layer patterns
- `automation_controls.md` — Advanced automation features (`/batch`, `/goal`, `/loop`)

**Loading:** Lazy-loaded (in `_rules/05_lazy_load/`) — loaded on-demand only when actively needed. Never imported in baseline CLAUDE.md.

---

## 🔗 Related

- Parent: `claude_rule_classification.md` — distribution summary and loading decision framework
