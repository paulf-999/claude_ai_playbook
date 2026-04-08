# 📌 Python Dependency Management

## 📋 requirements.txt

All project dependencies are declared in a single `requirements.txt`. Pin direct dependencies exactly using `==` — do not pin transitive (indirect) dependencies, as over-pinning creates unnecessary compatibility and upgrade friction.

```
boto3==1.34.0
requests==2.31.0
```

Let pip resolve transitive dependencies automatically.

## 🔄 Updating dependencies

When updating a dependency, update the pinned version in `requirements.txt` explicitly — do not rely on `pip install --upgrade` without updating the file.
