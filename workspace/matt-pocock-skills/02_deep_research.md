# Matt Pocock Skills - 深度研究素材

> 收集时间: 2026-07-23
> 项目源: https://github.com/mattpocock/skills (184K+ stars)
> 学习目标: 提取可复用的 Agent 框架设计原则，用于构建自己的 Agent 项目框架

---

## 第一部分：仓库核心文件完整内容

### 1.1 CLAUDE.md / AGENTS.md — 项目结构规则

两个文件内容相同，作为 Claude Code 和 Codex 两个平台的**跨系统契约**。

**核心规则：**
- Skills 按 bucket 目录组织：`engineering/`（日常编码）、`productivity/`（日常非编码）、`misc/`（保留但不推广）、`personal/`（个人）、`in-progress/`（草稿）、`deprecated/`（废弃）
- **Promoted buckets**（engineering 和 productivity）必须出现在 `README.md` 和 `.claude-plugin/plugin.json` 中
- 非 promoted buckets 不得出现在上述位置
- 每个 promoted skill 有对外文档页 `docs/<bucket>/<skill-name>.md`
- `ask-matt` 是中央路由器，随技能变更同步更新
- 双分发机制: skills.sh 安装器（可编辑）+ Claude Code Plugin（只读自动更新）

**设计原则: Bucketed curation with promotion gates** — 并非所有 skill 都平等，通过 bucket 实现发布/草稿生命周期管理。CLAUDE.md 是仓库结构规则的单一真相源。

---

### 1.2 CONTEXT.md — 领域模型与共享词汇

定义了整个 skill 系统的**通用语言（Ubiquitous Language）**：

| 术语 | 定义 | 禁止词 |
|------|------|--------|
| Issue tracker | 托管 Issue 的工具（GitHub Issues, Linear 等） | backlog manager, backlog backend, issue host |
| Issue | 一个工作单元 | ticket（仅在引用外部系统或用 Decision ticket 时可用） |
| Decision ticket | wayfinder 的子 Issue，其决议是决策而非构建 | — |
| Triage role | Issue 上的状态机标签 | — |

**关系模型：**
- Issue tracker 包含多个 Issues
- Issue 同时携带一个 Triage role
- Decision ticket 是 Issue 的子类型（wayfinder:map 的子节点）

**Flagged ambiguities 部分** 记录了已解决的术语冲突（例如 "backlog" 曾既指工具又指工作集）。

**设计原则: Domain glossary as architectural boundary object** — 所有 skill 共享的词汇表，通过 `_Avoid_` 指令防止术语漂移，通过 "Flagged ambiguities" 追踪已解决的混淆。

---

### 1.3 .agents/invocation.md — 调用模型

整个分类体系只有一个轴：**invocation（调用方式）**。

- **User-invoked**: `disable-model-invocation: true` + `policy.allow_implicit_invocation: false`，仅人类可调用。description 面向人类（一行摘要，无触发词列表）。其他 skill 无法触发它。
- **Model-invoked**: 默认状态。模型和人类都可调用。description 面向模型，包含丰富的触发词。其他 skill 可以通过名称引用它。

Skill 之间的依赖通过 `/skill` 风格的散文式引用表达（"Run the `/grilling` skill"），而非深度交叉引用。共享参考文档存在于拥有它的 skill 内部。

---

### 1.4 .agents/adr/ — 架构决策记录

**ADR-0001: 仅对硬依赖使用显式 setup 指针**

依赖分为硬（to-tickets, to-spec, triage）和软（diagnose, tdd, improve-codebase-architecture）：
- 硬依赖：必须包含 "run `/setup-matt-pocock-skills`" 指针，否则输出错误
- 软依赖：仅在散文中引用领域词汇表，无 setup 指针；无 setup 时退化为次优但仍可用

**设计原则: 硬/软依赖分离** — 防止 cargo-culting setup 指针到无需的地方，节省 token。

**ADR-0002: 以 Claude Code Plugin 形式分发，推迟 Codex Plugin**

