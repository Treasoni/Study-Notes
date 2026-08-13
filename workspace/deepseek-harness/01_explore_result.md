# DeepSeek-Harness 配置使用教程 - 探测结果

收集时间: 2026-08-13
搜索关键词: deepseek-harness 产品定位 / 安装与快速上手 / 配置·CLI·生态·对比迁移
收集方式: 3 个并行 subagent 粗筛（官方仓库 README、官方 docs、技术博客、新闻报道、社区讨论）

---

## 一、产品概览

- **deepseek-harness（dsh）**：DeepSeek 官方开源的 agent harness，2026-08-13 发布 v0.1 开发者预览，MIT 协议，仓库约 26.5k stars。
- 核心公式：**Model + Harness = Agent**。它不是新模型、不是 API 客户端，而是「模型 → 文件系统/终端/网页/工具/任务执行」的运行框架。
- 核心理念：**「一切皆插件」**（Everything is a Plugin），基于 Cordis 框架，无特权核心——模型适配器、工具、会话日志、Agent loop、沙箱均可替换。
- 官方对标：Claude Code 与 OpenAI Codex；中文报道称其「不只是 DeepSeek 版 Claude Code」，更接近可组装的 agent 运行时。

## 二、安装与快速上手

| 安装方式 | 命令/要求 | 备注 |
|---|---|---|
| npm（推荐） | `npx @deepseek-ai/dsh web` | 前置仅 Node.js；启动 Web UI，默认 `http://127.0.0.1:3080` |
| 源码构建 | `git clone` + `pnpm install` + `pnpm run build` + `pnpm dsh web` | 要求 Node `^22.19 \|\| >=24` |
| Python SDK | `pip install deepseek-harness-sdk` | Python 3.10+，Linux x64/arm64 或 macOS 14+ arm64，运行时无需系统 Node.js |

**首次配置（Web UI）**：
1. 启动后访问 `http://127.0.0.1:3080`
2. **Settings → Models** 填 DeepSeek API Key（存于 `$DSH_HOME/.credentials.yaml`，保存即生效，无需重启）；或设环境变量 `DEEPSEEK_API_KEY`
3. 点 **Choose workspace** 选择项目目录（不选工作区无法开始会话）
4. 新建会话发送首个任务，如 "Summarize this repository and identify its main packages."

**CLI 快速验证**：`dsh --profile headless "任务描述"` — 跑一次性持久会话并打印最终答案，最适合测试 Key 与连通性。

## 三、配置体系（重点：不是 config.toml）

- 配置是 **YAML 补丁树**（非 config.toml）：空根 → bundle 补丁（`dsh.profile.bundles` 清单）→ profile 的 `cordis.patch.yml` → 家目录 `$DSH_HOME/cordis.patch.yml` → `--patch` 覆盖层。**后层整行替换，不做深合并。**
- **两级配置**：Profile（进程级，决定装哪些 bundle）+ Agent Preset（会话级：工具/提示词/skill/子代理）；作用域解析 `agent → preset → global`。
- 内置 **4 个预设**：minimal / standard / code / cordis；默认新会话 `workspace-write` 权限预设。
- 模型：默认 DeepSeek **V4-Flash / V4-Pro**（1M 上下文，maxTokens 默认 256k）；支持约 40 家目录内第三方 + 自定义 OpenAI-compatible provider。
- 环境变量：`DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`、`$DSH_HOME`。
- 常见错误码：`MISSING_CREDENTIAL`（未配 key）、`UNKNOWN_MODEL`（模型未配置）、模型发现 401。

## 四、CLI 与日常使用

| 命令 | 用途 |
|---|---|
| `dsh web` | 启动 Web UI（= `--profile web`），默认端口 3080 |
| `dsh --profile headless "任务"` | 一次性任务，适合 CI；退出码 0/1，无端口无交互 |
| `dsh --profile <name>` | 以指定 profile 启动 |
| `dsh plugin --profile <name> <pnpm args>` | 管理插件（web/headless 首次自动初始化，其余 profile 需手动创建） |
| `dsh --dump-config` / `--dump-default-config` | 检查合成配置 |
| `--port` / `--patch` | 覆盖端口 / 覆盖配置层 |

## 五、生态与扩展

- **插件生态**：GitHub topic `dsh-plugin`，约 300 个社区插件；「一切皆插件」无特权核心。
- **MCP 客户端**：`@deepseek-ai/dsh-mcp-client`，支持 stdio + streamable-http；工具命名 `mcp__<server>__<tool>`（与 Claude Code/Codex 同形）。**限制：只桥接 tools，Resources/Prompts 尚无消费者。**
- **架构能力缝隙**：`ctx.llm`、`ctx.tools`、`ctx.shell`、`ctx.sandbox`、会话日志；核心不变量 **"Model-visible means logged"**（模型可见即已记录）。
- 会话日志 append-only + Trajectory 视图；多 Agent/子代理编排；可替换沙箱。

## 六、与 Claude Code 对照 / 迁移

| 维度 | Claude Code | deepseek-harness (dsh) |
|---|---|---|
| 定位 | 开箱即用的闭源 CLI 成品 | 开源（MIT）可组装的 agent 运行时 |
| 架构 | 单体核心 + 扩展 | 一切皆插件，无特权核心 |
| 一次性任务 | `claude -p "..."` | `dsh --profile headless "..."` |
| 配置 | `settings.json` / `CLAUDE.md` / `.mcp.json` | YAML 补丁树 + Profile + Agent Preset |
| 模型 | 绑定 Claude | 默认 DeepSeek V4，可换 ~40 家 + OpenAI-compatible |
| 成本 | 相对高 | V4 Flash 约 $0.007/任务 vs Claude Opus 约 $0.54（90% 缓存命中） |
| 成熟度 | 成熟 | developer preview，有破坏性变更 |

**迁移策略**（第三方建议）：
1. 整体换 harness（dsh）
2. 或**保留 Claude Code，经 DeepSeek Anthropic 兼容端点** `api.deepseek.com/anthropic` 换底模，结构性便宜 10–25 倍。

## 七、常见坑清单

1. 官方**不开 GitHub Issues**，bug 反馈只走 Discussions。
2. developer preview，升级注意破坏性变更。
3. Web 端口被占 → `--port <空闲端口>`。
4. npm 装插件 ERESOLVE 冲突 → `--legacy-peer-deps`。
5. Windows 下多插件重复注册 `ctx.bash` → "service bash has been registered"。
6. **注意同名第三方包**（`pip install deepseek-harness`、`npx @deepseek-harness/mcp` 均非官方）。
7. DeepSeek V4 协议坑（第三方整理 16 条）：thinking 默认开启烧 token；多轮必须回传 `reasoning_content` 否则 HTTP 400；必须设 `max_tokens`。

---

## 方向菜单（待用户选择）

- **方向 A：快速上手 + 安装配置** — 安装三路径、首次配置、跑通第一个会话、Web UI 与 headless 用法（对应「如何安装使用」核心诉求）
- **方向 B：配置体系详解** — YAML 补丁树、Profile + Agent Preset、模型/Provider、权限模式、CLI 命令全集
- **方向 C：生态与扩展** — MCP 接入、插件开发、架构原理（一切皆插件）、沙箱与安全
- **方向 D：对比迁移 + 成本优化** — Claude Code ↔ dsh 对照表、迁移步骤、V4 协议坑、成本对比

> 用户基础：熟悉 Claude Code。以上方向可单选或组合；推荐 **A + D** 起步，补齐 B/C 成完整系列。
