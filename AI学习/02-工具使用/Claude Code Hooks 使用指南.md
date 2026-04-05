---
tags: [claude, ai, 工具使用, hook, 自动化]
created: 2026-03-22
updated: 2026-04-05
---

# Claude Code Hooks 使用指南

> [!info] 文档定位
> **本文档是 Hook 的详细使用指南**。概念理解请先阅读 [[01-基础概念/Hook钩子]]。

> [!info] 概述
> **一句话定义**：通过配置文件定义自动化规则，在 Claude Code 生命周期的特定时间点执行自定义逻辑。

## 配置详解

### 配置位置

Hook 可以在多个层级配置，按优先级从低到高：

| 位置 | 作用范围 | 可共享 | 优先级 |
|------|----------|--------|--------|
| `~/.claude/settings.json` | 所有项目 | ❌ 个人 | 最低 |
| `.claude/settings.json` | 单个项目 | ✅ 可提交 Git | 中 |
| `.claude/settings.local.json` | 单个项目 | ❌ 不提交 | 高（覆盖项目和用户设置）|
| Managed settings | 组织级 | ✅ IT 管理 | 高 |
| Plugin `hooks/hooks.json` | 插件启用时 | ✅ 可提交 Git | 高 |
| Skill/Agent frontmatter | 组件活跃时 | ✅ | 最高 |

> [!tip] 配置层级说明
> - **项目级配置**（`.claude/settings.json`）优先级高于用户级配置
> - **本地配置**（`.claude/settings.local.json`）会覆盖项目级和用户级设置
> - 企业管理策略可由 IT 部门统一配置

### CLI 配置方法详解

#### 方法一：直接编辑 settings.json（推荐）

最简单直接的方式是在项目根目录创建或编辑配置文件：

```bash
# 创建项目级配置（可提交到 Git，团队共享）
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
EOF
```

```bash
# 创建本地配置（个人设置，不提交 Git）
cat > .claude/settings.local.json << 'EOF'
{
  "env": {
    "MY_API_KEY": "your-secret-key"
  }
}
EOF
```

```bash
# 创建全局用户配置（所有项目共享）
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' '✅ 任务完成！'"
          }
        ]
      }
    ]
  }
}
EOF
```

#### 方法二：使用 `/hooks` 命令查看

在 Claude Code 会话中使用斜杠命令查看当前配置：

```
/hooks
```

输出示例：
```
Configured Hooks:
├── PreToolUse
│   └── Bash → 阻止危险命令
├── PostToolUse
│   └── Edit|Write → 自动格式化
└── TaskCompleted
    └── * → 桌面通知
```

> [!tip] `/hooks` 命令用途
> - 快速查看当前已配置的 Hook
> - 验证配置是否正确加载
> - 检查 Hook 的匹配规则

#### 方法三：使用 `/config` 命令（交互式配置）

在 Claude Code 会话中使用交互式配置界面：

```
/config
```

这会打开设置界面，可以：
- 添加/编辑权限规则
- 配置 MCP 服务器
- 管理其他设置项

#### 方法四：使用 `--debug` 参数启动调试模式

启动 Claude Code 时添加调试参数查看详细信息：

```bash
claude --debug
```

输出示例：
```
debug mode enabled. Check JSON validity and verbose logging
Loading settings from: /Users/you/.claude/settings.json
Loading settings from: /Users/you/project/.claude/settings.json
Hooks loaded: 3 matchers configured
...
```

> [!tip] 调试模式用途
> - 查看配置文件加载顺序
> - 验证 JSON 语法是否正确
> - 排查 Hook 不生效的原因

#### 方法五：使用 `disableAllHooks` 临时禁用所有 Hook

在 settings.json 中添加此字段可临时禁用所有 Hook：

```json
{
  "disableAllHooks": true
}
```

适用于：
- 排查 Hook 是否导致问题
- 临时绕过所有自动化规则
- 测试原始行为

#### 方法六：配置环境变量（`env` 字段）

通过 `env` 字段配置环境变量，在 Hook 中通过 `$VAR_NAME` 访问：

```json
{
  "env": {
    "MY_PROJECT": "my-project",
    "NOTIFICATION_SOUND": "default"
  },
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' \"✅ $MY_PROJECT 任务完成！\""
          }
        ]
      }
    ]
  }
}
```

