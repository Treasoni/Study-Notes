---
name: tool-registry
description: Use when the collect skill needs to discover available search/fetch tools, when tool availability is uncertain, or when the registry file ~/.claude/rules/tool-registry.yaml is missing or stale (older than 7 days)
---

# Tool Registry

Discovers available search and fetch tools in the current environment, evaluates their capabilities, and writes a YAML registry that the collect skill (and others) read instead of hardcoding tool dependencies.

## Auto-Refresh Logic

Check `~/.claude/rules/tool-registry.yaml` before scanning:

1. If file does not exist — run full scan
2. If `metadata.generated_at` is older than `metadata.ttl_days` (default 7) — run full scan
3. If file exists and is fresh — skip scan, use existing registry

```powershell
# PowerShell: check registry age
$regPath = "$env:USERPROFILE\.claude\rules\tool-registry.yaml"
if (Test-Path $regPath) {
    $content = Get-Content $regPath -Raw
    if ($content -match 'generated_at:\s*"([^"]+)"') {
        $generated = [DateTime]::Parse($Matches[1])
        $age = (Get-Date) - $generated
        if ($age.TotalDays -gt 7) { "STALE" } else { "FRESH" }
    } else { "STALE" }
} else { "MISSING" }
```

## Execution Steps

### Step 1: Scan Built-in Tools

Built-in tools are always available. Add them directly:

| Tool | Type | Capabilities | Reliability |
|------|------|-------------|-------------|
| WebSearch | builtin | general_search, news, realtime | high |
| WebFetch | builtin | url_fetch, text_extraction | high |

These entries are unconditional — no probing needed.

### Step 2: Scan MCP Servers

Call `ListMcpResourcesTool` with no parameters to discover connected MCP servers.

For each server returned:
- Record `name` (server identifier)
- Record available `resources` (URIs listed)
- Set `status: available`
- Set `reliability: medium` (MCP connections can be transient)
- Classify capabilities based on server name and resource types:
  - GitHub-related servers → `code_search, repo_management, issue_tracking`
  - File-related servers → `file_access, search`
  - Other → inspect resource URIs for hints

If `ListMcpResourcesTool` fails or returns empty, record no MCP tools (do not error out).

### Step 3: Scan CLI Tools

Check for `opencli` in PATH:

```powershell
Get-Command opencli -ErrorAction SilentlyContinue
```

If found:
- Run `opencli list -f json` to discover available adapters
- Each adapter group becomes an entry with `type: cli`, `status: available`
- Capabilities derived from adapter strategy: `PUBLIC` → `web_search`, `COOKIE`/`INTERCEPT`/`UI` → `authenticated_scraping`
- Set `reliability: medium` (CLI tools depend on installation state)

If not found:
- Record opencli with `status: not_installed`, `reliability: low`

Also check for other useful CLI tools in PATH:
- `defuddle` → `web_fetch, content_extraction`
- `jq` → `json_processing`
- `gh` → `github_cli`

### Step 4: Calculate Priorities

Priority is a numeric score (1 = highest, 10 = lowest). Calculate per-tool:

```
base_score = 5

# Availability adjustment
if status == "available": base_score -= 2
elif status == "not_installed": base_score += 3
elif status == "error": base_score += 2

# Capability coverage (more capabilities = better)
cap_count = len(capabilities)
if cap_count >= 4: base_score -= 1
elif cap_count <= 1: base_score += 1

# Reliability adjustment
if reliability == "high": base_score -= 1
elif reliability == "low": base_score += 1

# Clamp to 1-10
priority = max(1, min(10, base_score))
```

Built-in tools typically score 1-2. MCP tools score 3-5. CLI tools score 2-6 depending on installation.

### Step 5: Write Registry File

Write the complete registry to `~/.claude/rules/tool-registry.yaml`.

**Important:** If user has previously set a `priority` value manually in the registry, respect it. Only calculate priority for new or updated entries. To detect manual override: compare existing `priority` with freshly calculated value — if they differ and the entry was not updated in this scan, preserve the manual value.

## Registry YAML Format

```yaml
# ~/.claude/rules/tool-registry.yaml
metadata:
  generated_at: "2026-06-01T10:00:00Z"
  generator: tool-registry skill v1.0
  ttl_days: 7
  scan_environment: "windows"  # windows | linux | macos

search_tools:
  - name: WebSearch
    type: builtin
    priority: 1
    status: available
    description: "Claude built-in web search"
    capabilities:
      - general_search
      - news
      - realtime
    reliability: high

  - name: opencli
    type: cli
    priority: 3
    status: available
    description: "OpenCLI multi-site search and scraping"
    capabilities:
      - web_search
      - authenticated_scraping
      - structured_data
    reliability: medium
    details:
      adapter_count: 12
      strategies:
        - PUBLIC
        - COOKIE

fetch_tools:
  - name: WebFetch
    type: builtin
    priority: 1
    status: available
    description: "Claude built-in page fetcher"
    capabilities:
      - url_fetch
      - text_extraction
    reliability: high

  - name: defuddle
    type: cli
    priority: 2
    status: available
    description: "Clean markdown extraction from web pages"
    capabilities:
      - web_fetch
      - content_extraction
      - metadata_extraction
    reliability: high

mcp_tools:
  - name: github
    type: mcp
    priority: 3
    status: available
    description: "GitHub MCP server"
    capabilities:
      - code_search
      - repo_management
      - issue_tracking
    reliability: medium
    resources_count: 0  # tools, not resources
```

## Field Reference

| Field | Required | Values |
|-------|----------|--------|
| `name` | yes | Tool identifier |
| `type` | yes | `builtin` \| `cli` \| `mcp` |
| `priority` | yes | 1-10, lower = preferred |
| `status` | yes | `available` \| `not_installed` \| `error` \| `disabled` |
| `description` | yes | One-line summary |
| `capabilities` | yes | Array of capability tags |
| `reliability` | yes | `high` \| `medium` \| `low` |
| `details` | no | Tool-specific metadata (adapter count, strategies, etc.) |

## Capability Tags

Standard tags for classification:

| Tag | Meaning |
|-----|---------|
| `general_search` | Broad web search |
| `news` | News and current events |
| `realtime` | Real-time information |
| `web_search` | Site-specific search via adapters |
| `authenticated_scraping` | Requires login/cookies |
| `structured_data` | Returns structured (JSON/YAML) output |
| `url_fetch` | Fetch and return page content |
| `text_extraction` | Extract readable text from HTML |
| `content_extraction` | Clean markdown extraction |
| `metadata_extraction` | Extract page metadata |
| `code_search` | Search code repositories |
| `repo_management` | Create/update repos, PRs, issues |
| `issue_tracking` | Issue and discussion management |
| `file_access` | Read/write files |
| `json_processing` | Parse and transform JSON |

## How Other Skills Consume This

The collect skill reads the registry and selects tools:

```yaml
# Pseudocode for collect skill
registry = Read("~/.claude/rules/tool-registry.yaml")
available_search = registry.search_tools | where status == "available" | sort priority
available_fetch = registry.fetch_tools | where status == "available" | sort priority
# Pick top-N tools by priority
```

Skills should NOT hardcode tool names. They should read the registry and adapt to what is available.

## Don't

- Don't hardcode tool availability — always scan
- Don't overwrite manually set priorities without reason
- Don't error out if a scan step fails — record `status: error` and continue
- Don't scan on every invocation — respect the TTL
- Don't include tools with `status: error` or `status: not_installed` in the active tool lists that skills consume (but do include them in the registry for diagnostics)
