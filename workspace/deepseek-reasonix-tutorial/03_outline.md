# DeepSeek-Reasonix 配置教程 - 大纲

> 笔记类型：实战配置教程（分册系列，对齐 `AI学习/Claude Code 教程/` 结构：分册目录 + MOC + 速查 + Callout）
> 系列规模：14 篇 / 4 层（01-入门 / 02-基础功能 / 03-进阶应用 / 04-高级功能）
> 目标读者：熟悉 Claude Code 的用户（省略通用概念铺垫，侧重对比与迁移）
> 预计总篇幅：约 39,000 字
> 素材唯一事实来源：`02_deep_research.md`（写作时不得超出其信源范围）

---

## 系列概览

- **定位**：以「配置为中心 + 对比迁移为中心 + 成本优化为中心」展开，面向已熟练使用 Claude Code、想上手或迁移到 DeepSeek-Reasonix 的用户。
- **四层递进**：入门（是什么 + 怎么装怎么跑）→ 基础（CLI/会话/配置/权限四大底座）→ 进阶（模型、MCP、成本、CI）→ 高级（ACP、插件、迁移、安全）。
- **写作基调**：以官方文档（README.zh-CN / GUIDE.zh-CN / reasonix.example.toml / CLI-REFERENCE(v1) / CLI.zh-CN(main-v2) / ACP.md / ARCHITECTURE.md）为准；社区实测（PR #6431、Issue #7907、智源报道）只作为「实测数据」引用并标注出处，不与官方断言混写。
- **贯穿全系列的三条关键澄清**（各章按分工出现，不重复展开）：
  1. **Profile 三档 ≠ smart/fast/max**：官方工作模式是 `economy|balanced|delivery`，`smart/fast/max` 是社区对 `/effort` 的俗称（正文在 03 第 7 章，其他章只做指认）。
  2. **v1 与 main-v2 文档命令列表不同**：以应用内 `/help`、`/keys` 为实时权威（正文在 02 第 4 章，其他章涉及命令时标注版本）。
  3. **成本实测数据出处**：官方口径（无纪律 <20% 命中、$150–250/月）、Issue #7907 对账（99.6%、¥1.37/全天、¥0.00869/请求、-55~60%）、智源报道（99.82%、$61→$12）（正文在 03 第 9 章与 04 第 13 章）。
- **无重叠边界原则**：每章在「内容边界」中写明负责范围；配置字段细节集中在 02 第 5 章，其他章只引用不复制；命令细节集中在 02 第 3 章；权限细节集中在 02 第 6 章；成本数据集中在 03 第 9 章、04 第 13 章仅做横向对比引用。

---

## 01-入门

> 篇幅档位：每篇 1500–2500 字。目标：让读者装得上、跑得起来、知道这工具是什么。

### 第 1 章 DeepSeek-Reasonix 使用指南

- **目标**：从零安装到跑起第一个会话，并给出一张日常速查表。
- **篇幅**：约 2000 字
- **结构**：
  - 一、安装：4 条路径（A. CLI：npm + brew 两条子命令；B. npx 免安装临时用；C. 桌面端 dmg/exe/deb；D. VS Code 扩展——先装 CLI、扩展启动本地 `reasonix acp` 后端）；补充小节：源码构建（`git clone` + `make build`，可选）
  - 二、首次配置 `reasonix setup`：向导作用、交互保存逻辑（暂存到「保存并退出」统一生效）、API Key 存储位置（config 只存 `api_key_env` 变量名，真实值在全局 `<Reasonix home>/.env`）、连接测试与默认模型
  - 三、第一个会话：`reasonix code .` 进入 TUI → `/init` 生成 REASONIX.md/AGENTS.md → 跑一个简单任务 → 用 `/status`、`/cost` 查看状态
  - 四、日常速查表：核心命令表（`reasonix`/`code`/`chat`/`run`/`setup`/`doctor`/`upgrade`/`stats`/`commit`）+ 常用斜杠命令 + 快捷键
  - 五、常见坑：国内网络/镜像安装、API Key 未配置、第一次跑不起来时用 `reasonix doctor`
- **内容边界**：只讲「装、配、跑、查」，不展开 CLI 全量参数（见第 3 章）、不展开配置全字段（见第 5 章）、不展开前缀缓存原理（见第 2 章/第 9 章）。
- **素材引用**：02_deep_research.md 第二节（安装与首次配置，2.1/2.2）、第四节（4.1 核心命令表）
- **代码示例**：安装命令（`npm i -g reasonix`、`brew install esengine/reasonix/reasonix`、`npx reasonix code`）、`reasonix setup`、`reasonix doctor`、`reasonix code .`
- **双链建议**：[[DeepSeek-Reasonix 是什么]]、[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix CLI 完整参考]]

### 第 2 章 DeepSeek-Reasonix 是什么

