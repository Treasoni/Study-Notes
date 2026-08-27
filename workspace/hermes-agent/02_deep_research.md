# Hermes Agent（Nous Research）— 深度研究

> 阶段 2 · 2026-08-28 · 项目 `workspace/hermes-agent/`
> 笔记类型：实战笔记 · 深度：上手实战 · 用户基础：有 agent 经验

## 1. 范围（Scope）

本文件为《Hermes Agent 上手实战》提供 claim 级研究素材，覆盖 5 个方向：定位与核心机制、安装与上手、核心机制实战、部署进阶、常见坑与最佳实践。素材以官方文档（tier 1）为主，tier 2/3 作为差异化与实操补充。

## 2. 来源表（Source Table）

| # | 来源 | Tier | 用途 | 抓取状态 |
|---|------|------|------|---------|
| S1 | GitHub README（github.com/NousResearch/hermes-agent） | 1 | 定位、特性、安装、坑 | ✅ 已深读 |
| S2 | 官方安装文档 `/docs/getting-started/installation` | 1 | 各平台安装、命令 | ✅ 已深读 |
| S3 | Memory Providers `/docs/user-guide/features/memory-providers` | 1 | 外置记忆机制 | ✅ 已深读 |
| S4 | Honcho `/docs/user-guide/features/honcho` | 1 | Honcho 用户建模 | ✅ 已深读 |
| S5 | providers `/docs/integrations/providers` | 1 | 模型 Provider 配置 | ✅ 已深读 |
| S6 | messaging `/docs/user-guide/messaging` | 1 | gateway、多平台、cron 投递 | ✅ 已深读 |
| S7 | cron `/docs/user-guide/features/cron` | 1 | 定时任务 | ✅ 已深读 |
| S8 | skills `/docs/user-guide/features/skills` | 1 | 技能体系 | ✅ 已深读 |
| S9 | memory `/docs/user-guide/features/memory` | 1 | 内置记忆实现 | ✅ 已深读 |
| S10 | delegation `/docs/user-guide/features/delegation` | 1 | 子代理 / RPC | ✅ 已深读 |
| S11 | docker `/docs/user-guide/docker` | 1 | Docker 部署 | ✅ 已深读 |
| S12 | code-execution `/docs/user-guide/features/code-execution` | 1 | 执行环境/沙箱 | ✅ 已深读 |
| S13 | creating-skills `/docs/developer-guide/creating-skills` | 1 | 技能开发规范 | ✅ 已深读 |
| S14 | Issue #16201（Windows/Git Bash bug） | 1 | Windows 坑 | ✅ 侦察确认 |
| S15 | DevelopersIO（Classmethod）源码阅读文 | 2 | 自改进机制复核 | 侦察摘要 |
| S16 | ZDNet 中国专访（联创 Karan） | 2 | 差异化/对齐哲学 | 侦察摘要 |
| S17 | 阿里云开发者社区（多后端运维） | 2 | 部署运维实操 | 侦察摘要 |
| S18 | CSDN（Windows 7 坑） | 3 | 社区实操经验 | 侦察摘要 |

> 注：P1 阶段发现的 `docs/user-guide/features/terminal-backends` 已 404（页面被重命名/迁移），相关内容由 S11/S12 承接。

## 3. Claim 地图（按方向）

### 3.1 定位与核心机制

- **定位**：Nous Research 出品的"自我改进 AI agent"，标语 "The agent that grows with you"；官方称"唯一带内置学习回路的 agent"（营销表述，竞品为 OpenClaw / Claude Code / Codex）。〔S1〕
- **运行形态**：可跑在 $5 VPS / GPU 集群 / serverless；不绑本地，云端 VM 上经 Telegram 对话。〔S1〕
- **模型无关**：Nous Portal / OpenRouter / OpenAI / 自建端点，`hermes model` 即时切换，无锁定。〔S1〕
- **学习闭环五要素**：从经验创建技能 → 使用中自改进 → 自我提示持久化知识 → 搜索历史对话 → 跨会话构建用户模型。〔S1〕
- **"封闭学习回路"清单**：agent 策展记忆 + 周期 nudge；复杂任务后自动创建技能；技能自改进；FTS5 会话搜索 + LLM 摘要跨会话回忆；Honcho dialectic 用户建模；兼容 agentskills.io 开放标准。〔S1〕
- **记忆分层**：内置 = 文件式 MEMORY.md + USER.md；另有 8 个外置 memory provider（同一时刻仅激活一个，内置始终并行）。〔S3〕
- **Honcho 机制**：plastic-labs 的 AI-native 记忆后端，在对话后推理"用户是谁"，存储"结论而非对话"；双层上下文注入（base 层 + dialectic 补充层）；三个正交旋钮 `contextCadence` / `dialecticCadence` / `dialecticDepth`；5 个工具；`hybrid/context/tools` 三种召回。〔S3/S4〕
- **差异化观点**（tier 2）：联创 Karan 主张核心是"自我改进系统"、拒绝向 prompt 灌输任意策略、重新定义对齐为"适配用户需求"、harness 比模型权重更能改变行为。〔S16〕
- **自改进实质**（tier 2）：源码阅读确认成长的是"技能与框架层而非模型权重"；v0.16 从"技能增长"转向"筛选与折叠"。〔S15〕

