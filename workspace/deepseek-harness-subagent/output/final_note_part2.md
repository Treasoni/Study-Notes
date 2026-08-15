> 生命周期理清了，模型却还「摸不到」provider——它只是后台实现，模型能调用的只有工具。这一章把 provider 暴露成模型可调能力，接上全局控制、反向汇报与委托沙箱策略。

# 第六章 工具化——把 provider 暴露成模型可调能力

> [!summary] 导读
> 前面几章把 provider 写好、把生命周期理清，但模型还是「摸不到」它——provider 只是后台实现，模型能调用的只有工具。这一章接上最后一段：用 `dsh-tool-subagent` 把一个 provider 包成模型可见的工具，用 `-control` 拿到全局控制权，用 `-report` 打通 child 反向汇报，并讲清委托时 sandbox 策略为什么会被「钉死」成确定性拒绝。读完你会得到一张「provider + tool + control/report」三件套的完整接线图，能把第 3 章挂载的 provider 真正暴露给模型用，也看得懂为什么子代理永远不会「卡在等人审批」上。

## 6.1 `dsh-tool-subagent`：一个 provider 绑一个 toolName

`dsh-tool-subagent` 是三层结构里的 Consumer/Tool 层：它的职责是把**某一个** provider 包装成模型能调的工具。[^S7-4.8-1] 它是 dsh 内置 `dsh-tool-*` 家族的一员——这个家族还有 `bash` / `fs` / `web` / `todo`，subagent 跟它们平级，都是「把某个能力暴露成模型工具」的消费层。[^S10-4.8-4] 记住它的核心设计一句话：**一个 tool-subagent 实例，绑定一个 provider，暴露成一个 toolName。**

- **绑定一个 provider**：`config.provider` 是必填字段，值就是 provider 的注册名（`acp` / `spawn` / `fork` / `dsh-sdk`…）。一个实例只服务一个 provider，不搞「一个工具背后轮询多家」。
- **暴露成一个 toolName**：模型看到的工具名由 `config.toolName` 决定，默认是 `subagent`。工具名在**全局工具注册表里必须唯一**——这也是埋坑 ① 的来源。
- 想同时暴露两个 provider？那就开**两个** tool-subagent 实例，各绑一个 provider、各取一个不重名的 toolName。

> [!tip] 大白话
> 把每个 tool-subagent 实例想成给模型发的一张**临时工牌**：工牌上印着「你只能找 acp 这位同事」（一个 provider 绑一个 toolName），而且全公司工牌号不能重号（全局唯一）。所以……想同时暴露 acp 和 spawn 两个 provider，就得发两张不同工号的工牌（不同 toolName），不能两个人都挂同一张「subagent」牌。

### 6.1.1 config 全字段

`dsh-tool-subagent` 的 config 全部字段如下（字段名与 `SubagentStartRequest` 选项一一呼应，第 2 章的能力检查在这里就是「把请求选项写进配置」）：[^S7-4.8-1]

| config 字段 | 必填 | 默认 | 作用 |
| --- | --- | --- | --- |
| `provider` | ✅ | — | 绑定哪个已注册 provider，值 = provider 的 `name`（如 `acp`） |
| `toolName` | — | `subagent` | 模型可见的工具名，**全局唯一** |
| `enableRunInBackground` | — | `false` | 是否允许 one-shot 后台运行（不阻塞当前 turn） |
| `backgroundMode` | — | `one-shot` | 后台模式：`one-shot` 一次性 / `continuable` 持久可恢复 |
| `agentOptions` | — | — | 透传给子代理的运行选项（如深度相关字段） |
| `persona` | — | — | 为 child 遮蔽部署 persona（要求 provider 有 `persona` 能力） |
| `toolFilter` | — | — | 命名工具过滤（要求 provider 有 `toolFilter` 能力） |
| `maxDepth` | — | `3` | 委派深度上限；`0` 表示禁止委派 |

`persona` / `toolFilter` / `maxDepth` 三个字段分别要求 provider 声明了对应 `capabilities`（第 2 章 2.2.2），否则启动时被 `UNSUPPORTED_CAPABILITY` 拒绝——这个检查规则在工具配置层同样生效。

