# Matt Pocock Skills — Agent 框架设计深度解析

> 大纲类型：概念笔记 + 实战笔记
> 总章节数：8 章
> 阅读方式：按顺序阅读，第 8 章是全书的应用落脚点

---

## 第 1 章：项目概览与设计哲学

**篇幅**: 中等（约 1500 字）
**素材引用**: [R1], [E1], [E2], [E3]

### 1.1 仓库背景
- Matt Pocock 是谁（TypeScript 专家、知名教育者）
- Skills 仓库的起源与目标（"Skills for Real Engineers"）
- 184K+ stars 背后的需求信号

### 1.2 四大问题域与对应方案
- 对齐问题 → Grilling 体系
- 冗余问题 → CONTEXT.md + 共享词汇
- 代码质量问题 → TDD + 调试 discipline
- 架构衰退 → Codebase design + 定期改进

### 1.3 设计哲学总览
- Small、Adaptable、Composable 三原则
- "模型大多做对的事" vs "模型会走捷径"的路线选择（对比 superpowers）[E3]
- 与"本项目"的设计哲学对比：工作流编排 vs 松散可组合指令集

### 1.4 核心概念速览
- Bucket 目录体系
- User-invoked / Model-invoked 二分
- Skill 即指令集（不是插件）
- 适用场景与局限

---

## 第 2 章：仓库架构与目录组织

**篇幅**: 中等（约 2000 字）
**素材引用**: [R1], [R2], [R5], [E1]

### 2.1 Bucketed Curation 模式
- 六种 bucket 的角色：engineering、productivity、misc、personal、in-progress、deprecated
- Promotion gates：什么能进 README 和 plugin
- 发布/草稿生命周期管理

### 2.2 CLAUDE.md / AGENTS.md 双文件契约
- 跨平台（Claude Code + Codex）的同一套规则
- 结构规则作为单一真相源

### 2.3 CONTEXT.md — 领域词汇表
- Ubiquitous Language 在 Agent 项目中的实践
- `_Avoid_` 指令防止术语漂移
- Flagged ambiguities 追踪已解决的混淆
- **对你自建框架的启示**: 你的项目需要共享词汇表吗？怎么写？

### 2.4 ADR 机制 — 架构决策记录
- ADR-0001: 硬/软依赖分离（setup 指针仅用于硬依赖）
- ADR-0002: 平台特定分发策略（Claude Plugin vs Codex）
- **模式**: 记录被拒方案 + 技术原因，不仅仅是记录决定

### 2.5 双分发机制
- skills.sh 安装器（可编辑，适合修改）
- Claude Code Plugin（只读，自动更新）
- 各自的适用场景

### 2.6 代码示例：典型目录结构
```
skills/
  engineering/     # 已推广
  productivity/    # 已推广
  misc/           # 保留不推广
  personal/       # 个人不推广
  in-progress/    # 草稿
  deprecated/     # 废弃
docs/<bucket>/<skill-name>.md  # 对外文档
```

---

## 第 3 章：调用模型深度解析

**篇幅**: 较大（约 2500 字）
**素材引用**: [R3], [R6], [R7], [E3]

### 3.1 为什么 invocation 是核心轴
- 整个分类体系只有一个轴：调用方式
- Context Load vs Cognitive Load 的根本权衡

### 3.2 User-Invoked 模式
- 特征：`disable-model-invocation: true`，零上下文负载
- 代价：认知负载（你得记住它存在）
- 适用场景：仅手动触发的操作
- 局限：其他 skill 无法调用它

### 3.3 Model-Invoked 模式
- 特征：有 description，agent 可自主发现和触发
- 代价：上下文负载（description 每轮在上下文中）
- 适用场景：agent 需要自主触发的行为，或作为共享参考

### 3.4 选择决策树
```
需要 agent 自主触发吗？
├── 是 → Model-invoked（付 context load 的代价）
└── 否 → 需要其他 skill 调用吗？
    ├── 是 → Model-invoked
    └── 否 → User-invoked（付 cognitive load 的代价）
```

### 3.5 Router Skill 模式
- ask-matt 是怎么工作的
- Cognitive load 的解药：用一个 skill 记住所有 skill
- 什么情况下需要 router？阈值判断

### 3.6 核心规则：调用边界
- User-invoked 可调用 model-invoked
- User-invoked 绝不调用另一个 user-invoked
- **对你自建框架的启示**: 你的项目中如何规划调用边界？

---

## 第 4 章：SKILL.md 编写艺术

**篇幅**: 最大（约 3500 字）
**素材引用**: [R6], [R7], [E4], [E6]

### 4.1 核心美德：可预测性
- 定义：相同过程，非相同输出
- 为什么是所有杠杆服务的根本

