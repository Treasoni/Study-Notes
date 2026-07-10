# Codex CLI Best Practices Guide

Source: https://github.com/shanraisshan/codex-cli-best-practice
Fetched: 2026-07-11

## Subagents Configuration

Configured as TOML files under `.codex/agents/<name>.toml`. Custom agents registered under `[agents.<name>]` with dedicated role configs. Global settings under `[agents]`: `max_threads`, `max_depth`, `job_max_runtime_seconds`.

**Built-in agents:** `default`, `worker`, `explorer`.

**Tips:**
- Create feature-specific sub-agents rather than generic roles (e.g., QA, backend engineer)
- Use multi-agent setups to "throw more compute at a problem" and keep main context clean
- Separate context windows produce better results

## Skills (Best Practices)

Location: `.agents/skills/<name>/SKILL.md`. Required frontmatter includes `name` and `description`.

**7 Tips:**
1. Use clear name and description for auto-discovery
2. Skills are folders, not files — use `references/`, `scripts/`, `examples/` subdirectories
3. Build a Gotchas section in every skill — highest-signal content
4. The description is a trigger, not a summary — write it for the model
5. Don't state the obvious — focus on pushing Codex beyond default behavior
6. Give goals and constraints, not prescriptive step-by-step instructions
7. Use the built-in skill creator to scaffold new skills

## Plugins

Defined in `.codex-plugin/plugin.json`. Distributable bundles combining skills + app integrations + MCP servers. Acts as a local/personal marketplace system. Built-in: `$plugin-creator`. Browse via `/plugins` or Codex App.

## Marketplace (v0.121.0+, beta)

Plugin catalog system managed via CLI:
```
codex plugin marketplace add|upgrade|remove
```
Accepts GitHub shorthand, git URLs, and local directories. Manifest at `.agents/plugins/marketplace.json`.

## Memories (v0.119.0+, beta)

Cross-session memory pipeline at `$CODEX_HOME/memories/`. Enable via `[features] memories = true`. Configure under `[memories]`. TUI control via `/memories`.

**Tips:**
- Enable memories once and forget about it — consolidation runs between sessions, not mid-turn
- Set `no_memories_if_mcp_or_web_search = true` for threads touching secrets or untrusted content

## AGENTS.md Tips

- Keep it concise — 150 lines is a useful heuristic, but the limit is byte-based (32 KiB)
- Use AGENTS.override.md for personal preferences without affecting the team
- Any developer should be able to launch Codex, say "run the tests" and it works on the first try
- Keep codebases clean — partially migrated frameworks confuse models
- Use config.toml for harness-enforced behavior, not AGENTS.md

## Hooks Tips

- Use hooks for logging, security scanning, and validation
- Use hooks for auto-formatting code — Codex generates well-formatted code, the hook handles the last 10%
- Branch SessionStart on `source` (`startup | resume | clear`) — skip heavy context on clear

## Orchestration Pattern

The core pattern: **Research -> Plan -> Execute -> Review -> Ship**

Agent -> Skill pattern works well. The full Command -> Agent -> Skill pattern is not yet achievable in Codex CLI because custom commands aren't supported.

## Workflow Frameworks

Popular community workflow frameworks (with stars/agents/skills counts):
- Superpowers (218k stars, 5 agents, 14 skills)
- Spec Kit (108k stars)
- gstack (107k stars, 41 skills)
- Get Shit Done (64k stars, 33 agents)
- oh-my-codex (30k stars, 19 agents, 36 skills)
- Compound Engineering (20k stars, 49 agents, 42 skills)

## General Tips

- Challenge Codex: "prove to me this works" and have it diff between branches
- Use `/plan` for explicit phase-wise gated plans
- Write detailed specs and reduce ambiguity before handing work off
- Spin up a second Codex or cross-model setup to review your plan
