# Global Claude configuration

> ⚠️ **Managed file** — do not edit directly.
> - **Rule:** add behaviour by editing imported files only — never inline
> - **Lazy load by default:** domain-specific rules go in `_rules/04_lazy_load/` — never imported, read on demand. `_rules/04_lazy_load/` is the only subdirectory that is never imported. **Why:** every imported rule consumes ~100-200 tokens per session regardless of task type. Load domain-specific rules only when actually needed to preserve context for the current task.
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

<!-- Root level: personal context and shortcuts -->
@~/.claude/memory/MEMORY.md
@~/.claude/aliases.md

<!-- Tier 1: 01_essentials/ — foundational principles and user-facing conventions -->
@~/.claude/_rules/01_essentials/authoring_rules.md
@~/.claude/_rules/01_essentials/authoring_skills.md
@~/.claude/_rules/01_essentials/conventions/claude_directory_structure.md
@~/.claude/_rules/01_essentials/conventions/naming_standards.md
@~/.claude/_rules/01_essentials/conventions/writing_style.md
@~/.claude/_rules/01_essentials/guiding_principles.md

<!-- Tier 2: 02_claude_standards/ — blocking standards and enforcement -->
@~/.claude/_rules/02_claude_standards/behaviour.md
@~/.claude/_rules/02_claude_standards/git.md
@~/.claude/_rules/02_claude_standards/security.md
@~/.claude/_rules/02_claude_standards/testing.md

<!-- Tier 3: 03_claude_reference/ — system knowledge and platform guidance -->
@~/.claude/_rules/03_claude_reference/claude_operational_efficiency.md
@~/.claude/_rules/03_claude_reference/_claude_rule_system/claude_rule_loading_strategy.md

---

## References

- [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/) — source of the Core Principles above
- [Boris Cherny — Steps of AI Adoption](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf) — source of `/batch`, `/goal`, `/loop` controls; engineer test heuristic; quality bar rule ([LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7483695059843043328/))
