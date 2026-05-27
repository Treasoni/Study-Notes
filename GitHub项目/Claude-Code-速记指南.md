---
title: Claude Code 速记指南
source: https://x.com/affaan/status/2012378465664745795
author:
  - "@affaan"
date: 2025-09-16
created: 2026-05-27
description: "Claude Code 10个月日常使用完整设置指南：Skills、Hooks、Subagents、MCPs、Plugins 及实战经验总结"
tags:
  - claude-code
  - productivity
  - workflow
  - AI-tooling
---

# Claude Code 速记指南

> [!quote] 来源
> @affaan (cogsec) 经过 10 个月日常使用后的完整设置总结，曾获 Anthropic x Forum Ventures Hackathon 冠军

## 概述

Claude Code 是 Anthropic 推出的 AI 编程工具，本文总结了其核心概念：Skills（技能）、Hooks（钩子）、Subagents（子代理）、MCPs（模型上下文协议）和 Plugins（插件）。作者从 2025 年 2 月实验版开始使用，并在纽约黑客马拉松中完全基于 Claude Code 完成了 Zenith 项目。

---

## 1. Skills and Commands 技能与命令

### 概念区分

| 类型 | 存储位置 | 用途 |
|------|----------|------|
| **Skills** | `~/.claude/skills/` | 广泛的工作流程定义 |
| **Commands** | `~/.claude/commands/` | 快速可执行的提示 |

### 核心理解

Skills 像规则一样运作，限制在特定范围和工作流程中。它们是执行特定工作流程时发出提示的**简写形式**。

### 典型使用场景

- **/refactor-clean** — 清理无用代码和 .md 文件
- **/tdd** — 测试驱动开发
- **/e2e** — 端到端测试
- **/test-coverage** — 测试覆盖率检查

### 技能结构示例

```bash
~/.claude/skills/
├── pmx-guidelines.md      # 项目特定模式
├── coding-standards.md    # 语言最佳实践
├── tdd-workflow/          # 多文件技能（含 README.md）
└── security-review/       # 基于检查清单的技能
```

### 命令链

可以在单个提示中将多个技能和命令串联使用，实现复杂工作流。

---

## 2. Hooks 钩子系统

### 6 种钩子类型

| 钩子类型 | 触发时机 | 典型用途 |
|----------|----------|----------|
| **PreToolUse** | 工具执行前 | 验证、提醒 |
| **PostToolUse** | 工具完成后 | 格式化、反馈循环 |
| **UserPromptSubmit** | 用户发送消息时 | 预处理输入 |
| **Stop** | Claude 回答完毕时 | 最终检查 |
| **PreCompact** | 上下文压缩前 | 清理、总结 |
| **Notification** | 权限请求时 | 权限确认 |

### 配置示例

```json
{
  "PreToolUse": [
    {
      "matcher": "tool == \"Bash\" && tool_input.command matches \"(npm|pnpm|yarn|cargo|pytest)\"",
      "hooks": [
        {
          "type": "command",
          "command": "if [ -z \"$TMUX\" ]; then echo '[Hook] Consider tmux for session persistence' >&2; fi"
        }
      ]
    }
  ]
}
```

### 专业提示

使用 **hookify** 插件可以通过对话方式创建钩子，无需手动编写 JSON。运行 **/hookify** 并描述需求即可。

---

## 3. Subagents 子代理

### 核心概念

Subagents 是编排器（主 Claude）可以委派任务的进程，拥有有限的权限范围。它们可以在**后台或前台运行**，从而为对话释放上下文资源。

### 关键优势

1. **任务委派** — 主代理将复杂任务分解给子代理
2. **权限隔离** — 每个子代理可配置不同的工具权限
3. **并行执行** — 多个子代理可同时处理独立任务
4. **技能自主** — 子代理可自主调用其技能集

### 典型子代理结构

