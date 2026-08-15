# 深度素材：dsh 接入 skills/hooks/mcp/rules（对照 Claude Code）

> 收集日期：2026-08-15 · 来源层级：官方仓库源码 + 官方 docs + 官方 Agent Notes（一手）

## 1. Rules / 指令文件（AGENTS.md 等价物）

- 来源：`packages/context/agent-instructions/src/config.ts`
- 默认候选：`instructionFileCandidates = ['AGENTS.md', 'CLAUDE.md']`
- 本地覆盖：`localInstructionFileCandidates = ['AGENTS.local.md', 'CLAUDE.local.md']`
- 项目根识别：从 session cwd 向上找含 `.git` 的最近祖先；无 git 用 cwd
- 用户级固定文件：`$DSH_HOME/AGENTS.md`（默认 `~/.dsh/AGENTS.md`）
- 控制开关：`workspaceContext` 配置（byte budget，可设 `false` 关闭）
- 结论：**用户现有 `CLAUDE.md` 原样生效，零迁移**

## 2. Skills

- 来源：`docs/subsystems/skills.md` + Agent Note `2026-07-05-skill-system`
- 本地扫描优先级（first-wins）：
  | Rank | 源 | 根 |
  |---|---|---|
  | 100 | project-dsh | `<projectRoot>/.dsh/skills` |
  | 200 | project-agents | `<projectRoot>/.agents/skills` |
  | 300 | custom | `Config.customSkillDirs` |
  | 400 | user-dsh | `<dshHome>/skills`（`~/.dsh/skills`） |
  | 500 | user-agents | `<agentsHome>/skills` |
  | 600 | bundled | `Config.bundledSkillDir` |
- 格式：`<name>/SKILL.md` 或 `<name>.md`（YAML frontmatter；`name`/`description` 必填，`whenToUse` 可选）；kebab-case
- 机制：热加载（watcher 监听根目录）；模型侧 `skill({name})` 工具按需加载正文（渐进式披露）
- 用户 `.dsh/skills` 扫描跳过 `.system` 子目录
- 结论：**建 `.dsh/skills/<name>/SKILL.md` 即可，格式与 Claude Code 兼容**

## 3. Hooks

- 来源：`docs/cookbook/extension-cookbook.md` + Agent Note `2026-06-30-hook-bridges`
- 两种路线：
  - **桥接复用**：`@deepseek-ai/dsh-hooks-claude-code`（CC 方言）与 `@deepseek-ai/dsh-hooks-codex`
    - 配置：`configPath` 指向 `hooks.json` 或 settings 的 `hooks` 键；`pluginRoot`/`projectDir` 做 `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PROJECT_DIR}` 替换
    - CC 支持 7 个点：SessionStart / UserPromptSubmit / PreToolUse / PostToolUse / Stop / SubagentStart / SubagentStop
    - 只跑 shell-form `type: 'command'`；http/mcp_tool/prompt/agent 解析后跳过
    - `updatedInput`（入参改写）不生效仅告警
    - `configPath` 进程级：启动读一次，相对进程启动 cwd；无 per-session 项目内发现（TODO）
  - **原生插件**：监听扩展点 `agent/session-start`、`agent/pre-step`、`agent/request`、`tools/pre-execute`、`tools/post-execute`、`agent/turn-stopping`，waterfall 返回类型化 Decision（`{kind:'deny'|'ask'}`）
- 结论：**迁移成本最低 = 桥接插件；更强大 = 原生插件（即系列 3.5 节已覆盖）**

## 4. MCP

- 来源：Agent Note `2026-07-07-mcp-client-plugin` + `docs/cookbook/extension-cookbook.md`
- 方式：每 server 一个 `@deepseek-ai/dsh-mcp-client` 插件实例（`cordis.yml`）
- 配置：`transport: 'stdio' | 'streamable-http'`；`serverName` 必填（`^[A-Za-z0-9_-]{1,32}$`，跨实例唯一）
- 工具命名：`mcp__<serverName>__<rawName>`（与 Claude Code/Codex 一致）
- 生命周期：boot 时连接→listTools→register；HMR 热换；自动重连（`reconnect.enabled: false` 可关）
- 只桥接 Tools，Resources/Prompts 不消费
- 社区辅助：`dshx mcp import`（从 `~/.claude.json` / `.mcp.json` / codex 迁移）、`dsh-extension-hub`
- 结论：**不是放 `.dsh` 文件，是 cordis.yml 插件条目**

## 5. `.dsh` 目录身份

- `$DSH_HOME`（默认 `~/.dsh`）= harness home（用户级）：含 `AGENTS.md`、`skills/`、`cordis.patch.yml`、profiles（`~/.dsh/profiles/`）
- 项目级 `.dsh/skills/`：技能源（rank 100）
- 结论：`.dsh` 是"用户级 home + 项目级 skills"，不是 hooks/mcp 的配置入口

## 关键引用（官方 URL）
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/config-catalog.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/src/config.ts
