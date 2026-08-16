# 深度收集结果 - 如何写 dsh hook 扩展点插件

> 阶段：P2 · 深度收集
> 日期：2026-08-16
> 方向：D 组合（A 语义模型 → B 实战代码 → C 迁移对照）
> 方法：3 个并行深研代理，深读 6 核心源，claim 级笔记带锚点；社区插件作佐证

## 范围（Scope）

围绕「在 dsh 插件里用代码实现 hook 扩展点」教学所需的三块：
1. **语义模型**：5 个扩展点（`pre-execute` / `guard()` / `execute` / `post-execute` / `result`）+ `next()` 瀑布 + 固定流水线顺序
2. **实战代码**：官方 permission-gate 完整示例 + 真实社区插件佐证 + 验证命令链复用来源
3. **迁移对照**：官方 `dsh-hooks-claude-code` 映射表 + 配置桥 vs 代码实现差异

## 源表（Source Table）

| ID | 标题 | 层级 | 用途 | 日期 |
|----|------|------|------|------|
| S1 | dsh-tools 工具作者参考（packages/core/tools/README） | official | 语义模型权威定义 + PreToolDecision/PostToolDecision 类型 + 约束 | master HEAD (2026-08) |
| S2 | 扩展插件形态 Cookbook（docs/cookbook/extension-cookbook） | official | permission-gate 唯一官方 TS 示例 + 扩展点选择规则 | master HEAD (2026-08) |
| S3 | 工具执行流水线（docs/tool-execution-pipeline） | official | 固定顺序 pre-execute→guard→execute→post-execute→finalizeContent→result | master HEAD (2026-08) |
| S4 | @deepseek-ai/dsh-tools (npm) | official | 类型包存在性（registry 核实，0.1.0-rc.6）；页面 403 代码未核 | 2026-08 |
| S5 | dsh-hooks-claude-code README（packages/hooks/hooks-claude-code） | official | 官方 CC↔dsh 映射表 + 配置桥限制 | master HEAD (2026-08) |
| S6 | Claude Code Hooks reference | official | CC 源侧：31 事件、三层 JSON、hookSpecificOutput | 持续更新 |
| S7 | dsh-guardian (GitHub, lonelymoon87) | community | 真实插件：pre-execute deny/ask + post-execute redact；DSH 0.1.0-rc.6 | 无日期 |
| S8 | dsh-permission-rules (npm) | community | 声明式 allow/deny/ask；registry 核实 v0.4.2；代码未核 | 无日期 |
| S9 | dsh-bridges (npm) | community | 第三方桥，宣称 CC hooks 原样运行；无映射表；v0.1.0 | 2026-08-15 |

**层级混合**：官方 5 / 社区 4（S7 有实测可引用，S8/S9 仅 registry 核实、代码未核）。

## Claim / 源映射

### 语义模型（A 透镜 → S1/S3）

| Claim | 源+锚点 |
|-------|---------|
| 固定流水线：`tools/pre-execute` → 单调 guard →（ask 经 `ctx.approval`）→ `tools/execute` → 工具体 → `tools/post-execute` → 归一化 → `finalizeContent` → `tools/result` → durable `tool/result` 事件 | S3 § Tool Execution Pipeline |
| 3 个 transformable waterfall：`pre-execute` / `execute` / `post-execute`；guard 只 deny-or-abstain；`finalizeContent` 仅内容；`tools/result` 只读观察 | S3 § Tool Execution Pipeline |
| `PreToolDecision = {kind:'allow'} \| {kind:'deny', reason} \| {kind:'ask', reason?}`；`ask` 由 `ctx.approval` 服务，无 mount 时降级为 deny | S1 § Injected services / Key types |
| `tools/pre-execute` **不能改写 `exec.arguments`**（记录/渲染的参数会与实际运行脱同步）——与 CC `updatedInput` 关键差异 | S1 § Known Limitations；S5 partial-support |
| `ctx.tools.guard()`：`(execution) => string \| undefined`；返回 string=最终单调 deny，undefined=abstain；后续 waterfall 监听者不能撤销 | S1 § dsh-tools/guard；S3 stage 4 |
| guard 不可重排（approval 先于 guard 解析 ask）；denial 路由到 `tools/post-execute` 跳过工具体 | S3 stage 4 |
| `tools/execute` 包装 dispatch：仅可替换 `exec.signal`，不可换 arguments；canonical 结果属于单一不可变 dispatch token | S1 § Key types |
| `tools/post-execute`：`PostToolDecision` accept 可替换 content **或** value（不同时）+ 附 additionalContexts；block 带 feedback 转 valueless failure | S1 § Key types |
| `tools/result`：观察不可变 lossless-JSON 结果，不能变换；同步 live notification | S1 § dsh-tools；S3 stage 14 |
| `finalizeContent`：definition-owned，对每个归一化结果恰一次，只换 content，必须同步且 total | S1 § Key types |

