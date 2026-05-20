# 🎯 Claude skill tests — behavioural

Behavioural tests for individual Claude skills. One file per skill.

---

## 💡 What these tests are

Skills are prose instructions — there is no Python to import and call. Every skill contains deterministic, rule-based logic that Claude must follow:

- Label mapping
- Title format validation
- Scope selection
- Post-creation prompt structure

These tests extract that logic into Python and assert it directly, serving two purposes:

- 📋 **Specification** — machine-checked description of what the skill requires; if the rules change, the tests must change too
- 🔒 **Regression** — a failing test surfaces dropped or changed rules before the PR is merged

---

## 🔀 How this differs from `test_skills_structural.py`

| | `test_skills_structural.py` | `skills/test_<skill>_skill.py` |
|---|---|---|
| **Scope** | All skills | One skill per file |
| **What it tests** | Shape: does the file exist, is front matter valid, do path references resolve? | Rules: does the logic embedded in the skill prose behave correctly? |
| **Failure means** | Authoring mistake — broken reference, missing field | A rule has changed or been dropped — the spec and the skill are out of sync |

---

## ➕ Adding a new skill test file

1. Create `tests/skills/test_<skill_name>_skill.py`
2. Extract the deterministic rules from the skill's `SKILL.md` as constants at the top of the file
3. Write parametrized test cases against those constants

> Structural checks (file presence, front matter) are already covered by `test_skills_structural.py` — do not duplicate them here.

---

## 📄 Files

| File | Skill | What it covers |
|---|---|---|
| `test_create_pr_skill.py` | `create_pr` | Title format regex, title cleanliness (no extensions, path separators, or backticks in description), label mapping, scope selection, post-creation prompt structure |
