# Tasks: Tool Registry + Collect Refactoring

## Phase 1: Create tool-registry skill

- [x] 1.1 Create `.claude/skills/tool-registry/SKILL.md` — skill definition
  - Probes built-in tools (WebSearch, WebFetch)
  - Checks MCP servers via ListMcpResourcesTool
  - Checks CLI tools (opencli)
  - Writes `~/.claude/rules/tool-registry.yaml`

- [x] 1.2 Create `~/.claude/rules/` directory if not exists

- [x] 1.3 Test: run tool-registry skill, verify YAML output

## Phase 2: Refactor collect skill

- [x] 2.1 Modify `.claude/skills/collect/SKILL.md`
  - Remove hardcoded opencli dependency
  - Add tool-registry reading step
  - Add tool selection logic (priority-based)
  - Add fallback strategy (WebSearch/WebFetch always available)

- [x] 2.2 Merge curate logic into collect
  - Add inline scoring (authority, freshness, completeness, readability)
  - Add deduplication logic
  - Add classification logic
  - Output metadata.yaml alongside source files

- [x] 2.3 Update `.claude/agents/collector.md` agent definition
  - Reflect new collect+curate merged workflow

## Phase 3: Update documentation

- [x] 3.1 Update `docs/phases.md` — reflect merged collect+curate
- [x] 3.2 Update `CLAUDE.md` — if needed, update directory convention or phase descriptions

## Phase 4: Test & verify

- [ ] 4.1 Test with WebSearch/WebFetch only (no opencli)
- [ ] 4.2 Test with opencli available
- [ ] 4.3 Verify tool-registry auto-detects MCP servers
- [ ] 4.4 Verify collect produces valid curated output
