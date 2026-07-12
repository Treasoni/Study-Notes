---
title: Claude Code Hooks 使用指南
tags: [claude, ai, 工具使用, hook, 自动化]
created: 2026-03-22
updated: 2026-07-12
status: updated
source_project: claude-code-tutorial
---

# Claude Code Hooks 使用指南

> [!info] 文档定位
> **本文档是 Hook 的详细使用指南**。概念理解请先阅读 [[01-基础概念/Hook钩子]]。

> [!info] 概述
> **一句话定义**：通过配置文件定义自动化规则，在 Claude Code 生命周期的特定时间点执行自定义逻辑。
>
> **通俗比喻**：就像给 Claude Code 设置"触发器"，当特定事件发生时自动执行你预设的操作。

---

## 快速开始

### 最简配置示例

在项目根目录创建 `.claude/settings.json`：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [{ "type": "command", "command": "notify-send 'Claude' '✅ 任务完成！'" }]
      }
    ]
  }
}
```

### 验证配置

```bash
/hooks    # 在 Claude Code 中查看已配置的 Hook
```

---

## 配置详解

### 配置位置与优先级

| 位置 | 作用范围 | 可共享 | 优先级 |
|------|----------|--------|--------|
| `~/.claude/settings.json` | 所有项目 | ❌ 个人 | 最低 |
| `.claude/settings.json` | 单个项目 | ✅ 可提交 Git | 中 |
| `.claude/settings.local.json` | 单个项目 | ❌ 不提交 | 高 |
| Managed settings | 组织级 | ✅ IT 管理 | 高 |
| Plugin `hooks/hooks.json` | 插件启用时 | ✅ 可提交 | 高 |
| Skill/Agent frontmatter | 组件活跃时 | ✅ | 最高 |

> [!tip] 配置建议
> - **团队共享规则** → `.claude/settings.json`
> - **个人密钥** → `.claude/settings.local.json`（加入 `.gitignore`）
> - **全局偏好** → `~/.claude/settings.json`

### 基本结构

```json
{
  "hooks": {
    "事件名称": [
      {
        "matcher": "匹配模式",
        "hooks": [
          {
            "type": "command|http|prompt|agent",
            "command": "shell命令",
            "timeout": 60000
          }
        ]
      }
    ]
  }
}
```

### Matcher 模式语法

| 语法 | 示例 | 匹配规则 |
|------|------|----------|
| 精确匹配 | `"Bash"` | 只匹配 Bash 工具 |
| 多个匹配 | `"Bash\|Edit"` | 匹配 Bash 或 Edit |
| 正则表达式 | `"Bash(rm\|sudo)"` | 使用正则表达式 |
| 通配符 | `"*"` 或 `""` | 匹配所有工具 |
| MCP 工具 | `"mcp__memory__.*"` | 匹配特定 MCP 服务器 |

```json
// 常用示例
"matcher": "Bash"                    // 只匹配 Bash
"matcher": "Edit|Write"              // 匹配 Edit 和 Write
"matcher": "Bash(rm)"                // 匹配包含 rm 的 Bash 命令
"matcher": "Edit", "pathMatcher": "\\.env$"  // 匹配 .env 文件的编辑
```

---

## Hook 类型

Claude Code 支持 **5 种 Hook 类型**：

### Command Hook（默认）

执行 Shell 命令，通过 stdin/stdout 通信：

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

### HTTP Hook（v2.1.63+）

发送事件到远程服务器：

```json
{
  "type": "http",
  "url": "https://${API_HOST}/hooks/notify",
  "allowedEnvVars": ["API_HOST"],
  "timeout": 5000
}
```

> [!warning] 安全要求
> URL 中使用环境变量必须显式声明 `allowedEnvVars`

### Prompt Hook（LLM 评估）

让 LLM 判断是否允许操作：

```json
{
  "type": "prompt",
  "prompt": "评估任务是否完成。检查：1) 所有文件是否已创建？2) 是否有未解决的错误？",
  "timeout": 30
}
```

**LLM 响应格式**：

```json
{
  "decision": "approve",
  "reason": "所有任务已成功完成",
  "continue": false
}
```

### Agent Hook（多步验证）

启动独立 Agent 进行复杂验证：

```json
{
  "type": "agent",
  "prompt": "验证代码变更是否符合架构指南。检查相关设计文档并进行比较。",
  "timeout": 120
}
```

> [!tip] 与 Prompt Hook 的区别
> Agent Hook 可以使用工具（Read、Grep、Bash 等）进行多步推理，Prompt Hook 只能单次评估。

### MCP Tool Hook

调用 MCP 服务器工具：

```json
{
  "type": "mcp_tool",
  "mcp_server": "memory",
  "mcp_tool": "store-memory",
  "timeout": 30
}
```

> MCP Tool Hook 可在 PreToolUse 中无缝集成外部服务。

---

## Hook 事件完整列表

Claude Code 支持 **24+ 个 Hook 事件**（v2.1.83+ 新增文件系统事件）：

### 核心事件

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **SessionStart** | 会话开始/恢复 | ❌ | 环境初始化 |
| **SessionEnd** | 会话结束 | ❌ | 清理、日志 |
| **InstructionsLoaded** | 规则文件加载后 | ❌ | 修改指令 |

### 用户交互

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **UserPromptSubmit** | 用户提交提示词 | ✅ | 验证提示词 |
| **Notification** | 发送通知时 | ❌ | 自定义处理 |

### 工具执行

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **PreToolUse** | 工具执行前 | ✅ | 验证、修改输入 |
| **PostToolUse** | 工具执行成功后 | ❌ | 添加上下文 |
| **PostToolUseFailure** | 工具执行失败 | ❌ | 错误处理 |
| **PermissionRequest** | 显示权限对话框 | ✅ | 自动批准/拒绝 |

### Subagent

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **SubagentStart** | Subagent 启动时 | ❌ | 初始化 |
| **SubagentStop** | Subagent 完成时 | ✅ | 验证结果 |

### 任务与工作流

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **Stop** | Claude 完成响应 | ✅ | 任务完成检查 |
| **StopFailure** | API 错误结束 | ❌ | 错误恢复 |
| **TaskCompleted** | 任务标记完成 | ✅ | 任务后操作 |
| **TaskCreated** | 创建任务 | ❌ | 任务跟踪 |
| **TeammateIdle** | 团队成员空闲 | ✅ | 团队协调 |

### 配置与环境

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **ConfigChange** | 配置文件变更 | ✅ | 响应更新 |
| **CwdChanged** | 工作目录变更 | ❌ | 目录初始化 |
| **FileChanged** | 监视文件变更 | ❌ | 文件监控 |

### 上下文压缩

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **PreCompact** | 压缩前 | ❌ | 压缩前操作 |
| **PostCompact** | 压缩后 | ❌ | 压缩后操作 |

### Git Worktree

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **WorktreeCreate** | 创建 Worktree | ✅ | 初始化 |
| **WorktreeRemove** | 移除 Worktree | ❌ | 清理 |

### MCP 交互

| 事件 | 触发时机 | 可阻止 | 用途 |
|------|----------|--------|------|
| **Elicitation** | MCP 请求用户输入 | ✅ | 输入验证 |
| **ElicitationResult** | 用户响应 | ✅ | 响应处理 |

---

## 关键事件详解

### PreToolUse（最常用）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/validate.py" }]
      }
    ]
  }
}
```