### 4.2 信息层级（Information Hierarchy）
- 三梯级：In-skill step → In-skill reference → External reference
- Progressive disclosure：把细节推下去，顶层保持可读
- Co-location：相关内容不分散
- Context pointer：措辞决定触发可靠性

### 4.3 Completion Criterion（完成标准）
- Clarity：是否可检查（agent 能否判断做完没有）
- Demand：是否穷尽（防止偷懒）
- **常见反例**："理解达成"而不是"每个修改的模型已核对"

### 4.4 Leading Words（引导词）
- 来自模型预训练的紧凑概念
- 双倍效果：锚定执行 + 锚定调用
- 例子：tight 替代 "fast, deterministic, low-overhead"
- **对你自建框架的启示**: 你的项目中可以用哪些 leading words？

### 4.5 修剪原则
- Single source of truth: 每含义只一个权威位置
- Relevance: 是否还与 skill 做的事情相关？
- No-op test: 删掉它会改变行为吗？

### 4.6 六种失败模式详解
| 模式 | 识别信号 | 修复方案 |
|------|---------|---------|
| Premature completion | agent 跳过关键步骤 | 强化完成标准 / 拆分步骤 |
| Duplication | 同一概念多处描述 | 归并到单一真相源 |
| Sediment | 过时内容沉积 | 定期修剪纪律 |
| Sprawl | SKILL.md 超 100 行 | 向下推 reference |
| No-op | "仔细检查"等默认行为 | 删除（别重写） |
| Negation | "不要想大象" | 正面描述目标 |

### 4.7 质量关卡（社区实践经验）
- Description 含触发词
- SKILL.md ≤ 100 行
- 无时间敏感信息
- 术语一致
- 含具体示例
- 引用仅一级深度

### 4.8 代码示例：高质量的 SKILL.md 模板
```markdown
---
name: my-skill
description: Use when [具体触发场景].
disable-model-invocation: true
---

# My Skill

[1-2 句话描述核心行为]

## Steps
1. [第一步，以完成标准结束]
2. [第二步，以完成标准结束]

## Reference
- [关键规则 1]: [清晰定义]
- [关键规则 2]: [清晰定义]
```
- 行数控制在 30-50 行以内

---

## 第 5 章：对话边界澄清 — Socratic Sparring 模式

**篇幅**: 中等（约 2000 字）
**素材引用**: [R8], [R9], [R10], [E2], [E3]

### 5.1 三层抽象架构
```
grill-me (user-invoked, 3行, 无状态)
  └── 委托 → grilling (model-invoked, 10行, 核心原语)

grill-with-docs (user-invoked, 3行, 有状态)
  └── 委托 → grilling + domain-modeling
```

### 5.2 grilling 核心原语详解
- 一次问一个问题（带推荐答案）
- 走决策树每个分支，逐个解决依赖
- 事实查环境，决策问用户
- 直到"共享理解"才行动

### 5.3 为什么 12 行就够了
- "grill" 是 leading word（模型预训练中已有）
- 单次一问防 bewildering
- 推荐答案减少决策疲劳
- 不重复用户已知的事实（查环境）

### 5.4 有状态 vs 无状态设计
- grill-me: 不留痕迹，适合无代码库场景
- grill-with-docs: 生成 CONTEXT.md + ADRs，适合项目环境
- **对你自建框架的启示**: 你的澄清阶段应该是什么策略？

### 5.5 适合你的项目的简化版
- 当前项目的意图澄清阶段如何借鉴
- 从"收集信息"升级为"共识对齐"
- 推荐答案模式在笔记项目中的变体

---

## 第 6 章：上下文管理 — Handoff 与 Context Compaction

**篇幅**: 中等（约 2000 字）
**素材引用**: [R11], [R12], [E2], [E3]

### 6.1 Context Hygiene（上下文卫生）
- Smart Zone 概念：约 12 万 token
- 超限前的应对策略
- "步骤 1-3 同一窗口，每个 implement 新会话"

### 6.2 Handoff 机制详解
- 压缩当前会话为交接文档
- 保存到 OS 临时目录（不污染工作区）
- 不复制已有 artifacts（通过路径引用）
- 含 "suggested skills" 章节
- 过滤敏感信息

### 6.3 Handoff vs Built-in Compact
| 维度 | /handoff | /compact |
|------|---------|----------|
| 方向 | 分叉→新会话 | 继续→同会话 |
| 信息保留 | 结构化文档 | 前文摘要 |
| 适用场景 | 长时间中断、原型探索 | 阶段间过渡 |
| 风险 | 低（显式重建上下文） | 中（可能丢失细节） |

### 6.4 在你的项目中的应用
- 长时间研究笔记项目的中断恢复
- 多篇笔记间的上下文切换
- 简化版 handoff 模板：何时生成、包含什么

