# 🪝 Hook Scorecards

**Purpose:** Home for hook quality scorecards — one per script in `hooks/`, scored on seven dimensions adapted to what makes a hook good.

---

## 📁 Location convention

One file per hook, named after the script: `_admin/_quality_scorecards/hooks/scorecard_<hook_file_stem>.md`.

- **Example:** `hooks/hook_enforcement_naming_convention.sh` → `scorecard_hook_enforcement_naming_convention.md`
- **Reserved hooks count too:** a hook kept on purpose but not registered is scored like any other, with Runtime Cost judged on what it would cost once wired in.
- **Never `@import` these files:** they're review records, not content Claude reads while working.

---

## 📋 Template

Use the shared `_templates/scorecard.md.template` with these seven dimensions, in this order.

---

## 🎯 Per-dimension criteria

| Dimension | 10 looks like | 1 looks like |
|---|---|---|
| **Clarity** | Header says what the hook checks, which event fires it and what it does on a hit, and the filename matches that | No header, or a name that describes something else |
| **Complexity** | Inverted shared formula (`03_authoring_guidelines/shared_standards/_complexity_scoring.md`): one concern, plain bash, no extra tools | Several concerns, several tools, logic spread across other folders |
| **Evidence of Need** | Fixes a recorded incident or a miss that kept recurring | Guards a hypothetical, with no record of the problem |
| **Test Coverage** | Tests cover the pass case, the hit case and bad or missing input | No test, or only the happy path |
| **Structural Compliance** | `hook_<type>_<domain>.sh` name, metadata header, registered in `settings.json` (or listed as reserved), paths resolved from the script's own location, listed in `_admin/_docs/decisions/hooks.md` | Wrong name, hardcoded paths, unregistered with no reason |
| **Failure Safety** | Fails open on missing tools or bad input, and blocks only when the action is truly wrong | Errors out noisily, or blocks valid work |
| **Runtime Cost** | Silent when nothing is wrong, well under 0.1s per event, and adds little or no text to the context | Slow on every event, or injects large text every turn |

**Overall:** the average of the seven dimensions, rounded to one decimal place.

---

## 📅 When to score

- **On creation:** every new hook gets a scorecard alongside it.
- **On re-score:** when a hook's behaviour or event changes, update its scorecard.
- **Summary:** update the hook's row in `hook_scorecards_summary.md` in the same commit.
