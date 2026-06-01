# Proposal: Tool Registry + Collect Skill Refactoring

## Problem

The `collect` skill is hardcoded to depend on `opencli` for search and fetch operations. This creates:

1. **Single point of failure** — if opencli is unavailable, collect breaks entirely
2. **Wasted capabilities** — Claude's built-in WebSearch/WebFetch and MCP servers (acgithub) go unused
3. **Cognitive overhead** — users must install and learn opencli before using the study system
4. **Maintenance burden** — any search tool changes require rewriting collect

## Goal

Create a tool discovery and registry layer that:

- Auto-discovers available search/fetch tools (MCP servers, CLI tools, built-in)
- Writes capabilities to `~/.claude/rules/tool-registry.yaml`
- Enables the collect skill to dynamically select the best available tool(s)

## Scope

### In Scope

1. **New skill: `tool-registry`** — scans environment, discovers tools, writes registry
2. **Refactor: `collect` skill** — reads registry, uses available tools by priority
3. **Merge: collect + curate** — combine into single phase for efficiency (reduces subagent overhead)

### Out of Scope

- Modifying opencli itself
- Adding new MCP servers
- Changing the write/beautify pipeline

## Success Criteria

- `collect` works without opencli installed (using WebSearch/WebFetch fallback)
- `collect` leverages available MCP tools when present
- New `tool-registry` skill auto-discovers tools on first run
- Merged collect+curate reduces token usage by ~5-12k per session
