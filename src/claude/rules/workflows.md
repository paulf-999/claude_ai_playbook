# Rules — Workflows

Common end-to-end patterns for the team's most frequent tasks. Each workflow references the detailed rules that govern individual steps — consult the linked files for specifics.

---

## Feature development

1. **Plan** — outline approach, assumptions, and risks before touching any file. For non-trivial designs, run `/grill_me` to stress-test the plan before proceeding. Wait for confirmation. See `rules/behaviour/general.md`.
2. **Branch** — create a `feature/` branch from `main`. See `rules/git.md` for naming conventions.
3. **Code** — apply idempotent, DRY design throughout. See `rules/development.md`. For Python files, Pyright LSP runs automatically on every edit — resolve type errors before moving on. Run `/simplify` after implementing to surface reuse, quality, and efficiency improvements. For non-trivial changes, follow with `/devils_advocate` to adversarially review the diff before moving on.
4. **Test** — write or update tests before considering the task complete. All tests must pass. See `rules/testing.md`.
5. **PR** — keep PRs under 20 files; use the repo PR template; flag breaking changes explicitly. See `rules/git.md`.

---

## Bug fix

1. **Reproduce** — confirm you can reproduce the issue before investigating further.
2. **Hypothesise** — state a working hypothesis explicitly before making changes.
3. **Fix** — implement the minimal fix that addresses the root cause. Do not refactor surrounding code.
4. **Test** — add a test that would have caught the bug. All existing tests must still pass.
5. **PR** — follow the standard PR process. Reference the bug in the PR description.

---

## Code review

1. **Verdict first** — lead with approve, approve with suggestions, or request changes.
2. **Group by severity** — blocking, recommended, optional. See `agents/utility/code_reviewer.md`.
3. **Quote and suggest** — reference specific lines; suggest the fix, not just the problem.
4. **Check coverage** — flag any test gaps. Do not flag style issues enforced by linters.

---

## Data pipeline (Airflow / dbt)

1. **Design for idempotency** — every task and model must be safe to re-run. See `style_guide_standards/airflow.md` and `rules/development.md`.
2. **Config-driven** — no hardcoded environment-specific values. Use `config.yaml` and Jinja templating.
3. **Model layers** — follow the dbt layered architecture (staging → base → intermediate → warehouse → mart). See `style_guide_standards/dbt.md`.
4. **Test** — every dbt model needs `not_null` and `unique` on primary keys. Run `dbt test` before raising a PR. See `rules/testing.md`.
5. **CI gate** — pipelines follow lint → test → build → deploy order. See `style_guide_standards/cicd.md`.

---

## Infrastructure change (Terraform)

1. **Plan first** — always run `terraform plan` and review output before `terraform apply`. See `rules/development.md`.
2. **No hardcoded credentials** — use environment variables or a secrets manager. See `rules/security.md`.
3. **Environment promotion** — deploy dev → UAT → prod sequentially. Never skip UAT. See `style_guide_standards/cicd.md`.
4. **Modules for reuse** — extract shared patterns into `terraform/modules/`. See `style_guide_standards/terraform.md`.
5. **Validate** — use `validation` blocks on variable inputs. Pin all provider versions explicitly.

---

## Documentation

1. **Audience first** — establish who the document is for before writing anything.
2. **Structure for scannability** — headings, bullet points, and tables over prose. See `agents/core/technical_writer.md`.
3. **One example per concept** — every major concept needs at least one concrete example.
4. **ADR format for decisions** — context → decision → consequences. Use this for any non-trivial architectural choice.
5. **Break up long documents** — documents exceeding ~100 lines should be split into a parent index with child pages.
