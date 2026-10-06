# Global Claude configuration

> 🚫 **Managed file** — do not edit directly. All changes belong in rule files, not here.
> - **Rule:** add behaviour by editing files in `rules/` or `_rules_lazy_load/` only — never inline
> - **Lazy load by default:** Claude Code loads every `.md` under `rules/` by itself, so domain-specific rules go in `_rules_lazy_load/` and are read on demand — or in `rules/04_path_scoped/` with `paths:` frontmatter, loading only with matching files. **Why:** every always-on rule consumes ~100-200 tokens per session regardless of task type. Load domain-specific rules only when actually needed to preserve context for the current task.
> - **Reset cadence:** Boris Cherny recommends resetting `~/.claude/` every ~6 months to prevent config bloat. Archive to `~/.claude_releases/` before resetting.
> - **Remember:** every file in `rules/` grows context — favour deliberate addition

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

<!-- Rules: every .md under rules/ loads natively — tiers 01–03 every session, 04_path_scoped/ when a matching file is read -->
<!-- Read-on-demand rules live in _rules_lazy_load/ and are never imported -->

---

## References

- [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/) — source of the Core Principles above
- [Boris Cherny — Steps of AI Adoption](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf) — source of `/batch`, `/goal`, `/loop` controls; engineer test heuristic; quality bar rule ([LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7483695059843043328/))