> [!warning] 敏感信息处理
> - API 密钥等敏感信息应放在 `settings.local.json` 中
> - 确保 `.gitignore` 包含 `.claude/settings.local.json`

#### 方法七：HTTP Hook 高级配置

HTTP Hook 支持环境变量白名单和 URL 白名单：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "http",
            "url": "https://api.example.com/webhook",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN",
              "Content-Type": "application/json"
            },
            "timeout": 5000,
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `allowedEnvVars` | 允许在 headers 中使用的环境变量白名单 |
| `timeout` | 请求超时时间（毫秒） |

> [!note] 企业策略
> URL 白名单（`allowedHttpHookUrls`）由企业管理员在组织级策略中设置

#### 方法八：完整的 settings.json 示例

包含 `$schema` 验证的完整配置示例：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qiE 'rm\\s+-rf|sudo' && echo '❌ 危险命令已被阻止' && exit 2 || exit 0"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  },
  "permissions": {
    "allow": [
      "Read(**)",
      "Bash(npm run*)",
      "Bash(git *)"
    ],
    "deny": [
      "Read(.env)",
      "Bash(rm -rf /*)"
    ]
  },
  "env": {
    "PROJECT_NAME": "my-awesome-project"
  }
}
```

> [!tip] 添加 `$schema` 的好处
> - 在 VS Code、Cursor 等 IDE 中支持 JSON Schema 验证
> - 自动补全配置字段
> - 实时检测语法错误

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

Matcher 用于筛选哪些工具/事件会触发 Hook：

| 语法 | 示例 | 匹配规则 |
|------|------|----------|
| 精确匹配 | `"Bash"` | 只匹配 Bash 工具 |
| 多个匹配 | `"Bash\|Edit"` | 匹配 Bash 或 Edit（用 `\|` 分隔） |
| 正则表达式 | `"Bash(rm\|sudo)"` | 使用正则表达式 |
| 通配符 | `"*"` 或 `""` | 匹配所有工具 |
| MCP 工具 | `"mcp__memory__.*"` | 匹配特定 MCP 服务器的工具 |

**常用 Matcher 示例**：

```json
// 只匹配 Bash 工具
"matcher": "Bash"

// 匹配 Edit 和 Write 工具
"matcher": "Edit|Write"

// 匹配所有包含 "rm" 的 Bash 命令
"matcher": "Bash(rm)"

// 匹配所有文件编辑操作
"matcher": "Edit|Write|NotebookEdit"

// 匹配特定文件路径
"matcher": "Edit",
"pathMatcher": "\\.env$|credentials"

