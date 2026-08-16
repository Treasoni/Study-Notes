---
title: "从零搭建 DeepSeek-Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战"
tags: [deepseek-harness, ai, agent, 脚手架, 实战, claude-code]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
---

# 从零搭建 DeepSeek-Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战

> 这是一份从零搭建 DeepSeek-Harness（dsh）工程脚手架的实战笔记，以「使用 dsh」为主线：从先建哪些文件出发，依次拆解 rules/指令体系（AGENTS.md、CLAUDE.md 与 workspaceContext）、skills 放置与结构、hooks 桥接与原生插件、subagents 挂载、补丁树/Profile/Agent Preset/MCP 配置体系与常见坑清单，最后汇总最小可运行骨架。全程保留 dsh ↔ Claude Code 对照视角，帮助从 Claude Code 迁移过来的你快速上手。

## 目录

1. [[01-心智模型|第一章 心智模型——dsh 工程和 Claude Code 工程差在哪]]
2. [[02-先创建哪些文件|第二章 开始一个项目——先创建哪些文件]]
3. [[03-Rules指令体系|第三章 Rules/指令体系——AGENTS.md、CLAUDE.md 与 workspaceContext]]
4. [[04-Skills放置与结构|第四章 Skills——往哪放、怎么写、扫描优先级]]
5. [[05-Hooks桥接与原生|第五章 Hooks——桥接复用 vs 原生插件]]
6. [[06-Subagents|第六章 Subagents——ctx.subagents 与 SubagentProvider]]
7. [[07-配置体系与坑清单|第七章 配置体系与常见坑清单]]
8. [[08-最小骨架与发布|第八章 最小可运行骨架总览 + 发布]]

> [!tip] 阅读顺序建议
> 每章都有「这在 Claude Code 里相当于」的对照框与本章小结。如果你是 Claude Code 迁移过来的，第一遍可先扫每章的对照框 + 小结，卡住再回正文；第 1 章的对照速查表是全笔记的地图。

## 常见坑清单速查（第 7 章汇总）

| 坑名 | 一句话规避 |
|---|---|
| patch `name` 相对路径静默失效 | 写绝对路径 |
| hooks 桥接只跑 shell command | `http`/`mcp_tool`/`prompt`/`agent` 被跳过 |
| `configPath` 进程级 | 启动 cwd 解析，写绝对路径或在该目录启动 |
| 补丁按行替换不深合并 | 同 id 整行覆盖，拿不准 `--dump-config` |
| skills 目录名 kebab-case、不支持嵌套 | `My Skill/` 不被发现 |
| MCP 只桥接 Tools | Resources/Prompts 不出现 |
| subagent UNSUPPORTED_CAPABILITY | 选错 provider，不是重试能解决 |

> 完整 11 条见 [[07-配置体系与坑清单|第七章 7.4 坑清单]]。

## 素材来源

- **B1-B3**：DeepSeek-Harness 官方仓库 `AGENTS.md`、`docs/config-catalog.md`、`docs/subsystems/skills.md`（2026-08-16 抓取）。
- **D1-D5**：你的 vault 笔记《03-配置实战-接入skills-hooks-mcp-rules》《02-配置体系-补丁树Profile与bundle》《12-实战-写自己的AgentPreset》《DeepSeek-Harness Subagent 教程》《DeepSeek-Harness 是什么 / 安装与快速上手 / 05-实战-起步-最小骨架与脚手架》（2026-08-16）。
- 发布规范来自项目 `.claude/rules/obsidian/note-system.md`。

---

> [!info] 导航
> 上一级：[[AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC|DeepSeek-Harness MOC]] · 第一站：[[01-心智模型|第一章 心智模型 →]]
