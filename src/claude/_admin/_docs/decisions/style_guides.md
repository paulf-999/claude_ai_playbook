# 📐 Style guides — decisions

## 📁 Lazy load, not permanent import

- **Why:** style guides are domain-specific — not every session involves bash or Python work. Permanent import would load 100–200 lines into every context window regardless of need.
- **How:** style guides live in `_rules/lazy_load/style_guide_standards/` and are read on demand when domain work begins.

## 🗂️ Language grouped under domain directories

- **Why:** flat `lazy_load/` would accumulate `bash.md`, `python.md`, `ohmyzsh.md` etc. with no grouping signal as more languages are added.
- **Structure:** `lazy_load/style_guide_standards/<domain>/<language>.md`
  - `unix/` — all Unix shell languages (bash today, zsh/ohmyzsh planned)
  - `python/` — Python coding standards and environment tooling

## 💬 Comment philosophy deviates from Claude's default

- **Why:** Claude defaults to no comments unless the WHY is non-obvious. These guides explicitly require "when in doubt, add a comment" and labelling of constant groups and logical phases in functions longer than ~10 lines.
- **Note:** intentional team-level override — the goal is readable, maintainable code for collaborators, not minimal output.

## 🐍 Python type hint constraints

- **Why:** bare container types (`dict`, `list`) are not informative — they add annotation noise without narrowing the type. `-> None` return annotations are equally noisy since absence of a return implies `None`.
- **Rule:** annotate only when the type is specific and non-obvious; omit `-> None` and bare `dict`/`list` without parameterization.
