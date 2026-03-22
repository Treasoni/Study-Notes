---
tags: [claude, ai, 工具使用, hook, 自动化]
created: 2026-03-22
updated: 2026-03-22
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
| `.claude/settings.local.json` | 单个项目 | ❌ 不提交 | 高 |
| Plugin `hooks/hooks.json` | 插件启用时 | ✅ | 高 |
| Skill/Agent frontmatter | 组件活跃时 | ✅ | 最高 |

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
```

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

Hook 还可以通过 stdin 接收完整的 JSON 输入：

```json
{
  "event": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules"
  },
  "session_id": "abc123",
  "timestamp": "2026-03-22T10:00:00Z"
}
```

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
