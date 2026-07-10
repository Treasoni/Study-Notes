# Codex CLI Overview and Setup

Source: https://learn.chatgpt.com/docs/codex/cli
Fetched: 2026-07-11

## Installation

**macOS/Linux (standalone installer - recommended):**
```
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```
The same command also updates Codex.

**Windows (PowerShell):**
```
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

**npm (cross-platform):**
```
npm install -g @openai/codex
```

**Homebrew (macOS):**
```
brew install --cask codex
```

**Binary downloads from GitHub Releases:**
- `codex-aarch64-apple-darwin.tar.gz` (macOS Apple Silicon)
- `codex-x86_64-apple-darwin.tar.gz` (macOS x86_64)
- `codex-x86_64-unknown-linux-musl.tar.gz` (Linux x86_64)
- `codex-aarch64-unknown-linux-musl.tar.gz` (Linux arm64)

## First Run & Authentication

1. Open a project directory and run `codex`
2. On first launch, choose **Sign in with ChatGPT** (recommended for ChatGPT Plus, Pro, Business, Edu, or Enterprise plan users)
3. API key authentication is also available via `OPENAI_API_KEY` environment variable

## CLI Interface

The interactive TUI displays:
- Active model (e.g., `gpt-5.6-sol medium`)
- Working directory
- Prompt area with example task suggestions

## Key CLI Flags

| Flag | Description |
|------|-------------|
| `--add-dir` | Grant additional directories write access |
| `-a` / `--ask-for-approval` | `untrusted | on-request | never` |
| `-C` / `--cd` | Set working directory |
| `-c` / `--config` | Override config values (TOML-parsed) |
| `--yolo` | Bypass all approvals and sandbox (containers only) |
| `--disable` / `--enable` | Force-disable/enable feature flags |
| `-i` / `--image` | Attach images to initial prompt |
| `--model` / `-m` | Override model |
| `--oss` | Use local open-source model (Ollama/LM Studio) |
| `--profile` / `-p` | Use named profile config |
| `--sandbox` / `-s` | `read-only | workspace-write | danger-full-access` |
| `--search` | Enable live web search |

## Key Subcommands

| Command | Description |
|---------|-------------|
| `codex` | Launch interactive TUI |
| `codex exec` | Non-interactive execution (alias: `codex e`) |
| `codex resume` | Resume a previous session |
| `codex fork` | Fork a previous session |
| `codex review` | Non-interactive code review |
| `codex mcp` | Manage MCP servers |
| `codex mcp-server` | Run Codex as an MCP server |
| `codex plugin` | Plugin management |
| `codex plugin marketplace` | Manage plugin marketplaces |
| `codex login` | Authenticate |
| `codex logout` | Remove stored credentials |
| `codex completion` | Generate shell completion scripts |
| `codex doctor` | Generate diagnostic report |
| `codex update` | Self-update |
| `codex archive` / `codex unarchive` | Manage session lifecycle |
| `codex apply` | Apply cloud task diff locally |
| `codex cloud` | Browse/execute cloud tasks |
| `codex features` | Manage feature flags |
| `codex sandbox` | Run commands inside sandbox |
| `codex app` | Launch desktop app |
| `codex delete` | Delete a saved session |

## Configuration

- Primary config file: `~/.codex/config.toml`
- Auth file: `~/.codex/auth.json`
- Config format: TOML (not JSON)

## Sandbox Modes

| Mode | Read | Write | Network |
|------|------|-------|---------|
| `read-only` | Yes | No | No |
| `workspace-write` | Yes | Project + temp | Default off |
| `danger-full-access` | Yes | Full system | Full access |

## Approval Policies

| Policy | Behavior |
|--------|----------|
| `untrusted` | Prompt for untrusted commands |
| `on-request` | Model decides when to ask |
| `never` | Auto-approve all |
| `on-failure` | (Deprecated) Ask only on failure |

## 5 Available Surfaces

1. Codex CLI (terminal)
2. Desktop app
3. ChatGPT web
4. IDE extension
5. Codex cloud
