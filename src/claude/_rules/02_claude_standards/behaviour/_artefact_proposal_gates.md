# 🚪 Artefact Proposal Gates

**Purpose:** Validate naming, placement, and duplication *before* proposing any new artefact (rule, skill, hook, agent, process), ensuring proposals already comply with established standards.

---

## 📋 Contents

- [The Three Gates](#-the-three-gates)
- [Gate Sequence](#-gate-sequence)
- [When to Present Options](#-when-to-present-options)

---

## 🚪 The Three Gates

Before proposing any new artefact, run these gates in order:

### Gate 1️⃣: Naming

**Check:** Does the artefact name follow established conventions?

- **Skills:** `<domain>_<action>` format (e.g., `confluence_create_page`, `jira_create`)
  - Domain must be valid (check `skill_domains.yaml` + `skill_domains_future.yaml`)
  - Action must be lowercase imperative verb
- **Rules:** snake_case, descriptive (e.g., `naming_standards.md`, `security.md`)
- **Hooks:** `hook_<type>_<domain>.sh` (e.g., `hook_enforcement_sql.sh`)
- **Agents:** `<name>_agent.py` or domain-grouped subdirectories
- **Processes:** snake_case, descriptive (e.g., `session_kickoff.md`)

**Reference:** `~/.claude/_rules/01_essentials/conventions/naming_standards.md` (parent) → `_claude_naming_patterns.md` (child file with detailed patterns)

**Action:** If naming violates convention, **recommend the corrected name directly** (no options needed — the standard is clear).

---

### Gate 2️⃣: Placement

**Check:** Is the artefact placed in the correct directory?

- **01_essentials/** — blocking/safety rules (always-on imports); security-critical artefacts
- **02_claude_standards/** — how Claude operates; efficiency/memory/git guidance
- **04_lazy_load/** — domain-specific; loaded on-demand only
- **skills/** — reusable skills (single domain per subdirectory: `_confluence_skills/`, `_git_skills/`, etc.)
- **hooks/** — enforcement and style-guide hooks
- **agents/** — custom sub-agents (domain-grouped subdirectories: `agents/core/`, `agents/tools/`, etc.)

**Reference:** `~/.claude/_rules/01_essentials/conventions/claude_directory_structure.md` (parent) → `_claude_directory_organization.md` (full tree) + `_claude_directory_naming.md` (naming patterns)

**Action:** If placement is wrong, **recommend the correct directory directly** (no options; the standard is clear).

---

### Gate 3️⃣: Duplication

**Check:** Does a similar artefact already exist?

- Search for existing rules with similar scope or naming in `~/.claude/_rules/`
- Search for skills in `~/.claude/skills/` with matching domain or action
- Search for hooks in `~/.claude/hooks/` with similar enforcement goal

**Reference:** `~/.claude/_rules/03_claude_reference/claude_rule_system/claude_rule_loading_strategy.md` (full rule index table)

**Action:** If found, offer integration option: extend existing artefact vs. create new one (present options with rationale).

---

## 🔄 Gate Sequence

**Always run gates in order:**

```
1. Does naming follow convention?
   ├─ No  → Recommend correct name
   └─ Yes → Continue to Gate 2

2. Is placement correct for artefact type?
   ├─ No  → Recommend correct directory
   └─ Yes → Continue to Gate 3

3. Does similar artefact already exist?
   ├─ Yes → Present integration options
   └─ No  → Safe to proceed with proposal
```

---

## ❓ When to Present Options

Present options *only* in these scenarios:

- **Gate 1 (Naming):** Standard is ambiguous or multiple valid patterns exist for the artefact type (rare)
- **Gate 2 (Placement):** Scope is genuinely unclear (e.g., "is this 01_essentials or 04_lazy_load?") — present placement options with token cost / scope tradeoffs
- **Gate 3 (Duplication):** Similar artefact exists; present integration options (extend existing + cost, vs. create new + maintenance)

**Otherwise:** Gates pass and proposal proceeds without options.

---

## 🔗 Related rules

- Parent: `behaviour.md` — Safe defaults and safe action guidelines
- Sibling: `_decision_making.md` — When to present options vs. decide unilaterally; gates should pass before options are presented
- Reference: `naming_standards.md`, `claude_directory_structure.md`, `~/.claude/_rules/03_claude_reference/claude_rule_system/claude_rule_loading_strategy.md`

---
