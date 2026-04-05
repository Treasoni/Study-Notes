---
tags: [claude, ai, 工具使用, subagents, 代理, 任务委托]
created: 2026-04-05
updated: 2026-04-05
---

# Claude Code Subagents 完整指南

> [!info] 概述
> **一句话定义**：Subagents 是 Claude Code 的专业化 AI 助手系统，可以委托特定任务给拥有独立上下文窗口和专用工具权限的专家代理。
> **通俗比喻**：就像一个项目经理（主 Agent）带领一群专业顾问（Subagents）—— 每个顾问有自己的专业���域、独立的工作空间，完成后向经理汇报结果。

## 核心概念

### 是什么

Subagents 是 Claude Code 中的**专业化 AI 助手**，具备以下特点：
- 🎯 **独立上下文**：每个 Subagent 拥有独立的上下文窗口，与主对话隔离
- 🔧 **可配置工具**：可以精确控制每个 Subagent 能使用的工具
- 📝 **自定义系统提示**：为特定任务定制专业知识和行为模式
- 🔄 **任务委托**：主 Agent 可以将复杂任务委托给专业 Subagent

### 为什么需要

**解决的问题**：
- ❌ 复杂任务污染主对话上下文
- ❌ 需要专业知识但主 Agent 不够专精
- ❌ 长时间运行的任务消耗主上下文
- ❌ 需要并行执行多个任务

**Subagents 提供的能力**：
- ✅ 保持主上下文清洁，防止 token 耗尽
- ✅ 为特定领域提供专业化能力
- ✅ 支持并行执行多个任务
- ✅ 可复用、可共享的专业代理

### 通俗理解

**🎯 比喻**：
- **主 Agent** = 项目经理，负责协调和综合
- **Code Reviewer Subagent** = 代码审查专家，专注代码质量
- **Test Engineer Subagent** = 测试工程师，专注测试覆盖
- **Documentation Writer** = 技术文档撰写者，专注文档质量
- **Debugger Subagent** = 调试专家，专注问题诊断

**📦 架构图**：

```
┌───────────────────��─────────────────────────────────────────┐
│                        用户请求                              │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     主 Agent (协调者)                        │
│  - 分析任务需求                                              │
│  - 决定委托策略                                              │
│  - 综合各 Subagent 结果                                      │
└─────┬───────────┬───────────┬───────────┬─────────────────┘
      ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Code    │ │ Test    │ │ Docs    │ │ Debug   │
│Reviewer │ │ Engineer│ │ Writer  │ │ ger     │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
     ▼           ▼           ▼           ▼
  独立上下文   独立上下文   独立上下文   独立上下文
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Subagents 完整参考指南

---

## 快速开始

### 使用 `/agents` 命令

**快速启动**：
```
/agents
```

**功能**：
- 查看所有可用的 Subagents（内置、用户级、项目级）
- 创建新的 Subagent（引导式设置）
- 编辑现有 Subagent 和工具权限
- 删除自定义 Subagent
- 查看重复定义时的激活状态

### 快速创建 Subagent

**方法 1：使用 `/agents` 命令（推荐）**
```
/agents
# 选择 'Create New Agent'
# 选择项目级或用户级
# 描述你的 Subagent
# 选择要授予的工具（或留空继承全部）
# 保存并使用
```

**方法 2：直接创建文件**

```bash
# 创建项目级 Subagent
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively
run the appropriate tests. If tests fail, analyze the failures and fix
them while preserving the original test intent.
EOF
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Managing Subagents

---

## 文件位置与优先级

### 存储位置

| 优先级 | 类型 | 位置 | 范围 |
|--------|------|------|------|
| 1 (最高) | **CLI 定义** | 通过 `--agents` 标志 (JSON) | 仅当前会话 |
| 2 | **项目 Subagents** | `.claude/agents/` | 当前项目 |
| 3 | **用户 Subagents** | `~/.claude/agents/` | 所有项目 |
| 4 (最低) | **插件 Subagents** | 插件 `agents/` 目录 | 通过插件 |

当存在同名 Subagent 时，**高优先级来源优先**。

### 项目结构

