# 🔄 Process

Instructions that govern how Claude structures its work within a session.

| File | Purpose | Imported | Status |
|------|---------|----------|--------|
| [`environment.md`](environment.md) | 🖥️ Declares the runtime environment: OS, shell, and primary tools | yes | active |
| [`planning.md`](planning.md) | 🗺️ Planning approach requirement, design principles, and plan catalogue — PLANS.md index, `YYYY-MM-DD_<keyword>` rename convention, and archive via `make clean_plans` | yes | active |
| [`session.md`](session.md) | 📋 Defines the start-of-session checklist (sub-agent selection, context load, planning mode) and end-of-session wrap-up | yes | active |
| [`permissions.md`](permissions.md) | 🔐 Permission model — what to suppress, what to keep, and why (read-only vs write, security concerns, `Bash(*:*)` anti-pattern) | yes | active |
| [`maintaining_claude_md.md`](maintaining_claude_md.md) | 🧹 Criteria for adding, updating, and removing rules from `CLAUDE.md` — what belongs vs. what should stay in a one-off prompt | yes | active |
| [`session_input.md`](session_input.md) | ⚙️ Pre-session configuration — set sub-agent and task before launching Claude to skip interactive prompts | no | active |
| [`task_brief.md`](task_brief.md) | 📋 Lean orchestration convention — task brief and output summary templates for delegating heavy file work to sub-agents | no | active |
| [`drafts.md`](drafts.md) | 📝 Draft file convention — root path `~/_drafts/`, subdirectory layout by type, and filename format | yes | active |
| [`graphify.md`](graphify.md) | 🔬 Graphify skill trigger — ensures `/graphify` invokes the Skill tool; persisted here so it survives playbook syncs | yes | active |
| [`sub_agent_selection.md`](sub_agent_selection.md) | 🤖 Sub-agent selection guidance — default agent, how to switch, and the full table of available sub-agents | yes | active |
