<!-- version: 3.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
<!-- applies_to: **/rules/**, **/_rules_lazy_load/** -->
<!-- miss_cost: medium — rules ship without tests or in the wrong tier -->
<!-- loading: always-on — a new rule can start before any rule file is open, and it points to the shared complexity formula -->
# 🛠️ Rule Authoring

**Purpose:** Establish a standardized process for creating rules that ensures intentionality, proper scoping, and mechanical rigor.

Create focused, well-tested rules that solve real problems. One concept per rule.

## ✅ Pre-Creation Checklist

Before writing any rule, answer these five essential questions:

1. **Mechanical enforcement or instructional?**
   - Enforcement (hook, test, pre-commit validation) → requires tests per `testing.md`
   - Instructional (Claude reads and follows) → structural tests via test_rules_structure.py

2. **Always-on or lazy-loaded?**
   - Always-on: place in `rules/01_essentials/`–`03_authoring_guidelines/`, which Claude Code loads every session (core safety rules, ~100–150 tokens/session cost)
   - Path-scoped: `rules/04_path_scoped/` with `paths:` frontmatter, loaded only when a matching file is open
   - Lazy-load: `_rules_lazy_load/` (domain-specific, read on demand only)
   - Justify token cost if always-on

3. **Evidence of need** (not hypothetical)
   - Usage data, recurring incidents, user feedback, or prior failures
   - If speculative: defer or rephrase as question/guidance instead (per `guiding_principles.md`)

4. **Related/conflicting rules?**
   - Check **full rule list** in `~/.claude/rules/04_path_scoped/claude_rule_loading_strategy.md`
   - Search codebase for similar guidance to prevent duplication
   - Clarify which rules this complements or overlaps with

5. **Which directory & how to name?**
   - Directory choice (per below); naming via `naming_standards.md` → children files for directory structure and naming patterns
   - `01_essentials/` — user-facing conventions and foundational principles (guiding_principles, response/usage standards)
   - `02_claude_standards/` — blocking standards, enforcement and operational conduct (behaviour, security, testing, git, efficiency)
   - `03_authoring_guidelines/` — meta-guidance for authoring rules, skills, and agents
     - **Agent authoring:** `~/.claude/rules/03_authoring_guidelines/authoring_agents.md`, whose children are read on demand when creating or reviewing an agent
   - `04_path_scoped/` — domain-specific rules tied to a file type through `paths:` (style guides, testing)
   - `_rules_lazy_load/` — discretionary rules and bulky children, read on demand (tools, automation, style-guide detail)

## 🚀 Rule Creation (5 Steps)

1. **Answer the checklist above** — clarify scope before writing
2. **Pick a template:** Use `~/.claude/_templates/rule.md.template`
   - Template A (single principle, ~60 lines) vs. Template B (multiple patterns, ~100 lines)
3. **Write the rule** — follow template structure, emoji headers, one sentence per bullet
4. **Write tests:** Enforcement rules require tests in `_tests/rules/`. Instructional rules use structural checks.
5. **Create a quality scorecard:** `_admin/_quality_scorecards/rules/<tier>/scorecard_<rule_name>.md`, per the template in that folder's `README.md` — centralized, never `@import`ed.

## 📏 Quality Gates

- **H1 emoji header** — scannability
- **Purpose statement** — one line, top of file
- **One concept per rule** — related patterns grouped, not split across files
- **~100-line limit** — split into parent + child files if needed (see writing_style.md)
- **Trailing newline** — exactly one `\n` at EOF
- **Contents only with 3+ headings** — add a Contents section only when the rule has 3 or more real `##` headings
- **No Related section in the rule** — parent, sibling and dependency links go in the tier README in `_rules_lazy_load/_tier_readmes/` under "🔗 Related rules", which never loads by itself — tiers 02–05 only, as `01_essentials/` keeps no links (#310)
- **Place every child by how it should load** — Claude Code loads every `.md` under `rules/` on its own, so a child there needs no `@import`; the parent names it in a `**Loads on its own from:**` line.
  - **On-demand children:** put them in `_rules_lazy_load/<topic>/` and name each in a `**Read on demand:**` pointer — `test_always_on_reachability.py` fails the build on a README, `_lazy_load/` folder or `@import` under `rules/`.
- **Test validation** — enforcement rules pass custom tests; all rules pass test_rules_structure.py
- **Metadata header** — lines 1–3 carry `version`, `created` and `updated`, one per line; bump `updated` and `version` on every edit, per the standard below
- **Staleness reviews** — per `guiding_principles.md` reset cycles, audit all rules every ~6 months, archiving unused rules and refreshing evidence for kept ones

- **Loads on its own from:** `rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md`

- **Loads on its own from:** `rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md`

## 🚫 Common Mistakes & ✅ Hard Gates Checklist

- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_guidelines/authoring_rules/_common_mistakes.md` — before writing or reviewing a rule, for the mistakes this config has already shipped.
- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_guidelines/authoring_rules/_hard_gates_checklist.md` — before finishing or merging a rule, for the final tick-box check.