```
project/
├── .claude/
│   └── agents/
│       ├── code-reviewer.md
│       ├── test-engineer.md
│       ├── documentation-writer.md
│       ├── secure-reviewer.md
│       ├── implementation-agent.md
│       ├── debugger.md
│       └── data-scientist.md
└── ...
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - File Locations

---

## 配置格式

### YAML Frontmatter

Subagent 通过 YAML frontmatter + Markdown 系统提示定义：

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # 可选 - 省略则继承所有工具
disallowedTools: tool4  # 可选 - 明确禁止的工具
model: sonnet  # 可选 - sonnet, opus, haiku, 或 inherit
permissionMode: default  # 可选 - 权限模式
maxTurns: 20  # 可选 - 限制代理轮次
skills: skill1, skill2  # 可选 - 预加载的技能
mcpServers: server1  # 可选 - 可用的 MCP 服务器
memory: user  # 可选 - 持久化记忆范围
background: false  # 可选 - 后台运行
effort: high  # 可选 - 推理努力程度
isolation: worktree  # 可选 - git worktree 隔离
initialPrompt: "Start by analyzing the codebase"  # 可选 - 自动提交的首轮提示
hooks:  # 可选 - 组件级钩子
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.
```

### 配置字段详解

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | ✅ | 唯一标识符（小写字母和连字符） |
| `description` | ✅ | 自然语言描述。包含 "use PROACTIVELY" 鼓励自动调用 |
| `tools` | ❌ | 逗号分隔的工具列表。省略则继承所有工具 |
| `disallowedTools` | ❌ | 明确禁止的工具列表 |
| `model` | ❌ | 模型：`sonnet`, `opus`, `haiku`, 完整模型ID, 或 `inherit` |
| `permissionMode` | ❌ | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | ❌ | 最大代理轮次限制 |
| `skills` | ❌ | 预加载的技能列表 |
| `mcpServers` | ❌ | 可用的 MCP 服务器 |
| `hooks` | ❌ | 组件级钩子 (PreToolUse, PostToolUse, Stop) |
| `memory` | ❌ | 持久化记忆范围：`user`, `project`, 或 `local` |
| `background` | ❌ | 设为 `true` 始终后台运行 |
| `effort` | ❌ | 推理努力级别：`low`, `medium`, `high`, 或 `max` |
| `isolation` | ❌ | 设为 `worktree` 给予独立的 git worktree |
| `initialPrompt` | ❌ | 作为主 Agent 运行时自动提交的首轮提示 |

### 工具配置选项

**选项 1：继承所有工具（省略字段）**
```markdown
---
name: full-access-agent
description: Agent with all available tools
---
```

**选项 2：指定特定工具**
```markdown
---
name: limited-agent
description: Agent with specific tools only
tools: Read, Grep, Glob, Bash
---
```

**选项 3：条件工具访问**
```markdown
---
name: conditional-agent
description: Agent with filtered tool access
tools: Read, Bash(npm:*), Bash(test:*)
---
```

### CLI 配置方式

使用 `--agents` 标志为单个会话定义 Subagent：

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Configuration

---

## 内置 Subagents

Claude Code 包含多个始终可用的内置 Subagents：

| Agent | 模型 | 用途 |
|-------|------|------|
| **general-purpose** | 继承 | 复杂多步骤任务 |
| **Plan** | 继承 | Plan 模式的研究任务 |
| **Explore** | Haiku | 只读代码库探索（quick/medium/very thorough） |
| **Bash** | 继承 | 独立上下文中执行终端命令 |
| **statusline-setup** | Sonnet | 配置状态栏 |
| **Claude Code Guide** | Haiku | 回答 Claude Code 功能问题 |

### General-Purpose Subagent

| 属性 | 值 |
|------|-----|
| **模型** | 继承自父级 |
| **工具** | 所有工具 |
| **用途** | 复杂研究任务、多步骤操作、代码修改 |

**使用场景**：需要同时进行探索和修改的复杂推理任务。

### Plan Subagent

| 属性 | 值 |
|------|-----|
| **模型** | 继承自父级 |
| **工具** | Read, Glob, Grep, Bash |
| **用途** | Plan 模式下自动研究代码库 |

**使用场景**：Claude 需要在呈现计划前理解代码库。

### Explore Subagent

| 属性 | 值 |
|------|-----|
| **模型** | Haiku（快速、低延迟） |
| **模式** | 严格只读 |
| **工具** | Glob, Grep, Read, Bash（仅只读命令） |
| **用途** | 快速代码库搜索和分析 |

**彻底程度级别**：
- **"quick"** - 快速搜索，最小探索，适合查找特定模式
- **"medium"** - 适度探索，平衡速度和彻底性，默认方式
- **"very thorough"** - 跨多个位置和命名约定的全面分析

