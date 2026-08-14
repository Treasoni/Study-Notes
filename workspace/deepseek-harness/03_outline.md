# 学习笔记大纲：《DeepSeek-Harness 配置使用教程》

> 笔记类型：实战配置教程（快速上手 + 从 Claude Code 对照迁移）
> 预计总篇幅：约 11,000 字
> 章节数：5 章（每章对应一篇分册笔记）
> 输出目标：Obsidian vault `AI学习/DeepSeek-Harness 教程/`（含 MOC）

---

### 第一章：dsh 是什么 —— 可组装的 agent 运行时

- **篇幅**：约 1,800 字
- **覆盖要点**：一句话定位（Model + Harness = Agent）、核心架构「一切皆插件」（Cordis 框架、无特权核心）、与 Claude Code / OpenAI Codex 生态的关系、开发状态与反馈渠道、同名第三方包避坑
- **素材引用**：`02_deep_research.md` 第一部分（产品定位）
- **代码示例**：无（仅包名与核心公式引用：`@deepseek-ai/dsh`、`deepseek-harness-sdk`）
- **章节结构**：
  - 1.1 一句话定位：dsh 不是模型、不是 API 客户端，而是 agent 运行框架
  - 1.2 核心架构：一切皆插件（模型适配器、工具注册表、会话日志、Agent loop、沙箱均可替换）
  - 1.3 与 Claude Code / Codex 生态的关系：开源 MIT 可组装 vs 闭源成品；26.5k stars
  - 1.4 开发状态与避坑：破坏性变更警告、官方不开 Issues（走 Discussions）、Discord/微信群、同名第三方包（`pip install deepseek-harness`、`npx @deepseek-harness/mcp` 均非官方）

---

### 第二章：安装与快速上手 —— 5 分钟跑通第一个会话

- **篇幅**：约 2,200 字
- **覆盖要点**：系统要求、安装三路径（npm / 源码构建 / Python SDK）、Web UI 首次配置（填 Key、Choose workspace）、跑通第一个会话、headless 一次性任务（CI 验证）、常见安装/上手坑
- **素材引用**：`02_deep_research.md` 第二部分（安装与快速上手）
- **代码示例**：有
  - `npx @deepseek-ai/dsh web`
  - 源码构建四步：`git clone` → `pnpm install` → `pnpm run build` → `pnpm dsh web`
  - `pip install deepseek-harness-sdk`
  - headless：`dsh --profile headless "run the tests"`
  - 端口占用：`dsh web --port <空闲端口>`
- **章节结构**：
  - 2.1 系统要求与安装三路径（Node `^22.19 || >=24` / pnpm / Python 3.10+；官方未发布预构建二进制）
  - 2.2 Web UI 首次配置：启动 → Settings→Models 填 API Key（write-only，存于 `$DSH_HOME/.credentials.yaml`）→ Choose workspace
  - 2.3 跑通第一个会话：示例任务与权限确认（默认 `workspace-write` 预设）
  - 2.4 headless 一次性任务：退出码 0/1、适合 CI、无 resume 机制
  - 2.5 常见安装/上手坑：端口占用、ERESOLVE peer 冲突（`--legacy-peer-deps`）、Windows `ctx.bash` 重复注册

---

### 第三章：配置体系 —— 从 settings.json 到 YAML 补丁树

- **篇幅**：约 3,000 字（全书最长，配置核心）
- **覆盖要点**：YAML 补丁树机制（多层叠加、后层整行替换不做深合并）、Profile 与 Agent Preset 两级配置、权限与安全模型、模型/Provider/API 配置、环境变量速查、默认装载与边界、CLI 完整参考
- **素材引用**：`02_deep_research.md` 第三部分（配置体系）+ 第四部分（CLI 完整参考）
- **代码示例**：有
  - 合成配置检查：`dsh --profile web --dump-default-config` / `dsh --profile web --patch ./extra.yml --dump-config`
  - 自定义 OpenAI-compatible provider（`$DSH_HOME/settings.yaml` 的 `llm-pi-ai.providers` YAML 片段）
  - 环境变量引用：`apiKeyEnv: DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`
  - CLI 命令表与 launcher 规则（`dsh web` / `dsh --profile headless` / `dsh plugin --profile <name> add ...`）