- **目标**：建立正确心智模型——它是什么、设计哲学、前缀缓存核心原理（概览）、与 Claude Code 的关系。
- **篇幅**：约 2000 字
- **结构**：
  - 一、产品定位：DeepSeek 原生终端 AI 编程 agent，MIT 开源，单 Go 静态二进制（CGO_ENABLED=0），本地引擎四入口（终端/桌面/浏览器/ACP 编辑器），定位「可以一直开着跑的编码 Agent」
  - 二、设计哲学：计划模式 + 权限 + 工作区沙箱 + 逐轮 checkpoint，保证长时自治运行可读、可撤销
  - 三、前缀缓存原理（概览层）：精确字节前缀匹配、命中按未命中 ~10% 计费、三区上下文设计（不可变前缀 / 只追加日志 / 易变草稿）、无纪律 agent 命中率 <20%（细节在第 9 章展开）
  - 四、与 Claude Code 的关系（概览）：同类工具非替代品、命令/概念大量对齐（PR #6431）、核心差异一句话（围绕 DeepSeek 前缀缓存深度调优 vs 通用多模型 harness）
  - 五、何时用 Reasonix / 何时留 Claude Code：判断框架（细节在第 13 章）
  - 六、生态与资源：仓库、官方文档清单、社区实测入口
- **内容边界**：只建立概念框架，不教操作（见第 1 章）、不讲配置细节（见第 5 章）、缓存原理只到「概览 + 指向第 9 章」。
- **素材引用**：02_deep_research.md 第一节（产品定位与核心原理，1.1–1.4）、第六节（6.1/6.3 概览口径）
- **代码示例**：无（至多展示 `default_model = "deepseek"` 一行示意，标注来源）
- **双链建议**：[[DeepSeek-Reasonix 使用指南]]、[[DeepSeek-Reasonix 前缀缓存与成本优化]]、[[从 Claude Code 迁移到 DeepSeek-Reasonix]]

---

## 02-基础功能

> 篇幅档位：每篇 2000–3000 字。目标：打牢 CLI、会话、配置、权限四大底座。

### 第 3 章 DeepSeek-Reasonix CLI 完整参考

- **目标**：一份可查询的 CLI 全量参考（命令 + 启动参数 + 无头模式 + 结构化输出）。
- **篇幅**：约 2800 字
- **结构**：
  - 一、命令总览速查表：`code`/`chat`/`run`/`setup`/`doctor`/`upgrade`(别名 update)/`acp`/`sessions`/`prune-sessions --days N`/`stats`/`mcp`/`replay`/`diff`/`commit`/`index`
  - 二、交互模式：`reasonix code [dir]`（TUI）、`reasonix chat`（纯聊天无文件系统/shell）
  - 三、启动参数详解：`--model`、`--profile`、`--effort`、`--max-steps`、`--dir`、`--add-dir`、`-c/--continue`、`-r/--resume`、`--copy`、`--allowed-tools`、`--permission-mode`、`--yolo`、`--auto/-y`、`--budget`、`--trajectory`/`--metrics`、`--ablate`（强调：测量工具非调优开关）
  - 四、无头与管道模式：`reasonix run "<task>"`、`-p/--print` 一次性只输出最终答案、管道输入 `echo "..." | reasonix run`、无人值守需 `--auto`/`-y`
  - 五、结构化输出：`--output-format text|json|stream-json`、result 对象字段逐项（`type`/`subtype`/`is_error`/`duration_ms`/`num_turns`/`result`/`session_id`/`total_cost`/`currency`/`total_cost_usd`/`usage`）、`--events-jsonl`（脱敏遥测，与 `--output-format` 互斥）、退出码约定（参数错误 2、状态/查询错误 1）
  - 六、常见坑：`--auto` 不能与显式 `--permission-mode` 组合；`--allowed-tools` 是权限覆盖不是 schema 过滤；废弃旧字段（`agent.auto_plan`/`agent.max_steps`）改用 `--max-steps`
- **内容边界**：命令全集与参数在此章；权限模式语义细节在第 6 章；会话管理交互在第 4 章；CI 编排在第 10 章（本章只列命令本身）。
- **素材引用**：02_deep_research.md 第四节（4.1/4.2）、第五节（5.4 结构化输出字段）、第七节（常见坑条目 5/6/8）
- **代码示例**：`reasonix run --output-format json` 输出示例、`echo "..." | reasonix run` 管道示例、各启动参数一行示例
- **双链建议**：[[DeepSeek-Reasonix 使用指南]]、[[DeepSeek-Reasonix 会话与交互]]、[[DeepSeek-Reasonix 自动化与 CI]]

### 第 4 章 DeepSeek-Reasonix 会话与交互