**使用场景**：搜索/理解代码而不进行修改。

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Built-in Subagents

---

## 使用 Subagents

### 自动委托

Claude 会根据以下因素主动委托任务：
- 请求中的任务描述
- Subagent 配置中的 `description` 字段
- 当前上下文和可用工具

**鼓励主动使用**，在 `description` 中包含 "use PROACTIVELY" 或 "MUST BE USED"：

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use PROACTIVELY after writing or modifying code.
---
```

### 显式调用

可以显式请求特定 Subagent：

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

### @-Mention 调用

使用 `@` 前缀保证调用特定 Subagent（绕过自动委托启发式）：

```
> @"code-reviewer (agent)" review the auth module
```

### 会话级 Agent

整个会话使用特定 Agent 作为主 Agent：

```bash
# 通过 CLI 标志
claude --agent code-reviewer

# 通过 settings.json
{
  "agent": "code-reviewer"
}
```

### 列出可用 Agents

```bash
claude agents
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Using Subagents

---

## 可恢复 Agents

Subagents 可以继续之前的对话，保持完整上下文：

```
# 初始调用
> Use the code-analyzer agent to start reviewing the authentication module
# 返回 agentId: "abc123"

# 稍后恢复
> Resume agent abc123 and now analyze the authorization logic as well
```

**使用场景**：
- 跨多个会话的长期研究
- 不丢失上下文的迭代优化
- 保持上下文的多步骤工作流

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Resumable Agents

---

## 链式 Subagents

按顺序执行多个 Subagents：

```
> First use the code-analyzer subagent to find performance issues,
  then use the optimizer subagent to fix them
```

这实现了复杂工作流，一个 Subagent 的输出作为另一个的输入。

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Chaining Subagents

---

## Subagent 持久化记忆

`memory` 字段为 Subagent 提供跨会话的持久化目录。

### 记忆范围

| 范围 | 目录 | 用途 |
|------|------|------|
| `user` | `~/.claude/agent-memory/<name>/` | 所有项目的个人笔记和偏好 |
| `project` | `.claude/agent-memory/<name>/` | 与团队共享的项目特定知识 |
| `local` | `.claude/agent-memory-local/<name>/` | 不提交到版本控制的本地项目知识 |

### 工作原理

- 记忆目录中 `MEMORY.md` 的前 200 行自动加载到 Subagent 系统提示
- `Read`、`Write` 和 `Edit` 工具自动启用，供 Subagent 管理记忆文件
- Subagent 可根据需要在记忆目录中创建其他文件

### 配置示例

```markdown
---
name: researcher
memory: user
---

You are a research assistant. Use your memory directory to store findings,
track progress across sessions, and build up knowledge over time.

Check your MEMORY.md file at the start of each session to recall previous context.
```

**数据流图**：

```
┌──────────────────┐     写入     ┌──────────────────┐
│ Subagent         │ ──────────▶ │ MEMORY.md        │
│ Session 1        │             │ (持久化)          │
└──────────────────┘             └────────┬─────────┘
                                          │
                                          ▼ 加载
┌──────────────────┐             ┌──────────────────┐
│ Subagent         │ ◀────────── │ MEMORY.md        │
│ Session 2        │    更新     │ (持久化)          │
└──────────────────┘ ──────────▶ └────────┬─────────┘
                                          │
                                          ▼ 加载
┌──────────────────┐             ┌──────────────────┐
│ Subagent         │ ◀────────── │ MEMORY.md        │
│ Session 3        │             │ (持久化)          │
└──────────────────┘             └──────────────────┘
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Persistent Memory

---

## 后台 Subagents

Subagents 可以在后台运行，释放主对话用于其他任务。

### 配置

在 frontmatter 中设置 `background: true`：

```markdown
---
name: long-runner
background: true
description: Performs long-running analysis tasks in the background
---
```

### 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+B` | 将当前运行的 Subagent 任务转为后台 |
| `Ctrl+F` | 终止所有后台 Agents（按两次确认） |

### 禁用后台任务

