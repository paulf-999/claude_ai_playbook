# 🔐 Secure Coding Practices

**Purpose:** Establish secure coding standards for handling secrets, authentication, input validation, and dependencies to prevent common vulnerabilities.

## 📋 Contents

- [Secrets and credentials](#-secrets-and-credentials)
- [Authentication](#-authentication)
- [Input validation](#-input-validation)
- [Dependencies](#-dependencies)
- [General](#-general)

---

## 🔑 Secrets and credentials

- **Use a secret manager:** store secrets in environment variables or a secret manager (Azure Key Vault, AWS Secrets Manager) — never hardcoded.
  - **Example:** Load from env: `api_key = os.getenv("API_KEY")` (not `api_key = "sk-abc123xyz"`)
- **Gitignore .env:** `.env` files must be listed in `.gitignore` — never committed.
  - **Example:** Add to `.gitignore`: `.env`, `.env.local`, `*.env`
- **Rotate on exposure:** if a secret is accidentally committed, treat it as compromised immediately and rotate it.

## 🔒 Authentication

- **Service principals over personal credentials:** use service principals and IAM roles — avoid long-lived personal credentials in code.
  - **Example:** Use AWS STS assume role: `sts_client.assume_role(RoleArn="arn:aws:iam::...", RoleSessionName="...")` instead of embedding `AWS_ACCESS_KEY_ID`
- **No credential sharing across environments:** do not share credentials between dev, UAT, and prod.
- **Rotate regularly:** rotate credentials regularly and on suspected compromise.

## 🛡️ Input validation

- **Validate at boundaries:** validate and sanitise inputs at system boundaries (user input, external APIs, file ingestion).
- **No dynamic SQL or shell from user input:** never construct SQL or shell commands from raw user input.
  - **Example:** ❌ `cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")` → ✅ `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
- **Parameterised queries:** use parameterised queries for all database interactions.

## 📦 Dependencies

- **Check for vulnerabilities:** do not add dependencies without checking for known CVEs.
  - **Example:** Run `pip-audit` or `safety check` before committing: `pip-audit --desc`
- **Pin versions:** pin dependency versions explicitly in `requirements.txt`.
  - **Example:** `requests==2.31.0` (not `requests>=2.0`)
- **Flag outdated packages:** flag packages with known CVEs before upgrading.

## ⚙️ General

- **Least privilege:** request only the permissions the service or user actually needs.
- **No sensitive logging:** do not log credentials, PII, or tokens.
- **Flag PII handling:** flag any code that handles PII — ensure it is treated with appropriate care and documented.

---

## 🔗 Related rules

- Parent: `security.md` — security overview and guardrails
- Sibling: `_security_guardrails.md` — Claude's conduct and prompt injection defence
- Reference: `~/.claude/_reference/claude_design_patterns/_security.md` — security architecture
