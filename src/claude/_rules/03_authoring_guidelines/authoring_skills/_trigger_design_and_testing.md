<!-- version: 2.0.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
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

**Designing phrase triggers:**
- **Verbs:** list every natural way to ask — e.g. "create", "make", "open", "submit" a PR.
- **Terminology:** include alternate names for the same concept — e.g. "pr", "pull request", "mr".
- **Case:** add both lowercase and uppercase variants — e.g. `create a pr` and `create a PR`.
- **Be exhaustive:** a false positive costs less than a missed invocation.
- **Not too generic:** "help" or "please" alone won't distinguish your skill from others.
- **Example:** see `git_create_pr`'s `skill.contract.yaml` for a complete trigger list.

## Quality & Testing Standards [REQUIRED]

**evals.yaml [REQUIRED]** — THE standard testing approach (not ad-hoc test_*_handler.py scripts)
- Format: each eval has `name`, `description`, `input`, `setup`, `expected_output`
- Organization: by phase/feature (e.g., Phase 1, Phase 2, error cases)
- Coverage: happy paths, error cases, edge cases, user interactions
- Count by maturity: **Draft 5–8 evals** | **Tactical 8–12 evals** | **Strategic 12+ evals**

**Quality scorecard [REQUIRED]** — table-only, per `_quality_scorecard_template.md`
- Location: `scorecard_<skill_name>.md` at skill root
- Includes: Date Created, Date Updated, the 7 dimensions, Overall
- Maturity justification lives in SKILL.md's Best For line, not here

**Reference files [REQUIRED]** — Keep SKILL.md lean by externalizing detail
- `_implementation.md` — Phases, logic, error handling
- `_formats.md` [IF APPLICABLE] — Standards, validation rules, format examples

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields
