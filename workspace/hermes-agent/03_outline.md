# 学习笔记大纲：《Hermes Agent（Nous Research）上手实战》

> 笔记类型：实战笔记（按「定位 → 环境搭建 → 核心机制 → 自动化 → 部署 → 坑」组织，对应实战笔记「环境搭建 → 核心功能 → 进阶优化 → 部署」的变体）
> 预计总篇幅：约 9,500-13,000 字
> 章节数：9
> 目标读者：已有 agent 工具经验（Claude Code / Cursor / OpenClaw），跳过 agent 基础概念，聚焦 hermes-agent 差异化特性与上手实战
> 版本基线：涉及后端数量、Vercel Sandbox、`terminal-backends` 页面等内容均标注"以 v0.18+ 文档为准"（版本漂移见 02_deep_research.md 第 3.5 / 4 节）

## 第一章：定位与核心理念：一个会自我改进的 agent

- **篇幅**：短（约 600-900 字）
- **覆盖要点**：
  - Hermes Agent 是什么：Nous Research 出品、标语 "The agent that grows with you"、运行形态（$5 VPS / GPU 集群 / serverless）
  - 与 Claude Code / OpenClaw 的差异：核心不是"更多工具"，而是"内置学习回路"
  - 学习闭环五要素与"封闭学习回路"清单（策展记忆 + 周期 nudge、任务后自动建技能、技能自改进、FTS5 会话检索 + LLM 摘要、Honcho 用户建模、agentskills.io 开放标准）
  - 自改进实质（tier 2 复核）：成长发生在技能与框架层而非模型权重；v0.16 从"技能增长"转向"筛选与折叠"
  - 营销口径与版本提示："唯一带学习回路"为官方营销表述，竞品为 OpenClaw / Claude Code / Codex
- **素材引用**：S1, S15, S16
- **代码示例**：无

## 第二章：安装与第一跑：从命令到首次对话

- **篇幅**：中（约 900-1,300 字）
- **覆盖要点**：
  - 平台安装：Linux/macOS/WSL2/Termux 一行脚本、Windows 原生 PowerShell、macOS/Windows Desktop 安装器（纯 CLI 后可随时 `hermes desktop` 补装）
  - 安装器行为与前置条件：自动装 uv / Python 3.11 / Node.js 22 / ripgrep / ffmpeg / Windows 便携 MinGit；唯一硬前置是 Git；Nix 不再显式支持
  - 目录布局：`~/.hermes/hermes-agent/`、`~/.local/bin/hermes`、`%LOCALAPPDATA%\hermes`（Windows 原生）
  - 第一跑：`hermes setup --portal` 最快打通（OAuth 登录 + Nous Provider + Tool Gateway）
  - Windows 原生 vs WSL2 决策：README"原生无需 WSL" vs providers"需 Unix 环境走 WSL2" vs 安装文档"原生 early beta"的口径矛盾与推荐结论（含杀软误报 uv.exe 预提示）
  - 常用命令速查：`hermes model` / `setup` / `tools` / `gateway setup` / `config set|get` / `doctor`
- **素材引用**：S1, S2, S14, S18
- **代码示例**：有（curl / iex 安装命令、`source ~/.bashrc`、`hermes setup --portal`、`hermes doctor`）

## 第三章：模型 Provider 配置：打破模型锁定

- **篇幅**：中（约 900-1,300 字）
- **覆盖要点**：
  - 配置唯一来源：`~/.hermes/config.yaml` + `~/.hermes/.env`（API key 在 .env、OAuth 凭据在 auth.json；`LLM_MODEL` 已移除）
  - Provider 全家桶：Nous Portal（OAuth 覆盖 300+ 模型 + Tool Gateway，推荐）、OpenRouter、OpenAI 直连、Anthropic 三种认证（Claude Max OAuth / `ANTHROPIC_API_KEY` / `ANTHROPIC_TOKEN`，Claude Pro 不能走 OAuth）、任意 OpenAI-compatible 端点作 custom、本地 Ollama（`context_length ≥ 64000`）
  - 会话外 `hermes model`（全向导）vs 会话内 `/model`（切换已配置项）
  - WSL2 访问 Windows 宿主模型服务：Win11 22H2+ mirrored 模式 vs NAT 模式用主机 IP + 服务绑 `0.0.0.0`（如 `OLLAMA_HOST`）