- **目标**：掌握会话模型、斜杠命令体系、/init 记忆、恢复与会话内快捷键。
- **篇幅**：约 2600 字
- **结构**：
  - 一、会话模型：会话（session）是什么、TUI 顶栏缓存/usage 显示、会话持久化与恢复入口
  - 二、会话管理命令：`reasonix sessions`、`prune-sessions --days N`、`-r/--resume [QUERY]`、`--copy`、`-c/--continue`、会话内 `/resume`、`/switch`、`/tree`、`/branch`
  - 三、斜杠命令分组：main-v2 命令族（`/help` `/model` `/provider` `/status` `/work-mode` `/effort` `/output-style` `/sandbox` `/goal` `/docs` `/mcp` `/skills` `/hooks` `/remember` `/memory` `/rewind` `/reload` `/paste-image` 等）；v1 特有命令族（`/new` `/retry` `/compact` `/copy` `/preset` `/cost` `/context` `/stats` `/doctor` `/keys` `/prompt` `/init [force]` `/apply` `/plan` `/checkpoint` `/restore` `/budget` `/permissions` `/loop` 等）
  - 四、v1 与 main-v2 版本差异（关键澄清）：main-v2 的 CLI.zh-CN 未收录 `/init`、`/plan`、`/mode`、`/budget`、`/preset` 等；main-v2 强调 `/work-mode`、`/currency`、`/docs`、`/reload`；以应用内 `/help` 为实时权威
  - 五、`/init` 与记忆：生成 REASONIX.md / AGENTS.md、记忆文件在双模型协同中的角色（指向第 7 章）
  - 六、快捷键与交互：`Up/Down`、`Ctrl+P/Ctrl+N` 选择器、`j/k`、`Shift+Tab` 权限循环、`Ctrl+Y` YOLO、审批键 `y/a/p/n`、编辑门控 `y/n`/`u`、图片粘贴（mac/Linux `Ctrl+V`、Windows `Alt+V`、`/paste-image`）
  - 七、常见坑：命令不存在多半是版本差异；先查 `/help`
- **内容边界**：斜杠命令与快捷键在此章；权限模式语义在第 6 章；CLI 全量参数在第 3 章；ACP 会话生命周期在第 11 章。
- **素材引用**：02_deep_research.md 第四节（4.3 斜杠命令、4.4 快捷键）、第七节（条目 9 版本差异）
- **代码示例**：会话管理命令、`/init` 用法、`/work-mode` 切换示例
- **双链建议**：[[DeepSeek-Reasonix CLI 完整参考]]、[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix 权限模式指南]]

### 第 5 章 reasonix.toml 配置详解

- **目标**：配置为中心的核心章节——全字段逐一解释、优先级、API Key 安全模型。
- **篇幅**：约 3000 字
- **结构**：
  - 一、配置体系概览：配置文件位置（项目 `./reasonix.toml` + 全局 `~/.reasonix/config.toml`）、解析优先级（flag > `./reasonix.toml` > 全局 > 内置默认）、TOML 结构总览
  - 二、顶层与 `[[providers]]`：`default_model`、`language`；provider 字段逐项（`name`/`kind` openai|anthropic/`base_url`/`models`/`model`/`default`/`api_key_env`/`context_window`/`effort`）；单模型 vs 多模型共用端点写法；可选字段（`reasoning_protocol`/`supported_efforts`/`default_effort`/`auth_header`/`prices`）；Anthropic 兼容端点示例（`kind="anthropic"` + `base_url=".../anthropic"`）
  - 三、`[agent]`：`system_prompt`/`temperature`/`recovery_model`/`reasoning_language`/`soft_compact_ratio`/`tool_result_snip_ratio`/`compact_ratio`/`compact_force_ratio`/`planner_model`/`subagent_model`/`max_subagent_concurrency`/`output_style`
  - 四、`[environment]` / `[tools]` / `[permissions]`：`enabled`/`offline`；`bash_timeout_seconds`/`mcp_startup_timeout_seconds`/`mcp_call_timeout_seconds`；`permissions.mode`（ask|allow|deny 兜底）+ `deny`/`allow` 规则
  - 五、`[sandbox]` / `[skills]` / `[[plugins]]` / `[ui]` / `[notifications]` / `[bot]`：各节字段速览（细节分工：sandbox 见第 14 章、plugins 见第 8/12 章、skills 见第 12 章）
  - 六、API Key 安全：config 只存 `api_key_env` 变量名、真实值在全局 `.env`、项目 `.env` 只作 MCP/plugin 的 `${VAR}` 展开来源（不导入 provider key）、Reasonix 从工具子进程移除已保存凭据
  - 七、Hooks 位置：`<Reasonix home>/settings.json`（全局）+ `<project>/.reasonix/settings.json`（项目）
  - 八、常见坑：废弃字段（`agent.auto_plan`/`agent.max_steps`/MCP 旧字段被忽略并移除）；Windows 沙箱 `bash="enforce"` 解析为 off
