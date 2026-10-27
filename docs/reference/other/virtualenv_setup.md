# 🐍 Virtual Environment Setup

Using a virtual environment keeps project dependencies isolated from system Python packages — it uses Python's built-in `venv` module with Python 3.10 or newer.

---

## 1. 🐍 Check your Python

```bash
python3 --version
```

- **Need 3.10 or newer:** on macOS the built-in `python3` is 3.9, so install a newer one with `brew install python@3.13`.
- **No extra tool:** `venv` ships with Python, so there's nothing else to install.

---

## 2. 📁 Create a Virtual Environment

Run the following in the project root:

```bash
python3 -m venv venv
```

- **Why not plain `pip install`:** Homebrew's Python refuses installs outside a virtual environment (PEP 668), so packages go in `venv/`.

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
- See the [Python environment standard](../../../src/claude/_reference/_style_guide_standards/python/_python_environment.md) for `requirements.txt` conventions and pinning rules.