Claude Code 的 `plugin.json` 接受 skills 为显式路径**数组**，能精确挑选 promoted 子集。Codex 只接受单个路径字符串，无法从 bucketed 结构中挑选子集。两种被拒方案：重构目录结构（影响面大）或提交重复副本（同步负担）。

**设计原则: 平台特定分发的 deferred symmetry** — 先发能发的，技术限制原因明确记录，被拒替代方案和技术原因留档。

---

### 1.5 writing-great-skills — 元技能设计

这是 repo 中最重要的文件，定义了 skill 设计的完整词汇和原则。参见第二部分详述。

---

### 1.6 grill-me / grilling / grill-with-docs — 三层抽象

| Skill | Invocation | 状态 | 职责 |
|-------|-----------|------|------|
| `grill-me` (3行) | User-invoked | 无状态 | 委托给 `grilling` |
| `grilling` (10行) | Model-invoked | — | 核心盘问原语 |
| `grill-with-docs` (3行) | User-invoked | 有状态 | 委托给 `grilling` + `domain-modeling` |

**grilling 核心指令：**
```
- 一次问一个问题，带推荐答案
- 走决策树的每个分支，逐个解决依赖
- 事实查环境（代码库、工具），决策问用户
- 直到用户确认达成共识才行动
```

**设计原则: Stateless vs Stateful 分离** — 相同行为核心（grilling），不同状态策略（grill-me 不留痕迹，grill-with-docs 写 CONTEXT.md + ADRs）。

---

### 1.7 handoff — 跨会话上下文压缩

**核心规则：**
- 压缩当前会话为交接文档，保存到 OS 临时目录（非工作区）
- 包含 "suggested skills" 章节
- 不复制已有 artifacts（specs, plans, ADRs, commits）中的内容 — 通过路径/URL 引用
- 过滤敏感信息（API keys, passwords, PII）
- 支持参数：描述下个会话的焦点

**设计原则: handoff vs compact 的明确区分** — `/handoff` 分叉（新会话），`/compact` 继续（同会话）。handoff 是"对话被榨干到可恢复的核心，让新 agent 继承动量而非噪音"。

---

### 1.8 ask-matt — 中央路由器

定义了完整的 **idea-to-ship 主流程**：

1. `/grill-with-docs` — 盘问对齐
2. 分支：需要原型 → `/handoff` 出去 → `/prototype` → `/handoff` 回来
3. 分支：多会话构建？→ `/to-spec` → `/to-tickets` → 每 ticket 一个 `/implement`
   - 单会话 → 直接 `/implement`
4. 每个 `/implement` 内部驱动 `/tdd` → 完成后 `/code-review` → commit

**上下文卫生规则：**
- 步骤 1-3 在同一个上下文窗口完成，不 compact 不清除直到 `/to-tickets`
- 每个 `/implement` 从新会话开始
- Smart Zone 限制：约 12 万 token，超限用 `/handoff` 分叉

---

### 1.9 codebase-design — 深模块词汇表

受 John Ousterhout《A Philosophy of Software Design》影响。定义了统一词汇：

- **Module** — 有 interface 和 implementation 的任何东西
- **Interface** — 调用者必须知道的所有信息（类型签名 + 约束 + 错误模式 + 性能特征）
- **Depth** — 每单位 interface 能调用的行为量
- **Seam** — 可改变行为而无需在那编辑的地方
- **Adapter** — 在 seam 处满足 interface 的具体实现

核心工具：**删除测试**（deletion test）— 想象删掉这个模块，如果复杂度消失，它是透传层；如果复杂度在 N 个调用方重现，它在创造价值。

**DESIGN-IT-TWICE.md**: 并行子代理模式，派发 3+ 子代理用不同约束设计同一接口。

---

## 第二部分：Skill 设计理论体系（writing-great-skills）

### 2.1 核心美德：可预测性（Predictability）

Skill 存在的意义是从随机系统中提取确定性。**可预测性**— agent 每次运行采用相同**过程**，而非产生相同**输出** — 是所有杠杆服务的根本美德。

