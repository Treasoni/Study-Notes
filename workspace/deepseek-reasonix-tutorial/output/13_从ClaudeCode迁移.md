---
title: 从 Claude Code 迁移到 DeepSeek-Reasonix
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 进阶
tags: [DeepSeek-Reasonix, Claude Code, 迁移, 成本对比, 配置迁移, reasonix]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# 从 Claude Code 迁移到 DeepSeek-Reasonix

> [!info] 文档定位
> 本文是 DeepSeek-Reasonix 的迁移章（03-进阶应用篇第 13 章）：面向已在用 Claude Code、想评估或切换 Reasonix 的用户，讲清动机、成本账、配置映射、权限模式差异、MCP/技能资产迁移与实操步骤。全程以「迁移前先建对照表、迁移后跑验证清单」为主线，让你迁得过去、也迁得明白。关联：[[DeepSeek-Reasonix 是什么]]、[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix 权限模式指南]]、[[DeepSeek-Reasonix MCP 使用指南]]。

本文回答的核心问题：**我每天开着 Claude Code，凭什么要（或不要）换到 Reasonix？** 以及如果真的换，**我现有的权限习惯、MCP server、技能资产要怎么搬？**

## 一、为什么迁：先算清楚「迁移动机」

迁移不是目的，解决痛点是目的。Reasonix 相对 Claude Code 的主打卖点与适用人群：

| 动机 | Reasonix 的回应 | 谁的痛点 |
|------|----------------|----------|
| **成本** | DeepSeek API 缓存价约 ¥0.02/1M token vs 未缓存 ¥1/1M（约 50 倍单价差）；项目自报长会话命中率 94%–99.8%，长会话输入成本约压到 1/5 | 长会话、高频使用、对账单敏感的用户 |
| **前缀缓存工程化** | 三区上下文设计（CacheFirstLoop）把「不可变前缀 / 只追加日志 / 易变草稿」分离，把命中率变成工程约束而非运气 | 用过 `claude` 但发现长会话成本飘忽不定的用户 |
| **模型选择** | 双模型协同（规划/执行）与 effort 分档，支持非 Claude 模型 | 想用 DeepSeek、或不想被单一模型绑定 |

但别只看优点，先泼两盆冷水：

1. **它不是 Claude Code 的「drop-in 替代」**：命令、权限模式、配置路径都有差异（下文逐项对照），迁移需要花时间建映射与验证。
2. **数据口径要清醒**：成本对比里 99.8% 命中率、$61→$12 这类数字多为**项目自报**（详见[[DeepSeek-Reasonix 前缀缓存与成本优化]]第三节口径表），做决策时用「用户实测对账」的口径更稳妥。

> [!tip] 大白话
> 迁移像「换一家健身房」：别因为广告上的「月卡便宜一半」就冲动转会，先确认**它有你天天用的那台器械**（你依赖的命令、MCP、权限习惯），再算总账。省下的会费是成本，换馆搬家花的时间也是成本。

## 二、成本账：缓存是核心杠杆

Reasonix 的成本优势几乎全部建立在 DeepSeek 前缀缓存上，核心数字（官方口径，详见[[DeepSeek-Reasonix 前缀缓存与成本优化]]）：

| 项目 | 数值 | 性质 |
|------|------|------|
| 缓存命中输入单价 | 约 ¥0.02/1M token | 官方口径 |
| 未缓存输入单价 | 约 ¥1/1M token | 官方口径 |
| 单价差 | 约 50 倍 | 官方口径 |
| 长会话命中率 | 94%–99.8% | 项目自报 |
| 无纪律 agent 命中率基线 | <20% | 官方口径 |
| 典型重度用户月成本 | 约 $150–250/月（Claude Code 侧） | 官方口径 |

**一句话：省不省钱，全看命中率；命中率全看前缀稳不稳。** 如果只是偶尔跑短会话、前缀没建立起来，成本优势就发挥不出来。所以迁移前先问自己：我的使用模式是「长会话、上下文高度复用」吗？是，才吃得到缓存红利。

> [!tip] 大白话
> 把缓存优惠想成「会员积分」：你要**长期、高频在同一家店消费**，积分才攒得动、才换得到折扣；偶尔路过买瓶水，积分形同虚设。Reasonix 的成本账同理——长会话复用越多，命中率越高，才越划算。

## 三、配置映射：从 `claude` 到 `reasonix`

迁移的第一关是「我原来的配置，新家对应在哪」。核心映射表：

