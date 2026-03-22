---
tags: [ai, 基础概念, hook, 自动化]
created: 2026-03-22
updated: 2026-03-22
---

# Hook 钩子

> [!info] 概述
> **一句话定义**：Hooks 是用户定义的 shell 命令/HTTP 端点/LLM 提示，在 Claude Code 生命周期的特定时间点自动执行。
> **通俗比喻**：就像 JavaScript 中的事件监听器 —— 当特定事件发生时，自动触发你预设的代码。

## 核心概念

### 是什么

Hook（钩子）是一种**事件驱动的自动化机制**，允许你在 Claude Code 运行过程中的特定"时机"插入自定义逻辑。

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code 生命周期                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  会话开始 ──→ 用户输入 ──→ 工具执行 ──→ 会话结束            │
│      │           │           │           │                  │
│      ▼           ▼           ▼           ▼                  │
│   [Hook]      [Hook]      [Hook]      [Hook]                │
│      │           │           │           │                  │
│   你的代码    你的代码    你的代码    你的代码               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 为什么需要

| 问题 | Hook 的解决方案 |
|------|-----------------|
| AI 可能忘记执行某些操作 | 通过 Hook **确保**操作必定发生 |
| 重复的手动确认 | 自动批准或拒绝特定权限请求 |
| 代码风格不一致 | 在编辑后自动格式化 |
| 敏感文件被误改 | 在编辑前拦截并阻止 |
| 团队协作需要审计 | 自动记录所有操作到日志 |

### 通俗理解

**🎯 比喻**：Hook 就像是公司的"前台接待员"

- 当有人来访（事件发生），接待员会按照预定流程处理
- 比如：VIP 客户来了 → 自动通知老板（触发自定义逻辑）
- 比如：推销员来了 → 自动拒绝（阻止操作）

**📦 示例**：
```json
// 当 Claude 要编辑 .env 文件时，自动阻止
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "echo 'Blocked: sensitive file' && exit 2"
      }]
    }]
  }
}
```

## Hook 类型

Claude Code 支持 4 种 Hook 类型：

| 类型 | 说明 | 执行方式 | 适用场景 |
|------|------|----------|----------|
| `command` | 执行 shell 命令 | 本地终端 | 格式化、验证、日志记录 |
| `http` | POST 到 HTTP 端点 | 网络请求 | 远程审计、团队通知 |
| `prompt` | 单轮 LLM 评估 | Claude 判断 | 需要判断力的决策 |
| `agent` | 多轮 Agent 验证 | 独立 Agent | 需要读文件/运行命令的验证 |

### 类型详解

#### 1. Command Hook
最常用的类型，执行本地 shell 命令。

```json
{
  "type": "command",
  "command": "prettier --write $CLAUDE_FILE_PATH"
}
```

#### 2. HTTP Hook
将事件数据 POST 到远程服务器。

```json
{
  "type": "http",
  "url": "https://api.example.com/claude-webhook"
}
```

#### 3. Prompt Hook
让 LLM 做出判断，返回 approve/deny/modify。

```json
{
  "type": "prompt",
  "prompt": "检查这个命令是否安全。如果涉及 rm -rf 或 sudo，返回 deny；否则返回 approve。"
}
```

#### 4. Agent Hook
启动一个独立的 Agent 进行多轮验证。

```json
{
  "type": "agent",
  "prompt": "检查要修改的文件是否包含敏感信息，如果包含则阻止修改。"
}
```

## Hook 事件

Claude Code 提供了 **23 种 Hook 事件**，按生命周期分类：

### 会话级别

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `SessionStart` | 会话开始/恢复 | 初始化环境、加载配置 |
| `SessionEnd` | 会话结束 | 清理资源、发送总结 |
| `InstructionsLoaded` | CLAUDE.md 加载时 | 注入额外指令 |

### 用户交互

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `UserPromptSubmit` | 用户提交提示前 | 检查输入、注入上下文 |
| `Notification` | 发送通知时 | 转发到其他渠道 |

### 工具执行

| 事件 | 触发时机 | 可阻止 | 典型用途 |
|------|----------|--------|----------|
| `PreToolUse` | 工具执行前 | ✅ | 安全检查、阻止危险操作 |
| `PostToolUse` | 工具执行成功后 | ❌ | 格式化、日志、通知 |
| `PostToolUseFailure` | 工具执行失败后 | ❌ | 错误处理、告警 |
| `PermissionRequest` | 权限对话框出现时 | ✅ | 自动批准/拒绝 |