- **素材引用**：S5
- **代码示例**：有（config.yaml 片段、.env 密钥清单、Ollama base_url 示例）

## 第四章：记忆与学习闭环：跨会话成长

- **篇幅**：长（约 1,200-1,700 字）
- **覆盖要点**：
  - 内置记忆两文件：MEMORY.md（agent 笔记，约 800 tokens）+ USER.md（用户画像，约 500 tokens）、容量与合并策略（memory 8-15 条 / user 5-10 条、>80% 建议合并）、冻结快照与前缀缓存
  - `memory` 工具：add / replace / remove（无 read，自动注入；replace/remove 用 old_text 唯一子串匹配）、超限同回合合并重试、注入/渗出安全扫描
  - 跨会话检索：`session_search` + SQLite FTS5（返回真实消息、约 20ms、免费；对比 memory 约 1300 tokens 固定开销）
  - 外置记忆与 Honcho：memory-providers 自称 8 个实列 9 个（同一时刻仅激活一个，内置始终并行）；Honcho dialectic 用户建模（"结论而非对话"）、三个正交旋钮 `contextCadence` / `dialecticCadence` / `dialecticDepth`、`hybrid/context/tools` 三种召回
  - 后台自我改进审查：自动写记忆/改技能、`write_approval` 前台内联确认或 staged 到 `/memory pending`
  - `/journey` 时间线（删 memory 块即移除、技能归档可恢复）
- **素材引用**：S3, S4, S9
- **代码示例**：有（memory 工具调用示例、Honcho 配置旋钮示例）

## 第五章：技能体系：把经验沉淀为可复用资产

- **篇幅**：中长（约 1,100-1,500 字）
- **覆盖要点**：
  - 技能是什么：按需加载的知识文档、"渐进式披露"省 token、兼容 agentskills.io 开放标准
  - 三级加载：L0 `skills_list()`（~3k tokens）→ L1 `skill_view(name)` → L2 `skill_view(name,path)`；已装技能自动成为斜杠命令、单条消息最多叠加 5 个
  - 用 `/learn` 从本地目录/URL/会话流程自动生成技能；大资料做成"知识库技能"（瘦 SKILL.md + references/ 逐章分文件）
  - SKILL.md 规范：frontmatter（name/description/version/author/license/platforms/metadata.hermes.*）+ 正文五段（When to Use / Quick Reference / Procedure / Pitfalls / Verification）
  - `skill_manage` 工具：agent 自建/改/删技能（程序记忆），`skills.write_approval` 审批门
  - Skills Hub 多源安装（official / skills.sh / GitHub / clawhub / lobehub…）与全量安全扫描（`dangerous` 不可 `--force` 绕过）
  - 条件激活 `fallback_for_toolsets`、`required_environment_variables` 存 .env 自动透传沙箱、项目级技能 `hermes skills trust`
- **素材引用**：S8, S13
- **代码示例**：有（/learn 命令、SKILL.md frontmatter 与结构示例、skills 安装命令）

## 第六章：多平台接入与定时任务：从"你找它"到"它找你"

- **篇幅**：长（约 1,500-2,000 字）
- **覆盖要点**：

### 6.1 Gateway 多平台接入

- `hermes gateway setup` 交互式配置；单 gateway 进程连 20+ 平台（Telegram/Discord/Slack/WhatsApp/Signal/Email…）
- bot 需要 model provider + tool provider（Nous Portal 一次捆绑）
- 默认 deny 白名单 + DM 配对：`hermes pairing approve telegram <code>`
- systemd / launchd 服务管理、日志 `~/.hermes/logs/gateway.log`、无头 VM `loginctl enable-linger`
- 平台适配器熔断器：熔断后不自动恢复，须手动 `/platform resume`