### 3.2 安装与上手

- **安装方式**：Linux/macOS/WSL2/Termux → `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`；Windows 原生 → PowerShell `iex (irm .../install.ps1)`；macOS/Windows 推荐 Desktop 安装器（纯 CLI 后可随时 `hermes desktop` 补装）。〔S2/S1〕
- **安装器行为**：自动装 uv、Python 3.11、Node.js v22、ripgrep、ffmpeg；Windows 另含便携 MinGit（`%LOCALAPPDATA%\hermes\git`）。〔S2/S1〕
- **前置条件**：非 Windows 唯一前置是 Git；Linux 另需 curl + xz-utils；桌面应用需 g++/build-essential。无需手动装 Python/Node。Nix 不再显式支持。〔S2〕
- **目录布局**：用户模式代码 `~/.hermes/hermes-agent/`、二进制 `~/.local/bin/hermes`、数据 `~/.hermes/`；Windows 原生 `%LOCALAPPDATA%\hermes`；root 模式 `/usr/local/lib/hermes-agent/`。〔S2〕
- **第一跑**：`source ~/.bashrc` → `hermes` 直接开聊；最快路径 `hermes setup --portal`（OAuth 登录 + Nous Provider + 开启 Tool Gateway）。〔S2〕
- **常用命令**：`hermes model`（完整向导）/ `hermes setup` / `hermes tools` / `hermes gateway setup` / `hermes config set|get` / `hermes doctor`（诊断）。〔S2〕
- **配置唯一来源**：`~/.hermes/config.yaml`；API key 在 `~/.hermes/.env`；OAuth 凭据在 `~/.hermes/auth.json`；`LLM_MODEL` 已移除。〔S5〕
- **Provider 要点**：至少要配一个 LLM provider；Nous Portal 推荐（OAuth 覆盖 300+ 模型 + Tool Gateway）；OpenRouter `OPENROUTER_API_KEY`；OpenAI 直连 `OPENAI_API_KEY` + `openai-api`；Anthropic 三认证（OAuth 需 Claude Max、`ANTHROPIC_API_KEY`、`ANTHROPIC_TOKEN`，Claude Pro 不能走 OAuth）；任意 OpenAI-compatible 端点可作 `custom` provider；本地 Ollama `http://localhost:11434/v1` 需 `context_length ≥ 64000`。〔S5〕
- **会话内/外切换**：`hermes model`（会话外全向导）vs `/model`（会话内切换已配置项）。〔S5〕
- **WSL2 网络**：连 Windows 宿主模型服务推荐 Win11 22H2+ mirrored 模式；NAT 模式用主机 IP（非 localhost），服务须绑 `0.0.0.0`（如 `OLLAMA_HOST`）。〔S5〕
- **Gateway**：`hermes gateway setup` 交互式配置；单 gateway 进程连 20+ 平台（Telegram/Discord/Slack/WhatsApp/Signal/Email 等）；bot 需要 model provider + tool provider（Nous Portal 一次捆绑）；默认 deny（白名单 + DM 配对 `hermes pairing approve telegram <code>`）；systemd/launchd 服务管理；日志 `~/.hermes/logs/gateway.log`。〔S6/S2〕

### 3.3 核心机制实战

