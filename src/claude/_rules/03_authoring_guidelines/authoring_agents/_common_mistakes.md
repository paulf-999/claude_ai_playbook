# 🚫 Agent Common Mistakes & Anti-Patterns

**Purpose:** The most frequent agent-authoring mistakes, shown as wrong/right pairs.

---

## ❌ **Over-scoping the persona**

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

## ❌ **Vague scope boundaries**

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

## ❌ **Too many principles**

**Wrong:** 15+ principles trying to capture every possible behavior.

**Right:** 5-7 core principles that guide decision-making. More detail in reference files if needed.

---

## ❌ **Ad-hoc tests instead of evals.yaml**

**Wrong:** Create custom test scripts (`test_agent_name.py`) instead of using evals.yaml standard.

**Right:** Use evals.yaml with structured scenarios; keep testing consistent across all agents.

---

## ❌ **Maturity without evidence**

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

## 🔗 Related

- Parent: `authoring_agents.md` — quick navigation and hard gates checklist
