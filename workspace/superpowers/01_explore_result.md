# Superpowers Agentic Skills Framework - 探测结果

> 探测时间：2026-07-23
> 项目：obra/superpowers
> 三个预定义方向：Workflow Pipeline / Subagent Dispatching / Git Worktree 隔离

---

## 方向 1：Workflow Pipeline（工作流状态机）

### 核心发现

Superpowers 实现了一个 **7 阶段硬门控状态机**，每个阶段之间都有二进制门控，不满足前置条件无法进入下一阶段：

```
Brainstorming → Git Worktrees → Writing Plans → Subagent-Driven Development → TDD → Code Review → Finishing Branch
```

**门控机制**：
- 设计必须经过用户审批才能进入计划阶段
- 需要干净的 Git Worktree + 通过测试后才能写任何实现代码
- 根因分析必须完成才能开始修复

**"1% 规则"**：
- 如果某个技能有 1% 的触发可能，Agent **必须**加载并遵循它
- 去除了 Agent 为了速度跳过流程的自主权
- 指令优先级：用户/项目指令 > Superpowers skills > 默认 system prompt

**TDD 强制执行**：
- 严格 RED-GREEN-REFACTOR 循环，零例外
- 没有失败的测试就不允许写生产代码
- 已提前预判并阻止 Agent 常见借口（"太简单了"、"这是 UI 代码"、"时间紧迫"）
- 通过强制检查清单将质量从自愿原则变为默认行为

