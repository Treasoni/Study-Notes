## Why

Subagent 启动时继承了 CLAUDE.md 中的全局指令（Resource Discovery、Pre-Task Init、Mandatory Triggered Reads），导致每个 subagent 在执行实际任务前先进行大量无意义的 Glob 搜索和文件读取。这造成：

1. **Token 消耗暴增** — 每个 subagent 读取 5-10 个无关文件
2. **Cache Miss** — Glob 结果变化导致上下文哈希变化，Anthropic prompt cache 反复失效
3. **任务延迟** — 实际工作前浪费 30-60% 的 token 在初始化上

## What Changes

- 在 4 个 agent 定义文件（writer/collector/curator/beautifier）中添加 **"skip global init" 指令**，明确告知 subagent 忽略 CLAUDE.md 中的 Resource Discovery、Pre-Task Init、Mandatory Triggered Reads
- 在 CLAUDE.md 中添加 **"MAIN AGENT ONLY" 标注**，区分主 Agent 和 subagent 的行为边界
- 修改 writer.md 和 beautifier.md 中的 **wikilink 验证逻辑**，从 `Glob **/目标名.md`（扫描整个 vault）改为 narrow path 搜索
- 在 TODO.md 中增加 **跨阶段文件路径传递**，让下一个 phase 的 subagent 知道先读哪些文件

## Capabilities

### New Capabilities

（无新增 capability）

### Modified Capabilities

- `subagent-orchestration`: 强制执行已有的"隔离上下文"要求——subagent 不应继承 CLAUDE.md 的全局初始化指令；新增跨阶段路径传递机制

## Impact

- **Agent 定义文件**: `.claude/agents/writer.md`, `.claude/agents/collector.md`, `.claude/agents/curator.md`, `.claude/agents/beautifier.md`
- **全局配置**: `CLAUDE.md`（添加 MAIN AGENT ONLY 标注）
- **Skill 文件**: `.claude/skills/write/SKILL.md`, `.claude/skills/beautify/SKILL.md`（更新 TODO.md 路径传递逻辑）
- **影响范围**: 所有使用 subagent 的笔记工作流（collect → curate → write → beautify）
- **风险**: 低——只是添加指令约束，不改变核心逻辑