**输出控制**：
- `permissionDecision`: `"allow"` / `"deny"` / `"ask"`
- `updatedInput`: 修改后的工具输入参数

### PostToolUse

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": ".claude/hooks/security-scan.py" }]
      }
    ]
  }
}
```

### Stop / SubagentStop（智能任务检查）

> **注意**：这两个事件会收到 `last_assistant_message` 字段。

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "评估是否完成所有任务。如果未完成，说明缺少什么。",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### SessionStart（环境变量持久化）

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

---

## 输入输出格式

### Hook 接收的 JSON（stdin）

```json
{
  "session_id": "sess_abc123",
  "cwd": "/Users/sarah/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" },
  "transcript_path": "/path/to/transcript.jsonl",
  "permission_mode": "ask"
}
```

### 退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| `0` | 成功 | 继续执行 |
| `2` | 阻止 | 阻止操作，显示错误 |
| 其他 | 失败 | 显示警告，继续执行 |

### 修改工具输入（PreToolUse）

```bash
#!/bin/bash
INPUT=$(cat)
MODIFIED=$(echo "$INPUT" | jq '.tool_input.command |= "safe-command"')
echo "$MODIFIED"
exit 0
```

---

## 组件级 Hooks

> [!tip] 新功能
> Hooks 可以直接附加到 Skills、Agents、Commands 的 frontmatter 中。

```yaml
---
name: secure-operations
description: 执行带有安全检查的操作
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true
---
```

**支持的事件**：`PreToolUse`、`PostToolUse`、`Stop`

> [!note] 自动转换
> Subagent frontmatter 中的 `Stop` hook 会自动转换为 `SubagentStop`。

---

## 实战示例

### 1. 桌面通知

```json
{
  "hooks": {
    "TaskCompleted": [
      { "hooks": [{ "type": "command", "command": "notify-send 'Claude' '✅ 完成！'" }] }
    ]
  }
}
```

### 2. 自动格式化

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true" }]
      }
    ]
  }
}
```

