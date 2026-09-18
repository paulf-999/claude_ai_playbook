# 📐 Skill Core Standards

**Purpose:** Define the baseline every skill must follow — naming, SKILL.md's 5-section structure, and what `skill.contract.yaml` must declare.

---

## Naming Pattern

- Format: `<domain>_<action>` (lowercase, snake_case)
- Domain: must match valid domain ID from `skill_domains.yaml`
- Action: imperative verb describing what the skill does
- Examples: `confluence_create_page`, `jira_create`, `git_create_pr`, `claude_review_config`
- Hard rule: Directory prefix must match domain (e.g., `confluence_create_page` → `_confluence_skills/`)

## SKILL.md Structure [REQUIRED]

5-section canonical structure, ~60 lines, scannable in <2 minutes:
1. **Frontmatter** — name, description, version, maturity, tags
2. **Purpose** — 1 sentence value prop + 3–4 bullets of key capabilities
3. **Example Usage** — Realistic scenario showing complete user journey end-to-end
4. **Best For** — Use case guidance + explicit caveats/limitations
5. **References** — Pointers to supporting docs in `reference/` subdirectory

**Example: Good SKILL.md Frontmatter**

```yaml
---
name: git_create_pr
description: Create a GitHub PR with auto-populated description, review checklist, and branch protection checks
version: 2.1.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
  test_coverage_level: comprehensive
---
```

**What makes this good:**
- ✅ name matches `<domain>_<action>` pattern (git_create_pr)
- ✅ description is 1 sentence, non-technical, shows user value
- ✅ version follows semver
- ✅ maturity justified (tactical = battle-tested, widely used)
- ✅ tags capture status + criticality for quick scanning

## Contract Requirements [REQUIRED]

skill.contract.yaml must include:

[REQUIRED]
- `name`, `version`, `summary`, `maturity`
- `dispatch.triggers` — what invokes this skill (see `_trigger_design_and_testing.md`)
- `dispatch.not_for` — explicit scope boundaries (what it does NOT do)
- `output` — type (conversational|asynchronous), confirmation_required, reversible, returns

[IF APPLICABLE]
- `requires.tools` — special tools needed (if any)
- `requires.resources` — resources or permissions (if any)
- `dependencies.external` — external APIs or systems (if any)
- `dependencies.permissions` — special access required (if any)

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_trigger_design_and_testing.md` — trigger phrase design, evals.yaml, quality scorecard