> [!warning] 埋坑 ①：重复 toolName 冲突
> 一个 provider 绑一个 toolName，且 toolName 需**全局唯一**。如果你再加一个 tool-subagent 实例、却仍用默认 `toolName: subagent`，工具注册时就会撞名——这跟 `ctx.tools.register` 的重名语义一致，不是「覆盖」，而是失败。想暴露第二个 provider，必须显式改 `toolName`（比如 `subagent_acp` / `subagent_spawn`）。

### 6.1.2 最小配置行

只暴露一个 provider 时，配置可以极简（第 3 章 6.3 底稿就是这么写的）：[^6.3]

```yaml
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config: { provider: acp, toolName: subagent }
```

`provider` 必填，`toolName` 不写就用默认值 `subagent`。第 6.4 节会给一份全字段展开的版本。

## 6.2 控制与汇报：`-control` 三件套 + `-report`

单靠 `dsh-tool-subagent`，模型只能「发起委派」，还不能「管」运行中的 agent、也不能让 child「说回来」。这两件事由两个兄弟工具补齐：[^S9-4.8-2][^S9-4.8-3]

### 6.2.1 `dsh-tool-subagent-control`：全局控制三件套

`dsh-tool-subagent-control` 注册三个**全局控制**工具，方向是「模型 → 任意 agent」，不绑定某个 provider：[^S9-4.8-2]

| 工具名 | 作用 | 对应核心包方法 |
| --- | --- | --- |
| `send_message` | 向一个运行中的 continuable agent 发送消息 | `followup` |
| `interrupt_agent` | 中断一个运行中的 agent | `interrupt` |
| `list_agents` | 枚举当前已知/运行中的 agent | `listChildren` / `listDescendants` |

注意「全局」的定位：`subagent` 工具只能「开新委派」，而这三个工具能跨 provider、跨 child 去发消息、掐断、枚举——是给模型的一台调度台。`send_message` / `interrupt_agent` 的语义细节与第 5 章 `followup` / `interrupt` 的编排规则一致（比如 interrupt 是同步鉴权后发 cancel、不等停稳即返回）。

> [!tip] 大白话
> 把 `-control` 想成**总机**：`list_agents` 是「查分机表」、`send_message` 是「给某个分机转电话」、`interrupt_agent` 是「强行掐断某条线」。所以……它不是给某个 provider 单独用的，而是面向所有运行中 agent 的全局调度台——这跟 6.1 那个「只认一个 provider 的临时工牌」是两种粒度。

### 6.2.2 `dsh-tool-subagent-report`：child→parent 反向汇报

`dsh-tool-subagent-report` 打通的是**反向**方向：child 通过它向自己的**直接 parent** 汇报。[^S9-4.8-3]

- 方向是「child → 直接 parent」，与委派工具（模型 → child）正好相反；这也呼应第 5 章 `reportFrom` 的语义——child 是权威凭证，调用方不能指定接收方。
- 汇报要求**存活的直接父代**（第 5 章 S3-4.6-5：report 需要存活直接父代，无持久 report 邮箱）。

> [!warning] 诚实标注：`-report` 细节待补
> 本分册 P2 只抓到了 `-report` 的**定位**（child→parent 汇报方向，来源 S9-4.8-3），**没有单独抓取 `tool-subagent-report` 包的 README 细节**（字段、示例、与 `reportFrom` 的对应关系）。本节按定位写，具体 config 与调用示例需对照 `packages/subagent/tool-subagent-control/README.md` 家族核实后再补——第 7 章速查里也会把它列进「未抓取项」。

## 6.3 委托沙箱策略：核心包的确定性拒绝

工具层把 provider 暴露给模型之后，还有一个安全面要处理：**子代理在什么权限下运行、能不能向人要更高权限？** 这个策略在核心包（`dsh-subagent`）里实现，三条规则值得单列：[^S3-4.9-5]