// 匹配 MCP 工具
"matcher": "mcp__memory__.*"
```

## Hook 事件完整列表

Claude Code 支持 **25 个 Hook 事件**，按功能分类如下：

### 核心事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **SessionStart** | 会话开始/恢复/压缩 | `startup`/`resume`/`clear`/`compact` | ❌ | 环境初始化 |
| **SessionEnd** | 会话结束 | `clear`/`logout`/`prompt_input_exit`/`other` | ❌ | 清理、日志记录 |
| **InstructionsLoaded** | CLAUDE.md 或规则文件加载后 | (无) | ❌ | 修改/过滤指令 |

### 用户交互事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **UserPromptSubmit** | 用户提交提示词 | (无) | ✅ | 验证提示词 |
| **Notification** | 发送通知时 | `permission_prompt`/`idle_prompt`/`auth_success`/`elicitation_dialog` | ❌ | 自定义通知处理 |

### 工具执行事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **PreToolUse** | 工具执行前 | 工具名称 | ✅ | 验证、修改输入 |
| **PostToolUse** | 工具执行成功后 | 工具名称 | ❌ | 添加上下文、反馈 |
| **PostToolUseFailure** | 工具执行失败 | 工具名称 | ❌ | 错误处理、日志 |
| **PermissionRequest** | 显示权限对话框 | 工具名称 | ✅ | 自动批准/拒绝 |

### Subagent 事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **SubagentStart** | Subagent 启动时 | Agent 类型名称 | ❌ | Subagent 初始化 |
| **SubagentStop** | Subagent 完成时 | Agent 类型名称 | ✅ | Subagent 验证 |

### 任务与工作流事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **Stop** | Claude 完成响应 | (无) | ✅ | 任务完成检查 |
| **StopFailure** | API 错误结束回合 | (无) | ❌ | 错误恢复、日志 |
| **TaskCompleted** | 任务标记完成 | (无) | ✅ | 任务后操作 |
| **TaskCreated** | 通过 TaskCreate 创建任务 | (无) | ❌ | 任务跟踪、日志 |
| **TeammateIdle** | Agent 团队成员空闲 | (无) | ✅ | 团队协调 |

### 配置与环境事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **ConfigChange** | 配置文件变更 | (无) | ✅（策略除外） | 响应配置更新 |
| **CwdChanged** | 工作目录变更 | (无) | ❌ | 目录特定初始化 |
| **FileChanged** | 监视文件变更 | (无) | ❌ | 文件监控、重建 |

### 上下文压缩事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **PreCompact** | 上下文压缩前 | `manual`/`auto` | ❌ | 压缩前操作 |
| **PostCompact** | 压缩完成后 | (无) | ❌ | 压缩后操作 |

### Git Worktree 事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **WorktreeCreate** | 创建 Worktree | (无) | ✅（返回路径） | Worktree 初始化 |
| **WorktreeRemove** | 移除 Worktree | (无) | ❌ | Worktree 清理 |

### MCP 交互事件

| 事件 | 触发时机 | Matcher 输入 | 可阻止 | 常见用途 |
|------|----------|--------------|--------|----------|
| **Elicitation** | MCP 服务器请求用户输入 | (无) | ✅ | 输入验证 |
| **ElicitationResult** | 用户响应 Elicitation | (无) | ✅ | 响应处理 |

### 关键事件详解

#### PreToolUse（工具执行前）

最常用的 Hook 事件，用于验证和修改工具输入：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
```

**输出控制**：
- `permissionDecision`: `"allow"`, `"deny"`, 或 `"ask"`
- `permissionDecisionReason`: 决策原因说明
- `updatedInput`: 修改后的工具输入参数

#### PostToolUse（工具执行后）

工具成功执行后触发，用于验证、日志或提供上下文：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py"
          }
        ]
      }
    ]
  }
}
```

#### Stop 和 SubagentStop（智能任务完成检查）

支持 **Prompt Hook** 进行 LLM 评估：

> **注意**：`Stop` 和 `SubagentStop` 事件会收到 `last_assistant_message` 字段，包含 Claude 或 subagent 停止前的最后一条消息。

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "评估 Claude 是否完成了所有请求的任务。检查：1) 所有文件是否已创建/修改？2) 是否有未解决的错误？如果未完成，说明缺少什么。",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

#### SessionStart（环境变量持久化）

使用 `CLAUDE_ENV_FILE` 持久化环境变量（`CwdChanged` 和 `FileChanged` 也支持）：

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

#### SessionEnd（会话结束清理）

执行清理或最终日志记录，**无法阻止终止**：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-cleanup.sh\""
          }
        ]
      }
    ]
  }
}
```

**reason 字段值**：
- `clear` - 用户清除了会话
- `logout` - 用户登出
- `prompt_input_exit` - 用户通过提示输入退出
- `other` - 其他原因

### 输入输出格式

#### 输入环境变量

Hook 执行时可以访问以下环境变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `CLAUDE_SESSION_ID` | 当前会话 ID | `abc123` |
| `CLAUDE_TOOL_NAME` | 工具名称 | `Bash`, `Edit` |
| `CLAUDE_TOOL_INPUT` | 工具输入（JSON） | `{"command": "ls"}` |
| `CLAUDE_FILE_PATH` | 文件路径（文件操作） | `/src/index.js` |

#### 输入 JSON（stdin）

