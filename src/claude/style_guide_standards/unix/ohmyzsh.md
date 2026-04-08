# 🐚 Oh My Zsh

The team uses [Oh My Zsh](https://ohmyz.sh/) as the standard shell framework on top of `zsh`. Setup is automated via scripts in [`dmt-scripts-environments`](https://github.com/payroc/dmt-scripts-environments/tree/main/src/sh/setup_scripts/ohmyzsh).

---

## 🎨 Theme

The team uses [Powerlevel10k](https://github.com/romkatv/powerlevel10k) as the zsh theme:

```zsh
ZSH_THEME="powerlevel10k/powerlevel10k"
```

---

## 🔌 Plugins

The following plugins are installed and activated in `.zshrc`:

| Plugin | Source | Purpose |
|--------|--------|---------|
| `git` | Built-in (Oh My Zsh) | Git aliases and prompt info |
| `zsh-syntax-highlighting` | [zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) | Highlights valid/invalid commands as you type |
| `zsh-autosuggestions` | [zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) | Fish-style command suggestions from history |
| `zsh-completions` | [zsh-users/zsh-completions](https://github.com/zsh-users/zsh-completions) | Additional completion definitions |

The `.zshrc` plugins block should look like:

```zsh
plugins=(
    git
    zsh-syntax-highlighting
    zsh-autosuggestions
    zsh-completions
)

# Required for zsh-completions
autoload -U compinit && compinit
```

---

## ⚙️ Installation

Run the automated setup script — do not install Oh My Zsh or its plugins manually:

```bash
make install   # or invoke install_ohmyzsh.sh directly
```

The install script handles, in order:
1. Installing `zsh` (via `apt` on Linux, `brew` on macOS)
2. Installing Oh My Zsh (`RUNZSH=no CHSH=no KEEP_ZSHRC=yes` to avoid overwriting existing config)
3. Installing plugins (`zsh-syntax-highlighting`, `zsh-autosuggestions`, `zsh-completions`)
4. Installing the Powerlevel10k theme
5. Setting `zsh` as the default login shell
6. Adding the appropriate `PATH` entries to `.zshrc`
7. Setting the VS Code default terminal to `zsh`

Installation is idempotent — safe to re-run if already installed.

---

## 🖥️ VS Code integration

The setup script configures VS Code to use `zsh` as its default integrated terminal. This is applied automatically as part of `make install`.
