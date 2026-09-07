# 🛠️ Agent Authoring

**Purpose:** Establish standardized process for creating agents that ensures clarity, consistency, and intentionality. One concept per agent.

---

## 🧭 Quick Navigation

**New agent author?** Start here in order:
1. **Core Standards** — Naming pattern, structure, maturity levels, testing requirements
2. **Decision Tree** — When to create an agent vs. rule vs. skill
3. **5-Step Creation Process** — Workflow: name → contract → AGENT.md → evals → score
4. **Hard Gates Checklist** — Final validation before finalizing

**Experienced author, need to refresh?** Jump to specific sections:
- **Scope Boundaries** — Defining what your agent does NOT do
- **Maturity Justification** — Choosing Draft vs. Tactical vs. Strategic
- **Low-Maintenance Design** — Preventing agent bloat and scope creep

**Reviewing someone else's agent?** Use these sections:
- **Hard Gates Checklist** — Verify completeness
- **Common Mistakes** — Catch anti-patterns
- **Maturity Justification** — Verify evidence-based maturity

---

## 📐 Core Standards

Every agent follows these baseline standards.

### 5-Section Structure at a Glance

```
┌─ Frontmatter (metadata)
├─ Purpose (one-liner value prop)
├─ When to use (scenarios + NOT use cases)
├─ Role & Principles (persona + 5-7 behavioral guidelines)
└─ Constraints (what it does NOT do + limitations)
```

### Naming Pattern

- Format: `<domain>_<purpose>` (lowercase, snake_case)
- Domain: primary area of expertise (e.g., `technical_writer`, `architect`, `code_reviewer`)
- Purpose: specific function the agent serves
- Examples: `technical_writer`, `architect`, `code_analyzer`, `design_reviewer`
- Hard rule: Naming must be self-describing — unambiguous without context

### Directory Structure

- **Location:** `~/.claude/agents/core/` or organized by domain (flexible for now)
- **Filename:** `<domain>_<purpose>.md`
- **Example:** `~/.claude/agents/core/technical_writer.md`

### Agent Frontmatter [REQUIRED]

```yaml
---
name: <domain>_<purpose>
description: One-sentence value prop, user-focused
version: 0.1.0
maturity: draft  # draft | tactical | strategic
triggers:
  - /agent_name
  - "invoke agent_name"
model: inherit
isolation: worktree
---
```

**Frontmatter fields explained:**
- `name` — identifier matching `<domain>_<purpose>` pattern
- `description` — one sentence, what does this agent do for users?
- `version` — semantic versioning (0.x = draft, 1.x = tactical, 2.x = strategic)
- `maturity` — draft | tactical | strategic (same as skills)
- `triggers` — how users invoke this agent (slash command + natural language variants)
- `model` — `inherit` (use active model) or specific model override
- `isolation` — `worktree` (recommended for agents that modify files) or none

### 5-Section Structure [REQUIRED]

All agents follow this structure (lean, end-user readable, Claude-operable):

1. **Purpose** — One-liner value prop + why it matters (2-3 sentences max)
2. **When to use** — Concrete scenarios where agent is invoked + NOT used
3. **Role & Principles** — Persona Claude adopts + behavioral guidelines (5-7 principles max)
4. **Constraints** — What agent does NOT do + limitations (tool requirements, isolation mode, etc.)
5. **[Optional] References** — Links to supporting documentation

See `AGENT.md.template` for detailed structure guidance.

### Maturity Levels [REQUIRED]

Agents follow the same maturity model as skills:

| Level | Evidence | Test Count | Use Case |
|-------|----------|-----------|----------|
| **Draft** | Speculative or one-time use | 5–8 evals | Exploring new agent concept |
| **Tactical** | Recurring problem, battle-tested | 8–12 evals | Actively used in workflows |
| **Strategic** | Core workflow, heavy use | 12+ evals | Production-critical agent |

**Maturity justification [REQUIRED]:** Document in agent why you chose this maturity level, with evidence (usage frequency, test coverage, dependencies, scope clarity).

### Testing [REQUIRED]

**evals.yaml [REQUIRED]** — THE standard testing approach
- Format: each eval has `name`, `description`, `input`, `setup`, `expected_output`
- Organization: by scenario/feature (e.g., "PR drafting", "Confluence page creation")
- Coverage: happy paths, error cases, edge cases, agent behavior under different contexts
- Count by maturity: **Draft 5–8** | **Tactical 8–12** | **Strategic 12+**