#### Cron 定时任务〔S7〕
- 统一 `cronjob` 工具，对话中自然语言即可建/停/改/删。
- 调度格式：相对延迟（30m/2h/1d）、间隔（every 2h）、cron 表达式、ISO 时间戳。
- 结果自动投递到 20+ 平台（origin/local/telegram/slack/whatsapp/email/dingtalk/feishu/wecom…），agent 不自己发消息。
- 模型解析：任务 pin → cron.model → 全局默认；未 pin 任务快照全局默认，默认变更后 **fails closed**（跳过运行、零推理）。
- 派发前配置校验；失败置 `blocked_config`，仅一条告警，零 LLM 调用。
- `no_agent` 脚本模式：按计划跑脚本、stdout 原文投递、零 LLM；空输出=静默 tick，非零退出告警。
- `wakeAgent` 预检门：脚本输出 `{"wakeAgent":false}` 跳过本轮 LLM，零成本门控高频轮询。
- `context_from` 链式传上一任务输出；`continuity=true` 注入自己上次输出防重复报告。
- 网关每 60 秒 tick；任务存 `~/.hermes/cron/jobs.json`，历史入 `executions.db`。
- cron 会话默认不能再建 cron（防递归）；`workdir` 任务串行执行并注入该目录 AGENTS.md/CLAUDE.md。

#### Skills 技能体系〔S8/S13〕
- 按需加载的知识文档，"渐进式披露"省 token；兼容 agentskills.io。
- 三级加载：L0 `skills_list()`（~3k tokens）→ L1 `skill_view(name)` → L2 `skill_view(name,path)` 读参考文件。
- 每个已装技能自动成为斜杠命令；单条消息最多叠加 5 个技能。
- `/learn` 可从本地目录/URL/会话流程自动生成技能；大资料做成"知识库技能"（瘦 SKILL.md + references/ 逐章分文件）。
- `skill_manage` 工具让 agent 自建/改/删技能（程序记忆），构成自改进循环；`skills.write_approval` 可开审批门。
- Skills Hub 多源安装（official / skills.sh / well-known / GitHub / clawhub / lobehub / browse-sh / url）；全量安全扫描，`dangerous` 判定不可 `--force` 绕过。
- 条件激活：`fallback_for_toolsets`（高级工具缺失时自动出现免费替代）。
- SKILL.md 结构：frontmatter（name/description/version/author/license/platforms/metadata.hermes.*）+ 正文（When to Use / Quick Reference / Procedure / Pitfalls / Verification）。
- `required_environment_variables` 密钥存 `~/.hermes/.env` 不暴露模型，自动透传 terminal/execute_code 沙箱。
- 项目级技能需 `hermes skills trust` 才加载；优先级 project → local → external_dirs。

#### 内置记忆实现〔S9〕
- 两文件：MEMORY.md（agent 笔记，2200 字符/~800 tokens）+ USER.md（用户画像，1375 字符/~500 tokens），存 `~/.hermes/memories/`；会话启动冻结快照注入 system prompt。
- `memory` 工具仅 add/replace/remove（无 read，记忆自动注入）；replace/remove 用 `old_text` 唯一子串匹配。
- 不自动压缩；超限写入返回错误，代理须同回合合并/删除后重试。
- 冻结快照会话内不变以保前缀缓存；写入立即落盘但下会话才显示。
- 容量：memory 8-15 条、user 5-10 条；>80% 建议先合并；精确重复自动拒绝。
- 安全扫描：条目经注入/渗出威胁扫描，不可见 Unicode 即阻断。
- `session_search`：SQLite `~/.hermes/state.db` FTS5 全文检索，返回真实消息、无摘要无截断。
- 对比：memory 约 1300 tokens/提示固定开销 vs session_search ~20ms 查询、免费。
- 每轮后有后台自我改进审查（自动写记忆/改技能）；`write_approval` 时前台内联确认或 staged 到 `/memory pending`。
- `/journey` 时间线：删 memory 块即移除，技能归档可恢复。