### 6.2 cron 定时任务

- `cronjob` 工具：自然语言建/停/改/删；四种调度格式（相对延迟 30m/2h、间隔 every 2h、cron 表达式、ISO 时间戳）
- 结果自动投递到 20+ 平台，agent 不自己发消息；`context_from` 链式传上一任务输出、`continuity=true` 防重复报告
- 模型解析与 `fails closed`（任务 pin → cron.model → 全局默认；默认变更后跳过运行、零推理）
- `no_agent` 脚本模式（零 LLM、stdout 原文投递、空输出=静默 tick）；`wakeAgent` 预检门（输出 `{"wakeAgent":false}` 跳过本轮）
- 任务存 `~/.hermes/cron/jobs.json`、历史入 `executions.db`、网关每 60 秒 tick、cron 会话防递归、`workdir` 任务串行执行并注入 AGENTS.md/CLAUDE.md
- **素材引用**：S6, S7
- **代码示例**：有（`hermes gateway setup` / pairing 命令、cron 调度定义、`no_agent` 脚本 JSON 输出、systemd 服务片段）

## 第七章：委派与并行：子代理与 execute_code

- **篇幅**：中（约 900-1,300 字）
- **覆盖要点**：
  - `delegate_task`：隔离子代理（全新会话、继承父工具权限、独立终端、只有最终摘要回主上下文、对父会话历史零知晓）
  - 并行批处理：默认最多 3 并发、结果按输入序返回、顶层委托后台自动运行
  - 成本策略："frontier 规划 + 廉价 worker"、`delegation.model` 全局 pin、子代理不能选工具集
  - `execute_code`：Python 脚本程序化调用工具（web_search / read_file / write_file / patch / terminal…）、Unix socket RPC、仅 `print()` 返回 LLM、中间结果不进上下文省 token
  - 执行模式：`project`（默认，会话 cwd + 当前解释器）vs `strict`（临时隔离目录）；资源限制（超时 300s / stdout 50KB / stderr 10KB / 工具 50 次，均可配置）
  - 安全不变量：子进程剔除 KEY/TOKEN/SECRET 等环境变量、工具白名单禁递归 execute_code/delegate_task/MCP
  - 委托结果跨重启不可靠（进程重启不续跑子代理）→ 持久执行用 cronjob / background terminal
- **素材引用**：S10, S12
- **代码示例**：有（delegate_task 调用示例、execute_code 脚本示例、资源限制配置）

## 第八章：部署进阶：Docker、多后端与安全基线

- **篇幅**：长（约 1,300-1,800 字）
- **覆盖要点**：
  - Docker 两种用途：跑 Hermes 本体 vs 作为 terminal 后端（单常驻沙箱容器执行所有命令）
  - 持久化：`/opt/data` 挂载宿主 `~/.hermes`（.env / config.yaml / SOUL.md / memories / skills / cron / hooks / logs…），镜像无状态、升级不丢配置
  - Gateway 模式：`-p 8642:8642` 暴露 OpenAI 兼容 API + 健康端点、s6-overlay 崩溃自重启、建议开 `tool_loop_guardrails.hard_stop_enabled`
  - 安全硬性要求：`API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0` + ≥8 位 `API_SERVER_KEY`；dashboard 非环回绑定必须配认证否则 fail-closed（2026-06 未认证仪表盘曾遭扫描器植入 SSH 后门）
  - 多容器/多 profile：禁止两个 gateway 容器挂同一数据目录、各 profile 独立 `API_SERVER_PORT`；镜像 `/init` root 后降权 hermes 用户（UID 10000）、默认拒绝 root 启动 gateway
  - 多后端清单与版本漂移：README 宣称 7 种（local/Docker/SSH/Singularity/Modal/Daytona/Vercel Sandbox）；v0.15.0 曾移除 Vercel Sandbox 又回归、`terminal-backends` 页 404 —— 标注"以 v0.18+ 文档为准"
  - 资源建议（内存 1GB 起 / 2-4GB 推荐；数据卷 500MB/2GB）与升级策略（pull 新镜像重建、配置自动迁移 + 时间戳备份）
