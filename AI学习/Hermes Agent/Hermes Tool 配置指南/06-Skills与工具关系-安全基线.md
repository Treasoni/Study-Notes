---
title: "Skills 与工具关系 · 安全基线"
tags:
  - AI学习
  - Agent
  - Hermes
  - 工具配置
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-tool-config
---

> [[05-MCP 接入与排错|⬅ 上一章]] · [[README|📖 返回目录]]

# 第 6 章 Skills 与工具关系 · 安全基线

前五章我们把工具本身讲透了：内置 toolsets（第 1、2 章）、网关与审批（第 3 章）、自定义工具（第 4 章）、MCP 接入（第 5 章）。这一章做两件事：先把 tool / skill / memory 三者的关系收束清楚，让你站在「工具视角」理解 skill 引用工具的约束；然后给出一套安全基线——从审批纵深、YOLO 与 hardline，到环境变量防泄漏，最后落到一份 Docker 场景的检查清单，把你前面配的所有能力「拧紧螺丝」。

## 6.1 关系收束：tool = 可执行能力，skill = 程序性知识文档，memory = facts

Hermes 里有三样东西都能跨会话存在，但它们分工完全不同（来源 FAQ「What's the difference between memory and skills?」）：

| 概念 | 存什么 | 谁来执行 | 何时被用到 |
| --- | --- | --- | --- |
| **tool** | 一段可调用的能力（schema + handler） | agent 直接调用，如 `web_search`、`terminal`、`read_file` | 模型决定「下一步做什么」时 |
| **skill** | 程序性步骤 procedures，一份 SKILL.md 文档 | 不自己执行，靠调用工具 / shell 落地 | agent 遇到相似任务时被召回 |
| **memory** | 事实 facts（关于你、项目、偏好） | 自动注入系统提示 | 按相关性自动检索 |

第 5 章《技能体系》已经把 skill 的生命周期、SKILL.md 结构讲透了（[[Hermes Agent 上手实战/05-技能体系|第 5 章]]）。这里不重复正文，只站在「工具视角」补一句关键关系：**skill 是工具的使用说明书**。它写的是「怎么做」的步骤，本身不执行任何东西，最终还是要落到调用工具或 shell 上。所以判断「某个能力该做成 skill 还是 tool」，本质是在问「它是一份说明书，还是一段必须精确执行的程序」——这个决策框架在第 4 章 4.1 已给出（来源 S6）。

> [!tip] 大白话
> 把 **skill 想成菜谱**（写清楚先放油还是先放盐），**memory 想成你家的食材清单和口味偏好**（自动记着你不吃辣），**tool 想成厨具**（锅、刀、灶）。厨师（agent）照着菜谱、用厨具、按口味偏好做菜。菜谱不会自己做饭——skill 永远不会自己执行，它只是指导 agent 去调用工具。

对「工具视角」还有一个直接后果：因为 skill 靠引用工具来干活，**skill 里点名引用的工具必须有来源**。贡献指南的硬性约束是：SKILL.md 正文里引用的工具，必须是原生 Hermes 工具，或者 skill 在 `## Prerequisites` 里显式写明如何接入的 MCP server（来源 S6）。`grep`、`cat`、`sed` 这类 shell 命令不该出现在正文里，要写成它们对应的封装工具（`search_files`、`read_file`、`patch`）。换句话说，**一个 skill 能干什么，取决于系统里有哪些工具可被它调用**——这就是 tool 和 skill 的耦合点。

## 6.2 skill 写安全：`write_approval` 门禁与内容守卫

skill 既然是可跨会话、会被自动召回的文档，agent 用 `skill_manage` 工具自己增删改 skill 就有风险：如果它写进一个带恶意指令的 SKILL.md，下一次会话就可能在毫无提示的情况下被执行。Hermes 给了两层闸门（来源 S11）：

**第一层：`skills.write_approval`（默认 false）**。设为 `true` 后，agent 的**每一次** skill 写操作（create / edit / patch / delete / supporting files）都会先进入待审队列，不会直接落盘：