- **内容边界**：全字段唯一权威章节；权限规则语义在第 6 章；profile/effort/双模型在第 7 章；sandbox 细节在第 14 章；MCP/插件配置在第 8/12 章。
- **素材引用**：02_deep_research.md 第三节（3.1–3.6）、第二节（2.2 API Key 存储）、第七节（条目 1/2/8）
- **代码示例**：`reasonix.toml` 完整示例（providers/agent/tools/permissions/sandbox/ui，源自 reasonix.example.toml 3.1–3.4）
- **双链建议**：[[DeepSeek-Reasonix 权限模式指南]]、[[DeepSeek-Reasonix 模型与运行模式]]、[[DeepSeek-Reasonix 沙箱与安全]]

### 第 6 章 DeepSeek-Reasonix 权限模式指南

- **目标**：彻底讲清 6 种权限模式、交互切换、YOLO 与 fail-closed 行为。
- **篇幅**：约 2400 字
- **结构**：
  - 一、为什么需要权限模式：长时自治运行 + 逐轮 checkpoint 可撤销的配合
  - 二、6 种权限模式逐一定义：`manual/ask`（弹审批）、`auto`（自动批准普通操作）、`acceptEdits`（只放行文件编辑）、`dontAsk`（拒绝不弹窗）、`plan`（只读 Plan）、`bypassPermissions`（YOLO）
  - 三、命令行与配置控制：`--permission-mode MODE`、`--yolo`（别名）、`--auto/-y`（auto 别名，不能与显式 permission-mode 组合）、`--allowed-tools`（session 作用域权限放行）、`[permissions] mode/deny/allow`（配置 deny 永远压过 CLI allow）
  - 四、交互切换：`Shift+Tab` 循环 Ask→Auto→Plan、`Ctrl+Y` 独立切 YOLO、编辑门控 `y/n` 接受/丢弃、`u` 撤销最近自动应用批次
  - 五、非交互 fail-closed：默认 ask/manual 拒绝显式 Ask 决定与普通写 fallback；bypassPermissions 仍遵守 deny、Sandbox、需人工审批的工具
  - 六、安全边界与常见坑：`--allowed-tools` 是权限覆盖不是 schema 过滤；无人值守场景必须 `--auto`；`deny` 优先级最高
- **内容边界**：权限语义集中在此章；配置字段的书写见第 5 章；沙箱/凭据见第 14 章；ACP 的 tool_approval 形态在第 11 章提及并回链。
- **素材引用**：02_deep_research.md 第四节（4.4 权限模式与快捷键）、第三节（3.3 permissions 段）、第七节（条目 4/5/6）
- **代码示例**：`--permission-mode`/`--yolo`/`--auto` 命令示例、`[permissions]` 配置片段
- **双链建议**：[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix CLI 完整参考]]、[[DeepSeek-Reasonix 沙箱与安全]]

---

## 03-进阶应用

> 篇幅档位：每篇 2500–3500 字。目标：模型、MCP、成本、CI 四大进阶能力。

### 第 7 章 DeepSeek-Reasonix 模型与运行模式

- **目标**：讲清 profile 三档（非 smart/fast/max）、effort 推理深度、双模型协同三件事及其相互关系。
- **篇幅**：约 2800 字
- **结构**：
  - 一、三组概念先分清：profile（工作模式）vs effort（推理深度）vs preset（v1 术语/社区俗称）——**重要澄清：官方无 smart/fast/max 三档，那是社区对 `/effort` 的通俗说法**
  - 二、Profile 三档详解：`economy`（初始只带 9 个工具、其余按需连接）、`balanced`（默认、完整工具面）、`delivery`（完整工具面 + 稳定能力代理 `use_capability`、强制交付合约）；`--profile` 启动参数与 TUI `/work-mode` 热切换（`/profile` 为兼容别名）
  - 三、effort 推理深度：`/effort` 与 `--effort LEVEL`；DeepSeek 档位 high|max（思考恒开）；Anthropic 兼容端点档位 low|medium|high|xhigh|max；与 provider 默认 `effort` 字段的覆盖关系
  - 四、双模型协同（执行器 + 规划器）：`[agent] planner_model = "deepseek-pro"` 一行启用；Planner 看 REASONIX.md/AGENTS.md 记忆 + 只读研究工具，写入工具只给执行器；确定性路由不额外调 classifier；`subagent_model`/`subagent_models` 的扩展
  - 五、辅助调用分层定价：摘要、subagent 生成、截断修复一律硬编码 `v4-flash + effort=high`，不随 preset 走（引向第 9 章成本）
  - 六、选型建议：何时用哪个 profile、何时开 planner、何时只跑默认 balanced
- **内容边界**：profile/effort/双模型语义在此章；配置文件书写见第 5 章；成本测算见第 9 章。
- **素材引用**：02_deep_research.md 第三节（3.5 运行模式与模型、3.2 agent 字段）、第一节（1.3 辅助调用分层定价）、第四节（4.2 --profile/--effort）
- **代码示例**：`--profile delivery` 启动、`/work-mode` 切换、`[agent] planner_model` 配置、`--effort max`
- **双链建议**：[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix 前缀缓存与成本优化]]