### 3. 阻止危险命令

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qiE 'rm\\s+-rf|sudo' && echo '❌ 危险命令已阻止' && exit 2 || exit 0"
        }]
      }
    ]
  }
}
```

### 4. 保护敏感文件

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_FILE_PATH\" | grep -qiE '\\.env|credentials|secrets' && echo '❌ 禁止编辑敏感文件' && exit 2 || exit 0"
        }]
      }
    ]
  }
}
```

### 5. 自动批准权限

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Read|Glob|Grep",
        "hooks": [{ "type": "command", "command": "echo '{\"decision\": \"approve\"}' && exit 0" }]
      }
    ]
  }
}
```

### 6. 上下文压缩提醒

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [{ "type": "command", "command": "echo '⚠️ 这是压缩后的会话，部分上下文可能丢失'" }]
      }
    ]
  }
}
```

### 7. 后台运行测试

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npm run lint && npm test", "background": true }]
      }
    ]
  }
}
```

### 8. 远程 Webhook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [{
          "type": "http",
          "url": "https://api.example.com/webhook",
          "headers": { "Authorization": "Bearer $TOKEN" },
          "allowedEnvVars": ["TOKEN"],
          "timeout": 5000
        }]
      }
    ]
  }
}
```

### 9. LLM 智能判断

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "prompt",
          "prompt": "检查命令是否安全。包含 rm/sudo/curl/wget 则返回 {\"decision\": \"deny\"}，否则返回 {\"decision\": \"approve\"}。命令：$CLAUDE_TOOL_INPUT"
        }]
      }
    ]
  }
}
```

---

## 调试与排错

### 查看配置

```bash
/hooks              # 查看已配置的 Hook
claude --debug      # 启动调试模式
```

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Hook 没有执行 | 配置位置错误 | 检查 `.claude/settings.json` |
| 执行失败 | 命令路径问题 | 使用 `$CLAUDE_PROJECT_DIR` 绝对路径 |
| 意外阻止 | Matcher 过宽 | 精确调整 matcher 模式 |
| Hook 超时 | 执行时间过长 | 增加 timeout 或使用 background |

### 测试脚本

```bash
#!/bin/bash
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' | python3 .claude/hooks/validate.py
echo $?  # 0=通过, 2=阻止
```

---

## 最佳实践

### 渐进式配置

```
第1步：桌面通知（验证 Hook 工作）
第2步：自动格式化（提升效率）
第3步：安全拦截（保护系统）
第4步：LLM 评估（智能决策）
```

### 精准匹配

```json
// ❌ 太宽泛
"matcher": ".*"

