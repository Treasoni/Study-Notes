# Codex CLI Configuration: feiskyer/codex-settings Community Collection

Source: https://github.com/feiskyer/codex-settings
Fetched: 2026-07-11

## Overview

A curated collection of Codex CLI settings, configurations, skills, and prompts. Supports multiple model providers (LiteLLM/Copilot proxy, ChatGPT subscription, Azure OpenAI, OpenRouter).

## Quick Start

```bash
# Clone to ~/.codex
git clone https://github.com/feiskyer/codex-settings ~/.codex
# Or symlink
```

Or install skills via npx:
```bash
npx -y skills add feiskyer/codex-settings --list        # list skills
npx -y skills add --all feiskyer/codex-settings          # install all
npx -y skills add feiskyer/codex-settings                 # manually select
```

## Configuration

Default `config.toml` uses LiteLLM as a gateway:
```toml
model = "gpt-5"
model_provider = "github"
# points to localhost:4000 (LiteLLM proxy)
approval_policy = "on-request"
```

## Alternative Configs

| Config | Description |
|--------|-------------|
| `configs/chatgpt.toml` | Uses ChatGPT subscription provider |
| `configs/azure.toml` | Uses Azure OpenAI service |
| `configs/github-copilot.toml` | Uses GitHub Copilot via LiteLLM proxy |
| `configs/openrouter.toml` | Uses OpenRouter provider |

## Custom Prompts Included

| Prompt | Description |
|--------|-------------|
| `deep-reflector` | Analyzes dev sessions for learnings |
| `insight-documenter` | Captures breakthroughs into reusable knowledge |
| `instruction-reflector` | Analyzes and improves AGENTS.md instructions |
| `github-issue-fixer` | Implements fixes for GitHub issues with PR |
| `github-pr-reviewer` | Thorough PR code analysis |
| `ui-engineer` | Production-ready frontend solutions |
| `prompt-creator` | Creates Codex custom prompts |

## Skills Included (Experimental)

| Skill | Description |
|-------|-------------|
| **claude-skill** | Hands-off task handoff to Claude Code CLI |
| **autonomous-skill** | Long-running task automation (dual-agent pattern) |
| **deep-research** | Multi-instance research orchestration |
| **nanobanana-skill** | Image generation via Google Gemini API |
| **youtube-transcribe-skill** | YouTube subtitle extraction |
| **kiro-skill** | Interactive feature development from idea to implementation |
| **spec-kit-skill** | GitHub Spec-Kit integration for spec-driven development |

## MCP Servers in Config

```toml
[mcp_servers.claude]
command = "npx"
args = ["-y", "@anthropic-ai/claude-code-mcp"]

[mcp_servers.exa]
command = "npx"
args = ["-y", "exa-mcp-server"]

[mcp_servers.chrome]
command = "npx"
args = ["-y", "@anthropic-ai/chrome-mcp"]
```

## Profiles

Define named config files for different scenarios:
```toml
model = "gpt-5.1-codex-max"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Use with: `codex --profile openrouter`
