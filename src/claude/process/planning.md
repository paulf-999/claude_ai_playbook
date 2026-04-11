# 🗺️ Planning

## ✅ Before trivial work

For simple, low-risk tasks, plan mode is still the minimum requirement — state what you are about to do and wait for confirmation before proceeding.

---

## ⚠️ Before non-trivial work

For any non-trivial task, plan mode is the minimum requirement — do not make changes until the plan has been reviewed and confirmed.

- Use plan mode to outline your approach before touching any file or running any command.
- Outline your approach in plain English.
- List assumptions you are making.
- Flag risks, tech debt, or security concerns.
- For complex or uncertain designs, run `/grill_me` to stress-test the plan — walks down the decision tree one question at a time before any code is written.
- Wait for my go-ahead before proceeding.

---

## 🔄 Design principles

Every design must be **idempotent** and **DRY** before being considered acceptable. Flag any violation explicitly when outlining your approach. See `rules/development.md` for definitions and technology-specific guidance.