#### 委派与 RPC〔S10/S12〕
- `delegate_task`：隔离子代理（全新会话、继承父工具权限、独立终端），只有最终摘要回主上下文；对父会话历史零知晓。
- 并行批处理：默认最多 3 并发，结果按输入序返回；顶层委托后台自动运行。
- 成本策略："frontier 规划 + 廉价 worker"；`delegation.model` 全局 pin。
- 子代理不能选工具集；leaf 禁用 delegate_task/clarify/memory/send_message/cronjob，但保留 `execute_code`。
- `execute_code` = Python 脚本程序化调用工具（web_search/web_extract/read_file/write_file/search_files/patch/terminal），经 Unix socket RPC，仅 `print()` 返回给 LLM，中间结果不进上下文（省 token）。
- 执行模式：`project`（默认，会话 cwd + 当前 VIRTUAL_ENV/CONDA 解释器）vs `strict`（临时隔离目录）。
- 资源限制：超时 300s（SIGTERM→5s 宽限→SIGKILL）、stdout 50KB、stderr 10KB、工具调用 50 次（均可配置）。
- 安全不变量：子进程环境剔除 KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/PASSWD/AUTH 变量；工具白名单禁递归 execute_code/delegate_task/MCP。
- 委托结果不可靠跨重启：进程重启不续跑子代理；要持久执行用 cronjob 或 background terminal。

### 3.4 部署进阶〔S11/S12〕

- **Docker 两种用途**：跑 Hermes 本体，或作为 terminal 后端（单常驻沙箱容器执行所有命令）。
- **持久化**：`/opt/data` 挂载宿主 `~/.hermes`（.env/config.yaml/SOUL.md/sessions/memories/skills/home/cron/hooks/logs/skins）；镜像无状态，升级不丢配置。
- **Gateway 模式**：`-p 8642:8642` 暴露 OpenAI 兼容 API + 健康端点；s6-overlay 监督崩溃自重启；建议开 `tool_loop_guardrails.hard_stop_enabled`。
- **安全硬性要求**：API server 需 `API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0` + ≥8 位 `API_SERVER_KEY`；dashboard `HERMES_DASHBOARD=1` 端口 9119，非环回绑定必须配认证否则 fail-closed（2026-06 未认证仪表盘曾遭扫描器植入 SSH 后门）。
- **多容器/多 profile**：禁止两个 gateway 容器挂同一数据目录（并发写不支持）；推荐单容器多 profile，各 profile API server 都默认绑 8642，需设独立 `API_SERVER_PORT`。
- **镜像权限模型**：`/init` root 运行后经 `s6-setuidgid` 降为 hermes 用户（UID 10000）；默认拒绝 root 启动 gateway（`HERMES_ALLOW_ROOT_GATEWAY=1` 覆盖）；`/opt/hermes` 安装树只读不可变。
- **镜像内容**：debian:13.4 + Python3.13(uv) + Node26 + Playwright/Chromium + docker-cli（可绑 `/var/run/docker.sock` 驱动宿主 Docker）+ openssh-client + s6-overlay。
- **Docker terminal 后端**：`terminal.backend: docker` + `docker_image/docker_volumes/docker_run_as_host_user/docker_persist_across_processes/docker_orphan_reaper`；skills 目录与凭据文件自动只读 bind-mount。
- **资源建议**：内存 1GB 起、2-4GB 推荐；数据卷 500MB/2GB；浏览器自动化最耗内存。
- **升级**：pull 新镜像重建容器，数据保留，自动配置迁移 + 时间戳备份。
- **多后端**：README 宣称 7 种后端（local/Docker/SSH/Singularity/Modal/Daytona/Vercel Sandbox）；Modal/Daytona 提供 serverless 持久化（空闲休眠、按需唤醒）。〔S1〕

### 3.5 常见坑与最佳实践

- **Windows 原生 vs WSL2 冲突**：README 称原生完全支持"无需 WSL"；providers.md 却称"Hermes Agent 需要 Unix 环境，Windows 用户应在 WSL2 内运行"。官方安装文档对原生标注 early beta，追求稳定推荐 WSL2。〔S1 vs S5〕
- **杀软误报**：Defender/Bitdefender/腾讯管家等把 `uv.exe`（Astral 未签名 Rust 二进制）误报为病毒；白名单应加**整个文件夹**而非文件哈希（uv 每版本哈希变化）；可用 `gh attestation verify` 校验。〔S1/S18〕
- **Windows 更新/文件锁**（Issue #16201）：uv.exe/hermes.exe 更新替换报 access denied（os error 5）；修复加指数退避 + 预隔离。更新前关闭 Hermes 进程。〔S14/S18〕
- **凭据泄露风险**：`~/.hermes` 同时含 `.env` 密钥与 `auth.json` OAuth token；同步到远程后端（Docker/SSH/Modal/Daytona）必须配置 ignore，否则凭据进不受控基础设施。〔S5/S17，推断〕
- **版本漂移**：Vercel Sandbox 后端 v0.15.0 移除、文档又回归；`terminal-backends` 文档页 404（已迁移）；涉及 Vercel 的旧配置（VERCEL_TOKEN 等）随版本失效。写笔记要标注版本依赖。〔S1/S14/实测〕
- **systemd**：勿加 `ExecStopPost` kill drop-in（无限重启循环）；无头 VM 用 user service + `loginctl enable-linger`；macOS launchd plist 静态固化 PATH，装新工具后重跑 `hermes gateway install`。〔S6〕
- **熔断器**：每平台适配器有熔断器，熔断后不自动恢复，须手动 `/platform resume`。〔S6〕
- **手动 clone**：venv 必须放源码树外，否则 agent 相对路径命令会清掉运行中环境。〔S1〕
- **后台进程**：默认 24h 后不再阻止会话自动重置（`bg_process_max_age_hours`，不 kill 仅忽略）。〔S6〕

