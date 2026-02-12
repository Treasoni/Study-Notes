---
title: Claude Subagent 使用指南
date: 2026-02-12
tags:
  - Claude
  - AI学习
  - Agent
  - CLI
---

# Claude Subagent 使用指南

> [!abstract] 概述
> Subagent（子代理）是 Claude Code 中用于处理复杂、多步骤任务的自主代理。它们就像「AI 专家助手」，每个 subagent 专注于特定领域的任务，可以独立工作并返回结果。

> [!info] CLI 场景的重要性
> 在 CLI 中，subagent 是处理复杂任务的核心机制。因为你在 CLI 中无法像 IDE 那样直接操作文件和代码库，subagent 成为你让 Claude 自主探索、搜索、分析代码的主要方式。

## 什么是 Subagent

> [!info] 核心机制
> Subagent 的运行机制如下：
>
> ```
> 主会话 (你)
>    │
>    ├─ 启动 Task 工具
>    │
>    ▼
> Subagent (独立上下文)
>    │
>    ├─ 拥有独立工具集
>    ├─ 自主规划和执行
>    ├─ 多轮对话（内部）
>    │
>    ▼
> 返回结果
>    │
>    ▼
> 主会话处理结果
> ```
>
> **关键点**：
> - Subagent 在**独立上下文**中运行，不会污染主会话的 token 使用
> - Subagent 内部可以进行**多轮对话**，自主迭代和优化
> - Subagent 返回**最终结果**而非中间过程，节省主会话上下文
> - 多个 subagent 可以**并行运行**，大幅提升效率

## 可用的 Subagent 类型

### 1. Bash
> [!tip] 命令执行专家
> 擅长运行 bash 命令，用于：
> - Git 操作（commit、push、分支管理）
> - 包管理（npm install、pip install、cargo build）
> - 文件系统操作（find、grep、ls）
> - 终端任务（运行测试、启动服务）

**可用工具**：仅 `Bash`

**CLI 使用示例**：
```bash
# 你在 CLI 中这样说：
"用 bash agent 运行项目的所有测试并收集覆盖率"

# Claude 会启动 Bash subagent，执行：
# npm test -- --coverage
# 然后将结果返回给你
```

### 2. General Purpose
> [!tip] 通用问题解决者
> 擅长处理复杂的研究、代码搜索和多步骤任务：
> - 跨文件研究复杂问题
> - 深度搜索代码库中的实现
> - 执行需要多轮迭代的任务
> - 分析代码模式和架构

**可用工具**：所有工具（`*`）

**CLI 使用场景**：
- "研究这个项目中错误处理的所有方式"
- "找出所有使用了 React Context 的组件"
- "分析项目的依赖关系和循环引用"

### 3. Statusline Setup
> [!tip] 状态栏配置专家
> 专门用于配置 Claude Code 状态栏设置。

**可用工具**：`Read`、`Edit`

### 4. Explore
> [!tip] 代码库快速探索者
> 专门用于快速探索代码库结构：
> - 查找文件模式（如 `src/**/*.tsx`）
> - 搜索代码关键词（如 "API endpoints"）
> - 理解代码库架构和组织方式
> - 回答「这个代码库怎么工作」类问题

**可用工具**：除 `Task`、`ExitPlanMode`、`Edit`、`Write`、`NotebookEdit` 外的所有工具

**探索级别**（通过 prompt 指定）：
- `quick` - 快速查找，适合「找到某个文件」
- `medium` - 适度探索，适合「了解某部分代码」
- `very thorough` - 全面分析，适合「理解整个项目」

**CLI 使用示例**：
```bash
# 快速查找
"用 explore agent 快速找到路由配置文件"

# 适度探索
"用 explore agent 探索 API 模块的结构"

# 深度分析
"用 very thorough 模式探索整个项目的架构"
```

### 5. Plan
> [!tip] 软件架构师
> 专门用于设计实现方案：
> - 规划实现策略和步骤
> - 识别需要修改的关键文件
> - 考虑架构权衡和设计决策
> - 生成实现计划供你审阅