```bash
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Background Subagents

---

## Worktree 隔离

`isolation: worktree` 设置给 Subagent 自己的 git worktree，允许独立修改而不影响主工作树。

### 配置

```markdown
---
name: feature-builder
isolation: worktree
description: Implements features in an isolated git worktree
tools: Read, Write, Edit, Bash, Grep, Glob
---
```

### 工作原理

- Subagent 在独立 git worktree 的单独分支上操作
- 如果 Subagent 没有修改，worktree 自动清理
- 如果存在修改，返回 worktree 路径和分支名供主 Agent 审查或合并

**流程图**：

```
┌──────────────────┐     生成     ┌──────────────────┐
│ 主工作树         │ ──────────▶ │ 带隔离 Worktree  │
│                  │             │ 的 Subagent      │
└──────────────────┘             └────────┬─────────┘
                                          │
                                          ▼ 修改
                                 ┌──────────────────┐
                                 │ 独立 Git         │
                                 │ Worktree + 分支  │
                                 └────────┬─────────┘
                                          │
                     ┌────────────────────┼────────────────────┐
                     │ 无修改             │ 有修改              │
                     ▼                    ▼                    │
              ┌──────────────┐     ┌──────────────┐           │
              │ 自动清理     │     │ 返回 worktree│           │
              │              │     │ 路径和分支   │           │
              └──────────────┘     └──────────────┘           │
```

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Worktree Isolation

---

## 限制可生成的 Subagents

使用 `Agent(agent_type)` 语法控制 Subagent 可以生成哪些其他 Subagent：

```markdown
---
name: coordinator
description: Coordinates work between specialized agents
tools: Agent(worker, researcher), Read, Bash
---

You are a coordinator agent. You can delegate work to the "worker" and
"researcher" subagents only. Use Read and Bash for your own exploration.
```

此例中，`coordinator` Subagent 只能生成 `worker` 和 `researcher` Subagent。

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Restrict Spawnable Subagents

---

## Agent Teams（实验性）

Agent Teams 协调多个 Claude Code 实例共同处理复杂任务。

> [!note] 注意
> Agent Teams 是实验性功能，需要 Claude Code v2.1.32+。使用前需启用。

### Subagents vs Agent Teams

| 方面 | Subagents | Agent Teams |
|------|-----------|-------------|
| **委托模型** | 父级委托子任务，等待结果 | Team Lead 分配工作，teammate 独立执行 |
| **上下文** | 每个子任务全新上下文，结果提炼返回 | 每个 teammate 维护自己的持久上下文 |
| **协调** | 顺序或并行，由父级管理 | 共享任务列表，自动依赖管理 |
| **通信** | 仅返回值 | 通过 mailbox 的代理间消息 |
| **会话恢复** | 支持 | 不支持 in-process teammates |
| **适用场景** | 聚焦、明确的子任务 | 需要并行工作的大型多文件项目 |

### 启用 Agent Teams

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

或在 `settings.json` 中：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 启动 Team

启用后，在提示中要求 Claude 与 teammates 协作：

```
User: Build the authentication module. Use a team — one teammate for the API endpoints,
      one for the database schema, and one for the test suite.
```

### 显示模式

| 模式 | 标志 | 描述 |
|------|------|------|
| **Auto** | `--teammate-mode auto` | 自动选择最佳显示模式 |
| **In-process** | `--teammate-mode in-process` | 在当前终端内联显示（默认） |
| **Split-panes** | `--teammate-mode tmux` | 在单独的 tmux 或 iTerm2 窗格中打开 |

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Team Lead (协调者)                        │
└────────┬────────────────────────┬───────────────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌─────────────────┐
│ 共享任务列表    │◀────▶│ Mailbox (消息)  │
│ (依赖管理)      │      │                 │
└────────┬────────┘      └────────┬────────┘
         │                        │
    ┌────┴────┬────────────┬──────┴────┐
    ▼         ▼            ▼           ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Team 1 │ │Team 2 │ │Team 3 │ │Team 4 │
│独立   │ │独立   │ │独立   │ │独立   │
│上下文 │ │上下文 │ │上下文 │ │上下文 │
└───────┘ └───────┘ └───────┘ └───────┘
```

### 最佳实践

- **团队规模**：保持 3-5 个 teammates 以获得最佳协调
- **任务大小**：分解为 5-15 分钟的任务
- **避免文件冲突**：将不同文件/目录分配给不同 teammates
- **从简单开始**：先使用 in-process 模式

> [!warning] 警告
> Agent Teams 是实验性功能。先用非关键工作测试，监控 teammate 协调的意外行为。

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Agent Teams

---

## 架构与上下文管理

### 高层架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户                                  │
└─────────────────────────┬───────────────────────────────────┘
                          │ 请求
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   主 Agent (协调者)                          │
│  - 分析任务                                                  │
│  - 委托给专业 Subagents                                      │
│  - 综合结果                                                  │
└─────┬───────────┬───────────┬───────────┬─────────────────┘
      ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Code    │ │ Test    │ │ Docs    │ │ Debug   │
