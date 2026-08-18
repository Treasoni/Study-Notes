## 学习笔记大纲：《如何写 subagent（DeepSeek-Harness）》

> 笔记类型：概念理解 + 实战（上手）
> 预计总篇幅：约 26-32 页（中长篇分册，补进 DeepSeek-Harness 教程系列）
> 章节数：7
> 读者画像：熟悉 Claude Code 扩展体系、已读 dsh 插件开发五章的「有了解」用户

### 系列统一结构（每章固定 4 板块）
1. **导读**：为什么读这章、解决什么问题
2. **章节小结**：读完带走什么
3. **与 Claude Code 对照**：迁移心智、对照差异
4. **更新记录**：developer preview（2026-08-13 锚点）下的变化标注

### 诚实标注约定（贯穿全文，成稿时不得删除）
- **综合推断**：官方无直接文档，由 S2 契约 + S4 方法论拼合（发布前必须对照源码核实，主要落在第 4 章）
- **未证实**：仅社区二手说法（如 subagent「数量限制」），笔记不展开或显式标注
- **未抓取**：本分册未收集，MOC 标注可扩展（codex/claude-code 配置表、tool-subagent-report 细节）

---

### 第一章：subagent 心智模型——能力缝与三层结构
- **篇幅**：中
- **覆盖要点**：为什么 subagent 是「能力缝」而不是单一插件（与 bash 可选能力缝并列）；三层结构——① Service Definition（`dsh-subagent` / `ctx.subagents`）→ ② Service Provider（spawn/fork/acp/codex/claude-code/dsh-sdk 六兄弟）→ ③ Consumer/Tool（`dsh-tool-subagent`）；provider 与 consumer 互不依赖、只依赖定义包（换实现只改一行配置）；微内核主张「核心循环固定，一切能力是扩展点上的监听者」；三段式原则「完整能力本身才是接缝，单一角色不是」
- **素材引用**：S1/S2（§3.1）、S10（§3.1）、S4（§3.1）、S4-4.9-2（命名律预告）
- **代码示例**：无（仅 §3.2 的 ASCII 三层结构图）
- **与 Claude Code 对照**：`.claude/agents/*.md` 单一角色文件注册 vs dsh 注册表 + provider + 工具松耦合——Claude Code 的「写一个 md 文件」对应 dsh 的「三段式三件套」
- **本章埋坑/诚实标注**：无具体坑；预告「inheritsParentContext 与『继承』直觉相反」悬念，埋指针到第 2 章；注明 developer preview 生态尚未稳定

### 第二章：核心契约——`ctx.subagents` 注册表与 `SubagentProvider` 接口
- **篇幅**：长
- **覆盖要点**：`ctx.subagents` 注册表（`registerProvider` effect-scoped / `getProvider` / `list` / 核心方法总览 / `subagent:start|end` 事件按委派 parent scope 分发）；`SubagentProvider` 契约（`name` / `capabilities` 四 flag / `inheritsParentContext` 描述性标注 / `start` 发布后返回 handle / `prepareContinuable` 存在即能力）；`SubagentStartRequest` 选项与能力检查（label/prompt/parent/agentOptions/outputSchema/maxDepth/toolFilter/persona）；`SubagentRun` / `SubagentResult` 语义（一次性前台委托、dispose、result 不因 child 级失败 reject、output 取最后一个非空 assistant 消息、stopReason 与 ACP/dsh-sdk 映射表）
- **素材引用**：S2-4.1、S3-4.1、S2-4.2、S3-4.2、S2-4.3、S2-4.4、S5-4.4-5、S6-4.4-6
- **代码示例**：有（6.1 骨架中的 `SubagentProvider` 类型与 `start()` 签名，作「契约速览」用途；类型以 S2/S3 为准，非完整实现，无需额外核实）
- **与 Claude Code 对照**：Claude Code subagent 的「运行即结果」vs dsh 的 `SubagentRun`/`SubagentResult` 显式生命周期与 stopReason 语义
- **本章埋坑/诚实标注**：
  - 能力不匹配启动时响亮失败（`UNSUPPORTED_CAPABILITY`），绝不静默忽略（S2-4.3-2）
  - `outputSchema` 请求了不保证得到 `structured`（S2-4.3-3）
  - `inheritsParentContext` 只是描述性标注，不暗示工具/服务/权限继承（S2-4.2-3、§5#1）

