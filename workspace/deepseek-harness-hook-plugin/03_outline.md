## 学习笔记大纲：《如何写 DeepSeek-Harness hook 扩展点插件》

> 笔记类型：实战教学分册（learning-note，大纲模式）
> 预计总篇幅：中量 12,000–15,000 字
> 内部章节数：8 章（第 1–8 章为本文内部规划，非系列章节号）
> 素材引用：深度素材 S1–S9（源编号与 `02_deep_research.md` 源表一致）
> 系列定位：DeepSeek-Harness 插件开发教程「第 11 章」，与 01 章 3.5 hook 速览互补（01 是目录速览，本篇是教学落地），与 03 章配置实战区分（03 讲搬配置，本篇讲写代码）
> 结构主线：方向 D 组合 —— A 语义模型 → B 实战代码 → C 迁移对照
> 输出位置：`AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/11-实战-写hook扩展点插件.md`（单文件成章，完成后同步系列 README + MOC）

### 第 1 章：导读与定位——本篇讲什么、不重复什么
- **篇幅**：5%（短）
- **覆盖要点**：
  - 本章在系列中的坐标：插件开发教程第 11 章，是 01 章 3.5「hook 扩展点」速览的教学落地；01 只给目录表格，本篇把 5 个扩展点逐个写给你看
  - 与 03 章「配置实战」的边界：03 讲把现有 Claude Code hooks 配置搬进 dsh（走配置桥），本篇讲在 dsh 代码里用 `apply(ctx)` 实现 hook 扩展点插件
  - 本篇三块结构预览：A 语义模型（流水线 + 5 扩展点 + next() 瀑布）→ B 实战代码（permission-gate 起步 + 手写 guard/post-execute/result + 验证链）→ C 迁移对照（官方映射表 + updatedInput 差异 + 配置桥限制）
  - 读者画像与前置：已读 01 章 3.5 + 系列 04–10 实战分册，熟悉 Claude Code 扩展体系
- **素材引用**：#S2（cookbook 定位）、#S1（工具作者参考定位）
- **代码示例**：无

### 第 2 章：语义模型——工具执行流水线与 next() 瀑布
- **篇幅**：15%（中）
- **覆盖要点**：
  - 固定流水线顺序（引用 S3 权威顺序）：`tools/pre-execute` → 单调 guard →（ask 经 `ctx.approval`）→ `tools/execute` → 工具体 → `tools/post-execute` → 归一化 → `finalizeContent` → `tools/result` → durable `tool/result` 事件
  - 三类角色分工：可变换瀑布（pre-execute / execute / post-execute）、只否决的 guard、只读观察（finalizeContent / result）
  - `next()` 瀑布语义：`return next()` = 委派放行（allow 的委派写法），不调用 next = 短路拦截；监听器按注册序串行
  - `ask` 决策经 `ctx.approval` 服务，无 mount 时降级为 deny
  - `PreToolDecision` 三态类型（allow / deny / ask）引入（类型细节放第 3 章）
- **素材引用**：#S3（流水线顺序）、#S1（瀑布语义与 PreToolDecision）
- **代码示例**：无（纯模型讲解，类型签名集中到第 3 章）

### 第 3 章：五个扩展点逐个拆解——职责、类型与选型
- **篇幅**：20%（长）
- **覆盖要点**：
  - `tools/pre-execute`：权限门决策点，`PreToolDecision` allow/deny/ask；**不能改写 `exec.arguments`**（记录/渲染参数会与实际运行脱同步，与 CC `updatedInput` 的关键差异）
  - `ctx.tools.guard()`：签名 `(execution) => string | undefined`；返回 string = 最终单调 deny、undefined = abstain；后续 waterfall 监听者不能撤销；guard 不可重排（approval 先于 guard 解析 ask）
  - `tools/execute`：包装 dispatch，仅可替换 `exec.signal`，不可换 arguments；canonical 结果属于单一不可变 dispatch token（超时 / 重试 / 指标用）
  - `tools/post-execute`：`PostToolDecision` accept 可替换 content **或** value（不同时）+ 附 `additionalContexts`；block 带 feedback 转 valueless failure
  - `tools/result`：只读观察 lossless-JSON 不可变结果，不能变换；同步 live notification
  - `finalizeContent`：definition-owned，对每个归一化结果恰一次，只换 content，必须同步且 total
  - 五扩展点选型口诀（引用 S2 选择规则引语）+ 常见坑（guard 叠加语义、post-execute 替换 vs result 只读的取舍、卸载自动清理）
