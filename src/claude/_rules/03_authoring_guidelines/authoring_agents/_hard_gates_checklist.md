# ✅ Agent Hard Gates Checklist

**Purpose:** Final validation checklist before finalizing an agent — verify naming, content quality, testing, scope, and integration.

---

## Before finalizing an agent, verify ALL of these:

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

## 🔗 Related

- Parent: `authoring_agents.md` — quick navigation and core standards
