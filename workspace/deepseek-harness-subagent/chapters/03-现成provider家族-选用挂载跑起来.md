# 第三章 现成 provider 家族——选用、挂载、跑起来

> [!summary] 导读
> 第 1 章说「六个 provider 兄弟 + 一个工具」，第 2 章把 `SubagentProvider` 契约讲透了。这一章落地到三个实际问题：**选哪个、怎么挂、怎么跑**。六个兄弟不是等价复制品，它们从根上分两个世界——in-process（spawn / fork）和 out-of-process（acp / dsh-sdk），每个都有自己擅长的场景和注定做不到的事。读完你会得到一张决策地图：什么时候选 spawn、什么时候选 fork、什么时候值得上 acp 或 dsh-sdk，以及把选好的 provider 挂进 cordis 插件树、让模型真正调得到它的完整动作。第 1 章承诺的「换执行后端只改一行配置」，这一章你会亲手做一遍。

## 3.1 in-process vs out-of-process：从根上分两个世界

选 provider 的第一个问题不是「哪个能力多」，而是**child 住在哪**。dsh 的 provider 家族从根上分成两派：[^S5-4.7-3][^S6-4.7-4]

- **in-process（进程内）**：child 跑在宿主 harness **同一个进程**里，共享运行时、agent 注册表、工具系统。启动快、开销小，而且因为大家共用一套运行时，**启动期 capabilities（outputSchema / depthLimit / toolFilter / persona）能完整落地**——约束是在同进程内直接施加的。[^S8-4.7-1]
- **out-of-process（独立子进程）**：child 是**独立子进程**，宿主通过协议（ACP / SDK JSON-RPC）握手驱动。隔离更强、更像「把活外包出去」，但代价是**跨进程传不过去的能力约束**——你没法远程强制对方「深度最多几层、只用这几个工具、按这个 schema 输出」。[^S5-4.7-3][^S6-4.7-4]

| 维度 | in-process（spawn / fork） | out-of-process（acp / dsh-sdk） |
| --- | --- | --- |
| child 位置 | 宿主同一进程 | 独立子进程 |
| 启动期 capabilities | 能完整落地 | 受限于协议，多为 false |
| 启动开销 | 低 | 高（每次全新进程） |
| 隔离性 | 弱（共享运行时） | 强 |
| 适合 | 要能力约束、要快 | 要隔离、要驱动外部 agent |

> [!tip] 大白话
> 把 in-process 想成「同一间办公室里的新工位」：新同事（child）和你共用复印机、门禁、前台（宿主运行时和工具系统），随时能叫、启动快，公司内部的各种资质（能力约束）直接就能给；把 out-of-process 想成「把活外包给楼外一家公司」：只能通过合同（协议）对接，对方有没有资质你说了不算。所以……选哪个先看你要不要「跨进程传不过去的能力约束」——要，就走 in-process；要隔离或要驱动外部 agent，才值得上 out-of-process。

> [!note] 这在 Claude Code 里相当于
> Claude Code 的 subagent 永远是框架内置执行，进程模型是框架内部细节，你根本不感知。dsh 把「child 住哪」变成你的显式选择——这是「执行后端可替换」的第一步，也是 Claude Code 用户最需要重建直觉的地方。

## 3.2 四兄弟逐个看

### 3.2.1 spawn：能力全开、空手入职（in-process）

`dsh-subagent-spawn-in-process` 是 in-process 的默认选择：[^S8-4.7-1]

- **四项启动期能力全支持**——`outputSchema` / `depthLimit` / `toolFilter` / `persona` 都能落地，这是它最大的卖点。
- **全新 child、无父历史**——child 从零开始，**看不到父会话聊过什么**。
- `providerName` 默认 `spawn`，配置里不写 provider 名时通常落到它。

> [!warning] 埋坑 ①：spawn 全新 child、无父历史
> 「全新 child」不是小细节，而是继承语义的正反两面：spawn 的能力**全开**，但历史**全无**。如果你想让子代理「接着父对话往下聊」，spawn 给不了——那是 fork 的活（3.2.2）。选 spawn 前先确认「子代理不需要父对话上下文」这个前提成立。

### 3.2.2 fork：唯一带对话种子的 in-process

`fork` 和 spawn 同属 in-process，能力同样全，但**继承语义恰好相反**：[^S1-4.7-2][^S2-4.7-2]

