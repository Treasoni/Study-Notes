# 第 6 章：上下文管理 — Handoff 与 Context Compaction

> 素材引用: [R11], [R12], [E2], [E3]

---

Agent 对话的上下文窗口是有限的——这是所有 Agent 框架设计者必须面对的现实。Matt Pocock 的方案不是对抗这个限制（"模型应该有更大的上下文"），而是**管理它**：什么时候用一个窗口完成所有工作，什么时候换一个窗口，什么时候把工作打包带走。

## 6.1 Context Hygiene（上下文卫生）

Matt 在 ask-matt 的 router skill 中明确规定了上下文使用的纪律：

> "Keep steps 1-3 in one unbroken context window — don't compact or clear until after `/to-tickets`. Each `/implement` then starts fresh."

### 具体规则

```
同一个窗口完成（不分叉）：
  1. /grill-with-docs  — 盘问对齐
  2. /to-spec          — 生成规格说明
  3. /to-tickets       — 拆分为任务
  ── 在此之后可以 compact 或 handoff ──

新会话开始（每个任务）：
  4a. /implement (ticket 1)  ← 新会话
  4b. /implement (ticket 2)  ← 新会话
  4c. /implement (ticket 3)  ← 新会话
```

为什么前 3 步要在一个窗口完成？因为它们是**互相依赖的认知工作**。盘问产生的理解是规格说明的输入，规格说明又是任务拆分的输入。如果中间分叉了，每个新 session 都需要重新建立上下文，丢失之前的思考动量。

为什么每个 implement 要新会话？因为实现是**执行性的工作**，它只需要从 ticket 中读取规格，不需要知道盘问的完整细节。新会话减少 token 污染，也让 Agent 专注于当前任务。

### Smart Zone

Matt 把这个限制称为 **smart zone**——模型还能清晰推理的窗口范围，大约 12 万 token。他建议：

- 在接近 smart zone 上限之前完成步骤 1-3
- 如果快到了但还没完成，用 `/handoff` 分叉到新线程继续（不要推着 Agent 在退化状态下工作）

---

## 6.2 Handoff 机制详解

Handoff 是 Matt 体系中的跨会话桥梁。它的完整实现只有 7 条规则：

```markdown
Write a handoff document summarising the current conversation
so a fresh agent can continue the work.
Save to the temporary directory of the user's OS — not the current workspace.

Include a "suggested skills" section in the document,
which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts
(specs, plans, ADRs, issues, commits, diffs).
Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords,
or PII.

If the user passed arguments, treat them as a description of
what the next session will focus on and tailor the doc accordingly.
```

逐条分析每一条的设计意图：

### 规则 1：保存到临时目录

> Save to the temporary directory of the user's OS — not the current workspace.

为什么不保存到工作区？因为交接文档是"临时"的——它唯一的用途是被新会话读取一次，之后就没有价值了。如果保存到工作区，会成为项目中需要管理的文件，且可能被版本控制。

### 规则 2：包含 "suggested skills"

> Include a "suggested skills" section...

这是最巧妙的规则。交接文档不只是"到目前为止的对话摘要"，还包含"接下来应该用什么 skill"。接收方 Agent 读到文档时，不仅知道之前发生了什么，还知道下一步该做什么。

### 规则 3：不重复已有内容

> Do not duplicate content already captured in other artifacts. Reference them by path or URL instead.

交接文档不是打包所有上下文——它是指向上下文的索引。已存在的文件（规格说明、ADR、commit diff）通过路径引用，交接文档只保存"无法从文件恢复的对话状态"。

这条规则极大地压缩了 handoff 文档的大小。

### 规则 4：过滤敏感信息

> Redact any sensitive information...

防止在传递过程中泄露 API keys、密码等。

### 规则 5：参数定制

> If the user passed arguments, treat them as a description of what the next session will focus on...

Handoff 支持 `argument-hint`——传参时交接文档会聚焦于特定方面。不是生成通用的"全部状态"，而是"只生成下一个 session 需要的部分"。

```bash
# 通用 handoff
/handoff

# 聚焦 handoff（下个 session 只关注性能优化部分）
/handoff "focus on the performance optimization tickets"
```

---

## 6.3 Handoff vs Built-in Compact

Matt 明确区分了 handoff 和 Claude Code 内置的 `/compact`：

| 维度 | `/handoff`（自定义 skill） | `/compact`（内置） |
|------|---------------------------|-------------------|
| 方向 | **分叉 → 新会话** | **继续 → 同会话** |
| 输出 | 结构化 Markdown 文档 | 内置上下文摘要 |
| 可控性 | 高（可定制内容、聚焦领域） | 低（系统决定摘要内容） |
| 保留内容 | 关键决策 + 引用路径 + 建议 skill | 系统选择的上下文摘要 |
| 丢失风险 | 低（显式包含 + 引用保留） | 中（细节可能被摘要丢失） |
| 适用场景 | 长时间中断、原型探索、大任务分拆 | 阶段间平滑过渡 |
| 敏感信息 | 自动过滤 | 不过滤 |