### Agent 相关

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `SubagentStart` | 子 Agent 启动 | 日志记录 |
| `SubagentStop` | 子 Agent 停止 | 结果处理 |
| `TeammateIdle` | 团队成员即将空闲 | 任务分配 |
| `TaskCompleted` | 任务标记完成 | 通知、清理 |

### 其他事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `Stop` / `StopFailure` | Claude 停止响应 | 清理、总结 |
| `ConfigChange` | 配置文件变更 | 重新加载 |
| `PreCompact` / `PostCompact` | 上下文压缩前后 | 保存/恢复状态 |
| `WorktreeCreate` / `WorktreeRemove` | Worktree 操作 | 同步配置 |
| `Elicitation` / `ElicitationResult` | MCP 用户输入请求 | 审计 |

## 与其他概念的关系

### Hook vs Skills

| 特性 | Hook | Skill |
|------|------|-------|
| **触发方式** | 事件驱动（自动） | 用户调用（手动） |
| **主要目的** | 自动化、拦截、验证 | 扩展功能、复用操作 |
| **执行时机** | 生命周期特定点 | 用户请求时 |
| **典型场景** | 代码格式化、安全检查 | 代码审查、文档生成 |

### Hook vs MCP

| 特性 | Hook | MCP |
|------|------|-----|
| **本质** | 事件回调机制 | 工具/资源协议 |
| **方向** | Claude → 你的代码 | Claude ← 外部服务 |
| **主要目的** | 自动化、控制 | 扩展能力边界 |
| **典型场景** | 拦截敏感操作、自动格式化 | 访问数据库、调用 API |

### Hook vs CLAUDE.md

| 特性 | Hook | CLAUDE.md |
|------|------|-----------|
| **作用** | 执行代码 | 提供指令 |
| **确定性** | 强制执行 | AI 可能忽略 |
| **适用场景** | 必须发生的操作 | 建议性的规则 |

**最佳配合**：
- CLAUDE.md 告诉 AI "应该怎么做"
- Hook 确保 AI "必须这样做"

## 最佳实践

### 1. 安全防护

```json
// 阻止危险命令
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo \"$CLAUDIAN_TOOL_INPUT\" | grep -E 'rm -rf|sudo|chmod' && exit 2 || exit 0"
      }]
    }]
  }
}
```

### 2. 自动格式化

```json
// 编辑后自动格式化
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "prettier --write $CLAUDE_FILE_PATH"
      }]
    }]
  }
}
```

### 3. 桌面通知

```json
// 任务完成时通知
{
  "hooks": {
    "TaskCompleted": [{
      "type": "command",
      "command": "notify-send 'Claude Code' 'Task completed!'"
    }]
  }
}
```

### 4. 异步执行

对于耗时操作，使用 `background: true` 避免阻塞：

```json
{
  "type": "command",
  "command": "long-running-task.sh",
  "background": true
}
```

## 常见问题

**Q: Hook 和 Slash 命令有什么区别？**

A: Slash 命令是用户主动调用的，Hook 是事件触发的。Slash 命令需要你输入 `/commit`，Hook 会在特定事件发生时自动运行。

**Q: Hook 可以修改 Claude 的行为吗？**

A: 可以。通过返回特定的退出码或 JSON，Hook 可以：
- `exit 0`：允许操作继续
- `exit 2`：阻止操作并显示错误
- 返回 JSON：修改工具的输入参数

**Q: 如何调试 Hook？**

A: 使用 `/hooks` 命令查看当前配置的 Hook，或启用 debug 模式查看详细日志。

**Q: Hook 会在什么环境下执行？**

A: Command Hook 在你的终端环境下执行，可以访问环境变量和 PATH 中的命令。

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[02-工具使用/Claude Code Hooks 使用指南]] - 详细配置和实战示例
- [[01-基础概念/Skills 是什么]] - 用户主动调用的技能系统
- [[03-进阶应用/CLAUDE.md 使用指南]] - 项目级指令配置
- [[02-工具使用/Claude Code 常用功能]] - /hooks 命令速查

## 参考资料

- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - 完整技术参考
- [Automate workflows with hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide) - 使用指南
- [How to configure hooks - Claude Blog](https://claude.com/blog/how-to-configure-hooks) - 官方配置详解
- [Claude Code settings.json: Complete config guide (2026)](https://www.eesel.ai/blog/settings-json-claude-code) - 配置层级详解
