# ✈️ Air-Gapped Deployment

> **Scope:** Payroc-specific conventions for the `pyrc-cac-ans` estate — not generic Ansible guidance.

Standards for deploying roles into environments with no outbound internet access. STG and PRD hosts have zero outbound connectivity — all artefacts must be sourced before deployment and served from an internal mirror.

## 📋 Contents

- [🚫 Core constraint](#-core-constraint)
- [📦 Artefact sourcing — Cloudsmith](#-artefact-sourcing-cloudsmith)
- [🗄️ Cache directory pattern](#-cache-directory-pattern)
- [🐳 Docker image handling](#-docker-image-handling)
- [⎈ Helm chart deployment](#-helm-chart-deployment)
- [✅ Pre-deployment checklist](#-pre-deployment-checklist)

---

## 🚫 Core constraint

**Never design a task that requires outbound internet access on STG or PRD hosts.**

This includes:
- Pulling Docker images directly from Docker Hub, `registry.k8s.io`, `ghcr.io`, or any public registry
- Fetching Helm charts from `https://charts.helm.sh` or any public Helm repo
- Installing packages via `pip install` from PyPI or `apt` from public mirrors
- Downloading binaries from GitHub Releases or any public URL

SDX is also air-gapped unless a session or ticket explicitly states otherwise.

---

## 📦 Artefact sourcing — Cloudsmith

All artefacts are hosted in the Cloudsmith internal mirror before deployment:

| Artefact type | Hosted as | Retrieved via |
|---|---|---|
| Docker images | Cloudsmith Docker registry | `docker pull <cloudsmith-url>/...` |
| Helm chart tarballs | Cloudsmith generic/Helm repo | `get_url` to `download_cache_dir` |
| Binaries (kind, helm, etc.) | Cloudsmith generic repo | `get_url` to `download_cache_dir` |
| Python packages | Cloudsmith PyPI mirror | pip with `--index-url` pointing to Cloudsmith |

If an artefact is not yet in Cloudsmith, raise a Platops ticket to have it uploaded before beginning implementation.

---

## 🗄️ Cache directory pattern

Each role that manages binaries, charts, or images should define a `download_cache_dir` variable and download all artefacts there before use:

```yaml
# defaults/main.yml
myapp_dir: /pyrc/myapp
myapp_download_cache_dir: "{{ myapp_dir }}/cache"
```

Always set `checksum` on `get_url` — it enables idempotent re-runs (skips if the file already exists and matches) and guards against corrupted downloads.

---

## 🐳 Docker image handling

The correct sequence for loading images into an air-gapped environment: pull from Cloudsmith → re-tag to canonical names → load into kind (if applicable).

See working example: `~/.claude/_rules/lazy_load/style_guide_standards/infra/ansible/templates/template_docker_airgapped.yml`

- Do not attempt to load images using their Cloudsmith URL name — kind will not resolve them. Always load using the canonical name after re-tagging.

---

## ⎈ Helm chart deployment

Pass the local `.tgz` path to `helm upgrade` instead of a repo URL. Never add a public Helm repo with `helm repo add` on the target host.

See working example: `~/.claude/_rules/lazy_load/style_guide_standards/infra/ansible/templates/template_helm_deploy.yml`

---

## ✅ Pre-deployment checklist

Before implementing a role targeting air-gapped hosts, confirm:

- [ ] All Docker images are available in Cloudsmith
- [ ] All Helm chart tarballs are available in Cloudsmith
- [ ] All binaries are available in Cloudsmith
- [ ] SHA256 checksums are captured for all `get_url` tasks
- [ ] No task references a public URL (PyPI, Docker Hub, GitHub, helm.sh)
