# 第一章：dsh 是什么——可组装的 agent 运行时

对熟悉 Claude Code 的用户，装 dsh 前最该先建立心智模型：dsh 不是又一个模型，而是「可组装的 agent 运行时」——它与 Claude Code 是两种不同的东西。

## 1.1 一句话定位：dsh 不是模型，而是 agent 运行框架

官方核心公式：`Model + Harness = Agent`。dsh 是 DeepSeek 官方开源的 agent harness——不是模型或 API 客户端，而是「把模型接入文件系统、终端、网页、代码工具，组织上下文、工具调用与任务执行」的运行框架[1]。

> **大白话**：模型像发动机，dsh 是车架、方向盘和刹车。发动机决定动力，能不能上路由车架说了算——dsh 换的是「驾驶体验」，不是「发动机」。

与 Claude Code 的本质差异：Claude Code 绑定 Claude 模型、框架与模型一体；dsh 把两者解耦，模型只是可插拔的一层，可接第三方与 OpenAI-compatible 模型。

## 1.2 核心架构：一切皆插件（无特权核心）

dsh 由 Cordis 框架驱动，核心原则是「一切皆插件」：模型适配器、工具注册表、会话日志、Agent loop、沙箱均可替换，无特权核心[1]。对比 Claude Code 的「单体核心 + 扩展」，dsh 是「空壳 + 插件树」——插件约 300 个，用 `dsh plugin --profile <name> add <package>` 管理。

> **大白话**：dsh 像没有「核心引擎」的乐高车，方向盘、轮子全是可插拔积木块。嫌轮子不好就整个换掉，不必换车。

## 1.3 与 Claude Code / Codex 生态的关系

dsh 官方对标 Claude Code 与 OpenAI Codex，中文报道称它「不只是 DeepSeek 版 Claude Code」，更接近可组装的 agent 运行时[1]。Claude Code 是开箱即用的闭源成品，dsh 是开源（MIT）可组装的运行时（约 26.5k stars）——是「另一种选择」，而非成熟度竞品[1]。

## 1.4 开发状态与避坑

dsh 处于 developer preview（v0.1，2026-08-13 发布），README 明确 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES."，接口可能随时不兼容[1]。反馈：官方不开 GitHub Issues，bug 与建议走 GitHub Discussions；另有 Discord 与微信群[1]。

避坑——同名第三方包：`pip install deepseek-harness` 与 `npx @deepseek-harness/mcp` 均非官方。官方包名只有 `@deepseek-ai/dsh`（npm）与 `deepseek-harness-sdk`（Python）[1]。

> **大白话**：官方包名像「官方工牌」，同名包像戴假工牌的人。认准 `@deepseek-ai/dsh`，别被看着像的名字带走。

---

## 本章小结

- 定位：**Model + Harness = Agent**——agent 运行框架，不是模型或 API 客户端；
- 架构：「一切皆插件」、无特权核心，由 Cordis 驱动；模型、工具、Agent loop 均可替换；
- 生态：开源 MIT、约 26.5k stars，与 Claude Code / Codex 是「另一种选择」而非竞品；
- 状态：developer preview，有破坏性变更，反馈走 GitHub Discussions；认准官方包名 `@deepseek-ai/dsh` 与 `deepseek-harness-sdk`。

下一章直接动手：安装三路径、Web UI 首次配置，5 分钟跑通第一个会话。

---

[1]: 素材来源：`workspace/deepseek-harness/02_deep_research.md` 第一部分（产品定位）。
