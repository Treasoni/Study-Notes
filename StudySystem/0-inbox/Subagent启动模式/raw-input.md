# Subagent 的两种启动模式 — 原始输入

## A. General-purpose（通用型）

特点：
- 作为独立新会话启动
- 不继承当前会话的已授权状态
- 需要重新审批权限
- 适合完全独立的任务

问题场景：
- 主会话 (已授权 Read/Edit) → 启动 general-purpose subagent (新会话，无权限) → 尝试 Read/Edit → 权限弹窗 → 后台运行，弹窗被隐藏 → 卡住等待 → 超时失败

## B. Fork（分叉型）

特点：
- 继承父会话的完整上下文
- 继承已授权的权限状态
- 无需重新审批
- 适合需要相同权限的并行任务

优势：
- 主会话 (已授权 Read/Edit) → 启动 fork subagent (继承权限) → 直接执行 Read/Edit → 无需审批 ✓

## Subagent 权限继承详解

| 类型 | 继承权限 | 继承上下文 | 需要重新审批 |
|------|---------|-----------|------------|
| General-purpose | ❌ 不继承 | ❌ 不继承 | ✅ 是 |
| Fork | ✅ 继承 | ✅ 继承 | ❌ 否 |
| Explore/Plan | ✅ 继承 | 部分（跳过 CLAUDE.md 和 git） | ❌ 否 |

## 权限评估流程

1. Hooks 检查
2. 拒绝规则 (deny)
3. 询问规则 (ask) → 需要用户交互
4. 权限模式 (permission mode)
5. 允许规则 (allow)
6. canUseTool 回调 → 需要用户交互

后台 subagent 的问题：第 3 步和第 6 步需要用户交互，后台运行时权限提示被隐藏，导致 subagent 卡在等待状态。

## Subagent 继承的内容

Subagent 接收：
- ✅ 自己的系统提示 (AgentDefinition.prompt)
- ✅ Agent 工具的提示词字符串
- ✅ 项目 CLAUDE.md (通过 settingSources 加载)
- ✅ 工具定义 (从父代理继承或 tools 中的子集)
- ✅ 预加载的 skills (在 AgentDefinition.skills 中列出)

Subagent 不接收：
- ❌ 父代理的对话历史
- ❌ 父代理的工具结果
- ❌ 父代理的系统提示
- ❌ 预加载的 skill 内容 (除非在 skills 字段中列出)

## Subagent 的上下文隔离优势

问题场景：
- 主会话读取 50 个文件进行研究 → 所有 50 个文件内容都在主对话中累积 → 主对话上下文膨胀，后续操作变慢

解决方案：
- 主会话 → 启动 research subagent → research subagent 读取 50 个文件 (在自己的上下文中) → 返回摘要到主会话 (仅摘要进入主对话) → 主对话保持清洁，可继续高效工作