│Reviewer │ │ Engineer│ │ Writer  │ │ ger     │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
     ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ 独立    │ │ 独立    │ │ 独立    │ │ 独立    │
│ 上下文  │ │ 上下文  │ │ 上下文  │ │ 上下文  │
│ 20K tok │ │ 20K tok │ │ 20K tok │ │ 20K tok │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### 上下文管理要点

- 每个 Subagent 获得**全新上下文窗口**，无主对话历史
- 只传递**相关上下文**给 Subagent 的特定任务
- 结果**提炼**返回主 Agent
- 这防止长项目的**上下文 token 耗尽**

### 关键行为

- **无嵌套生成**：Subagents 不能生成其他 Subagents（除非使用 Agent() 语法限制）
- **后台权限**：后台 Subagents 自动拒绝非预批准的权限
- **后台化**：按 `Ctrl+B` 将当前任务转为后台
- **转录存储**：Subagent 转录存储在 `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`
- **自动压缩**：Subagent 上下文在约 95% 容量时自动压缩

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Architecture

---

## 何时使用 Subagents

| 场景 | 使用 Subagent | 原因 |
|------|--------------|------|
| 多步骤复杂功能 | ✅ 是 | 分离关注点，防止上下文污染 |
| 快速代码审查 | ❌ 否 | 不必要的开销 |
| 并行任务执行 | ✅ 是 | 每个 Subagent 有独立上下文 |
| 需要专业知识 | ✅ 是 | 自定义系统提示 |
| 长时间分析 | ✅ 是 | 防止主上下文耗尽 |
| 单一简单任务 | ❌ 否 | 增加不必要的延迟 |

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - When to Use Subagents

---

## 最佳实践

### 设计原则

**✅ 应该做的**：
- 从 Claude 生成的 agents 开始 - 让 Claude 生成初始 Subagent，然后迭代定制
- 设计聚焦的 Subagents - 单一、清晰的职责
- 编写详细的提示 - 包含具体指令、示例和约束
- 限制工具访问 - 只授予必要工具
- 版本控制 - 将项目 Subagents 提交到 git 供团队协作

**❌ 不应该做的**：
- 创建职责重叠的 Subagents
- 给 Subagents 不必要的工具访问
- 对简单单步任务使用 Subagents
- 在一个 Subagent 提示中混合多个关注点
- 忘记传递必要的上下文

### 系统提示最佳实践

1. **明确角色**
   ```markdown
   You are an expert code reviewer specializing in security and performance.
   ```

2. **清晰定义优先级**
   ```markdown
   Review priorities (in order):
   1. Security Issues
   2. Performance Problems
   3. Code Quality
   ```

3. **指定输出格式**
   ```markdown
   For each issue provide: Severity, Category, Location, Description, Fix, Impact
   ```

4. **包含操作步骤**
   ```markdown
   When invoked:
   1. Run git diff to see recent changes
   2. Focus on modified files
   3. Begin review immediately
   ```

### 工具访问策略

1. **从限制开始**：只从必要工具开始
2. **按需扩展**：根据需求添加工具
3. **尽可能只读**：分析类 Agent 使用 Read/Grep
4. **沙箱执行**：将 Bash 命令限制为特定模式

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Best Practices

---

## 示例 Subagents

### 1. Code Reviewer

**用途**：全面的代码质量和可维护性分析

**工具**：Read, Grep, Glob, Bash

**专业化**：
- 安全漏洞检测
- 性能优化识别
- 代码可维护性评估
- 测试覆盖分析

**使用场景**：需要自动化代码审查，关注质量和安全

### 2. Test Engineer

**用途**：测试策略、覆盖分析和自动化测试

**工具**：Read, Write, Bash, Grep

**专业化**：
- 单元测试创建
- 集成测试设计
- 边缘情况识别
- 覆盖分析（>80% 目标）

**使用场景**：需要创建全面的测试套件或覆盖分析

### 3. Documentation Writer

**用途**：技术文档、API 文档和用户指南

**工具**：Read, Write, Grep

**专业化**：
- API 端点文档
- 用户指南创建
- 架构文档
- 代码注释改进

**使用场景**：需要创建或更新项目文档

### 4. Secure Reviewer

**用途**：安全聚焦的代码审查，最小权限

**工具**：Read, Grep