---

## 第 7 章：可组合工作流设计

**篇幅**: 较大（约 2500 字）
**素材引用**: [R12], [R13], [R14], [E1]

### 7.1 ask-matt 路由器 — 工作流的"全面图"
- 主流程（idea → ship）
- 三个 on-ramp（triage、diagnosing-bugs、wayfinder）
- 词汇底层（domain-modeling、codebase-design）
- 跨会话（handoff、compact）
- 独立使用（grill-me、prototype、research、teach）

### 7.2 implement 管线 — 执行的终点
- implement 内部链：/tdd → 类型检查 → 单测 → 全量测试 → /code-review → commit
- "Pre-agreed seams"：先定测试边界再写代码
- 任务粒度：每 ticket 单独实现

### 7.3 词汇表即架构 — codebase-design
- 统一术语表：Module、Interface、Depth、Seam、Adapter
- 删除测试（Deletion Test）
- 设计两次（Design It Twice）— 并行子代理模式
- **对你自建框架的启示**: 你的项目需要什么共享词汇？

### 7.4 三种组合模式
1. **链式委托**：user-invoked → model-invoked（如 grill-me → grilling）
2. **状态组合**：user-invoked + model-invoked（如 grill-with-docs = grilling + domain-modeling）
3. **并行子代理**：code-review 双轴审查、design-it-twice

### 7.5 你的项目可以借鉴的工作流设计
- 如何从"单线程研究笔记"进化为"可组合工作流"
- 什么技能该是 user-invoked，什么该是 model-invoked
- 如何设计 router skill

---

## 第 8 章：实战应用 — 构建你自己的 Agent 框架

**篇幅**: 较大（约 3000 字）
**素材引用**: 全章综合

### 8.1 设计原则清单（来自前 7 章提炼）
- Bucketed curation → 你的目录结构
- Invocation 二分法 → 你的调用模型
- Progressive disclosure → 你的信息层级
- Leading words → 你的核心词汇
- Context hygiene → 你的会话管理
- Failure mode vocabulary → 你的诊断语言

### 8.2 自制框架目录结构模板
```
your-agent-framework/
  skills/
    core/           # 核心技能（已推广）
      your-skill-1/SKILL.md
      your-skill-2/SKILL.md
    auxiliary/      # 辅助技能（草稿/实验）
    deprecated/     # 废弃
  docs/             # 对外文档
  CONTEXT.md        # 共享词汇表
  ADR/              # 架构决策记录
```

### 8.3 你需要创建的第一个 Skill（推荐）
- 先写一个最简单的 skill（参考 grill-me 的 3 行）
- 逐步添加第二个 skill（参考 implement 管线）
- 什么时候需要 router skill

### 8.4 质量保障 — 自检清单
- [ ] 每个 SKILL.md < 100 行
- [ ] 有清晰的 completion criterion
- [ ] 无否定指令（只用正面描述）
- [ ] 运行 no-op test（删除后行为不变？）
- [ ] 术语一致（不替换同义词）
- [ ] 引用只有一级深度
- [ ] User-invoked / Model-invoked 选择合理

### 8.5 常见陷阱与对策
- 过早引入太多 skill（从 2-3 个开始）
- 不维护 CONTEXT.md（词汇漂移）
- 不做 pruning（沉积）
- 无视上下文窗口限制（不 handoff）
- 把 skill 当 plugin 期望（它不是）

### 8.6 下一步行动
- 你当前项目中的哪些流程可以做成 skill
- 优先级建议：先盘问 → 再实现 → 再 review → 再路由
- 社区的进一步资源（writing-great-skills、GLOSSARY.md、ADR 模式）

---

## 附录

### A. 术语对照表（中英）
| 英文 | 中文 | 简要说明 |
|------|------|---------|
| Predictability | 可预测性 | 相同过程，不同输出 |
| Context Load | 上下文负载 | Model-invoked skill description 每轮的消耗 |
| Cognitive Load | 认知负载 | 用户必须记住 skill 存在的负担 |
| Leading Word | 引导词 | 利用模型先验的紧凑概念 |
| Progressive Disclosure | 渐进式披露 | 沿信息层级向下推细节 |
| Completion Criterion | 完成标准 | 判断任务完成的检查条件 |
| Premature Completion | 过早完成 | 步骤未完成就跳转 |
| No-Op | 无效指令 | 不改变默认行为的指令 |

### B. 素材引用索引
全部 22 个素材引用源（R1-R14, E1-E8），含简要说明

### C. 快速参考 — 最有价值的 5 个模式卡片
1. 调用决策树
2. 信息层级梯级
3. 修剪检查清单
4. Grilling 核心指令
5. Handoff 决策矩阵
