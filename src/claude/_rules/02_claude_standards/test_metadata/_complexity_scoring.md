# 🧮 Test Complexity Scoring (0–10)

**Purpose:** Score how complex a test file is to write and maintain, using the same 0–10 formula `authoring_skills.md` already uses for skills — one consistent complexity model across the config, not two. Reward simplicity: a test can't claim top quality by being comprehensive at the cost of being complex.

---

## 📐 The formula

**Complexity = Concepts (0–3) + Scope (0–3) + Dependencies (0–2) + Prerequisites (0–2)**

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Concepts** — distinct behaviors/rules verified | 1 | 2–3 | 4–5 | 6+ |
| **Scope** — how much of the config it touches | Single file | One directory | Multiple directories | Whole repo scan |
| **Dependencies** — external tools beyond stdlib + pytest | None | 1 (e.g. `subprocess`, `jq`) | 2+ | — (capped at 2) |
| **Prerequisites** — fixture/setup complexity | None | Simple fixture | Complex fixture/mocking | — (capped at 2) |

**Example:** `test_portable_paths.md`'s test scans 2 directories (Scope 1), verifies 3 distinct patterns — hardcoded source, `.expanduser()`, home-dir constants (Concepts 1), uses no external tools (Dependencies 0), needs no fixtures (Prerequisites 0) → Complexity 2.

---

## 🔒 Complexity caps the achievable quality score

A complex test cannot claim excellence just by being thorough. Complexity sets a **ceiling** on quality score, independent of assertion/function counts:

| Complexity | Max quality score |
|---|---|
| **0–4** (simple) | 10 — no cap |
| **5–6** (moderate) | 8 |
| **7–8** (complex) | 6 |
| **9–10** (very complex) | 4 |

**Why:** A 900-line test with 40 assertions scores high on the raw quality rubric (`test_metadata.md`) but is expensive to maintain and hard to reason about when it breaks. Capping by complexity forces the simpler design — split a complex test into several simple ones rather than write one comprehensive, tangled file.

**Consequence:** since `testing.md` requires new tests to reach quality ≥9/10, they must also keep complexity ≤4 — both constraints apply together, not one or the other.

---

## 🔗 Related

- Parent: `test_metadata.md` — the quality-score rubric this complements
- Reference: `authoring_skills.md` — source of the Concepts/Scope/Dependencies/Prerequisites formula
