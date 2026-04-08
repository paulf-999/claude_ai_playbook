# 🔁 CI/CD Style Guide & Standards

Defines the team's standards for CI/CD pipelines. Platform-agnostic principles are documented here. Platform-specific standards are in the child pages below.

The team currently uses **Azure DevOps**. **GitHub Actions** will be adopted in future.

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`cicd/azure_devops.md`](cicd/azure_devops.md) | Azure DevOps pipeline YAML structure, triggers, variables, stages, and templates |
| [`cicd/github_actions.md`](cicd/github_actions.md) | GitHub Actions workflow structure, secrets, pinning, and reusable workflows |

---

## 🏗️ Platform-agnostic principles

### Pipeline structure

- Pipelines must follow a logical gate order: **lint → test → build → deploy**.
- Each stage must only run if the previous stage passes — use explicit stage dependencies.
- One job per concern — do not bundle unrelated steps into a single job.
- Fail fast: surface failures early so developers get feedback without waiting for long-running stages.

### Path-based triggers

- Only trigger pipelines when files relevant to the pipeline have changed.
- Define explicit path includes in trigger configuration — do not run the full pipeline on every commit regardless of what changed.

### Secrets management

- Never hardcode secrets, credentials, or connection strings in pipeline YAML.
- Use the platform's secret store (Azure Key Vault via variable groups, GitHub Secrets via environments).
- Do not echo or print secret values in pipeline logs.

### Environment promotion

- Promote artefacts through environments in order: dev → UAT → prod.
- Do not deploy directly to prod without passing UAT.
- Use environment-specific variable groups or secrets — never share credentials between environments.

### Idempotency and repeatability

- Pipeline runs must be safe to re-run — do not rely on state left over from a previous run.
- Clean up working directories and temporary artefacts between runs where possible.

### Commenting

- Comment each stage and job to describe what it does and why.
- Keep debugging steps commented out (not deleted) so they can be re-enabled quickly during troubleshooting.

### Dependency pinning

- Pin all external action and task versions explicitly — do not use floating references such as `@latest` or `@main`.
- Review pinned versions periodically for security updates.

---

## 📥 Imports

@./cicd/azure_devops.md
@./cicd/github_actions.md