1. **快照父的显式 sandbox 覆盖**：`captureDelegatedPolicyOverrides(parent)` 在委托发生时，把父级**显式设置**的 sandbox 覆盖快照下来，作为子代理运行的沙箱基准。注意是「快照那一刻的显式授权」，不是「继承父的整套运行时」——跟第 2 章 `inheritsParentContext` 的克制是同一个味道。
2. **子代理审批策略钉死为 `'never'`**：子代理的审批策略被硬性设为「永不审批」。任何需要人工审批的升级请求（比如 `sandbox_permissions` 提权）都会被**确定性拒绝**，而不是弹出一个提示等人点——因为子代理运行时背后**没有人在看**，等审批提示等于死锁。
3. **`subagent:delegation` 运行时上下文声明越权不重试**：子代理的运行上下文标记 `subagent:delegation`，一旦某次授权越权被拒，**不重试**——拒绝是确定性的，不存在「再试一次说不定就过了」的循环。

把第 3 章 6.3 的 provider 配置翻出来看，你会发现 `permission: reject` 正是这条策略在 provider 侧的落点：acp provider 的 config 里写 `permission: reject`，等于把「审批」这道门从配置层面焊死。[^6.3]

> [!tip] 大白话
> 把子代理想成拿**临时门禁卡**的实习生：卡上写死「无审批权限」。他想进机房（升级 sandbox 权限）——门禁直接拒，而不是呼叫保安（等待人工审批），因为值班室根本没人。所以……「确定性拒绝」不是 bug，是**防死锁设计**：宁可当场说 No，也不让整个委派任务卡在一个无人观看的审批提示上干等。

## 6.4 完整接线示例：provider + tool + control/report 三件套

把 6.1/6.2/6.3 合起来，就是一份「三件套」齐活的 `cordis.patch.yml`。下面以第 3 章 6.3 底稿为骨架扩展：[^6.3]

```yaml
# cordis.patch.yml —— provider + tool + control/report 三件套接线骨架
# 前提：subagent 系列包都是纯 Cordis 插件，先 dsh plugin add 让包可解析，
#       再手动 insert 进插件树（既有配置体系笔记结论）

# ① Provider：acp（out-of-process，独立子进程驱动）
- id: subagent-acp
  name: '@deepseek-ai/dsh-subagent-acp'
  config:
    providerName: acp
    command: node
    args: ['--import', 'tsx', './packages/examples/acp-demo/src/bin.ts']
    permission: reject          # 审批策略钉死 reject：升级请求确定性拒绝（见 6.3）
    env:
      DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY

# ② Consumer/委托工具：把 acp 包成模型可见工具
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config:
    provider: acp               # 绑定的 provider 注册名（必填）
    toolName: subagent          # 模型可见工具名，全局唯一
    enableRunInBackground: true # 允许 one-shot 后台运行
    backgroundMode: one-shot    # one-shot | continuable
    maxDepth: 3                 # 默认 3；0 禁止委派

# ③ Consumer/控制工具：全局控制三件套
- id: tool-subagent-control
  name: '@deepseek-ai/dsh-tool-subagent-control'
  config:
    # send_message / interrupt_agent / list_agents 三件套默认注册
    # 具体 config 字段以 README 为准（本分册素材未逐字段收录）

# ④ Consumer/汇报工具：child→parent 反向汇报
- id: tool-subagent-report
  name: '@deepseek-ai/dsh-tool-subagent-report'
  # 细节待补：本分册未单独抓取该包 README（见 6.2 诚实标注）
```

接线要点：

- **换 provider 只改两处**：把 ① 的 provider 条目换成另一个（比如 `dsh-subagent-spawn-in-process`），再把 ② 的 `config.provider` 改成对应注册名。定义层与工具层一行不动——第 1 章「换实现只改一行配置」在这里落地成「换 provider + 改 provider 字段」两处。
- **想暴露第二个 provider**：再复制一份 ②，改 `toolName`（如 `subagent_spawn`），否则撞名（埋坑 ①）。

### 6.4.1 埋坑 ②：maxDepth 的三态

`maxDepth` 有三个状态要分清：[^S7-4.8-1][^S6-4.5-5]