### 第三章：现成 provider 家族——选用、挂载、跑起来
- **篇幅**：中
- **覆盖要点**：in-process vs out-of-process 大分流；spawn（能力全开、无父历史）/ fork（对话种子、`inheritsParentContext: true`）vs acp（独立子进程、零启动期能力、每次全新进程）/ dsh-sdk（完整 peer harness、自管组合/模型路由/递归预算、成本更高）；codex/claude-code 仅列名并标注可扩展；环境变量处理（先擦除凭据形状与陈旧 `DSH_*` 名）与 cwd 规则（绝不用 server 进程自身 cwd）；挂载——`cordis.patch.yml` provider + tool 两行（6.3 底稿）；选择 provider 的决策依据表（6.4）
- **素材引用**：S8-4.7-1、S1/S2-4.7-2、S5-4.7-3、S6-4.7-4、S1/S10-4.7-5、S5/S6-4.7-6/7、S7-4.8-1（工具预告）、6.3、6.4
- **代码示例**：有（6.3 底稿 `cordis.patch.yml` 的 acp provider + tool 两行；acp 命令参数需对照 S5 README 核实；`dsh plugin add` 后手动 insert 的精确语法需对照配置体系笔记 + C1 第三方插件示例核实）
- **与 Claude Code 对照**：Claude Code 内置 subagent 执行器是「唯一实现」，dsh 是「可替换 provider 全家桶」——换执行后端只改配置一行
- **本章埋坑/诚实标注**：
  - spawn 全新 child、无父历史；只有 fork 带对话种子（§5#3 对照表）
  - acp 不声明任何启动期 capabilities，本地服务拒绝而非静默忽略（S5-4.7-3）
  - subagent 系列包都是纯 Cordis 插件：`dsh plugin add` 只让包可解析，必须手动在 `cordis.patch.yml` insert 才能挂进插件树（6.3）
  - codex/claude-code 配置表本分册未抓取（§7#3）

### 第四章：写自己的 provider——三段式与最小实现（深度章节）
- **篇幅**：长
- **覆盖要点**：三段式方法论（① Service Definition 定义包：抽象 Service 类 + Request/Result 类型 + `declare module` 扩展 Context → ② Service Provider 实现包：`export const name` + `export function apply(ctx){ ctx.plugin(...) }` → ③ Consumer/Tool：`inject: ['tools','cap']` + `defineTool` + `ctx.tools.register`）；命名律 `dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>`；设计要点（Do not split preemptively、类型归定义包、默认值在显式 `resolve` 里不在 `run()` 藏 `?? default`）；最小 provider 骨架逐行讲解（6.1 底稿）；in-process `start()`（经 `ctx.agents`）vs out-of-process `start()`（子进程握手 ACP/SDK initialize）两条实现路径；`registerProvider` effect-scoped 注册与卸载；从 Claude Code subagent 迁移映射（`.claude/agents/*.md` → provider 插件 + 工具实例）
- **素材引用**：S4-4.9-1/2/3、S2-4.2、S2-4.3、S3-4.2-5、S5、S6、S8、6.1、6.2
- **代码示例**：有（**6.1 最小骨架 + 6.2 三段式三件套**；6.2 为 S4 官方 my-cap 示例可直接引用；**6.1 标注综合推断，发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码核实 `start()` 的 in-process 实现**；可选 `prepareContinuable` 写法以 S2-4.2-5 语义为准）
- **与 Claude Code 对照**：写 dsh provider 类比在 Claude Code 侧写「自定义 subagent + 脚本工具」——Claude Code 的 md 角色声明对应 dsh 的 `SubagentProvider` 契约声明
- **本章埋坑/诚实标注**：
  - 包级坑：subagent 相关包**无默认导出**，Cordis loader 解包会隐藏命名 `inject` 元数据（S5/S6-4.9-4、postmortem 0001）
  - `capabilities` 不声明 → 请求对应能力的 start 被 `UNSUPPORTED_CAPABILITY` 拒绝（呼应第 2 章）
  - `start()` 发布前失败必须清理未发布部分资源，不得留孤儿（S2-4.2-4）
  - 诚实标注：官方无独立 SubagentProvider 教程，6.1 骨架为 S2+S4 综合推断（§5#7、§7#1）

### 第五章：生命周期深度——one-shot / continuable 与委派深度
- **篇幅**：中
- **覆盖要点**：one-shot（前台默认 / 后台 `enableRunInBackground`+`backgroundMode`）vs continuable（持久可恢复 child）两族；continuable 编排四 API 语义——`startContinuable`（收件箱准入即 resolve，不等轮次开始）/ `followup`（唯一继续执行消息操作，看 Activation 状态路由）/ `interrupt`（唯一公开停止，同步鉴权后发 cancel、不等停稳）/ `reportFrom`（child 向直接 parent 上报，child 是权威凭证）；委派深度双重表示（持久 `SessionHeader.delegationDepth` + 运行时 `AgentOptions.subagentDepth`）、冷恢复不可降深度、深度上界校验；maxDepth 默认 3 与 `'provider-managed'`；已知限制（无 host-user 续写、不能转向当前 turn、驻留仅进程本地、跨进程 ownership 未设计 + 社区方案 dsh-background-agents 仅作经验标注）
- **素材引用**：S2-4.6、S3-4.6-6/7/8/9、S2-4.5、S7-4.5-4、S6-4.5-5、S2-4.1-4、C2
- **代码示例**：无（概念为主；可放一个 `startContinuable`/`followup` 调用语义示意，标注为 S2/S3 语义示意、非可运行代码）
- **与 Claude Code 对照**：Claude Code subagent 的一次性 task 委派 vs dsh 的 continuable 持久化子代理与 followup/interrupt 编排
- **本章埋坑/诚实标注**：
  - 冷恢复无法降低委派深度（S2-4.5-2）
  - 已接受但未落日志的消息不可重放；report 需存活直接父代（S3-4.6-9、S3-4.6-5）
  - 跨进程 continuable ownership 官方「未设计」（§7#5）；dsh-background-agents 只作社区经验标注（C2），不作为官方能力

