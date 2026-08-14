---
title: "DeepSeek-Harness 插件开发：心智模型"
tags: [deepseek-harness, ai, agent, 插件, 教程, 心智模型]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 插件开发：心智模型——插件树 vs 单体 + 扩展

> [!summary] 本章导读
> 你想写自己的 dsh 插件，又熟悉 Claude Code。开始写之前最该先做的不是装环境，而是把心智模型转过来：**Claude Code 是「单体核心 + 扩展」，dsh 是「空壳 + 插件树」**。这一章用你已会的 Claude Code 概念作桥，讲清 dsh 插件体系，让你理解「为什么我写的插件能像官方插件一样有地位」。

## 1.1 一句话定位：dsh 不是模型，而是可组装的 agent 运行时

官方核心公式：`Model + Harness = Agent`。dsh 是 DeepSeek 官方开源的 agent harness——不是模型或 API 客户端，而是「把模型接入文件系统、终端、网页、代码工具，组织上下文、工具调用与任务执行」的运行框架[^1]。

> [!tip] 大白话
> 模型像发动机，dsh 是车架、方向盘和刹车。发动机决定动力，能不能上路由车架说了算——写插件改的是「驾驶体验」，不是「发动机」。

与 Claude Code 的本质差异：Claude Code 绑定 Claude 模型，框架与模型一体；dsh 把两者解耦，模型只是可插拔的一层，可接第三方与 OpenAI-compatible 模型。

## 1.2 核心架构：一切皆插件（无特权核心）

dsh 由 Cordis 框架驱动，核心原则是「一切皆插件」：模型适配器、工具注册表、会话日志、Agent loop、沙箱均可替换，无特权核心[^1]。对比 Claude Code 的「单体核心 + 扩展」，dsh 是「空壳 + 插件树」——插件约 300 个，用 `dsh plugin --profile <name> add <package>` 管理。

> [!tip] 大白话
> dsh 像没有「核心引擎」的乐高车，方向盘、轮子全是可插拔积木块。嫌轮子不好就整个换掉，不必换车——**你想写的插件，和官方插件是同一种积木**。

## 1.3 桥接：Claude Code 的「扩展」在 dsh 里是什么

你在 Claude Code 里已经用过的扩展能力，在 dsh 里各有对应。记住这张表，后面每章都会引用它[^2]：

| 你在 Claude Code 里的概念 | dsh 里对应的插件机制 |
|---|---|
| hooks（`session-start` / `pre-step` / `pre-tool-use` …） | 监听 `agent/session-start` / `agent/pre-step` / `tools/pre-execute` / `tools/post-execute` 等扩展点（官方 `dsh-hooks-claude-code` 直接把 hook 配置文件映射到这些点） |
| CLAUDE.md 里的自定义指令 | `ctx.systemPrompt.section()` 往系统提示词加段落 |
| MCP server（新增工具） | 每个 server 一个插件：发现工具 → `ctx.tools.register()` |
| Skills / 自定义命令 | section + 工具注册，调用时注入内容 |
| Subagent 类型 | `ctx.subagents` 提供方注册表（`dsh-subagent-*` 系列） |
| settings.json / .mcp.json 声明式配置 | `cordis.patch.yml` / bundle 的可编程组合 |
| 自定义工具 | `ctx.tools.register(defineTool({...}))` |

> [!note] 核心差异：扩展的「地位」
> 在 Claude Code 里，你的扩展永远依附于一个不开源的单体核心；在 dsh 里**没有特权核心**——你写的插件和 `dsh-tool-bash`、`web_search` 这些官方插件在架构上完全对等。这既是自由，也意味着你要自己理解插件生态的规则。

## 1.4 为什么要先转心智模型

写 dsh 插件常见的第一类挫败，是拿 Claude Code 的「改配置声明文件」思路去套 dsh：

- Claude Code：改 `settings.json` / `CLAUDE.md` 是「改配置」；
- dsh：**写插件 = 写代码 + 用 `cordis.yml` patch 把它装进插件树**。配置声明（YAML）只是「装载」的手段，能力本身是 TypeScript 代码。

想写自己的插件，正确路径是：理解插件形态（函数/对象/类）→ 注册机制（patch）→ 生命周期（effect）→ 依赖（inject）→ 能力注册（`ctx.tools.register` 等）。这正是后续章节的顺序。

## 1.5 开发状态与避坑

dsh 处于 developer preview（v0.1，2026-08-13 发布），README 明确 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES."，接口可能随时不兼容[^1]。反馈：官方不开 GitHub Issues，bug 与建议走 GitHub Discussions；另有 Discord 与微信群[^1]。

> [!warning] 同名第三方包避坑
> `pip install deepseek-harness` 与 `npx @deepseek-harness/mcp` 均**非官方**。官方包名只有 `@deepseek-ai/dsh`（npm）与 `deepseek-harness-sdk`（Python）。认准官方包名，别被看着像的名字带走。

---

## 本章小结

> [!summary]
> - 定位：**Model + Harness = Agent**——agent 运行框架，不是模型或 API 客户端；
> - 架构：「一切皆插件」、无特权核心，由 Cordis 驱动；**你写的插件与官方插件架构对等**；
> - 桥接：Claude Code 的 hooks / CLAUDE.md / MCP / Skills 在 dsh 里分别对应扩展点监听、systemPrompt section、tools.register、section+工具；
> - 状态：developer preview，有破坏性变更，反馈走 GitHub Discussions；认准官方包名 `@deepseek-ai/dsh` 与 `deepseek-harness-sdk`。

下一章动手搭环境：[[DeepSeek-Harness 安装与快速上手]]——为什么写插件必须走源码运行路径，5 分钟把开发环境跑起来。

---

## 更新记录

- 2026-08-15：全套重构为「写自己的 dsh 插件」主线；新增 1.3 Claude Code 扩展模型对照表（hooks/CLAUDE.md/MCP/Skills → dsh 插件机制）、1.4 心智模型转换；删除「换还是留」视角。

---

[^1]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-13 收集）。
[^2]: 素材来源：官方「扩展插件形态 Cookbook」（2026-08-15 收集）。