**可用工具**：除 `Task`、`ExitPlanMode`、`Edit`、`Write`、`NotebookEdit` 外的所有工具

**CLI 使用示例**：
```bash
# 规划新功能
"用 plan agent 为用户认证功能设计实现方案"

# 规划重构
"用 plan agent 规划如何将状态管理迁移到 Zustand"
```

### 6. Claude Code Guide
> [!tip] Claude Code 专家
> 专门回答关于 Claude Code 的问题：
> - Claude Code CLI 特性和命令
> - 钩子（hooks）配置和使用
> - 斜杠命令（slash commands）
> - MCP 服务器配置
> - IDE 集成方式
> - Agent SDK 使用

**可用工具**：`Glob`、`Grep`、`Read`、`WebFetch`、`WebSearch`

**CLI 使用示例**：
```bash
# 了解 CLI 功能
"用 Claude Code Guide 了解如何配置 pre-commit 钩子"

# 学习高级功能
"用 Claude Code Guide 解释 MCP 服务器的工作原理"
```

## CLI 中的使用模式

### 模式 1：让 Claude 自主探索

> [!info] 为什么这样用
> 在 CLI 中，你无法像在 IDE 中那样浏览文件树。让 subagent 自主探索，它能：
> 1. 查找相关文件
> 2. 读取关键内容
> 3. 理解代码结构
> 4. 将理解结果返回给你

**示例对话**：

```bash
你: 这个项目的路由是怎么配置的？
    我需要了解所有路由规则和组件映射。

Claude: (启动 Explore subagent)
    Claude Code 会启动 Explore agent 来探索路由配置。

(Explore 内部执行)
    - 搜索路由相关文件（router、route、navigation等关键词）
    - 读取找到的路由配置文件
    - 分析路由规则和组件映射
    - 返回结果给主会话

Claude: 根据探索结果，我找到了以下路由配置：

    路由定义在 src/router/index.ts 中：
    - 使用 React Router v6
    - 主路由布局在 App.tsx
    - 认证相关路由需要登录

    具体路由规则包括：
    / → HomePage
    /login → LoginPage
    /dashboard → DashboardLayout → DashboardPage
    ...
```

### 模式 2：并行搜索多个话题

> [!info] 性能优化技巧
> 当你需要了解多个不相关的话题时，让 Claude 启动多个并行 subagent 可以大幅节省时间。

**示例对话**：

```bash
你: 我需要同时了解这个项目的三个方面：
    1. 错误处理机制
    2. 认证流程
    3. 数据库连接配置

Claude: (启动三个并行 General Purpose subagent)
    我将并行搜索这三个话题。

(三个 subagent 同时运行)
    Agent 1: 搜索错误处理相关的代码（try/catch、error handler等）
    Agent 2: 搜索认证相关的代码（login、auth token等）
    Agent 3: 搜索数据库配置相关代码（database、connection等）

Claude: 搜索完成，结果如下：

    ## 错误处理机制
    - 使用自定义 Error 类继承
    - 在 api 模块有统一的错误处理包装器
    - 前端使用 ErrorBoundary 捕获错误
    ...

    ## 认证流程
    - 使用 JWT token
    - 在 LocalStorage 存储 token
    - 通过 api/auth.ts 进行认证
    ...

    ## 数据库连接
    - 使用 Prisma ORM
    - 配置在 prisma/schema.prisma
    - 连接池大小为 10
    ...
```

### 模式 3：规划复杂改动

> [!info] 架构思考
> 在做复杂改动前，让 Plan subagent 先分析方案，可以避免踩坑。

**示例对话**：

