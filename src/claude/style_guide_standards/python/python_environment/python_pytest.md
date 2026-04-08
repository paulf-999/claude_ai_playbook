# 🧪 Python Testing — pytest

- Every Python script must have an associated `pytest` test file.
- Tests are not optional — untested code is not considered complete.

## 📏 Conventions

- Test files must be named `test_<script_name>.py` and co-located in a `tests/` directory.
- Test functions must be named `test_<function_name>_<scenario>`, e.g. `test_get_secret_invalid_key`.
- All tests must pass before committing.

---

## ▶️ Running tests

```bash
pytest                                              # run all tests
pytest --cov=src --cov-report=term-missing         # run with coverage report
```

Coverage must be run and reviewed before committing. A minimum threshold may be enforced in future.

---

## 🎭 Mocking

Use [`pytest-mock`](https://github.com/pytest-dev/pytest-mock) for all mocking — do not use `unittest.mock` directly.

```python
def test_get_secret_returns_value(mocker):
    mocker.patch("module.get_secret_by_name", return_value="secret123")
```
