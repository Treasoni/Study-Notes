# Codex CLI Skills Configuration

Source: https://learn.chatgpt.com/docs/build-skills
Fetched: 2026-07-11

## What Are Skills

Skills extend Codex with task-specific capabilities, packaging instructions, resources, and optional scripts so Codex can follow a workflow reliably. They build on the open agent skills standard at agentskills.io.

## Progressive Disclosure & Context Budgeting

Codex starts with each skill's name, description, and file path. It loads the full SKILL.md instructions only when it decides to use a skill.

The initial skills list uses at most 2% of the model's context window, or 8,000 characters when the context window is unknown. If many skills are installed, Codex shortens skill descriptions first.

## Skill Directory Structure

```
my-skill/
├── SKILL.md              # Required: instructions + metadata
├── scripts/              # Optional: executable code
├── references/           # Optional: documentation
├── assets/               # Optional: templates, resources
└── agents/
    └── openai.yaml       # Optional: appearance and dependencies
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

The file must include `name` and `description` in YAML frontmatter.

## Invocation Methods

1. **Explicit invocation**: In CLI/IDE, run `/skills` or type `$` to mention a skill. Use `$skill-name [prompt]`.
2. **Implicit invocation**: Codex can choose a skill when your task matches the skill `description`.

Because implicit matching relies on `description`, write concise descriptions with clear scope. Front-load the key use case and trigger words.

## Creating Skills

**Via Record & Replay:** Codex records the workflow, inspects the steps, and drafts a reusable skill.

**Via built-in creator:** Run `$skill-creator` in the CLI. It asks what the skill does, when it should trigger, and whether it should stay instruction-only or include scripts.

**Manually:** Create a folder with a `SKILL.md` file. Codex detects skill changes automatically.

## Skill Scopes (Save Locations)

| Scope | Location | Suggested Use |
|-------|----------|---------------|
| REPO | `$CWD/.agents/skills` | Team-shared skills for a module |
| REPO | `$CWD/../.agents/skills` | Shared area in parent folder |
| REPO | `$REPO_ROOT/.agents/skills` | Root skills for any subfolder |
| USER | `$HOME/.agents/skills` | Personal skills across any repo |
| ADMIN | `/etc/codex/skills` | System-wide for all users |
| SYSTEM | Bundled by OpenAI | Built-in skills (skill-creator, plan) |

Codex supports symlinked skill folders.

## Enabling/Disabling Skills

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after changing `~/.codex/config.toml`.

## Optional Metadata (agents/openai.yaml)

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt to use the skill with"

policy:
  allow_implicit_invocation: false

dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

`allow_implicit_invocation` defaults to `true`. When `false`, Codex won't implicitly invoke the skill.

## Installing Curated Skills

Use `$skill-installer` to add curated skills beyond built-ins. Example: `$skill-installer linear`. Codex detects newly installed skills automatically.

## Distributing Skills with Plugins

To distribute reusable skills or bundle them with connectors, use plugins. Plugins can include one or more skills and optionally bundle app mappings, MCP server config, and presentation assets.

## Best Practices

- Keep each skill focused on one job
- Prefer instructions over scripts unless you need deterministic behavior
- Write imperative steps with explicit inputs and outputs
- Test prompts against the skill description to confirm the right trigger behavior