```yaml
# ~/.hermes/config.yaml
skills:
  write_approval: true   # false = 自由写入（默认） | true = 每次写都先审
```

开启后，被 stage 的写操作放在 `~/.hermes/pending/skills/`，在 CLI 或任何消息平台上用这些命令审查：

```bash
/skills pending            # 查看待审队列
/skills diff <id>          # 看具体改动 diff
/skills approve <id>       # 批准
/skills reject <id>        # 拒绝
/skills approval on|off    # 运行时开关
```

注意它和 dangerous-command 审批是同一套机制：你在会话里批准它，和在 CLI 里敲 `[o]nce` 批准一条危险命令，走的是同一个 approve/deny 通道（来源 S11）。

**第二层：`skills.guard_agent_created`（默认 false）**。这是独立于写审批的内容扫描器——agent 创建/编辑 skill 时，扫描新内容里是否有危险关键词模式（窃取凭据、明显的提示注入、外传指令），命中就弹审批并给出扫描理由。默认关，是因为真实工作流里 agent 合法地提到 `~/.ssh/` 或 `$OPENAI_API_KEY` 会频繁误触；想要就打开：

```yaml
skills:
  guard_agent_created: true   # 默认 false
```

> [!tip] 大白话
> 把 `skills.write_approval` 想成**临时工牌审批**：agent 每次想给自己办一张「新门禁卡」（新增/改一份 skill），都要先填申请表，你点头才发卡。默认关闭等于「工牌自助领取」，全看你对这个 agent 的信任程度。

## 6.3 全局禁用：`agent.disabled_toolsets`

第 1 章讲过 `hermes tools` 可以按平台逐项开关 toolset。但如果你要的是「**任何平台都关掉某个工具集**」——比如不想让 memory 工具自动注入 `MEMORY_GUIDANCE`，或者完全不想要 web 搜索——一条条改十几个平台行就很烦。`agent.disabled_toolsets` 就是为这个场景准备的全局总闸（来源 S11）：

```yaml
# ~/.hermes/config.yaml
agent:
  disabled_toolsets:
    - memory       # 隐藏 memory 工具 + 去掉 MEMORY_GUIDANCE 注入
    - web          # 任何平台都没有 web_search / web_extract
```

它的执行时机很关键：**在** `hermes tools` 写入的 `platform_toolsets` **之后生效**。也就是说，即使某个平台保存的配置里还列着 `web`，只要 `disabled_toolsets` 里有它，这个平台一样会被移除。留空或省略该键等于什么都不做（no-op）。这正好和第 3 章、第 5 章接上：你可以在平台层精细控制「哪些工具可用」，但总闸一拉，所有平台同步失效——这是「single switch」和「15+ 行平台配置」的分工。

> [!tip] 大白话
> 把 `agent.disabled_toolsets` 想成家里的**总电闸**。房间里的灯（各平台配置）你可以逐盏开关，但总闸一拉，全屋断电，房间开关再开着也没用。

## 6.4 安全基线：approvals 三种模式、YOLO 三入口、hardline 永不可覆盖

第 3 章 3.6 已经介绍了 `approvals` 体系的基础。这里从「纵深防御」角度把它串成一条线：从最宽松到最严格，层层都有独立执行点（来源 Sec）。

**审批模式 `approvals.mode`（默认 smart）**：

| mode | 行为 | 适用 |
| --- | --- | --- |
| `smart` | 用辅助 LLM 评估风险：低风险命令仅本次自动放行，真危险命令自动拒绝，拿不准的弹人工审批 | 默认，日常 |
| `manual` | 危险命令一律弹窗等你批准 | 需要最大可控性 |
| `off` | 禁用所有审批检查，等价于 `--yolo` | 仅在可信环境（CI/CD、容器） |

配套键：`timeout`（默认 300 秒，超时按 **deny** fail-closed）、`cron_mode: deny`（cron 无头场景遇危险命令默认拒绝）、`single_query_mode: deny`（`-q` 一次性会话同理由）。