```bash
你: 我想把项目的状态管理从 Redux 迁移到 Zustand。
    需要先规划一下怎么做。

Claude: (启动 Plan subagent)
    我将使用 Plan agent 来设计迁移方案。

(Plan 内部执行)
    - 探索现有 Redux store 结构
    - 找出所有使用 Redux 的组件
    - 设计 Zustand store 的对应结构
    - 规划迁移步骤和顺序
    - 识别潜在的坑点

Claude: 迁移方案如下：

    ## 实现方案

    ### 第一步：创建 Zustand stores
    - 将 Redux slices 转换为 Zustand stores
    - 文件位置：src/stores/

    ### 第二步：更新组件
    - 需要修改的组件（共 15 个）：
      - UserProfile.tsx
      - Cart.tsx
      - ...

    ### 第三步：移除 Redux 依赖
    - 删除 Redux store 配置
    - 移除 Provider 包装

    ### 关键文件
    - 需要新建：src/stores/userStore.ts
    - 需要修改：src/App.tsx（移除 Provider）
    - 需要删除：src/store/

    ### 注意事项
    - ⚠️ 有些组件使用了 Redux 的 createSelector，需要改写为 Zustand 的 computed
    - ⚠️ 中间件有日志效果，需要在 Zustand 中实现
```

### 模式 4：研究特定实现

> [!info] 深度理解代码
> 当你想深入了解某个功能的实现细节时，General Purpose subagent 可以进行多轮研究。

**示例对话**：

```bash
你: 这个项目中的 WebSocket 连接是怎么实现的？
    我想了解连接建立、重连逻辑、消息处理等所有细节。

Claude: (启动 General Purpose subagent)
    我将深入研究 WebSocket 实现。

(subagent 内部多轮执行)
    Round 1: 搜索 WebSocket 相关代码
    Round 2: 读取连接管理文件，理解连接建立流程
    Round 3: 分析重连逻辑的实现
    Round 4: 研究消息处理器
    Round 5: 总结所有发现

Claude: WebSocket 实现分析如下：

    ## 架构概览
    使用原生 WebSocket库，在 src/utils/websocket.ts 实现。

    ## 连接建立流程
    1. 通过 connectWebSocket() 函数建立连接
    2. 连接 URL 从环境变量获取
    3. 支持 token 认证，通过 URL query 参数传递

    ## 重连逻辑
    - 使用指数退避策略
    - 首次重连等待 1s，每次失败时间翻倍
    - 最大重连间隔 30s
    - 最大重连次数 10 次
    - 实现位置：src/utils/websocket.ts:45-67

    ## 消息处理
    - 使用消息类型分发（type 字段）
    - 注册的处理器在 messageHandlers 对象中
    - 支持的心跳机制：每 30s 发送 ping

    ## 代码片段（关键部分）
    ```typescript
    // src/utils/websocket.ts:45-67
    function reconnect() {
      if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
        logger.error('Max reconnect attempts reached');
        return;
      }

      const delay = Math.min(
        INITIAL_RECONNECT_DELAY * Math.pow(2, reconnectAttempts),
        MAX_RECONNECT_DELAY
      );

      setTimeout(connectWebSocket, delay);
    }
    ```
```

## CLI 使用提示词模式

> [!tip] 如何在 CLI 中触发 subagent
> 你不需要直接指定使用哪个 subagent。只需描述你的需求，Claude 会自动判断是否需要 subagent 以及使用哪种类型。

### 探索型提示词

```bash
"探索这个项目的结构，找出所有 API 端点"
"了解这个项目是如何组织组件的"
"找出处理用户输入的所有地方"
```

Claude 会自动使用 **Explore subagent**。

### 研究型提示词

```bash
"研究这个项目中错误处理的所有实现方式"
"深入分析认证系统的完整流程"
"找出所有数据库查询的模式和优化点"
```

Claude 会自动使用 **General Purpose subagent**。

### 规划型提示词

```bash
"规划如何为这个项目添加多语言支持"
"设计用户权限系统的实现方案"
"规划将代码库迁移到 TypeScript 的步骤"
```

Claude 会自动使用 **Plan subagent**。

### 多话题并行提示词

```bash
"我需要了解以下三个方面：XXX、YYY、ZZZ"
"同时搜索这些关键词：A、B、C"
```

Claude 会自动启动多个 **并行 subagent**。

## 中级使用技巧

### 技巧 1：指定探索深度

```bash
# 快速查找（默认）
"快速找到处理认证的文件"

# 明确指定深度
"用 medium 深度探索认证模块"
"用 very thorough 模式分析整个权限系统"
```