- **素材引用**：#S1（类型定义）、#S3（各阶段位置）、#S2（选择规则引语）
- **代码示例**：有（各扩展点的类型签名与最小写法片段）

### 第 4 章：实战起步——permission-gate 权限门
- **篇幅**：18%（中）
- **覆盖要点**：
  - 官方唯一 hook 插件示例逐行拆解：`ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`（引用 S2 权威代码）
  - deny 返回 `{ kind: 'deny', reason }` 类型化对象；放行走 `return next()`；说明「无显式 `{kind:'allow'}` 字面量」与 S1 类型的表述差异
  - 原生 hook = 普通 Cordis 插件挂到拦截点，无外部协议；`apply(ctx)` 内注册，`src/index.ts` 做注册中心
  - 扩展成 allow / deny / ask 三态 + 可配置规则列表：参考 S7 dsh-guardian「最严格者胜出 deny > ask > allow」落地样板
  - 代码文件归属：`src/index.ts` 挂载 + 规则函数拆到 `src/hooks/`
- **素材引用**：#S2（官方 permission-gate 示例）、#S7（dsh-guardian 三态与最严格胜出）、#S1（PreToolDecision 类型）
- **代码示例**：有（完整 permission-gate 插件 TS）

### 第 5 章：实战进阶——手写 guard / post-execute / result 三个示例
- **篇幅**：20%（长）
- **覆盖要点**：
  - guard 单调否决示例：`ctx.tools.guard()` 返回 string=拒绝、undefined=弃权；agent-scoped 用 `agent.ctx`；演示「后面监听者无法翻案」
  - post-execute 改汇报示例：accept 替换 content 给模型看、或换 value；`additionalContexts` 附加上下文；block 带 feedback 转失败
  - result 只读观察示例：订阅不可变结果做审计 / 日志 / 指标，演示「只看不改」
  - 一个插件内叠加多个扩展点的顺序演示：pre-execute + guard + post-execute + result 同一 `apply(ctx)` 里共存，验证瀑布与观察点各自触发
  - **标注说明**：guard / post-execute / result 无官方 TS 示例（S2 仅选择规则 + 功能表提及），本三例依据 S1 语义自行构造
  - 卸载自动清理：`ctx.on` 注册即 effect，无需手动 removeListener
- **素材引用**：#S1（构造依据）、#S3（瀑布位置与不可撤销语义）、#S2（选型规则）、#S7（社区 redact 佐证）
- **代码示例**：有（guard / post-execute / result 三个手写 TS 示例 + 叠加顺序）

### 第 6 章：验证命令链——复用 08 章跑通
- **篇幅**：7%（短）
- **覆盖要点**：
  - 复用 08 章验证四连（S1–S9 无验证链，需显式标注从本教程 08 章复用）：`pnpm dsh web --patch` 验加载 → `--dump-config` 验配置层 → `--dump-default-config` 验 bundle 默认 → `pnpm dsh --profile headless` 验端到端
  - hook 行为如何观测：`console.log` 加载日志确认扩展点挂载；headless 端到端验证权限门真实拦截（deny 时模型被拒、退出码语义）
  - 常见排查：扩展点没触发 → 检查 `ctx.on` 是否在 `apply(ctx)` 内注册、`inject` 依赖是否就绪
- **素材引用**：#S2（确认无验证链）、#S7（社区插件验证实践）
- **代码示例**：有（bash 验证命令链，来源为 08 章）

### 第 7 章：迁移对照——从 Claude Code hooks 到 dsh
- **篇幅**：10%（中）
- **覆盖要点**：
  - 官方映射表（引用 S5）：`PreToolUse → tools/pre-execute`、`PostToolUse → tools/post-execute`、`UserPromptSubmit → agent/pre-step`、`Stop → agent/turn-stopping`、`SessionStart → agent/session-start`、`SubagentStart/SubagentStop → subagent/start|end`
  - 事件支持差异：约 7 个支持 / 其余不支持；不支持事件在 group 解析前忽略，不使配置失效（避开「30 vs 31」绝对总数口径争议，注明来源时间点）
  - **`updatedInput` 差异**：CC 可用 `updatedInput` 改写工具入参，dsh 无对应能力 → 改走「附加 context + 下游决策」模式（呼应第 3 章 pre-execute 不能改 arguments）
  - 配置桥限制：仅 shell-form `type:'command'` handler 执行，http/mcp_tool/prompt/agent 解析后跳过并告警；CC 分层 project/user/plugin/policy 发现 + live reload 未实现；匹配 handler 串行执行不去重（CC 并行去重）
  - 桥 vs 手写代码的取舍：何时用官方 `dsh-hooks-claude-code` 配置桥（S5）、何时手写 hook 插件（本篇主线）；社区第三方桥 S9 宣称「原样运行」与官方桥差异
  - emit vs waterfall：SessionStart / SubagentStart / SubagentStop → emit（不可阻塞，仅注入/观察）；PreToolUse / PostToolUse / UserPromptSubmit / Stop → waterfall/serial 决策点