### 第 8 章 DeepSeek-Reasonix MCP 使用指南

- **目标**：掌握 MCP 三类 server、命令行管理、配置与 MCP over ACP。
- **篇幅**：约 2800 字
- **结构**：
  - 一、MCP 简介（面向已熟悉 Claude Code 用户只讲差异）：Reasonix 支持三类 server
  - 二、三类 server：stdio、Streamable HTTP、legacy SSE 及其适用场景
  - 三、命令行管理：`reasonix mcp list` / `search` / `install` / `inspect` / `browse`
  - 四、配置方式：`reasonix.toml [[plugins]]` 声明外部 stdio 插件；MCP over ACP（`session/new`/`session/load`/`session/resume` 可带 `mcpServers`）；stdio 的 `env` 与 HTTP 的 `headers` 采用官方 ACP 形状 `[{"name":"...","value":"..."}]`
  - 五、环境变量展开：项目 `.env` 作 `${VAR}` 展开来源（不导入 provider key）
  - 六、超时与常见坑：`mcp_startup_timeout_seconds`/`mcp_call_timeout_seconds`；Windows 沙箱对部分 server 的影响
- **内容边界**：MCP 使用与配置在此章；插件/扩展开发（Extension Protocol）在第 12 章；ACP 会话协议在第 11 章；`[[plugins]]` 字段书写见第 5 章。
- **素材引用**：02_deep_research.md 第五节（5.1 MCP）、第三节（3.4 [[plugins]]、3.3 mcp 超时）
- **代码示例**：`reasonix mcp list/search/install/inspect` 命令、`[[plugins]]` 配置、`mcpServers` JSON 片段
- **双链建议**：[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix ACP 协议指南]]、[[DeepSeek-Reasonix 插件与扩展开发]]

### 第 9 章 DeepSeek-Reasonix 前缀缓存与成本优化

- **目标**：成本优化为中心——缓存原理、三区设计、命中率实测（含出处）、预算控制与调优建议。
- **篇幅**：约 3200 字
- **结构**：
  - 一、前缀缓存原理（深入）：精确字节前缀匹配、命中按未命中 ~10% 计费、为什么无纪律 agent 命中率 <20%（重排上下文/重写旧日志/每轮注入时间戳）
  - 二、三区上下文设计（CacheFirstLoop）：IMMUTABLE PREFIX（system+tool_specs+few_shots 每会话算一次并钉住）、APPEND-ONLY LOG（单调追加绝不重写）、VOLATILE SCRATCH（R1 思维/临时计划每轮重置、先经 Tool-Call Repair 蒸馏）；三条不变量；命中率公式 `prompt_cache_hit_tokens/(hit+miss)` 与 TUI 顶栏缓存单元格
  - 三、缓存友好工程实践：并行工具分发（`parallelSafe` + `Promise.allSettled`，结果仍按声明顺序落盘；`REASONIX_PARALLEL_MAX` 默认 3 上限 16、`REASONIX_TOOL_DISPATCH=serial` 强制串行）；Pillar 2 Tool-Call Repair 四轮修复（flatten/scavenge/truncation/storm）；轮末自动压缩（`TURN_END_RESULT_CAP_TOKENS`=3000）
  - 四、命中率与成本实测数据（**标注出处**）：官方口径（无纪律 <20%、前沿模型活跃用户 $150–250/月、北极星=便宜到可常开）；Issue #7907 用户对账（8/8 命中率 99.6%、¥1.37/全天 158 请求、¥0.00869/请求、优化后 -55~60%、最大 miss 约 2K/请求）；智源 BAAI 报道（单日 4.35 亿输入 token 命中率 99.82%、$61→$12 约 2 折、长会话 90%+）
  - 五、预算控制：`--budget <usd>`（80% 警告/100% 拒绝）【v1】；`[agent]` 压缩参数（`soft_compact_ratio`/`tool_result_snip_ratio`/`compact_ratio`/`compact_force_ratio`）；辅助调用分层定价（v4-flash + effort=high）
  - 六、调优建议清单：保命中率该做什么/不该做什么；何时开/关 compact；`reasonix stats` 查看 cost/cache 分解
  - 七、成本横向对比（简要引向第 13 章）：缓存价约 ¥0.02/1M vs 未缓存 ¥1/1M（约 50 倍单价差）、长会话输入成本约 1/5
- **内容边界**：成本与缓存唯一权威章节；`--budget` 参数出现处（第 3 章参数表）只列不展开；迁移章只做对比引用。
- **素材引用**：02_deep_research.md 第一节（1.2 前缀缓存原理、1.3 缓存友好实践、1.4 成本实测）、第三节（3.2 压缩参数、3.5）、第四节（4.2 --budget）、第六节（6.3 成本单价对比）、第七节（条目 3/7）
- **代码示例**：命中率公式、`--budget 5` 命令、`[agent]` 压缩参数配置、`reasonix stats`
- **双链建议**：[[DeepSeek-Reasonix 是什么]]、[[DeepSeek-Reasonix 模型与运行模式]]、[[从 Claude Code 迁移到 DeepSeek-Reasonix]]