| Claude Code 概念 | Reasonix 对应 | 差异要点 |
|------------------|---------------|----------|
| `claude` 命令 | `reasonix code .`（TUI 入口） | 命令名不同，入口习惯需重建 |
| `claude -p` | `reasonix run` | 无头模式，参数不完全等价 |
| settings.json（全局 + 项目） | `<Reasonix home>/settings.json` + `<project>/.reasonix/settings.json` | hooks 位置对齐，但路径不同 |
| `.claude/` 目录 | `.reasonix/` 目录 | 项目级目录改名 |
| settings.json 里的 hooks | 同样在 settings.json（见[[DeepSeek-Reasonix 插件与扩展开发]]） | 事件回调机制对齐 |
| MCP 配置 `mcpServers` | `[[plugins]]`（本地 stdio）或 ACP `mcpServers`（MCP over ACP） | 入口有两处，见[[DeepSeek-Reasonix MCP 使用指南]] |
| Ask / Auto / Yolo | `ask` / `auto` / `yolo`（`tool_approval`），以及权限模式 `ask` / `auto` / `manual` / `yolo` | 权限语义基本对齐，但多了 `manual`，且 ACP 里经 `configId` 下发 |

**迁移的核心教训：别指望「复制粘贴就生效」。** 目录名、配置路径、命令名都变了，迁完要跑一遍验证清单（见第六节），而不是凭「感觉能用」。

> [!warning] 权限模式不是完全一比一
> Claude Code 的 Ask/Auto/Yolo 是本地键盘循环；Reasonix 除了命令行的权限模式，还通过 ACP 协议把审批暴露给编辑器（`session/set_config_option` + `session/request_permission`）。如果你重度依赖「终端里按 `y` 审批」，换过来要适应新的交互入口。详见[[DeepSeek-Reasonix 权限模式指南]]与[[DeepSeek-Reasonix ACP 协议指南]]。

## 四、迁移步骤：建对照表 → 迁配置 → 迁资产 → 验证

### 第 1 步：盘点现状，建对照表

把「现在天天用的东西」列全：常用命令、settings.json hooks、MCP server、skills、权限习惯。逐项对照第三节的映射表，标出「能直接迁 / 要改写法 / 没有对应」。

### 第 2 步：迁移配置

- 复制全局 settings.json 到 `<Reasonix home>/settings.json`，项目配置到 `<project>/.reasonix/settings.json`，**逐项核对 hooks 语义**。
- 在 `reasonix.toml` 里配置 provider 与模型：`[[providers]]`（`kind = "openai"` + `base_url` + `models` + `default` + `api_key_env`），详见[[reasonix.toml 配置详解]]。
- 把 API Key 放进全局 `<Reasonix home>/.env`（不是项目 `.env`，项目 `.env` 只作 `${VAR}` 展开来源，不导入 provider key）。

### 第 3 步：迁移 MCP 与技能资产

- **MCP**：本地 stdio server → `[[plugins]]`（`name` + `command`）；远程/会话级 → ACP `mcpServers`。`env`/`headers` 用 `[{"name":"...","value":"..."}]` 形状，`${VAR}` 由项目 `.env` 展开。详见[[DeepSeek-Reasonix MCP 使用指南]]。
- **skills**：加载目录与禁用在 `reasonix.toml` 的 `[skills]` 里声明（`paths` / `excluded_paths` / `disabled_skills` / `disable_implicit_invocation`），会话内 `/skills` 查看。详见[[DeepSeek-Reasonix 插件与扩展开发]]。
- **插件/扩展**：版本化插件包经 `[[plugins]]` 声明启动命令；Sidecar 扩展协议以官方 `EXTENSION_PROTOCOL.zh-CN.md` 为准。

### 第 4 步：跑验证清单（最小可用集）

1. 启动 `reasonix code .` 能进 TUI，模型已连通（provider key 生效）。
2. `/help` 里能看到你依赖的核心命令；迁移前用不到的冷门命令先不管。
3. MCP server 能 `list` 到、`inspect` 通过、实际调用一次成功（记得调 `mcp_startup_timeout_seconds` 应对慢启动）。
4. 权限模式下你的工作流能走通：日常轮次能完成，需要审批的动作有入口。
5. 跑一个真实小任务，确认 hooks 事件回调触发、结果正常。

> [!tip] 大白话
> 迁移验证像「搬新办公室后先试电」：别等住进去一周才发现插座没电。第 4 步就是搬家当天的「开灯、插电、拨号」三连——能亮、能充、能通，才算真正搬完。

