<!-- version: 3.0.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# 🎯 Trigger Design

**Purpose:** Define how to design trigger phrases so a skill runs whenever users naturally ask for it.

---

## Trigger Design [REQUIRED]

Triggers determine how users invoke your skill. Comprehensive trigger coverage ensures the skill auto-invokes when users naturally ask for it, not just via explicit slash commands.

**Trigger Types**

- **Explicit triggers:** `/skill_name` slash commands and direct phrase matches
  - Format: `- /skill_name` or `- exact phrase`
  - Example: `/confluence_create_page`, `create a confluence page`
- **Contextual triggers:** Natural language patterns the system uses to detect user intent
  - Format: `- user wants to <action>`
  - Example: `user wants to create a Confluence page`

**Explicit triggers drive auto-invocation.** Contextual triggers are fallback guidance. Prioritize explicit phrase coverage.

**Designing phrase triggers:**
- **Verbs:** list every natural way to ask — e.g. "create", "make", "open", "submit" a PR.
- **Terminology:** include alternate names for the same concept — e.g. "pr", "pull request", "mr".
- **Case:** add both lowercase and uppercase variants — e.g. `create a pr` and `create a PR`.
- **Be exhaustive:** a false positive costs less than a missed invocation.
- **Not too generic:** "help" or "please" alone won't distinguish your skill from others.
- **Example:** see `git_create_pr`'s `skill.contract.yaml` for a complete trigger list.

---

## 🔗 Related

- Parent: `authoring_skills.md` — child index and file organisation
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields, maturity levels
- Sibling: `_hard_gates_checklist.md` — evals.yaml, scorecard and reference-file requirements