```bash
~/.claude/agents/
├── planner.md           # 功能实现规划
├── architect.md         # 系统设计决策
├── tdd-guide.md         # 测试驱动开发
├── code-reviewer.md     # 质量/安全审查
├── security-reviewer.md # 漏洞分析
├── build-error-resolver.md
├── e2e-runner.md
├── refactor-cleaner.md
└── doc-updater.md       # 文档同步
```

---

## 4. Rules and Memory 规则与记忆

### 两种策略

1. **单文件 CLAUDE.md** — 所有规则集中在一个文件
2. **规则文件夹** — 按关注点分组的模块化 .md 文件

### 规则文件夹示例

```bash
~/.claude/rules/
├── security.md      # 无硬编码密钥，输入验证
├── coding-style.md  # 不可变性，文件组织
├── testing.md       # TDD 工作流，80% 覆盖率
├── git-workflow.md  # 提交格式，PR 流程
├── agents.md        # 子代理委派时机
└── performance.md   # 模型选择（Haiku/Sonnet/Opus）
```

### 规则示例

> [!example] 好的规则示例
> - 代码库中不使用表情符号
> - 前端设计避免紫色调
> - 部署前必须测试代码
> - 优先模块化代码而非巨型文件
> - 永远不提交 console.log

---

## 5. MCPs Model Context Protocol

### 核心定位

MCPs 连接 Claude 与外部服务。它不是 API 的替代品，而是围绕 API 的**提示驱动包装器**，提供更大的灵活性。

### 典型应用

**Supabase MCP** — 直接拉取特定数据，在上游直接运行 SQL，无需复制粘贴。

### Chrome in Claude

内置插件 MCP，允许 Claude 自主控制浏览器，点击查看内容工作方式。

### ⚠️ 关键警告：上下文窗口管理

> [!warning] 上下文窗口危机
> 启用过多 MCP 会严重消耗上下文窗口。200k 的上下文窗口在启用过多工具后可能只剩下 70k。

**实践经验：**
- 配置 20-30 个 MCP
- 保持 **< 10 个启用**
- 活跃工具数 **< 80 个**

### 配置示例

```json
// 用户级配置
{
  "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"] },
  "supabase": { "command": "npx", "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=YOUR_REF"] },
  "memory": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] },
  "sequential-thinking": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"] }
}
```

**项目级禁用：**

```json
"disabledMcpServers": [
  "playwright",
  "cloudflare-workers-builds",
  "AbletonMCP",
  "context7",
  "magic"
]
```

---

## 6. Plugins 插件系统

### 与 MCP 的区别

Plugin 将工具打包便于安装，包含技能、MCP、钩子或工具的组合。

### 安装流程

```bash
# 添加市场
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep

# 打开 Claude，运行 /plugins，找到新市场并安装
```

### LSP 插件价值

对于频繁在编辑器外运行 Claude Code 的用户，语言服务器协议（LSP）插件特别有用，提供：
- 实时类型检查
- 跳转定义
- 智能补全

### 推荐插件

```markdown
# TypeScript / Python 智能
typescript-lsp@claude-plugins-official
pyright-lsp@claude-plugins-official

# 工作流增强
hookify@claude-plugins-official
mgrep@Mixedbread-Grep

# 安全与代码质量
security-guidance@claude-code-plugins
code-review@claude-code-plugins

# 其他
ralph-wiggum@claude-code-plugins       # 循环自动化
frontend-design@claude-code-plugins    # UI/UX 模式
commit-commands@claude-code-plugins    # Git 工作流
pr-review-toolkit@claude-code-plugins  # PR 自动化
context7@claude-plugins-official       # 实时文档
```

---

## 7. Tips and Tricks 实用技巧

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| **Ctrl+U** | 删除整行 |
| **!** | 快速 bash 命令前缀 |
| **@** | 搜索文件 |
| **/** | 启动斜杠命令 |
| **Shift+Enter** | 多行输入 |
| **Tab** | 切换 thinking 显示 |
| **Esc Esc** | 中断 Claude / 恢复代码 |

### 并行工作流

- **/fork** — 分叉对话，并行执行非重叠任务
- **Git Worktrees** — 无冲突的并行 Claude 实例

