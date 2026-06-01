---
change: fix-subagent-init-overhead
design-doc: openspec/changes/fix-subagent-init-overhead/design.md
base-ref: e25a5ace28b759cc7d5e8bae9e09d1515d6b97f6
archived-with: 2026-06-02-fix-subagent-init-overhead
---

# Fix Subagent Init Overhead

## 目标

消除 subagent 启动时的无意义 Glob/Read 操作，减少 token 浪费和 cache miss。

## 任务

### Task 1: Agent 定义加 skip global init 指令

在 4 个 agent 定义文件的 "核心原则" 或 "禁止行为" 段落中添加：

```markdown
## 全局指令豁免

你是 subagent，以下 CLAUDE.md 指令**不适用于你**，忽略它们：
- Resource Discovery（Glob skills/agents/templates）
- Pre-Task Initialization（Read TODO.md、.obsidian-config.md 等）
- Mandatory Triggered Reads 表格

只执行主 Agent 传给你的任务。你已拥有完成任务所需的全部输入路径。
```

文件列表：
- `.claude/agents/writer.md`
- `.claude/agents/collector.md`
- `.claude/agents/curator.md`
- `.claude/agents/beautifier.md`

### Task 2: CLAUDE.md 添加 MAIN AGENT ONLY 标注

在以下段落添加标注：
- Resource Discovery: "以下指令仅适用于主 Agent，subagent 不应执行这些搜索"
- Pre-Task Init: "以下步骤仅适用于主 Agent，subagent 已由主 Agent 提供所需上下文"
- Mandatory Triggered Reads: "此表仅约束主 Agent"

### Task 3: 修复 wikilink 验证路径

writer.md Step 3.5 和 beautifier.md Step 3b:
- `Glob **/目标名.md` → `Glob {OUTPUT_PATH}/目标名.md`
- 补充: `Glob {SYSTEM_ROOT}/**/目标名.md`（仅搜索系统目录）

### Task 4: TODO.md 路径传递格式

更新 write/SKILL.md、collect/SKILL.md、beautify/SKILL.md 中对 TODO.md 的引用，添加 input/output 路径字段格式。

### Task 5: 验证

手动触发一次 collect → write 流程，观察 subagent Glob/Read 调用次数。
