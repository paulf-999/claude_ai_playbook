# 📐 Rule Directory Tier Classification

**Purpose:** Explain how Claude rules are organized into four directory tiers (01_essentials through 04_lazy_load), each representing a distinct purpose and scope. Tier assignment determines loading strategy (always-on import vs. lazy-loaded on-demand).

**Scope:** Rules in `~/.claude/_rules/` are organized into four tiers. Directory placement determines whether a rule is always-on (imported in CLAUDE.md) or lazy-loaded (in `_rules/04_lazy_load/`), and defines the rule's scope and application.

---

## 📜 Historical Note

This document replaces the prior five-tier classification system (Tier 1–5) with a four-tier directory-based structure implemented in the Q3 2026 config reorganization. The new structure aligns tiers directly with directory organization for clarity and maintainability.

---

## 📁 Tier 1: `01_essentials/` — User-Facing & Foundational

**Definition:** Foundational decision-making principles and user-facing conventions that apply to every session and every user contribution.

**Characteristics:**
- Foundational principles governing all decisions (intentionality, explicitness, context efficiency)
- User-facing conventions (naming, writing style, authoring standards)
- User-facing quality requirements (secure coding practices, test requirements)
- Applies to every session and every task
- Cost of omission: confused user experience, quality decay, or violated conventions

**Examples:**
- `guiding_principles.md` — Foundational meta-principles: intentionality, explicitness, context efficiency
- `naming_standards.md` — Self-describing naming conventions for all identifiers
- `authoring_skills.md` — User-facing standards for skill creation and structure
- `authoring_rules.md` — User-facing standards for rule creation and testing
- `writing_style.md` — Content presentation standards (emojis, bullets, clarity)
- `security.md` — Secure coding practices (secrets, auth, input validation)
- `testing.md` — Test requirements: write tests for all new features

**Loading:** Always-on (imported in CLAUDE.md) — foundational to every session.

---

## ⚙️ Tier 2: `02_claude_standards/` — Blocking Standards & Enforcement

**Definition:** Rules that enforce quality gates, operational standards, secure coding practices, and structural standards. Blocking rules for code quality, system stability, and safe operational conduct.

**Characteristics:**
- Blocking operational standards (safe conduct, decision-making, preventing unsafe actions)
- Mechanical enforcement rules (testing, security, naming validation)
- Gates new features, rules, and abstractions
- Applies to every session, every code addition, and every operational decision
- High cost of violation: quality decay, security vulnerabilities, scope creep, **safety regression**
- Often paired with tests and hooks for automated enforcement

**Examples:**
- `behaviour.md` — Safety-critical operational conduct (ask before risky operations, investigate state before deletion)
- `security.md` — Secure coding guardrails and Claude's conduct (prevent prompt injection, secret exposure)
- `testing.md` — Requires tests for all new features and enforcement rules

**Loading:** Always-on — blocking rules must apply universally to enforce standards and ensure safe conduct.

---

## 📚 Tier 3: `03_claude_reference/` — System Knowledge & Platform Guidance

**Definition:** Meta-knowledge about how Claude Code and the config system work. Reference material for operational decisions, architectural understanding, and platform-specific behavior.

**Characteristics:**
- Technical/meta-knowledge about Claude Code operation (efficiency, git workflow, MCP trust)
- Platform-specific guidance (how to use tools, when to load rules, external system access)
- Applies during specific activities (git work, tool use, config decisions)
- Not blocking — Claude reads and follows when relevant
- Candidate for lazy-loading if usage data supports it

**Examples:**
- `claude_efficiency.md` — Token efficiency, sub-agent constraints, model selection
- `git.md` — Git workflow patterns, commit format, branch naming, PR standards
- `external_system_access.md` — Check tool availability before claiming inaccessibility
- `loading_strategy_rules.md` — Decision tree for rule placement (always-on vs. lazy-load)
- `mcp_server_toggling.md` — Operational guidance on MCP server toggling
- `task_request_conventions.md` — Behavioral patterns for user request types

**Loading:** Mostly always-on (high session coverage for git and efficiency guidance), but some are lazy-load candidates. See `loading_strategy_rules.md` for individual loading decisions.

---

## 🎯 Tier 4: `04_lazy_load/` — Domain-Specific & Niche

**Definition:** Domain-specific style guides, tools, and specialized guidance. Loaded on-demand only when actively needed.

**Characteristics:**
- Solves real, recurring problems in specific domains (SQL, Airflow, dbt, Terraform, etc.)
- Not applicable to every session — only when working in that domain
- Reduces baseline token cost by lazy-loading
- Candidate for lazy-loading by design

**Examples:**
- `style_guide_standards/sql.md` — SQL formatting and SQLFluff standards
- `style_guide_standards/airflow.md` — Airflow DAG conventions
- `style_guide_standards/dbt.md` — dbt model structure and layer patterns
- `automation_controls.md` — Advanced automation features (`/batch`, `/goal`, `/loop`)

**Loading:** Lazy-loaded (in `_rules/04_lazy_load/`) — loaded on-demand only when actively needed. Do not import in baseline CLAUDE.md.

---

## 📊 Distribution Summary

| Tier | Directory | Count | Scope | Loading |
|---|---|---|---|---|
| **1** | `01_essentials/` | 6–8 | User-facing conventions, foundational principles | Always-on (non-negotiable) |
| **2** | `02_claude_standards/` | 6–8 | Blocking standards, enforcement, operational conduct | Always-on (non-negotiable) |
| **3** | `03_claude_reference/` | 8–10 | System knowledge, platform guidance, architecture | Mostly always-on; some candidates for lazy-load |
| **4** | `04_lazy_load/` | 10+ | Domain-specific style guides, niche tools | Lazy-loaded (on-demand only) |

---

## 🔄 Loading Decision Framework

**Always-on (imported in CLAUDE.md):**
- Safety-critical (behaviour, guiding_principles)
- Quality gates (testing, security)
- High session coverage (>70%)
- Foundational for all work (naming, writing style)

**Lazy-load (in `04_lazy_load/`):**
- Domain-specific (style guides for SQL, Airflow, dbt, etc.)
- Session coverage <70%
- Clear trigger (command invocation, tool use)
- No safety cost if omitted in irrelevant sessions

**See also:** `claude_rule_loading_strategy.md` for detailed always-on vs. lazy-load decision tree.

---

## 🔗 Related References

- **Loading strategy decision tree:** `claude_rule_loading_strategy.md` — Authoritative guide for always-on vs. lazy-load placement
- **Rule registries:** `claude_rule_loading_strategy.md` (parent index) + children files (`_always_on_rules.md`, `_lazy_loaded_rules.md`)
- **Tier-specific guidance:**
  - `01_essentials/` — Foundational rules (safety, user-facing, quality)
  - `02_claude_standards/` — Standard enforcement and quality gates
  - `03_claude_reference/` — This directory; system knowledge and platform guidance
  - `04_lazy_load/` — Domain-specific rules (load on-demand)
