# Codex CLI Slash Commands & Developer Commands Reference

Source: https://learn.chatgpt.com/docs/developer-commands?surface=cli
Fetched: 2026-07-11

## Overview

Reference for commands and slash commands in Codex developer surfaces. These do not apply to ChatGPT web.

## Built-in Slash Commands (in-session, triggered by `/`)

### Session Commands
| Command | Purpose |
|---------|---------|
| `/compact` | Compress context to save tokens |
| `/diff` | View current Git diff |
| `/review` | Have another Codex agent review your code |
| `/resume` | Resume a previous conversation |
| `/fork` | Clone current conversation to a new thread |
| `/plan` | Plan mode — plan only, don't execute |
| `/quit` / `/exit` | Exit Codex |
| `/clear` | Clear session |
| `/rewind` | Go back to a previous state |
| `/checkpoints` | File-level undo points |

### Config/Model Commands
| Command | Purpose |
|---------|---------|
| `/model` | Switch model or adjust reasoning level |
| `/personality` | Switch personality: `friendly`, `pragmatic`, `none` |
| `/permissions` | Adjust permissions |
| `/status` | Show working directory, model, token usage |
| `/agent` | Manage agents (subagent threads) |
| `/experimental` | Toggle experimental features (e.g., Multi-agents) |
| `/fast` | Toggle Fast mode (1.5x speed) |
| `/goal` | Set/pause/resume/clear a persistent task goal |

### Development/Tools Commands
| Command | Purpose |
|---------|---------|
| `/init` | Create AGENTS.md in project |
| `/skills` | Browse and insert skills |
| `/mcp` | List connected MCP tools |
| `/plugins` | Plugin management interface |
| `/theme` | Change theme/colors |
| `/statusline` | Customize bottom status bar |
| `/debug-config` | Debug config loading order |
| `/hookify` | Conversational hook creation |
| `/apps` | App integrations |
| `/memories` | Memory management (use, generate, reset) |
| `/archive` | Session archiving |

### Persistence Commands
| Command | Purpose |
|---------|---------|
| `/export session.json` | Export current session |
| `/load session.json` | Load previous session |
| `/feedback` | Submit feedback |

## Global CLI Flags

| Flag | Type | Details |
|------|------|---------|
| `--add-dir` | path | Grant additional directories write access |
| `-a` / `--ask-for-approval` | string | `untrusted | on-request | never` |
| `-C` / `--cd` | path | Set working directory |
| `-c` / `--config` | key=value | Override config values (parses as TOML) |
| `--yolo` | boolean | Bypass all approvals and sandbox |
| `--dangerously-bypass-hook-trust` | boolean | Skip hook trust for automation |
| `--disable` | feature | Force-disable a feature flag |
| `--enable` | feature | Force-enable a feature flag |
| `-i` / `--image` | path | Attach images to initial prompt |
| `--local-provider` | string | `lmstudio` or `ollama` |
| `-m` / `--model` | string | Override model |
| `--no-alt-screen` | boolean | Disable alternate screen mode |
| `--oss` | boolean | Use local open-source model provider |
| `-p` / `--profile` | string | Layer profile config on user config |
| `--remote` | URL | Connect to remote app-server |
| `--remote-auth-token-env` | env_var | Bearer token env var for --remote |
| `-s` / `--sandbox` | string | Sandbox policy |
| `--search` | boolean | Enable live web search |
| `--strict-config` | boolean | Error on unrecognized config fields |
| `PROMPT` | string | Optional text instruction |

## CLI Subcommands (full reference)

| Command | Maturity | Description |
|---------|----------|-------------|
| `codex` | Stable | Launch TUI |
| `codex app` | Stable | Launch desktop app |
| `codex apply` | Stable | Apply cloud task diff (alias: `codex a`) |
| `codex archive` | Stable | Archive a saved session |
| `codex cloud` | Experimental | Browse/execute cloud tasks |
| `codex completion` | Stable | Shell completion scripts |
| `codex delete` | Stable | Delete a saved session |
| `codex doctor` | Stable | Diagnostic report |
| `codex exec` | Stable | Non-interactive execution (alias: `codex e`) |
| `codex execpolicy` | Experimental | Check execution policy rules |
| `codex features` | Stable | List/enable/disable feature flags |
| `codex fork` | Stable | Fork a previous session |
| `codex login` | Stable | Authenticate |
| `codex logout` | Stable | Remove credentials |
| `codex mcp` | Stable | Manage MCP servers |
| `codex mcp-server` | Stable | Run Codex as MCP server |
| `codex plugin` | Stable | Plugin management |
| `codex plugin marketplace` | Stable | Manage plugin marketplaces |
| `codex remote-control` | Experimental | Remote control for app-server |
| `codex resume` | Stable | Continue a previous session |
| `codex review` | Stable | Non-interactive code review |
| `codex sandbox` | Stable | Run commands inside sandbox |
| `codex unarchive` | Stable | Restore archived session |
| `codex update` | Stable | Self-update |

## Shell Completions

```bash
# Zsh
codex completion zsh > "${fpath[1]}/_codex"
# Bash
codex completion bash > /etc/bash_completion.d/codex
# Fish
codex completion fish > ~/.config/fish/completions/codex.fish
```

## Feature Flags Management

```
codex features list                    # list all flags
codex features enable shell_snapshot   # enable a flag
codex features disable shell_snapshot  # disable a flag
```

These persist in `$CODEX_HOME/config.toml`.
