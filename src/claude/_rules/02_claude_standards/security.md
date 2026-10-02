<!-- version: 1.2.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-02 -->
<!-- applies_to: * -->
<!-- miss_cost: high — secrets leak or injected instructions get followed -->
<!-- loading: always-on — secrets and prompt injection can turn up in any session -->
# 🔐 Rules — Security

**Purpose:** Establish security standards across two concerns: (1) secure coding practices for user-generated code, and (2) Claude's own conduct guardrails to prevent prompt injection and secret exposure.

## 📋 Contents

- [Secure coding practices](#-secure-coding-practices) — standards for secrets, auth, input validation, dependencies
- [Claude's security guardrails](#-claudes-security-guardrails) — prompt injection defence and Claude's conduct

---

## 🔐 Secure coding practices

Standards for secure code generation. Covers secrets management, authentication, input validation, and dependency security.

@~/.claude/_rules/02_claude_standards/security/_code_security.md

---

## 🔐 Claude's security guardrails

@~/.claude/_rules/02_claude_standards/security/_security_guardrails.md

---

## 📖 Reference (Claude's design patterns)

- **Read on demand:** `~/.claude/_reference/claude_config_architecture/_security.md` — the four security layers, threat model and design rationale