### 2.2 调用权衡

| 维度 | User-invoked | Model-invoked |
|------|-------------|---------------|
| 上下文负载 | 零 | 高（description 每轮加载） |
| 认知负载 | 高（人类必须记住它存在） | 低 |
| 可发现性 | 仅人类 | Agent + 人类 |
| 其他 Skill 可调用 | 否 | 是 |
| 适用场景 | 仅手动触发 | agent 需要自主触发 / 其他 skill 需要调用 |

### 2.3 信息层级（Information Hierarchy）

内容是分级的，按 agent 需要它的紧急程度排列：

1. **In-skill step** — SKILL.md 中的有序动作。每步以 completion criterion 结束。
2. **In-skill reference** — SKILL.md 中的定义/规则/事实，按需查阅。
3. **External reference** — 从 SKILL.md 推到独立文件，通过 context pointer 按需加载。

**Progressive disclosure** = 沿梯子向下推，保持顶部可读。

**Co-location** = 处于同一梯级的内容保持在一起，不分散。

### 2.4 Leading Words（引导词）

来自模型预训练的紧凑概念，agent 在运行 skill 时用它来思考（如 lesson, fog of war, tracer bullets）。

双倍效果：
- 在 body 中锚定**执行**：每次出现都让 agent 做同样的事
- 在 description 中锚定**调用**：当 prompt/docs/code 中使用同一词汇时，agent 更可靠地触发 skill

例子：用 `tight` 替代 "fast, deterministic, low-overhead"；用 `red` 替代 "a loop you believe in"。

### 2.5 何时拆分 Skill

两个合理拆分点：
1. **By invocation** — 当有一个独立的 leading word 应该触发它，或其他 skill 需要调用它时
2. **By sequence** — 当后续步骤导致 agent 过早完成当前步骤时

### 2.6 修剪原则

- **Single source of truth**: 每个含义只在一个权威位置
- **Relevance**: 保持相关，去除过时
- **No-op test**: 删除后行为不变吗？如果是，删除它

### 2.7 六种失败模式

| 失败模式 | 描述 | 防御 |
|---------|------|------|
| **Premature completion** | 步骤未真正完成就提前结束 | 强化 completion criterion → 拆分后续步骤 |
| **Duplication** | 同一含义多处出现 | 单一真相源 |
| **Sediment** | 沉积的过时内容 | 修剪纪律 |
| **Sprawl** | Skill 太长（即使每行都活跃） | 信息层级：向下推 reference |
| **No-op** | 不改行为的指令 | 删除而不是重写 |
| **Negation** | 负面指令反效果 | 正面描述目标行为 |

### 2.8 完成标准（Completion Criterion）

两个维度：
- **Clarity**: agent 能否区分完成与未完成？防过早完成
- **Demand**: 要求的彻底程度，设定 legwork 量

最强的标准：既可检查又穷尽。

---

## 第三部分：十大架构模式总结

| # | 模式 | 描述 | 代表文件 |
|---|------|------|---------|
| 1 | **Bucketed curation** | Bucket 目录实现发布/草稿生命周期 | CLAUDE.md |
| 2 | **Two-tier invocation** | User-invoked vs model-invoked 的明确权衡 | invocation.md, 各 SKILL.md |
| 3 | **Router skill** | ask-matt 作为认知负载的解药 | ask-matt/SKILL.md |
| 4 | **Core primitive + wrapper** | grilling 为核心，grill-me/grill-with-docs 为薄封装 | grill-me, grilling, grill-with-docs |
| 5 | **Progressive disclosure** | 信息层级：步骤 > 参考 > 外部引用 | writing-great-skills |
| 6 | **Leading words** | 利用模型先验的紧凑概念锚 | writing-great-skills 体系 |
| 7 | **Domain glossary** | CONTEXT.md 作为跨 skill 词汇契约 | CONTEXT.md |
| 8 | **ADR for decisions** | 架构决策记录（被拒方案 + 原因） | .agents/adr/ |
| 9 | **Failure mode vocabulary** | 六种失败的诊断语言 | writing-great-skills + GLOSSARY.md |
| 10 | **Context hygiene** | 会话窗口管理规则 + handoff 桥接 | ask-matt, handoff |

