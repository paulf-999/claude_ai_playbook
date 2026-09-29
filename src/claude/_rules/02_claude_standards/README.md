# 02_claude_standards

**Purpose:** Blocking standards and enforcement rules that Claude must apply to all work — ensuring code quality, system stability, and safe operational conduct.

**Scope:** Foundational blocking rules applied universally. Includes both operational conduct (safe defaults, decision-making) and quality/security gates. Claude-facing guidance, not user-facing conventions.

---

## How to use

Import rules from this tier in `~/.claude/CLAUDE.md` when they are:
1. **Blocking** — prevent unsafe actions, quality decay, or security vulnerabilities
2. **Foundational** — apply to every session and every operational decision
3. **Universal** — no exceptions or conditional application
4. **High cost of violation** — safety regression, data loss, or systemic quality issues

Rules in this tier cost ≈20k tokens every session together and must justify their baseline presence through frequency and impact.

---

## Files in this tier

| File | Purpose |
|---|---|
| **behaviour.md** | Safe operational conduct — ask before risky operations, investigate state before deletion, intentional action |
| **security.md** | Secure coding standards (secrets, auth, input validation) + Claude's conduct (prompt injection defence) |
| **testing.md** | Requirements and patterns for test creation; all code artifacts must be tested |

---

## Child file organization

- **`behaviour/`** — Child files covering decision-making and artefact proposal gates
- **`git/`** — Child files covering safe git patterns, commits, and pull requests
- **`testing/`** — Child files covering test design patterns, anti-patterns, maintenance, and the test metadata/scoring standard

---

## When to add new rules

Add to this tier only when:
- The rule is **blocking** (prevents unsafe action or quality decay)
- It applies to **every session and every operational decision**
- The token cost is justified by **safety-critical** or **quality-critical** impact
- It establishes **universal standards** with no exceptions

Otherwise, place in:
- **01_essentials/** — user-facing conventions (naming, writing, authoring)
- **04_claude_reference/** — system/meta knowledge about how the config works
- **05_lazy_load/** — domain-specific, load on-demand only

---

## Related

- **01_essentials/** — User-facing principles and conventions (guiding_principles, authoring, naming, writing)
- **04_claude_reference/** — System knowledge and reference material (git, efficiency, external systems)
- **05_lazy_load/** — Domain-specific rules (lazy-loaded)

---

## 🔗 Related rules

Parent, sibling and dependency links for each file in this tier — kept here, not in the file, because READMEs aren't `@import`ed (#121).

### `behaviour/_artefact_proposal_gates.md`

- Parent: `behaviour.md` — Safe defaults and safe action guidelines
- Sibling: `_decision_making.md` — When to present options vs. decide unilaterally; gates should pass before options are presented
- Reference: `naming_standards.md`, `claude_directory_structure.md`, `~/.claude/_rules/04_claude_reference/claude_rule_loading_strategy.md`

### `behaviour/_before_acting.md`

- Parent: `behaviour.md` — safe defaults and safe action patterns
- Sibling: `_artefact_proposal_gates.md` — validating proposals before presenting them
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally

### `behaviour/_decision_making.md`

- `guiding_principles.md` — Intentionality principle; decide before proceeding
- Parent: `behaviour.md` — Safe defaults and safe action guidelines; decision-making is one aspect
- `writing_style.md` — Clarity principles; progressive disclosure

### `behaviour/_how_to_approach.md`

- Parent: `behaviour.md` — safe action defaults; decision-making patterns

### `behaviour/_model_selection_strategy.md`

- Parent: `behaviour.md` — safe defaults and decision-making patterns
- Reference: `claude_operational_efficiency.md` — context management principles (related but separate concern)

### `behaviour/_pre_existing_issue_disclosure.md`

- Parent: `behaviour.md` — safe action defaults; decision-making patterns
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally
- Sibling: `claude_plans.md` — phase reports are a natural place to disclose findings

### `behaviour/_session_conduct.md`

- Parent: `behaviour.md` — safe defaults and decision-making patterns
- Sibling: `_model_selection_strategy.md` — when to escalate models
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally

### `behaviour.md`

- `guiding_principles.md` — Intentionality principle; decide before proceeding
- `decision_making.md` (child: `_decision_making.md`) — When to present options vs. decide unilaterally
- `claude_plans.md` — Sibling; phase gates, plan-mode rules, and plan-file format
- `writing_style.md` — Clarity principles; progressive disclosure

### `claude_plans/_plan_file_format.md`

- Parent: `_multi_phase_implementation_gates.md` — general phase-gate principle and chat-response format
- Sibling: `_plan_mode_phase_gates.md` — mandatory gating specifically in plan mode

### `claude_plans/_plan_mode_phase_gates.md`

- Parent: `claude_plans.md` — general phase-gate principle and chat-response format
- Sibling: `_plan_file_format.md` — how to format the persisted plan document itself

### `claude_plans.md`

- Sibling: `behaviour.md` — safe action defaults; decision-making patterns (see its child `_decision_making.md` for when to present options vs. decide unilaterally)
- Reference: `~/.claude/_rules/04_claude_reference/claude_operational_efficiency.md` — turn budgets, context preservation

### `git/_commits.md`

- Parent: `git.md` — safe patterns, branch naming, pull requests, complex operations

### `git/_concurrent_sessions.md`

- Parent: `git.md` — git workflow, commits, branch naming, pull requests
- Sibling: `_safe_patterns.md` — hook-execution risk in untrusted repos
- Sibling: `_commits.md` — stage-by-name, branch confirmation, logical commits
- `behaviour.md` — investigate unfamiliar state before overwriting or deleting

### `git/_safe_patterns.md`

- Parent: `git.md` — git workflow, commits, branch naming, pull requests

### `git.md`

- `testing.md` — test requirements and design patterns
- `behaviour.md` — safe action defaults and decision-making

### `portable_paths.md`

- `testing.md` — every hook and script needs a test; this rule is part of what "correct" looks like
- `authoring_rules.md` / `authoring_skills.md` — apply this when writing any new hook, test, or script

### `security/_code_security.md`

- Parent: `security.md` — security overview and guardrails
- Sibling: `_security_guardrails.md` — Claude's conduct and prompt injection defence
- Reference: `~/.claude/_reference/claude_design_patterns/_security.md` — security architecture

### `testing/_test_metadata.md`

- Parent: `testing.md` — When tests are required; test design pattern and gates
- `claude_plans.md` — Gate testing before merging
- `~/.claude/_tests/` — Location of all test files and metadata headers

### `testing/_test_metadata_complexity_scoring.md`

- Parent: `_test_metadata.md` — the quality-score rubric this complements
- `_complexity_scoring.md` (in `03_authoring_guidelines/`) — the shared formula this file applies

### `testing/_test_metadata_maintenance.md`

- Parent: `_test_metadata.md` — format and scoring definitions
- Sibling: `_test_metadata_complexity_scoring.md` — the complexity dimension referenced above
