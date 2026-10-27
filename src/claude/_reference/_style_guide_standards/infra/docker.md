---
paths:
  - "**/Dockerfile*"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
---
<!-- version: 1.2.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
<!-- miss_cost: medium — images that fail review or bloat -->
<!-- loading: path-scoped — only applies to Docker, so it loads when a Dockerfile or compose file is open -->
# 🐳 Docker & Dockerfile Style Guide & Standards

**Purpose:** Define the team's standards for writing Dockerfiles and working with Docker images.

## 📋 Structure

- [**Fundamentals**](docker/_fundamentals.md) — Base images, Dockerfile structure, naming conventions
- [**Advanced Techniques**](docker/_advanced.md) — Layer optimisation, security, .dockerignore, multi-stage builds
