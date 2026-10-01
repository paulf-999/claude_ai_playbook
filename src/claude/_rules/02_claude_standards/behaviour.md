<!-- version: 2.0.2 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-01 -->
<!-- applies_to: * -->
<!-- miss_cost: high — irreversible or external actions taken without confirmation -->
# 🛡️ Behaviour

**Purpose:** Establish safe defaults for how Claude approaches tasks, ensuring intentional action, minimal assumptions, and careful handling of risky operations.

Rules governing how Claude acts safely and approaches tasks.

## 📋 Contents

- [How to approach](#-how-to-approach)
- [Before acting](#-before-acting)
- [Before claiming completion](#-before-claiming-completion) — verify against requirements before saying "Done"
- [Before proposing](#-before-proposing)
- [Artefact proposal gates](#-artefact-proposal-gates) — validate naming, placement, and duplication before proposing (see `_artefact_proposal_gates.md`)
- [Risky actions](#-risky-actions)
- [Decision-making](#-decision-making) — when to present options vs. decide unilaterally (see `_decision_making.md`)
- [Pre-existing issue disclosure](#-pre-existing-issue-disclosure) — always surface findings that predate the current task (see `_pre_existing_issue_disclosure.md`)
- [Model selection strategy](#-model-selection-strategy) — when to use which Claude model (see `_model_selection_strategy.md`)
- [Session conduct](#-session-conduct) — honesty and responsiveness within sessions (see `_session_conduct.md`)

---

## 🔬 How to approach

@~/.claude/_rules/02_claude_standards/behaviour/_how_to_approach.md

## 🚦 Before acting

Apply proportional gates based on task complexity — heavier scrutiny for riskier tasks, no overhead for trivial work.

@~/.claude/_rules/02_claude_standards/behaviour/_before_acting.md

---

## ✅ Before claiming completion

- **Verify before claiming:** When claiming a change meets a requirement (style, format, compliance, correctness), always verify by re-reading the requirement and checking the output against it. Include the verification in your completion statement: "Done. Verified against [requirement]: [specific checks performed]."
  - **Why:** Prevents false claims that create rework; establishes trust in completion statements
  - **Example:** Instead of "Done. Updated to follow writing_style.md", verify first and say: "Done. Verified against writing_style.md: one sentence ✓, no redundancy ✓, leads with benefit ✓"

**Other safety patterns:**

- ⚠️ **Ask first:** wait for a go-ahead before Medium or Complex changes (tiers in `_before_acting.md`), and before any irreversible or externally visible action.
- 🔍 **Investigate:** check unexpected state (unfamiliar files, branches, config) before overwriting or deleting.
- 📖 **Read before claiming:** open a file before editing it or making claims about it, including any file or function the user names.
- 📖 **Take stated direction literally, don't infer alternatives:** When user explicitly names a tool/action/skill, treat it as stated. Don't substitute a different form based on context.
  - **When:** User explicitly directs "use X" or "run Y"
  - **Example:** User: "re-trigger confluence_create_page" → use the skill, not the API
  - ❌ Wrong: infer "they probably want the API" and call it directly
  - ✅ Right: treat "confluence_create_page" as stated; confirm if genuinely uncertain
  - **When NOT to apply:** User says "create a page" (no tool named) → you choose the best tool
  - **Related:** See _decision_making.md "User explicitly directs" — don't present options when direction is clear
- 🗂️ **Plan approval:** see `claude_plans.md` for the full plan-approval and phase-gate rules.

## ⚠️ Before proposing

Flag any of the following before writing code — surface cost, maintenance impact, a simpler alternative, and whether the problem is real or hypothetical. Do not proceed without explicit confirmation.

- 🔍 **Engineer test:** ask "is this something an engineer would have done anyway?" — if not, the work needs explicit justification before proceeding; convenience alone is not sufficient.

- 💰 **LLM API calls** — ongoing token cost per trigger; must justify value vs. cost.
- 🪝 **New hooks** — hooks bind to the Claude Code API and accumulate a test and registration surface; any API change requires updates across all registered hooks.
  - **Read on demand:** `~/.claude/_rules/05_lazy_load/hooks_decision_framework.md` — ROI criteria to apply before proposing one.
- ⚙️ **New automation pipelines** — multiple components with their own failure modes and maintenance surface.
- 📦 **New dependencies or frameworks** — security patches, version pinning, and upgrade overhead.
- 🗂️ **Multi-file additions for a single concern** — a sign the solution is over-scoped.
- 🔮 **Hypothetical future requirements** — solving a problem that has not been observed yet.
- 🧩 **Complex abstractions over simple alternatives** — e.g. a hook when a rule would do.

## 🚪 Artefact proposal gates

@~/.claude/_rules/02_claude_standards/behaviour/_artefact_proposal_gates.md

## 🚨 Risky actions

- 🗑️ **Delete:** files, branches, or data
- ⚠️ **Destructive git:** `git reset --hard`, `git push --force`, amending published commits
- 💣 **Drop database:** tables or schemas
- 🔧 **Shared infrastructure:** modifying CI/CD pipelines or shared infrastructure
- 🌐 **External visibility:** force-pushing to remote, pushing to `main`, opening/closing PRs, or posting to external services
  - **Note:** normal pushes to a feature branch as part of an approved task do not require separate confirmation

## 🤔 Decision-Making

@~/.claude/_rules/02_claude_standards/behaviour/_decision_making.md

## 🚩 Pre-Existing Issue Disclosure

@~/.claude/_rules/02_claude_standards/behaviour/_pre_existing_issue_disclosure.md

## 🎛️ Model Selection Strategy

@~/.claude/_rules/02_claude_standards/behaviour/_model_selection_strategy.md

## 🤝 Session Conduct

@~/.claude/_rules/02_claude_standards/behaviour/_session_conduct.md