| 值 | 含义 |
| --- | --- |
| 不写 / `3` | 默认 3，子代理最多往下委派 3 层 |
| `0` | **禁止委派**——child 不能再往下派活 |
| `'provider-managed'` | **只在 dsh-sdk 上有效**：表示子 harness 自己管理递归预算，父级不施加上限 |

注意 `'provider-managed'` 不是通用值：它是 dsh-sdk 这种「完整 peer harness」的特权——子进程自管递归预算，父级不越俎代庖。spawn 这类 in-process provider 上别指望它生效（第 5 章 §5#2 的区分在这里收口）。

### 6.4.2 埋坑 ③：后台 one-shot 结果走 task 工具回传

`enableRunInBackground: true` + `backgroundMode: one-shot` 时，委派不阻塞当前 turn——child 在后台跑，结果**不**直接出现在委派处，而是经由 **task 工具**回传。[^S7-4.8-1][^S2-4.6-1] 这对写工具消费方的意义是：

- 别期待「await 工具调用 = 拿到 child 最终输出」；后台 one-shot 的结算路径绕了一圈，结果由 task 工具带回来。
- 如果这个模式对你太绕，前台 one-shot（默认）就是「等结果再回来」的直觉路径——后台是给「不想卡住当前 turn」的场景用的。

## 本章小结

- `dsh-tool-subagent` 把**一个** provider 包成一个模型工具：`provider` 必填、`toolName` 默认 `subagent` 且全局唯一；`enableRunInBackground` / `backgroundMode` / `agentOptions` / `persona` / `toolFilter` / `maxDepth` 是其余 config 字段。
- `dsh-tool-subagent-control` 是全局调度台：`send_message` / `interrupt_agent` / `list_agents` 三件套，方向是「模型 → 任意 agent」。
- `dsh-tool-subagent-report` 打通反向：child → 直接 parent 汇报；本分册只抓了定位、细节待补（诚实标注）。
- 委托沙箱策略三连：快照父显式 sandbox 覆盖（`captureDelegatedPolicyOverrides`）→ 审批钉死 `'never'` → `subagent:delegation` 越权不重试；`permission: reject` 是它在 provider 配置侧的落点。
- 埋了三个坑：① 重复 toolName 撞名 ② `maxDepth` 默认 3、`0` 禁止、`'provider-managed'` 仅 dsh-sdk ③ 后台 one-shot 结果走 task 工具回传，不是「await 即结果」。

下一章把这些坑连同第 2-5 章埋的坑汇总成一张避坑速查表，写作与排错时当索引用。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 委派调用面 | `task` 工具内嵌 subagent 调用 | `dsh-tool-subagent` 把 provider 包成工具，一个 provider 绑一个 toolName |
| 全局控制 | 内置的任务/会话管理 UI | `dsh-tool-subagent-control` 三件套（send_message / interrupt_agent / list_agents） |
| 反向汇报 | 无独立汇报工具，结果经 task 返回 | `dsh-tool-subagent-report`：child → 直接 parent 反向汇报 |
| 后台运行 | `task` 后台任务 | `enableRunInBackground` + `backgroundMode`（one-shot / continuable） |
| 沙箱审批 | 交互式审批提示（有人看） | 审批钉死 `'never'`：无人审批 → 升级请求确定性拒绝 |

迁移心智：Claude Code 里「subagent + task 工具 + 任务管理」是框架收敛在一起的一组能力；dsh 把它们拆成**三个方向**的工具——`subagent` 委派（模型→child）、`control` 全局控制（模型→任意 agent）、`report` 反向汇报（child→parent）。你在 Claude Code 里「发起一个 task、看任务列表、收结果」的心智，到 dsh 要拆成「调 subagent 发起、调 list_agents 看、调 send_message 续写、由 report/task 收口」。安全模型也不同：Claude Code 把审批弹窗给「看着屏幕的人」，dsh 直接假设子代理背后没人，把审批焊死成拒绝——这是「无人值守」假设带来的必然差异。

