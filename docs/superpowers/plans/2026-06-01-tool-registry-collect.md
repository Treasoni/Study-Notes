---
change: tool-registry-collect-refactor
design-doc: docs/superpowers/specs/2026-06-01-tool-registry-collect-design.md
base-ref: manual-windows-no-bash
archived_with: 2026-06-01-tool-registry-collect-refactor
---

# Implementation Plan: Tool Registry + Collect Refactoring

## Overview

Create a tool discovery layer and refactor the collect skill to use it, merging collect+curate into a single phase.

## Tasks

### Task 1: Create tool-registry skill

**File**: `.claude/skills/tool-registry/SKILL.md`

Create a new skill that:
- Probes built-in tools (WebSearch, WebFetch) — always marks as available
- Checks MCP servers via ListMcpResourcesTool — discovers acgithub and others
- Checks CLI tools (opencli) — checks if in PATH
- Evaluates capabilities and calculates dynamic priorities
- Writes `~/.claude/rules/tool-registry.yaml`
- Auto-refreshes if registry is >7 days old

### Task 2: Create rules directory

**File**: `~/.claude/rules/` (user home directory)

Ensure the rules directory exists for storing tool-registry.yaml.

### Task 3: Test tool-registry skill

Run the tool-registry skill and verify:
- YAML output is valid
- All available tools are discovered
- Priority calculation is reasonable
- Status reflects actual tool availability

### Task 4: Refactor collect skill

**File**: `.claude/skills/collect/SKILL.md`

Changes:
- Remove hardcoded opencli dependency
- Add tool-registry reading step (with auto-refresh logic)
- Add user scope discussion (source count, types, depth)
- Add dynamic tool selection (read priority from registry)
- Add fallback strategy (WebSearch/WebFetch always available)
- Merge curate logic inline (score, dedup, classify)

### Task 5: Merge curate into collect

**File**: `.claude/skills/collect/SKILL.md`

Add inline curate logic:
- Score each file (1-5) on authority, freshness, completeness, readability
- Mark duplicates for removal
- Classify into core_concepts, practical_examples, advanced
- Remove low-quality files
- Output metadata.yaml with scores and classifications

### Task 6: Update collector agent

**File**: `.claude/agents/collector.md`

Update agent definition to reflect:
- New collect+curate merged workflow
- Tool registry integration
- User scope discussion

### Task 7: Update phases documentation

**File**: `docs/phases.md`

Update to reflect:
- Merged collect+curate phase
- Tool registry auto-discovery
- User scope discussion step

### Task 8: Update CLAUDE.md if needed

**File**: `CLAUDE.md`

Review and update if directory convention or phase descriptions need changes.

### Task 9: Test without opencli

Verify collect works using only WebSearch/WebFetch:
- Run collect with a topic
- Confirm search results are obtained
- Confirm fetch works
- Confirm curate logic runs inline

### Task 10: Test with opencli available

Verify collect uses opencli when available:
- Run collect with opencli installed
- Confirm opencli is selected by priority
- Confirm fallback works if opencli fails

### Task 11: Test tool-registry MCP detection

Verify tool-registry discovers MCP servers:
- Run tool-registry with acgithub connected
- Confirm MCP tools appear in registry
- Confirm correct capabilities listed

### Task 12: Test user scope discussion

Verify scope discussion controls collection:
- Run collect, choose "few (3-5)" sources
- Confirm only 3-5 files collected
- Run collect, choose "many (15+)" sources
- Confirm more files collected
