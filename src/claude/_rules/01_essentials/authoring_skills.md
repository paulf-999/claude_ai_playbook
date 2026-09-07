# 🛠️ Skill Authoring

**Purpose:** Create focused, well-documented, properly tested skills. One concept per skill.

---

## 🧭 Quick Navigation

**New skill author?** Start here in order:
1. **Core Standards** — Naming pattern, SKILL.md structure, specification fields, testing standards
2. **7-Step Process** — Workflow: name → specification → SKILL.md → reference/ → evals.yaml → score → submit
3. **Hard Gates Checklist** — Final validation before submitting

**Experienced author, need to refresh?** Jump to specific sections:
- **Scope Boundaries** — If designing what your skill does NOT do
- **Maturity Justification** — If choosing Draft vs. Tactical vs. Strategic maturity
- **Low-Maintenance Design** — If updating an existing skill or preventing maintenance debt
- **Common Mistakes** — If you're stuck or uncertain about a choice

**Reviewing someone else's skill?** Use these sections:
- **Hard Gates Checklist** — Verify completeness and compliance
- **Common Mistakes** — Catch anti-patterns and design flaws
- **Maturity Justification** — Verify evidence-based maturity choice

---

## 📐 Core Standards

Every skill follows these baseline standards:

### Naming Pattern
- Format: `<domain>_<action>` (lowercase, snake_case)
- Domain: must match valid domain ID from `skill_domains.yaml`
- Action: imperative verb describing what the skill does
- Examples: `confluence_create_page`, `jira_create`, `git_create_pr`, `claude_review_config`
- Hard rule: Directory prefix must match domain (e.g., `confluence_create_page` → `_confluence_skills/`)

### SKILL.md Structure [REQUIRED]
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

### Contract Requirements [REQUIRED]
skill.contract.yaml must include:

[REQUIRED]
- `name`, `version`, `summary`, `maturity`
- `dispatch.triggers` — what invokes this skill (see Trigger Design section below)
- `dispatch.not_for` — explicit scope boundaries (what it does NOT do)
- `output` — type (conversational|asynchronous), confirmation_required, reversible, returns

[IF APPLICABLE]
- `requires.tools` — special tools needed (if any)
- `requires.resources` — resources or permissions (if any)
- `dependencies.external` — external APIs or systems (if any)
- `dependencies.permissions` — special access required (if any)

### Trigger Design [REQUIRED]

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

### Quality & Testing Standards [REQUIRED]

**evals.yaml [REQUIRED]** — THE standard testing approach (not ad-hoc test_*_handler.py scripts)
- Format: each eval has `name`, `description`, `input`, `setup`, `expected_output`
- Organization: by phase/feature (e.g., Phase 1, Phase 2, error cases)
- Coverage: happy paths, error cases, edge cases, user interactions
- Count by maturity: **Draft 5–8** | **Tactical 8–12** | **Strategic 12+**

**Quality scorecard [REQUIRED]** — 8 dimensions scored + maturity justification
- Location: `reference/_quality_scorecard.md`
- Includes: Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards, Overall

**Reference files [REQUIRED]** — Keep SKILL.md lean by externalizing detail
- `_quality_scorecard.md` — Dimensions, maturity justification, design rationale
- `_implementation.md` — Phases, logic, error handling
- `_formats.md` [IF APPLICABLE] — Standards, validation rules, format examples

---

## 🏆 Baseline Skill Pattern

All new skills should follow this proven pattern:

- **Ultra-lean SKILL.md** (~60 lines) — all detail externalized to reference/
- **Contract-first** — skill.contract.yaml defines scope *before* SKILL.md is written
- **Evals-driven** — test scenarios organized by phase; quality scorecard scored *against* evals, not independently
- **Explicit boundaries** — dispatch.not_for is authoritative; v2.0 enhancements documented separately
- **Confirmation gates** — destructive operations include explicit user confirmation
- **Maturity justified** — scorecard explains why skill is Draft/Tactical/Strategic with evidence

This pattern balances scannability (SKILL.md readable in <2 min) with comprehensive detail (reference/ files for implementation, formats, rationale).