## 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档撰写。`dsh-tool-subagent` 全字段、`-control` 三件套、委托沙箱策略均引自官方 README/核心包；**`-report` README 细节本分册未抓取，6.2.2 按定位写并标注待补**。若 preview 更新改动工具 config 字段或沙箱策略表述，本章 6.1 / 6.3 是受影响区域，优先对照检查。

---

[^S7-4.8-1]: S7 · `dsh-tool-subagent` README §4.8-1——一个 provider 绑一个 toolName（默认 `subagent`）、config 全字段（provider/toolName/enableRunInBackground/backgroundMode/agentOptions/persona/toolFilter/maxDepth）、maxDepth 默认 3 / 0 禁止委派。
[^S9-4.8-2]: S9 · `tool-subagent-control` / `-report` README §4.8-2——`send_message` / `interrupt_agent` / `list_agents` 全局控制工具。
[^S9-4.8-3]: S9 · `tool-subagent-control` / `-report` README §4.8-3——`dsh-tool-subagent-report` child→parent 汇报方向（本分册未单独抓取细节，见 6.2.2 诚实标注）。
[^S10-4.8-4]: S10 · 扩展 Cookbook §4.8-4——内置 `dsh-tool-*` 家族含 subagent（"bash, fs, web, subagent, todo"），subagent 是消费层工具家族的成员。
[^S3-4.9-5]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.9-5——委托沙箱策略：`captureDelegatedPolicyOverrides(parent)` 快照父显式 sandbox 覆盖、子代理审批钉死 `'never'`（`sandbox_permissions` 等升级请求确定性拒绝）、`subagent:delegation` 运行时上下文声明越权不重试。
[^S2-4.6-1]: S2 · Subagent 子系统设计文档（中文）§4.6-1——one-shot 前台（默认）/ 后台（`enableRunInBackground` + `backgroundMode`）区分；后台结算语义。
[^S6-4.5-5]: S6 · `dsh-subagent-dsh-sdk` README §4.5-5——`maxDepth: 'provider-managed'`：子 harness 自管递归预算，父级不施加。
[^6.3]: 02 深度研究 §6.3——`cordis.patch.yml` 注册 + 挂载 + 暴露为工具示例（provider + tool 两行、`permission: reject`、纯 Cordis 插件需手动 insert）。

---

> 坑位攒了不少，最后一章不再讲新内容，只把第 2–6 章埋的坑、三个选型速查与三类诚实标注集中收口成一张可扫的速查索引。

# 第七章 速查与避坑清单

> [!summary] 导读
> 前六章把 subagent 从心智模型一路讲到工具化，信息量不小。这一章不做新内容，只做三件事：把第 2–6 章埋下的坑汇总成一屏可扫的索引表；把三个高频决策（选 provider / 选 one-shot vs continuable / 选 in-process vs out-of-process）压成速查；并把全系列的诚实标注（综合推断 / 未证实 / 未抓取）集中列明，方便写作与排错时快速定位。它不替代前面的任何一章——当你遇到报错或拿不准选型时，回这里翻表，再回到对应章节看细节。

## 7.1 避坑速查表（一屏索引）

下表索引第 2–6 章埋下的坑，只给「坑名 → 出处 → 一句话规避」。每条坑的完整论证与代码上下文，回到出处章查看；素材源头见 02 深度研究 §5 矛盾表与 S2/S3/S5/S6/S7 要点汇总。[^R5]

