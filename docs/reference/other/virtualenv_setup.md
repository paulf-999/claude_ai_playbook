# 🐍 Virtual Environment Setup

Using a virtual environment keeps project dependencies isolated from system Python packages — the team uses `virtualenv` targeting Python 3.10.

---

## 1. 📦 Install virtualenv

If not already installed:

```bash
pip install virtualenv
```

---

## 2. 📁 Create a Virtual Environment

Run the following in the project root:

```bash
virtualenv venv                    # uses system default Python
virtualenv -p python3.10 venv      # explicitly target Python 3.10
```

This creates a `venv/` directory containing the isolated environment.

---

## 3. ▶️ Activate the Virtual Environment

```bash
source venv/bin/activate       # Linux / macOS
```

Once activated, your shell prompt will show `(venv)`.

---

## 4. 📥 Install Requirements

With the environment active, install dependencies:

```bash
pip install -r requirements.txt
```

---

## 5. ⏹️ Deactivate the Environment

When finished, deactivate with:

```bash
deactivate
```

---

## 🔍 Notes

- The `venv/` folder is ignored via `.gitignore` and should not be committed.
- Each project should have its own virtual environment — do not share environments across projects.
- See the [Python dependency management standard](../src/claude/style_guide_standards/python/python_environment/python_dependencies.md) for `requirements.txt` conventions and pinning rules.
