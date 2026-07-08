---
type: experience
topic: Subagent 启动模式
tags:
  - subagent
  - Claude-Code
  - 权限管理
  - 工作流优化
created: 2026-07-08
updated: 2026-07-08
source: 个人经验
---

# Subagent 的两种启动模式

## 背景

研究系统依赖 Subagent 来执行隔离的任务。最初我默认使用 General-purpose（通用型）模式来启动所有 Subagent，结果在实际运行中频繁遇到**权限弹窗卡死**的问题：Subagent 被派发到后台执行任务，需要用户审批权限，但弹窗被隐藏，Subagent 卡在等待状态直至超时失败。

这个问题的根源在于对 Subagent 启动模式的理解不深——Claude Code 实际上提供了不止一种启动 Subagent 的方式。 [来源: 个人经验]

## 过程

在排查后台 Subagent 频繁超时的过程中，我仔细研究了 Claude Code 的 Subagent 机制，发现了两种启动模式：

### General-purpose（通用型）

这是最直观的启动方式——Subagent 以一个**完全独立的新会话**启动。它不继承当前会话的任何已授权状态，所有权限都需要重新审批。

**实际工作流：**

```
主会话 (已授权 Read/Edit)
  → 启动 general-purpose subagent (新会话，零权限)
  → subagent 尝试 Read/Edit
  → 权限弹窗出现
  → subagent 在后台运行，弹窗被隐藏
  → subagent 卡住等待审批
  → 超时失败 ❌
```

这正是在研究系统中不断重复的现象。General-purpose 模式适合**完全独立**的任务——比如一个只读分析任务，不需要操作代码库。 [来源: 个人经验]

### Fork（分叉型）

Fork 模式从根本上解决了权限问题。它以当前会话为蓝本"分叉"出一个子会话，**继承了父会话的完整上下文和已授权权限状态**。

**实际工作流：**

```
主会话 (已授权 Read/Edit)
  → 启动 fork subagent (继承全部权限和上下文)
  → subagent 直接执行 Read/Edit
  → 无需审批 ✓
```

切换到 Fork 模式后，后台 Subagent 再没有因为权限弹窗而卡死。 [来源: 个人经验]

## 权限继承详解

除了 General-purpose 和 Fork，还有 Explore/Plan 这种中间类型。它们的权限继承关系对比如下：

| 类型 | 继承权限 | 继承上下文 | 需要重新审批 |
|------|---------|-----------|------------|
| General-purpose | 不继承 | 不继承 | 是 |
| Fork | 继承 | 继承 | 否 |
| Explore/Plan | 继承 | 部分（跳过 CLAUDE.md 和 git） | 否 |

### Subagent 接收 vs 不接收的内容清单

**Subagent 会接收：**
- 自己的系统提示（定义在 `AgentDefinition.prompt` 中）
- Agent 工具的提示词字符串
- 项目的 CLAUDE.md（通过 settingSources 加载）
- 工具定义（从父代理继承或 tools 中指定的子集）
- 预加载的 skills（在 `AgentDefinition.skills` 中列出）

**Subagent 不会接收：**
- 父代理的对话历史
- 父代理的工具执行结果
- 父代理的系统提示
- 预加载的 skill 具体内容（除非在 skills 字段中明确列出） [来源: 个人经验]

## 权限评估的 6 步流程

理解为什么权限弹窗会卡住后台 Subagent，需要了解 Claude Code 的权限评估流水线：

1. **Hooks 检查** — 自定义钩子拦截
2. **拒绝规则 (deny)** — 硬性拒绝，无需交互
3. **询问规则 (ask)** — 需要用户交互 ⚠️
4. **权限模式 (permission mode)** — 根据模式决定行为
5. **允许规则 (allow)** — 自动放行，无需交互
6. **canUseTool 回调** — 需要用户交互 ⚠️

第 3 步（ask）和第 6 步（canUseTool 回调）是**用户交互瓶颈**。当 Subagent 在后台运行时，这些权限提示被隐藏，Subagent 就卡死了。 [来源: 个人经验]

## 踩坑

> [!warning] General-purpose 在后台任务中的权限陷阱
> **现象**：后台 Subagent 莫名其妙地超时，没有错误日志，只有超时提示。
>
> **原因**：General-purpose 模式下，Subagent 需要重新审批所有权限。后台进程的权限弹窗无法在前端展示，Subagent 等待用户响应的过程变成了无限等待，最终触发超时机制。
>
> **解决**：将后台执行任务的 Subagent 切换为 Fork 模式。如果确实需要一个独立的会话（例如执行清理、测试等不可中断的操作），确保该任务不需要此前已授权的权限，或在父会话中预先配置好权限规则。

## 上下文隔离优势

顺带发现，Subagent 的上下文隔离不仅是权限层面的，也是**上下文管理**层面的一大优势。

**问题场景：** 主会话读取 50 个文件做研究，50 个文件的内容全部堆积在主对话中，导致上下文膨胀，后续操作越来越慢。

**利用 Subagent 的解决方案：**

```
主会话
  → 启动 research subagent（Fork 模式）
  → research subagent 在自己的上下文中读取 50 个文件
  → 返回摘要到主会话（仅摘要进入主对话）
  → 主对话保持清洁，可继续高效工作 ✓
```

这是利用 Subagent 做"脏活"的经典用法——把高 Token 消耗的操作隔离到子会话中执行，只把精炼的结果带回主会话。 [来源: 个人经验]

## 适用场景对比

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 后台执行读写代码的任务 | Fork | 避免权限弹窗卡死，直接继承已授权状态 |
| 独立的数据分析/爬取 | General-purpose | 独立会话，权限隔离，不影响主会话 |
| 研究性任务读取大量文件 | Fork | 利用上下文隔离，主会话不受影响 |
| 执行敏感操作（删除、修改配置） | Fork 或 General-purpose | 视是否需要独立权限而定；如用 General-purpose 确保用户在场审批 |
| 并行执行多个独立子任务 | Fork | 继承相同权限，无需逐个审批，提升效率 |

## 延伸

- 深入了解 Explore/Plan 模式的行为差异，以及在什么场景下应该使用它们
- 如何在权限评估的配置层（permission mode）预先放行特定操作，减少交互瓶颈
- 相关笔记：[[Subagent资料搜集的Token失控-笔记]] — 关于 Subagent Token 消耗的深入分析
- 相关笔记：[[Claude Code Subagent 与 Skill 调度机制]] — 关于 Subagent 调度与 Skill 编排

## 思考题

1. 如果主会话没有预先授权任何权限，Fork 模式和 General-purpose 模式在行为上还有区别吗？
2. 在什么场景下你**不应该**使用 Fork 模式，即使它解决了权限问题？（提示：想想安全性）
3. 权限评估的 6 步流程中，有哪些步骤可以通过代码编写静态规则来避免用户交互？
4. 如果多个 Subagent 共享同一个 Fork 父会话，它们之间的上下文会相互影响吗？为什么？
5. 上下文隔离的"摘要传递"策略，在什么情况下反而会成为性能瓶颈？（提示：如果摘要本身很大呢？）