| 坑名 | 出处章 | 一句话规避 |
|---|---|---|
| UNSUPPORTED_CAPABILITY 响亮失败 | 第 2 章（2.3.1） | 能力不匹配启动即拒、绝不静默；要能力选 spawn/fork，收到此错不是重试能解决 [^S2] |
| outputSchema 不保证 | 第 2 章（2.3.2） | 请求了 schema 不一定拿到 `structured`；消费方回退 `output` 文本 [^S2] |
| inheritsParentContext 反直觉 | 第 2 章（2.2.3） | 只担保对话种子；工具/服务/权限要显式走 agentOptions / toolFilter [^S2] |
| spawn 无父历史 | 第 3 章（provider 家族） | 想让孩子接父对话用 fork；spawn 是全新 child [^S8] |
| acp 零能力 | 第 3 章（acp） | acp 不声明任何启动期能力；要能力强制换 in-process [^S5] |
| 纯 Cordis 需手动 insert | 第 3 章（挂载） | `dsh plugin add` 只让包可解析；必须手动在 `cordis.patch.yml` insert 才挂进插件树 |
| codex/claude-code 未抓配置 | 第 3 章（外部后端） | 本分册未抓 config 表；需要时查官方，别当已完整 |
| 无默认导出（postmortem 0001） | 第 4 章（包级坑） | subagent 系列包无默认导出，Cordis loader 解包会隐藏命名 `inject` 元数据；用命名导出 [^S56] |
| capabilities 不声明即拒绝 | 第 4 章（契约） | 不声明 → 请求对应能力的 start 被 `UNSUPPORTED_CAPABILITY` 拒绝；按需声明四 flag [^S2] |
| start 发布前清理 | 第 4 章（start） | fulfill 前失败必须清理未发布资源，别留孤儿 [^S2] |
| 6.1 骨架综合推断 | 第 4 章（6.1） | 官方无独立教程，骨架是 S2+S4 拼合；发布前对照 `subagent-spawn-in-process` 源码核实 [^R7] |
| 冷恢复不可降深度 | 第 5 章（委派深度） | 冷恢复无法降低 delegationDepth；别指望冷恢复缩深度 [^S2] |
| 消息不可重放 | 第 5 章（continuable） | 已接受未落日志的消息不可重放；别依赖重放恢复 [^S3] |
| report 需存活父代 | 第 5 章（report） | report 需存活直接父代；父代已死则上报不可达 [^S3] |
| 跨进程 ownership 未设计 | 第 5 章（已知限制） | 官方未设计跨进程 continuable ownership；多进程共享要持久 mailbox + 租约，C2 只作经验 [^S3] |
| toolName 全局唯一 | 第 6 章（dsh-tool-subagent） | 一个 provider 绑一个 toolName；重复会冲突，全局唯一命名 [^S7] |
| maxDepth 默认 3 / provider-managed | 第 6 章（maxDepth） | 默认 3、0 禁止委派；dsh-sdk 上设 `'provider-managed'` 才由子 harness 自管递归预算 [^S7][^S6] |
| 后台结果走 task 工具 | 第 6 章（后台 one-shot） | 后台 one-shot 结果经 task 工具回传；消费方监听 task 回传而非前台 await [^S7] |

> [!tip] 大白话
> 把这张表想成药盒上的「不良反应速查」：你不需要背每一种坑，只需要在症状出现时回来对一下。所以……这章的价值不是「多讲了几条知识」，而是把前六章的知识点压成了「出错时能翻到的索引」。

## 7.2 决策速查

三个高频选型，各一张表。规则都一样：先对需求，再选实现，最后回头查 7.1 的坑。

### 7.2.1 选 provider

| 需求 | 选 | 一句依据 |
|---|---|---|
| 要结构化输出 / toolFilter / persona / 深度强制 | spawn / fork | in-process 四项启动期能力全支持 [^S8][^S2] |
| 要子代理继承父对话上下文 | fork | `inheritsParentContext: true`，带对话种子 [^S2] |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | 三者均 `inheritsParentContext: false` [^S2][^S5][^S6] |
| 要驱动任意 ACP 协议 agent | acp | 独立子进程、ACP 客户端驱动 [^S5] |
| 要完整独立 harness（自管模型/组合/递归预算） | dsh-sdk | 子进程是完整 peer harness；可设 `maxDepth: 'provider-managed'` [^S6] |

### 7.2.2 选 one-shot vs continuable

| 场景 | 选 |
|---|---|
| 一次性委派，await 结果，用完 dispose | one-shot（前台，默认） |
| 一次性委派，不想阻塞，跑完回传 | one-shot（后台：`enableRunInBackground` + `backgroundMode`） |
| 需要跨 turn 续写、可恢复、可中断 | continuable（`startContinuable` + `followup` / `interrupt`） |
| 需要 child 反向上报给 parent | continuable（`reportFrom`） |
| 注意 | 两者驻留都仅进程本地；continuable 不跨进程协调 |