### 第 10 章 DeepSeek-Reasonix 自动化与 CI

- **目标**：把无头执行、结构化输出、事件遥测接进 CI 流水线。
- **篇幅**：约 2800 字
- **结构**：
  - 一、无头模式：`reasonix run "<task>"`、`-p/--print`、管道输入 `echo "..." | reasonix run`、无人值守权限（`--auto`/`-y`/`--permission-mode auto`）、headless 审批超时默认 infinite
  - 二、结构化输出：`--output-format json`/`stream-json`；result 对象字段逐项（`type:"result"`/`subtype`/`is_error`/`duration_ms`/`num_turns`/`result`/`session_id`/`total_cost`/`currency`/`total_cost_usd`/`usage`）；流式消费与一次性消费的选择
  - 三、事件遥测：`--events-jsonl PATH`（脱敏生命周期遥测、不能与 `--output-format` 组合）、`--trajectory PATH`/`--metrics PATH`
  - 四、CI 集成：只读接口（`session list/show/status/recovery`、`task list/show/monitor`、`hook list/status`，支持 `--json`）；退出码约定（参数错误 2、状态/查询错误 1）；GitHub Actions 片段示例
  - 五、CI 中的成本与状态：`--budget` 上限、`reasonix stats`、会话保留策略 `prune-sessions`
  - 六、常见坑：fail-closed 需显式 `--auto`；`--events-jsonl` 与 `--output-format` 互斥；`--copy` 提示转 stderr 保证 stdout 纯 machine-readable
- **内容边界**：CI 编排与输出解析在此章；命令定义细节在第 3 章；成本数据在第 9 章；沙箱/凭据对 CI 的影响在第 14 章。
- **素材引用**：02_deep_research.md 第五节（5.4 自动化与 CI）、第四节（4.2 参数表）、第七节（条目 4/6）
- **代码示例**：`reasonix run --output-format json` 输出示例、管道输入示例、GitHub Actions workflow 片段、`--events-jsonl` 用法
- **双链建议**：[[DeepSeek-Reasonix CLI 完整参考]]、[[DeepSeek-Reasonix 前缀缓存与成本优化]]

---

## 04-高级功能

> 篇幅档位：每篇 2500–3500 字。目标：ACP 协议、插件扩展、迁移、沙箱安全。

### 第 11 章 DeepSeek-Reasonix ACP 协议指南

- **目标**：为编辑器/IDE 集成方讲清 ACP v1、session 生命周期与协作模式。
- **篇幅**：约 3000 字
- **结构**：
  - 一、ACP 概览：Agent Client Protocol v1、NDJSON JSON-RPC 2.0 over stdio、stdout 专用 ACP 消息/诊断走 stderr、与 MCP 的关系（MCP 是工具服务、ACP 是 agent 会话协议）
  - 二、启动 ACP 后端：`reasonix acp`、`reasonix acp --model deepseek-pro`、`reasonix acp --profile delivery`
  - 三、能力协商：`agentCapabilities`（`loadSession`/`sessionCapabilities`/`promptCapabilities` embeddedContext:true/`mcpCapabilities` http:true sse:false）、`_meta["reasonix.io"]`（sessionSteer/sessionInbox/reloadExtensions）
  - 四、session 生命周期：`session/new`、`session/load`、`session/resume`、`session/prompt`、`session/cancel`、`session/list`、`session/close`、`session/delete`
  - 五、协作模式与工具审批：`normal`/`plan`/`goal`（旧 default/auto 映射 Normal+Ask / Normal+Yolo）；`configOptions.tool_approval` = ask/auto/yolo；经 `session/set_config_option` 设置（注意字段是 `configId` 而非 optionId）
  - 六、编辑器/IDE 接入：客户端通告 `fs.readTextFile`/`fs.writeTextFile`/`terminal` 时，文件操作路由到编辑器未保存缓冲区、前台命令路由到客户端终端；MCP over ACP（session 带 `mcpServers`）
  - 七、与 Claude Code 集成差异：工具审批经 ACP 协议暴露（`session/set_config_option` + `session/request_permission`）而非本地键盘循环
- **内容边界**：ACP 协议细节在此章；MCP server 类型见第 8 章；编辑器侧 VS Code 扩展见第 1 章（安装路径）。
- **素材引用**：02_deep_research.md 第五节（5.2 ACP）、第六节（6.3 审批差异）、第八节（ACP.md 文档）
- **代码示例**：`reasonix acp` 启动、session 生命周期 JSON-RPC 消息示例、`session/set_config_option` 请求体
- **双链建议**：[[DeepSeek-Reasonix 会话与交互]]、[[DeepSeek-Reasonix MCP 使用指南]]、[[DeepSeek-Reasonix 插件与扩展开发]]

