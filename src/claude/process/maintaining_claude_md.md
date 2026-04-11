# Maintaining the Claude config

Claude automatically flags pruning candidates at the end of each session (see the **Pruning candidates** field in the wrap-up output). This doc describes the criteria it uses, so you can make an informed decision when a candidate is flagged.

---

## Criteria for removing a rule

A rule is a candidate for removal if any of the following apply:

- It was never relevant to anything done across recent sessions (low signal)
- It duplicates what a tool already enforces (ruff, shellcheck, sqlfluff, pre-commit hooks, test gates)
- It was added reactively for a one-off situation and no longer applies broadly
- It conflicts with another rule — resolve the conflict rather than keeping both

---

## What belongs in CLAUDE.md vs. a one-off prompt

| Belongs in CLAUDE.md | Use a one-off prompt instead |
|---|---|
| Standards that apply to every session (style, git, security) | Instructions specific to a single task |
| Persistent behaviour overrides (tone, caution level) | Context that will be stale after this session |
| Team conventions Claude cannot infer from the codebase | Reminders you only need once |

---

## Acting on a pruning candidate

1. Review the flagged rule in `src/claude/`
2. If you agree it should be removed, delete or consolidate it and raise a PR
3. Run `make test` to confirm no broken `@import` references
4. Run `make update` to sync the change to `~/.claude/`
