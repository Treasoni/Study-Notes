# 意图文件：DeepSeek-Harness 配置接入指南

## 用户原始请求
- "我要只是如何做可以让 deepseek harness 可以像 claudecode 一样可以使用 skills，hooks，mcp，rules 等。我该如何？"
- "是不是只用创建一个 .dsh 的文件夹，像 .claude"

## 意图澄清
- **笔记类型**：实战配置指南（对照 Claude Code 的配置迁移/接入）
- **学习深度**：上手（会配置即可用，不深入插件源码开发）
- **用户基础**：熟悉 Claude Code（其扩展体系 hooks / CLAUDE.md / MCP / Skills 作桥）
- **核心问题**：dsh 如何接入 skills / hooks / mcp / rules 四类能力；`.dsh` 目录是不是唯一的配置入口

## 已确定的关键结论（来自官方源码/文档核对）
1. `.dsh`（默认 `~/.dsh`，可 `$DSH_HOME` 覆盖）是 harness home ≈ `~/.claude/`
2. **rules**：项目根 `AGENTS.md` **和** `CLAUDE.md` 默认都读（`instructionFileCandidates` 默认 `['AGENTS.md','CLAUDE.md']`），本地覆盖 `AGENTS.local.md`/`CLAUDE.local.md`，用户级固定 `~/.dsh/AGENTS.md`
3. **skills**：项目 `.dsh/skills/<name>/SKILL.md`（rank 100）→ 项目 `.agents/skills`（200）→ `customSkillDirs`（300）→ 用户 `~/.dsh/skills`（400）→ 用户 `~/.agents/skills`（500）；热加载
4. **hooks**：桥接插件 `@deepseek-ai/dsh-hooks-claude-code`（`configPath` 指向 hooks.json，直接复用 CC hooks）或原生 cordis 插件监听 `tools/pre-execute` 等扩展点
5. **mcp**：每个 server 一个 `@deepseek-ai/dsh-mcp-client` 插件实例（cordis.yml），工具名 `mcp__<serverName>__<tool>`

## 输出位置策略
- 系列目录：`AI学习/DeepSeek-Harness 教程/`（零散分册模式，独立单篇）
- 文件名：`DeepSeek-Harness 配置实战.md`（与系列命名一致）
- MOC：更新 `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`
- Vault：用户 Obsidian vault（`AI学习/` 即 vault 内路径）

## 模式
- 单篇独立分册 → **freeform 模式**（跳过 P3 大纲 / P4 逐章写作，直接产出单篇）