## 4. 矛盾与风险（Contradictions）

1. **Windows 支持口径**：README "原生完全支持" vs providers "需要 Unix 环境走 WSL2" vs 安装文档 "原生 early beta"。结论：原生可跑，但模型服务/开发链路与稳定性以 WSL2 为准。
2. **后端数量漂移**：README 称 7 种；v0.15.0 commit 曾移除 Vercel Sandbox（7→6）；`terminal-backends` 文档页已 404。后端清单随版本剧烈变动。
3. **"唯一带学习回路"**：官方营销主张；联创访谈承认竞品为 OpenClaw（可迁移）/Claude Code/Codex。
4. **发布时间线**：仓库创建 2025-07-22，公开产品化约 2026-02/03（v0.2.0 于 2026-03-12）。引用时区分"创建"与"发布"。
5. **外置 memory provider 数量**：memory-providers 页自称"8 个"，但实际对比列出 9 个（Honcho/OpenViking/Mem0/Hindsight/Holographic/RetainDB/ByteRover/Supermemory/Memori）。

## 5. 实战指引（Practical Guidance）

- **上手路径**：安装（Windows 用 WSL2 或原生 PowerShell）→ `hermes setup --portal` 最快打通 → `hermes` 开始聊天 → 用 `/model` 切模型 → 深度用 `/learn` 造第一个技能 → 配 `hermes gateway setup` 连 Telegram 实现"随时可聊"。
- **给有 agent 经验的用户**：核心关注点应为**学习闭环**（`/journey` 时间线、`/skills`、记忆自动维护）与 **cron/delegation 自动化**，这两者区别于 Claude Code/OpenClaw。
- **配置最小集**：`~/.hermes/config.yaml`（模型/provider/base_url）+ `~/.hermes/.env`（密钥）。先 `hermes doctor` 诊断。
- **写笔记时的版本标注**：所有涉及后端数量、Vercel Sandbox、`terminal-backends` 页面的内容都应标注"以 v0.18+ 文档为准"。
- **安全基线**：密钥只放 `~/.hermes/.env`；远程后端同步时 exclude `~/.hermes` 密钥文件；Docker 用非 root gateway + `API_SERVER_KEY` ≥8 位 + dashboard 强制认证。

## 6. 开放问题（Open Questions）

- 技能"自改进"的具体评估/触发规则（文档只有行为描述，无 eval 机制）。
- cron 与 delegation 的并发资源预算是否共享。
- 各终端后端（SSH/Singularity/Modal/Daytona）的配置参数与休眠/唤醒细节（本次主要深读 Docker + 本地执行环境）。
- Nous Portal 免费额度与 Tool Gateway 能力边界。

## 7. 下游交接（Handoff）

- **给 outline-generator**：以上 5 个方向的 claim 均可映射到章节；建议大纲按"定位 → 安装 → 上手 → 核心机制 → 自动化/部署 → 坑"组织。素材充足度：安装/定位/记忆/skills/cron/delegation/docker 高；SSH/Modal/Daytona 后端细节中等（可选章节）。
- **引用策略**：官方文档路径已记录（S2-S13）；引用时给出 URL + 章节锚点。tier 2/3 只用于差异化观点与实操佐证，标注来源层级。
- **遗留**：如需补 SSH/Modal/Daytona 具体配置，可在章节写作阶段按需增量抓取 `docs/user-guide/features/*` 或开发者文档。