### 第六章：工具化——把 provider 暴露成模型可调能力
- **篇幅**：中
- **覆盖要点**：`dsh-tool-subagent`——一个 provider 绑一个 toolName（默认 `subagent`）、config 全字段（provider/toolName/enableRunInBackground/backgroundMode/agentOptions/persona/toolFilter/maxDepth）；`dsh-tool-subagent-control`（send_message / interrupt_agent / list_agents 全局控制）；`dsh-tool-subagent-report`（child→parent 汇报方向）；委托沙箱策略（`captureDelegatedPolicyOverrides` 快照父显式 sandbox 覆盖 + 子代理审批钉死 `'never'`，需审批的升级请求确定性拒绝）；完整接线示例（6.3 底稿扩展：provider + tool + control/report 三件套）
- **素材引用**：S7-4.8-1、S9-4.8-2/3、S10-4.8-4、S3-4.9-5、6.3
- **代码示例**：有（6.3 中 tool-subagent 配置行可直接用；control/report 接线需对照 S9 README 补充——**tool-subagent-report 细节本分册未单独抓取（§7#4），写章时补齐**）
- **与 Claude Code 对照**：Claude Code 的 subagent/tool 调用面 vs dsh 委托工具三件套（subagent 委派 / control 全局控制 / report 反向汇报）
- **本章埋坑/诚实标注**：
  - 重复 toolName 冲突：一个 provider 绑一个 toolName，需全局唯一（S7-4.8-1）
  - `maxDepth` 默认 3、`0` 禁止委派；在 dsh-sdk 上设 `'provider-managed'` 才由子 harness 自管递归预算（§5#2）
  - 后台 one-shot 结果走 task 工具回传（S2-4.6-1 + S7 语义）

### 第七章：速查与避坑清单（精简）
- **篇幅**：短
- **覆盖要点**：避坑速查表（汇总第 2-6 章埋的坑，一屏索引、不重复展开）；决策速查（选 provider / 选 one-shot vs continuable / 选 in-process vs out-of-process）；**诚实标注清单**——综合推断项（6.1 骨架）、未证实项（subagent 数量限制，§5#5/§7#2）、未抓取项（codex/claude-code 配置表、tool-subagent-report 细节、cordis.patch.yml 精确语法）集中列明；与 Claude Code 迁移对照速查表；更新记录与开放问题（§7）
- **素材引用**：§5 矛盾表、§7 开放问题、S2/S3/S5/S6/S7 要点汇总
- **代码示例**：无
- **本章埋坑/诚实标注**：仅索引既有坑，不新增；developer preview 破坏性变更风险在此统一标注

---

## 学习路径说明

### 前置要求
- 熟悉 Claude Code 扩展体系：`.claude/agents/*.md`、subagent 调用心智、工具定义
- 已读完 DeepSeek-Harness 插件开发五章：cordis 插件结构、`ctx.tools`/`defineTool`、`dsh plugin add`、`cordis.patch.yml`
- 能读 TypeScript 接口/泛型/可选方法签名（`SubagentProvider` 契约是类型收窄驱动的）

### 学完能做什么
- 说清 dsh subagent 的「能力缝 + 三层结构」心智模型，并迁移 Claude Code 的 subagent 心智
- 按需选择并挂载现成 provider（spawn/fork/acp/dsh-sdk），用 `dsh-tool-subagent` 暴露给模型
- 独立写一个最小 provider 插件，用 `ctx.subagents.registerProvider` 注册并挂进 cordis 插件树
- 理解 one-shot/continuable 生命周期与委派深度限制，避开 `UNSUPPORTED_CAPABILITY`、无默认导出等已知坑
- 给后续分册留好接口（codex/claude-code provider 配置、跨进程 continuable 社区方案）

### 建议学习顺序
- 顺序通读第 1-4 章（心智 → 契约 → 现成 provider → 写自己的 provider），这是主路径
- 第 5 章生命周期对只想快速上手的读者可先跳读，写 provider 遇到 `prepareContinuable` 或配置 backgroundMode 时再回来补
- 第 6 章工具化在动手「把 provider 给模型用」时精读；第 7 章速查在写作与排错时当索引用
- 预估时间：通读约 2-3 小时；动手写第一个 provider 另加 1-2 小时（含对照源码核实 6.1）
- 每章读完建议做一次「与 Claude Code 对照」的迁移笔记，沉淀进个人 Obsidian

### 写作前需用户补充/确认的点
1. 第四章 6.1 骨架发布前需对照 `subagent-spawn-in-process` 真实源码核实 `start()`——写正文时是否有该源码可读，还是保持「综合推断」标注输出？
2. `cordis.patch.yml` 手动 insert 的精确语法需对照既有配置体系笔记 + C1 第三方插件示例——是否需要我在写第 3 章前先取回该示例？
3. 未证实项（subagent 数量限制）按约定不展开，仅在第 7 章标注「未证实」——是否认可？
