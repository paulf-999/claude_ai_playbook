<!-- version: 1.0.0 -->
<!-- created: 2026-10-17 -->
<!-- updated: 2026-10-17 -->
<!-- miss_cost: low — a feature kept or added without evidence it gets used -->
<!-- loading: lazy — only matters when adding or keeping a config feature, so a pointer in guiding_principles.md loads it then -->
# 📊 Usage Evidence

**Purpose:** Show a config feature solves a real, recurring problem before adding or keeping it, per the intentionality principle in `guiding_principles.md`.

When reviewing features for intentionality, ask: "Have I actually used this, or am I protecting against a hypothetical problem?"

---

## Evidence collection methods

| Method | When to use | Example |
|--------|-----------|---------|
| 🔢 **Session count** | • **Use when:** estimating recurring use across recent sessions. | • **Example:** "I've used `/faster-mode` in 5 of the last 10 sessions." |
| ⏱️ **Time saved** | • **Use when:** quantifying the benefit of removed friction. | • **Example:** "This alias saved ~2 min per workflow (vs. typing it out)." |
| ❓ **Problem statement** | • **Use when:** articulating the real problem the feature solves. | • **Example:** "`/fewer-permission-prompts` eliminates 3–5 permission dialogs per session." |
| 🫥 **Absence test** | • **Use when:** checking whether you'd miss the feature once disabled. | • **Example:** "I disabled the alias and re-enabled it 3 times in a week." |
| 🔁 **Replacement cost** | • **Use when:** weighing the effort of the manual alternative. | • **Example:** "Without this hook, I'd need to re-type this config every session." |

## Red flags (suggests the feature might be speculative)

- ❌ "Might be useful someday" — no concrete use case yet
- ❌ "Could save time if..." — hypothetical benefit, not proven
- ❌ "Good to have in case..." — defending against edge cases not yet hit
- ❌ "Just added it last week" — no real-world feedback yet
- ❌ "Nobody complained about it" — absence of complaint ≠ presence of value

## How to document evidence

When adding a feature or deciding to keep it:

```markdown
## Usage evidence

- **Problem:** [What real, recurring problem does this solve?]
- **Frequency:** [How often is it used? Recent session count?]
- **Friction removed:** [What's the alternative without this feature? How much time/effort saved?]
- **First use date:** [When was this first added/enabled?]
```

## Audit cadence

- **Monthly:** Quick scan — any obviously unused features?
- **Quarterly:** Deep review — spot-check recent session transcripts for evidence of actual use
- **Every ~6 months:** Reset decision — per Boris Cherny, archive and reset your Claude config directory to force intentionality review
