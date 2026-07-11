# Claude Code Hooks 规范

## 配置位置

| 文件 | 作用域 | 提交 git |
|------|--------|----------|
| `.claude/settings.json` | 项目共享 | ✅ |
| `.claude/settings.local.json` | 本地个人 | ❌ |
| `~/.claude/settings.json` | 全局 | ❌ |

## 事件速查

| 事件 | 时机 | 可阻止 |
|------|------|--------|
| `PreToolUse` | 工具执行前 | ✅ |
| `PostToolUse` | 工具执行后 | ❌ |
| `Stop` | Claude 停止响应 | ✅ 可阻止继续对话 |
| `UserPromptSubmit` | 用户提交 prompt | ✅ |
| `SessionStart` | 会话开始 | ❌ |
| `SubagentStart/Stop` | 子代理生命周期 | Stop ✅ |

完整事件列表见[官方文档](https://code.claude.com/docs/en/hooks)。

## Matcher

- `""` / `*` / 省略 → 匹配所有
- `Bash` / `Edit|Write` → 精确匹配（`|` 分隔）
- `^Notebook` / `mcp__memory__.*` → 正则匹配

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 成功，stdout 解析为 JSON |
| **2** | **阻止**，stderr 送回 Claude |
| 其他 | 非阻止错误，仅记录日志 |

> ⚠️ exit 1 不阻止，强制策略必须用 exit 2。

## JSON 输出

```bash
# 允许（exit 0 无输出）
exit 0

# 阻止工具执行
jq -n '{ hookSpecificOutput: { hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: "原因" } }'
exit 0

# 阻止（exit 2）
echo "错误原因" >&2
exit 2

# 重写工具输入
jq -n '{ hookSpecificOutput: { hookEventName: "PreToolUse", permissionDecision: "allow", updatedInput: { command: "safe-cmd" } } }'
exit 0
```

## 脚本模板

```bash
#!/bin/bash
set -euo pipefail
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

if [[ "$command" == *"危险模式"* ]]; then
  jq -n '{ hookSpecificOutput: { hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: "不允许" } }'
  exit 0
fi
exit 0
```

## 约定

1. **exit 2 做阻止**，不要用 exit 1
2. **fail-open** — 无法判断时 exit 0 放行
3. **jq 输出用 `jq -n`** — 避免转义问题
4. **一个脚本一件事** — 单一职责
5. **脚本放 `.claude/hooks/<event>/`** — 按事件分目录
6. **脚本必须 `chmod +x`**
