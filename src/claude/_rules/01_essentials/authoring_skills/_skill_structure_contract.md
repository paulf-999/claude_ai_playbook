# 📐 Structure & Contract

**Purpose:** Define SKILL.md structure and skill.contract.yaml fields required for all skills.

---

## SKILL.md Canonical Structure: 5-Section Ultra-Lean

All SKILL.md files use a **5-section ultra-lean structure (~50–60 lines)**. This pattern prioritizes scannability: skill overview + example + guidance in the main file; implementation detail + formats + quality rationale externalized to `reference/` subdirectory.

**Core principle:** If SKILL.md exceeds 60 lines, the detail belongs in `reference/`, not in the main file.

### The 5 Sections

1. **Frontmatter** (3 lines) — name, version, maturity, description, tags
2. **Purpose** (3–4 bullets) — what it does + key capabilities (non-technical)
3. **Example Usage** (10–15 lines) — realistic user journey end-to-end
4. **Best For** (4–6 bullets) — use cases + explicit caveats (when NOT to use)
5. **References** (2–3 lines) — links to reference/_*.md files

**Total: 50–60 lines. No other sections.**

**If you need more, detail belongs in `reference/` subdirectory.**

---

## What Goes Where

| Content | SKILL.md? | reference/ file? |
|---------|-----------|-----------------|
| Purpose & capabilities | ✅ Yes (3–4 bullets) | ❌ No |
| Example user journey | ✅ Yes (realistic scenario) | ❌ No |
| Prerequisites & dependencies | ✅ Yes (brief) | ✅ reference/_implementation.md (detail) |
| Error handling & recovery | ❌ No | ✅ reference/_implementation.md |
| Validation rules & formats | ❌ No | ✅ reference/_formats.md |
| Quality scorecard & design rationale | ❌ No | ✅ reference/_quality_scorecard.md |
| Phases & workflow logic | ❌ No | ✅ reference/_implementation.md |

---

## Template Structure

Use `~/.claude/_templates/skills/SKILL.md.template` as starting point. The template shows:
- Frontmatter with all required fields
- 5-section body with inline examples
- Bold keywords on every bullet
- Reference links to reference/ subdirectory

**Do not extend the template.** If content doesn't fit the 5 sections, it belongs in reference/.

---

## skill.contract.yaml Contract Fields

Use `~/.claude/_templates/skills/skill.contract.yaml.template` as your starting point. It contains all required fields with detailed inline comments explaining purpose and examples for each one.

**Key fields:**

- **name** — Skill identifier (must match `<domain>_<action>` format)
- **version** — Semantic versioning (0.x = draft, 1.x = tactical, 2.x = strategic)
- **maturity** — draft, tactical, or strategic
- **dispatch.triggers** — When is this skill invoked? (slash command, phrase trigger, etc.)
- **dispatch.not_for** — Explicit scope boundaries (what skill does NOT do) — **MOST IMPORTANT FIELD**
- **requires** — Tools, resources, permissions needed
- **output** — Type (conversational, asynchronous, etc.), confirmation required, reversible
- **dependencies** — External APIs or systems accessed

