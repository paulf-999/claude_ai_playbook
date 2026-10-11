# Decisions — settings.json

## `defaultMode: plan`

Plan mode is the default. Prevents accidental execution on non-trivial tasks and forces
explicit approval before changes land.

## `autoMemoryEnabled: true`

Claude saves notable facts, preferences, and corrections to `~/.claude/memory/`
automatically. Keeps context coherent across sessions without manual invocation.

## `showClearContextOnPlanAccept: true`

Clears accumulated planning context after a plan is approved, keeping the implementation
window clean.

## Git and `gh` permissions

Auto-approved universally across all repos. Prompted on every git operation without
these, which creates friction on the most common dev workflow actions.

## `find:*`

Read-only filesystem search. Safe to auto-approve with no side-effect risk.
