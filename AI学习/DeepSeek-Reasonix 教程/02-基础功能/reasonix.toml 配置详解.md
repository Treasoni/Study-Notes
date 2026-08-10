---
title: reasonix.toml 配置详解
topic: DeepSeek-Reasonix 配置教程
type: reference
difficulty: 基础
tags: [DeepSeek-Reasonix, reasonix.toml, 配置, providers, agent, API-Key]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
sources:
  - R1: "DeepSeek-Reasonix 官方仓库 README（配置入口总览）(esengine, 2026-08) https://github.com/esengine/DeepSeek-Reasonix"
  - R2: "配置指南 GUIDE.zh-CN（setup 与配置体系）(esengine, 2026-08) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/GUIDE.zh-CN.md"
  - R3: "配置文件路径与优先级 CONFIG_PATHS.zh-CN (esengine, 2026-08) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/CONFIG_PATHS.zh-CN.md"
  - R4: "配置示例 reasonix.example.toml（字段权威来源，262 行）(esengine, 2026-08) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/reasonix.example.toml"
  - R5: "官方 CLI 参考 main-v2（CLI.zh-CN.md，废弃字段与 --max-steps 替代）(esengine, 2026-08) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/CLI.zh-CN.md"
concepts:
  - reasonix-toml
  - providers
  - agent
  - permissions
  - sandbox
  - config-priority
  - api-key-security
  - hook
related_notes:
  - "[[DeepSeek-Reasonix 使用指南]]"
  - "[[DeepSeek-Reasonix 权限模式指南]]"
  - "[[DeepSeek-Reasonix 模型与运行模式]]"
  - "[[DeepSeek-Reasonix 前缀缓存与成本优化]]"
  - "[[DeepSeek-Reasonix 沙箱与安全]]"
  - "[[DeepSeek-Reasonix MCP 使用指南]]"
---

# reasonix.toml 配置详解

> [!info] 文档定位
> 本文是 DeepSeek-Reasonix 的配置核心章，逐一解释 `reasonix.toml` 的字段、配置优先级与 API Key 安全模型。它属于「02-基础功能」层，也是全系列中「配置字段细节」的唯一权威出处——其他章节只引用、不复制。建议在读完[[DeepSeek-Reasonix 使用指南]]、完成安装与 `reasonix setup` 之后阅读；阅读本文后再进入权限（第 6 章）与运行模式（第 7 章）会更顺。文中字段名与示例值均取自官方 `reasonix.example.toml`，未超出其信源范围。

本文回答一个核心问题：**当你拿到一个陌生项目或想调优自己的 `reasonix.toml` 时，应该按什么顺序、在哪里改哪个字段？** 先建立配置体系与优先级的心智模型，再逐节过字段。

## 一、配置体系与优先级

Reasonix 的配置分成两层文件，叠加出四层取值来源：

| 层级 | 位置 | 说明 |
|------|------|------|
| 命令行 flag | 每次启动传入 | 临时覆盖，优先级最高 |
| 项目级 | `./reasonix.toml` | 跟随仓库，可提交给团队共享 |
| 用户级 | `~/.reasonix/config.toml`（macOS/Linux）/ `%AppData%\reasonix\`（Windows） | 个人偏好与凭据声明 |
| 内置默认 | 程序内置 | 兜底，优先级最低 |

解析顺序严格为：**flag > `./reasonix.toml` > 用户全局配置 > 内置默认**。同一个键出现在更高层级时，直接盖过低层级。

> [!tip] 大白话
> 把配置优先级想成「现场口头指令 > 项目组规定 > 公司制度 > 行业惯例」：命令行参数是现场指令，最优先；项目里的 `reasonix.toml` 是项目组规定；全局 `config.toml` 是公司制度；内置默认是行业惯例。
> 所以当你改了全局配置却「不生效」时，先检查是不是项目里的 `reasonix.toml` 或命令行参数把全局配置盖掉了——多半不是没保存，而是层级更低。

TOML 结构总览（顶层 + 若干节）：

```toml
default_model = "deepseek"     # 顶层：默认 provider（名或 "provider/model"）
# language = "zh"              # 顶层：界面/输出语言（可选）

