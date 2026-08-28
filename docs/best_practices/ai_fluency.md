# 🧠 AI Fluency — 4D Framework

Based on research by Dakan & Feller (via Anthropic's Claude 101 course), effective AI collaboration rests on four dimensions — and the playbook operationalises all of them.

| Dimension | What it means | Where it's addressed in the playbook |
|---|---|---|
| 🎯 **Delegation** | Deciding what work goes to AI vs human — matching tasks to the model's strengths and knowing when to stay in the loop | - [`process/sub_agent_selection.md`](../../src/claude/process/sub_agent_selection.md) (sub-agent selection)<br>- [`process/planning.md`](../../src/claude/process/planning.md) (plan mode gates)<br>- [`rules/cost_efficiency.md`](../../src/claude/rules/cost_efficiency.md) (sub-agent discipline) |
| 📝 **Description** | Communicating clearly — outputs, constraints, context, and desired behaviour | - [`process/planning.md`](../../src/claude/process/planning.md) (outline + assumptions before any code)<br>- [`rules/behaviour/general.md`](../../src/claude/rules/behaviour/general.md) (state "do not" constraints)<br>- [`rules/skill_standards.md`](../../src/claude/rules/skill_standards.md) (trigger/output contract) |
| 🔍 **Discernment** | Critically evaluating AI outputs for quality, accuracy, and completeness — not treating responses as ground truth | - [`rules/testing.md`](../../src/claude/rules/testing.md)<br>- [`process/planning.md`](../../src/claude/process/planning.md) (plan review before execution) |
| 🛡️ **Diligence** | Responsible use — transparency, accountability, and ethical practice | - [`rules/security.md`](../../src/claude/rules/security.md)<br>- [`rules/transparency.md`](../../src/claude/rules/transparency.md)<br>- [`rules/behaviour/risky_actions.md`](../../src/claude/rules/behaviour/risky_actions.md) |

---

## Evaluating Claude for your workflows

Most prompts work well on the first try. Some don't. Before you depend on Claude for a recurring workflow, spend thirty minutes running a simple evaluation — it will tell you where Claude excels, where it needs guidance, and where a human must stay in the loop.

**The approach:**

1. **Gather examples** — pull 5–10 real instances of the task: past outputs, representative cases, and at least one or two edge cases that matter.
2. **Write test prompts** — write prompts that would produce similar outputs for each example, as if you were asking Claude for the first time.
3. **Compare honestly** — does it capture the key information? Is the tone right? What did it miss or get wrong? What surprised you?
4. **Refine** — tighten the prompt, add examples, and flag the steps where human review is non-negotiable before this goes anywhere near production.

No tooling needed. No scoring framework. Just an honest read on quality and failure modes before you commit to relying on the output.

**In this repo:**

The playbook has a mature eval infrastructure for skills. Whether you're building something new or assessing an existing workflow, these are worth reading:

- [`style_guide_standards/claude.md`](../../src/claude/style_guide_standards/claude.md) — the full skill development cycle (create → eval → improve → benchmark) and when evals become mandatory
- [`rules/skill_standards.md`](../../src/claude/rules/skill_standards.md) — maturity tiers (draft / tactical / strategic); strategic maturity requires evals to demonstrate reliability
- Simple evals (prompts only): [`skills/_admin_skills/archive_claude_config_snapshots/evals/`](../../src/claude/skills/_admin_skills/archive_claude_config_snapshots/evals/)
- Complex evals with fixtures: [`skills/_git_skills/git_review_pr/evals/`](../../src/claude/skills/_git_skills/git_review_pr/evals/)
- Behavioural tests: [`tests/skills/`](../../tests/skills/)
