---
paths:
  - "**/Dockerfile*"
  - "**/docker-compose*.yml"
---
<!-- version: 1.1.2 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: medium — images that fail review or bloat -->
<!-- loading: path-scoped — only applies to Docker, so it loads when a Dockerfile or compose file is open -->
# 🐳 Docker & Dockerfile Style Guide & Standards

**Purpose:** Define the team's standards for writing Dockerfiles and working with Docker images.

## 📋 Structure

- [**Fundamentals**](../../../../_rules_lazy_load/style_guide_standards/infra/docker/fundamentals.md) — Base images, Dockerfile structure, naming conventions
- [**Advanced Techniques**](../../../../_rules_lazy_load/style_guide_standards/infra/docker/advanced.md) — Layer optimisation, security, .dockerignore, multi-stage builds