[[providers]]                  # 可重复：声明一个 provider 端点
[agent]                        # 执行器行为：温度、压缩、双模型
[environment]                  # 运行环境开关
[tools]                        # 工具集与超时
[permissions]                  # 权限兜底与 deny/allow 规则
[sandbox]                      # 工作区沙箱
[skills]                       # 技能路径与开关
[[plugins]]                    # 可重复：MCP/外部 stdio 插件
[ui]                           # TUI 主题与用量显示
[notifications]                # 通知开关
[bot]                          # QQ/飞书/微信多通道机器人
```

## 二、顶层与 `[[providers]]`

`[[providers]]` 是配置的入口：Reasonix 的 provider 体系是**插件式声明**，内核没有硬编码模型。你可以声明多个 provider，并用顶层 `default_model` 指定默认。

```toml
default_model = "deepseek"           # provider 名，或 "provider/model"

[[providers]]
name = "deepseek"                    # 唯一标识，default_model 引用它
kind = "openai"                      # openai|anthropic，决定请求协议
base_url = "https://api.deepseek.com"
models = ["deepseek-v4-flash", "deepseek-v4-pro"]   # 多模型共享同一端点
default = "deepseek-v4-flash"        # 该 provider 的默认模型
api_key_env = "DEEPSEEK_API_KEY"     # 环境变量名（不是密钥本身！）
context_window = 1000000
effort = "high"                      # high|max；DeepSeek 思考恒开

