# 📋 Ansible Playbooks

## Standards

- The top-level playbook is `playbooks/site.yml`.
- Comment each role reference to describe what it does and why it runs in that position.
- Use `tags` on every role so individual roles can be run in isolation.
- Set `gather_facts` and `become` explicitly — do not rely on defaults.

---

## 💡 Example

<details>
<summary>Click to expand — <code>playbooks/site.yml</code></summary>

```yaml
---
# Playbook to set up a web server environment for hosting applications.

- name: Create (Docker) VM & Install Webserver
  hosts: sandbox        # defined in inventories/sandbox/inventory.ini
  gather_facts: no      # skip fact gathering where not needed
  become: false         # use non-root user

  roles:
    # Bootstrap secrets from local environment (.env via Makefile)
    - role: secrets_env
      tags: [secrets]

    # Install and configure the webserver in the sandbox container
    - role: webserver
      tags: [webserver]
```

</details>

---

## 🏷️ Running specific roles with tags

Tags allow individual roles to be executed in isolation without running the full playbook:

```bash
# Run only the secrets role
ansible-playbook playbooks/site.yml --tags secrets

# Run only the webserver role
ansible-playbook playbooks/site.yml --tags webserver
```
