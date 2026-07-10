# Codex vs Claude Code Configuration Differences

Source: Developer Aliyun article (https://developer.aliyun.com/article/1714675) and community comparisons
Fetched: 2026-07-11

## Comparison Table

| Aspect | Codex CLI (cx) | Claude Code (cc) |
|--------|---------------|-------------------|
| Developer | OpenAI | Anthropic |
| Default model | gpt-5.3-codex | Claude Sonnet/Opus |
| Project instructions | AGENTS.md | CLAUDE.md |
| Config format | TOML | JSON |
| Full auto mode | `--full-auto` / `--yolo` | `--dangerously-skip-permissions` |
| Built-in sandbox | Yes (Seatbelt/Landlock) | No |
| Resume last | `codex resume --last` | `claude -c` |
| Code review | `/review` | `/review` |
| Context compress | `/compact` | `/compact` |
| MCP support | Yes | Yes |
| Open source | Yes (Rust) | Yes (TypeScript) |

## Key Differences Relevant to Configuration

### Config Format
- Codex uses **TOML** (`~/.codex/config.toml`)
- Claude Code uses **JSON** (`~/.codex/claude_settings.json` or `.claude.json`)

### Project Instructions
- Codex reads `AGENTS.md` natively
- Claude Code reads `CLAUDE.md` natively
- Both can be configured to read the other as fallback

### Sandbox (Codex Differentiator)
Codex has built-in OS-level sandbox (Seatbelt on macOS, Landlock/Bubblewrap on Linux). Claude Code currently does not have a built-in sandbox.

Two-layer security:
1. **Sandbox** — OS-level physical restrictions
2. **Approval policy** — procedural controls on when to prompt the user

### Skills Standard
Both Codex CLI and Claude Code support the **Agent Skills open standard** (same SKILL.md format). Skills created for one tool can work on the other, making them cross-compatible.

### Hooks Support
- Codex: Supports hooks but the system is more experimental, with fewer events than Claude Code
- Claude Code: More mature hook system with more events

### Cross-Tool Rule Sharing

Many developers maintain shared rules across both tools using:
- `AGENTS.md` as universal format (read by Codex natively, Claude Code can be configured)
- Symlinks between `AGENTS.md` and `CLAUDE.md`
- Tools like `sync-rules`, `base-agent-rules`, `@devground/agents-md` for automation

## Strategic Considerations

When configuring both tools for the same project:
1. Put universal instructions in `AGENTS.md`
2. Have `CLAUDE.md` reference `AGENTS.md` via `@AGENTS.md` plus Claude-specific additions
3. Use config.toml for Codex-specific behavior (sandbox, approval policy)
4. Use claude_settings.json for Claude-specific behavior
