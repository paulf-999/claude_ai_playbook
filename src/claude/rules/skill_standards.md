# ✏️ Rules — Skill authoring standards

Apply these rules whenever writing a new skill or revising an existing one.

---

## 📏 File length

- `SKILL.md` must not exceed **100 lines**. Up to 110 lines is tolerated where the overage is incidental (e.g. a long frontmatter description or a single extra TODO line) — but not as a routine allowance.
- If a skill materially exceeds this limit, extract the largest phase or reference sections into child markdown files co-located in the skill directory (e.g. `phase1.md`, `parameters.md`) and reference them from `SKILL.md`.
- The parent `SKILL.md` describes the skill and references child pages — it does not contain all the content itself.

---

## 🗂️ Structure

Every `SKILL.md` must contain, in order:

1. **Frontmatter** — `name`, `description`, `version`, `maturity`, `tags` (criticality, status, tested), `tools`, `triggers`, `not_for`, `output`
2. **Scope gate** — the maturity table immediately after frontmatter
3. **Phase sections** — one section per major workflow phase; extract to child pages if long

---

## 🎯 Trigger and output contract — triggers, not_for, output

Structured frontmatter fields that make skill dispatch machine-readable. Required on all new and revised skills.

### Minimum (Option A — frontmatter only)

```yaml
triggers:
  explicit:                              # slash commands and exact phrases
    - /skill-name
    - "exact phrase"
  contextual:                            # situational conditions
    - user asks to do X
not_for:
  - when /other-skill is a better fit    # competing skill
  - condition where this skill misfires  # anti-trigger condition
output:
  type: conversational   # conversational | file | external_service | mixed
  confirmation_required: false           # true if irreversible or external actions
```

**Rules:**
- `description` must be a clean one-line summary — move all trigger phrases into `triggers`
- `triggers` should include all slash commands, exact phrases, and contextual conditions that should route to this skill
- `not_for` should call out the most likely routing mistakes — competing skills and edge cases
- `output.type` and `output.confirmation_required` are the minimum contract an orchestrator needs

### Extended (Option B — `skill_schema.yaml`)

A `skill_schema.yaml` file co-located alongside `SKILL.md` carries the full machine-readable contract. **Encouraged for all skills; not mandatory.** Authoritative over frontmatter fields if present.

See [`skills/skill_schema.yaml.template`](../skills/skill_schema.yaml.template) for the full schema.

Use Option B when the skill:
- Has external side effects (API calls, git operations, file writes)
- Requires MCP servers
- Has multiple trigger types that benefit from explicit/contextual split
- Needs a richer output contract (artifacts, side effects, required sections)

---

## 🚫 Negative constraints

Any skill phase that calls an external API or modifies a structured file must include at least one explicit "do not" statement covering its known failure modes. These belong inline in the phase step, not in a separate section.

Examples:
- `Do NOT include sprint field when creating sub-tasks.`
- `Do NOT modify the parent ticket.`
- `Do NOT add CODEOWNERS entries for paths that were not explicitly requested.`

If a skill has no known failure modes, no statement is required. Apply on new skills and when revising existing ones.

---

## 😀 Emojis

Use emojis on all major headings, table rows where appropriate, and callout blocks. They aid scannability and are consistent with the style of the rest of the playbook.

---

## 🚫 No hardcoded personal references

Do not hardcode the names of specific individuals (team members, managers, direct reports) anywhere in repo content — skills, templates, patterns, style guides, or rules.

Use generic terms instead:

| Instead of | Use |
|---|---|
| A person's first name | "Data Management team member(s)" |
| Named examples in templates | Placeholder text (e.g. `Sprint N`, `DM team member 1 / DM team member 2`) |

Personal context belongs in `~/.claude/memory/` — loaded at runtime, never committed.

---

## 🔗 Child page imports

When a phase or reference section is extracted to a child file, reference it clearly in `SKILL.md`:

```
See [Phase 1 — Workspace PR](phase1.md) for the full step sequence.
```

Do not leave the parent file pointing to a child page without any context — include a one-line summary of what the child page covers.
