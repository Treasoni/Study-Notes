---
title: 快速参考卡片
tags: [codex, ai, 工具使用, 高级功能, 速查]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# 快速参考卡片

> [!info] 文档定位
> **一句话定位** - 本篇是 Codex 配置体系的速查卡片，浓缩三张核心参考表：**配置文件路径速查**、**常用 CLI 命令速记**、**关键配置项默认值一览**。适合已读完配置详解、需要随手检索路径、命令与默认值的用户快速查阅。

---

## 配置文件路径速查

下表汇总 Codex 与 Claude Code 各类配置文件的存放位置，便于迁移时逐项对应。

| 配置类型 | Codex 路径 | Claude Code 路径 |
|---------|-----------|-----------------|
| 用户全局配置 | `~/.codex/config.toml` | `~/.claude/settings.json` |
| 项目配置 | `<repo>/.codex/config.toml` | `<repo>/.claude/settings.json` |
| 用户全局指令 | `~/.codex/AGENTS.md` | — |
| 项目指令 | `<repo>/AGENTS.md`（分层级联） | `<repo>/CLAUDE.md`（单文件） |
| 规则文件 | `.codex/rules/*.rules`（Starlark） | `.claude/rules/*.md` |
| Skills 目录 | `.agents/skills/` | `.claude/skills/` |
| 用户 Skills | `~/.agents/skills/` | `~/.claude/skills/` |
| Agent 定义 | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Hooks 配置 | `.codex/hooks.json` 或 config.toml 内联 | settings.json 内联 |
| 插件目录 | `.codex/plugins/` | — |
| 环境变量文件 | `<project>/.env` | — |

---

## 常用 CLI 命令速记

覆盖启动、单次执行、配置覆盖、MCP 管理与会话内斜杠命令，随查随用。

| 命令 | 用途 | 示例 |
|------|------|------|
| `codex` | 启动交互式 REPL | `codex` |
| `codex exec` | 单次执行 | `codex exec "解释这个项目"` |
| `codex status` | 查看工作区状态 | `codex status` |
| `codex --cd DIR` | 指定工作目录启动 | `codex --cd /path/to/proj` |
| `codex --profile NAME` | 使用特定配置档 | `codex --profile fast` |
| `codex -c key=val` | 临时覆盖配置项 | `codex -c model=gpt-5.4-mini` |
| `codex mcp add` | 交互式添加 MCP 服务器 | `codex mcp add` |
| `/skills` | 列出可用技能 | `/skills` |
| `/hooks` | 管理钩子 | `/hooks trust 1` |
| `/config` | 查看/修改配置 | `/config get sandbox_mode` |
| `/feedback` | 提交反馈 | `/feedback` |

---

## 关键配置项默认值一览

下列均为开箱即用默认值；改动前请先评估对安全与性能的影响。

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `sandbox_mode` | `workspace-write` | 沙箱模式 |
| `approval_policy` | `on-request` | 审批策略 |
| `shell_environment_policy.inherit` | `all` | 环境变量继承策略 |
| `project_doc_max_bytes` | 32768（32 KiB） | 指令容量上限 |
| `[agents].max_threads` | 2 | 最大并行子代理数 |
| `[agents].max_depth` | 2 | 子代理最大嵌套深度 |
| `[features].hooks` | `true` | 钩子系统开关 |
| `[features].multi_agent` | `true` | 多代理开关 |
| `[features].shell_snapshot` | `true` | 快照加速开关 |
| MCP `startup_timeout_sec` | 10 | MCP 服务器启动超时 |
| MCP `tool_timeout_sec` | 60 | MCP 工具调用超时 |
| MCP `approval_mode` | `auto` | MCP 审批模式 |
| MCP `required` | `false` | MCP 服务器必要性 |

---

## 常见问题

### Q: Codex 与 Claude Code 的配置文件路径如何对应？

**回答**：全局用户配置对应 `~/.codex/config.toml` 与 `~/.claude/settings.json`，项目配置对应 `<repo>/.codex/config.toml` 与 `<repo>/.claude/settings.json`。指令与规则层面差异较大：Codex 用 `<repo>/AGENTS.md`（分层级联）+ `.codex/rules/*.rules`（Starlark），Claude Code 用 `<repo>/CLAUDE.md`（单文件）+ `.claude/rules/*.md`；Codex 还独有插件目录 `.codex/plugins/` 与 `<project>/.env` 环境变量文件。

### Q: 如何临时覆盖某个配置项，而不修改配置文件？

**回答**：用 `codex -c key=val` 在启动时临时覆盖配置项，例如 `codex -c model=gpt-5.4-mini`；或使用 `codex --profile NAME` 切换到特定配置档（如 `--profile fast`）。这类覆盖不会写入 `config.toml`，适合"先验证、再固化到配置文件"的工作流。

### Q: 有哪些默认值需要特别留意？

**回答**：安全相关默认值——`sandbox_mode` 默认为 `workspace-write`、`approval_policy` 默认为 `on-request`；性能相关默认值——`[agents].max_threads` 与 `[agents].max_depth` 均为 2；容量限制——`project_doc_max_bytes` 默认 32 KiB。MCP 服务器默认 `startup_timeout_sec` 10 秒、`tool_timeout_sec` 60 秒、`approval_mode` 为 `auto`。

---

## 最佳实践

### Do's

- 用 `codex --profile NAME` 为不同场景（如 `fast`）维护独立配置档，快速切换。
- 用 `codex -c key=val` 临时覆盖配置项，先验证生效再写回 `config.toml`。
- 用 `codex --cd DIR` 明确指定工作目录，避免误在错误目录启动。
- 用 `codex mcp add` 交互式添加 MCP 服务器，降低手写配置的门槛。
- 用 `/config get <key>`、`/hooks`、`/skills` 随时查看当前生效的配置与能力。

### Don'ts

- 不要混淆 Codex 与 Claude Code 的配置路径（`~/.codex/config.toml` vs `~/.claude/settings.json`）。
- 不要轻易放宽安全默认值：`sandbox_mode`（`workspace-write`）与 `approval_policy`（`on-request`）。
- 不要忽略 `[agents].max_threads` / `[agents].max_depth`（默认均 2），高并发任务需先调大。
- 不要让 `project_doc_max_bytes`（默认 32 KiB）承载过大的指令文档，超出容量上限的指令需拆分处理。

---

## 小结

快速参考卡片浓缩了 Codex 配置体系的三个入口：配置文件路径速查表帮助与 Claude Code 逐项对照，常用 CLI 命令速记表覆盖启动、单次执行与配置覆盖，关键配置项默认值一览表标出安全与性能基线。日常配置时可随手翻阅，改动前先核对默认值，避免误放权限或遗漏子代理并发上限。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Codex CLI 与调试]] | CLI 命令详解与调试方法 |
| [[config.toml 核心配置]] | 配置项详细解读 |
| [[对照表与迁移实战]] | 完整对照表与迁移策略 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
