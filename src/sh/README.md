# git_commit.sh

Interactive commit helper enforcing [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Format

```
<type>[(<scope>)][!]: <description>
```

## Usage

```bash
./git_commit.sh              # standard
./git_commit.sh --no-verify  # pass-through git flags
```

## Prompts

| Step | Required | Notes |
|------|----------|-------|
| Type | yes | Common: `feat` `fix` `docs` `refactor` `test` `chore` — Advanced (via submenu): `build` `ci` `perf` `revert` `style` |
| Scope | no | Lists staged files; `0` to type custom, `s` or Enter to skip, re-prompts if custom is blank |
| Breaking change | no | Appends `!` before `:` |
| Description | yes | Re-prompts if blank |

Body and footers are omitted intentionally. Use `git commit --amend` to add them after.

## Examples

```
feat(parser): add ability to parse arrays
feat(api)!: remove deprecated v1 endpoints
fix: prevent racing of requests
docs: correct spelling of CHANGELOG
```

## SemVer mapping

| Commit | Bump |
|--------|------|
| `fix` | PATCH |
| `feat` | MINOR |
| Any type with `!` | MAJOR |