### 实战代码（B 透镜 → S2/S7）

| Claim | 源+锚点 |
|-------|---------|
| 官方唯一 hook 插件示例 = permission-gate：`ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`；deny 返回 `{kind:'deny', reason}`，allow 走 `next()`，无显式 `{kind:'allow'}` 字面量 | S2 § a-hook-plugin-permission-gate-example |
| 原生 hook 是「普通 Cordis 插件挂到拦截点」，无外部协议；`apply(ctx)` 内注册 | S2 § a-hook-plugin-permission-gate-example |
| 选择规则引语：单调最终拒绝用 `guard()`；包装 dispatch（超时/重试/metrics，仅 signal 可换）用 `execute`；显式结果变换用 `post-execute`；只读观察用 `result` | S2 § a-hook-plugin-permission-gate-example（引述 adding-a-tool.md） |
| **S2 无 guard / post-execute / result 的 TS 代码示例**（仅选择规则 + 功能表提及）——教学需自行构造 | S2（缺失确认） |
| **S2 未含验证命令链**（load/dump-config/headless 均无）→ 从本教程 08 章复用 | S2 § Runnable wirings（缺失确认） |
| S7 佐证：`pre-execute` 将危险命令分类 deny/ask/unchanged；`post-execute` redact 凭据；「最严格者胜出 deny>ask>allow」；target DSH 0.1.0-rc.6，Node ^22.19\|\|>=24，tarball 分发 | S7 § MVP / Policy behavior / Redaction behavior / Install |

### 迁移对照（C 透镜 → S5/S6）

| Claim | 源+锚点 |
|-------|---------|
| 官方映射表：`PreToolUse→tools/pre-execute`、`PostToolUse→tools/post-execute`、`UserPromptSubmit→agent/pre-step`、`Stop→agent/turn-stopping`、`SessionStart→agent/session-start`、`SubagentStart→subagent/start`、`SubagentStop→subagent/end` | S5 README mapping table |
| 支持 7 / 不支持 23（"Unsupported hook events (23 of Claude Code's current 30)"）；不支持事件在 group 解析前忽略，不使配置失效 | S5 README unsupported-events |
| 桥读取 JSON 配置：`configPath` 必填，进程级解析一次，相对 launch cwd | S5 README config |
| 仅 shell-form `type:'command'` handler 会执行；http/mcp_tool/prompt/agent 解析后跳过并告警；`args`/`async`/`if`/`once` 等选项不 honored | S5 partial-support |
| CC 分层 project/user/plugin/policy 发现 + live reload **未实现**；匹配 handler 串行执行不去重（CC 并行去重）；UserPromptSubmit 桥用 600s 超时（CC 事件专用 30s） | S5 README |
| CC 侧：hooks → matcher group → handler 三层嵌套；`hookSpecificOutput` 含 `permissionDecision`/`additionalContext`/`updatedInput`/`systemMessage`，输出 cap 10,000 字符 | S6 Configuration / JSON output |
| CC 事件表列 **31** 个事件（页面未声明"30"）——与 S5 "30" 口径不一致 | S6 Hook events 表 |
| emit vs waterfall：SessionStart/SubagentStart/SubagentStop → emit（不可阻塞，仅注入/观察）；PreToolUse/PostToolUse/UserPromptSubmit/Stop → waterfall/serial 决策点 | S5 mapping table |
| `dsh-hooks-codex` 未在 S5 出现（not found）；桥自称 "the CC dialect half of the hooks subsystem"，方言无关原语来自 `@deepseek-ai/dsh-hook-protocol` | S5 |

