# 🐍 Python Environment

## 🗂️ Project structure

All Python projects must follow the standard structure defined in the [team Python template repo](https://github.com/payroc/pyrc-lib-template_python_git_repo):

```
src/my_project/   Application source code
tests/            Unit tests
docs/             Supporting documentation
```

---

## 🐍 Python version

The team currently supports and targets **Python 3.10** due to environment constraints. When writing or packaging code intended to run on others' machines, always assume Python 3.10.

---

## 📦 Virtual environment

[`python_virtual_environment.md`](./python_environment/python_virtual_environment.md) — virtualenv setup and dependency management.

---

## 📌 Dependencies

[`python_dependencies.md`](./python_environment/python_dependencies.md) — requirements.txt conventions and pinning strategy.

---

## 🔧 Linting & formatting — [`ruff`](https://github.com/astral-sh/ruff)

[`ruff`](https://github.com/astral-sh/ruff) is the primary linter and formatter for all Python code.

---

## 🧪 Testing

[`python_pytest.md`](./python_environment/python_pytest.md) — pytest standards and expectations.

---

## 🔗 Imports

@./python_environment/python_pytest.md

@./python_environment/python_virtual_environment.md

@./python_environment/python_dependencies.md
