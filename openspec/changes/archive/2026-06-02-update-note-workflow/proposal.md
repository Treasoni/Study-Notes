## Why

创建笔记有完整的 6-phase 工作流（phases.md）和 TODO.md 状态追踪，但更新笔记只有一个孤立的 `update` skill，缺少编排层。当用户说"更新我的 React hooks 笔记"时，系统无法：
- 自动定位目标笔记并分析结构
- 根据用户意图（追加 vs 刷新）选择正确路径
- 在 REFRESH 模式下可靠地执行 mini collect→curate→write 循环
- 在更新后进行验证并让用户确认 diff

现有 `update` skill 定义了 INSERT 和 REFRESH 两种模式的步骤，但没有工作流级别的编排——没有阶段门禁、没有状态追踪、没有用户确认阻塞点。

## What Changes

- 新增 `update-workflow` skill：封装更新笔记的完整编排流程，委托现有 `update` skill 执行实际插入操作
- 更新 `docs/updating-notes.md`：补充工作流编排说明，与新 skill 保持一致
- 现有 `update` skill 保持不变，作为底层执行者被调用

## Capabilities

### New Capabilities
- `note-update-workflow`: 笔记更新工作流编排——定位目标笔记、识别更新意图（INSERT/REFRESH）、执行更新、轻量验证、用户确认

### Modified Capabilities
（无现有 spec 需要修改）

## Impact

- `.claude/skills/` 目录：新增 `update-workflow/SKILL.md`
- `docs/updating-notes.md`：内容更新
- 现有 `update` skill：不受影响，作为底层依赖被包装调用
- 子 agent 定义（`collector.md`、`curator.md`、`writer.md`）：不受影响，mini 循环复用现有 subagent
