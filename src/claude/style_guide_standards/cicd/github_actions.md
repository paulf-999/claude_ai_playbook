# 🐙 GitHub Actions Standards

> GitHub Actions is the team's future CI/CD platform. This page will be expanded as adoption grows.

---

## 📁 File location and naming

- Workflow files live under `.github/workflows/`.
- Name workflow files descriptively using `snake_case`: `pr_validation.yml`, `release.yml`.
- Reusable workflows live under `.github/workflows/` with a `_reusable_` prefix or in a dedicated subdirectory.

---

## 🗂️ Workflow structure

Follow this top-level section order:

```yaml
name:       # 1. Workflow name (displayed in GitHub UI)
on:         # 2. Trigger definition
env:        # 3. Workflow-level environment variables (non-secret)
jobs:       # 4. Jobs
```

---

## ⚡ Triggers

- Use `pull_request:` for PR pipelines and `push:` for branch/merge pipelines.
- Use `paths` to limit execution to relevant files — do not run on every commit.
- Use `concurrency` to cancel in-progress runs when a newer commit arrives (equivalent to Azure DevOps `autoCancel: true`).

```yaml
on:
    pull_request:
        branches:
            - main
        paths:
            - 'src/**'
            - 'requirements.txt'

concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
```

---

## 🔒 Secrets

- Never hardcode secrets in workflow YAML.
- Reference secrets via `${{ secrets.SECRET_NAME }}` — store them in GitHub Secrets at the repository or environment level.
- Use GitHub Environments to scope secrets to specific deployment targets (dev, UAT, prod).
- Do not print secret values in workflow logs — GitHub masks known secrets, but avoid `echo`ing them explicitly.

```yaml
env:
    SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
```

---

## 📌 Action version pinning

- Pin all third-party actions to a specific commit SHA — do not use floating tags such as `@main`, `@master`, or `@v3`.
- For first-party GitHub actions (`actions/*`), pinning to an immutable tag (e.g., `@v4.1.0`) is acceptable.
- Review pinned versions periodically for security updates.

```yaml
# Good
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Bad
- uses: actions/checkout@main
- uses: actions/checkout@v4
```

---

## 🏗️ Jobs

- Give every job a descriptive `name` displayed in the GitHub UI.
- Use `needs` to enforce job ordering — jobs run in parallel by default.
- One job per logical concern.

```yaml
jobs:
    lint:
        name: Lint
        runs-on: ubuntu-latest
        steps:
            ...

    test:
        name: Test
        needs: lint
        runs-on: ubuntu-latest
        steps:
            ...
```

---

## ♻️ Reusable workflows

- Extract shared pipeline logic into reusable workflows using `workflow_call`.
- Call reusable workflows from the parent workflow using `uses:`.
- Pin reusable workflow references to a specific SHA or tag.

```yaml
jobs:
    run_tests:
        uses: ./.github/workflows/reusable_test.yml@main
        secrets: inherit
```

---

## 🏷️ Naming conventions

| Construct | Convention |
|-----------|------------|
| Workflow files | `snake_case.yml` |
| Job IDs | `snake_case` |
| Step names | Sentence case, descriptive |
| Environment variable names | `UPPER_SNAKE_CASE` |
| Secret names | `UPPER_SNAKE_CASE` |
