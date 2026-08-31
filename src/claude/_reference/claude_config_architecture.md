# 🏗️ Claude Config Architecture & Design Patterns

**Purpose:** Reference guide to your global Claude config's structural and design decisions. Use when understanding how rules fit together — or when deciding where to add features, whether to automate, and how to keep config lean.

---

## 🎯 Design Philosophy: Seven Guiding Principles

The Claude config is built on **seven guiding principles** (from `guiding_principles.md`):

| Principle | How it shapes config |
|---|---|
| **Lazy-load by default** | Rules imported at session start are baselined; domain-specific rules loaded on-demand via `lazy_load/` |
| **Explicit over implicit** | Every rule is listed in CLAUDE.md with a comment explaining its purpose; no silent automation |
| **Context efficiency** | Token cost is tracked; broad imports are flagged during review; unused features are retired |
| **Intentionality** | Features exist because they solve real, recurring problems — not "nice to have" |
| **Reversible by design** | Rules are small, single-purpose; can be commented out or deleted without side effects |
| **Goal-driven design** | Align config to current work goals, ruthlessly prune during 6-month resets; don't build for "all scenarios" |
| **Automation ROI** | Only automate (hooks, skills, commands) when cost is justified by frequency; calculate actual payback period |

---

## 🎯 New Principles: B & C (Goal-Driven Design + Automation ROI)

### Principle B: Goal-Driven Design

**Pattern:** Align config to current work goals; ruthlessly prune during 6-month resets.

**Why:** Config designed for "all scenarios" becomes noise and bloat. Every unused rule wastes tokens. Periodic resets are opportunities to re-align to what matters *now*.

**How it works:**
- Every 6 months (per Boris Cherny), archive and reset `~/.claude/`
- During reset: audit every rule — "Have I used this in the last 6 months? Does it serve my current work?"
- Keep only what's actively needed
- Move unused rules to lazy-load or archive

**Gotcha:** Don't mistake "comprehensive" for "good." Lean config beats complete config.

### Principle C: Automation ROI

**Pattern:** Only automate (hooks, skills, commands) when cost is justified by frequency.

**Why:** Not everything should be automated. A $5 hook that saves 5 min/month costs more than manual work. Automation has hidden costs: development, registration, testing, maintenance.

**How it works:**
1. **Frequency:** How many times/month?
2. **Manual cost:** How long (minutes)?
3. **Automation cost:** Setup time (hours) + monthly API cost ($)
4. **Payback period:** (automation cost) / (frequency × manual time / 60)
5. **Rule:** If payback < 6 months → automate; else → manual

**Example:** Pre-commit hook saves 2 min/month. Setup cost = 1 hour. Payback = 30 months. **Decision: Stay manual.**

**Gotcha:** Automation convenience ≠ automation value. Calculate before you build.

---

## 📂 Directory structure

```
~/.claude/
├── CLAUDE.md                 # Entry point: 14 imports
├── _rules/                   # Core rules (top-level)
│   ├── guiding_principles.md · behaviour.md · security.md
│   ├── testing.md · writing_style.md · naming_standards.md
│   ├── mcp_trust_model.md
│   └── claude_internal/      # 5 Claude Code specifics
│       └── lazy_load/        # Domain-specific rules
├── _tests/                   # 16 test files
├── hooks/                    # Enforcement + style hooks
├── skills/                   # Workflows
└── _reference/               # Reference (this doc + children)
```

---

## 🔄 Import strategy

### 1. Core imports (14 total, in CLAUDE.md)

All imported at session start. Each rule is foundational:

```
CLAUDE.md imports:
├── guiding_principles.md      (foundation)
├── memory/MEMORY.md           (user context)
├── behaviour.md               (safe defaults)
├── security.md                (coding standards)
├── testing.md                 (quality gate)
├── claude_internal/           (5 files: efficiency, automation, git, memory, guardrails)
├── mcp_trust_model.md         (security-critical)
├── writing_style.md           (output standards)
├── naming_standards.md        (identifier conventions)
└── aliases.md                 (command reference)
```

**Estimated cost:** ~2,000–2,500 tokens baseline.

### 2. Lazy-load imports (on-demand)

Rules in `lazy_load/` are **not** imported by CLAUDE.md. Instead, they're loaded explicitly when needed:

- **style_guide_standards/** — one per domain (SQL, Airflow, dbt, etc.)
- **claude_config_naming.md** — config structure naming
- **environment_setup/** — one-time setup guides (Oh My Zsh, etc.)
- **standards/** — domain-specific standards

**Cost:** ~50–150 tokens per file, only when needed.

---

## 🎯 How rules interact

Rules are organized by concern, creating clear separation that simplifies auditing:

| Interaction layer | Key files | Purpose |
|---|---|---|
| **Security** | behaviour.md → security_guardrails.md → security.md | Progressive gates from task approach to code standards |
| **Quality** | testing.md + hook_enforcement_naming_convention.sh | Enforce tests and naming at commit time |
| **Efficiency** | hook_style_guide_*.sh + lazy_load/ | Inject domain context on-demand, preserve baseline cost |

For detailed security architecture, see **[claude_config_architecture/_security.md](claude_config_architecture/_security.md)**.

For testing strategy and coverage, see **[claude_config_architecture/_testing.md](claude_config_architecture/_testing.md)**.

---

## 🔄 Evolution & Maintenance (Goal-Driven Auditing)

Regular maintenance cycles ensure the config stays intentional and focused on current goals:

### Audit Cadence

- **Monthly:** Spot-check — any obviously unused features?
- **Quarterly:** Deep review — search session transcripts for actual usage of each rule
- **Every 6 months:** Full reset (per Boris Cherny) — archive and restart to force intentionality review
  - **During reset:** Audit every rule — "Does this serve my current work?" Archive ruthlessly.
  - **Move to lazy-load:** Any domain-specific rule not immediately relevant
  - **Keep always-on:** Only foundational rules (guiding principles, security, testing)

### Adding a New Rule

Use this decision tree:

1. **Does it apply to EVERY session** (regardless of project type)?
   - **Yes** → Place in `_rules/01_essentials/` or `_rules/02_claude_internal/`; add to CLAUDE.md
   - **No** → Go to step 2

2. **Is it domain-specific** (SQL, dbt, Terraform, etc.)?
   - **Yes** → Place in `_rules/03_lazy_load/`; document in README
   - **No** → Reconsider whether it's needed at all

3. **Will you use this 5+ times/month**?
   - **Yes** → Consider always-on if foundational; else lazy-load with easy reference
   - **No** → Archive or leave out; add when you need it

### Deciding: Automation vs. Manual (Principle C)

Before creating a hook or skill:

1. **What's the task?** Be specific.
2. **How often?** Times/month?
3. **Manual cost?** Minutes to do manually?
4. **Automation cost?** Hours to build + test + register?
5. **Payback period:** Calculate in months. If < 6: automate. Else: stay manual.

---

## 📚 Related docs

- **Guiding principles:** `~/.claude/_rules/guiding_principles.md`
- **Test coverage:** `~/.claude/_tests/README.md`
- **Lazy-load guide:** `~/.claude/_rules/lazy_load/README.md`
