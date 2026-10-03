# 🧠 AI Fluency — 4D Framework

Based on research by Dakan & Feller (via Anthropic's Claude 101 course), effective AI collaboration rests on four dimensions — and the playbook operationalises all of them.

| Dimension | What it means | Where it's addressed in the playbook |
|---|---|---|
| 🎯 **Delegation** | Deciding what work goes to AI vs human — matching tasks to the model's strengths and knowing when to stay in the loop | - [`delegating_to_subagent.md`](../../src/claude/_rules/05_lazy_load/delegating_to_subagent.md) (sub-agent selection)<br>- [`claude_plans.md`](../../src/claude/_rules/02_claude_standards/claude_plans.md) (plan mode gates)<br>- [`claude_operational_efficiency.md`](../../src/claude/_rules/04_claude_reference/claude_operational_efficiency.md) (sub-agent discipline) |
| 📝 **Description** | Communicating clearly — outputs, constraints, context, and desired behaviour | - [`claude_response_standards.md`](../../src/claude/_rules/01_essentials/claude_response_standards.md) (outline + assumptions before any code)<br>- [`behaviour.md`](../../src/claude/_rules/02_claude_standards/behaviour.md) (state "do not" constraints)<br>- [`authoring_skills.md`](../../src/claude/_rules/03_authoring_guidelines/authoring_skills.md) (trigger/output contract) |
| 🔍 **Discernment** | Critically evaluating AI outputs for quality, accuracy, and completeness — not treating responses as ground truth | - [`testing.md`](../../src/claude/_rules/05_lazy_load/testing.md)<br>- [`claude_plans.md`](../../src/claude/_rules/02_claude_standards/claude_plans.md) (plan review before execution) |
| 🛡️ **Diligence** | Responsible use — transparency, accountability, and ethical practice | - [`security.md`](../../src/claude/_rules/02_claude_standards/security.md)<br>- [`behaviour/_session_conduct.md`](../../src/claude/_rules/02_claude_standards/behaviour/_session_conduct.md) (honesty)<br>- [`behaviour.md` → Risky actions](../../src/claude/_rules/02_claude_standards/behaviour.md#-risky-actions) |

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
- [`authoring_skills.md`](../../src/claude/_rules/03_authoring_guidelines/authoring_skills.md) — maturity tiers (draft / tactical / strategic); strategic maturity requires evals to demonstrate reliability
- Simple evals (prompts only): [`skills/_admin_skills/archive_claude_config_snapshots/evals/`](../../src/claude/skills/_admin_skills/archive_claude_config_snapshots/evals/)
- Complex evals with fixtures: [`skills/_git_skills/git_review_pr/evals/`](../../src/claude/skills/_git_skills/git_review_pr/evals/)
- Behavioural tests: [`tests/skills/`](../../tests/skills/)
