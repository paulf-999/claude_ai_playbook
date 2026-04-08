# 🔷 Azure DevOps Pipeline Standards

## 📁 File location and naming

- Pipeline YAML files live under `src/cicd/`.
- Reusable pipeline templates live under `src/cicd/pipelines/`.
- Name pipeline files descriptively using `snake_case`: `azure_pipeline_pr.yml`, `azure_pipeline_release.yml`.

---

## 🗂️ YAML structure

Follow this top-level section order:

```yaml
variables:       # 1. Pipeline variables (Key Vault references, branch names, paths)
pr: / trigger:   # 2. Trigger definition
pool:            # 3. Agent pool
stages:          # 4. Stages (each containing jobs and steps)
```

---

## 📦 Variables

- Declare all pipeline variables at the top of the file.
- Group related variables with inline comments as section headers.
- Reference secrets from Azure Key Vault — never hardcode values in the YAML.
- Use `UPPER_SNAKE_CASE` for all variable names.

```yaml
variables:
    # Azure Key Vault name
    AZURE_KEY_VAULT_NAME: dmt-uat-uscn-oos-kv

    # ------------------------------------------
    # Git branch names
    # ------------------------------------------
    PR_SOURCE_BRANCH_SHORT: $[ replace(variables['System.PullRequest.SourceBranch'], 'refs/heads/', '') ]
    SOURCE_GIT_BRANCH_NAME: origin/$(PR_SOURCE_BRANCH_SHORT)
    TARGET_GIT_BRANCH_NAME: origin/main

    # Other variables
    CICD_SCRIPTS_DIR: src/cicd/scripts
```

- Note: `DBT_PROJECT_DIR` is a reserved dbt environment variable — use an alternative name such as `DBT_PROJECT_DIRECTORY` to avoid conflicts.

---

## ⚡ Triggers

- Use `pr:` for pull request pipelines and `trigger:` for branch/merge pipelines.
- Always set `autoCancel: true` on PR pipelines to cancel stale builds when a newer commit arrives.
- Use `paths.include` to limit pipeline execution to relevant files — do not run on every commit.

```yaml
pr:
    autoCancel: true
    branches:
        include:
            - main
    paths:
        include:
            - prod_analytics/models/*
            - prod_analytics/macros/*
            - requirements.txt
            - .sqlfluff
```

---

## 🖥️ Agent pool

- Define the agent pool at the top level so all stages inherit it.
- Use the team's designated on-premises pool unless a stage explicitly requires a different agent.

```yaml
pool: onprem-linux-elksdx
```

---

## 🏗️ Stages

- Give every stage a `displayName` that describes what it does in plain English.
- Use `dependsOn` to enforce stage ordering — stages run in parallel by default.
- Use `condition` to restrict stages to the appropriate trigger type (e.g., PR only).
- Comment each stage to describe its purpose.

```yaml
stages:
    - stage: Git
      displayName: Git tests
      condition: eq(variables['Build.Reason'], 'PullRequest')
      jobs:
          ...

    - stage: dbt_and_sqlfluff
      displayName: dbt & SQLFluff tests
      dependsOn: Git
      condition: eq(variables['Build.Reason'], 'PullRequest')
      jobs:
          ...
```

- Stage names use `PascalCase` or `snake_case` — be consistent within the file.

---

## ⚙️ Jobs

- Give every job a `displayName` prefixed with `- ` to make the pipeline UI readable.
- Job IDs use `camelCase`.
- One job per logical concern — do not bundle unrelated steps.

```yaml
jobs:
    - job: validateGitBranchName
      displayName: '- validate branch name'
      steps:
          ...

    - job: dbtSlimCIJob
      displayName: "- dbt 'Slim CI' job"
      steps:
          ...
```

---

## 🔧 Steps and templates

- Extract reusable step sequences into template files under `src/cicd/pipelines/`.
- Reference templates using the `template:` key rather than inlining steps.
- Organise templates by stage/concern: `pipelines/pr_pipelines/git/`, `pipelines/pr_pipelines/dbt_slim_ci_pipeline.yml`, etc.

```yaml
steps:
    - template: pipelines/pr_pipelines/git/git_branch_validation_pipeline.yml
```
