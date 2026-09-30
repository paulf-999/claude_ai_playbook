<!-- version: 1.5.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-30 -->
# 🛠️ Rule Authoring

**Purpose:** Establish a standardized process for creating rules that ensures intentionality, proper scoping, and mechanical rigor.

Create focused, well-tested rules that solve real problems. One concept per rule.

## ✅ Pre-Creation Checklist

Before writing any rule, answer these five essential questions:

1. **Mechanical enforcement or instructional?**
   - Enforcement (hook, test, pre-commit validation) → requires tests per `testing.md`
   - Instructional (Claude reads and follows) → structural tests via test_rules_structure.py

2. **Always-on or lazy-loaded?**
   - Always-on: import into CLAUDE.md (core safety rules, ~100–150 tokens/session cost)
   - Lazy-load: `05_lazy_load/` (domain-specific, load on-demand only)
   - Justify token cost if always-on

3. **Evidence of need** (not hypothetical)
   - Usage data, recurring incidents, user feedback, or prior failures
   - If speculative: defer or rephrase as question/guidance instead (per `guiding_principles.md`)

4. **Related/conflicting rules?**
   - Check **full rule list** in `~/.claude/_rules/04_claude_reference/claude_rule_loading_strategy.md`
   - Search codebase for similar guidance to prevent duplication
   - Clarify which rules this complements or overlaps with

5. **Which directory & how to name?**
   - Directory choice (per below); naming via `naming_standards.md` → children files for directory structure and naming patterns
   - `01_essentials/` — user-facing conventions and foundational principles (guiding_principles, response/usage standards)
   - `02_claude_standards/` — blocking standards and enforcement (behaviour, security, testing, git)
   - `03_authoring_guidelines/` — meta-guidance for authoring rules, skills, and agents
     - **Agent authoring:** read `~/.claude/_rules/05_lazy_load/authoring_agents.md` on demand when creating or reviewing an agent
   - `04_claude_reference/` — system knowledge and platform guidance (efficiency, rule loading strategy)
   - `05_lazy_load/` — domain-specific or discretionary (style guides, tools, automation)

## 🚀 Rule Creation (5 Steps)

1. **Answer the checklist above** — clarify scope before writing
2. **Pick a template:** Use `~/.claude/_templates/RULE.md.template`
   - Template A (single principle, ~60 lines) vs. Template B (multiple patterns, ~100 lines)
3. **Write the rule** — follow template structure, emoji headers, one sentence per bullet
4. **Write tests:** Enforcement rules require tests in `_tests/rules/`. Instructional rules use structural checks.
5. **Create a quality scorecard:** `_rules/quality_scorecards/<tier>/scorecard_<rule_name>.md`, per `quality_scorecards/README.md`'s template — centralized, never `@import`ed.

## 📏 Quality Gates

- **H1 emoji header** — scannability
- **Purpose statement** — one line, top of file
- **One concept per rule** — related patterns grouped, not split across files
- **~100-line limit** — split into parent + child files if needed (see writing_style.md)
- **Trailing newline** — exactly one `\n` at EOF
- **Contents only with 3+ headings** — add a Contents section only when the rule has 3 or more real `##` headings
- **No Related section in the rule** — parent, sibling and dependency links go in the tier's `README.md` under "🔗 Related rules", which isn't `@import`ed
- **Wire up every documented child** — if a parent rule describes child files (e.g. under a "Load details on-demand" section), each one needs a real `@import` line, not just prose naming it. A file mentioned but never imported is silently unreachable — see `test_always_on_reachability.py`, which fails the build if any file under `01_essentials/`–`04_claude_reference/` exists on disk but isn't reachable from `CLAUDE.md`.
  - **Exception:** children kept in a parent's `<parent>/_lazy_load/` folder are read on demand, so the parent names them in a `**Read on demand:**` pointer instead.
- **Test validation** — enforcement rules pass custom tests; all rules pass test_rules_structure.py
- **Metadata header** — lines 1–3 carry `version`, `created` and `updated`, one per line; bump `updated` and `version` on every edit, per the standard below
- **Staleness reviews** — per `guiding_principles.md` reset cycles, audit all rules every ~6 months, archiving unused rules and refreshing evidence for kept ones

@~/.claude/_rules/03_authoring_guidelines/_claude_config_metadata.md

## 🚫 Common Mistakes & ✅ Hard Gates Checklist

- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_rules/_lazy_load/_common_mistakes.md` — before writing or reviewing a rule, for the mistakes this config has already shipped.
- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_rules/_lazy_load/_hard_gates_checklist.md` — before finishing or merging a rule, for the final tick-box check.
