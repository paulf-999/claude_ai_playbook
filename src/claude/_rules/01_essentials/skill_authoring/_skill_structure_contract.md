# 📐 Structure & Contract

**Purpose:** Define SKILL.md structure and skill.contract.yaml fields required for all skills.

---

## SKILL.md Canonical Structure

All SKILL.md files use a canonical 8-section structure (~110 lines). **Use the template file as your starting point:** `~/.claude/_templates/skills/SKILL.md.template`.

**When creating a skill via `/skill_creator`**, the template is copied automatically. It contains:

1. **Frontmatter** — skill metadata (name, version, maturity, summary)
2. **Overview** — one plain-language sentence: "What is this?"
3. **Quality Scorecard** — dimensions (Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards, Overall)
4. **Scope** — what's allowed by maturity level (draft/tactical/strategic)
5. **Capabilities** — what it can and can't do
6. **Security** — data handling, access, reversibility
7. **Prerequisites** — what the user needs
8. **Workflow** — phases and steps
9. **Error Recovery** — failure modes and fixes
10. **Known Gaps** — limitations and roadmap

The template shows all sections with placeholder content and inline examples. **Do not copy the template structure into documentation** — the template file is the source of truth.

---

## skill.contract.yaml Contract Fields

Use `~/.claude/_templates/skills/skill.contract.yaml.template` as your starting point. It contains all required fields with detailed inline comments explaining purpose and examples for each one.
