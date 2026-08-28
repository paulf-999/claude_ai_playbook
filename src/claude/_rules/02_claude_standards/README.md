# 02_claude_standards

**Purpose:** Blocking standards and enforcement rules that Claude must apply to all work — ensuring code quality, system stability, and safe operational conduct.

**Scope:** Foundational blocking rules applied universally. Includes both operational conduct (safe defaults, decision-making) and quality/security gates. Claude-facing guidance, not user-facing conventions.

---

## How to use

Import rules from this tier in `~/.claude/CLAUDE.md` when they are:
1. **Blocking** — prevent unsafe actions, quality decay, or security vulnerabilities
2. **Foundational** — apply to every session and every operational decision
3. **Universal** — no exceptions or conditional application
4. **High cost of violation** — safety regression, data loss, or systemic quality issues

Rules in this tier have a token cost (~150 tokens/session) and must justify their baseline presence through frequency and impact.

---

## Files in this tier

| File | Purpose |
|---|---|
| **behaviour.md** | Safe operational conduct — ask before risky operations, investigate state before deletion, intentional action |
| **security.md** | Secure coding standards (secrets, auth, input validation) + Claude's conduct (prompt injection defence) |
| **testing.md** | Requirements and patterns for test creation; all code artifacts must be tested |

---

## Child file organization

- **`behaviour/`** — Child files covering decision-making and artefact proposal gates
- **`git/`** — Child files covering safe git patterns, commits, and pull requests
- **`testing/`** — Child files covering test design patterns, anti-patterns, and maintenance

---

## When to add new rules

Add to this tier only when:
- The rule is **blocking** (prevents unsafe action or quality decay)
- It applies to **every session and every operational decision**
- The token cost is justified by **safety-critical** or **quality-critical** impact
- It establishes **universal standards** with no exceptions

Otherwise, place in:
- **01_essentials/** — user-facing conventions (naming, writing, authoring)
- **03_claude_reference/** — system/meta knowledge about how the config works
- **04_lazy_load/** — domain-specific, load on-demand only

---

## Related

- **01_essentials/** — User-facing principles and conventions (guiding_principles, authoring, naming, writing)
- **03_claude_reference/** — System knowledge and reference material (git, efficiency, external systems)
- **04_lazy_load/** — Domain-specific rules (lazy-loaded)