### 技巧 2：明确输出格式

```bash
# 要求结构化输出
"探索 API 端点，以表格形式列出：路径、方法、描述"

# 要求代码示例
"研究错误处理，找出所有自定义错误类的定义并展示"

# 要求对比分析
"分析新旧两种实现方式的差异"
```

### 技巧 3：结合多个操作

```bash
# 探索 + 分析
"探索路由配置，然后分析每个路由需要的权限"

# 规划 + 估算
"规划缓存系统的实现，并估算需要修改多少文件"

# 研究 + 建议
"研究当前的性能瓶颈，给出优化建议"
```

### 技巧 4：追问和细化

```bash
你: 探索项目的状态管理

Claude: (返回结果) 项目使用 Redux，有 3 个 slices...

你: 进一步分析 userSlice 的所有 action

Claude: (使用 subagent 深入分析)
    userSlice 包含以下 actions：

    - setUser(payload: User): 设置当前用户
    - updateUser(field: string, value: any): 更新单个字段
    - clearUser(): 清除用户信息

    每个 action 被 X 个组件使用...
```

## 常见问题

> [!faq] Q: 为什么有时候 Claude 不使用 subagent？
> A: Subagent 的启动有成本。对于简单的、单次性的操作（如读取一个文件、搜索一个类名），Claude 会直接使用专用工具更快。只有在真正需要多轮、复杂操作时才会启动 subagent。

> [!faq] Q: 我能控制使用哪个 subagent 吗？
> A: 可以，通过在提示词中明确指定：
> ```bash
> "用 explore agent 搜索..."
> "用 general purpose agent 研究..."
> "用 plan agent 规划..."
> ```

> [!faq] Q: Subagent 的执行过程我能看到吗？
> A: 在 CLI 中，subagent 的内部对话是隐藏的，你只能看到最终结果。如果你需要了解过程，可以在提示词中要求：
> ```bash
> "研究错误处理，并展示你的探索过程"
> ```

> [!faq] Q: 多个 subagent 并行执行会更快吗？
> A: 是的。并行执行的 subagent 之间互不阻塞，可以同时进行不同的任务。对于不相关的研究话题，这种方式能显著节省总时间。

## 实战练习

> [!example] 练习 1：探索未知项目
>
> **目标**：拿到一个新项目，快速理解其结构
>
> **提示词**：
> ```bash
> "探索这个项目的整体结构，告诉我：
> 1. 项目类型（前端/后端/全栈）
> 2. 使用的主要技术栈
> 3. 代码组织方式
> 4. 关键模块有哪些
> 5. 如何启动项目"
> ```
>
> **预期输出**：项目概览、技术栈、目录结构说明、启动命令

> [!example] 练习 2：研究特定功能
>
> **目标**：深入理解某个功能的实现
>
> **提示词**：
> ```bash
> "深入研究这个项目中用户认证的完整实现：
> 1. 认证方式（JWT/Session/OAuth）
> 2. 登录流程的每一步
> 3. token 如何存储和验证
> 4. 登录状态的持久化
> 5. 需要认证的路由如何保护"
> ```
>
> **预期输出**：详细的流程分析、关键代码位置、代码片段

> [!example] 练习 3：规划改动
>
> **目标**：为某个改动制定详细方案
>
> **提示词**：
> ```bash
> "规划如何为这个项目添加深色模式：
> 1. 需要新建/修改哪些文件
> 2. 如何管理主题状态
> 3. 需要修改哪些组件
> 4. 如何持久化用户的选择
> 5. 估算改动范围"
> ```
>
> **预期输出**：详细的实现步骤、文件列表、注意事项

## 参考资源

- [Subagent 工具文档](https://docs.anthropic.com/claude-code/tools/task)
- [Explore Agent 最佳实践](https://docs.anthropic.com/claude-code/agents/explore)
- [Plan Agent 使用指南](https://docs.anthropic.com/claude-code/agents/plan)

## 相关概念

[[Claude Code 基础]] | [[Agent Skills]] | [[MCP 服务器]]
