<!-- version: 1.1.2 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-01 -->
<!-- applies_to: **/claude/**, **/.claude/** -->
<!-- miss_cost: medium — config bloat the user later has to prune -->
# 🧭 Guiding Principles — Claude Config

**Purpose:** Establish decision-making principles that prevent configuration bloat and ensure every setting, hook, and import justifies its token cost.

Configuration principles that govern all decisions about settings, hooks, imports, and automation.

| Principle | Description | Rationale | How to apply |
|-----------|-------------|-----------|--------------|
| **Lazy-load by default** | • **Default:** don't import or auto-inject context.<br>• **On demand:** load only when actively needed. | • **Finite context:** baseline bloat limits capability.<br>• **Cost:** every import or injection has a token cost.<br>• **Imports aren't free:** `@` imports load at launch, so splitting a file into imports organises it but saves no context. | • **New features:** off by default, enabled explicitly.<br>• **Imports:** only when directly referenced.<br>• **Hooks:** fire on specific events, not every session.<br>• **Path-scoped rules:** prefer `paths:` frontmatter for a rule tied to one file type, so it loads only when Claude reads a matching file. |
| **Explicit over implicit** | • **Default:** avoid silent automation.<br>• **Prefer:** visible choices and active confirmation over magic behaviour. | • **Debuggability:** hidden behaviour is hard to debug and audit.<br>• **Cost:** surprises waste context. | • **Hooks:** announce what they're doing.<br>• **Settings:** should be obvious.<br>• **Defaults:** should be minimal. |
| **Context efficiency is non-negotiable** | • **Justify cost:** every setting, hook and import must justify its token cost against the value delivered.<br>• **Measure:** measure, don't assume. | • **Cost:** wasted context means wasted reasoning capability for the task at hand. | • **Before adding:** estimate the tokens of a hook, import or setting.<br>• **Before keeping:** verify it's actively used.<br>• **Size target:** keep each CLAUDE.md, rule and imported file under 200 lines, because longer files lower adherence ([memory docs](https://code.claude.com/docs/en/memory)).<br>• **Audit:** review regularly with `/doctor prompt-audit`. |
| **Right mechanism for the job** | • **CLAUDE.md:** facts Claude needs in every session.<br>• **Path-scoped rule:** guidance for one part of the codebase or one file type.<br>• **Skill:** multi-step procedures run on demand.<br>• **Hook or permission setting:** anything that must happen every time. | • **Context, not enforcement:** CLAUDE.md guides Claude but can't enforce anything ([memory docs](https://code.claude.com/docs/en/memory)). | • **Before adding:** ask whether the need is a fact, scoped guidance, a procedure or a guarantee.<br>• **Must-happen:** move it out of prose and into a hook or permission setting. |
| **Intentionality gates everything** | • **Real problem:** a feature (hook, setting, import, alias) only exists if it solves a real, recurring problem.<br>• **Not enough:** convenience alone is not sufficient. | • **Silent bloat:** config bloat is cumulative and silent — a hundred "nice-to-haves" becomes noise. | • **Reject speculation:** "might be useful someday" is not a reason.<br>• **Require evidence:** "I've used this N times and it saved me X minutes."<br>• **Tracking usage:** see **How to gather usage evidence** below. |
| **Reversible by design** | • **Easy in, easy out:** new features should be easy to add and remove.<br>• **Expect iteration:** assume you'll experiment and refine.<br>• **Not permanent:** don't optimise for permanence. | • **Evolution:** configuration evolves, and locked-in decisions prevent iteration.<br>• **Low barrier:** easy removal lowers the barrier to trying something. | • **Comment out:** before deleting.<br>• **Test removal:** check for side effects.<br>• **Small hooks:** keep hooks small and single-purpose so removal is safe. |
| **Goal-driven design** | • **Alignment:** align your config to your current long-term work goals, not comprehensive coverage.<br>• **Prune:** ruthlessly prune during resets. | • **Noise:** config designed for "all scenarios" becomes noise and bloat.<br>• **Resets:** periodic resets are opportunities to re-align to what matters now. | • **6-month resets:** audit every rule, hook and import.<br>• **Question:** for each, ask "Does this serve my current work?"<br>• **Archive:** lazy-load or archive anything not immediately relevant.<br>• **Refocus:** re-centre on work goals. |
| **Automation ROI** | • **Frequency:** only automate (hooks, skills, commands) when cost justifies frequency.<br>• **Example:** manual 10 min < Claude 2 min + $5. | • **Myth:** "automation is free" is false.<br>• **Payback:** a $5 hook saves money only if frequency justifies setup cost.<br>• **Calculate:** work out the actual ROI. | • **Estimate:** manual time × frequency per month.<br>• **Threshold:** if manual time per month < automation setup + monthly API cost, stay manual.<br>• **5+ uses a month:** likely ROI-positive.<br>• **Quarterly use:** probably not. |
| **Progressive Maturation** | • **Progression:** structure everything (features, rules, implementations, hardening) with an explicit crawl → walk → run progression.<br>• **Restraint:** don't over-build prematurely. | • **Crawl:** minimal, gets it working.<br>• **Walk:** add guardrails, validation and tests.<br>• **Run:** harden, optimise, productionise.<br>• **Intentional stops:** stopping at any stage is deliberate, and you validate before advancing. | • **Start at crawl:** any new artefact (rule, skill, hook, feature) begins as an MVP with minimal scope.<br>• **Walk criteria:** define tests and validation.<br>• **Run criteria:** define hardened, production-ready standards.<br>• **Advance:** only when criteria are met.<br>• **Defer:** ambitions beyond the current stage. |
| **Progressive Disclosure** | • **Structure:** present all information (documentation, explanations, proposals, rule and skill definitions) with progressive disclosure.<br>• **Layers:** opening = complete idea, first section = enough to act, later sections = advanced detail. | • **Reader time:** progressive disclosure respects reader time and preserves context for decision-making.<br>• **Optional depth:** the opening and first section are enough to act, and detail is available but not forced. | • **Plans and proposals:** opening = what, first = how, later = alternatives.<br>• **Explanations:** opening = answer, first = path to answer, later = deep rationale.<br>• **Rules and skills:** opening = principle, first = when/how, later = examples.<br>• **Documentation:** opening = purpose, first = quick start, later = advanced usage. |
| **False truth rots silently** | • **Drift:** specific lists drift from reality and mislead without warning.<br>• **Principles:** document principles instead and point to authoritative sources.<br>• **Priority:** maintainability > exhaustiveness. | • **False confidence:** comprehensive-looking but unmaintained documentation creates false confidence.<br>• **Wrong assumptions:** when real state silently diverges from documented state, readers act on stale information. | • **No exhaustive lists:** never maintain file trees, all possible options or complete catalogues.<br>• **Instead:** document the *principle* governing organisation, then point to a current authoritative source (e.g. README.md, live config file).<br>• **Example:** explain the tier system and link to README.md files rather than maintaining a full directory tree.<br>• **Contradictions:** when two instructions conflict Claude may follow either, so remove conflicts during audits. |

---

## 📊 How to gather usage evidence

When reviewing features for intentionality, ask: "Have I actually used this, or am I protecting against a hypothetical problem?"

### Evidence collection methods

| Method | When to use | Example |
|--------|-----------|---------|
| **Session count** | • **Use when:** estimating recurring use across recent sessions. | • **Example:** "I've used `/faster-mode` in 5 of the last 10 sessions." |
| **Time saved** | • **Use when:** quantifying the benefit of removed friction. | • **Example:** "This alias saved ~2 min per workflow (vs. typing it out)." |
| **Problem statement** | • **Use when:** articulating the real problem the feature solves. | • **Example:** "`/fewer-permission-prompts` eliminates 3–5 permission dialogs per session." |
| **Absence test** | • **Use when:** checking whether you'd miss the feature once disabled. | • **Example:** "I disabled the alias and re-enabled it 3 times in a week." |
| **Replacement cost** | • **Use when:** weighing the effort of the manual alternative. | • **Example:** "Without this hook, I'd need to re-type this config every session." |

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
- **Every ~6 months:** Reset decision — per Boris Cherny, archive and reset your Claude config directory to force intentionality review
