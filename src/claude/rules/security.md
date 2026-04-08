# 🔐 Rules — Security

## 🔑 Secrets and credentials

- Never commit secrets, credentials, API keys, or connection strings.
- Use environment variables or a secret manager (Azure Key Vault, AWS Secrets Manager).
- `.env` files must be listed in `.gitignore` — never committed.
- If a secret is accidentally committed, treat it as compromised immediately and rotate it.

---

## 🔒 Authentication

- Use service principals and IAM roles — avoid long-lived personal credentials in code.
- Do not share credentials between environments (dev, UAT, prod).
- Rotate credentials regularly and on suspected compromise.

---

## 🛡️ Input validation

- Validate and sanitise inputs at system boundaries (user input, external APIs, file ingestion).
- Never construct SQL or shell commands from raw user input.
- Use parameterised queries for all database interactions.

---

## 📦 Dependencies

- Do not add dependencies without checking for known vulnerabilities.
- Pin dependency versions in `requirements.txt`.
- Flag outdated packages with known CVEs before upgrading.

---

## ⚙️ General

- Apply the principle of least privilege: request only the permissions the service or user actually needs.
- Do not log sensitive data (credentials, PII, tokens).
- Flag any code that handles PII — ensure it is treated with appropriate care and documented.
- Raise a security concern immediately if spotted during unrelated work — do not leave it for later.
