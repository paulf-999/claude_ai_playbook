# Phase 2: MoSCoW Prioritisation

## 🗂️ MoSCoW — what should exist

After scoring, produce a MoSCoW table evaluating the artefacts found (and any notable absences) against the following canonical list.

**Must have** — a global config without these is unsafe or unreliable:
- Behaviour rules with risky action gates
- Security coding standards
- Claude-conduct security guardrails (prompt injection, secret handling)
- Git rules (branch protection, commit format)
- Memory scoping rules
- Core Principles in CLAUDE.md
- Tests for enforcement hooks

**Should have** — important for quality and consistency:
- Writing style rules
- Naming standards (ideally hook-enforced)
- Efficiency rules (parallelism, sub-agent constraints, turn budgets)
- Populated MEMORY.md index
- Rule structural tests

**Could have** — worthwhile but low-priority:
- Lazy-load style guide standards
- Aliases for common phrases
- Config-specific naming conventions (lazy load)

**Want** — polish and completeness:
- MCP server trust model rule
- System-level architecture rationale document
- Git rule test coverage

**How to evaluate:**
- Assess presence, absence, and partial coverage of each artefact
- For each Must item absent, flag it as a **Must** recommendation
- Track which artefacts are present, absent, or partially covered