- **素材引用**：S1, S11, S12, S17
- **代码示例**：有（docker run / 数据卷挂载、API server 环境变量、Docker terminal 后端配置）

## 第九章：常见坑与最佳实践

- **篇幅**：中（约 900-1,300 字）
- **覆盖要点**：
  - Windows 原生 vs WSL2 再总结：原生可跑但模型服务/开发链路与稳定性以 WSL2 为准
  - 杀软误报：Defender/Bitdefender/腾讯管家把 uv.exe 误报为病毒；白名单加整个文件夹而非文件哈希（uv 每版本哈希变化）；`gh attestation verify` 校验
  - Windows 文件锁（Issue #16201）：更新替换报 access denied（os error 5），更新前关闭 Hermes 进程
  - 凭据泄露风险：`~/.hermes` 同时含 .env 密钥与 auth.json OAuth token；同步到 Docker/SSH/Modal/Daytona 等远程后端必须配置 ignore
  - systemd 反模式：勿加 `ExecStopPost` kill drop-in（无限重启循环）；无头 VM 用 user service + `loginctl enable-linger`；macOS 装新工具后重跑 `hermes gateway install` 固化 PATH
  - 其他坑：熔断器不自动恢复、手动 clone 时 venv 必须放源码树外、后台进程默认 24h 后不再阻止会话自动重置
  - 版本漂移总原则：后端数量 / Vercel / 页面路径一律标注版本依赖
  - 安全基线速查：密钥只放 `~/.hermes/.env`、远程后端 exclude 密钥文件、Docker 非 root gateway + `API_SERVER_KEY` ≥8 位 + dashboard 强制认证
- **素材引用**：S1, S5, S6, S14, S17, S18
- **代码示例**：无（仅少量命令佐证，如 `gh attestation verify`、`loginctl enable-linger`）

## 学习路径说明

### 前置要求

- 已有任一 agent 工具使用经验（Claude Code / Cursor / OpenClaw），熟悉 prompt、工具调用、项目目录等概念，本笔记不再讲解 agent 基础
- 能熟练使用命令行（bash / PowerShell）；Windows 用户需在 WSL2 与原生路线之间做出选择
- 一个可用的模型入口：Nous Portal 账号（推荐，OAuth 一条龙）或 OpenRouter / OpenAI / Anthropic API key，或本地 Ollama
- 可选：Telegram / Discord 账号（体验第六章多平台网关）

### 学完能做什么

- 在 Windows / WSL2 / Linux 完成 Hermes Agent 安装，跑通第一次对话
- 配置多种模型 Provider 并即时切换，理解 config.yaml + .env 的配置唯一来源原则
- 观察并理解"学习闭环"：记忆自动维护、技能自动创建与改进、跨会话检索
- 用 `/learn` 和 SKILL.md 规范创建自己的第一个技能
- 接入 Telegram / Discord 随时可聊，配置 cron 定时任务与子代理并行执行
- 在 Docker / 多后端完成部署，掌握安全基线，规避 Windows 与版本漂移类常见坑

### 建议学习顺序

- 第 1-3 章为"上手三连"，建议连续阅读并照做命令实操（约 1-2 小时）
- 第 4-5 章是核心差异化，实操后隔一段时间回来观察"学习闭环"是否真实发生
- 第 6-7 章为自动化进阶，按需选用（只玩 CLI 可暂缓 gateway 部分）
- 第 8-9 章按部署需求选读；第 9 章建议全读（踩坑成本最低的章节）