---

## 第四部分：外部资料与社区分析

### 4.1 深度分析文章

**文章 1: 告别 AI 制造的"代码泥球"——Matt Pocock 工程师级 Agent Skills 架构全解析**
- URL: https://cloud.tencent.com.cn/developer/article/2666153
- 核心观点：定义四层模型 User → Entrypoint → Skill Buckets → Config
- 解释了硬/软依赖治理模型：硬依赖配置错误时报错，软依赖优雅降级
- 盘问协议四阶段：主动探索 → 词汇对齐 → 收敛确认 → 架构沉积
- 核心论断："AI 辅助开发质量的上限由工程纪律设定，而非模型基准"

**文章 2: 拒绝 Vibe Coding——Matt Pocock 的工程级 Claude Code Skills 仓库精读**
- URL: https://cloud.tencent.com.cn/developer/article/2704288
- 三大值得复制的设计：Grilling（12行足矣）、Diagnosing bugs（90%工作是建反馈回路）、Codebase design（统一术语表 + 删除测试）
- 完整的流程管线：grill-with-docs → to-prd → to-issues（同一窗口）→ implement per issue（新会话）
- "Smart Zone" 约 12 万 token

**文章 3: 12 行 vs 689 行——mattpocock/skills 与 superpowers 的路线之争**
- URL: https://cloud.tencent.com.cn/developer/article/2706290
- Matt 的假设："模型大多做对的事" → 提供最小锚点
- Superpowers 的假设："模型会走捷径" → 掌控流程
- Matt 的核心 skill 仅 12 行依靠：leading words + progressive disclosure + 清晰的完成标准 + 否定回避
- 核心规则：User-invoked skill 可调用 model-invoked，但绝不调用另一个 user-invoked

### 4.2 社区评测

**评测 1: I Tried the Claude Code Skills Repo (dev.to)**
- 优点：grill-with-docs 最有价值，项目术语表后续省 token
- 局限：Skill 是指令集而非插件，不适合快速原型，28 个一次装太多
- 建议：从 4 个核心开始逐步扩展

**评测 2: 一周使用体验 (Devtalk)**
- 最大收获："思考方式的改变"而非单纯效率提升
- 盘问流程在小项目中显得过于正式和耗时

### 4.3 博客与播客

**播客 1: Matt Pocock — 用检查清单终结 AI Agent 的技能地狱**
- 引入 skill 质量的四个维度：Trigger（如何调用）、Structure（SKILL.md < 100行）、Guidance（leading words）、Pruning（去除死重）
- 多数 skill 失败源于：太长、太模糊、完成标准不清晰

**播客 2: Matt Pocock — 开发者如何用 AI 放大十倍产出**
- 战术 vs 战略编程：AI 处理战术工作，开发者聚焦战略（架构、分解、测试策略）
- "你的 skills 是 AI 能成就的上限"
- AFK Agents: 异步运行在任务队列上，通过 GitHub Actions 实现自动 PR review

### 4.4 质量关卡（社区衍生）

从 Matt 的方法论衍生出六项强制质量关卡：
1. Description 包含触发词（"Use when..."）
2. SKILL.md 不超过 100 行（防过度条件化 agent）
3. 无时间敏感信息（无日期/版本声明）
4. 术语一致（无同义词漂移）
5. 包含具体示例（防幻觉）
6. 引用仅一级深度（深层嵌套导致 agent 放弃）

---

## 第五部分：与本项目的对比