[[providers]]
name = "claude"
kind = "anthropic"                   # 走 Messages API，不发送 temperature
model = "claude-opus-4-8"            # 单模型用 model 而不是 models
api_key_env = "ANTHROPIC_API_KEY"
context_window = 1000000
thinking = "adaptive"
effort = "high"                      # low|medium|high|xhigh|max
```

字段逐项说明：

- `name`：provider 标识，`default_model` 与 `--model` 都引用它。
- `kind`：`openai` 或 `anthropic`。`anthropic` 走 Messages API，且**不发送 `temperature`**。
- `base_url`：端点地址。**单模型**共用端点用 `model = "..."`；**多模型**共享同一端点用 `models = [...]`。这两种写法互斥地表达模型集合。
- `default`：该 provider 内的默认模型。
- `api_key_env`：**只存环境变量名**，不存真实密钥（见第六节安全模型）。
- `context_window`：上下文窗口大小，单位 token。
- `effort`：推理深度。DeepSeek 档位 `high|max`（思考恒开）；Anthropic 兼容端点档位 `low|medium|high|xhigh|max`。`effort` 字段与 `/effort`、`--effort` 的覆盖关系在第 7 章展开。

可选字段：

- `reasoning_protocol`：`auto|deepseek|openai|none`，控制推理内容协议。
- `supported_efforts`、`default_effort`：声明该 provider 支持的 effort 档位与默认值。
- `auth_header`：布尔值，供 Bearer 鉴权网关使用。
- `prices`：自定义计价（覆盖内置单价，成本测算见第 9 章）。

Anthropic 兼容端点示例——用 DeepSeek 的 Anthropic 兼容网关：

```toml
[[providers]]
name = "deepseek-anthropic"
kind = "anthropic"
base_url = "https://api.deepseek.com/anthropic"
model = "deepseek-v4-pro"
api_key_env = "DEEPSEEK_API_KEY"
```

> [!tip] 大白话
> 把 `api_key_env = "DEEPSEEK_API_KEY"` 想成「保险箱上贴的标签，只写着钥匙在哪只抽屉」，而真实密钥放在全局 `.env` 保险箱里。
> 所以就算你把 `reasonix.toml` 提交到仓库或发给同事，里面也不含任何真实密钥——泄露面被压缩到全局那一个文件。

## 三、[agent]

`[agent]` 控制执行器（干活的那个模型）的行为。核心是温度、恢复模型与四个上下文压缩比例。

```toml
[agent]
# system_prompt / system_prompt_file   # 自定义系统提示，二选一（文件版用于长提示）
temperature = 0.0                       # 采样温度，Anthropic 协议端点不发送
# recovery_model = ""                   # 恢复/兜底模型（留空走默认）
# reasoning_language = "auto"           # auto|zh|en
soft_compact_ratio = 0.5                # 缓存优先压缩提示
tool_result_snip_ratio = 0.6            # 裁剪工具结果
compact_ratio = 0.8                     # 完整压缩阈值
compact_force_ratio = 0.9               # 强制压缩阈值
# planner_model = "deepseek-pro"        # 双模型协同：规划器
# subagent_model = "deepseek-pro"       # 子代理默认模型
# subagent_models = { review = "deepseek-pro", security_review = "deepseek-pro" }
# max_subagent_concurrency = 6          # 子代理并发上限
# max_parallel_writers = 3              # 并行写文件上限
# output_style = "explanatory"          # explanatory|learning|concise
```

要点：

- `system_prompt` 与 `system_prompt_file` 二选一，后者适合较长的提示内容。
- 四个比例 `soft_compact_ratio → tool_result_snip_ratio → compact_ratio → compact_force_ratio` 是触发层级越来越重的上下文压缩阈值：先轻量压缩提示词，再裁剪工具结果，接着完整压缩，最后强制压缩。它们直接关系前缀缓存命中率，机制在第 9 章展开。
- `planner_model` 一行即可启用「执行器 + 规划器」双模型协同：规划器只看记忆与只读研究工具，写入工具只给执行器（语义见第 7 章）。
- `subagent_model` 设置所有子代理默认模型；`subagent_models` 可对 `review`、`security_review` 等角色单独指定。
- `output_style` 控制回答风格：`explanatory`（解释型）/ `learning`（学习型）/ `concise`（精简型）。

> [!tip] 大白话
> 把四个压缩比例想成「衣柜整理的四个动作」：`soft_compact_ratio` 是先把不常穿的衣服叠好（轻量压缩提示词）、`tool_result_snip_ratio` 是把过长袖口折起来（裁剪工具结果）、`compact_ratio` 是换季彻底收纳（完整压缩）、`compact_force_ratio` 是衣柜爆了必须扔（强制压缩）。
> 所以它们是越来越重的四档阈值，理解触发顺序能帮你保住前缀缓存命中率、少花冤枉钱。

> [!note] 补充
> 关于 `effort` 字段、`planner_model` 双模型协同与 profile 三档的完整运行语义，见[[DeepSeek-Reasonix 模型与运行模式]]。本文只讲字段写在哪、取值有哪些，不展开运行机制。

## 四、[environment] / [tools] / [permissions]

这三个节分别是运行环境开关、工具集与超时、权限兜底规则。

```toml
[environment]
enabled = true                  # 是否启用环境能力
offline = false                 # 离线模式开关

[tools]
enabled = []                    # 空数组 = 启用全部内置工具；可列出子集
bash_timeout_seconds = 120      # 单个 bash 命令超时
mcp_startup_timeout_seconds = 30   # MCP server 启动超时
mcp_call_timeout_seconds = 300     # MCP 单次调用超时

