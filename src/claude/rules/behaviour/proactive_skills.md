# 🎯 Rules — Proactive skill dispatch

When a user request matches the contextual trigger of an installed skill, invoke the skill
rather than answering inline. Skill output is more structured and consistent than ad hoc prose.

## 🔍 Analysis skills — dispatch table

| If the user... | Invoke |
|---|---|
| Wants to stress-test a plan, find what could kill it, or work backwards from failure | `/premortem` |
| Wants adversarial critique, to find weaknesses, or to tear an idea apart | `/redteam` |
| Wants to surface implementation traps, hidden risks, or what they might be missing | `/pitfalls` |
| Is choosing between two or more options, tools, or approaches | `/compare` |
| Wants to question inherited assumptions or rebuild reasoning from scratch | `/first-principles` |
| Needs a short stakeholder-ready summary for Slack, email, or Confluence | `/exec-summary` |

## ⚠️ When not to dispatch

- The user has already invoked the skill explicitly — do not re-invoke it.
- The request is a narrow, one-sentence question — a skill invocation would be overkill.
- The context is mid-task (e.g. "what could go wrong with this SQL join?") — answer inline;
  reserve dispatch for whole-plan or whole-proposal analysis.