## 五、常见坑

1. **把项目 `.env` 当 provider key 入口**。项目 `.env` 只作 `${VAR}` 展开来源，provider 凭据只在全局 `<Reasonix home>/.env`。
2. **配置文件路径想当然**。hooks 在 settings.json（全局 `<Reasonix home>/settings.json` + 项目 `<project>/.reasonix/settings.json`），插件在 `reasonix.toml`，别混。
3. **命令名照抄 `claude`**。入口是 `reasonix code .`，无头是 `reasonix run`；`claude -p` 的参数不等价，`reasonix run` 有自己的 `--auto` / `--output-format` / `--events-jsonl` 约定（见[[DeepSeek-Reasonix 自动化与 CI]]）。
4. **权限模式当一比一**。多了 `manual` 模式；无头默认 fail-closed（`ask/manual` 下拒绝写操作），CI 里必须显式 `--auto`。
5. **拿「项目自报」成本数据做决策**。$61→$12、99.8% 命中是项目自报口径；真实对账看 [[DeepSeek-Reasonix 前缀缓存与成本优化]] 第三节的 #7907 数据，别被宣传口径带偏。
6. **版本差异导致命令找不到**。v1 与 main-v2 的 CLI 文档命令列表不同，实时权威是应用内 `/help`。

---

一句话收束：迁移 = 动机（成本红利在缓存、在长会话）+ 对照表（命令、配置路径、权限、MCP、skills 逐项建映射）+ 验证清单（能启动、能连通、能跑通小任务）。迁完别急着删 Claude Code，先并行跑两周。

## 常见问题

**Q: Reasonix 真的能比 Claude Code 省钱吗？**
A: 大概率，但取决于使用模式。成本红利建立在 DeepSeek 前缀缓存上：长会话、上下文高度复用才吃得到（官方口径缓存约 10% 计费、单价差约 50 倍）。偶尔短会话、前缀建立不起来时，优势会大打折扣。做决策用用户实测对账口径（见成本章节），别信项目自报宣传数字。

**Q: 我的 Claude Code MCP server 能直接搬过来吗？**
A: 能，但要换入口。本地 stdio server 用 `reasonix.toml` 的 `[[plugins]]`（`name` + `command`），远程/会话级用 ACP 的 `mcpServers`。`env`/`headers` 用 `[{"name":"...","value":"..."}]` 形状。

**Q: Claude Code 的 Ask/Auto/Yolo 在 Reasonix 里怎么对应？**
A: 对应 `tool_approval` 的 `ask` / `auto` / `yolo`，另外还有权限模式 `manual`。注意无头模式默认 fail-closed（`ask/manual` 下拒绝写操作），CI 场景要显式 `--auto`。

**Q: 迁移后怎么确认没迁漏？**
A: 按最小可用集验证：能进 TUI、provider key 生效、MCP 能 list/inspect/调用、权限工作流走通、hooks 触发。并行跑两周再决定是否停用 Claude Code。

## 相关文档

- [[DeepSeek-Reasonix 是什么]]：动机与定位（为什么叫「便宜到能常开」）
- [[reasonix.toml 配置详解]]：`[[providers]]`、`[skills]`、配置路径与优先级
- [[DeepSeek-Reasonix 权限模式指南]]：ask/auto/manual/yolo 与 fail-closed 语义
- [[DeepSeek-Reasonix MCP 使用指南]]：`[[plugins]]` 与 MCP over ACP 接入
- [[DeepSeek-Reasonix 前缀缓存与成本优化]]：成本账与命中率口径
- [[DeepSeek-Reasonix 自动化与 CI]]：`reasonix run` 无头模式与 CI 集成

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/docs/CLI.zh-CN.md` 与 `v1/docs/CLI-REFERENCE.md`：`reasonix code` / `reasonix run` 命令
- `main-v2/docs/GUIDE.zh-CN.md` 与 `docs/CONFIG_PATHS.zh-CN.md`：settings.json 与 hooks 位置
- `main-v2/reasonix.example.toml`：`[[providers]]` / `[skills]` / `[[plugins]]` 声明示例
- 官方 ARCHITECTURE.md：成本口径与缓存设计（素材 5.1 官网首页）
- 对齐 PR（命令与 Claude Code 对齐）：https://github.com/esengine/DeepSeek-Reasonix/pull/6431

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（进阶应用篇第 13 章，从 Claude Code 迁移） |
