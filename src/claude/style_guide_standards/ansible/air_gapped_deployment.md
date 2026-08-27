# ✈️ Air-Gapped Deployment

> **Scope:** This page describes Payroc-specific conventions for the `pyrc-cac-ans` estate.
> It is not generic Ansible guidance — it reflects constraints and tooling choices specific
> to Payroc's infrastructure.

Standards for deploying roles into environments with no outbound internet access. STG and PRD
hosts in this estate have zero outbound connectivity — all artefacts must be sourced before
deployment and served from an internal mirror.

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

All artefacts are hosted in the Cloudsmith internal mirror before deployment. This covers:

| Artefact type | Hosted as | Retrieved via |
|---|---|---|
| Docker images | Cloudsmith Docker registry | `docker pull <cloudsmith-url>/...` |
| Helm chart tarballs | Cloudsmith generic/Helm repo | `get_url` to `download_cache_dir` |
| Binaries (kind, helm, etc.) | Cloudsmith generic repo | `get_url` to `download_cache_dir` |
| Python packages | Cloudsmith PyPI mirror | pip with `--index-url` pointing to Cloudsmith |

If an artefact is not yet in Cloudsmith, raise a Platops ticket to have it uploaded before
beginning implementation. Do not design a workaround that pulls from the public internet.

---

## 🗄️ Cache directory pattern

Each role that manages binaries, charts, or images should define a `download_cache_dir`
variable (defaulting to a subdirectory of the role's working directory) and download all
artefacts there on the target host before use.

```yaml
# defaults/main.yml
myapp_dir: /pyrc/myapp
myapp_download_cache_dir: "{{ myapp_dir }}/cache"
```

```yaml
- name: Create cache directory
  ansible.builtin.file:
    path: "{{ myapp_download_cache_dir }}"
    state: directory
    mode: "0755"

- name: Download Helm chart tarball
  ansible.builtin.get_url:
    url: "{{ myapp_chart_url }}"
    dest: "{{ myapp_download_cache_dir }}/myapp-{{ myapp_chart_version }}.tgz"
    checksum: "sha256:{{ myapp_chart_checksum }}"
  # get_url is idempotent — no changed_when needed (skips if file exists and checksum matches)
```

Always set `checksum` on `get_url` — it enables idempotent re-runs (skips if the file
already exists and matches) and guards against corrupted downloads.

---

## 🐳 Docker image handling

The correct sequence for loading images into an air-gapped environment:

### 1. Pull from Cloudsmith to the host Docker daemon

```yaml
- name: Pull Airbyte images from Cloudsmith
  community.docker.docker_image:
    name: "{{ item.cloudsmith_name }}"
    source: pull
  loop: "{{ myapp_images }}"
  no_log: true   # if item contains credentials
```

### 2. Re-tag to canonical names

Images pulled from Cloudsmith carry the Cloudsmith registry URL as their name. Tools like
`kind` and Kubernetes resolve images by canonical name (e.g. `airbyte/webapp:1.5.1`). Re-tag
after pulling:

```yaml
- name: Re-tag images to canonical names
  ansible.builtin.command:
    cmd: docker tag {{ item.cloudsmith_name }} {{ item.canonical_name }}
  loop: "{{ myapp_images }}"
  changed_when: false   # tag is idempotent; docker tag always exits 0
```

### 3. Load into kind (if deploying to a kind cluster)

```yaml
- name: Load images into kind cluster
  ansible.builtin.command:
    cmd: kind load docker-image {{ item.canonical_name }} --name {{ kind_cluster_name }}
  loop: "{{ myapp_images }}"
  register: result
  changed_when: "'Image loaded' in result.stdout"
```

Do not attempt to load images using their Cloudsmith URL name — kind will not resolve them.
Always load using the canonical name after re-tagging.

---

## ⎈ Helm chart deployment

Pass the local `.tgz` path to `helm upgrade` instead of a repo URL:

```yaml
- name: Deploy application via Helm
  ansible.builtin.command:
    cmd: >
      helm upgrade --install {{ helm_release_name }}
      {{ myapp_download_cache_dir }}/myapp-{{ myapp_chart_version }}.tgz
      --namespace {{ myapp_namespace }}
      --values -
  args:
    stdin: "{{ myapp_helm_values | to_yaml }}"
  register: result
  changed_when: "'STATUS: deployed' in result.stdout"
  no_log: true   # values may contain secrets
```

- Never add a public Helm repo with `helm repo add` on the target host.
- Use `--values -` (stdin) for values that contain secrets — see `secrets_and_inventory.md`.

---

## ✅ Pre-deployment checklist

Before implementing a role targeting air-gapped hosts, confirm:

- [ ] All Docker images are available in Cloudsmith
- [ ] All Helm chart tarballs are available in Cloudsmith
- [ ] All binaries are available in Cloudsmith
- [ ] SHA256 checksums are captured for all `get_url` tasks
- [ ] No task references a public URL (PyPI, Docker Hub, GitHub, helm.sh)