## 矛盾与需注意（Contradictions）

1. **事件总数口径不一致**：S5 说 "23 of CC's current **30**"，S6 事件表列 **31** 个。教学引用计数时需注明来源时间点，或写「约 30（CC 文档当前列表 31）」。→ 建议教程用「7 个支持 / 其余不支持」，避开绝对总数争议。
2. **S2 示例与 S1 类型的表述差异**：S2 示例无显式 `{kind:'allow'}` 字面量，S1 类型定义含 `allow` 分支。教学可说明「`next()` 是 allow 的委派写法，字面量 allow 存在但少见」。
3. **npm 包代码未核实**：S4/S8/S9 页面 403，仅 registry 元数据确认存在。教程若引用其类型/API 需标注「未直接核实代码」，或改为引用 S1 仓库源码。

## 实践指引（Practical Guidance）

- **写一个 hook 插件的骨架**：`src/index.ts` 里 `apply(ctx)` 中 `ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`；deny 返回类型化对象，放行 `return next()`。
- **五扩展点选型口诀**（来自 S2 选择规则）：权限门→`pre-execute`；单调最终拒绝→`guard()`；超时/重试/指标→`execute`；改结果/附 context→`post-execute`；只看不改成审计→`result`。
- **guard 是「一票否决」**：`undefined` 弃权，字符串=最终拒绝，后续监听者无法翻案；不可重排；agent-scoped 用 `agent.ctx`。
- **post-execute 替换规则**：accept 换 content 或 value 二选一；block=带反馈的失败；`additionalContexts` 可附加。
- **迁移注意**：CC 的 `updatedInput`（改写工具入参）在 dsh 侧无对应能力，需改走「附加 context + 下游决策」模式；CC 五种 handler 只有 `command` 会执行。
- **验证**：S2 无验证命令链，复用教程 08 章（load → dump-config → dump-default-config → headless）。
- **社区可参照**：S7 dsh-guardian（deny>ask>allow 最严格胜出、post-execute redact）是真实落地样板。

## 开放问题（Open Questions）

1. `PostToolDecision` 的 accept 中「content 或 value 二选一」的具体字段名与 TS 类型——S1 提取为 paraphrase，教程引用时建议直接核 `@deepseek-ai/dsh-tools` 类型源码（S4 代码未核）。
2. `tools/result` 与 durable `tool/result` 事件在 agent loop 中的具体消费方（metrics/audit/capture 由谁订阅）——S1/S3 只描述，未给下游消费者代码。
3. `ctx.approval` 的 `ask` 交互如何在 CLI / UI 呈现——S1 只说明「mounted 时服务，否则降级 deny」。
4. 桥不支持的事件（23 个）在教程里是否值得给一张「迁移对照表」完整列出——S5 有逐列清单，可作附录。

## 下游交接（Handoff）

- **大纲（P3）**：按 D 顺序组织三块 → ①语义模型（流水线 + 5 扩展点 + next() 瀑布）②实战（permission-gate 起步 + 手写 guard/post-execute/result 三示例 + 验证链）③迁移对照（官方映射表 + updatedInput 差异 + 配置桥限制）。
- **写作（P4）**：代码以 S2 官方示例为权威基线；guard/post-execute/result 无官方示例 → 依据 S1 语义自行构造并标注「基于 S1 语义构造」。补 frontmatter/callout 按 note-system.md。
- **信源引用**：9 源编号 S1–S9，脚注引用锚点优先（章节名 + 短引文）。
- **产出位置**：Obsidian `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/` 新增章节，同步 README + MOC。
