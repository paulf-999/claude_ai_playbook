# 📁 Plan-mode output location

**Purpose:** Document where Claude Code writes plan-mode files and why, so the setting isn't
mistaken for something a rule/CLAUDE.md instruction controls.

## Setting

`plansDirectory` in `settings.json` is set to `~/claude/_plans` (global, in
`~/claude/settings.json`).

## Why this needs to live in settings.json, not a behavioral rule

The plan-file path is injected by the Claude Code harness via a system reminder before the
model runs — it is not something the model decides or a rule can redirect. Changing it requires
the `plansDirectory` key; documenting it here is for reference only, not enforcement.

## Related rules

- `guiding_principles.md` — lazy-load by default; this is domain-specific, not always-on
- `claude_rule_loading_strategy.md` — placement rationale for `04_lazy_load/`
