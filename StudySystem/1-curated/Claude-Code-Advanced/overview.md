# Claude Code 高级使用技巧 - 知识地图

## 主题结构

```
Claude Code 高级使用技巧
├── 1. 核心概念
│   ├── Agentic Loop（Agentic 循环）
│   ├── Context Window Management（上下文窗口管理）
│   ├── Checkpoints & Permissions（检查点与权限）
│   └── Model Selection（模型选择）
│
├── 2. 记忆与持久化
│   ├── CLAUDE.md 的正确使用
│   ├── Skills 按需加载机制
│   ├── Session Persistence（会话持久化）
│   ├── Memory Persistence Hooks（记忆持久化钩子）
│   └── Continuous Learning（持续学习）
│
├── 3. Token 优化策略
│   ├── Subagent Architecture（子代理架构）
│   ├── Model Selection Strategy（模型选择策略）
│   ├── Strategic Context Compaction（战略性上下文压缩）
│   ├── Dynamic System Prompt Injection（动态系统提示注入）
│   ├── Tool 优化（mgrep 替代 grep）
│   └── Modular Codebase（模块化代码库）
│
├── 4. 验证与评估
│   ├── Verification Criteria（验证标准）
│   ├── Checkpoint-Based Evals（检查点式评估）
│   ├── Continuous Evals（持续式评估）
│   ├── Grader Types（评估器类型）
│   └── pass@k / pass^k 指标
│
├── 5. 并行化策略
│   ├── Worktrees（Git Worktrees）
│   ├── Cascade Method（级联法）
│   ├── Fan-out Pattern（扇出模式）
│   └── Agent Abstraction Tierlist（Agent 抽象层级）
│
└── 6. 高级用法
    ├── Two-Instance Kickoff（双实例启动模式）
    ├── Orchestrator Pattern（编排器模式）
    ├── llms.txt Pattern
    └── MCP 替代方案
```

## 核心约束

> **Claude's context window fills up fast, and performance degrades as it fills.**

所有最佳实践都基于这一核心约束。

## 子主题 → 关键知识点

### 1. Agentic Loop
- 三阶段：gather context → take action → verify results
- 由模型（reasoning）和工具（action）驱动

### 2. Context Window Management
- 自动压缩机制
- `/clear` 手动重置上下文
- `/compact` 手动压缩
- Skills 按需加载，不污染主上下文
- Subagents 独立上下文

### 3. Memory Persistence
- CLAUDE.md：每次会话读取
- Skills：按需加载
- Hooks：PreCompact/SessionComplete/SessionStart
- Stop Hook：会话结束时自动提取可复用知识

### 4. Token Optimization
- 模型选择：Haiku（简单任务）→ Sonnet（90% 任务）→ Opus（复杂任务）
- mgrep 替代 grep：节省约 50% tokens
- 后台进程外执行：减少输入 tokens
- 系统提示精简：18k → 10k tokens

### 5. Verification
- 提供测试用例、截图、预期输出
- Checkpoint-Based：线性流程，有明确里程碑
- Continuous：长时间会话，探索性重构

### 6. Parallelization
- Worktrees：避免 git 冲突
- Cascade：3-4 个任务并行
- 明确边界，最小化重叠

### 7. Subagent Best Practices
- Tier 1（易用）：Subagents、Metaprompting
- Tier 2（难用）：Long-running agents、Parallel multi-agent
- Iterative Retrieval：max 3 cycles

## 来源覆盖矩阵

| 子主题 | 官方文档 | @affaan | YK |
|--------|----------|---------|-----|
| Agentic Loop | ✅ | - | - |
| Context Management | ✅ | ✅ | ✅ |
| Memory Persistence | ✅ | ✅ | ✅ |
| Token Optimization | 部分 | ✅ | ✅ |
| Verification/Evals | - | ✅ | - |
| Parallelization | - | ✅ | - |
| Subagent Patterns | ✅ | ✅ | - |
| Groundwork | - | ✅ | - |
