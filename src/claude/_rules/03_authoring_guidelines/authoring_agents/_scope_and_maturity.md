# 🚪 Agent Scope Boundaries & Maturity Justification

**Purpose:** Every agent must declare what it does NOT do, and justify its maturity level with evidence, not aspiration.

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

## 🔗 Related

- Parent: `authoring_agents.md` — quick navigation and hard gates checklist