- 从父的**已完成 turn** 种子启动——child 能顺着父对话的思路接续。
- `inheritsParentContext: true`——第 2 章已经拆过，这个 flag 只担保「带对话种子」这一件事，工具 / 服务 / 权限一概不继承。

| 维度 | spawn | fork |
| --- | --- | --- |
| 进程模型 | in-process | in-process |
| 启动期 capabilities | 全支持 | 全支持 |
| 父对话历史 | 无（全新 child） | 有（已完成 turn 种子） |
| `inheritsParentContext` | false | **true** |
| 适合 | 子代理不应被父对话带偏 | 子代理要延续父对话上下文 |

> [!tip] 大白话
> 把 spawn 想成「空手入职的新员工」，fork 想成「接上一任工作笔记的老员工」。新员工工位电脑全配齐（能力全开），但桌上没有前任的笔记——从零干起；老员工入职时把父会话的已完成对话拷进 U 盘带过去，能顺着前面的思路接。所以……能力上 spawn / fork 没差别，差别只在「带不带话」：要子代理接续父对话，就选 fork；要子代理别被父对话带偏，就选 spawn。

### 3.2.3 acp：独立子进程、零启动期能力（out-of-process）

`dsh-subagent-acp` 是 out-of-process 的第一个代表，它把每个 subagent 跑在**独立子进程**里，作为 **ACP（Agent Client Protocol）客户端**驱动。[^S5-4.7-3]

- **不声明任何启动期 capabilities**：acp 无法在远程强制深度 / 工具过滤 / persona / 结构化输出，所以这四项它**全不声明**。
- **本地服务拒绝而非静默忽略**：请求依赖了 acp 不具备的能力，服务会以 `UNSUPPORTED_CAPABILITY` 响亮拒绝（呼应第 2 章），而不是「假装支持、结果不对」。这不是 bug，是设计——**别选 acp 却想要 spawn 的能力**。
- `inheritsParentContext: false`；**每次运行全新进程、无进程池**——跑一次开一个，跑完就销毁。
- 仅限本地工作区。

> [!warning] 埋坑 ②：acp 不声明任何启动期 capabilities
> 想在 acp 上用结构化输出 / 工具过滤 / persona / 强制深度？**别选它**。acp 一个都不声明，请求这些能力的 start 会被 `UNSUPPORTED_CAPABILITY` 响亮拒绝（第 2 章）。这不是「能力弱一点」的降级，而是「明确拒绝」——本地服务宁可拒绝也不静默忽略。要这些能力，回 in-process（spawn / fork）。

> [!tip] 大白话
> 把 acp 想成「外包公司派来的驻场团队」：他们很专业，但拿不到你公司内部的资格清单（没有启动期 capabilities）——你没法远程强制他们「深度最多 3 层、只能用这几个工具、按这个 schema 输出」。所以……acp 适合「只要能跑 ACP 协议的任意 agent」这类场景，但别指望它对子代理做细粒度能力约束——你要的约束对方在墙外接不住，本地服务会**直接拒绝**而不是糊弄你。

### 3.2.4 dsh-sdk：完整 peer harness（out-of-process）

`dsh-subagent-dsh-sdk` 是 out-of-process 的第二个代表，也是最「重」的一个：[^S6-4.7-4]

- 通过 **stdio JSON-RPC** 驱动 harness SDK runtime，子进程是一个**完整 peer harness**——有自己的 cordis 组合、会话、模型路由、工具系统。它不是「一个被驱动的脚本」，而是「一整套独立运行的 dsh」。
- 启动期 capabilities 全 false（和 acp 同理：跨进程传不过去）；`inheritsParentContext: false`。
- **每次 run 都是全新的 runtime 进程**，启动成本**高于 acp 的典型子进程**。
- 子进程的 transcript 留在**子进程自己的 session root**，不跟父会话混在一起。

> [!note] 这在 Claude Code 里相当于
> dsh-sdk 大概是 Claude Code 里最没有直接对应物的一个：它像是「为单个子代理单独起一个完整的 Claude Code 实例」——重、独立、自管一切。Claude Code 里你不会想为一次 task 委派起一个全新实例，但 dsh-sdk 正是为此设计的「完整隔离档位」。

### 3.2.5 codex / claude-code：只列名的外部 CLI 后端