### 7.2.3 选 in-process vs out-of-process

| 维度 | in-process（spawn/fork） | out-of-process（acp/dsh-sdk） |
|---|---|---|
| 运行位置 | 同进程新建 child | 独立子进程（ACP / SDK 握手） |
| 启动期能力 | spawn 四项全支持 / fork 支持 | acp 零能力 / dsh-sdk 全 false |
| 继承语义 | spawn:false、fork:true | 均 false |
| 隔离与成本 | 无进程隔离、成本低 | 环境变量擦除 + 独立 session root；dsh-sdk 成本更高 |
| 适用 | 要能力强制、快速上手 | 要隔离 / 驱动外部协议 / 完整 peer harness |

决策箭头：要能力强制 → in-process；要进程隔离或驱动外部 ACP agent → acp；要完整 peer harness（自管递归预算）→ dsh-sdk。

> [!tip] 大白话
> 把决策速查想成餐厅的「点单对照」：先说自己要什么（需求），服务员再给你指对应的菜（provider / 模式）。所以……别从「哪个 provider 最好」开始问，要从「我这单要什么能力」开始对表。

## 7.3 诚实标注清单（集中列明）

全系列三类「信心等级」在此集中收口，不散落各章。写作或排错时若引用下列任一项，请保持标注。[^R5][^R7]

| 类型 | 项 | 状态 | 处置 |
|---|---|---|---|
| 综合推断 | 第 4 章 6.1 最小 provider 骨架（尤其 `start()` 的 in-process 实现） | 官方无独立 SubagentProvider 教程，由 S2 契约 + S4 三段式拼合 | 发布前对照 `subagent-spawn-in-process` 真实源码核实 |
| 未证实 | 「dsh 无内置 subagent 数量限制」 | 仅社区二手说法（P1 已 403），未经官方证实 | 本系列不展开；需要时查官方 |
| 未抓取 | codex / claude-code provider 完整 config 表 | 本分册 P2 未抓取 | MOC 标注可扩展，留给后续分册 |
| 未抓取 | tool-subagent-report README 细节 | 未单独抓取（与 -control 同 README 族） | 写第 6 章时补齐；本章只索引 |
| 未抓取 | cordis.patch.yml 手动 insert 精确语法 | 未对照 C1 第三方插件 insert 示例核实 | 写第 3 章时对照配置体系笔记核实 |

> [!tip] 大白话
> 把三个等级想成「信心标签」：综合推断 =「我们拼出来的，别当定论」；未证实 =「网传，官方没认」；未抓取 =「这页书我们还没读」。所以……看到这三个词，你就知道哪些话能直接引用、哪些要先核实再用。

## 本章小结

- 第 2–6 章共埋约 18 个坑，全部收进 7.1 一屏索引；排错先对表、再回出处章看细节。
- 三个选型速查：选 provider 看能力需求与继承语义；one-shot 看要不要跨 turn；in/out-of-process 看要不要隔离与能力强制。
- 诚实标注集中在 7.3：综合推断（6.1 骨架）、未证实（数量限制）、未抓取（codex/claude-code 配置表、tool-subagent-report、cordis.patch.yml 语法）。
- 本系列到此收尾：1 章心智 → 2 章契约 → 3 章选型 → 4 章写 provider → 5 章生命周期 → 6 章工具化 → 7 章速查。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness | 迁移动作 |
|---|---|---|---|
| 心智单元 | 写一个 `.md` 角色文件 | 三段式三件套（定义 + provider + 工具） | 把「一个 subagent」换成「一条能力缝」 |
| 声明方式 | `.claude/agents/*.md` 框架自动发现 | `ctx.subagents.registerProvider` 显式注册（effect-scoped） | 写 provider 插件并注册 |
| 执行后端 | 内置唯一实现，不可换 | 六 provider 可替换，配置一行切换 | 换执行只改 `config.provider` |
| 能力声明 | md frontmatter 隐含 | `capabilities` 四 flag 静态声明，缺则拒 | 显式声明 outputSchema / depthLimit / toolFilter / persona |
| 结果模型 | 「运行即结果」，失败即异常 | `SubagentRun` / `Result` + stopReason 五值 | 处理 stopReason；result 不因 child 失败 reject |
| 上下文继承 | 隐式 | `inheritsParentContext` 描述性标注（只担保对话种子） | 别指望 flag 带工具/服务/权限 |
| 续写能力 | 一次性 task 委派 | continuable + followup / interrupt / reportFrom | 要跨 turn 恢复用 continuable |
| 工具调用面 | 框架自动暴露 subagent | dsh-tool-subagent / -control / -report 三件套 | 配置工具实例暴露给模型 |
| 委派深度 | 无显式概念 | maxDepth / delegationDepth（默认 3） | 按 provider 区分配置 |