CLI 里危险命令的审批流是四个选项：`[o]nce`（仅本次）/ `[s]ession`（本会话）/ `[a]lways`（写入 `command_allowlist` 永久放行）/ `[d]eny`（默认拒绝）。消息平台上则回 `yes`/`y`/`approve`/`ok` 批准、`no`/`n`/`deny`/`cancel` 拒绝；网关运行时会自动设 `HERMES_EXEC_ASK=1`（来源 Sec）。

**YOLO 三入口**——绕过的是「审批提示」，不是「所有安全检查」：

```bash
hermes --yolo                          # 1) 启动时 CLI 参数
# 会话内：/yolo                        # 2) 斜杠命令，开关切换
# .env / 环境：HERMES_YOLO_MODE=1      # 3) 环境变量
```

YOLO 生效时界面会常驻两个视觉提醒：会话起始的红字横幅 `⚠ YOLO mode — all approval prompts bypassed`，以及状态栏里的 `⚠ YOLO` 片段（来源 Sec）。这是防「开着 YOLO 忘了关」。

**hardline blocklist（UNRECOVERABLE_BLOCKLIST）永不可覆盖**——这是 `--yolo` 之下的地板（floor），**先于审批层执行**，没有任何开关能绕过：不管 `--yolo`、`approvals.mode: off`、cron 的 `approve` 模式，还是你手动点过「allow always」，命中一律拒绝并返回解释性错误，且 agent 被明确告知不要换说法重试。目前覆盖的模式包括：

- `rm -rf /` 及其明显变体、`rm -rf --no-preserve-root /`
- bash 炸弹 `:(){ :|:& };:`
- 对已挂载根设备的 `mkfs.*`、`dd if=/dev/zero of=/dev/sd*`
- 把不受信任的 URL 直接管道给 rootfs 顶层的 `sh`

`approvals.deny` 是它的用户可编辑镜像：glob 模式（fnmatch，大小写不敏感，匹配的是去混淆后的命令文本），同样**先于** YOLO/off 生效，用来跑「yolo-with-exceptions」——除了这几件事，别的随便来（来源 Sec）：

```yaml
approvals:
  deny:
    - "git push --force*"
    - "*curl*|*sh*"
    - "dd if=* of=/dev/*"
```

> [!warning] YAML 引号
> `approvals.deny` 的每条模式**务必加引号**。裸开头的 `*` 在 YAML 里是别名，会解析失败；`{`、`!`、`:` 也各有 YAML 含义。shell 类内容用单引号最安全（来源 Sec）。

**容器后端跳过危险命令检查**：当 terminal 后端是 `docker` / `singularity` / `modal` / `daytona` / `vercel_sandbox` 时，危险命令检查**整体跳过**——因为容器本身就是安全边界，容器里跑 `rm -rf /` 伤不到宿主（来源 Sec）。这是「纵深」的最后一环：生产网关建议直接上容器后端，彻底免掉审批的人肉负担，把安全交给隔离而不是提示。反过来也要记住：**只读性的守卫（hardline blocklist、`approvals.deny`）对容器后端同样不生效**，因为它根本不会走到检查栈。

> [!tip] 大白话
> 把 **hardline blocklist 想成银行的「不可交易名单」**。你可以在柜台（approvals）、甚至开 VIP 免排队通道（YOLO）减少验证，但名单上的人（`rm -rf /` 这类）无论你开什么权限、找什么关系，柜员都直接拒绝办理——不是「等你确认」，是**根本没资格被提交审批**。

## 6.5 防泄漏与沙箱：四个环境变量与执行沙箱

除了审批，安全基线的另一半是「防泄漏」。四个 `HERMES_*` 环境变量是核心（来源 S5）：

| 变量 | 默认 | 作用 |
| --- | --- | --- |
| `HERMES_SAFE_MODE` | 关 | 排障模式：禁用**所有**自定义——跳过插件发现、MCP server 加载、shell hook 注册。`--safe-mode` 会自动设置它（并连带两个 ignore 开关） |
| `HERMES_WRITE_SAFE_ROOT` | 不设 | `write_file` / `patch` 只能写进列出的目录前缀，越界**硬拦截**（不走审批、无提示）。官方 Docker 镜像设 `/opt/data` |
| `HERMES_REDACT_SECRETS` | `true` | 在工具输出、日志、聊天回复里自动打码密钥 |
| `HERMES_MAX_ITERATIONS` | `500` | 每次对话最大 tool-call 迭代数 |

