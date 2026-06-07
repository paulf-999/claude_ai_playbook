# 🔀 Orchestration decision guide

Use this flowchart before reaching for sub-agents or multi-step orchestration patterns.
Every added pattern is an added failure mode — the goal is the simplest thing that works.

```mermaid
flowchart TD
    A([Task received]) --> B{"Can a single\nwell-prompted call\nanswer this?"}

    B -- Yes --> C([Single call — stop here])

    B -- No --> D{"Requires parallelism\nor context isolation?"}

    D -- No --> C

    D -- Yes --> E{"Reads >3 files,\nedits across >1 directory,\nor search → edit cycle?"}

    E -- Yes --> F["Task brief pattern\n─────────────────\nWrite /tmp/task_brief_slug.md\nDelegate to sub-agent\nRead /tmp/task_output_slug.md only\n(do not re-read files the sub-agent processed)"]

    E -- No --> G[Direct sub-agent spawn]

    F --> H["Brief fully\n─────────────────\nGoal · surrounding context\nWhat has already been tried\nExpected output shape\n\nSub-agent has no memory of this\nconversation — never write\n'based on our conversation'"]

    G --> H
```

## Related

- [Sub-agents](sub_agents.md) — which sub-agent to use for a given task
- [`rules/cost_efficiency.md`](../../../src/claude/rules/cost_efficiency.md) — the underlying rules this diagram visualises
