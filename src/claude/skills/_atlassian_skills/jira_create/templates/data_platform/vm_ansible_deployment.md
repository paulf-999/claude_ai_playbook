# Template: vm_ansible_deployment

Ticket set for deploying a service to a new environment using VM provisioning and Ansible configuration. Modelled on DM-39229.

Creates 5 stories covering the full deployment lifecycle: scoping → infrastructure → configuration → deployment → validation.

---

## Variable fields (per use)

| Field | Description | Example |
|---|---|---|
| `service_name` | Name of the service being deployed | `Airbyte` |
| `environment` | Target environment or data centre | `DC3` |
| `sprint_id` | Plain integer sprint ID (see sprint ID reference below) | `15561` |

Components and parent epic are derived from the sprint number via the quarter mapping below — no manual input needed.

---

## Fixed fields (all tickets)

| Field | Value |
|---|---|
| Project | `DM` |
| Issue type | `Story` |
| Assignee | `<session_user_account_id>` — resolved at runtime via `atlassianUserInfo` |
| Priority | `Medium` |
| Labels | `["dm-claude-created"]` |
| Components | Derived from sprint number — see quarter mapping below |

---

## Quarter mapping

Map the sprint number to the correct component IDs and parent epic:

| Sprints | Components | Parent epic |
|---|---|---|
| 63–65 (H1) | `13377`, `13444` | `444372` |
| 66–69 (H2 Q3) | `13377`, `13445` | `495840` |
| 70–73 (H2 Q4) | `13377`, `13446` | `495840` |

> ⚠️ Component IDs and epic IDs are year-specific. Verify before use — these reflect 2026 H1/H2 values.

---

## Sprint ID reference

Sprint IDs for board 217 (DM board):

| Sprint | ID |
|---|---|
| 61 | 15560 |
| 62 | 15561 |
| 63 | 15562 |
| 64 | 15563 |
| 65 | 15564 |
| 66 | 15565 |
| 67 | 15566 |
| 68 | 15567 |
| 69 | 15568 |
| 70 | 15569 |
| 71 | 15570 |

If the target sprint is not listed, look it up via JQL: `project = DM AND sprint = "DM Sprint <number>"` and read `customfield_10020[0].id` from any matching ticket. After resolving the ID, add the new sprint → ID row to this table so future runs do not need to re-query Jira.

---

## Ticket set

Create all 5 tickets in order. Substitute `{service_name}` and `{environment}` throughout.

---

### Ticket 1 — Scoping

| Field | Value |
|---|---|
| Title | `Data Platform — {service_name} {environment}: Scope and task breakdown` |
| Story points (`customfield_10028`) | `1` |

**Description:**

> Scope the task breakdown required to deploy {service_name} to {environment}.
>
> * Review the existing {service_name} deployment approach in the current environment
> * Identify infrastructure requirements for {environment} (VM sizing, networking, storage)
> * Identify configuration changes needed in Ansible playbooks and roles
> * Produce a task list covering provisioning, configuration, deployment, and validation
>
> ### Acceptance criteria
>
> * Infrastructure requirements for {environment} documented
> * Ansible configuration changes identified and listed
> * Full task breakdown produced and tickets created in Jira

**Business value:**

> Defines the scope of the {service_name} {environment} deployment before work begins, reducing risk of mid-sprint discovery and ensuring the team has a clear task breakdown.
>
> Impact Rating (per Data Team Prioritization Framework):
> * a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
> * b. Priority Value Driver: Platform Reliability & Technical Risk – Score: 3
> * c. Secondary Value Driver: Ops Efficiency – Score: 2
> * d. Calculated Score: 0.75

---

### Ticket 2 — VM Provisioning

| Field | Value |
|---|---|
| Title | `Data Platform — {service_name} {environment}: Provision VMs in {environment}` |
| Story points (`customfield_10028`) | `2` |

**Description:**

> Provision the virtual machines required to run {service_name} in {environment}.
>
> * Define VM specifications (CPU, memory, storage) based on scoping output
> * Provision VMs using the agreed infrastructure tooling
> * Configure networking (IP addressing, firewall rules, DNS)
> * Verify VMs are accessible and meet OS requirements for Ansible
>
> ### Acceptance criteria
>
> * VMs provisioned and accessible in {environment}
> * Networking configured and verified (connectivity to required services)
> * VMs inventoried in the Ansible inventory file for {environment}

