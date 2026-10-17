<!-- version: 3.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-17 -->
# 🚪 Artefact Proposal Gates

**Purpose:** Validate naming, placement, and duplication *before* proposing any new artefact (rule, skill, hook, agent, process), ensuring proposals already comply with established standards.

---

## 🚪 The Three Gates

Before proposing any new artefact, run these gates in order — when every gate passes, the proposal proceeds without options:

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

**Action:** If naming violates convention, **recommend the corrected name directly** (no options needed — the standard is clear), and present options only when the standard is ambiguous or several patterns fit.

---

### Gate 2️⃣: Placement

**Check:** Is the artefact placed in the correct directory?

- **01_essentials/** — foundational principles and user-facing conventions (e.g. guiding_principles, writing style, naming)
- **02_claude_standards/** — quality gates and operational conduct Claude applies to all work (e.g. behaviour, security, git, operational efficiency)
- **03_authoring_guidelines/** — meta-guidance for authoring rules, skills, agents
- **02_claude_standards/path_scoped_rules/** — domain-specific rules with `paths:`; load only when a matching file is open
- **_rules_lazy_load/** — under `rules/` in the repo and beside it once installed; read on demand only, never loaded automatically
- **skills/** — reusable skills, in the folder their domain names in `skill_domains.yaml` (e.g. `_atlassian_skills/`, `_git_skills/`)
- **hooks/** — enforcement and style-guide hooks
- **agents/** — custom sub-agents (domain-grouped subdirectories, e.g. `agents/core/`)

**Reference:** `~/.claude/rules/02_claude_standards/path_scoped_rules/claude_directory_structure.md` (parent) → `_claude_directory_organisation.md` (full tree) + `_claude_directory_naming.md` (naming patterns)

**Action:** If placement is wrong, **recommend the correct directory directly** (no options; the standard is clear), and present placement options with token-cost and scope trade-offs only when scope is genuinely unclear.

---

### Gate 3️⃣: Duplication

**Check:** Does a similar artefact already exist?

- Search for existing rules with similar scope or naming in `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`
- Search for skills in `~/.claude/skills/` with matching domain or action
- Search for hooks in `~/.claude/hooks/` with similar enforcement goal

**Reference:** `~/.claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` (full rule index table)

**Action:** If found, offer integration option: extend existing artefact vs. create new one (present options with rationale).