| 对比维度 | 本项目 | mattpocock/skills |
|---------|--------|-------------------|
| 设计哲学 | 工作流编排（planner → orchestrator → 模板） | 松散可组合的指令集（small, adaptable, composable） |
| 安装方式 | 项目内置 .claude/skills/ | npx skills@latest add 或 Plugin 市场 |
| 技能结构 | SKILL.md + 模板/参考文件 | SKILL.md（<100行）+ references/ 子目录 |
| 状态管理 | workflow state file + 断点恢复 | 无统一状态管理，依赖上下文窗口 |
| 核心流程 | 单线程研究笔记生产 | 通用 AI 编码 idea-to-ship |
| 适用场景 | 学习笔记自动化生产 | 通用软件工程 AI 辅助 |
| 错误处理 | 结构化检查点 + 回退路径 | Skill 内部反模式文档化 + 断点 |
| 上下文管理 | 逐章处理 + token 优化规则 | Smart Zone（~12万 token）+ /handoff 分叉 |

### 对本项目最有借鉴价值的模式

1. **Bucket 目录组织** — 用 promotion gates 实现发布/草稿生命周期，解决技能多了之后的管理问题
2. **User-invoked vs Model-invoked 分离** — 严格的调用边界，防止不受控的链式反应
3. **Leading words 替代冗长指令** — 利用模型先验减少 token 消耗
4. **信息层级 + 渐进式披露** — 保持顶层可读，细节按需加载
5. **盘问原语** — 一次一问 + 带推荐答案，适合本项目的意图澄清阶段
6. **Handoff 机制** — 跨会话上下文桥接，适合长时间的研究笔记项目
7. **Failure mode 诊断语言** — 系统性地诊断和改进技能质量
8. **硬/软依赖分离** — 关键路径必须配置正确，非关键路径优雅降级

---

## 素材索引

| 编号 | 内容 | 位置 |
|------|------|------|
| [R1] | CLAUDE.md — 结构规则 | /tmp/skills/CLAUDE.md |
| [R2] | CONTEXT.md — 领域词汇 | /tmp/skills/CONTEXT.md |
| [R3] | Invocation 模型 | /tmp/skills/.agents/invocation.md |
| [R4] | ADR-0001 硬/软依赖 | /tmp/skills/.agents/adr/0001-*.md |
| [R5] | ADR-0002 Plugin 分发 | /tmp/skills/.agents/adr/0002-*.md |
| [R6] | writing-great-skills 元技能 | /tmp/skills/skills/productivity/writing-great-skills/SKILL.md |
| [R7] | GLOSSARY.md 完整词汇表 | /tmp/skills/skills/productivity/writing-great-skills/GLOSSARY.md |
| [R8] | grill-me | /tmp/skills/skills/productivity/grill-me/SKILL.md |
| [R9] | grilling 核心原语 | /tmp/skills/skills/productivity/grilling/SKILL.md |
| [R10] | grill-with-docs | /tmp/skills/skills/engineering/grill-with-docs/SKILL.md |
| [R11] | handoff | /tmp/skills/skills/productivity/handoff/SKILL.md |
| [R12] | ask-matt 路由器 | /tmp/skills/skills/engineering/ask-matt/SKILL.md |
| [R13] | implement | /tmp/skills/skills/engineering/implement/SKILL.md |
| [R14] | codebase-design 深模块 | /tmp/skills/skills/engineering/codebase-design/SKILL.md |
| [E1] | 架构全解析（腾讯云） | https://cloud.tencent.com.cn/developer/article/2666153 |
| [E2] | 仓库精读（腾讯云） | https://cloud.tencent.com.cn/developer/article/2704288 |
| [E3] | Skills vs Superpowers 对比 | https://cloud.tencent.com.cn/developer/article/2706290 |
| [E4] | 播客：检查清单终结技能地狱 | https://podcasts.apple.com/.../id1850900599 |
| [E5] | 播客：AI 放大十倍产出 | https://www.xiaoyuzhoufm.com/... |
| [E6] | 第三方对比评测 | https://github.com/addyosmani/agent-skills/... |
| [E7] | 实战评测 dev.to | https://dev.to/... |
| [E8] | 社区一周体验 | https://forum.devtalk.com/... |
