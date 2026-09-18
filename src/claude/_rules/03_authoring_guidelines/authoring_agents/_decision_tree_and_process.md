# 🎯 Agent Decision Tree & Creation Process

**Purpose:** Decide whether to build a rule, skill, or agent; know when NOT to create an agent at all; and the 5-step process once you've decided to.

---

## Rule vs. Skill vs. Agent Decision Tree

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

## 🚫 When NOT to create an agent

Do NOT create an agent if:
- **Use case is simpler as a rule** — e.g., "always use scannability in writing" belongs in writing_style.md, not an agent
- **Use case is simpler as a skill** — e.g., "create a Confluence page" is a user workflow (skill), not just a persona (agent)
- **Agent duplicates existing functionality** — check existing agents first; extend or combine instead
- **Scope is too narrow** — agent does only one trivial thing (e.g., "capitalize titles"); likely a rule or skill instead
- **Scope is aspirational** — "might use this eventually"; create only for recurring, observed problems

**Acid test:** If you can't name 3+ concrete scenarios where this agent would be invoked, create a rule or skill instead.

## 🚀 Create an Agent (5 Steps)

1. **Name it:** `<domain>_<purpose>` format, self-describing
2. **Define frontmatter:** name, description, version, maturity, triggers, model, isolation
3. **Write AGENT.md** using 5-section structure (Purpose → When to use → Role & Principles → Constraints)
4. **Create evals.yaml** with 8–12 test scenarios (by maturity level)
5. **Document maturity:** Justify maturity level with evidence in agent file

---

## 🔗 Related

- Parent: `authoring_agents.md` — quick navigation and hard gates checklist
