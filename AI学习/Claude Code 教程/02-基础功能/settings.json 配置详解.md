---
title: settings.json 配置详解
tags: [claude, ai, 工具使用, claude-code, 配置]
created: 2026-07-27
updated: 2026-08-07
status: draft
source_project: claude-code-tutorial
---

# settings.json 配置详解

> [!info] 一句话
> **settings.json 是 Claude Code 的核心配置文件**，控制模型选择、权限范围、自动化钩子、环境变量等行为。支持全局、项目、本地三级配置层级。

---

## 配置文件层级

Claude Code 按优先级从低到高合并多个位置的 settings.json：

| 位置 | 作用范围 | 是否提交 Git | 优先级 |
|------|----------|-------------|--------|
| `~/.claude/settings.json` | 所有项目（全局） | ❌ 个人 | 最低 |
| `.claude/settings.json` | 单个项目 | ✅ 可共享 | 中 |
| `.claude/settings.local.json` | 单个项目本地覆盖 | ❌ 不提交 | 高 |
| `~/.claude/managed-settings.d/*.json` | 组织级托管 | ❌ IT 管理 | 最高 |

**合并规则**：低优先级字段与高优先级字段合并，同名键高优先级覆盖低优先级。

```bash
# 查看当前生效的完整配置
/checkup

# 在 Claude Code 中查看已配置的 Hook
/hooks
```