迁移心智：Claude Code 把 subagent 的「注册、能力、结果、续写」都收敛在框架和 md 文件里，上手快但扩展面小；dsh 把这些全部显式化——代价是你要记更多契约字段和坑，收益是执行后端可替换、生命周期可编程。速查表的使用方式一样：在 Claude Code 侧你查「subagent 怎么写」的文档，在 dsh 侧你查「能力缝怎么补全」的这张表。

## 更新记录与开放问题

> [!warning] developer preview（2026-08-13 锚点）破坏性变更风险
> 整个 dsh subagent 生态锚定在 2026-08-13 的 developer preview：包名、配置、契约都可能破坏性变更。本系列第 2–6 章的坑位、7.1 索引与 7.2 决策依据都以此版本为准；若你读到的版本与本文不一致，先查官方 release notes 与各章更新记录，再决定是否调整选型。

**开放问题（索引，源自 02 素材 §7）：**[^R7]

1. **6.1 骨架 `start()` in-process 实现**——如何用 `ctx.agents` 创建 child 并满足「发布后返回 handle / 发布前清理」，需对照 `subagent-spawn-in-process` 源码。
2. **「无内置 subagent 数量限制」未获官方证实**——本系列按未证实处理，不展开。
3. **codex / claude-code provider 完整 config 表未抓取**——MOC 标注可扩展。
4. **tool-subagent-report README 细节未单独抓取**——写第 6 章时补。
5. **continuable 跨进程所有权契约官方「未设计」**——社区方案 dsh-background-agents（C2）只作经验标注。
6. **cordis.patch.yml 手动挂载精确语法**——需对照配置体系笔记 + C1 第三方插件 insert 示例核实。

- **2026-08-16（成稿）**：本章为全系列速查索引，不新增内容。避坑表、决策表、诚实标注清单分别汇总第 2–6 章坑位、选型依据与三类信心等级；若 preview 更新改变坑位或决策依据，7.1 / 7.2 是受影响区域，优先对照检查。

---

[^S2]: S2 · Subagent 子系统设计文档（中文）——第 2 章坑位契约（UNSUPPORTED_CAPABILITY、outputSchema、inheritsParentContext、start 清理）与委派深度机制出处。
[^S3]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README——第 5 章坑位（消息不可重放、report 需存活父代、跨进程 ownership 未设计）。
[^S5]: S5 · `dsh-subagent-acp` README——acp 零能力、独立子进程语义（§4.7）。
[^S6]: S6 · `dsh-subagent-dsh-sdk` README——dsh-sdk 完整 peer harness、`'provider-managed'`（§4.5/§4.7）。
[^S7]: S7 · `dsh-tool-subagent` README——toolName 唯一、maxDepth 默认 3、后台 one-shot 走 task 工具（§4.8）。
[^S8]: S8 · `subagent-spawn-in-process` README——spawn 无父历史、in-process 四项能力全支持（§4.7）。
[^S56]: S5/S6 §4.9——subagent 系列包无默认导出（postmortem 0001）。
[^R5]: 02 深度研究 §5 矛盾表——坑与细微差别的集中汇总。
[^R7]: 02 深度研究 §7 开放问题——开放问题与 6.1 综合推断的出处。
