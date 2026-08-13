# 第一章：dsh 是什么——可组装的 agent 运行时

如果你已经习惯了 Claude Code 这种开箱即用的 agent 成品，那么在动手装 dsh 之前，最值得花十分钟的是先建立正确的心智模型：dsh 不是又一个模型，也不是某个模型的小包装，而是一个「可组装的 agent 运行时」。这一章回答四个问题——它到底是什么、内部怎么组织、和 Claude Code / Codex 是什么关系、现在用它有哪些坑要避开。

## 1.1 一句话定位：dsh 不是模型，而是 agent 运行框架

官方给出的核心公式只有一行：

```
Model + Harness = Agent
```

dsh（deepseek-harness）是 DeepSeek 官方开源的 agent harness。它既不是新模型，也不是 API 客户端，而是「把模型接入文件系统、终端、网页、代码工具，并组织上下文、工具调用、任务执行」的运行框架。[1]

> **大白话**：把模型想成发动机，dsh 是给它配的车架、方向盘和刹车。发动机决定动力，但能不能上路、怎么转向由车架说了算。所以 dsh 换掉的是「驾驶体验」，不是「发动机」本身。

对 Claude Code 用户来说，最关键的差异在于：Claude Code 是绑定 Claude 模型的成品，模型与运行框架是一体的；而 dsh 把两者解耦，模型只是可插拔的一层。后面第三章你会看到，它甚至能接 Anthropic、OpenAI 以及任意 OpenAI-compatible 的第三方模型——这就是「Model + Harness」拆开后的直接后果。

## 1.2 核心架构：一切皆插件（无特权核心）

dsh 的架构由 Cordis 框架驱动，核心原则是「一切皆插件」（Everything is a Plugin）。意思是：模型适配器、工具注册表、会话日志、Agent loop、沙箱——这些在其他 agent 里通常被写死的部件，在 dsh 里全部可以替换。[1]

> **大白话**：把 dsh 想成一台没有「核心引擎」的乐高车，方向盘、座椅、轮子全是可插拔的积木块。没有哪一块是特权部件——嫌轮子不好，可以整个换掉，而不必换车。

对比 Claude Code：它是「单体核心 + 扩展」——核心功能内建，插件在核心之外做增量。dsh 则反过来，先有一个空壳（Cordis 插件树），所有能力都以插件形式装入。这种设计对使用者的实际影响是：

- **模型层可换**：默认 DeepSeek V4，但第三方 provider 与自定义 OpenAI-compatible provider 都能接入；
- **工具层可扩展**：插件生态约有 300 个包，通过 `dsh plugin --profile <name> add <package>` 管理；
- **行为层可改**：连 Agent loop（任务循环）本身都是可替换插件。

## 1.3 与 Claude Code / Codex 生态的关系

dsh 官方对标的就是 Claude Code 与 OpenAI Codex，但中文报道对它的定位是「不只是 DeepSeek 版 Claude Code」，更接近可组装的 agent 运行时。[1]

两者关系用一句话概括：Claude Code 是**开箱即用的闭源成品**，dsh 是**开源（MIT）可组装的运行时**。dsh 目前约 26.5k stars，v0.1 以 MIT 协议开源。[1]

> **大白话**：Claude Code 像一台「提车就能开」的整车；dsh 像一套「零件都送你、但需要自己拼」的组装套件。前者省心，后者灵活，不存在谁完全替代谁。

注意，这不是说 dsh 要和 Claude Code 正面比拼成熟度——官方目标是提供一个可替换的 agent 运行时，让模型、工具、循环都能按需换装。所以它是「另一种选择」，而不是「更成熟的竞品」。

## 1.4 开发状态与避坑

dsh 目前处于 developer preview（v0.1，2026-08-13 发布），README 里明确写着 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES."——破坏性变更是预期内的，迭代很快，接口可能随时不兼容。升级前务必留意变更。[1]

反馈渠道也和一般开源项目不同：官方**不开 GitHub Issues**，bug 与建议一律走 GitHub Discussions；社区另有 Discord 与微信群。[1]

最后是包名避坑。市面上存在与官方同名的第三方包，最容易踩的两个：

- `pip install deepseek-harness`——非官方，官方 Python SDK 是 `deepseek-harness-sdk`；
- `npx @deepseek-harness/mcp`——非官方。

官方包名只有两个：npm 上的 `@deepseek-ai/dsh` 与 Python 上的 `deepseek-harness-sdk`。安装时认准这两个名字。[1]

> **大白话**：把官方包名想成「官方工牌」，第三方同名包想成「门口有人戴着一样的假工牌」。认准 `@deepseek-ai/dsh` 这张牌，别被看着像的名字带走。

---

## 本章小结

- dsh 的定位是 **Model + Harness = Agent**：它不是模型或 API 客户端，而是可组装的 agent 运行框架；
- 架构核心是**「一切皆插件」**：由 Cordis 驱动，模型适配器、工具注册表、会话日志、Agent loop、沙箱均可替换，无特权核心；
- 与 Claude Code / Codex 的关系：官方对标对象，但定位是**开源可组装的运行时**（MIT，约 26.5k stars），而非成熟度竞品；
- 开发状态：**developer preview**，明确会有破坏性变更；官方不开 Issues，反馈走 GitHub Discussions；
- 避坑：认准官方包名 `@deepseek-ai/dsh` 与 `deepseek-harness-sdk`，`pip install deepseek-harness` 与 `npx @deepseek-harness/mcp` 均非官方。

下一章我们直接动手：安装三路径、Web UI 首次配置，5 分钟跑通第一个会话。

---

[1]: 素材来源：`workspace/deepseek-harness/02_deep_research.md` 第一部分（产品定位）。