`HERMES_SAFE_MODE` 是排障时的「最小化启动」：怀疑是插件、MCP 或 hook 搞坏了环境时，开了它就能用最干净的状态复现问题（来源 S5）。

`HERMES_WRITE_SAFE_ROOT` 的坑值得单独警告：官方 Docker 镜像把它设为 `/opt/data`，所以 agent 的写操作天然被锁在挂载卷里，出不去——这正是想要的。但如果你**手工**把它指向一个项目目录，agent 就再也写不了 `~/.hermes/cron/jobs.json`、`~/.hermes/skills/` 这些 Hermes 状态文件，全都会报 `outside HERMES_WRITE_SAFE_ROOT`。要多根就按 `os.pathsep` 分隔（Unix 用 `:`）：

```bash
export HERMES_WRITE_SAFE_ROOT=/path/to/project:/home/you/.hermes
```

> [!warning] 别随便往 `.env` 加 `HERMES_WRITE_SAFE_ROOT`
> 它不是「更安全就开着」的变量，而是一个**行为约束**。设了它，等于告诉 Hermes「agent 只许写这几个目录」，所有 Hermes 自身的状态文件也被一并挡住。除非你真的要沙箱化写操作（Docker 场景就是），否则保持不设（来源 S5 / Sec）。

**执行沙箱剥离 API keys**：`execute_code` 的子进程环境会过滤掉名字含 `KEY` / `TOKEN` / `SECRET` / `PASSWORD` / `CREDENTIAL` / `PASSWD` / `AUTH` 的变量，只放行安全前缀变量（来源 S6 / Sec）。也就是说，agent 生成的代码即使想偷 `OPENAI_API_KEY`，它拿不到——除非某个 skill 在 SKILL.md 里显式声明了 `required_environment_variables`，那是唯一被允许的 passthrough。MCP 的 stdio 子进程也一样：宿主环境只透传 `PATH/HOME/USER/LANG/LC_ALL/TERM/SHELL/TMPDIR` 加 `XDG_*`，其余全部剥掉；MCP 工具的错误消息还会做脱敏（GitHub PAT、`sk-` key、Bearer token 一律替换为 `[REDACTED]`）（来源 Sec）。

> [!tip] 大白话
> 把 `HERMES_REDACT_SECRETS` 想成**自动打码**。就像综艺节目里敏感词自动「哔——」，Hermes 在把工具输出、日志、回复交给你看之前，先把像密钥的东西涂黑，默认一直开着。

## 6.6 实操：Docker 场景安全检查清单

最后落地。假设你按《上手实战》第 2 章用 Docker 跑 Hermes（宿主机 `-v ~/.hermes:/opt/data`），并启用了 `terminal.backend: docker` 的「容器内的容器」。这份清单把本章所有点串起来（来源 Sec / S11）：

**① 密钥只落在宿主机 `~/.hermes/.env`，不进容器镜像**

```bash
chmod 600 ~/.hermes/.env          # 文件权限收紧
```

- 镜像里的任何 layer 都不该有密钥：用 `docker_forward_env: []`（默认空）保持容器**不继承**宿主环境变量，密钥天然进不去（来源 Sec / S11）。
- 确需临时给容器用的 token（如 `GITHUB_TOKEN`）才放进 `docker_forward_env`——但要明白：一旦放进去，容器内代码就**能读并能外传**，只forward你能接受暴露的（来源 Sec）。
- `.env` 永远不进 git。`.env.example` 只放占位符（来源 S5）。

**② 容器即边界：资源限制 + 加固参数**

```yaml
# ~/.hermes/config.yaml — 安全基线片段（v0.20.x，以 hermes doctor 为准）
agent:
  disabled_toolsets:
    - memory
    - web
approvals:
  mode: smart
  timeout: 300
  cron_mode: deny
  single_query_mode: deny
skills:
  write_approval: true
  guard_agent_created: false
terminal:
  backend: docker
  docker_image: "python:3.11-slim"
  docker_forward_env: []     # 空 = 密钥不进容器
  container_cpu: 2
  container_memory: 4096
  container_disk: 20480
  # docker_network: false    # 需要时空气隙：--network=none
```