Hook 通过 stdin 接收完整的 JSON 输入，包含以下关键字段：

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `session_id` | 当前会话 ID | `"abc123"` |
| `cwd` | 当前工作目录 | `"/Users/sarah/myproject"` |
| `hook_event_name` | 触发此事件的名称 | `"PreToolUse"` |
| `tool_name` | 工具名称 | `"Bash"` |
| `tool_input` | 工具输入参数 | `{"command": "npm test"}` |
| `timestamp` | 事件时间戳 | `"2026-03-22T10:00:00Z"` |
| `transcript_path` | 会话记录文件路径 | `"/path/to/transcript.jsonl"` |
| `stop_hook_active` | Stop hook 是否激活 | `true`（防止无限循环） |
| `permission_mode` | 当前权限模式 | `"ask"` / `"auto"` |

**完整示例**：

```json
{
  "session_id": "sess_abc123xyz",
  "cwd": "/Users/sarah/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules"
  },
  "timestamp": "2026-03-22T10:00:00Z",
  "transcript_path": "/Users/sarah/.claude/transcripts/sess_abc123xyz.jsonl",
  "stop_hook_active": false,
  "permission_mode": "ask"
}
```

> [!tip] 使用 jq 解析 JSON
> ```bash
> # 读取 stdin 并提取字段
> INPUT=$(cat)
> TOOL=$(echo "$INPUT" | jq -r '.tool_name')
> CMD=$(echo "$INPUT" | jq -r '.tool_input.command')
> ```

#### 输出与退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| `0` | 成功 | 操作继续执行 |
| `2` | 阻止 | 阻止操作，显示错误信息 |
| 其他 | 失败 | 显示警告，操作继续 |

**返回 JSON 修改输入**（仅 PreToolUse）：

```bash
#!/bin/bash
# 读取 stdin 中的 JSON
INPUT=$(cat)

# 修改命令
MODIFIED=$(echo "$INPUT" | jq '.tool_input.command |= "safe-command"')

# 输出修改后的 JSON（退出码 0 表示应用修改）
echo "$MODIFIED"
exit 0
```

## 组件级 Hooks（Component-Scoped Hooks）

> [!tip] 新功能
> Hooks 可以直接附加到特定组件（Skills、Agents、Commands）的 frontmatter 中。

### 在组件 Frontmatter 中定义 Hooks

在 `SKILL.md`、`agent.md` 或 `command.md` 文件中：

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
          once: true  # 每个会话只运行一次
---
```

**支持的事件**：`PreToolUse`、`PostToolUse`、`Stop`

### Subagent 中的 Stop Hook 自动转换

当在 Subagent 的 frontmatter 中定义 `Stop` hook 时，它会自动转换为该 Subagent 专属的 `SubagentStop` hook：

```yaml
---
name: code-review-agent
description: 自动代码审查 Subagent
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "验证代码审查是否全面完整。"
  # 上述 Stop hook 自动转换为 SubagentStop，仅在此 subagent 完成时触发
---
```

**工作原理**：
- 组件级 Hook 只在该组件活跃时生效
- 相关代码集中在一起，便于维护
- 无需修改全局配置文件

## HTTP Hooks（远程 Webhooks）

> [!info] v2.1.63 新增
> HTTP Hooks 允许将 Hook 事件发送到远程服务器处理。

### 基本配置

```json
{
  "hooks": {
    "PostToolUse": [{
      "type": "http",
      "url": "https://my-webhook.example.com/hook",
      "matcher": "Write"
    }]
  }
}
```

### 环境变量插值

> [!warning] 安全要求
> 在 URL 中使用环境变量需要显式声明 `allowedEnvVars` 列表：

```json
{
  "hooks": {
    "PostToolUse": [{
      "type": "http",
      "url": "https://${API_HOST}/hooks/notify",
      "allowedEnvVars": ["API_HOST"],
      "matcher": "Write"
    }]
  }
}
```

**关键特性**：
- `"type": "http"` — 标识为 HTTP hook
- `"url"` — Webhook 端点 URL
- 启用沙箱时通过沙箱路由
- 需要显式声明环境变量以防止敏感信息泄露

## Prompt Hooks（LLM 评估）

用于 `Stop` 和 `SubagentStop` 事件的智能任务完成检查。

### 配置示例

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "评估 Claude 是否完成了所有请求的任务。检查：1) 所有文件是否已创建/修改？2) 是否有未解决的错误？",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### LLM 响应格式

```json
{
  "decision": "approve",
  "reason": "所有任务已成功完成",
  "continue": false,
  "stopReason": "任务完成"
}
```

## Agent Hooks（Subagent 验证）

> [!tip] 与 Prompt Hook 的区别
> Agent Hooks 可以使用工具进行多步推理，而 Prompt Hooks 只能进行单次 LLM 评估。

### 配置示例

```json
{
  "type": "agent",
  "prompt": "验证代码变更是否符合我们的架构指南。检查相关设计文档并进行比较。",
  "timeout": 120
}
```

**关键特性**：
- `"type": "agent"` — 标识为 Agent hook
- `"prompt"` — Subagent 的任务描述
- Agent 可以使用工具（Read、Grep、Bash 等）进行评估
- 返回与 Prompt Hooks 类似的结构化决策

## 实战示例

### 1. 桌面通知

在任务完成时发送桌面通知：

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' '✅ 任务已完成！'"
          }
        ]
      }
    ]
  }
}
```

