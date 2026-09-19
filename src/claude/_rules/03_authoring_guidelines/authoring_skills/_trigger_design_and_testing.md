# 🎯 Trigger Design & Testing Standards

**Purpose:** Define how to design comprehensive trigger phrase coverage, and the evals.yaml/quality-scorecard testing standard every skill must follow.

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

**Designing Comprehensive Phrase Triggers**

1. **Core action verbs:** List all natural ways to request the action
   - Git PR creation: "create", "make", "open", "submit", "push"
   - Confluence page creation: "create", "add", "write"
   - Jira ticket creation: "create", "log", "file"

2. **Domain terminology variants:** Include alternate names for the same concept
   - Pull requests: "pr", "PR", "pull request"
   - Merge requests: "mr", "MR", "merge request"
   - Both: `create a pr`, `create a PR`, `create a mr`, `create a MR`

3. **Case sensitivity:** Include both lowercase and uppercase variants
   - `create a pr` and `create a PR`
   - `create a mr` and `create a MR`
   - **Why:** Ensures matching regardless of how users type it

4. **Natural language patterns:** Cover how users naturally phrase requests
   - Instead of just: `create a pr`
   - Also add: `make a pr`, `open a pr`, `submit a pr`, `push a pr`
   - **Why:** Different users have different phrasing preferences

**Example: Comprehensive Trigger List**

```yaml
dispatch:
  triggers:
    explicit:
      - /git_create_pr
      - create a pr
      - create a PR
      - make a pr
      - make a PR
      - open a pr
      - open a PR
      - submit a pr
      - submit a PR
      - push a pr
      - push a PR
      - create a mr
      - create a MR
      - make a mr
      - make a MR
      - open a mr
      - open a MR
      - submit a mr
      - submit a MR
      - push a mr
      - push a MR
    contextual:
      - user wants to create a pull request
      - user wants to submit code changes
```

**Best Practices**

- ✅ **Be exhaustive:** Add every natural variant you can think of. False positives are better than false negatives (missing an invocation)
- ✅ **Test coverage:** Ask team members how they'd phrase the request; add those phrases
- ✅ **Symmetry:** If you add "create a pr", also add "create a PR"
- ✅ **Domain-aware:** Know the terminology your users use (PR vs MR, issue vs ticket, etc.)
- ❌ **Don't be too generic:** "help" or "please" alone won't distinguish your skill from others
- ❌ **Don't assume lowercase:** Include uppercase variants; users write in different styles

## Quality & Testing Standards [REQUIRED]

**evals.yaml [REQUIRED]** — THE standard testing approach (not ad-hoc test_*_handler.py scripts)
- Format: each eval has `name`, `description`, `input`, `setup`, `expected_output`
- Organization: by phase/feature (e.g., Phase 1, Phase 2, error cases)
- Coverage: happy paths, error cases, edge cases, user interactions
- Count by maturity: **Draft 5–8** | **Tactical 8–12** | **Strategic 12+**

**Quality scorecard [REQUIRED]** — 8 dimensions scored + maturity justification
- Location: `_quality_scorecard.md`
- Includes: Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards, Overall

**Reference files [REQUIRED]** — Keep SKILL.md lean by externalizing detail
- `_quality_scorecard.md` — Dimensions, maturity justification, design rationale
- `_implementation.md` — Phases, logic, error handling
- `_formats.md` [IF APPLICABLE] — Standards, validation rules, format examples

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields
