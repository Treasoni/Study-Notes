# Codex 完整配置体系 — 探测式收集结果

收集时间: 2026-07-31
搜索策略: 4 路 subagent 并行探测

## 探测结果总览

### Codex 配置维度全景图

| # | 配置维度 | Codex 方式 | Claude Code 对应 |
|---|---------|-----------|-----------------|
| 1 | **核心配置** | `~/.codex/config.toml`（TOML/YAML/JSON，五层作用域） | `settings.json`（JSON，三层作用域） |
| 2 | **指令/Rules** | `AGENTS.md` 分层发现（全局→仓库根→目录，32KiB上限） | `CLAUDE.md` + `rules/` 路径作用域 |
| 3 | **Skills** | `.agents/skills/*/SKILL.md`，延迟加载，Agent Skills Standard | `.claude/skills/*/SKILL.md`，扫描注册 |
| 4 | **Agents** | `.codex/agents/*.toml`（default/worker/explorer） | `.claude/agents/` 子代理 |
| 5 | **MCP** | config.toml `[mcp]` 区块，`codex mcp add` | settings.json `mcpServers` |
| 6 | **Hooks** | `hooks.json`，6+ 生命周期事件（含 PreCompact/SubagentStart） | 类似但事件较少 |
| 7 | **Workflows** | 通过 Skills + 社区框架（OMX/WorkHarness） | 内置 workflow 定义 |
| 8 | **插件** | `.codex-plugin/plugin.json`，与 ChatGPT 共享目录 | 无等效系统 |
| 9 | **权限** | `sandbox_mode` + `approval_policy` + Starlark `.rules` | `allow/deny/ask` 细粒度权限 |
| 10 | **CLI/环境** | 15+ flags，`-c key=val`，`.env` 加载，多提供商 | 类似功能不同参数 |

### 关键对比发现

1. **格式**: Codex TOML（也支持 YAML/JSON） vs Claude JSON
2. **指令兼容**: AGENTS.md 可 fallback 读取 CLAUDE.md
3. **Skills 共享**: 两者基于同一 Agent Skills Standard，可符号链接共享
4. **Hook 事件**: Codex 比 Claude 多 PreCompact/PostCompact/SubagentStart
5. **权限范式**: 粗粒度沙箱 vs 细粒度权限匹配 — 迁移需意图转换

### 高评分资料汇总

| 资料 | URL | 评分 |
|------|-----|------|
| Codex config.md 官方文档 | https://github.com/openai/codex/blob/main/docs/config.md | 5 |
| AGENTS.md 官方文档 | https://learn.chatgpt.com/docs/agent-configuration/agents-md | 5 |
| Codex Skills 官方文档 | https://developers.openai.com/codex/skills | 5 |
| Codex Best Practices | https://developers.openai.com/codex/learn/best-practices | 5 |
| Codex MCP 官方文档 | https://learn.chatgpt.com/docs/extend/mcp?surface=cli | 5 |
| Codex Hooks 官方文档 | https://developers.openai.com/codex/hooks | 5 |
| Codex 插件体系 | https://developers.openai.com/plugins/concepts/plugins | 5 |
| Codex vs Claude Code Skills | https://docs.kanaries.net/articles/codex-vs-claude-code-skills | 5 |
| Codex config.toml Deep Dive | https://dev.to/owen_fox/codex-cli-configtoml-deep-dive-every-setting-explained-5gpm | 5 |
| everything-openai-codex 指南 | https://github.com/mturac/everything-openai-codex/blob/main/the-shortform-guide.md | 5 |

## 用户选择

- **方向**: 全面覆盖 — 按 1→2→3→4→5 维度顺序深入
- **顺序**: 核心配置 → 指令/Rules → Skills & Agents → MCP & Hooks & 插件 → 权限安全