### 第 12 章 DeepSeek-Reasonix 插件与扩展开发

- **目标**：讲清扩展体系（Extension Protocol v1 Sidecar）、插件包分发与配置声明。
- **篇幅**：约 2800 字
- **结构**：
  - 一、扩展体系概览：Extension Protocol v1、Sidecar 模式（MCP server 提供工具/提示词/资源 + Sidecar 拦截运行时事件、提供 Provider 与结构化 UI）
  - 二、概念边界：扩展（Extension）vs MCP server vs 插件（plugin）的职责分工
  - 三、配置声明：`reasonix.toml [[plugins]]` 声明外部 stdio 插件；`[skills] paths`/`excluded_paths`/`disabled_skills`；插件管理走配置声明、无独立插件子命令
  - 四、插件包分发：版本化插件包（PLUGIN_PACKAGES）的打包、发布与消费
  - 五、开发入门：SDK（`sdk/go/README.md`）与文档路径（EXTENSIONS / EXTENSION_PROTOCOL / PLUGIN_PACKAGES）；一个最小插件示例
  - 六、常见坑：插件经 reasonix.toml 声明而非独立命令；Sidecar 与纯 MCP 的选型
- **内容边界**：扩展开发与分发在此章；MCP 使用与命令见第 8 章；ACP 协议见第 11 章；`[[plugins]]` 字段书写见第 5 章。
- **素材引用**：02_deep_research.md 第五节（5.3 插件与扩展）、第三节（3.4 [[plugins]]/skills）、第八节（扩展文档）
- **代码示例**：`[[plugins]]` 配置、`[skills]` 配置、最小插件包结构示意
- **双链建议**：[[DeepSeek-Reasonix MCP 使用指南]]、[[DeepSeek-Reasonix ACP 协议指南]]、[[reasonix.toml 配置详解]]

### 第 13 章 从 Claude Code 迁移到 DeepSeek-Reasonix

- **目标**：对比迁移为中心——命令/概念对照、迁移步骤、成本对比（含数据出处）。
- **篇幅**：约 3200 字
- **结构**：
  - 一、迁移前评估：核心差异（DeepSeek 前缀缓存深度调优 vs 通用多模型闭源 harness）、何时值得迁移、何时保留 Claude Code；provider 机制为插件式（以文档为准、不做绝对断言）
  - 二、命令对照表：`claude`↔`reasonix`、`claude -p`↔`reasonix -p`/`run`、`--output-format json`↔`--output-format json/stream-json`、`--allowed-tools`、`--add-dir`、`--permission-mode`、`--continue`、`--resume`（对齐 PR #6431）
  - 三、概念对照：协作模式三态（normal/plan/goal ↔ Claude 交互/plan 模式）、工具审批三态（ask/auto/yolo）、工作 profile（economy/balanced/delivery）、记忆文件（CLAUDE.md ↔ REASONIX.md/AGENTS.md）、Hooks 位置（settings.json）
  - 四、交互差异：Shift+Tab 模式循环（Ask/Auto/Plan、Ctrl+Y 独立 YOLO）、picker 方向键/Vim/Ctrl+P/N、`/model`/`/provider`/`/resume` 对齐
  - 五、迁移步骤：安装 → `reasonix setup` → 项目指令 `/init` 生成记忆 → 命令逐项替换 → 权限/hooks/settings.json 迁移 → `reasonix doctor` 验证
  - 六、成本对比（**数据出处**）：缓存价约 ¥0.02/1M vs 未缓存 ¥1/1M（约 50 倍单价差）；Reasonix 命中率 94–99.8%；长会话输入成本约 1/5；引用 Issue #7907 与智源实测（回链第 9 章）
  - 七、迁移常见坑：v1/main-v2 命令列表差异、API Key 存储位置不同（全局 .env vs 其他）、`--auto` 组合限制、`deny` 优先级
- **内容边界**：横向对比与迁移路径在此章；命令/概念细节各自回链（第 3/4/5 章）；成本数据引用第 9 章不复制推导。
- **素材引用**：02_deep_research.md 第六节（6.1–6.3）、第二节（2.2）、第七节（条目 3/4/5/6/8/9）、第八节（PR #6431、Issue #7907）
- **代码示例**：命令对照示例（成对展示）、迁移后的 `reasonix.toml` provider 段
- **双链建议**：[[DeepSeek-Reasonix 是什么]]、[[DeepSeek-Reasonix 使用指南]]、[[DeepSeek-Reasonix 前缀缓存与成本优化]]

### 第 14 章 DeepSeek-Reasonix 沙箱与安全