**专业化**：
- 安全漏洞检测
- 认证/授权问题
- 数据暴露风险
- 注入攻击识别

**使用场景**：需要无修改能力的安全审计

### 5. Implementation Agent

**用途**：功能开发的完整实现能力

**工具**：Read, Write, Edit, Bash, Grep, Glob

**专业化**：
- 功能实现
- 代码生成
- 构建和测试执行
- 代码库修改

**使用场景**：需要 Subagent 端到端实现功能

### 6. Debugger

**用途**：错误、测试失败和意外行为的调试专家

**工具**：Read, Edit, Bash, Grep, Glob

**专业化**：
- 根因分析
- 错误调查
- 测试失败解决
- 最小修复实现

**使用场景**：遇到 bug、错误或意外行为

> [!info] 📚 来源
> - [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - Example Subagents

---

## 与其他功能的关系

### 功能对比

| 功能 | 用户调用 | 自动调用 | 持久化 | 外部访问 | 独立上下文 |
|------|----------|----------|--------|----------|------------|
| **Slash Commands** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Subagents** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Memory** | 自动 | 自动 | ✅ | ❌ | ❌ |
| **MCP** | 自动 | ✅ | ❌ | ✅ | ❌ |
| **Skills** | ✅ | ✅ | ❌ | ❌ | ❌ |

### 集成模式

```
┌─────────────────────────────────────────────────────────────┐
│                      用户请求                                │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      主 Agent                                │
└─────┬───────────┬───────────┬───────────┬─────────────────┘
      │           │           │           │
      ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Memory  │ │  MCP    │ │ Skills  │ │Subagents│
│ (上下文)│ │(实时数据)│ │(自动工具)│ │(专家)   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
                                      │
                                      ▼
                              ┌─────────────┐
                              │ 独立上下文  │
                              │ 窗口        │
                              └─────────────┘
```

---

## 常见问题

### Q: Subagents 和 Skills 有什么区别？

| 特性 | Subagents | Skills |
|------|-----------|--------|
| **上下文** | 独立上下文窗口 | 共享主上下文 |
| **调用方式** | 显式或自动委托 | 命令或自动检测 |
| **适用场景** | 复杂、独立的任务 | 快速、上下文相关的操作 |
| **持久化** | 可选 memory 字段 | 无 |

### Q: 如何调试 Subagent 问题？

1. 使用 `/status` 查看当前配置
2. 检查 YAML frontmatter 格式
3. 验证工具名称拼写
4. 查看 Claude Code 日志
5. 检查 `~/.claude/projects/{project}/{sessionId}/subagents/` 中的转录

### Q: Subagent 可以调用其他 Subagent 吗？

默认情况下不可以。需要使用 `Agent(agent_name)` 语法在 `tools` 字段中明确允许。

### Q: 后台 Subagent 的权限如何处理？

后台 Subagents 自动拒绝任何非预批准的权限请求。

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[AI学习/02-工具使用/Claude Code Memory 完整指南]] - Memory 持久化上下文
- [[AI学习/01-基础概念/Skills 是什么]] - Skills 概念详解
- [[AI学习/02-工具使用/Claude Code Hooks 使用指南]] - 事件驱动自动化
- [[AI学习/02-工具使用/Claude Code Slash Commands 完整参考]] - 斜杠命令
- [[AI学习/02-工具使用/Claude Code 插件系统使用指南]] - 插件系统

---

## 参考资料

### 官方资源
- [Claude Code Overview](https://code.claude.com/docs/en/overview) - 官方文档
- [Claude Code Subagents Docs](https://code.claude.com/docs/en/subagents) - Subagents 官方文档

### 社区资源
- [GitHub - claude-howto Subagents Guide](https://github.com/luongnv89/claude-howto/tree/main/04-subagents) - 完整 Subagents 参考
- [Claude Code SubAgents Guide: 30 Free AI Developer Tools](https://medium.com/@kelvin.luong/claude-code-subagents-guide-30-free-ai-developer-tools-b6d2d0d6e5d8) - 30 个免费工具
- [dl-ezo/claude-code-sub-agents](https://github.com/dl-ezo/claude-code-sub-agents) - 35+ Subagents 集合
- [rshah515/claude-code-subagents](https://github.com/rshah515/claude-code-subagents) - 133 个专业 Subagents

### 相关功能
- [Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Skills 完整参考
- [Hooks Guide](https://code.claude.com/docs/en/hooks) - 事件驱动自动化
- [Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - 持久化上下文
