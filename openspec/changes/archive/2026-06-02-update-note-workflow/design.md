## Context

Study System 有两种笔记生命周期：
1. **创建**：完整的 6-phase 工作流（collect → curate → write → beautify → evaluate → digest），由 `phases.md` 编排，有 TODO.md 状态追踪和阶段门禁
2. **更新**：现有 `update` skill 支持 INSERT（插入新内容）和 REFRESH（刷新过时内容），但缺少工作流级别的编排

更新笔记的典型场景：
- "给我的 React hooks 笔记加上 useEffect cleanup 的内容" → INSERT
- "React hooks 笔记的 hooks 规则部分过时了，更新一下" → REFRESH
- REFRESH 模式可能需要 mini collect→curate→write 研究循环

现有 `update` skill 已定义了详细的执行步骤（分析笔记、确认模式、最小改动插入、验证），但它是一个独立 skill，没有编排层来管理多步骤流程、状态追踪和用户确认。

## Goals / Non-Goals

**Goals:**
- 提供一个编排层（`update-workflow` skill），封装更新笔记的完整流程
- 支持两种核心场景：追加新内容（INSERT）和定向刷新章节（REFRESH）
- 在 REFRESH 模式下可靠地执行 mini collect→curate→write 循环
- 更新后进行轻量验证（格式一致性、双链完整性）
- 保留用户确认阻塞点，让用户审核 diff 后决定

**Non-Goals:**
- 不替换现有 `update` skill — 新 skill 包装它作为底层执行者
- 不支持批量更新多个笔记
- 不支持模板迁移或元数据批量更新
- 不做完整的质量评估（evaluate）— 只做轻量验证
- 不修改现有 collect/curate/write 子 agent 定义

## Decisions

### D1: 包装现有 skill 而非替换

**选择**：新增 `update-workflow` skill 作为编排层，委托现有 `update` skill 执行实际插入操作。

**替代方案**：
- A) 废弃旧 skill，用新 skill 完全替代 → 风险：破坏已有的用户习惯和文档引用
- B) 在旧 skill 内部增加编排逻辑 → 风险：单个 skill 职责过重

**理由**：包装模式保持关注点分离。`update` skill 负责"怎么插入"，`update-workflow` 负责"什么时候插入什么"。

### D2: TODO.md 状态追踪用于 REFRESH 模式

**选择**：仅在 REFRESH 模式的 mini 研究循环中使用 TODO.md 追踪状态（mini-collect → mini-curate → mini-write）。INSERT 模式不需要状态追踪（单步操作）。

**理由**：REFRESH 的 mini 循环涉及多个阶段，需要状态追踪来支持中断恢复。INSERT 是单步操作，TODO.md 增加的复杂度不值得。

### D3: 轻量验证策略

**选择**：更新后执行三项检查：
1. 标题层级连贯性（不越级）
2. 双链完整性（不破坏现有 `[[wikilinks]]`）
3. frontmatter `updated` 字段已更新

**替代方案**：
- A) 调用 evaluate skill 做完整质量评估 → 过重，不适合小范围更新
- B) 不做任何验证 → 风险：格式错误和断链静默传播

**理由**：轻量验证覆盖最常见的更新引入问题（格式破坏、链接断裂），同时不增加不必要的复杂度。

### D4: 复用现有子 agent

**选择**：REFRESH 模式的 mini 循环直接调用现有 `/collect`、`/curate`、`/write` skill，不创建新的子 agent。

**理由**：现有子 agent 已经功能完整，只是调用范围缩小到子主题。通过传入父主题上下文和目录隔离来适配更新场景。

## Risks / Trade-offs

- **[Risk] REFRESH mini 循环的上下文传递可能不完整** → Mitigation: 在调用各 skill 时显式传入父笔记信息（父主题名、笔记类型、标题层级、格式约定）
- **[Risk] Windows 环境下 bash 脚本执行** → Mitigation: comet 脚本通过 Git Bash 执行，已在当前环境验证可用
- **[Trade-off] INSERT 模式不追踪状态** → 单步操作不需要，但如果用户在插入过程中中断，需要重新开始（可接受）
- **[Trade-off] 不支持批量更新** → 聚焦核心场景，批量需求可通过多次调用满足
