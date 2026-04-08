# 🐳 Docker & Dockerfile Style Guide & Standards

Defines the team's standards for writing Dockerfiles and working with Docker images.

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

# 2. Metadata
LABEL maintainer="..." \
    name="..." \
    desc="..." \
    version="..."

# 3. Working directory
WORKDIR /app

# 4. OS-level dependencies
RUN apt-get update && \
    apt-get install -yqq --no-install-recommends \
    <packages> \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 5. Dependency files (before source — maximises cache reuse)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 6. Application source files
COPY <src> <dest>

# 7. Runtime configuration
ENTRYPOINT [...]
CMD [...]
```

---

## 📋 Metadata

Every Dockerfile must include a `LABEL` block with at minimum:

```dockerfile
LABEL maintainer="Your Name" \
    name="image-name" \
    desc="Brief description of the image" \
    version="1.0"
```

---

## ⚡ Layer optimisation

- Chain related `RUN` commands with `&&` and `\` to reduce the number of layers.
- Always clean up package manager caches in the same `RUN` step as the install — cleaning in a later step does not reduce image size.
- Copy dependency files (`requirements.txt`, `packages.yml`) **before** copying source code so that the dependency install layer is cached and only invalidated when dependencies change.

```dockerfile
# Good — single layer, cache cleaned in same step
RUN apt-get update && \
    apt-get install -yqq --no-install-recommends \
    git \
    gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Bad — unnecessary layers, cache not cleaned
RUN apt-get update
RUN apt-get install -y git gcc
RUN apt-get clean
```

```dockerfile
# Good — requirements copied and installed before source
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY src/ /app/src/

# Bad — source copied first, invalidates dependency cache on any code change
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
```

---

## 🔒 Security

- Do not run containers as root. Create and switch to a non-root user unless the base image or tooling requires root.
- Never embed secrets, credentials, or API keys in a Dockerfile or image layer. Use environment variables injected at runtime or a secrets manager.
- Do not use `ADD` with remote URLs — use `curl` or `wget` in a `RUN` step so the layer is explicit and auditable.
- Use `--no-install-recommends` with `apt-get` to avoid pulling in unnecessary packages.
- Use `--no-cache-dir` with `pip install` to avoid storing the pip cache in the image layer.

```dockerfile
# Create and use a non-root user
RUN useradd --create-home appuser
USER appuser
```

---

## 📁 .dockerignore

Every repo with a Dockerfile must have a `.dockerignore` file. It should exclude everything not needed in the image build context:

```
.git
.env
.env.*
__pycache__/
*.pyc
*.pyo
venv/
.venv/
*.egg-info/
dist/
.terraform/
.DS_Store
```

Excluding irrelevant files reduces build context size, speeds up builds, and prevents accidental inclusion of secrets or local state.

---

## 📌 Instructions reference

### COPY vs ADD

Always use `COPY` over `ADD` unless you explicitly need `ADD`'s tar extraction behaviour. `COPY` is explicit and predictable.

```dockerfile
# Good
COPY src/ /app/src/

# Only use ADD when tar auto-extraction is needed
ADD archive.tar.gz /app/
```

### ENTRYPOINT vs CMD

- Use `ENTRYPOINT` to define the fixed executable for the container.
- Use `CMD` to provide default arguments that can be overridden at runtime.
- Use the exec form (`["executable", "arg"]`) over the shell form (`executable arg`) to ensure signals are passed correctly.

```dockerfile
ENTRYPOINT ["python", "-m", "myapp"]
CMD ["--config", "config.yml"]
```

### ARG vs ENV

- Use `ARG` for build-time variables that are not needed at runtime.
- Use `ENV` for runtime environment variables.
- Never pass secrets via `ARG` — they are visible in the image build history.

```dockerfile
ARG PYTHON_VERSION=3.10
ENV APP_ENV=production
```

---

## 🏗️ Multi-stage builds

Use multi-stage builds to produce lean production images — compile or install in a builder stage, then copy only the artefacts needed into a minimal final stage.

```dockerfile
# Builder stage
FROM python:3.10 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.10-slim
COPY --from=builder /install /usr/local
COPY src/ /app/src/
WORKDIR /app
ENTRYPOINT ["python", "-m", "myapp"]
```

---

## 🏷️ Naming conventions

- Image names: `snake_case`, descriptive of the image's purpose (e.g., `baseline_dbt_docker_image`).
- Image tags: use semantic versioning (`1.0`, `1.1`) — never `:latest` in non-local environments.
- Container names: `snake_case`, matching the image name where possible.
