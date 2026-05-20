# WIP Hooks

Hooks in this file are at `wip` status — registered in `settings.json` but behaviour is not yet as expected.
Location: `src/claude/wip/hooks/`. All fire automatically via lifecycle events; no manual invocation.

← [Back to REGISTRY.md](../REGISTRY.md)

| Hook | Lifecycle | Maturity | Criticality | Tested | Status | Notes |
|---|---|---|---|---|---|---|
| `claude_session_cost.py` | Stop | draft | should | no | wip | Output (`💰 session: $X.XXXX`) not surfaced clearly enough. Needs rework. |
| `claude_prompt_reviewer.py` | UserPromptSubmit | draft | should | [yes](../../../tests/hooks/test_claude_prompt_reviewer.py) | wip | Low-severity tips are silent (`additionalContext` not visible to user). Needs rework. |