---

## 🚀 Create a Skill (7 Steps)

1. **Run `/skill_creator`** → answers questions → generates directory with template
2. **Name it:** `<domain>_<action>` format (see Core Standards above for naming rules and examples)
3. **Populate `skill.contract.yaml` FIRST** [REQUIRED] — defines scope before SKILL.md
   - Define what the skill does: `dispatch.triggers`
   - Define what it does NOT do: `dispatch.not_for` (prevents scope creep; MOST IMPORTANT FIELD)
   - List required tools, resources, dependencies
   - Declare output type and confirmation requirements
   - Reference: See Core Standards section above
4. **Write `SKILL.md` using 5-section structure** [REQUIRED]
   - Use the 5-section canonical structure (see Core Standards)
   - Reference: `~/.claude/_templates/skills/SKILL.md.template`
   - Keep to ~60 lines; externalize detail to `reference/` files
   - If SKILL.md exceeds 60 lines, detail belongs in reference/
5. **Create `reference/` files** [REQUIRED]
   - `_quality_scorecard.md` — dimensions + maturity justification
   - `_implementation.md` — phases, logic, error handling
   - `_formats.md` (if applicable) — standards, validation, examples
6. **Write `evals.yaml`** [REQUIRED] — THE standard testing approach
   - 10–15 scenarios organized by phase/feature
   - Each eval: name, description, input, setup, expected_output
   - Coverage: happy paths, error cases, edge cases
   - Count matches maturity level (Draft 5–8, Tactical 8–12, Strategic 12+)
   - Evals are THE source of truth; quality scorecard is scored *against* evals
7. **Score complexity & submit**
   - Complexity (0–10): Concepts (0–3) + Scope (0–3) + Dependencies (0–2) + Prerequisites (0–2)
   - Maturity gates: Draft ≤4, Tactical ≤6, Strategic ≤8, 9+ = must split
   - Pre-commit validates structure + naming + complexity
   - Human review validates design clarity and scope focus

---

## 🚪 Scope Boundaries [REQUIRED]

Every skill must explicitly declare what it does AND what it does NOT do. This prevents feature creep and sets user expectations upfront.

**In `skill.contract.yaml`, use the `dispatch.not_for` field:**

```yaml
dispatch:
  not_for:
    - Edge case 1 (skill doesn't handle this)
    - Edge case 2 (skill explicitly out of scope)
    - Future enhancement (v2.0+)
```

**Example (git_create_pr):**
```yaml
not_for:
  - complex merge conflict scenarios
  - non-main branch PRs
  - release branch workflows (v2.0+)
```

**In `reference/_quality_scorecard.md`, explain why:**
- Why these boundaries? (design choice? technical limitation? future roadmap?)
- What would v2.0 add?
- What's the tradeoff? (keeps skill lean vs. limits applicability)

### Anti-Patterns: What NOT to Do

**❌ Don't try to handle everything**
- A skill that handles "all Confluence page operations" becomes bloated and unmaintainable
- Better: narrow scope (e.g., `confluence_create_page`, `confluence_update_page` as separate skills)
- Use `not_for` to document explicit boundaries

**❌ Don't use ad-hoc test_*_handler.py scripts**
- Use `evals.yaml` (THE standard for all skills)
- Ad-hoc test scripts become unmaintained and unreliable
- evals.yaml is discoverable, testable, and documented

**❌ Don't claim maturity without evidence**
- Draft: speculative, one-time use only
- Tactical: recurring problem, battle-tested, fully tested
- Strategic: core workflow, heavy use, all edge cases covered
- Justify maturity in `reference/_quality_scorecard.md` with evidence

---

## 🛠️ Low-Maintenance Design [CRITICAL]

Skills should be designed to minimize ongoing maintenance burden. This section establishes principles for creating skills that are stable, self-contained, and resist scope creep and complexity debt.

### The Maintenance Trap: What NOT to Do

