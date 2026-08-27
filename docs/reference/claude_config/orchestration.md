# 🔀 Orchestration decision guide

Use this flowchart before reaching for sub-agents or multi-step orchestration patterns.
Every added pattern is an added failure mode — the goal is the simplest thing that works.

```mermaid
flowchart TD
    A([Task received]) --> B{"Can a single\nwell-prompted call\nanswer this?"}

    B -- Yes --> C([Single call — stop here])

    B -- No --> D{"Requires parallelism\nor context isolation?"}

    D -- No --> C

    D -- Yes --> G[Direct sub-agent spawn]

    G --> H["Brief fully\n─────────────────\nGoal · surrounding context\nWhat has already been tried\nExpected output shape\n\nSub-agent has no memory of this\nconversation — never write\n'based on our conversation'"]
```

## Related

- [Sub-agents](sub_agents.md) — which sub-agent to use for a given task
- [`rules/cost_efficiency.md`](../../../src/claude/rules/cost_efficiency.md) — the underlying rules this diagram visualises