**Business value:**

> Provisions the infrastructure foundation required for the {service_name} {environment} deployment, unblocking all downstream configuration and deployment work.
>
> Impact Rating (per Data Team Prioritization Framework):
> * a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
> * b. Priority Value Driver: Platform Reliability & Technical Risk – Score: 3
> * c. Secondary Value Driver: Ops Efficiency – Score: 2
> * d. Calculated Score: 0.75

---

### Ticket 3 — Ansible Configuration

| Field | Value |
|---|---|
| Title | `Data Platform — {service_name} {environment}: Configure Ansible playbook for deployment` |
| Story points (`customfield_10028`) | `3` |

**Description:**

> Update the Ansible playbook and roles to support deploying {service_name} to {environment}.
>
> * Update inventory file to include {environment} hosts
> * Create or update Ansible roles with {environment}-specific configuration (URLs, credentials references, paths)
> * Parameterise environment-specific values via group_vars or an inputs file
> * Validate the playbook runs cleanly against {environment} in dry-run mode
>
> ### Acceptance criteria
>
> * {environment} hosts added to Ansible inventory
> * Ansible roles updated with {environment}-specific configuration
> * Playbook dry-run completes without errors against {environment}
> * No hardcoded credentials — all secrets referenced from the vault or environment variables

**Business value:**

> Extends the Ansible automation to cover {environment}, enabling repeatable and auditable deployment without manual configuration steps.
>
> Impact Rating (per Data Team Prioritization Framework):
> * a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
> * b. Priority Value Driver: Platform Reliability & Technical Risk – Score: 3
> * c. Secondary Value Driver: Ops Efficiency – Score: 3
> * d. Calculated Score: 0.90

---

### Ticket 4 — Deployment

| Field | Value |
|---|---|
| Title | `Data Platform — {service_name} {environment}: Deploy {service_name}` |
| Story points (`customfield_10028`) | `3` |

**Description:**

> Run the Ansible playbook to deploy {service_name} to {environment}.
>
> * Execute the Ansible playbook against {environment}
> * Verify the service starts successfully and passes health checks
> * Confirm connectivity to dependent services (databases, message queues, APIs)
> * Document any post-deployment manual steps required
>
> ### Acceptance criteria
>
> * {service_name} deployed and running in {environment}
> * Service health checks passing
> * Connectivity to all dependent services confirmed
> * Deployment steps documented (runbook updated if applicable)

**Business value:**

> Delivers the {service_name} service into {environment}, making it operational and available for pipeline execution and downstream consumers.
>
> Impact Rating (per Data Team Prioritization Framework):
> * a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
> * b. Priority Value Driver: Platform Reliability & Technical Risk – Score: 4
> * c. Secondary Value Driver: Transaction Integrity – Score: 3
> * d. Calculated Score: 1.20

---

### Ticket 5 — Validation

| Field | Value |
|---|---|
| Title | `Data Platform — {service_name} {environment}: Validate {service_name} deployment in {environment}` |
| Story points (`customfield_10028`) | `2` |

**Description:**

> Validate the end-to-end {service_name} deployment in {environment} is functioning correctly.
>
> * Run a representative pipeline or job end-to-end in {environment}
> * Verify data flows correctly through the full stack
> * Confirm monitoring, alerting, and logging are active
> * Sign off deployment as production-ready (or document outstanding gaps)
>
> ### Acceptance criteria
>
> * End-to-end pipeline run completed successfully in {environment}
> * Monitoring and alerting confirmed active
> * Any outstanding gaps documented as follow-up tickets
> * Deployment signed off as production-ready or blockers clearly identified

**Business value:**

> Confirms the {service_name} {environment} deployment is functioning correctly end-to-end before the environment is relied upon for production workloads.
>
> Impact Rating (per Data Team Prioritization Framework):
> * a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
> * b. Priority Value Driver: Transaction Integrity – Score: 4
> * c. Secondary Value Driver: Platform Reliability & Technical Risk – Score: 3
> * d. Calculated Score: 1.25
