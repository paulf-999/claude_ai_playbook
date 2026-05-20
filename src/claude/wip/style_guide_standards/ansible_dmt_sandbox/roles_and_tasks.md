# 🔧 Ansible Roles & Tasks

## 🗂️ Role structure

Each role must follow the standard subdirectory structure — `tasks/` and `defaults/` are the minimum required:

```
roles/
  <role_name>/
    defaults/
      main.yml    # default variable values (all variables the role accepts)
    tasks/
      main.yml    # task entry point — all task logic starts here
    handlers/     # (if needed)
    templates/    # Jinja2 templates (if needed)
    files/        # static files (if needed)
```

- Roles must be self-contained and reusable — do not hardcode environment-specific values inside a role.
- `defaults/main.yml` must define and comment every variable the role accepts.

<details>
<summary>Click to expand — example <code>defaults/main.yml</code></summary>

```yaml
---
# Repo identity
git_repo_owner: ""
git_repo_name: ""

# Auth (injected by secrets_env role or playbook vars)
GIT_PAT_TOKEN: ""

# Checkout settings
git_repo_version: "main"
git_repo_dest_root: "/opt/git_repos"
git_repo_dest: "{{ git_repo_dest_root }}/{{ git_repo_name }}"

# Repo URL — override if switching to SSH
git_repo_url: "https://{{ GIT_PAT_TOKEN }}@github.com/{{ git_repo_owner }}/{{ git_repo_name }}.git"
```

</details>

---

## ✅ Task standards

- Every task must have a `name` in sentence case describing what it does.
- Use FQCN for all modules (`ansible.builtin.*`, `community.*`, etc.).
- Assert required variables are defined and non-empty at the start of a role — fail fast with a clear message.
- Use `register` + a follow-up `debug` or `assert` task to verify side effects where meaningful.
- Use `no_log: true` on any task that handles secrets or sensitive values.

<details>
<summary>Click to expand — example <code>tasks/main.yml</code> (clone_git_repo role)</summary>

```yaml
---
- name: Assert required vars are provided
  ansible.builtin.assert:
    that:
      - GIT_PAT_TOKEN is defined
      - GIT_PAT_TOKEN | length > 0
    fail_msg: "This role requires GIT_PAT_TOKEN to be passed in."

- name: Install git client
  ansible.builtin.apt:
    name: git
    state: present
    update_cache: yes

- name: Clone repo
  ansible.builtin.git:
    repo: "{{ git_repo_url }}"
    dest: "{{ git_repo_dest }}"
    version: "{{ git_repo_version }}"
    force: yes

- name: Check that cloned repo exists
  ansible.builtin.stat:
    path: "{{ git_repo_dest }}/.git"
  register: repo_stat

- name: Confirm repo was cloned successfully
  ansible.builtin.debug:
    msg: "Cloned {{ git_repo_owner }}/{{ git_repo_name }} into {{ git_repo_dest }}."
  when: repo_stat.stat.exists
```

</details>