家族里还剩两个外部 CLI 后端：`codex` 和 `claude-code`。[^S1-4.7-5][^S10-4.7-5] 本分册**只列名、不展开**——它们的完整配置表未抓取，属于「本分册未抓取，可扩展」项（第 7 章诚实标注清单会集中列）。你只需要知道：它们和 acp / dsh-sdk 一样属于「外部后端」一族，将来若需要驱动 Codex CLI 或 Claude Code CLI 作为子代理，接口上仍是同一个 provider 口子。

### 3.2.6 全家福对照

| provider | 进程模型 | 启动期 capabilities | 父对话 | 特点 | 成本 |
| --- | --- | --- | --- | --- | --- |
| spawn | in-process | 全支持 | 无 | 能力全、空手 | 低 |
| fork | in-process | 全支持 | **有种子** | 唯一带话的 in-process | 低 |
| acp | out-of-process | 全不声明 | 无 | 驱动任意 ACP agent、每次全新进程（无池） | 中 |
| dsh-sdk | out-of-process | 全 false | 无 | 完整 peer harness、自管模型/组合/递归预算 | 高 |
| codex / claude-code | 外部 CLI | 未抓取 | 未抓取 | 仅列名，可扩展 | — |

## 3.3 环境变量与 cwd：out-of-process 的公共规矩

acp 和 dsh-sdk 虽然是两个 provider，但它们的子进程管理共用同一套 `dsh-subprocess` 语义——两条规矩在写配置时必须遵守。[^S5-4.7-6][^S6-4.7-6][^S5-4.7-7][^S6-4.7-7]

### 3.3.1 环境变量：先擦除、再合并

子进程的环境不是「父环境的复刻」，而是经过两道工序：[^S5-4.7-6][^S6-4.7-6]

1. **先擦除**：「凭据形状」的变量（像 `*_API_KEY` / `*_TOKEN` 这类形似密钥的）和**陈旧的 `DSH_*` 名**（可能残留旧版本的 harness 配置）一律清掉；
2. **再合并**：把显式 `config.env` 里写的变量合进去。

> [!tip] 大白话
> 把环境变量想成「出门前清空口袋再按清单装东西」：先确保口袋里没有上一趟留下的凭据（擦除凭据形状变量）和过期旧证件（陈旧 `DSH_*` 名），再按清单（`config.env`）装你要带的。所以……子进程的环境是「消毒后按需注入」，不是父环境的复制品——目的是防止父会话的密钥或过期配置泄漏进子代理。

### 3.3.2 cwd：绝不用 server 进程自身 cwd

cwd 的优先级是一句背下来的规则：[^S5-4.7-7][^S6-4.7-7]

1. 配置了 `cwd` → 用配置值（在 load 时校验一次）；
2. 没配置 → 用**委托方父会话**的 cwd；
3. **绝不用 server 进程自身的 cwd**。

> [!tip] 大白话
> 把 cwd 想成「在哪张桌上干活」：server 进程自己的 cwd 是「安装地点」，跟这次委托没关系；子代理应该在「叫活的人所在的那张桌」（委托方父会话的 cwd）上干活。所以……cwd 永远先看配置、再看父会话，唯独不看 server 自己站在哪——否则子代理会在一个跟任务无关的目录里乱跑，读写全都落错地方。

## 3.4 挂载：cordis.patch.yml 两行跑起来

选好 provider 之后，把它挂进插件树、暴露给模型，是**配置层**的动作。以 acp 为例，`cordis.patch.yml` 需要两行——一行 provider、一行 tool（底稿见 02 素材 6.3）：[^6.3]

```yaml
# cordis.patch.yml 示例：provider + tool 两行（纯 Cordis 插件，需手动 insert）
- id: subagent-acp
  name: '@deepseek-ai/dsh-subagent-acp'
  config:
    providerName: acp
    command: node
    args: ['--import', 'tsx', './packages/examples/acp-demo/src/bin.ts']
    permission: reject
    env:
      DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config: { provider: acp, toolName: subagent }
```

逐行读：

- **provider 行**（`id: subagent-acp`）：加载 `dsh-subagent-acp` 包。`config.providerName: acp` 是注册进 `ctx.subagents` 的名字（spawn 的默认值就是 `spawn`，这里显式写 `acp`）；`command` / `args` 定义子进程怎么拉起；`permission: reject` 是子进程权限策略；`env` 是显式注入的环境变量——正好用上 3.3.1 的「先擦除再合并」。
- **tool 行**（`id: tool-subagent`）：加载 `dsh-tool-subagent`，`config: { provider: acp, toolName: subagent }` 把 **acp 这个 provider** 绑成一个模型可见的、名叫 `subagent` 的工具——**一个 provider 绑一个 toolName**，toolName 全局唯一（默认 `subagent`，工具层的完整字段在第 6 章展开）。[^S7-4.8-1]

