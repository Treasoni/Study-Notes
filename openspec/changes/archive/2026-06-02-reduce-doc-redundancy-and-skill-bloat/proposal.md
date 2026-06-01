## Why

Study System 的文档和 skill 定义存在严重的冗余问题，导致每次会话消耗大量无用 token：

1. **TODO.md 状态机规则分散在 17 个文件中**，同一规则（Phase Gate、rm TODO.md 等）重复定义 9-12 次，总计 ~7000 tokens 冗余
2. **update-workflow/SKILL.md 与 docs/updating-notes.md 60-70% 内容重复**（~3000 tokens）
3. **scoring rubric 在 3 个文件中完全相同**（~400 tokens）
4. **37 个非 study-system skills（~300KB）每次会话全量注入系统提示**，但从未被引用

这些问题不仅浪费 token，还增加了维护成本——修改一个规则需要同步更新多个文件。

## What Changes

- **抽取 TODO.md 状态机为单一权威参考文档**，其他文件改为引用而非重复定义
- **合并 update-workflow/SKILL.md 与 docs/updating-notes.md**，消除 60-70% 重复
- **scoring rubric 单一来源**，只在 collector.md 定义，其他位置引用
- **研究并实现 skill 过滤/分组机制**，让 .study-config.yaml 能控制哪些 skill 注入系统提示
- **精简 4 个 agent 定义中的重复豁免块**

## Capabilities

### New Capabilities

- `skill-filtering`: 机制控制哪些 skills 注入系统提示，减少 ~300KB 无用上下文

### Modified Capabilities

- `note-update-workflow`: 合并 update-workflow 与 updating-notes.md，统一文档来源
- `subagent-orchestration`: 精简 agent 定义中的重复豁免块

## Impact

- **docs/** 目录：phases.md、experience-notes.md、updating-notes.md 内容精简
- **.claude/skills/**：update-workflow/SKILL.md 合并或删除
- **.claude/agents/**：4 个 agent 定义精简
- **.study-config.yaml**：新增 skill 过滤配置项
- **CLAUDE.md**：TODO.md 状态机规则改为引用新参考文档
- **Token 节省**：预计每次会话减少 ~10,000+ tokens（不含 skill 过滤的额外节省）