- **目标**：讲清沙箱实现（Seatbelt/bubblewrap/Windows off）与凭据保护，给出安全最佳实践清单。
- **篇幅**：约 2800 字
- **结构**：
  - 一、安全模型三层：权限（第 6 章）+ 工作区沙箱 + 凭据保护，及其协作关系
  - 二、工作区沙箱：`[sandbox]` 字段（`workspace_root`/`allow_write`/`forbid_read`/`bash`=enforce|off/`network`）；macOS Seatbelt、Linux bubblewrap、Windows 强制 off（`bash="enforce"` 解析为 off）
  - 三、凭据保护：config 只存 `api_key_env` 变量名、真实值在全局 `<Reasonix home>/.env`、项目 `.env` 不导入 provider key、Reasonix 从工具子进程移除已保存凭据
  - 四、权限与沙箱协同：`deny`/`allow` 规则、fail-closed 默认拒绝、bypassPermissions 仍遵守 deny/Sandbox/需人工审批工具
  - 五、安全最佳实践清单：`forbid_read` 保护 `${HOME}/.ssh` 等敏感目录、`allow_write` 白名单、Windows 无 OS 级沙箱的替代策略（容器/CI 隔离）、无人值守 CI 的最小权限配置
  - 六、常见坑：Windows 上 `bash="enforce"` 被忽略；无沙箱环境下 enforce 会拒绝 bash 执行；`deny` 永远压过 CLI allow
- **内容边界**：沙箱与凭据唯一权威章节；权限模式语义见第 6 章；配置字段书写见第 5 章；CI 安全引用第 10 章。
- **素材引用**：02_deep_research.md 第三节（3.4 [sandbox]）、第四节（4.4 fail-closed）、第六节（6.3）、第七节（条目 2/3/5）、第二节（2.2 API Key 存储）
- **代码示例**：`[sandbox]` 配置示例（workspace_root/allow_write/forbid_read/bash/network）
- **双链建议**：[[DeepSeek-Reasonix 权限模式指南]]、[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix 自动化与 CI]]

---

## 学习路径说明

### 前置要求
- 熟悉 Claude Code 的基本操作（命令、会话、权限、settings.json 概念），本系列不做通用 agent 工具铺垫。
- 会读 TOML/YAML 配置，能区分「项目级配置」与「用户级配置」。
- 具备一个可用的 DeepSeek API Key（或愿意在 setup 向导中配置 provider 凭据）。
- 本系列假设本地可运行终端命令；Windows 用户需注意沙箱差异（第 14 章）。

### 学完能做什么
- 独立完成 DeepSeek-Reasonix 的安装、setup 配置、日常会话与排障（`doctor`/`stats`）。
- 熟练使用 CLI 全量参数、会话管理、斜杠命令与快捷键，知道 v1/main-v2 差异如何自查。
- 能手写并调优 `reasonix.toml`（providers/agent/tools/permissions/sandbox/plugins），理解配置优先级与 API Key 安全模型。
- 能配置 MCP 服务、选择权限模式与沙箱策略，实现安全的长时自治运行。
- 能理解并优化前缀缓存命中率与成本，用 `--budget`/`stats` 做预算控制。
- 能把 `reasonix run` + 结构化输出接入 CI 流水线。
- 能通过 ACP 协议把 Reasonix 接入编辑器/IDE，并理解插件扩展体系。
- 能把已有 Claude Code 工作流迁移到 DeepSeek-Reasonix，并对比成本。

### 建议学习顺序
1. **入门（0.5 天）**：先读第 2 章（是什么）建立心智模型 → 第 1 章（装、配、跑、查）上手。
2. **基础（2 天）**：第 3 章 CLI 参考（按需查询）→ 第 5 章配置详解（核心）→ 第 6 章权限 → 第 4 章会话交互。建议边用边查，不必一次背完。
3. **进阶（2–3 天）**：第 7 章模型与运行模式 → 第 9 章缓存与成本（重点）→ 第 8 章 MCP → 第 10 章自动化与 CI。
4. **高级（按需）**：需要接入编辑器时读第 11 章 ACP；要扩展时读第 12 章；正在用 Claude Code 的读者尽早读第 13 章迁移；生产环境务必读第 14 章安全。
5. **推荐速查路径**：日常多用第 1 章速查表 + 第 3 章命令表；成本敏感时回第 9 章；排障先跑 `reasonix doctor` 与 `/help`。

---

## 覆盖检查（质量自检）

- [x] 14 篇 / 4 层结构完全对齐用户已确认的系列结构
- [x] 每篇结构细化到 H2（一、二、三…）
- [x] 每篇篇幅标注在对应档位区间内
- [x] 每篇标注 02_deep_research.md 章节引用
- [x] 每篇标注代码示例与双链建议（仅高价值概念）
- [x] 关键澄清点已覆盖：profile 三档非 smart/fast/max（第 7 章）、v1/main-v2 版本差异（第 4 章）、成本实测数据出处（第 9 章 + 第 13 章）
- [x] 每篇「内容边界」保证全系列无重叠（配置→第 5 章、命令→第 3 章、权限→第 6 章、成本→第 9 章、沙箱→第 14 章）
- [x] 素材引用编号与 02_deep_research.md 实际内容一致
