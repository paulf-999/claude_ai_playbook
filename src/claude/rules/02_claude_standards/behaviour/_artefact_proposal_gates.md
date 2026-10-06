<!-- version: 2.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
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
  - Domain must be valid (check `skill_domains.yaml`)
  - Action must be lowercase imperative verb
- **Rules:** snake_case, descriptive (e.g., `naming_standards.md`, `security.md`)
- **Hooks:** `hook_<type>_<domain>.sh` (e.g., `hook_enforcement_naming_convention.sh`)
- **Agents:** `agents/<group>/<name>/AGENT.md` (e.g. `agents/core/technical_writer/AGENT.md`)
- **Processes:** snake_case, descriptive (e.g., `session_kickoff.md`)

**Reference:** `~/.claude/rules/01_essentials/claude_usage_standards/naming_standards.md` (parent) → `_claude_naming_patterns.md` (child file with detailed patterns)

**Action:** If naming violates convention, **recommend the corrected name directly** (no options needed — the standard is clear).

---

### Gate 2️⃣: Placement

**Check:** Is the artefact placed in the correct directory?

- **01_essentials/** — foundational principles and user-facing conventions (e.g. guiding_principles, writing style, naming)
- **02_claude_standards/** — quality gates Claude applies to all work (e.g. behaviour, security, testing, git)
- **03_authoring_guidelines/** — meta-guidance for authoring rules, skills, agents
- **04_claude_reference/** — system knowledge and platform guidance (e.g. operational efficiency, rule loading strategy)
- **05_path_scoped/** — domain-specific rules with `paths:`; load only when a matching file is open
- **_rules_lazy_load/** — beside `rules/`; read on demand only, never loaded automatically
- **skills/** — reusable skills, in the folder their domain names in `skill_domains.yaml` (e.g. `_atlassian_skills/`, `_git_skills/`)
- **hooks/** — enforcement and style-guide hooks
- **agents/** — custom sub-agents (domain-grouped subdirectories, e.g. `agents/core/`)

**Reference:** `~/.claude/rules/05_path_scoped/claude_directory_structure.md` (parent) → `_claude_directory_organisation.md` (full tree) + `_claude_directory_naming.md` (naming patterns)

**Action:** If placement is wrong, **recommend the correct directory directly** (no options; the standard is clear).

---

### Gate 3️⃣: Duplication

**Check:** Does a similar artefact already exist?

- Search for existing rules with similar scope or naming in `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`
- Search for skills in `~/.claude/skills/` with matching domain or action
- Search for hooks in `~/.claude/hooks/` with similar enforcement goal

**Reference:** `~/.claude/rules/05_path_scoped/claude_rule_loading_strategy.md` (full rule index table)

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
- **Gate 2 (Placement):** Scope is genuinely unclear (e.g., "is this 01_essentials or _rules_lazy_load?") — present placement options with token cost / scope tradeoffs
- **Gate 3 (Duplication):** Similar artefact exists; present integration options (extend existing + cost, vs. create new + maintenance)

**Otherwise:** Gates pass and proposal proceeds without options.
