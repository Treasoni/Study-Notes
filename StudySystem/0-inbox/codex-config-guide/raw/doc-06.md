# Codex CLI MCP Configuration

Source: Community resources, official documentation, and MCP server projects
Fetched: 2026-07-11

## Overview

Codex CLI supports MCP (Model Context Protocol) servers, allowing it to connect to external services and tools. MCP servers can be configured as stdio processes or HTTP endpoints.

## Configuring MCP Servers in config.toml

### Stdio Server
```toml
[mcp_servers.calculator]
command = "python"
args = ["/path/to/server.py"]
```

### HTTP Server
```toml
[mcp_servers.my-api]
url = "https://api.example.com/mcp"
```

### With Environment Variables
```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
[mcp_servers.github.env]
GITHUB_TOKEN = "ghp_xxxxx"
```

### With Transport and Timeout
```toml
[mcp_servers.subagents]
transport = "stdio"
command = "uvx"
args = ["codex-as-mcp@latest"]
tool_timeout_sec = 600
```

## Configuration Scopes

- **Global scope**: `~/.codex/config.toml`
- **Project scope**: `.codex/config.toml` (trusted projects only)

## CLI Management

```bash
codex mcp add <name> --env VAR=VALUE -- <command> [args]
codex mcp list
codex mcp remove <name>
codex mcp login <name>   # OAuth authentication
codex mcp get <name>
```

## Running Codex as an MCP Server

```bash
codex mcp-server
```

This exposes `codex()` and `codex-reply()` tools for other agents to consume.

For Claude Code consuming Codex:
```json
{
  "mcpServers": {
    "codex": {
      "type": "stdio",
      "command": "codex",
      "args": ["mcp-server"]
    }
  }
}
```

## Context Window Management

- Configure 20-30 MCPs in config, but keep under 10 enabled
- Keep under 80 tools active total
- Disable unused MCPs: `[mcp_servers.context7] enabled = false`
- Many tools consume context — "Your 200k context window before compacting might only be 70k with too many tools enabled"
- Navigate via `/plugins` or use `/mcp` to check enabled servers

## Common Community MCP Servers

| MCP | Launch Method |
|-----|---------------|
| github | `npx -y @modelcontextprotocol/server-github` |
| firecrawl | `npx -y firecrawl-mcp` |
| supabase | `npx -y @supabase/mcp-server-supabase@latest --project-ref=YOUR_REF` |
| memory | `npx -y @modelcontextprotocol/server-memory` |
| sequential-thinking | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| vercel | HTTP — `https://mcp.vercel.com` |
| railway | `npx -y @railway/mcp-server` |
| cloudflare-docs | HTTP — `https://docs.mcp.cloudflare.com/mcp` |

## Codex-Specific MCP Server Projects

| Project | Description |
|---------|-------------|
| ogmios2/claude-code-codex-mcp | Claude Code uses Codex CLI for multi-agent orchestration |
| codex-mcp (npm) | Connects IDEs or AI assistants to Codex CLI |
| LanceVCS/codex-mcp | Stateful MCP server with multi-turn conversation support |
| kky42/codex-as-mcp | Spawn Codex subagents: `spawn_agent(prompt)` and `spawn_agents_parallel(agents)` |
| itto-ki/codex-cli-architect-mcp | Technical consultation, code review, code explanation |
| madwiki/codex-persistent-mcp | Persistent sessions via `codex resume` |
| thebusted/mcp-mysql-server | MySQL database integration via MCP |

## OAuth Support

MCP servers with OAuth authentication can be configured via:
```bash
codex mcp login <name>
```

## Parallel Tool Calls (v0.121.0+)

```toml
[mcp_servers.my-server]
supports_parallel_tool_calls = true
```

## Feature: MCP Apps (v0.119.0+)

Enables resource reads, elicitations, and file-parameter uploads.