**❌ Don't create skills that require constant updates:**
- **Coupling to external APIs** — Requires updates when API changes, external dependencies introduce fragility
- **Versioning complexity** — Multiple major versions (v1.0, v1.1, v2.0 branches) = maintenance debt, user confusion
- **Interdependencies** — Skill A depends on Skill B = cascade failures, hidden coupling
- **Broad scope** — "Handle all X operations" = endless feature requests, scope creep, bloat

**Anti-pattern consequence:** A skill that's updated 5+ times/year is a sign of poor design, not evolution. It's a maintenance liability.

### Stability-First Design Principles

**✅ Design for immutability:**
- Once v1.0 ships, assume it won't need changes
- Future enhancements = new skill with different name (e.g., `slack_send_message` v1.0 stays frozen; threading goes in `slack_send_thread` v1.0)
- Deprecate old version cleanly: announce 6-month sunset, provide migration guide

**✅ Isolate dependencies:**
- **No skill-to-skill calls** — Use MCP or CLI for inter-skill communication, not direct calls
- **No external API coupling if avoidable** — Local-only > API-dependent (fewer failure modes)
- **Battle-tested tools only** — Slack API, GitHub API = proven stable; experimental tools = avoid

**✅ Enforce tight boundaries:**
- Use `dispatch.not_for` to explicitly freeze scope (v1.0 says "no thread replies, no reactions, no editing")
- Document v2.0 roadmap separately (doesn't belong in v1.0 contract)
- Future enhancements are *new* skills, not updates to existing ones

**✅ Test for stability:**
- `evals.yaml` captures the contract (what this skill does and doesn't do)
- Future maintainers: run evals before any update
- **If evals break, you've broken the contract → don't merge the update**

### Maintenance Policy

**Update only for critical reasons:**
- 🔴 **Security vulnerability** — Something is actively broken/unsafe
- 🔴 **Broken external dependency** — External API changed, tool deprecated
- ❌ **Feature requests** — Create new skill instead (prevents scope creep)
- ❌ **"Improvements"** — Refactoring is scope creep in disguise (old version works fine)

**Deprecate when truly necessary:**
- Old version is superseded by better design (e.g., `slack_send_message` → `slack_send_with_threading`)
- Announce 6-month sunset date upfront (give users time to migrate)
- Provide clear migration guide (how to switch to new skill)
- Keep old skill functional for full deprecation period (no breaking changes during sunset)

### Measurement: Tracking Maintenance Burden

For each skill, track:
- **Update frequency** — How many times per year is this skill updated? (Target: <2/year for Tactical, <1/year for Strategic)
- **Reason for update** — Security? API change? Feature request? (Only first two are valid reasons)
- **Contract breakage** — Do updates require changing evals.yaml? (If yes, you've broken the contract)

**Red flag:** If a skill requires updates more than 2x/year, it's too broad or too coupled. **Redesign it.**

**Healthy pattern:** Stable Tactical skill gets 0-1 update/year (only security or API breaks). Strategic skills get 0 updates/year.

---

## 📈 Maturity Justification [REQUIRED]

Maturity level (draft, tactical, strategic) must be justified with evidence, not aspirations.

### How to Choose Your Maturity Level

Use this decision framework:

| Evidence | Draft | Tactical | Strategic |
|----------|-------|----------|-----------|
| **Real problem** | Speculative or one-time | Recurring, observed need | Core workflow, heavy use |
| **Use frequency** | <2/month | 5–20/month | 20+/month or always-on |
| **Test coverage** | 5–8 evals (happy paths) | 8–12 evals (paths + errors) | 12+ evals (+ edge cases) |
| **Dependencies** | Experimental tools | Battle-tested tools | Core infrastructure |
| **Documentation** | Basic how-to | Clear + reference docs | Ultra-lean + comprehensive refs |
| **Scope maturity** | Still exploring | Well-defined boundaries | Stable, frozen scope |

### Testing by Maturity Level

**Draft (5–8 evals)**
- Happy paths: user invokes skill, gets expected output
- Basic validation: inputs are checked, bad inputs fail gracefully
- No error cases or edge cases required (scope still evolving)

**Tactical (8–12 evals)**
- All from Draft, PLUS:
- Error cases: network failures, invalid API responses, permission denied
- Retry logic: does the skill recover from transient failures?
- User interactions: does the skill ask clarifying questions when needed?

**Strategic (12+ evals)**
- All from Tactical, PLUS:
- Edge cases: unusual inputs, boundary conditions, race conditions
- Adversarial inputs: what if the user passes malicious or contradictory data?
- Performance: does the skill scale? Does it handle large datasets?
- Security: are secrets handled safely? Are inputs validated against injection?

### Writing Your Maturity Justification

Document in `reference/_quality_scorecard.md`:

```markdown
## Maturity Justification

**Real problem solved:** <What recurring user need does this skill address?>

**Use frequency:** <How often is this used per month? Data from sessions?>

**Test coverage:** <# evals total; what's covered (happy paths, errors, edge cases)>

**Dependency assessment:** <Battle-tested tools? Experimental?>

**Scope assessment:** <Clear boundaries? Stable for v1.0? Future enhancements documented?>

**Conclusion:** This skill justifies [Draft|Tactical|Strategic] maturity because:
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]
```

---

## ⚠️ Common Mistakes & Security

### Common Mistakes to Avoid

**❌ Mistake 1: Too much detail in SKILL.md**
```markdown
## Purpose
This skill creates Confluence pages with formatting, validation, error handling, 
retry logic, permission checking, and extensive documentation...
[continues for 80+ lines]
```
**✅ Fix:** Externalize to reference files
- Keep SKILL.md to ~60 lines
- Move implementation details to `reference/_implementation.md`
- Move format specs to `reference/_formats.md`

**❌ Mistake 2: Vague purpose statement**
```markdown
## Purpose
Do Confluence stuff
```
**✅ Fix:** Be specific and user-focused
```markdown
## Purpose
Create Confluence pages with auto-populated templates and validation:
- **Template-based creation** — Use pre-built page templates
- **Field validation** — Ensure required fields are populated
- **Error recovery** — Handle invalid inputs gracefully
```

**❌ Mistake 3: Missing scope boundaries**
```yaml
dispatch:
  not_for: []  # Empty! Undefined scope, will bloat over time
```
**✅ Fix:** Be explicit about what you DON'T do
```yaml
dispatch:
  not_for:
    - Page editing or updating (use /confluence_update_page)
    - Permission management (separate skill)
    - Deleting pages (intentionally excluded for safety)
```

**❌ Mistake 4: No maturity justification**
```yaml
maturity: tactical
# No evidence, no explanation
```
**✅ Fix:** Document why this level
```markdown
## Maturity Justification

**Real problem solved:** Teams repeatedly create Confluence pages from templates.

**Use frequency:** Used in 12% of sessions, 3-4 times per week in active projects.

**Test coverage:** 15 evals covering template selection, validation errors, API failures.

**Dependency assessment:** Confluence API is stable; no experimental tools.

**Scope assessment:** Clear boundaries; v1.0 = creation only. Editing deferred to v2.0.

**Conclusion:** Justifies Tactical maturity because:
- Real, recurring problem (template creation)
- 15 evals cover all phases (Tactical requirement)
- Stable external dependency (Confluence API)
- Clear boundaries prevent scope creep
```

### Security Considerations [IMPORTANT]

When authoring skills, prioritize security:

**Secrets & Credentials**
- ❌ Never hardcode API keys, tokens, or passwords
- ✅ Use environment variables only (e.g., `SLACK_BOT_TOKEN`, `JIRA_TOKEN`)
- ✅ Document required env vars in `requires.resources` section

**Input Validation**
- ❌ Don't pass user input directly to APIs or shell commands
- ✅ Validate all inputs against expected format (length, type, allowed chars)
- ✅ Reject suspicious patterns (command injection, path traversal, etc.)

**Permissions & Least Privilege**
- ❌ Don't request more permissions than needed
- ✅ List required permissions in `dependencies.permissions` (e.g., `chat:write`, `channels:read`)
- ✅ Document why each permission is needed

**Error Messages**
- ❌ Don't expose internal details or stack traces
- ✅ Provide clear, user-friendly error messages
- ✅ Guide users on how to fix the issue (e.g., "Set SLACK_BOT_TOKEN environment variable")

---

## ✅ Hard Gates Checklist

### Before Submitting

- [ ] **Contract complete BEFORE SKILL.md** — never write SKILL.md without contract finalization
  - [ ] name, version, summary, maturity all defined
  - [ ] dispatch.triggers documented (when is skill invoked?)
  - [ ] dispatch.not_for documented (scope boundaries; MOST IMPORTANT)
  - [ ] output (type, confirmation_required, reversible, returns) declared
  - [ ] requires [IF APPLICABLE] — tools, resources, permissions
  - [ ] dependencies [IF APPLICABLE] — external APIs or systems
- [ ] **SKILL.md structure [REQUIRED]:** 5 sections only, ~60 lines max
  - [ ] Frontmatter: name, description, version, maturity, tags
  - [ ] Purpose: 1 sentence value prop + 3–4 bullets
  - [ ] Example Usage: realistic scenario showing complete journey
  - [ ] Best For: use cases + explicit caveats (when NOT to use)
  - [ ] References: links to reference/ files (no inline detail)
  - [ ] Total length: ≤60 lines (if longer, detail belongs in reference/)
- [ ] **Complexity score [REQUIRED]:** 0–10 rating
  - [ ] Score ≤ maturity limit (Draft ≤4, Tactical ≤6, Strategic ≤8)
  - [ ] If over limit: reduce scope or split into multiple skills
- [ ] **evals.yaml [REQUIRED]:** 10–15 scenarios organized by phase
  - [ ] Each eval: name, description, input, setup, expected_output
  - [ ] Coverage: happy paths, error cases, edge cases, user interactions
  - [ ] Count matches maturity (Draft 5–8, Tactical 8–12, Strategic 12+)
  - [ ] evals.yaml is THE testing vehicle (not ad-hoc test_*_handler.py)
- [ ] **Quality scorecard [REQUIRED]:** reference/_quality_scorecard.md
  - [ ] 7 dimensions scored (Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards)
  - [ ] Dimensions scored *against evals.yaml*, not independently
  - [ ] Maturity level justified with evidence
  - [ ] Design rationale explained
- [ ] **Reference files [REQUIRED]:**
  - [ ] reference/_quality_scorecard.md exists with all 7 dimensions
  - [ ] reference/_implementation.md exists (phases, logic, error handling)
  - [ ] reference/_formats.md [IF APPLICABLE] (standards, validation, examples)
- [ ] **Scope boundaries enforced:**
  - [ ] dispatch.not_for defined and specific (not empty)
  - [ ] Rationale documented in quality scorecard
  - [ ] Skill has clear, narrow focus (not "everything related to X")
- [ ] **Naming:** `<domain>_<action>` format, valid domain ID, directory matches

---

## 📚 Reference

@~/.claude/_rules/01_essentials/authoring_skills/_skill_structure_contract.md

@~/.claude/_rules/01_essentials/authoring_skills/_skill_quality_checklist.md

@~/.claude/_rules/01_essentials/authoring_skills/_skill_review_framework.md

---

## 📁 File Organization

Minimal, focused structure. Each skill directory contains **only**:

```
skill_name/
├── SKILL.md              # User-facing overview (5 sections, ~60 lines)
├── skill.contract.yaml   # Machine-readable contract (scope, triggers, maturity)
├── evals.yaml            # Test scenarios (10–15, organized by phase)
└── reference/            # Supporting docs (keep SKILL.md lean)
    ├── _quality_scorecard.md  # Dimensions, maturity justification, design rationale
    ├── _implementation.md     # Phases, logic, error handling
    └── _formats.md            # Standards, validation, examples (if applicable)
```

**Nothing else.** No `templates/`, `patterns/`, `references/`, or domain-specific subdirectories. Keep scope tight, keep structure clean.

---

## 🔗 Related Rules

- **naming_standards.md** — Foundational naming principles; skill naming patterns in child file
- **testing.md** — Skill testing requirements by maturity level
- **authoring_rules.md** — General rule authoring process (complementary to skill authoring)
