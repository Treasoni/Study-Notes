# CodeBuddy CLI 配置结构详解

## Source

Compiled from: codebuddy.ai/docs/cli/settings, Tencent Cloud documentation

## Overview

CodeBuddy (Tencent Cloud's AI coding assistant) uses a layered configuration system with JSON files. It supports three configuration scopes: user-level, shared project-level, and local project-level.

## Configuration Files & Layering

| File | Scope | Git |
|------|-------|-----|
| `~/.codebuddy/settings.json` | User settings -- applies to all projects | No |
| `.codebuddy/settings.json` | Shared project settings | Yes |
| `.codebuddy/settings.local.json` | Local project settings | Auto-gitignored |

## Settings Priority (Highest to Lowest)

1. Command-line arguments (one-session overrides)
2. Local project settings (`.codebuddy/settings.local.json`)
3. Shared project settings (`.codebuddy/settings.json`)
4. User settings (`~/.codebuddy/settings.json`)

Settings are merged; more specific settings add to or override broader ones.

## Settings.json Structure

```json
{
  "language": "English",
  "permissions": { ... },
  "env": { "NODE_ENV": "development" },
  "model": "gpt-5",
  "cleanupPeriodDays": 30,
  "includeCoAuthoredBy": false,
  "statusLine": { "type": "command", "command": "..." }
}
```

## Key Configuration Options

| Key | Purpose |
|-----|---------|
| `language` | Response language (auto-detect if empty) |
| `permissions` | Tool access control (allow/ask/deny rules) |
| `env` | Per-session environment variables |
| `model` | Default model override |
| `agent` | Override agent name (built-in or custom) |
| `hooks` | Pre/post tool execution commands |
| `sandbox` | Bash sandbox configuration |
| `memory` | Persistent cross-session memory |
| `autoMode` | Classifier-based auto permission rules |
| `gateway` | Remote Gateway configuration |
| `reasoningEffort` | Depth of reasoning: low/medium/high/xhigh |

## Permission System

```json
{
  "permissions": {
    "allow": ["Bash(git *)", "Read(*)"],
    "ask": ["Bash(rm *)", "Bash(git push *)"],
    "deny": ["Read(./.env)", "Read(./secrets/**)"],
    "defaultMode": "default",
    "subagentPermissionMode": "default"
  }
}
```

## Auto Mode Configuration

`autoMode` is a top-level field (not under `permissions`). It has four classifier rule arrays:

| Field | Purpose |
|-------|---------|
| `environment` | Describes trusted repositories, domains, services |
| `allow` | Actions auto-approvable under auto mode |
| `soft_deny` | Actions blocked but retriable with explicit intent |
| `hard_deny` | High-risk actions blocked by default |

Important security rule: `autoMode` is NOT read from shared `.codebuddy/settings.json` -- because "repository-committed configuration should not silently change your local machine's judgment."

## Bash Sandbox

```json
{
  "sandbox": {
    "enabled": false,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "network": {
      "allowUnixSockets": [],
      "allowLocalBinding": false
    }
  }
}
```

## Hooks

```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "echo 'Running command...'"
    }
  },
  "disableAllHooks": false,
  "allowUntrustedFrontmatterHooks": false
}
```

## Memory Configuration (Experimental)

```json
{
  "memory": {
    "autoMemoryEnabled": true,
    "typedMemory": true,
    "relevanceSelection": true,
    "memoryExtraction": false,
    "teamMemory": { "enabled": true, "userId": "my-name" }
  }
}
```

| Storage | Location |
|---------|----------|
| Personal mode | `~/.codebuddy/memories/{project-id}/` |
| Team mode | `{project}/.codebuddy/memories/@{user-id}/` |
| Global | `~/.codebuddy/memories/global/` |

## Sub-Agents

Defined in `agents/` directory (both user and project level). Sub-agents are Markdown files with YAML frontmatter, defining:
- Custom system prompts
- Restricted tool sets
- Specific models
- Two modes: **agentic** (auto-invoked) or **manual** (user-selected)

## Configuration Commands

```bash
codebuddy config list                     # show all config
codebuddy config get <key>                # get a value
codebuddy config set [options] <key> <value>   # set a value (-g for global)
codebuddy config add <key> <values...>    # add to array
codebuddy config remove <key> [values...] # remove from array
```

## Models Configuration

Defined in `models.json` (both user and project level):

```json
{
  "models": [
    {
      "id": "my-model",
      "name": "My Custom Model",
      "vendor": "OpenAI",
      "apiKey": "${API_KEY_VAR}",
      "url": "https://api.example.com/v1/chat/completions",
      "maxInputTokens": 128000,
      "maxOutputTokens": 8192,
      "supportsToolCall": true,
      "supportsImages": false
    }
  ],
  "availableModels": ["my-model", "gpt-5"]
}
```

Supports environment variable references (`${VAR_NAME}`) for secure API key handling.