[permissions]
mode = "ask"                    # ask|allow|deny 兜底
deny  = ["Bash(rm -rf*)", "Bash(git push*)"]   # 黑名单：永远禁止
allow = ["Bash(go test:*)"]     # 白名单：放行
```

要点：

- `[tools] enabled = []` 表示「不限制」，启用全部内置工具；想收紧就列出允许的子集。
- MCP 两类超时（启动 30s / 调用 300s）在接入慢启动的 MCP server 时经常需要调大，具体见第 8 章。
- `[permissions] mode` 是**兜底**规则（`ask|allow|deny`），配合 `deny`/`allow` 规则使用。规则语义（6 种权限模式、交互切换、fail-closed）在第 6 章完整展开，这里只讲书写位置。

> [!tip] 大白话
> 把 `[permissions]` 想成一张门禁卡：`mode = "ask"` 是默认规则「进门要刷卡审批」，`deny` 是黑名单（永远不放行），`allow` 是白名单（放行）。
> 所以黑名单永远压过白名单——哪怕你在命令行临时用 `--allowed-tools` 放行了某个工具，配置里的 `deny` 照样拦住（详见[[DeepSeek-Reasonix 权限模式指南]]）。

## 五、[sandbox] / [skills] / `[[plugins]]` / [ui] / [notifications] / [bot] 概览

这些节在示例文件中大多以注释形式给出，本节做速览；详细语义按分工散落在后续章节。

```toml
# [sandbox]
# workspace_root = ""            # 沙箱工作区根目录
# allow_write = ["/tmp"]         # 可写目录白名单
# forbid_read = ["${HOME}/.ssh"] # 禁读目录（保护敏感路径）
# bash = "enforce"               # enforce|off；Windows 强制 off
# network = true                 # 沙箱网络开关

# [skills]
# paths = ["~/my-skills", "../shared/skills"]
# excluded_paths = ["~/.agents/skills"]
# disable_implicit_invocation = true
# disabled_skills = ["review"]

# [[plugins]]                    # MCP/外部 stdio 插件
# name = "example"
# command = "reasonix-plugin-example"

[ui]
theme = "auto"                   # auto|dark|light
show_turn_usage = true           # 显示每次请求 token 与费用

[notifications]
enabled = false
turn_done = true
approval_request = true