Hermes 给每个终端容器内置的安全加固（`tools/environments/docker.py`）是：`--cap-drop ALL` + 只补回 `DAC_OVERRIDE/CHOWN/FOWNER`、`--security-opt no-new-privileges`（禁止提权）、`--pids-limit 256`（限进程数）、大小受限的 tmpfs（`/tmp` 512MB、`/var/tmp` 256MB 且 noexec）（来源 Sec / S11）。资源限制（`container_cpu/memory/disk`）由你控制上限；要完全断网可设 `docker_network: false`。`execute_code` 沙箱剥离 API keys 的机制在 6.5 已讲。

**③ 网关授权顺序——默认拒绝**

如果你跑消息网关，`_is_user_authorized()` 按这个顺序检查（来源 Sec）：

```
平台 allow-all（如 DISCORD_ALLOW_ALL_USERS=true）
  → DM pairing 已批准名单
  → 平台 allowlist（TELEGRAM_ALLOWED_USERS=...）
  → 全局 GATEWAY_ALLOWED_USERS
  → 全局 GATEWAY_ALLOW_ALL_USERS
  → 默认：拒绝
```

关键推论：**什么都不配 = 所有人被拒**。网关启动时会警告 `No user allowlists configured. All unauthorized users will be denied.`。生产环境永不设 `GATEWAY_ALLOW_ALL_USERS=true`，配显式 allowlist + DM pairing 即可。

**④ 上线前复查**（对应官方生产部署清单的核心项）：跑 `docker version` 确认后端健康、用 `hermes config show` 核对 `approvals` / `disabled_toolsets` / `skills.write_approval` 生效、定期 `hermes config edit` 审 `command_allowlist`、检查 `~/.hermes/logs/` 有无未授权访问、`hermes update` 保持补丁（来源 Sec）。配完跑一遍 `hermes doctor`，以它的输出为最终准绳。

## 本章小结

- tool / skill / memory 三者可跨会话，但分工不同：tool 是**可执行能力**，skill 是**程序性知识文档**（菜谱，靠调工具落地），memory 是 **facts**；skill 引用工具必须是原生 Hermes 工具或显式写明接入的 MCP server（来源 FAQ / S6）。
- `skills.write_approval: true` 把 agent 的每次 `skill_manage` 写操作 stage 到 `~/.hermes/pending/skills/`，用 `/skills approve|reject` 审查；`skills.guard_agent_created` 是独立的内容扫描器，默认关（来源 S11）。
- `agent.disabled_toolsets` 在平台配置之后生效，**任何平台都移除**，是「一处关、处处关」的全局总闸（来源 S11）。
- 审批纵深：`approvals.mode` 三档（smart/manual/off）、YOLO 三入口（`--yolo`、`/yolo`、`HERMES_YOLO_MODE=1`）、hardline blocklist 永不可覆盖；容器后端整体跳过危险命令检查（来源 Sec）。
- 防泄漏基线：`HERMES_SAFE_MODE`（排障最小化）、`HERMES_WRITE_SAFE_ROOT`（写操作硬沙箱，勿随意加进 `.env`）、`HERMES_REDACT_SECRETS`（默认 true 自动打码）、`HERMES_MAX_ITERATIONS`（默认 500）；`execute_code` 与 MCP stdio 子进程都剥离密钥（来源 S5 / S6 / Sec）。
- Docker 检查清单：密钥只落 `~/.hermes/.env` 并 `chmod 600`、`docker_forward_env` 留空、容器资源设上限、网关授权默认拒绝，最后以 `hermes doctor` 复核。

到这里，整本《Hermes Tool 配置指南》的工具、网关、MCP、自定义与安全基线就齐了。下一环节会把六个章节组装成完整的 Obsidian 分册，并统一加上前后导航与 frontmatter。