```bash
git worktree add ../feature-branch feature-branch
# 每个 worktree 运行独立的 Claude 实例
```

### tmux 集成

```bash
tmux new -s dev
# Claude 在此运行命令，可分离和重新附加
tmux attach -t dev
```

### 搜索工具

**mgrep > grep** — 显著优于 ripgrep/grep

```bash
mgrep "function handleSubmit"  # 本地搜索
mgrep --web "Next.js 15 app router changes"  # 网页搜索
```

### 其他实用命令

- **/rewind** — 返回上一状态
- **/statusline** — 自定义显示（分支、上下文 %、待办）
- **/checkpoints** — 文件级撤销点
- **/compact** — 手动触发上下文压缩

---

## 8. Editor Integration 编辑器集成

### Zed（作者首选）

**优势：**
- Rust 编写的轻量级编辑器
- Agent Panel 集成 — 实时跟踪 Claude 的文件变更
- **CMD+Shift+R** — 快速访问自定义命令
- 最小资源占用 — 不与 Claude 争抢系统资源
- 完整 Vim 模式支持

**协作流程：**
1. 分屏 — 一侧终端运行 Claude Code，另一侧编辑器
2. **Ctrl+G** — 快速打开 Claude 当前工作的文件
3. 启用自动保存
4. 使用编辑器的 Git 功能审查 Claude 的更改
5. 启用文件监视器

### VSCode / Cursor

同样可行，支持：
- 终端模式
- **\ide** 启用 LSP 功能的自动同步
- 或使用更集成的扩展

---

## 9. 作者的完整配置

### 启用的插件（通常 4-5 个）

```markdown
ralph-wiggum@claude-code-plugins       # Loop automation
frontend-design@claude-code-plugins    # UI/UX patterns
commit-commands@claude-code-plugins    # Git workflow
security-guidance@claude-code-plugins  # Security checks
pr-review-toolkit@claude-code-plugins  # PR automation
typescript-lsp@claude-plugins-official # TS intelligence
hookify@claude-plugins-official        # Hook creation
code-simplifier@claude-plugins-official
feature-dev@claude-code-plugins
explanatory-output-style@claude-code-plugins
code-review@claude-code-plugins
context7@claude-plugins-official       # Live documentation
pyright-lsp@claude-plugins-official    # Python types
mgrep@Mixedbread-Grep                  # Better search
```

### 关键 Hooks 配置

```json
{
  "PreToolUse": [
    { "matcher": "npm|pnpm|yarn|cargo|pytest", "hooks": ["tmux reminder"] },
    { "matcher": "Write && .md file", "hooks": ["block unless README/CLAUDE"] },
    { "matcher": "git push", "hooks": ["open editor for review"] }
  ],
  "PostToolUse": [
    { "matcher": "Edit && .ts/.tsx/.js/.jsx", "hooks": ["prettier --write"] },
    { "matcher": "Edit && .ts/.tsx", "hooks": ["tsc --noEmit"] },
    { "matcher": "Edit", "hooks": ["grep console.log warning"] }
  ],
  "Stop": [
    { "matcher": "*", "hooks": ["check modified files for console.log"] }
  ]
}
```

---

## 10. 核心经验总结

> [!success] 5 Key Takeaways
>
> 1. **不要过度复杂化** — 把配置当作微调，而非架构设计
> 2. **上下文窗口很珍贵** — 禁用未使用的 MCP 和插件
> 3. **并行执行** — 分叉对话，使用 git worktrees
> 4. **自动化重复任务** — 用 Hooks 处理格式化、linting、提醒
> 5. **限制子代理范围** — 有限工具 = 专注执行

---

## 相关资源

- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)
- [Memory System](https://code.claude.com/docs/en/memory)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [MCP Overview](https://code.claude.com/docs/en/mcp-overview)