- **素材引用**：#S5（官方映射表与桥限制）、#S6（CC 源侧三层 JSON 与 hookSpecificOutput）、#S9（第三方桥对照）
- **代码示例**：有（CC `settings.json` hook 配置片段 + 对应 dsh 写法对照）

### 第 8 章：小结与下一步
- **篇幅**：5%（短）
- **覆盖要点**：
  - 五扩展点选型口诀收口：权限门→`pre-execute`；单调最终拒绝→`guard()`；超时/重试/指标→`execute`；改结果/附 context→`post-execute`；只看不改→`result`
  - 本章产出文件清单：`src/index.ts`（注册中心挂 4 类扩展点）+ `src/hooks/`（规则与变换函数）+ 验证命令链回顾
  - 与 01 章 3.5 速览闭合：速览表格 → 本篇逐点落地
  - 下一步：参照社区插件（S7 dsh-guardian / S8 dsh-permission-rules / S9 dsh-bridges）、开放问题 4 项（PostToolDecision 字段名核类型源码、result 消费方、ask 交互呈现、桥不支持事件完整清单作附录）
- **素材引用**：#S2（选型口诀）、#S7（社区样板）、#S1（类型源码锚点）
- **代码示例**：无

## 学习路径说明

### 前置要求
- 已读《插件开发核心》01 章 3.5「hook 扩展点」速览（本篇的教学基线，不重复目录表格）
- 已读系列实战分册 04–10 章，特别是 08 章验证命令链（本篇验证直接复用）与 01 章 `apply(ctx)` / fiber / inject 心智模型
- 熟悉 Claude Code 扩展体系：hooks / `settings.json` / `hookSpecificOutput`
- 本地 dsh 源码仓库就绪（clone → `pnpm install` → `pnpm run build`），命令统一在仓库根目录执行

### 学完能做什么
- 说清 dsh 工具执行流水线的固定顺序与 5 个扩展点的职责边界（含 guard 单调否决、post-execute 替换 vs result 只读的取舍）
- 从零手写一个带权限门 + guard 一票否决 + post-execute 改汇报 + result 审计的 hook 插件，并用 08 章验证命令链跑通
- 读懂官方 `dsh-hooks-claude-code` 桥的映射表与限制，判断「搬现有 CC hooks 配置」还是「在 dsh 代码里手写插件」

### 建议学习顺序
- 顺序通读第 1–8 章：第 2–3 章语义模型是地基（约 45 分钟），第 4–6 章动手落地（约 1–1.5 小时），第 7 章迁移对照按需精读（约 30 分钟）
- 动手节奏：先照抄跑通 permission-gate（第 4 章），再逐个叠加 guard / post-execute / result（第 5 章），每加一个跑一次验证链（第 6 章），不要攒到最后一次验证
- 迁移对照（第 7 章）建议读完立刻做一次「你现有 CC hooks 配置 → dsh」的映射练习，沉淀成迁移笔记
- 预估总时间：通读约 2 小时；动手写第一个 hook 插件另加 1–2 小时

## 待确认与缺口提示
- **guard / post-execute / result 无官方 TS 示例**：写作时依据 S1 语义自行构造，代码内标注「基于 S1 语义构造」；`PostToolDecision` 的 content/value 字段名建议直接核 `@deepseek-ai/dsh-tools` 类型源码（S4 代码未核）
- **事件总数口径**：S5 说「CC 当前 30」、S6 事件表列 31，教学引用时用「约 7 个支持 / 其余不支持」，避开绝对总数争议
- **社区源可信度分层**：S7 可引用（实测插件），S8/S9 仅 registry 核实、代码未核，引用其 API 时标注「未直接核实代码」
