# 🐳 Docker Advanced Techniques

## 📋 Contents

- [⚡ Layer optimisation](#-layer-optimisation)
- [🔒 Security](#-security)
- [📁 .dockerignore](#-dockerignore)
- [🏗️ Multi-stage builds](#-multi-stage-builds)

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