### 2. 自动格式化

在编辑代码后自动运行格式化工具：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 3. 阻止危险命令

阻止包含 `rm -rf` 或 `sudo` 的 Bash 命令：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qiE 'rm\\s+-rf|sudo' && echo '❌ 危险命令已被阻止' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

### 4. 阻止敏感文件编辑

保护 `.env`、`credentials` 等敏感文件：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_FILE_PATH\" | grep -qiE '\\.env|credentials|secrets|private_key' && echo '❌ 禁止编辑敏感文件' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

### 5. 上下文压缩后注入提醒

在会话恢复或压缩后注入提醒信息：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '注意：这是压缩后的会话，部分上下文可能丢失'"
          }
        ]
      }
    ]
  }
}
```

### 6. 自动批准特定权限

自动批准特定工具的权限请求：

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Read|Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"decision\": \"approve\"}' && exit 0"
          }
        ]
      }
    ]
  }
}
```

## 高级用法

### Prompt Hook（LLM 评估决策）

使用 LLM 判断是否允许操作：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "检查以下命令是否安全。如果命令包含 rm、sudo、chmod、chown 或向外部发送数据（curl、wget），返回 {\"decision\": \"deny\", \"reason\": \"原因\"}；否则返回 {\"decision\": \"approve\"}。命令：$CLAUDE_TOOL_INPUT"
          }
        ]
      }
    ]
  }
}
```

### Agent Hook（多轮验证）

启动独立 Agent 进行复杂验证：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "agent",
            "prompt": "检查要写入的文件内容是否包含敏感信息（API密钥、密码等）。如果包含，阻止操作并说明原因。"
          }
        ]
      }
    ]
  }
}
```

### HTTP Hook（远程处理）

将事件发送到远程服务器：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "http",
            "url": "https://api.example.com/claude-webhook",
            "headers": {
              "Authorization": "Bearer your-token",
              "Content-Type": "application/json"
            },
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### 异步 Hook（后台运行）

对于耗时操作，使用 `background: true` 避免阻塞：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint && npm test",
            "background": true
          }
        ]
      }
    ]
  }
}
```

### 超时设置

为长时间运行的操作设置超时：

```json
{
  "type": "command",
  "command": "npm run build",
  "timeout": 120000
}
```

### 上下文使用追踪器（Hook 配对）

> [!tip] 高级示例
> 使用 `UserPromptSubmit`（消息前）和 `Stop`（响应后）Hook 配对追踪 Token 消耗。

**Python 脚本** (`.claude/hooks/context-tracker.py`)：

```python
#!/usr/bin/env python3
"""
上下文使用追踪器 - 追踪每次请求的 Token 消耗

使用 UserPromptSubmit 作为"消息前" Hook，Stop 作为"响应后" Hook
来计算每次请求的 Token 使用增量。

Token 计数方法：
1. 字符估算（默认）：约 4 字符 = 1 token，无依赖
2. tiktoken（可选）：更准确（~90-95%），需要 pip install tiktoken
"""
import json
import os
import sys
import tempfile

# 配置
CONTEXT_LIMIT = 128000  # Claude 上下文窗口（根据模型调整）
USE_TIKTOKEN = False    # 设置 True 以获得更好准确性

def get_state_file(session_id: str) -> str:
    """获取存储消息前 Token 计数的临时文件路径"""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")

