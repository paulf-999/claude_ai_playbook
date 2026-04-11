# 🛠️ Agents — Tools

Technology-specific agents — one per style guide. Use for focused work on a single technology, or for automated code review via hooks (each agent is auto-assigned when changes are detected for its file patterns).

When a task spans multiple technologies, use the `architect` agent instead.

| File | Agent name | Owns | Purpose |
|------|------------|------|---------|
| [`python.md`](python.md) | `python` | `*.py` | 🐍 Python code review and standards enforcement |
| [`sql.md`](sql.md) | `sql` | `**/*.sql` | 🗄️ SQL / Snowflake query review and SQLFluff conventions |
| [`unix.md`](unix.md) | `unix` | `*.sh` | 🐚 Bash/shell scripting review and shellcheck compliance |
| [`makefile.md`](makefile.md) | `makefile` | `Makefile`, `*.mk` | 🔨 Makefile and GNU Make conventions |
| [`dbt.md`](dbt.md) | `dbt` | `models/**/*.sql`, `models/**/*.yml` | 🔄 dbt model review, layer conventions, and test coverage |
| [`docker.md`](docker.md) | `docker` | `Dockerfile`, `.dockerignore` | 🐳 Dockerfile security, layer optimisation, and pinning |
| [`cicd.md`](cicd.md) | `cicd` | `.github/workflows/*.yml`, `azure-pipelines.yml` | 🚀 CI/CD pipeline structure, secrets, and deployment safety |
| [`ansible.md`](ansible.md) | `ansible` | `*.yml` (playbooks/roles/inventory) | ⚙️ Ansible playbook review and FQCN enforcement |
| [`airflow.md`](airflow.md) | `airflow` | `dags/**/*.py` | 🌊 Airflow DAG review, idempotency, and config conventions |
| [`terraform.md`](terraform.md) | `terraform` | `*.tf`, `*.tfvars` | 🏗️ Terraform IaC review, module structure, and pinning |
