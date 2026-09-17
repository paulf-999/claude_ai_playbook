# 🐳 Docker Fundamentals

## 📋 Contents

- [🏷️ Base images](#-base-images)
- [🗂️ Dockerfile structure](#-dockerfile-structure)
- [🏷️ Naming conventions](#-naming-conventions)

---

## 🏷️ Base images

- Always use an official base image from Docker Hub.
- Pin base image tags to a specific version — never use `:latest` in any non-local environment.
- Prefer minimal base images (`slim`, `alpine`, or distroless variants) to reduce attack surface and image size. Only use full images (e.g., `ubuntu`) when required OS tooling cannot be installed on a minimal base.

```dockerfile
# Good
FROM python:3.10-slim

# Bad
FROM python:latest
```

---

## 🗂️ Dockerfile structure

Follow this section order for consistency and cache efficiency:

```dockerfile
# 1. Base image
FROM <image>:<tag>

# 2. Working directory
WORKDIR /app

# 3. OS-level dependencies
RUN apt-get update && \
    apt-get install -yqq --no-install-recommends \
    <packages> \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Dependency files (before source — maximises cache reuse)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 5. Application source files
COPY <src> <dest>

# 6. Runtime configuration
ENTRYPOINT [...]
CMD [...]
```

---

## 🏷️ Naming conventions

- Image names: `snake_case`, descriptive of the image's purpose (e.g., `baseline_dbt_docker_image`).
- Image tags: use semantic versioning (`1.0`, `1.1`) — never `:latest` in non-local environments.
- Container names: `snake_case`, matching the image name where possible.