def count_tokens(text: str) -> int:
    """计算文本中的 Token 数量"""
    if USE_TIKTOKEN:
        try:
            import tiktoken
            enc = tiktoken.get_encoding("p50k_base")
            return len(enc.encode(text))
        except ImportError:
            pass  # 回退到估算

    # 基于字符的估算：英文约 4 字符 = 1 token
    return len(text) // 4

def read_transcript(transcript_path: str) -> str:
    """读取并合并 transcript 文件中的所有内容"""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)

def handle_user_prompt_submit(data: dict) -> None:
    """消息前 Hook：保存当前 Token 计数"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 保存到临时文件供后续比较
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)

def handle_stop(data: dict) -> None:
    """响应后 Hook：计算并报告 Token 增量"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 加载消息前计数
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 计算增量
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 报告使用情况
    method = "tiktoken" if USE_TIKTOKEN else "estimated"
    print(f"Context ({method}): ~{current_tokens:,} tokens ({percentage:.1f}% used, ~{remaining:,} remaining)", file=sys.stderr)
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)

def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**配置**：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ]
  }
}
```

**Token 计数方法比较**：

| 方法 | 准确度 | 依赖 | 速度 |
|------|--------|------|------|
| 字符估算 | ~80-90% | 无 | <1ms |
| tiktoken (p50k_base) | ~90-95% | `pip install tiktoken` | <10ms |

> [!note] 注意
> Anthropic 尚未发布官方离线 tokenizer。两种方法都是近似值。Transcript 包含用户提示、Claude 响应和工具输出，但不包括系统提示或内部上下文。

## 调试与排错

### /hooks 命令

在 Claude Code 会话中使用 `/hooks` 命令查看当前配置的所有 Hook：

```bash
/hooks
```

输出示例：
```
Configured Hooks:
├── PreToolUse
│   └── Bash → 阻止危险命令
├── PostToolUse
│   └── Edit|Write → 自动格式化
└── TaskCompleted
    └── * → 桌面通知
```

### 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Hook 没有执行 | 配置文件位置错误 | 检查是否在 `.claude/settings.json` |
| Hook 执行失败 | 命令路径问题 | 使用绝对路径或检查 PATH |
| 操作被意外阻止 | Matcher 过于宽泛 | 调整 matcher 模式 |
| Hook 超时 | 命令执行时间过长 | 增加 timeout 或使用 background |

### Debug 模式

启用详细日志查看 Hook 执行情况：

```bash
CLAUDE_DEBUG=1 claude
```

### 测试 Hook

创建测试脚本验证 Hook 是否正常工作：

```bash
#!/bin/bash
# test-hook.sh
echo "Hook triggered!"
echo "Session: $CLAUDE_SESSION_ID"
echo "Tool: $CLAUDE_TOOL_NAME"
echo "Input: $CLAUDE_TOOL_INPUT"
```

然后在配置中引用：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/test-hook.sh"
          }
        ]
      }
    ]
  }
}
```

## 最佳实践

### 1. 渐进式配置

从简单开始，逐步添加更复杂的 Hook：

```
第1步：添加桌面通知（验证 Hook 工作）
第2步：添加自动格式化（提升效率）
第3步：添加安全拦截（保护系统）
第4步：添加 LLM 评估（智能决策）
```

### 2. 避免过度拦截

不要拦截所有操作，只拦截真正需要控制的：

```json
// ❌ 太严格
"matcher": ".*"

// ✅ 精准定位
"matcher": "Bash(rm|sudo)"
```

### 3. 使用后台执行

耗时操作使用 `background: true`：

```json
{
  "type": "command",
  "command": "npm test",
  "background": true
}
```

### 4. 提供清晰的反馈

阻止操作时给出明确原因：

```json
{
  "type": "command",
  "command": "echo '❌ 阻止原因：该命令会删除重要文件' && exit 2"
}
```

### 5. 分层配置

- 全局配置：个人偏好（如通知）
- 项目配置：团队规范（如格式化）
- 本地配置：个人敏感设置（如密钥）

## 常见问题

**Q: Hook 配置不生效怎么办？**

A: 检查以下几点：
1. 配置文件位置是否正确
2. JSON 语法是否有效（使用 `jq` 验证）
3. 使用 `/hooks` 命令确认配置已加载