- **章节结构**：
  - 3.1 配置机制：多层 YAML 补丁树（bundle → profile `cordis.patch.yml` → home 补丁 → `--patch` 覆盖层）；「Later layers win per row」语义；`--dump-config` 排查
  - 3.2 两级配置：Profile（进程级，决定 bundle）与 Agent Preset（会话级，内置 `minimal`/`standard`/`code`/`cordis` 四预设；作用域 `agent → preset → global`）
  - 3.3 权限与安全：默认 `workspace-write`、`DSH_PERMISSION_MODE`、sandbox 隔离、env 清洗（`*KEY*/*SECRET*/*TOKEN*/*PASSWORD*`）、「模型可见即已记录」
  - 3.4 模型 / Provider / API：默认 V4-Flash/Pro（1M 上下文、maxTokens 256,000、thinking/reasoningEffort/retryPolicy）、凭据解析顺序、第三方 provider（~40 家）与自定义 OpenAI-compatible provider、常见错误（`MISSING_CREDENTIAL` / `UNKNOWN_MODEL` / 401）
  - 3.5 环境变量速查：`DSH_HOME`、`DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`、`DSH_PERMISSION_MODE`、`DSH_TOOLS_MODE`、`DSH_TELEMETRY_*`、`NODE_USE_ENV_PROXY`
  - 3.6 默认装载与边界：`web_fetch` 默认禁用、MCP 默认不启用任何 server、内存 SQLite 索引、`AGENTS.md`/`CLAUDE.md` 加载与 65,536 字节预算
  - 3.7 CLI 完整参考：launcher 规则（标志须在 app 参数前、`--` 处理）+ 命令表

---

### 第四章：与 Claude Code 对照迁移 —— 换还是留？

- **篇幅**：约 2,600 字
- **覆盖要点**：概念对照表、成本对比（90% 缓存命中场景、28 倍输出价差、规模化月成本）、性能对比（SWE-bench 等四基准）、三选迁移策略、选择建议
- **素材引用**：`02_deep_research.md` 第五部分（与 Claude Code 对照/迁移）+ 综合分析
- **代码示例**：有
  - DeepClaude 模式环境变量：`export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"`、`export ANTHROPIC_API_KEY="your-deepseek-api-key"`
  - 对照示例：`claude -p "..."` vs `dsh --profile headless "..."`
- **章节结构**：
  - 4.1 概念对照表：定位/架构/一次性任务/配置文件/权限/工作区根/上下文文件/模型/MCP/成熟度
  - 4.2 成本对比：V4 Flash/Pro vs Claude Opus/Sonnet；每任务成本与每 $100 任务数；规模化对比（5,000 任务/天，$79,000 vs $3,150）
  - 4.3 性能对比：SWE-bench Pro / Verified、LiveCodeBench、Terminal-Bench、MCPAtlas；结论「harness 与工具 schema 设计比模型选择更重要」
  - 4.4 三选迁移策略：整体换 harness / DeepClaude 模式（保留 Claude Code 换底模，结构性便宜 10–25 倍）/ 按复杂度路由（Flash → 琐碎改动、Pro → 标准功能、Opus → 多文件架构重构）
  - 4.5 选择建议：什么场景留在 Claude Code（仓库级重构、高风险任务、Anthropic 专属功能）、什么场景换 dsh（高频低成本循环、并行子代理、自托管/数据主权、GUI）
  - 4.6 迁移前置提醒：DeepSeek V4 协议差异详见第五章 5.3（thinking 默认开启、reasoning_content 回传等）

---

### 第五章：常见坑与速查