> [!warning] 埋坑 ③：subagent 系列是纯 Cordis 插件，必须手动 insert
> 第 1 章提过、这里落地：subagent 系列包**都是纯 Cordis 插件**（没有 `dsh.bundle.patch`）。这意味着 `dsh plugin add` 只让包「可被解析」，**并不会把它挂进插件树**——你还得手动在 `cordis.patch.yml` 里 insert 一条，它才会真正被加载。这是和「自带 bundle 配置」的插件最不一样的地方，忘了 insert，包装好了却毫无作用。

> [!tip] 大白话
> 把 `dsh plugin add` 想成「把新书记进书店的进货清单」：仓库（包解析）知道有这本书了，但书还没摆上货架（插件树）。纯 Cordis 插件要再「手动上架」——在 `cordis.patch.yml` 里 insert 一条，它才会真正被顾客（模型）看到。所以……subagent 包 add 完不等于能用，记得手动 insert。

两点诚实标注（本分册约定，成稿时保留）：

1. **acp 命令参数以 02 素材 6.3 为准**（示例里是一个 demo bin 路径），**需对照 S5 README 核实**后再用于你的项目；
2. **手动 insert 的精确语法**标注为**需对照配置体系笔记 + C1 第三方插件示例核实**——`cordis.patch.yml` 的完整 schema 细节见 [[DeepSeek-Harness 配置体系]]。

## 3.5 选择 provider：一张决策表

把上面的特性收敛成选择依据（02 素材 6.4）：[^6.4]

| 需求 | 选 | 依据 |
| --- | --- | --- |
| 想要结构化输出 / 工具过滤 / persona / 深度强制 | spawn / fork | in-process 能力全（S8/S2） |
| 想要完整独立 harness（自管模型 / 组合 / 递归预算） | dsh-sdk | 完整 peer harness（S6） |
| 想要驱动任意 ACP 协议 agent | acp | ACP 客户端驱动（S5） |
| 想要子代理继承父对话上下文 | fork | 唯一带种子的 in-process（S2） |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | 均无父历史（S2/S5/S6） |

用法建议：

1. **默认问句**：子代理要不要父对话？要 → fork；不要 → 继续往下问。
2. **第二问句**：要不要 in-process 才能给的能力约束（结构化输出 / 工具过滤 / persona / 强制深度）？要 → spawn；不要 → 看第三问。
3. **第三问句**：要驱动外部 agent 吗？驱动任意 ACP 协议 agent → acp；要完整独立 harness（连模型路由都自己管）→ dsh-sdk；驱动 Codex / Claude Code CLI → 留给后续分册扩展。

第 1 章那句「换执行后端只改一行配置」，到这里就是：把 `cordis.patch.yml` 里 tool 行的 `config.provider` 从 `acp` 改成 `spawn`，再换上对应 provider 行——定义包和工具一行都不用动。写自己的 provider（第 4 章）时，in-process 的 `start()` 走 `ctx.agents`，out-of-process 的 `start()` 要握手 ACP / SDK initialize，这两条路在第 4 章分别展开。

## 本章小结

- provider 家族从根上分两派：in-process（spawn / fork）能力全、开销低；out-of-process（acp / dsh-sdk）隔离强、但跨进程能力约束传不过去。
- spawn 能力全开、全新 child 无父历史；fork 是唯一带对话种子的 in-process（`inheritsParentContext: true`，但只担保对话种子）。
- acp 不声明任何启动期 capabilities，本地服务**拒绝而非静默忽略**；每次运行全新进程（无池）；dsh-sdk 是完整 peer harness，自管模型 / 组合 / 递归预算，每次全新 runtime 进程、成本最高。
- codex / claude-code 仅列名，配置表本分册未抓取，可扩展。
- out-of-process 公共规矩：环境变量先擦除凭据形状变量与陈旧 `DSH_*` 名、再合并 `config.env`；cwd 优先配置、其次父会话 cwd，**绝不用 server 进程自身 cwd**。
- 挂载是配置层动作：`cordis.patch.yml` 的 provider + tool 两行；subagent 系列是纯 Cordis 插件，`dsh plugin add` 之后必须手动 insert 才生效。
- 选择决策：父对话 → fork；能力约束 → spawn；驱动外部 agent → acp / dsh-sdk；换执行后端只改配置一行。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 执行后端 | 内置唯一实现，不可换 | provider 全家桶，配置一行切换 |
| 首问 | 「subagent 用什么引擎跑」不是个问题 | 第一问题：spawn / fork / acp / dsh-sdk |
| 进程模型 | 框架内部细节，用户不感知 | in-process vs out-of-process 是显式选择 |
| 上下文继承 | 隐式 | fork 显式带种子（`inheritsParentContext: true`） |
| 挂载 | 丢一个 md 文件即自动发现 | 纯 Cordis 插件需手动 insert 进 `cordis.patch.yml` |

