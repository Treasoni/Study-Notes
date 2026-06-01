## Why

Study System 的当前工作流存在四个核心痛点，严重影响使用体验和笔记质量：

1. **上下文爆满**：Main Agent 承担所有重计算（读取、打分、生成），单阶段上下文可达 20k+ tokens，容易超出限制
2. **确认过多**：Phase 边界强制 STOP，每个阶段都需要用户确认，5 个阶段至少 5 次中断
3. **类型不确定**：5 种笔记类型（concept/practice/compare/cheat-sheet/experience）必须在开始时选定，用户 often 不清楚自己想要什么类型
4. **质量不达标**：缺少需求发现阶段，系统假设用户已明确目标，但实际用户 often 不知道自己想要达到什么效果

## What Changes

- **引入 Subagent 分担机制**：将重计算任务（资料采集、打分整理、笔记生成）委托给专用 subagent，Main Agent 仅负责协调
- **添加自治分级系统**：支持 Level 0-3 四级自治，用户可配置确认频率（每步确认 → 每阶段确认 → 关键点确认 → 全自动）
- **支持混合笔记类型**：允许笔记包含多种类型的元素（如概念解释 + 实战示例），支持自动推断最佳类型组合
- **新增讨论澄清阶段**：在正式开始前，通过问答明确学习目的、目标读者、深度要求、笔记用途，生成定制化执行计划

## Capabilities

### New Capabilities

- `subagent-orchestration`: Subagent 调度与协调机制，包括任务分发、结果聚合、错误处理
- `autonomy-levels`: 自治分级系统，支持用户配置确认频率，Main Agent 根据级别决定是否自动推进
- `requirement-discovery`: 需求发现阶段，通过结构化问答明确用户意图，生成执行计划
- `hybrid-note-types`: 混合笔记类型系统，支持多类型元素组合，自动推断最佳类型

### Modified Capabilities

<!-- 无现有 capability 需要修改，这是全新重构 -->

## Impact

- **Core Workflow**：Phase 0-4 流程需要重构，新增讨论澄清阶段
- **Skills**：`collect`、`curate`、`write`、`beautify` 需要适配 subagent 调用
- **Templates**：需要支持混合类型模板或动态组合
- **Configuration**：需要新增 autonomy level 配置项
- **Documentation**：CLAUDE.md、docs/phases.md 需要更新