### 什么时候用哪个？

**用 Handoff（分叉）当**：
- 会话窗口接近 smart zone 上限
- 需要切换到完全不同但相关的任务（如原型验证）
- 长时间中断后恢复（第二天继续）
- 需要显式控制传递给下个会话的内容

**用 Compact（继续）当**：
- 大阶段完成，进入下一阶段（如从盘问转到规格编写）
- 窗口还没用完，但早期的上下文已经不再需要
- 快速整理，不需要精确控制

一个实用的原则：**当你不想丢失任何细节时用 handoff，当你愿意接受一定程度的摘要时用 compact。**

---

## 6.4 Handoff 文档的结构

handoff 生成的结构化文档大致如下：

```markdown
# Handoff: [项目/任务名称]

## 当前状态
[1-2 段描述已完成的步骤、进行中的工作]

## 关键决策
- [决策 1]: [内容]，记录在 [ADR 路径]
- [决策 2]: [内容]，记录在 [文件路径]

## 未完成的工作
- [剩余步骤 1]
- [剩余步骤 2]

## 参考文件
- [路径/URL 1] — [说明]
- [路径/URL 2] — [说明]

## 建议使用的 Skills
- `/grilling` — 如果还有未决的问题需要澄清
- `/implement` — 下一阶段是落地实现
- `/code-review` — 实现后做审查

## 附件（可选）
- 敏感信息已过滤
```

关键设计：**"参考文件" 部分只有路径，没有内容复制。** 这是 handoff 保持精简的核心机制。

---

## 6.5 在你的项目中的应用

### 场景 1：长时间学习笔记的会话管理

你的学习笔记工作流通常跨越多个阶段（意图 → 收集 → 大纲 → 写作 → 组装）。每个阶段可能持续数小时或跨天。handoff 模式很适合在不同阶段之间传递上下文：

```
会话 1（同一个窗口）：
  P0 意图澄清 + P2 深度收集
  │
  ├── 如果一次完成 → 继续
  └── 如果中断 → /handoff 保存状态 → 新会话恢复

会话 2（同一个窗口）：
  P3 大纲生成
  │
  ├── 如果一次完成 → 继续
  └── 如果中断 → /handoff → 新会话

会话 3 - N（逐章新会话）：
  P4 逐章写作（每章新会话，类似 implement per ticket）
```

### 场景 2：简化的 Handoff 模板

针对学习笔记项目，可以设计轻量版的 handoff：

```markdown
# Handoff: [主题]

## 项目结构
- 意图: path/to/00_intent.md
- 素材: path/to/02_deep_research.md
- 大纲: path/to/03_outline.md
- 当前章节: path/to/chapters/N_*.md

## 当前进度
- 已完成章节: [列表]
- 当前写作: [第 N 章]
- 完成标准: [该章节的什么部分已经完成]

## 下一步
1. [下一步行动 1]
2. [下一步行动 2]

## 待确认事项
- [Agent 需要用户确认的问题]
```

> **关键**：这个模板的核心不是复制内容，而是**索引**——指向 00_intent.md、02_deep_research.md、03_outline.md 的路径。新 session 的 Agent 读取这些文件来重建上下文。

### 最佳实践总结

1. **同一阶段不分叉**：在同一个窗口完成一个逻辑阶段
2. **阶段间可 handoff**：不同阶段间允许中断恢复
3. **每个实现的子任务新会话**：逐章写作时每章新会话，类似 implement per ticket
4. **handoff 文档是索引，不是仓库**：引用已有文件路径，不复制内容
5. **always suggested skills**：告诉下个 Agent 该用什么 skill/流程继续

---

## 本章要点

1. **Context Hygiene**：前 3 步同一窗口（思考不断），每 implement 新会话（减少 token 污染）
2. **Smart Zone**：约 12 万 token，超限前用 handoff 分叉
3. **Handoff 的精髓**：不是打包上下文，而是索引已有的 artifacts + 增量状态
4. **Handoff vs Compact**：分叉 vs 继续，结构化 vs 摘要，高可控 vs 低可控
5. **在你的项目中的应用**：逐章写作 = implement per ticket 模式，阶段间可用轻量 handoff 恢复

> **对你自建框架的启示**：上下文管理策略不只是"遇到窗口限制时怎么办"，它是一个设计决策——哪些工作属于同一个认知单元（同窗口），哪些工作应该隔离（新会话）。提前规划好上下文卫生规则，比在窗口满了再想方案有效得多。

> **下一章**：可组合工作流设计——ask-matt 路由器、implement 管线、三种组合模式。