**Agent behavioral tests validate:**
- Agent adopts correct persona
- Agent follows documented principles
- Agent produces expected output format
- Agent respects constraints and scope boundaries
- Agent handles errors gracefully

---

## 🎯 Rule vs. Skill vs. Agent Decision Tree

Use this tree to decide what to create:

```
Is this guidance Claude reads and follows?
├─ YES → RULE (behaviour patterns, standards, principles)
│   └ Example: security.md, naming_standards.md, writing_style.md
│
└─ NO → Continue

Is this a user-invoked multi-step workflow?
├─ YES → SKILL (user-facing, slash-command invoked)
│   └ Example: git_create_pr, confluence_create_page, jira_create
│
└─ NO → Continue

Is this a persona/role Claude adopts when working?
├─ YES → AGENT (system prompt, invoked via subagent_type)
│   └ Example: technical_writer, architect, code_reviewer
│
└─ NO → Reconsider your approach
```

**Key distinction:**
- **Rule:** Claude reads it and changes behavior
- **Skill:** User invokes it and Claude executes steps
- **Agent:** Claude adopts a persona/role (internal system prompt)

---

## 🚫 When NOT to create an agent

Do NOT create an agent if:
- **Use case is simpler as a rule** — e.g., "always use scannability in writing" belongs in writing_style.md, not an agent
- **Use case is simpler as a skill** — e.g., "create a Confluence page" is a user workflow (skill), not just a persona (agent)
- **Agent duplicates existing functionality** — check existing agents first; extend or combine instead
- **Scope is too narrow** — agent does only one trivial thing (e.g., "capitalize titles"); likely a rule or skill instead
- **Scope is aspirational** — "might use this eventually"; create only for recurring, observed problems

**Acid test:** If you can't name 3+ concrete scenarios where this agent would be invoked, create a rule or skill instead.

---

## 🚀 Create an Agent (5 Steps)

1. **Name it:** `<domain>_<purpose>` format, self-describing
2. **Define frontmatter:** name, description, version, maturity, triggers, model, isolation
3. **Write AGENT.md** using 5-section structure (Purpose → When to use → Role & Principles → Constraints)
4. **Create evals.yaml** with 8–12 test scenarios (by maturity level)
5. **Document maturity:** Justify maturity level with evidence in agent file

---

## 🚪 Scope Boundaries [REQUIRED]

Every agent must explicitly declare what it does NOT do. This prevents feature creep and sets expectations.

**In Constraints section, use:**

```markdown
## Constraints

This agent:
- Does NOT [boundary 1] (why: prevents scope creep / technical limitation / future enhancement)
- Does NOT [boundary 2]
- Works in [isolation mode]
- Uses [model] model
- Requires [specific tools, if any]
```

**Example (technical_writer):**
```markdown
This agent:
- Does NOT write ADRs or runbooks (v1.0)
- Does NOT improve existing documentation (separate concern)
- Does NOT provide diagram guidance or architecture visualization (v1.0)
- Works in worktree isolation
- Inherits active Claude model
```

