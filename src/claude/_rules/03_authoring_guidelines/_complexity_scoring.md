# 🧮 Complexity Scoring (0–10)

**Purpose:** One shared complexity formula for every authored artefact type in this config — skills, agents, rules, hooks, and tests — defined once here so each new domain references it instead of redefining or drifting from it.

---

## 📐 The formula

**Raw complexity = Concepts (0–3) + Scope (0–3) + Dependencies (0–2) + Prerequisites (0–2)**

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Concepts** — distinct behaviors/rules covered | 1 | 2–3 | 4–5 | 6+ |
| **Scope** — how much of the config/codebase it touches | Single file | One directory | Multiple directories | Whole repo scan |
| **Dependencies** — external tools/integrations beyond the basics | None | 1 | 2+ | — (capped at 2) |
| **Prerequisites** — setup/fixture/mocking complexity | None | Simple | Complex | — (capped at 2) |

---

## 🔀 Two presentations, one formula

**Raw sum (0–10, higher = more complex)** — used directly for maturity/scope gates, e.g. skill maturity caps (Draft ≤4, Tactical ≤6, Strategic ≤8; 9+ means split it). This is a structural ceiling, not a 1–10 quality-style rating — don't invert it here.

**Complexity score = 10 − raw sum (higher = simpler, better)** — used wherever a domain scores complexity *alongside* a 1–10 quality-style rating (e.g. a skill's quality-scorecard "Complexity" dimension, or a test's complexity score). This direction matches every other 1–10 rating in this config, where 10 is always the best outcome — a raw complexity of 0 (single concept, single file, no dependencies, no fixtures) scores 10; a raw complexity of 10 (whole-repo scan, 6+ concepts, 2+ dependencies, complex fixtures) scores 0.

**Example:** something scanning 2 directories (Scope 1), verifying 3 distinct concepts (Concepts 1), no external tools (Dependencies 0), no fixtures (Prerequisites 0) → raw complexity 2 → **complexity score 8**.

---

## 🎯 Applying it per domain

- **Skills** (`authoring_skills.md`): maturity gates use the *raw sum* (Draft ≤4, Tactical ≤6, Strategic ≤8); the quality scorecard's "Complexity" dimension uses the *inverted score* (10 = simple, 1 = tangled) — both draw from this same formula.
- **Agents** (`authoring_agents.md`): same raw-sum maturity gates as skills — reference this file rather than redefining the formula when agent authoring is built out further.
- **Tests** (`testing.md`'s complexity scoring): uses the *inverted score* — see that file for how it relates to the required quality floor.
- **Rules and hooks:** no maturity levels or complexity gates exist for these yet — this formula is here so that whenever one is designed, it starts from this definition rather than a new one. Don't invent gate thresholds for rules/hooks speculatively; wait until that design work is actually needed.

---

## 🔗 Related

- `authoring_skills.md` — skill maturity gates and quality scorecard, applying the raw sum and inverted score respectively
- `authoring_agents.md` — agent maturity gates, same raw-sum convention as skills
- `testing.md` — test complexity scoring, applying the inverted score
- `authoring_rules.md` — rule authoring; no complexity gate defined yet
- `authoring_skills/_hard_gates_checklist.md` and equivalents — where a domain's specific gate thresholds live once defined