- **篇幅**：约 1,800 字
- **覆盖要点**：坑清单（安装/配置/运行）、命令速查（高频命令 + launcher 规则）、DeepSeek V4 协议坑、生态资源与下一步
- **素材引用**：`02_deep_research.md` 第二部分（常见坑）+ 第四部分（CLI）+ 第五部分（V4 协议坑）+ 综合分析
- **代码示例**：有
  - 端口重设：`dsh web --port <空闲端口>`
  - npm peer 冲突：`--legacy-peer-deps`
  - 配置检查：`dsh --profile web --dump-config`
  - 插件管理：`dsh plugin --profile <name> add <package>`
- **章节结构**：
  - 5.1 坑清单：端口占用、ERESOLVE、Windows 多插件重复注册、`MISSING_CREDENTIAL`/`UNKNOWN_MODEL`/401、第三方同名包、破坏性变更升级策略
  - 5.2 命令速查表：web / headless / plugin / dump-config / help / version + launcher 规则（标志前置、`--` 处理、热重载、关闭行为）
  - 5.3 DeepSeek V4 协议坑：thinking 默认烧 token、多轮必须回传 `reasoning_content`（否则 HTTP 400）、必须设 `max_tokens`、thinking 下 `tool_choice` 只能 `auto`
  - 5.4 生态资源与下一步：GitHub Discussions（官方唯一反馈渠道）、Discord/微信群、插件生态约 300 个、官方包名清单

---

## 学习路径说明

### 前置要求

- 非常熟悉 Claude Code 基本操作（CLI 会话、`settings.json` / `CLAUDE.md`、权限确认流程）——本书以此为基础做对照，不再铺垫通用概念
- 会读基础 YAML（能看懂缩进与键值结构即可）
- 安装环境二选一：Node.js（`^22.19 || >=24`）走 npm/npx；或 Python 3.10+（Linux/macOS）走 SDK
- 有一个 DeepSeek API Key（用于跑通第一个会话与后续配置示例）

### 学完能做什么

- 5 分钟内用 `npx @deepseek-ai/dsh web` 跑通 Web UI 并完成第一个真实任务
- 用 `dsh --profile headless "任务"` 在 CI 中跑一次性自动化任务（并理解退出码语义）
- 理解并动手改 dsh 的 YAML 补丁树配置，配置第三方或自定义 OpenAI-compatible provider
- 用成本/性能对照表判断哪些任务适合迁移到 DeepSeek/dsh、哪些留在 Claude Code
- 用 DeepClaude 模式（Anthropic 兼容端点）保留 Claude Code 界面、换 DeepSeek 底模省钱
- 规避 V4 协议与安装环节的高频坑，知道遇到问题去哪里反馈

### 建议学习顺序

- **主路径（推荐）**：第 1 → 2 → 3 → 4 → 5 章顺序阅读。第 1 章建立心智模型，第 2 章动手跑通，第 3 章深入配置（全书核心，篇幅最长），第 4 章做迁移决策，第 5 章作为日常速查随时翻阅。每章阅读 + 实操约 30-40 分钟。
- **急用路径**：先读第 2 章跑通环境，再读第 4 章做「换还是留」决策，之后回头补第 3、5 章。若暂不迁移，第 4 章可跳读成本与性能表格。
- **注意**：第 3 章是全书的配置核心，后续章节的迁移对比会大量引用其概念（补丁树、Profile、Agent Preset），不建议跳过。

---

## 素材覆盖核对

- [x] 产品定位（第一部分）→ 第 1 章
- [x] 安装与快速上手（第二部分）→ 第 2 章
- [x] 配置体系（第三部分）→ 第 3 章
- [x] CLI 完整参考（第四部分）→ 第 3 章 3.7 + 第 5 章 5.2
- [x] 与 Claude Code 对照/迁移（第五部分）→ 第 4 章 + 第 5 章 5.3
- [x] 综合分析 → 第 4 章 + 第 5 章 5.4
