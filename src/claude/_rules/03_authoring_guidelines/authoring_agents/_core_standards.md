# 📐 Agent Core Standards

**Purpose:** The baseline every agent follows — 5-section structure, naming pattern, frontmatter fields, maturity levels, and testing requirements.

---

## 5-Section Structure at a Glance

```
┌─ Frontmatter (metadata)
├─ Purpose (one-liner value prop)
├─ When to use (scenarios + NOT use cases)
├─ Role & Principles (persona + 5-7 behavioral guidelines)
└─ Constraints (what it does NOT do + limitations)
```

## Naming Pattern

- Format: `<domain>_<purpose>` (lowercase, snake_case)
- Domain: primary area of expertise (e.g., `technical_writer`, `architect`, `code_reviewer`)
- Purpose: specific function the agent serves
- Examples: `technical_writer`, `architect`, `code_analyzer`, `design_reviewer`
- Hard rule: Naming must be self-describing — unambiguous without context

## Directory Structure

- **Location:** `~/.claude/agents/core/` or organized by domain (flexible for now)
- **Filename:** `<domain>_<purpose>.md`
- **Example:** `~/.claude/agents/core/technical_writer.md`

## Agent Frontmatter [REQUIRED]

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

## 5-Section Structure [REQUIRED]

All agents follow this structure (lean, end-user readable, Claude-operable):

1. **Purpose** — One-liner value prop + why it matters (2-3 sentences max)
2. **When to use** — Concrete scenarios where agent is invoked + NOT used
3. **Role & Principles** — Persona Claude adopts + behavioral guidelines (5-7 principles max)
4. **Constraints** — What agent does NOT do + limitations (tool requirements, isolation mode, etc.)
5. **[Optional] References** — Links to supporting documentation

See `AGENT.md.template` for detailed structure guidance.

## Maturity Levels [REQUIRED]

Agents follow the same maturity model as skills:

| Level | Evidence | Test Count | Use Case |
|-------|----------|-----------|----------|
| **Draft** | Speculative or one-time use | 5–8 evals | Exploring new agent concept |
| **Tactical** | Recurring problem, battle-tested | 8–12 evals | Actively used in workflows |
| **Strategic** | Core workflow, heavy use | 12+ evals | Production-critical agent |

**Maturity justification [REQUIRED]:** Document in agent why you chose this maturity level, with evidence (usage frequency, test coverage, dependencies, scope clarity).

## Testing [REQUIRED]

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

## 🔗 Related

- Parent: `authoring_agents.md` — quick navigation and hard gates checklist