// ✅ 精准定位
"matcher": "Bash(rm|sudo)"
```

### 清晰反馈

```json
{
  "type": "command",
  "command": "echo '❌ 阻止原因：该命令会删除重要文件' && exit 2"
}
```

---

## 安全注意事项

> [!warning] 免责声明
> **使用风险自负**：Hooks 执行任意 Shell 命令，您需要自行负责配置的命令、文件权限和潜在的数据丢失。

### 最佳实践对照

| ✅ 应该做 | ❌ 不应该做 |
|-----------|-------------|
| 验证和清理所有输入 | 盲目信任输入数据 |
| 引用变量：`"$VAR"` | 使用未引用：`$VAR` |
| 使用绝对路径 | 硬编码路径 |
| 跳过敏感文件 | 处理所有文件 |
| 先在隔离环境测试 | 部署未测试的 Hook |
| HTTP Hook 使用 `allowedEnvVars` | 暴露所有环境变量 |

### 工作区信任

`statusLine` 和 `fileSuggestion` 输出需要**工作区信任接受**后才生效。

### 托管设置

组织级 `disableAllHooks` 设置可以**强制禁用 Hook**，个人用户无法覆盖。

---

## 环境变量参考

| 变量 | 可用性 | 描述 |
|------|--------|------|
| `CLAUDE_PROJECT_DIR` | 所有 Hook | 项目根目录绝对路径 |
| `CLAUDE_SESSION_ID` | 所有 Hook | 当前会话 ID |
| `CLAUDE_TOOL_NAME` | 工具事件 | 工具名称 |
| `CLAUDE_TOOL_INPUT` | 工具事件 | 工具输入（JSON） |
| `CLAUDE_FILE_PATH` | 文件操作 | 文件路径 |
| `CLAUDE_ENV_FILE` | SessionStart/CwdChanged/FileChanged | 持久化环境变量文件 |
| `CLAUDE_CODE_REMOTE` | 所有 Hook | 远程环境时为 `"true"` |
| `CLAUDE_PLUGIN_ROOT` | 插件 Hook | 插件目录路径 |
| `CLAUDE_PLUGIN_DATA` | 插件 Hook | 插件数据目录 |

---

## 常见问题

**Q: Hook 配置不生效？**

A: 检查：1) 配置文件位置 2) JSON 语法（用 `jq` 验证）3) 使用 `/hooks` 确认加载

**Q: 如何让 Hook 只在特定条件下触发？**

A: 使用 matcher + pathMatcher 组合：

```json
{ "matcher": "Edit", "pathMatcher": "src/.*\\.js$", "hooks": [...] }
```

**Q: Hook 可以链式调用吗？**

A: 可以，按顺序执行：

```json
{
  "hooks": [
    { "type": "command", "command": "prettier --write $CLAUDE_FILE_PATH" },
    { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATH" }
  ]
}
```

**Q: 如何临时禁用 Hook？**

A: 1) 从配置移除 2) 命令中添加条件判断 3) 使用 `exit 0` 直接通过

**Q: 如何一次性配置 Auto-Mode 权限？**

A: 运行一次性脚本种子 `~/.claude/settings.json`，添加约 67 条安全权限规则（等效于 Auto-Mode 基线），详见官方文档。

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[01-基础概念/Hook钩子]] - Hook 概念详解
- [[Claude Code 常用功能]] - /hooks 命令速查
- [[03-进阶应用/CLAUDE.md 使用指南]] - 项目级指令配置
- [[01-基础概念/Skills 是什么]] - 用户主动调用的技能系统

## 参考资料

- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - 完整技术参考
- [Automate workflows with hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide) - 使用指南
- [claude-howto/06-hooks - GitHub](https://github.com/luongnv89/claude-howto/tree/main/06-hooks) - 社区视觉化示例
- [anthropics/claude-code GitHub](https://github.com/anthropics/claude-code) - 官方仓库
