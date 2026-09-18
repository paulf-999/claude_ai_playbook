# Global Claude configuration

> 🚫 **Managed file** — do not edit directly. All changes belong in imported rule files, not here.
> - **Rule:** add behaviour by editing imported files only — never inline
> - **Lazy load by default:** domain-specific rules go in `_rules/05_lazy_load/` — never imported, read on demand. `_rules/05_lazy_load/` is the only subdirectory that is never imported. **Why:** every imported rule consumes ~100-200 tokens per session regardless of task type. Load domain-specific rules only when actually needed to preserve context for the current task.
> - **Reset cadence:** Boris Cherny recommends resetting `~/.claude/` every ~6 months to prevent config bloat. Archive to `~/.claude_releases/` before resetting.
> - **Remember:** every import grows context — favour deliberate addition

## Core Principles

*Adapted from [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/)*

1. **Don't assume. Don't hide confusion. Surface tradeoffs.**
2. **Minimum code that solves the problem. Nothing speculative.**
3. **Touch only what you must. Clean up only your own mess.**
4. **Define success criteria. Loop until verified.**

### Why "don't assume" needs a specific rule

Abstract principles get rationalized — "don't assume" is easy to override with a
plausible internal justification (e.g. "resume means continue the work"). Specific
constraints are harder to bypass silently.

- **Problem:** Claude infers intent from context and acts — filling gaps rather than surfacing them.
- **Rule:** If any detail, requirement, or architecture choice is unclear, ask one clarifying question before writing code or making changes.

## Imports

<!-- User context: cross-project memories (preferences, corrections, project facts) -->
@~/.claude/memory/MEMORY.md
<!-- Quick-reference command/skill shortcuts table -->
@~/.claude/aliases.md

<!-- Tier 1: 01_essentials/ — foundational principles and user-facing conventions -->
<!-- Response format, delivery cadence, and timing footer — user-facing output contract -->
@~/.claude/_rules/01_essentials/claude_response_standards.md
<!-- Entry point for naming, writing style, and directory structure conventions -->
@~/.claude/_rules/01_essentials/claude_usage_standards.md
<!-- Foundational decision-making principles: lazy-load, intentionality, context efficiency -->
@~/.claude/_rules/01_essentials/guiding_principles.md

<!-- Tier 2: 02_claude_standards/ — blocking standards and enforcement -->
<!-- Safety-critical: ask-first gates, decision-making, risky-action handling -->
@~/.claude/_rules/02_claude_standards/behaviour.md
<!-- Phase-gate rules for multi-phase plans and plan-mode execution -->
@~/.claude/_rules/02_claude_standards/claude_plans.md
<!-- Git workflow: commits, branch naming, PR standards, safe patterns -->
@~/.claude/_rules/02_claude_standards/git.md
<!-- Blocks hardcoded filesystem paths in hooks/tests that silently break on other configs -->
@~/.claude/_rules/02_claude_standards/portable_paths.md
<!-- Secure coding practices and Claude's own prompt-injection/secret-handling guardrails -->
@~/.claude/_rules/02_claude_standards/security.md
<!-- Test quality/complexity scoring standard required on every test file -->
@~/.claude/_rules/02_claude_standards/test_metadata.md
<!-- Requires tests for all new features and enforcement rules -->
@~/.claude/_rules/02_claude_standards/testing.md

<!-- Tier 3: 03_authoring_guidelines/ — meta-guidance for authoring rules, skills, agents -->
<!-- Standards for creating new sub-agents (naming, structure, maturity) -->
@~/.claude/_rules/03_authoring_guidelines/authoring_agents.md
<!-- Standards for creating new rule files (placement, testing, scope) -->
@~/.claude/_rules/03_authoring_guidelines/authoring_rules.md
<!-- Standards for creating new skills (contract, triggers, maturity) -->
@~/.claude/_rules/03_authoring_guidelines/authoring_skills.md

<!-- Tier 4: 04_claude_reference/ — system knowledge and platform guidance -->
<!-- Token/turn discipline: when to delegate, parallelize, or spawn sub-agents -->
@~/.claude/_rules/04_claude_reference/claude_operational_efficiency.md
<!-- Decision tree for always-on vs. lazy-load rule placement -->
@~/.claude/_rules/04_claude_reference/claude_rule_system/claude_rule_loading_strategy.md

---

## References

- [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/) — source of the Core Principles above
- [Boris Cherny — Steps of AI Adoption](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf) — source of `/batch`, `/goal`, `/loop` controls; engineer test heuristic; quality bar rule ([LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7483695059843043328/))
