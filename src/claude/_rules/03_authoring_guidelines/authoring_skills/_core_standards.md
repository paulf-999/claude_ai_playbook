<!-- version: 2.0.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# 📐 Skill Core Standards

**Purpose:** Define the baseline every skill must follow — naming, SKILL.md's 5-section structure, what `skill.contract.yaml` must declare, and how to choose a maturity level.

---

## Naming Pattern

- Format: `<domain>_<action>` (lowercase, snake_case)
- Domain: must match valid domain ID from `skill_domains.yaml`
- Action: imperative verb describing what the skill does
- Examples: `confluence_create_page`, `jira_create`, `git_create_pr`, `claude_review_config`
- Hard rule: Directory prefix must match domain (e.g., `confluence_create_page` → `_confluence_skills/`)

## SKILL.md Structure [REQUIRED]

5-section canonical structure, ~60 lines, scannable in <2 minutes:
1. **Frontmatter** — name, description, maturity, tags, followed by the three-line metadata header (version, created, updated)
2. **Purpose** — 1 sentence value prop + 3–4 bullets of key capabilities
3. **Example Usage** — Realistic scenario showing complete user journey end-to-end
4. **Best For** — Use case guidance + explicit caveats/limitations
5. **References** — Pointers to supporting docs in `reference/` subdirectory

**Example: Good SKILL.md Frontmatter**

```yaml
---
name: git_create_pr
description: Create a GitHub PR with auto-populated description, review checklist, and branch protection checks
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 2.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-19 -->
```

**What makes this good:**
- ✅ name matches `<domain>_<action>` pattern (git_create_pr)
- ✅ description is 1 sentence, non-technical, shows user value
- ✅ version sits in the metadata header straight after the frontmatter, follows semver, and matches `skill.contract.yaml` (see `_claude_config_metadata.md`)
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

## Maturity Levels [REQUIRED]

Choose the maturity level from evidence, not aspiration:

| Evidence | Draft | Tactical | Strategic |
|----------|-------|----------|-----------|
| **Real problem** | Speculative or one-time | Recurring, observed need | Core workflow, heavy use |
| **Use frequency** | <2/month | 5–20/month | 20+/month or always-on |
| **Test coverage** | 5–8 evals: happy paths + basic validation | 8–12 evals: + error cases, retries, clarifying questions | 12+ evals: + edge cases, adversarial inputs, security |
| **Complexity (raw sum)** | ≤4 | ≤6 | ≤8 (9+ means split it) |
| **Dependencies** | Experimental tools | Battle-tested tools | Core infrastructure |
| **Scope** | Still exploring | Well-defined boundaries | Stable, frozen scope |

- **Where to justify it:** one sentence in SKILL.md's **Best For** line, naming the stage and what it doesn't yet cover.
- **Not in the scorecard:** `scorecard_<skill_name>.md` is table-only (see `_quality_scorecard_template.md`).
- **Example:** "Currently at the **tactical** stage — main path plus light error handling, not full edge-case coverage yet."
- **Complexity formula:** see `_complexity_scoring.md` (sibling of `authoring_skills.md`).

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_trigger_design_and_testing.md` — trigger phrase design, evals.yaml, quality scorecard
