---
title: "Codex 配置体系 MOC"
tags: [moc, codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
---

# Codex 配置体系 MOC

> 从 Claude Code 出发，系统掌握 Codex 的完整配置体系。8 章 + 附录，约 3-4 小时。

## 目录

### 概览

- [[01 配置哲学概览]] — TOML vs JSON、目录结构、五层优先级
- [[02 config.toml 核心配置]] — sandbox、approval、permissions、profiles

### 行为控制

- [[03 AGENTS.md 分层体系]] — 层级级联、CLAUDE.md fallback、Starlark 规则
- [[04 Skills 技能系统]] — 创建、注册、渐进加载、跨工具共享

### 扩展机制

- [[05 Agents 与 MCP]] — 子代理定义、MCP STDIO/HTTP、审批模式
- [[06 Hooks 与插件]] — 11 种生命周期事件、插件体系

### 实战

- [[07 CLI 与调试]] — 核心命令、环境变量、故障排查
- [[08 对照表与迁移实战]] — 21 维对照、四步迁移、陷阱与最佳实践

### 参考

- [[附录 快速参考卡片]] — 路径速查、命令速记、默认值