迁移心智：Claude Code 里「执行后端」是个伪问题——内置唯一实现，你没得选；dsh 把它降级成配置里的一个字符串，于是「选哪个 provider」成了使用 subagent 的第一决策点。Claude Code 用户最容易踩的三处是：以为所有 provider 能力一样（其实 acp 零能力约束）、以为 add 包就能用（其实要手动 insert）、以为父对话会自动继承（其实只有 fork 带种子）。这三条分别对应本章埋的 ①③② 三个坑，跑起来之前先对一遍。

## 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档。provider 特性对照引自 S8 / S1/S2 / S5 / S6 README 与子系统文档；`cordis.patch.yml` 底稿来自 02 素材 6.3，acp 命令参数需对照 S5 README 核实、手动 insert 精确语法需对照 [[DeepSeek-Harness 配置体系]] + C1 第三方插件示例核实。若 preview 更新改变 provider 的 capabilities 声明、子进程环境/cwd 语义或配置 schema，本章 3.2-3.4 是受影响区域，优先对照检查。codex / claude-code 配置表未抓取，留待后续分册扩展。

---

[^S8-4.7-1]: S8 · `subagent-spawn-in-process` README §4.7——spawn：in-process、全新 child 无父历史、四项启动期能力全支持、`providerName` 默认 `spawn`。
[^S1-4.7-2]: S1 · Subagent 子系统设计文档（EN）§4.7——fork 从父已完成 turn 种子启动。
[^S2-4.7-2]: S2 · Subagent 子系统设计文档（中文）§4.7——fork 的 `inheritsParentContext: true`。
[^S5-4.7-3]: S5 · `dsh-subagent-acp` README §4.7——acp：out-of-process、独立子进程、ACP 客户端驱动、零启动期 capabilities、本地服务拒绝而非静默忽略、每次全新进程（无池）、仅本地工作区。
[^S6-4.7-4]: S6 · `dsh-subagent-dsh-sdk` README §4.7——dsh-sdk：stdio JSON-RPC 驱动、完整 peer harness（自管 cordis 组合/会话/模型路由/工具）、启动期 capabilities 全 false、每次 run 全新 runtime 进程、成本更高、transcript 留在子进程自己的 session root。
[^S1-4.7-5]: S1 §4.7——codex / claude-code 外部 CLI 后端仅列名。
[^S10-4.7-5]: S10 · 扩展 Cookbook §4.7——provider 家族全景（六兄弟 + tool）。
[^S5-4.7-6]: S5 §4.7——acp 环境变量处理（dsh-subprocess 语义：先擦除凭据形状变量与陈旧 `DSH_*` 名，再合并显式 `config.env`）。
[^S6-4.7-6]: S6 §4.7——dsh-sdk 同用 `dsh-subprocess` 环境变量语义。
[^S5-4.7-7]: S5 §4.7——acp cwd 规则（配置优先且在 load 时校验一次、否则父会话 cwd、绝不用 server 进程自身 cwd）。
[^S6-4.7-7]: S6 §4.7——dsh-sdk 同 cwd 规则。
[^S7-4.8-1]: S7 · `dsh-tool-subagent` README §4.8——一个 provider 绑一个 toolName（默认 `subagent`）、`config.provider` 必填、toolName 全局唯一。
[^6.3]: 02 深度研究 §6.3——`cordis.patch.yml` 挂载底稿（acp provider + tool 两行）；acp 命令参数以 6.3 为准、需对照 S5 README 核实；纯 Cordis 插件需手动 insert。
[^6.4]: 02 深度研究 §6.4——选择 provider 决策依据表。