**Q: 如何让 Hook 只在特定条件下触发？**

A: 使用 matcher 和 pathMatcher 组合：

```json
{
  "matcher": "Edit",
  "pathMatcher": "src/.*\\.js$",
  "hooks": [...]
}
```

**Q: Hook 可以链式调用吗？**

A: 可以。一个事件可以配置多个 Hook，它们会按顺序执行：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "prettier --write $CLAUDE_FILE_PATH"},
          {"type": "command", "command": "eslint --fix $CLAUDE_FILE_PATH"}
        ]
      }
    ]
  }
}
```

**Q: 如何临时禁用某个 Hook？**

A: 可以：
1. 从配置文件中移除或注释
2. 在命令中添加条件判断
3. 使用 `exit 0` 让 Hook 直接通过

---

## 环境变量完整列表

| 变量 | 可用性 | 描述 |
|------|--------|------|
| `CLAUDE_PROJECT_DIR` | 所有 Hook | 项目根目录的绝对路径 |
| `CLAUDE_ENV_FILE` | SessionStart, CwdChanged, FileChanged | 持久化环境变量的文件路径 |
| `CLAUDE_CODE_REMOTE` | 所有 Hook | 在远程环境运行时为 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 插件 Hook | 插件目录路径 |
| `${CLAUDE_PLUGIN_DATA}` | 插件 Hook | 插件数据目录路径 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd Hook | SessionEnd Hook 的超时时间（毫秒）|

### 使用示例

**持久化环境变量**（SessionStart/CwdChanged/FileChanged）：

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export MY_CUSTOM_VAR="value"' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**插件 Hook 中使用插件路径**：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

## 安全注意事项

> [!warning] 免责声明
> **使用风险自负**：Hooks 执行任意 Shell 命令。您需要自行负责：
> - 配置的命令
> - 文件访问/修改权限
> - 潜在的数据丢失或系统损坏
> - 在生产环境使用前在安全环境中测试

### 最佳实践对照表

| ✅ 应该做 | ❌ 不应该做 |
|-----------|-------------|
| 验证和清理所有输入 | 盲目信任输入数据 |
| 引用 Shell 变量：`"$VAR"` | 使用未引用：`$VAR` |
| 阻止路径遍历（`..`） | 允许任意路径 |
| 使用 `$CLAUDE_PROJECT_DIR` 绝对路径 | 硬编码路径 |
| 跳过敏感文件（`.env`, `.git/`, 密钥）| 处理所有文件 |
| 先在隔离环境测试 Hook | 部署未测试的 Hook |
| HTTP Hook 使用显式 `allowedEnvVars` | 暴露所有环境变量给 Webhook |

### 工作区信任

- `statusLine` 和 `fileSuggestion` Hook 输出命令现在需要**工作区信任接受**后才会生效

### HTTP Hook 安全

- HTTP Hook 需要显式的 `allowedEnvVars` 列表才能在 URL 中使用环境变量插值
- 这可以防止敏感环境变量意外泄露到远程端点

### 托管设置层级

- `disableAllHooks` 设置现在遵循托管设置层级
- 这意味着组织级设置可以**强制禁用 Hook**，个人用户无法覆盖

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[01-基础概念/Hook钩子]] - Hook 概念详解
- [[02-工具使用/Claude Code 常用功能]] - /hooks 命令速查
- [[03-进阶应用/CLAUDE.md 使用指南]] - 项目级指令配置
- [[01-基础概念/Skills 是什么]] - 用户主动调用的技能系统

## 参考资料

- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - 完整技术参考
- [Automate workflows with hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide) - 使用指南
- [How to configure hooks - Claude Blog](https://claude.com/blog/how-to-configure-hooks) - 官方配置详解
- [Claude Code settings.json: Complete config guide (2026)](https://www.eesel.ai/blog/settings-json-claude-code) - 配置层级详解
- [anthropics/claude-code GitHub](https://github.com/anthropics/claude-code) - 官方仓库与示例
- [claude-howto/06-hooks - GitHub](https://github.com/luongnv89/claude-howto/tree/main/06-hooks) - 社区维护的视觉化示例指南