# [bot]                          # QQ/飞书/微信多通道机器人，见 reasonix.example.toml
```

分工边界：

- `[sandbox]`：工作区沙箱字段（`workspace_root` / `allow_write` / `forbid_read` / `bash` / `network`），完整语义见[[DeepSeek-Reasonix 沙箱与安全]]。
- `[skills]`：技能路径、排除路径与禁用列表，扩展机制见第 12 章。
- `[[plugins]]`：声明 MCP/外部 stdio 插件，`name` + `command`，使用与 MCP 接入见第 8 章，扩展开发见第 12 章。
- `[ui]` 与 `[notifications]`：界面主题、单轮 token/费用显示与通知开关，可直接按需设置。
- `[bot]`：多通道机器人配置入口，完整字段在官方 `reasonix.example.toml` 中，本系列不展开。

## 六、API Key 安全模型

这是配置里最容易被误用的一环。Reasonix 的密钥管理遵循「**声明与凭据分离**」：

1. **config 只存变量名**：`reasonix.toml` 里写 `api_key_env = "DEEPSEEK_API_KEY"`，这是环境变量名，不是密钥本身。
2. **真实值只在全局 `.env`**：密钥放在全局 `<Reasonix home>/.env`（macOS/Linux 为 `~/.reasonix/`，Windows 为 `%AppData%\reasonix\`），由 `reasonix setup` 统一管理。
3. **项目 `.env` 不导入 provider key**：项目根目录的 `.env` 只作为 MCP/plugin 的 `${VAR}` 展开来源，Reasonix **不会**从项目 `.env` 导入 provider 密钥。
4. **运行时禁读边界**：Reasonix 会从工具子进程中移除已保存的凭据，避免子进程读走密钥。

> [!warning] 坑点：别把密钥写进 config
> 不要把真实 API Key 直接写进 `reasonix.toml` 的 `api_key_env` 或项目 `.env`。前者只认环境变量名，后者不会导入 provider key——写错了只会让连接测试失败，且密钥一旦进仓库就再也删不干净。

## 七、Hooks 位置

Hooks **不在** `reasonix.toml` 里。Reasonix 沿用了 Claude Code 的 `settings.json` 模型，分两处：

| 作用域 | 位置 |
|--------|------|
| 全局 | `<Reasonix home>/settings.json` |
| 项目 | `<project>/.reasonix/settings.json` |

写 Hook 时注意选择正确的文件：个人通用逻辑放全局，跟随仓库的团队逻辑放项目。具体 Hook 配置条目以官方 settings.json 文档为准。

## 八、常见坑

1. **废弃字段会被静默清理**：`agent.auto_plan`、`agent.max_steps` 以及 MCP 的旧字段会被 Reasonix **忽略，并在保存时自动移除**。不要照抄旧教程里的这些字段；改用 `--max-steps` 启动参数。

> [!warning] 坑点：废弃字段
> `agent.auto_plan`、`agent.max_steps` 已被移除，保存配置时会被忽略并清理。升级后若发现「配置里写了却不生效」，先怀疑是不是这类废弃字段，改用 `--max-steps`。

2. **Windows 沙箱差异**：Reasonix 不在 Windows 提供 OS 级 Bash 沙箱，`[sandbox] bash = "enforce"` 在 Windows 上会被解析为 `off`；而在无沙箱环境下 `enforce` 又会直接拒绝 bash 执行（macOS 用 Seatbelt、Linux 用 bubblewrap）。

> [!warning] 坑点：Windows 沙箱
> Windows 上把 `bash = "enforce"` 写进配置不会报错，但实际被当成 `off` 处理——不要指望它提供和 macOS/Linux 同等的隔离。替代策略见[[DeepSeek-Reasonix 沙箱与安全]]。

3. **优先级排查**：改配置「不生效」时，按 flag → 项目 → 全局 → 内置默认的顺序从上往下找覆盖者，十有八九是更高层级里有同键配置。

## 常见问题

**Q：我改了 `reasonix.toml` 但没生效，可能是什么原因？**
A：先检查配置优先级：命令行 flag 盖过项目 `reasonix.toml`，项目盖过全局 `~/.reasonix/config.toml`，全局盖过内置默认。如果存在同名键，永远是高一层级生效。

**Q：API Key 到底该放在哪？**
A：config 里只写 `api_key_env = "变量名"`；真实密钥放在全局 `<Reasonix home>/.env`（由 `reasonix setup` 管理）。项目 `.env` 只作 MCP/plugin 的 `${VAR}` 展开，不会导入 provider key。

**Q：Hooks 在哪个文件配置？**
A：不在 `reasonix.toml`。全局 Hook 在 `<Reasonix home>/settings.json`，项目 Hook 在 `<project>/.reasonix/settings.json`。

**Q：`agent.max_steps` 还能用吗？**
A：不能。`agent.auto_plan`、`agent.max_steps` 与 MCP 旧字段已被废弃，保存时会被忽略并移除，请改用 `--max-steps` 启动参数。

## 相关文档

- [[DeepSeek-Reasonix 使用指南]]：安装与 `reasonix setup` 首次配置
- [[DeepSeek-Reasonix 权限模式指南]]：`[permissions]` 的 6 种模式与规则语义
- [[DeepSeek-Reasonix 模型与运行模式]]：`effort`、profile、双模型协同
- [[DeepSeek-Reasonix 前缀缓存与成本优化]]：压缩参数与缓存命中率
- [[DeepSeek-Reasonix 沙箱与安全]]：`[sandbox]` 与凭据保护细节
- [[DeepSeek-Reasonix MCP 使用指南]]：`[[plugins]]` 与 MCP 配置

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/docs/GUIDE.zh-CN.md`：官方配置指南
- `docs/CONFIG_PATHS.zh-CN.md`：配置文件路径与优先级
- `main-v2/reasonix.example.toml`：官方配置示例（字段权威来源，262 行）

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（基础功能篇第 5 章，配置为核心章） |
