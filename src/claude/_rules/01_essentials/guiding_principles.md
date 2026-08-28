# 🧭 Guiding Principles — Claude Config

**Purpose:** Establish decision-making principles that prevent configuration bloat and ensure every setting, hook, and import justifies its token cost.

Configuration principles that govern all decisions about settings, hooks, imports, and automation.

## 📋 Contents

- [How to gather usage evidence](#-how-to-gather-usage-evidence)

---

| Principle | Description | Rationale | How to apply |
|-----------|-------------|-----------|--------------|
| **Lazy-load by default** | Don't import or auto-inject context. Load on-demand only when actively needed. | Context is finite; baseline bloat limits capability. Every import/injection has a token cost. | New features: off by default; enable explicitly. Imports: only when directly referenced. Hooks: fire on specific events, not every session. |
| **Explicit over implicit** | Avoid silent automation. Prefer visible choices and active confirmation over magic behavior. | Hidden behavior is hard to debug and audit. Surprises waste context. | Hooks should announce what they're doing. Settings should be obvious. Defaults should be minimal. |
| **Context efficiency is non-negotiable** | Every setting, hook, and import must justify its cost in tokens vs. actual value delivered. Measure, don't assume. | Wasted context = wasted reasoning capability for the task at hand. | Before adding a hook/import/setting: estimate tokens. Before keeping one: verify it's actively used. Audit regularly. |
| **Intentionality gates everything** | A feature (hook, setting, import, alias) only exists if it solves a real, recurring problem. Convenience alone is not sufficient. | Config bloat is cumulative and silent — a hundred "nice-to-haves" becomes noise. | Reject speculation ("might be useful someday"). Require evidence: "I've used this N times and it saved me X minutes." For guidance on tracking usage, see **How to gather usage evidence** below. |
| **Reversible by design** | New features should be easy to add and remove; assume you'll experiment and refine. Don't optimize for permanence. | Configuration evolves; locked-in decisions prevent iteration. Easy removal lowers the barrier to trying something. | Comment out before deleting. Test removal for side effects. Keep hooks small and single-purpose so removal is safe. |
| **Goal-driven design** | Align your config to your current long-term work goals, not comprehensive coverage. Ruthlessly prune during resets. | Config designed for "all scenarios" becomes noise and bloat. Periodic resets are opportunities to re-align to what matters now. | During 6-month resets: audit every rule, hook, import. For each: "Does this serve my current work?" Lazy-load or archive anything not immediately relevant. Refocus on work goals. |
| **Automation ROI** | Only automate (hooks, skills, commands) when cost justifies frequency. Manual 10 min < Claude 2 min + $5. | "Automation is free" is false. A $5 hook saves money only if frequency justifies setup cost. Calculate actual ROI. | Before adding automation: estimate manual time × frequency/month. If (manual time/month) < (automation setup + monthly API cost), stay manual. Hooks used 5+ times/month? Likely ROI-positive. Quarterly? Probably not. |

---

## 📊 How to gather usage evidence

When reviewing features for intentionality, ask: "Have I actually used this, or am I protecting against a hypothetical problem?"

### Evidence collection methods

| Method | When to use | Example |
|--------|-----------|---------|
| **Session count** | Estimate recurring use across recent sessions | "I've used `/faster-mode` in 5 of the last 10 sessions" |
| **Time saved** | Quantify the benefit when you removed friction | "This alias saved ~2 min per workflow (vs. typing it out)" |
| **Problem statement** | Articulate the real problem the feature solves | "`/fewer-permission-prompts` eliminates 3-5 permission dialogs per session" |
| **Absence test** | Disable the feature and see if you miss it | "I disabled the alias and re-enabled it 3 times in a week" |
| **Replacement cost** | How much effort would the manual alternative take? | "Without this hook, I'd need to re-type this config every session" |

### Red flags (suggests the feature might be speculative)

- ❌ "Might be useful someday" — no concrete use case yet
- ❌ "Could save time if..." — hypothetical benefit, not proven
- ❌ "Good to have in case..." — defending against edge cases not yet hit
- ❌ "Just added it last week" — no real-world feedback yet
- ❌ "Nobody complained about it" — absence of complaint ≠ presence of value

### How to document evidence

When adding a feature or deciding to keep it:

```markdown
## Usage evidence

- **Problem:** [What real, recurring problem does this solve?]
- **Frequency:** [How often is it used? Recent session count?]
- **Friction removed:** [What's the alternative without this feature? How much time/effort saved?]
- **First use date:** [When was this first added/enabled?]
```

### Audit cadence

- **Monthly:** Quick scan — any obviously unused features?
- **Quarterly:** Deep review — spot-check recent session transcripts for evidence of actual use
- **Annually:** Reset decision — per Boris Cherny, archive and reset `~/.claude/` every ~6 months to force intentionality review
