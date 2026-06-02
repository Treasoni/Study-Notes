Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
(also from DeepWiki: https://deepwiki.com/Fission-AI/OpenSpec/5.1-supported-tools and https://deepwiki.com/Fission-AI/OpenSpec/5-ai-tool-integration)

# Supported Tools

OpenSpec integrates with 29+ AI coding assistants using a two-layer architecture:

1. **Skills Layer** — Universal, cross-editor `SKILL.md` files (with YAML frontmatter) that any compatible tool can discover.
2. **Commands Layer** — Tool-specific invocation files tailored to each assistant's native format.

## Full Supported Tools List

| Tool | Tool ID | Command Support |
|---|---|---|
| Amazon Q Developer | `amazon-q` | Full adapter |
| Antigravity | `antigravity` | Full adapter |
| Auggie | `auggie` | Full adapter |
| IBM Bob Shell | `bob` | Full adapter |
| **Claude Code** | `claude` | Full adapter |
| **Cline** | `cline` | Full adapter |
| CodeBuddy | `codebuddy` | Full adapter |
| Codex | `codex` | Full adapter |
| **Continue** | `continue` | Full adapter |
| CoStrict | `costrict` | Full adapter |
| Crush | `crush` | Full adapter |
| **Cursor** | `cursor` | Full adapter |
| Factory Droid | `factory` | Full adapter |
| **ForgeCode** | `forgecode` | Skills only |
| **Gemini CLI** | `gemini` | Full adapter (TOML format) |
| **GitHub Copilot** | `github-copilot` | Full adapter (IDE only) |
| iFlow | `iflow` | Full adapter |
| Junie | `junie` | Full adapter |
| Kilo Code | `kilocode` | Full adapter |
| **Kimi CLI** | `kimi` | Skills only |
| Kiro | `kiro` | Full adapter |
| Lingma | `lingma` | Full adapter |
| **OpenCode** | `opencode` | Full adapter |
| Pi | `pi` | Full adapter |
| Qoder | `qoder` | Full adapter |
| Qwen Code | `qwen` | Full adapter |
| RooCode | `roocode` | Full adapter |
| **Trae** | `trae` | Skills only |
| **Windsurf** | `windsurf` | Full adapter |

## Delivery Modes

Configure which integration layer to use via the `delivery` setting:

- **`skills`** — Only generates `SKILL.md` files (universal compatibility)
- **`commands`** — Only generates tool-specific slash command files
- **`both`** (default) — Generates both layers

## Command Formats by Tool

| Tool | Command File Format |
|---|---|
| Claude Code | `.claude/commands/opsx/<id>.md` |
| Cursor | `.cursor/commands/opsx-<id>.md` |
| Windsurf | `.windsurf/workflows/opsx-<id>.md` |
| Gemini CLI | TOML format |
| Continue | `.prompt` extension files |
| GitHub Copilot (IDE) | `.github/prompts/` |
| Amazon Q | `.amazonq/prompts/opsx-<id>.md` |
| OpenCode | `.opencode/commands/` (hyphen format) |

## Tool-Specific Command Syntax

| Tool | Syntax Example |
|---|---|
| Claude Code | `/opsx:propose`, `/opsx:apply` |
| Cursor | `/opsx-propose`, `/opsx-apply` |
| Windsurf | `/opsx-propose`, `/opsx-apply` |
| Copilot (IDE) | `/opsx-propose`, `/opsx-apply` |
| Kimi CLI | `/skill:openspec-propose`, `/skill:openspec-apply-change` |
| Trae | `/openspec-propose`, `/openspec-apply-change` |

## Custom / Proprietary Tools

For custom/proprietary AI plugins that don't have a dedicated adapter:
- The **Skills layer** (universal `SKILL.md` files) provides the broadest compatibility — any tool that supports the Agent Skills RFC (https://agents.md/) can auto-discover them.
- Generate skills-only output and point your tool at the `.github/skills/` or `.claude/skills/` directory.

## Architecture

- **Tool Registry**: All supported tools are defined in `src/core/config.ts` in the `AI_TOOLS` constant array.
- **Command Adapters**: Each tool has an adapter file implementing `ToolCommandAdapter` interface (`formatFile`, `getFilePath`).
- **Slash Commands**: Mapped from workflow IDs — e.g., `/opsx:propose`, `/opsx:explore`, `/opsx:apply`.
- **Skills**: All tools receive the same `SKILL.md` template structure; only the directory path changes based on `skillsDir`.
