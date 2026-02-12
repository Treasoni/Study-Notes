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

## 内置 Subagent 类型

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

### 3. Explore
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

### 4. Plan
> [!tip] 软件架构师
> 专门用于设计实现方案：
> - 规划实现策略和步骤
> - 识别需要修改的关键文件
> - 考虑架构权衡和设计决策
> - 生成实现计划供你审阅

**可用工具**：除 `Task`、`ExitPlanMode`、`Edit`、`Write`、`NotebookEdit` 外的所有工具

### 5. Claude Code Guide
> [!tip] Claude Code 专家
> 专门回答关于 Claude Code 的问题：
> - Claude Code CLI 特性和命令
> - 钩子（hooks）配置和使用
> - 斜杠命令（slash commands）
> - MCP 服务器配置
> - IDE 集成方式

**可用工具**：`Glob`、`Grep`、`Read`、`WebFetch`、`WebSearch`

---

# 创建自定义 Subagent

> [!warning] 重要概念
> **在 CLI 中创建自定义 subagent 需要通过「插件（Plugin）**来实现**。**
>
> Claude Code 的插件系统允许你创建包含自定义 agent、command、skill、hook 的扩展包。

## 插件结构

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据（必需）
├── agents/                   # 自定义 agents 目录
│   └── my-agent.md          # agent 定义文件（.md 格式）
├── commands/                 # 斜杠命令
│   └── my-command.md         # 命令定义文件
├── skills/                  # 自定义 skills
│   └── my-skill/
│       ├── SKILL.md
│       └── metadata.json
├── hooks/                   # 钩子脚本
│   └── my-hook.sh
└── README.md                # 插件文档
```

## Agent 文件格式

每个 agent 是一个 `.md` 文件，包含 **YAML frontmatter** 和 **系统提示词**：

```markdown
---
name: my-agent                  # agent 标识符（小写，连字符）
description: Use this agent when...  # 触发条件描述
model: inherit                 # 使用的模型（inherit/sonnet/opus/haiku）
color: blue                   # 显示颜色（blue/cyan/green/yellow/red/magenta）
tools: ["Read", "Write"]      # 可用工具列表（可选）
---

你是一个专业的 [领域] 专家...

## 核心职责

1. [职责 1]
2. [职责 2]
...

## 执行流程

1. [步骤 1]
2. [步骤 2]
...

## 输出格式

[定义输出规范]
```

### Frontmatter 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | agent 标识符，小写字母、数字、连字符，3-50 字符 |
| `description` | string | ✅ | 触发条件描述，包含 `<example>` 块 |
| `model` | string | ❌ | 使用的模型，默认 `inherit` |
| `color` | string | ❌ | 显示颜色 |
| `tools` | array | ❌ | 允许使用的工具列表，不填则全部可用 |

### 触发示例（description 中的 `<example>`）

```markdown
---
description: Use this agent when user asks to "create an agent" or "generate an agent". Examples:

<example>
Context: User wants to create a code review agent
user: "Create an agent that reviews code for quality issues"
assistant: "I'll use the agent-creator agent to generate it."
<commentary>
User requesting new agent creation, trigger agent-creator.
</commentary>
</example>

<example>
Context: User describes needed functionality
user: "I need an agent that generates unit tests for my code"
assistant: "I'll use the agent-creator agent to create a test generator."
<commentary>
User describes agent need, trigger agent-creator.
</commentary>
</example>
---
```

## 在 CLI 中创建 Agent

### 方法 1：使用 plugin-dev 插件（推荐）

**plugin-dev** 是官方提供的插件开发工具包，包含 agent-creator agent。

```bash
# 首先安装 plugin-dev
/plugin install plugin-dev@claude-code-marketplace

# 创建 agent
"创建一个 agent，用于代码审查"
```

Claude 会：
1. 询问你 agent 的用途
2. 自动生成 agent 配置
3. 创建 agent 文件

### 方法 2：手动创建

```bash
# 1. 创建插件目录结构
mkdir -p my-plugin/agents
cd my-plugin

# 2. 创建 plugin.json
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "description": "我的自定义插件",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  }
}
EOF

# 3. 创建 agent 文件（见下一节的示例）
cat > agents/my-agent.md << 'EOF'
[agent 内容]
EOF

# 4. 使用插件
claude --plugin-dir /path/to/my-plugin
```

## 完整示例：创建代码审查 Agent

```markdown
---
name: code-reviewer
description: Use this agent when user asks to "review code", "check code quality", "analyze code issues", or wants code review. Examples:

<example>
Context: User just wrote code and wants review
user: "Review the code I just wrote"
assistant: "I'll use the code-reviewer agent to analyze the code."
<commentary>
User explicitly requests code review, trigger code-reviewer.
</commentary>
</example>

<example>
Context: User mentions checking code quality
user: "Check if there are any issues with this code"
assistant: "I'll use the code-reviewer agent to identify issues."
<commentary>
User asks for code quality check, trigger code-reviewer.
</commentary>
</example>
model: sonnet
color: blue
---

你是一个资深的代码审查专家，擅长识别代码质量问题和最佳实践偏差。

## 核心职责