> 配置优先级详细说明见 [[Claude Code 会话管理#配置系统详解]]

---

## 完整配置字段

### 1. 模型配置

```json
{
  "model": "sonnet",
  "fallbackModel": ["haiku"]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `model` | string | 默认使用的模型（`sonnet`、`opus`、`haiku` 等） |
| `fallbackModel` | string[] | 主模型不可用时的备选模型链，按顺序尝试，最多 3 个 |

模型设置支持多种方式覆盖：settings.json → 环境变量 `ANTHROPIC_MODEL` → CLI 参数 `--model`，后者的优先级更高。

> 模型与推理参数详细说明见 [[Claude Code 模型与推理设置]]

### 2. 推理努力级别

```json
{
  "effortLevel": "high"
}
```

| 值 | 说明 |
|----|------|
| `low` | 快速响应，最少 token |
| `medium` | 标准思考（默认） |
| `high` | 深度推理 |
| `xhigh` | 极深推理（Opus 4.7/4.8+） |
| `max` | 最大推理（Opus 4.6+） |

会话中可用 `/effort` 命令动态切换，优先级高于配置文件。

### 3. 权限控制

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(npm *)",
      "Bash(git *)",
      "Bash(node *)",
      "Bash(cargo *)",
      "WebSearch",
      "WebFetch"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(chmod 777 *)"
    ]
  }
}
```

权限配置是 settings.json 中**最重要也最需要谨慎**的部分：

| 字段 | 类型 | 说明 |
|------|------|------|
| `allow` | string[] | 允许 Claude Code 自动执行的操作（无需每次确认） |
| `deny` | string[] | 禁止执行的操作（即使你手动确认也不行） |

**匹配规则**：

| 模式 | 示例 | 说明 |
|------|------|------|
| 精确工具名 | `"Read"` | 匹配 Read 工具的所有调用 |
| Bash 命令前缀 | `"Bash(git *)"` | 匹配所有 git 开头的 bash 命令 |
| Bash 命令精确 | `"Bash(npm install)"` | 只匹配 npm install |
| 通配符 | `"Bash(*)"` | 放行所有 bash 命令（不推荐） |

> [!warning] 权限配置建议
> - `allow` 列表应遵循**最小权限原则**，只放行你信任的、高频使用的操作
> - `Bash(*)` 放行所有 bash 命令有安全风险，建议按需放行具体命令
> - 不要放行 `rm -rf`、`sudo`、`chmod 777` 等危险命令
> - 不熟悉时保持默认，让 Claude Code 每次询问，更安全

### 4. 自动压缩

```json
{
  "autoCompactEnabled": true
}
```

控制上下文接近上限时是否自动压缩：

| 值 | 行为 |
|----|------|
| `true` | 开启自动压缩（默认） |
| `false` | 关闭自动压缩，需要手动 `/compact` |

> [!warning] 旧配置已变更
> 旧版 `autoCompactThreshold`（按百分比设置阈值）已废弃。压缩窗口改为**按 token 数**控制：用会话内 `/autocompact` 命令、CLI 参数 `--autocompact` 或环境变量 `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 调整（范围 100000–1000000 token）。

> 手动压缩用 `/compact` 命令，比自动压缩更可控。

### 5. 环境变量

```json
{
  "env": {
    "NODE_ENV": "development",
    "WORKSPACE_PATH": "./workspace",
    "API_URL": "http://localhost:3000",
    "DEBUG": "true"
  }
}
```

在 Claude Code 会话中预设环境变量，影响子进程和工具执行：

- 可以覆盖系统环境变量
- 项目级 settings.json 中的 `env` 适合存放非敏感的项目配置
- **不要**在 settings.json 中存放 API Key、Token 等敏感信息，应使用 `.env` 文件或系统的环境变量

### 6. Hooks（事件钩子）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(rm *)",
        "hooks": [
          { "type": "command", "command": "echo '阻止 rm 命令'", "timeout": 5000 }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "npx prettier --write {{tool_input.file_path}}" }
        ]
      }
    ]
  }
}
```

Hooks 是 settings.json 中最复杂的功能，支持多个事件点和多种钩子类型：

| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 工具执行前（可阻止操作） |
| `PostToolUse` | 工具执行后 |
| `Stop` | Claude 停止响应 |
| `UserPromptSubmit` | 用户提交消息时 |
| `SessionStart` | 会话开始时 |
| `SubagentStart` / `SubagentStop` | 子代理生命周期 |

| 钩子类型 | 说明 |
|----------|------|
| `command` | 执行 shell 命令 |
| `http` | 发送 HTTP 请求 |
| `prompt` | 向 Claude 发送额外提示 |
| `agent` | 调用子代理 |

> Hook 完整配置指南见 [[Claude Code Hooks 使用指南]]

### 7. MCP 服务器配置（CLI 管理）

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

> [!tip] 管理方式
> MCP 服务器推荐使用 `claude mcp add` 命令管理，而非手动编辑 settings.json：
> ```bash
> claude mcp add my-server -- npx -y @myserver/mcp
> ```
>
> 手动编辑适合需要自定义 `env` 映射或精确控制参数时。

### 8. 其他配置

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "verbose": false,
  "plugins": ["@anthropic/claude-code-plugin-pull-request"]
}
```

> [!note] 已移除的字段
> `maxTokens` 已不在当前 schema 中；自定义系统提示词应通过 CLAUDE.md 文件管理，settings.json 不再支持 `systemPrompt`。

| 字段 | 类型 | 说明 |
|------|------|------|
| `$schema` | string | JSON Schema 地址，编辑器可自动补全和校验 |
| `plugins` | string[] | 启用的插件列表 |
| `verbose` | boolean | 是否输出详细日志 |

---

## 场景配置示例

### 个人日常开发

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Grep", "Glob",
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(node *)",
      "Bash(ls *)", "Bash(cat *)", "Bash(mkdir *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

### 团队项目共享

```json
{
  "model": "opusplan",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git push *)",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/check-branch.sh" }
        ]
      }
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "PROJECT_STANDARD": "typescript-strict"
  }
}
```

### 最小安全配置（新手推荐）

```json
{
  "model": "sonnet"
}
```

留空 allow 列表，Claude Code 会在执行每个操作前询问确认，适合初学者或安全敏感场景。

---

## 常见问题

### Q: 配置不生效怎么办？

**排查步骤**：

1. **检查位置**：确认文件在正确的位置（`.claude/settings.json` 而非 `.claude/settings.json.txt`）
2. **检查 JSON 格式**：JSON 不允许注释，末尾不能有多余逗号
3. **检查优先级**：是否有 `.claude/settings.local.json` 覆盖了你的配置
4. **使用 `/checkup`**：运行 `/checkup` 命令进行系统诊断
5. **重启会话**：修改 settings.json 后需要重启 Claude Code 会话

### Q: .claude/settings.json 和 .claude/settings.local.json 有什么区别？

| | `settings.json` | `settings.local.json` |
|--|----------------|----------------------|
| 用途 | 团队共享配置 | 个人本地覆盖 |
| Git | ✅ 提交 | ❌ `.gitignore` 已排除 |
| 优先级 | 低 | 高 |
| 典型内容 | 模型、Hooks、权限白名单 | 个人 API Key、本地路径、调试开关 |

### Q: 修改后需要重启会话吗？

大部分配置需要，少部分不需要。安全做法：修改后重启 Claude Code 会话。

### Q: 全局和项目配置会冲突吗？

会合并。项目级配置覆盖全局配置的同名字段。例如全局设置 `"model": "haiku"`，项目设置 `"model": "sonnet"`，该项目实际使用 `sonnet`。

### Q: 如何在 settings.json 中使用环境变量引用？

`mcpServers` 的 `env` 字段支持 `${VARIABLE_NAME}` 语法引用系统环境变量。其他字段不支持变量引用，需要直接写值。

---

## 最佳实践

### Do's（推荐）

- 把**团队规范**放 `.claude/settings.json`，提交到 Git 共享
- 把**个人偏好**放 `.claude/settings.local.json`，不提交
- 用 `allow` 列表放行高频安全操作，减少确认干扰
- Hooks 配置先在本地测试，再推广到团队
- 使用 `$schema` 字段获得编辑器的自动补全和校验

### Don'ts（避免）

- ❌ 不要在 settings.json 中存放 API Key、Token、密码
- ❌ 不要放行 `Bash(*)` 或过于宽泛的权限
- ❌ 不要提交 `.env` 或 `settings.local.json` 到 Git
- ❌ 不要创建冗余的配置项（多个地方设置同一个值）

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Claude Code 会话管理]] | 配置优先级、记忆文件、会话恢复 |
| [[Claude Code 模型与推理设置]] | 模型选择、Effort Level、Fallback |
| [[Claude Code Hooks 使用指南]] | Hook 事件、类型、Matcher 语法 |
| [[Claude Code CLI 完整参考]] | CLI 启动参数、环境变量 |
| [[Claude Code 插件系统使用指南]] | 插件安装与管理 |
| [[如何使用Claude code]] | 安装与基本使用 |

---

## 参考资料

- [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings)
- [JSON Schema for settings.json](https://json.schemastore.org/claude-code-settings.json)
- [Claude Code Overview](https://code.claude.com/docs/en/overview)

---

## 更新记录

- 2026-08-07：同步官方 schema 与文档。`autoCompactThreshold` 废弃 → `autoCompactEnabled` + `/autocompact`；`fallbackModels` → `fallbackModel`；移除 `maxTokens`、`systemPrompt`。