**Anti-patterns:**
- ❌ Empty Constraints section (undefined scope leads to feature creep)
- ❌ Vague boundaries ("handles documentation" without saying what it doesn't)
- ❌ Aspirational scope ("will eventually support X") without v2.0 documentation

---

## 📈 Maturity Justification [REQUIRED]

Document why you chose this maturity level, with evidence.

**Format:**
```markdown
## Maturity Justification

**Real problem solved:** [What recurring user need does this agent address?]

**Use frequency:** [How often is this used? Across how many sessions?]

**Test coverage:** [# evals total; what's covered]

**Dependency assessment:** [Battle-tested tools? Experimental?]

**Scope assessment:** [Clear boundaries? Stable for v1.0?]

**Conclusion:** This agent justifies [Draft|Tactical|Strategic] maturity because:
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]
```

---

## ✅ Hard Gates Checklist

Before finalizing an agent, verify ALL of these:

### Naming & Structure
- [ ] Name follows `<domain>_<purpose>` pattern, self-describing
- [ ] Frontmatter complete: name, description, version, maturity, triggers, model, isolation
- [ ] 5-section structure: Purpose, When to use, Role & Principles, Constraints, [References]
- [ ] Total length ~40-60 lines (lean, scannable)

### Content Quality
- [ ] Purpose: one-liner + brief value prop (2-3 sentences max)
- [ ] When to use: concrete scenarios + NOT use cases
- [ ] Role & Principles: persona + 5-7 core principles
- [ ] Constraints: explicit scope boundaries (what agent does NOT do)
- [ ] All sections use bold keywords (`**Principle:**`, `**Constraint:**`)
- [ ] No jargon or unnecessarily complex language

### Testing & Maturity
- [ ] evals.yaml exists with correct count (Draft 5-8, Tactical 8-12, Strategic 12+)
- [ ] Each eval: name, description, input, setup, expected_output
- [ ] Maturity justified with evidence (problem, frequency, test coverage, dependencies, scope)
- [ ] Maturity level justified (Draft ≤4, Tactical ≤6, Strategic ≤8 complexity)

### Scope & Boundaries
- [ ] Constraints section is explicit and complete (what it does NOT do)
- [ ] Rationale documented (why these boundaries exist)
- [ ] No aspirational features in v1.0 (document for v2.0 separately)

### Integration & Documentation
- [ ] Agent placed in correct directory (agents/core/ or domain-organized)
- [ ] Triggers defined (slash command + natural language variants)
- [ ] Model and isolation mode specified
- [ ] References or related rules linked (if applicable)

---

## 🚫 Common Mistakes & Anti-Patterns

### ❌ **Over-scoping the persona**

**Wrong:**
```markdown
## Role
You are a technical writer with expertise in distributed systems, microservices, cloud-native architecture, 
container orchestration, and API design. You have deep knowledge of Kubernetes, Docker, and infrastructure. 
You write for both engineers and business stakeholders...
```

**Right:**
```markdown
## Role
You are a clear, precise technical writer. You produce documentation suited to your audience, adjusting tone 
and depth accordingly between engineers and non-technical stakeholders.
```

---

### ❌ **Vague scope boundaries**

**Wrong:**
```markdown
## Constraints
This agent handles all documentation tasks and adapts as needed.
```

**Right:**
```markdown
## Constraints
This agent:
- Does NOT write ADRs or runbooks (v1.0)
- Does NOT improve existing documentation (separate concern)
- Does NOT provide diagram guidance (v1.0)
```

---

### ❌ **Too many principles**

**Wrong:** 15+ principles trying to capture every possible behavior.

**Right:** 5-7 core principles that guide decision-making. More detail in reference files if needed.

---

### ❌ **Ad-hoc tests instead of evals.yaml**

**Wrong:** Create custom test scripts (`test_agent_name.py`) instead of using evals.yaml standard.

**Right:** Use evals.yaml with structured scenarios; keep testing consistent across all agents.

---

### ❌ **Maturity without evidence**

**Wrong:**
```markdown
## Maturity Justification
Strategic maturity because this is a cool idea and could be very useful.
```

**Right:**
```markdown
## Maturity Justification
Tactical maturity because:
- Solves recurring problem (used in 60% of sessions)
- Battle-tested in git_create_pr and confluence_create_page skills
- 12 evals cover all phases (PR body drafting, Confluence creation, error cases)
- Stable external dependencies (GitHub API, Atlassian API)
```

---

## 📚 References & Related Rules

**Naming & placement:**
- `naming_standards.md` — Self-describing naming principles
- `~/.claude/_rules/01_essentials/claude_usage_standards/_claude_directory_structure.md` — Directory organization patterns

**Authoring & testing:**
- `~/.claude/_templates/AGENT.md.template` — Agent template with examples
- `testing.md` — When tests are required; evals.yaml patterns

**Principles & maintenance:**
- `guiding_principles.md` — Intentionality principle; evidence-gathering methods
- `behaviour.md` — Safe defaults and decision-making patterns
- `_multi_phase_implementation_gates.md` — Review/approval gates during implementation

**Related agent standards:**
- `authoring_rules.md` — Rule creation standards (model for some agent patterns)
- `authoring_skills.md` — Skill creation standards (model for maturity levels, testing)

---

## 🔗 Related rules

- `behaviour.md` → `_multi_phase_implementation_gates.md` — Review gates after each implementation phase
- `guiding_principles.md` — Intentionality; when to create new agents vs. enhance existing ones
- `testing.md` — Testing requirements for all artifacts including agents