1. **分析代码质量**：识别潜在 Bug、性能问题、安全漏洞
2. **检查最佳实践**：对照语言/框架的最佳实践
3. **提供具体建议**：给出可执行的改进建议
4. **评估代码风格**：检查一致性和可读性

## 审查流程

1. **读取代码**：使用 Read 工具读取相关文件
2. **静态分析**：识别常见问题模式
3. **深度分析**：理解代码意图和上下文
4. **生成报告**：按优先级整理问题

## 输出格式

### 严重问题
> [!danger] 问题标题
> 描述和影响

### 警告
> [!warning] 警告标题
> 描述和建议

### 建议
> [!tip] 优化建议
> 具体可执行的改进建议

## 审查检查点

- [ ] 命名规范
- [ ] 代码复杂度
- [ ] 错误处理
- [ ] 安全问题
- [ ] 性能优化
- [ ] 代码重复
- [ ] 注释质量
- [ ] 类型安全
```

## Agent 最佳实践

### 命名规范

```bash
✅ 好的命名：
- code-reviewer
- test-generator
- api-explorer
- config-validator

❌ 不好的命名：
- helper           # 太泛
- my-agent         # 无意义
- do_something      # snake_case 应该用 kebab-case
```

### 颜色选择指南

| 颜色 | 适用场景 |
|--------|----------|
| `blue` | 分析、审查、探索 |
| `cyan` | 信息展示、文档 |
| `green` | 生成、创建、构建 |
| `yellow` | 验证、警告、检查 |
| `red` | 安全、严重错误 |
| `magenta` | 转换、创意生成 |

### 模型选择指南

```yaml
# 简单任务，快速响应
model: haiku

# 标准任务，平衡性能和质量
model: inherit   # 或 sonnet

# 复杂推理，需要深度分析
model: sonnet

# 最高质量要求
model: opus
```

### 工具权限原则

> [!tip] 最小权限原则
> 只给 agent 必要的工具，而不是全部。

```yaml
# ❌ 不推荐：给予过多权限
tools: ["*"]

# ✅ 推荐：只给必要的工具
tools: ["Read", "Glob", "Grep"]
```

## 测试和验证

### 使用 Claude Code 测试

```bash
# 1. 启动带有你的插件的 Claude
claude --plugin-dir /path/to/my-plugin

# 2. 测试触发
"用 code-reviewer agent 审查这段代码"

# 3. 验证 agent 是否被正确触发
```

### 使用 plugin-dev 的验证工具

```bash
# plugin-dev 提供了验证脚本
./scripts/validate-agent.sh agents/my-agent.md
```

## 发布到市场

当你完成插件开发后，可以发布到 claude-code-marketplace：

```bash
# 参考官方发布指南
https://github.com/anthropics/claude-code-marketplace/blob/main/docs/PLUGIN_PUBLISHING.md
```

---

# CLI 中使用 Subagent 的模式

## 模式 1：让 Claude 自主探索

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

## 模式 2：并行搜索多个话题

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
    Agent 1: 搜索错误处理相关的代码
    Agent 2: 搜索认证相关的代码
    Agent 3: 搜索数据库配置相关代码

Claude: 搜索完成，结果如下：
    [三个话题的分析结果...]
```

## CLI 提示词模式

### 探索型提示词

```bash
"探索这个项目的结构，找出所有 API 端点"
"了解这个项目是如何组织组件的"
"找出处理用户输入的所有地方"
```

### 研究型提示词

```bash
"研究这个项目中错误处理的所有实现方式"
"深入分析认证系统的完整流程"
"找出所有数据库查询的模式和优化点"
```

### 规划型提示词

```bash
"规划如何为这个项目添加多语言支持"
"设计用户权限系统的实现方案"
"规划将代码库迁移到 TypeScript 的步骤"
```

### 使用自定义 Agent

```bash
"用 code-reviewer agent 审查这段代码"
"让 test-generator agent 为这个函数生成测试"
```

## 常见问题

> [!faq] Q: 为什么有时候 Claude 不使用 subagent？
> A: Subagent 的启动有成本。对于简单的、单次性的操作（如读取一个文件、搜索一个类名），Claude 会直接使用专用工具更快。只有在真正需要多轮、复杂操作时才会启动。

> [!faq] Q:我能在 CLI 中创建自定义 subagent 吗？
> A: 可以！但需要通过创建**插件（Plugin）**来实现。在插件目录的 `agents/` 文件夹中创建 `.md` 文件定义 agent。

> [!faq] Q: 如何测试我创建的 agent？
> A: 使用 `claude --plugin-dir /path/to/my-plugin` 启动带有你插件的 Claude，然后尝试触发你的 agent。

> [!faq] Q: plugin-dev 插件是什么？
> A: `plugin-dev` 是官方提供的插件开发工具包，包含 `agent-creator` agent，可以帮助你快速生成高质量的 agent 配置。

## 参考资源

- [Agent SDK Overview](https://docs.anthropic.com/claude-code/tools/task)
- [Plugin 开发指南](https://github.com/anthropics/claude-code-marketplace/tree/main/plugins/plugin-dev)
- [Claude Code Marketplace](https://github.com/anthropics/claude-code-marketplace)

## 相关概念

[[Claude Code 基础]] | [[MCP 服务器]] | [[Agent Skills]]
