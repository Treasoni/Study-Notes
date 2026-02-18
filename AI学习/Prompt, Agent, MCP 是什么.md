---
tags: [ai]
---

# Prompt、Agent、MCP 核心概念

> [!info] 概述
> **AI 的进化之路**：Prompt 让 AI 会说话（有人设），Agent 让 AI 能动手（有工具），MCP 让工具可以随意换（通用接口）。就像从"聊天机器人"升级到"全能管家"！

## 核心概念 💡

### Prompt（提示词）

**是什么**：给 AI 的输入指令，定义对话内容和人设

**为什么需要**：
- 让 AI 理解用户意图
- 设定 AI 的角色和行为准则
- 提供上下文信息

**与其他概念关系**：是用户与 AI 交互的基础，Agent 和 MCP 都依赖 Prompt 来工作

| 类型 | 作用 | 比喻 |
|------|------|------|
| **System Prompt** | 定义角色、人设、行为准则 | 演员的角色卡 |
| **User Prompt** | 用户的实际输入 | 观众的问题 |

### Agent（智能体）

**是什么**：能调用工具的 AI 系统，从"只会说"变成"能说能做"

**为什么需要**：
- 让 AI 执行具体功能
- 操作外部系统和数据
- 自动化复杂任务流程

**与其他概念关系**：使用 Prompt 与 AI 通信，通过 Function Calling 调用工具，通过 MCP 连接外部服务

### MCP（Model Context Protocol）

**是什么**：Agent 与工具之间的标准化通信协议

**为什么需要**：
- 统一工具接口格式
- 实现工具可复用、跨语言
- 支持分布式部署

**与其他概念关系**：MCP Server 提供工具，Agent（作为 MCP Client）调用工具

## 操作步骤

### 使用 Prompt 的基本流程

```bash
# 1. 定义 System Prompt（角色设定）
system_prompt = "你是一个专业的程序员助手"

# 2. 发送 User Prompt（用户问题）
user_prompt = "帮我写一个快速排序算法"

# 3. AI 结合两者生成回复
```

### Agent 工作流程

```
┌─────────────────────────────────────────────┐
│  1. 收集所有 Tools 信息                     │
│  2. 构造 System Prompt                      │
│  3. 发送 System + User Prompt 给 AI          │
│  4. AI 决定是否调用工具                      │
│  5. 执行 Tool 函数                           │
│  6. 将结果返回给 AI                          │
│  7. 重复直到生成最终答案                      │
└─────────────────────────────────────────────┘
```

### 配置 MCP Server

```bash
# 1. 安装 MCP Server
npm install -g @modelcontextprotocol/server-filesystem

# 2. 配置到 Claude Code
# 在 .mcp.json 中添加配置

# 3. 重启 Claude Code
claude

# 4. 验证配置
/mcp
```

## 注意事项 ⚠️

### 常见错误

**Prompt 编写问题**：
- ❌ 角色设定不清晰
- ❌ 缺少必要的上下文
- ❌ 约束条件不明确

**Agent 使用问题**：
- ❌ 期望 Agent 做超出其能力的事
- ❌ 工具描述不准确
- ❌ 忘记处理工具调用结果

**MCP 配置问题**：
- ❌ 配置文件格式错误
- ❌ 环境变量设置不当
- ❌ 服务器类型选择错误

### 关键配置点

**Prompt 最佳实践**：
- 明确角色定位
- 提供具体示例
- 设定输出格式
- 添加必要的约束

**Agent 最佳实践**：
- 工具描述要准确
- 只暴露必要的工具
- 处理好错误情况
- 记录调用历史

**MCP 配置要点**：
- 选择正确的通信类型
- 使用环境变量管理敏感信息
- 配置文件使用绝对路径
- 定期检查服务器状态

## 常见问题 ❓

**Q: System Prompt 和 User Prompt 有什么区别？**

A: System Prompt 是预设的角色和行为准则，每次对话都会发送；User Prompt 是用户的具体问题。就像演员的角色卡（System）和观众的提问（User）。

**Q: Agent 一定会调用工具吗？**

A: 不一定。Agent 会根据用户问题判断是否需要调用工具。对于简单问题，可能直接回答而不调用任何工具。

**Q: MCP 和传统 API 有什么区别？**

A: MCP 是标准化协议，所有 MCP Server 都遵循相同的接口规范。传统 API 则各自定义格式。就像 USB（MCP）vs 各种专用接口。

**Q: 如何选择 MCP 服务器类型？**

A:
- **stdio**：本地工具、NPM 包
- **SSE**：云端服务、需要 OAuth
- **HTTP**：REST API
- **WebSocket**：实时通信

**Q: Skills 和 Agent 有什么区别？**

A: Skills 是预定义的任务模板，通过命令触发；Agent 是能自主决策的工具调用系统。Skills 更像"快捷键"，Agent 更像"智能助手"。

## 相关文档
[[Skills 是什么]] | [[Claude MCP 使用指南]] | [[Claude Subagent 使用指南]]
