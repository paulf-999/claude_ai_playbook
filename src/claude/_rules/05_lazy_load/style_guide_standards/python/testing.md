# 🧪 Python Testing Conventions

**Purpose:** Establish pytest conventions for test naming, structure, fixtures, mocking, and assertions — preventing testing debt and validating intended behaviour.

---

## 📋 Contents

- [Test naming & structure](#-test-naming--structure) — `testing/_naming_structure.md`
- [Pytest fixtures & mocking](#-pytest-fixtures--mocking) — `testing/_fixtures_mocking.md`
- [Assertions & exception testing](#-assertions--exception-testing) — `testing/_assertions.md`
- [Quick reference](#-quick-reference)
- [Related](#-related)

---

## 🏷️ Test naming & structure

@testing/_naming_structure.md

---

## 🔧 Pytest fixtures & mocking

@testing/_fixtures_mocking.md

---

## ✅ Assertions & exception testing

@testing/_assertions.md

---

## ⚡ Quick reference

| Goal | Pattern | Example |
|---|---|---|
| **Mock a dependency** | `MagicMock()` | `client = MagicMock(); client.create.return_value = {...}` |
| **Verify mock was called** | `assert_called_once()` | `client.create.assert_called_once()` |
| **Test exception raised** | `pytest.raises()` | `with pytest.raises(ValueError, match="pattern"):` |
| **Use temp files** | `tmp_path` fixture | `path = tmp_path / "file.txt"; path.write_text(...)` |
| **Override env var** | `monkeypatch` fixture | `monkeypatch.setattr("os.environ", {"VAR": "value"})` |
| **Setup helpers** | `_make_*()` functions | `def _make_client(): return MagicMock()` |

---

## 🔗 Related

- Parent: `python.md` — Full Python style guide including error handling, naming, imports
- Sibling: `python/logging.md` — Logging conventions
- Sibling: `python/module_organisation.md` — Module organisation and structure