### 关键来源
- [obra/superpowers GitHub](https://github.com/obra/superpowers)
- [Superpowers 原理分析 - 腾讯云](https://cloud.tencent.com.cn/developer/article/2665629)
- [Superpowers 和 GSD - 腾讯云](https://cloud.tencent.com.cn/developer/article/2689449)
- [5 Hidden Uses - Dev.to](https://dev.to/_cbd692d476c5faf3b61bcf/superpowers-agentic-skills-framework-5-hidden-uses-of-the-233k-star-ai-coding-methodology-470d)

---

## 方向 2：Subagent Dispatching（子 Agent 派发）

### 核心发现

**Subagent-Driven-Development** 是 Superpowers 的核心执行引擎，工作流第 4 步：

**派发模式**：
- 每个任务派发全新的 subagent，独立的上下文隔离
- Claude Code 使用 `Task` 工具 + 命名 agent 类型（如 `superpowers:code-reviewer`）
- Codex 使用 `spawn_agent` + `worker` 角色
- v6.0 引入模型分层：快速/廉价模型做机械实现，标准模型做集成/判断，最强模型做架构/设计/审查

**两阶段审查（v5）/ 合并审查（v6）**：
- v5：每个任务后做 spec 合规审查 + 代码质量审查两次
- v6：合并为一次 diff 通读，同时返回合规性和质量判定
- 审查者只读，不能修改代码，不能被说服跳过发现的问题

**Subagent 状态报告**：
- `DONE` — 完成
- `DONE_WITH_CONCERNS` — 完成但有担忧
- `NEEDS_CONTEXT` — 需要更多上下文
- `BLOCKED` — 阻塞（需要人工介入）

**跨平台分发差异**：
- Claude Code 有命名 Agent 注册表，Codex 需要手动映射
- 已知 bug：Codex 上的 `requesting-code-review` 可能静默跳过审查步骤

**v6.0 架构改进**：
- 预飞行计划冲突检查
- 通过文件传递 diff 和任务文本（减少上下文成本）
- 每次分发明确指定模型（避免意外使用昂贵模型）

### 关键来源
- [subagent-driven-development/SKILL.md](https://github.com/obra/superpowers/blob/f2cbfbef/skills/subagent-driven-development/SKILL.md)
- [Superpowers v6.0.0 Release Notes](https://newreleases.io/project/github/obra/superpowers/release/v6.0.0)
- [Issue #647 - Codex review 静默跳过 bug](https://github.com/obra/superpowers/issues/647)
- [Zhihu 技术教程](https://zhuanlan.zhihu.com/p/2030628504719639855)

---

## 方向 3：Git Worktree 隔离执行

### 核心发现

**Git Worktree 作为前置门控**：
- 在写任何生产代码前，`using-git-worktrees` skill 创建一个隔离工作区
- 运行项目设置，验证干净的测试基线
- 如果实现出错，直接删除 worktree 重试，无需 Git 考古

**实现机制**：
- 创建独立链接的工作目录（共享 `.git` 对象存储）
- 每个 subagent 拥有独立的 HEAD、index 和分支状态

**已知问题**：
- Claude Code worktree 隔离有时静默回退到父仓库
- 子 agent 中的分支切换可能改变父仓库的 HEAD
- 推荐替代方案：基于 clone 的隔离（`--dissociate --reference --single-branch`）

**生态扩展**：
- Qwen Code 实现了类似功能，带有自动过期清理（30 天 mtime 保护）
- Ubuntu Workshop 将 worktree 与容器沙箱结合
- 至少 7 个已知的 Superpowers fork/port

### 关键来源
- [Claude Code Worktrees 文档](https://code.claude.com/docs/en/worktrees)
- [Issue #55708 - worktree 隔离 bug](https://github.com/anthropics/claude-code/issues/55708)
- [Issue #47548 - worktree 分支突变 bug](https://github.com/anthropics/claude-code/issues/47548)
- [Qwen Code Worktrees](https://qwenlm.github.io/qwen-code-docs/en/users/features/worktree/)

---

## 综合分析

### 项目架构总览

Superpowers 是一个 **Plugin-per-Harness 架构** 的 Agentic Skills Framework：

```
superpowers/
├── .claude-plugin/    # Claude Code 插件配置
├── .codex-plugin/     # Codex CLI 插件配置
├── .cursor-plugin/    # Cursor 插件配置
├── .kimi-plugin/      # Kimi Code 插件配置
├── hooks/             # 启动钩子（session-start 自动触发 brainstorming）
├── skills/            # 14 个可组合技能（核心）
│   ├── brainstorming/         # 协作
│   ├── writing-plans/         # 协作
│   ├── executing-plans/       # 协作
│   ├── subagent-driven-development/ # 协作
│   ├── dispatching-parallel-agents/ # 协作
│   ├── requesting-code-review/      # 协作
│   ├── receiving-code-review/       # 协作
│   ├── finishing-a-development-branch/ # 协作
│   ├── using-git-worktrees/     # 协作
│   ├── test-driven-development/ # 测试
│   ├── systematic-debugging/    # 调试
│   ├── verification-before-completion/ # 调试
│   ├── using-superpowers/       # 元技能
│   └── writing-skills/          # 元技能
└── docs/              # 文档和移植指南
```

### 三个方向的关联

这三个方向不是独立的，而是 **层层递进的执行流水线**：

1. **Workflow Pipeline** 定义了整体的阶段流转和门控规则
2. **Subagent Dispatching** 是执行引擎，在工作流第 4 步发挥作用
3. **Git Worktree 隔离** 是执行的基础设施保障，在工作流第 2 步和环境隔离中发挥作用

### 适用场景

这套框架尤其适合：
- 大型项目需要严格质量控制
- 多人/多 Agent 协作场景
- 需要可复现、可审计的开发流程
- 团队需要统一开发方法论

### 局限与注意事项
- Claude Code worktree 隔离存在已知 bug
- 跨平台分发需要额外映射工作
- 框架约束较强，小项目可能过度设计

---

## 方向确认

| 方向 | 用户指定 | 探测确认 | 优先级 |
|------|---------|---------|--------|
| Workflow Pipeline | ✅ | ✅ 丰富的资料 | ⭐⭐⭐ |
| Subagent Dispatching | ✅ | ✅ 非常详细 | ⭐⭐⭐ |
| Git Worktree 隔离 | ✅ | ✅ 有实际应用和已知问题 | ⭐⭐⭐ |

三个方向均已确认，可以直接进入深度收集阶段（P2）。
