---
title: settings.json 配置详解
tags: [claude, ai, 工具使用, claude-code, 配置]
created: 2026-07-27
updated: 2026-08-10
status: updated
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
  "defaultMode": "manual",
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

**权限模式（defaultMode）**

权限模式决定 Claude Code 如何审批操作。v2.1.200 起原「Default」模式改名为「Manual」，settings 中对应 `"defaultMode": "manual"`（CLI 等价 `--permission-mode manual`）。

| 值 | 说明 |
|----|------|
| `manual` | 默认模式（原名 Default），每个需要权限的操作逐次询问、手动确认 |
| `acceptEdits` | 自动接受文件编辑 |
| `plan` | 只读规划模式，不实际改动 |
| `bypassPermissions` | 跳过权限检查（最危险，不推荐日常使用） |

> [!tip] 大白话
> `defaultMode` 就是"Claude Code 该多听话"的档位。`manual` 相当于"每件事都先问我一声"，最安全；档位越往上，Claude 越自主，风险也越高。

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
> - 不熟悉时保持默认（`defaultMode: "manual"`），让 Claude Code 每次询问，更安全

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

### 9. 沙盒与安全配置

```json
{
  "sandbox": {
    "filesystem": {
      "disabled": true
    },
    "network": {
      "strictAllowlist": true
    }
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `sandbox.filesystem.disabled` | boolean | 跳过文件系统隔离，但保留网络出口控制（v2.1.216+） |
| `sandbox.network.strictAllowlist` | boolean | 沙盒网络启用严格白名单，只允许明确放行的域名/地址 |

> [!tip] 大白话
> 沙盒像给 Claude Code 穿了一层"防护服"：文件系统隔离限制它只能读写当前目录，网络白名单限制它只能访问指定网站。`sandbox.filesystem.disabled` 相当于脱掉文件系统那层防护（信任 Claude 不乱动别的目录），但网络那层仍然穿着。

> [!note] 凭据掩码（credential masking）
> 沙盒还支持凭据掩码能力：mask 模式新增 `mode: "mask"`；支持 `extract` / `onExtractNoMatch`、`decode: "jwt"` + `maskClaims`、`awsPairs` / `sigv4`（AWS SigV4 重新签名）等，用于在子进程中保护敏感凭据。

### 10. Auto Mode 配置

```json
{
  "disableAutoMode": true,
  "autoMode": {
    "classifyAllShell": true
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `disableAutoMode` | boolean | 关闭 Auto mode。v2.1.207 起第三方平台（Bedrock/Vertex/AWS）无需 `CLAUDE_CODE_ENABLE_AUTO_MODE` 即可用 Auto mode，不想用可在此关闭 |
| `autoMode.classifyAllShell` | boolean | 让所有 Bash/PowerShell 命令都走 auto 分类器统一判断，而不是由模型逐个处理 |

> [!note] Auto mode 行为变化（v2.1.205/207）
> Auto mode 会阻止篡改会话 transcript 文件；对 `$(…)` / 反引号 / `<(…)` 中的灾难性删除命令（如 `rm -rf ~`），即使加了 `--dangerously-skip-permissions` 也会提示确认。

### 11. 无障碍模式（Screen Reader）

```json
{
  "axScreenReader": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `axScreenReader` | boolean | 屏幕阅读器模式，把终端界面转成线性纯文本，供 VoiceOver / NVDA 使用 |

> [!tip] 大白话
> 普通终端界面是"图形化布局"，屏幕阅读器读起来很吃力。开启 `axScreenReader` 后，Claude Code 会把界面变成一行行能朗读的纯文本，方便视障用户用读屏软件操作。

等效方式：

| 方式 | 写法 |
|------|------|
| CLI 参数 | `claude --ax-screen-reader` |
| 环境变量 | `CLAUDE_AX_SCREEN_READER=1` |
| settings.json | `"axScreenReader": true` |

### 12. 输入与工作流体验

```json
{
  "emojiCompletionEnabled": true,
  "vimInsertModeRemaps": {
    "jj": "Esc"
  },
  "workflowSizeGuideline": "medium"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `emojiCompletionEnabled` | boolean | 开启 emoji 短码自动补全（如输入 `:thumbsup:` 自动补全 👍） |
| `vimInsertModeRemaps` | object | 自定义 Vim 插入模式按键映射，如把 `jj` 映射为 `Esc` 快速退出插入模式 |

`workflowSizeGuideline` 用于给动态工作流提供规模建议：

| 值 | 说明 |
|----|------|
| `small` | 小型任务 |
| `medium` | 中等规模任务（默认） |
| `large` | 大型任务，触发更动态的工作流规划 |

> [!note] 说明
> `vimInsertModeRemaps` 的键名与取值以官方 schema 为准；本文示例为常见用法（`jj` → `Esc`）。

### 13. 跨会话消息

```json
{
  "crossSessionInbound": true,
  "dialogExpiry": "24h"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `crossSessionInbound` | boolean | 允许跨会话入站消息（例如后台会话或子代理向当前会话推送消息） |
| `dialogExpiry` | string | 跨会话消息/对话框的有效期，超过后自动过期失效（示例为 24h，具体格式以官方 schema 为准） |

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

留空 allow 列表（保持 `defaultMode: "manual"`），Claude Code 会在执行每个操作前询问确认，适合初学者或安全敏感场景。

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

### Q: 权限模式有哪些，怎么选？

`defaultMode` 控制审批档位：`manual`（默认，逐次询问）、`acceptEdits`（自动接受编辑）、`plan`（只读规划）、`bypassPermissions`（跳过权限检查）。新手或安全敏感场景选 `manual`。

---

## 最佳实践

### Do's（推荐）

- 把**团队规范**放 `.claude/settings.json`，提交到 Git 共享
- 把**个人偏好**放 `.claude/settings.local.json`，不提交
- 用 `allow` 列表放行高频安全操作，减少确认干扰
- 权限模式从 `manual` 起步，确认信任后再逐步放宽
- Hooks 配置先在本地测试，再推广到团队
- 使用 `$schema` 字段获得编辑器的自动补全和校验

### Don'ts（避免）

- ❌ 不要在 settings.json 中存放 API Key、Token、密码
- ❌ 不要放行 `Bash(*)` 或过于宽泛的权限
- ❌ 不要提交 `.env` 或 `settings.local.json` 到 Git
- ❌ 不要创建冗余的配置项（多个地方设置同一个值）

---

## 小结

settings.json 是 Claude Code 的"总控面板"：模型、推理级别、权限、自动压缩、环境变量、Hooks、MCP、沙盒、Auto mode、无障碍、输入体验等行为都能在这里配置，并按 全局 → 项目 → 本地 三级合并。

新手建议从最小配置开始（只设 `model`，保持 `defaultMode: "manual"`），用 `$schema` 获得编辑器校验，再按需逐项开启；权限与安全相关字段（`defaultMode`、`permissions`、`sandbox`）始终遵循最小权限原则。修改后可用 `/checkup` 诊断，必要时重启会话生效。

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
- 2026-08-10：同步 2026-08 现状。权限模式「Default」改名「Manual」（`defaultMode: "manual"`）；新增沙盒（`sandbox.filesystem.disabled` / `sandbox.network.strictAllowlist`）、Auto mode（`disableAutoMode` / `autoMode.classifyAllShell`）、无障碍（`axScreenReader`）、输入与工作流体验（`emojiCompletionEnabled` / `vimInsertModeRemaps` / `workflowSizeGuideline`）、跨会话消息（`crossSessionInbound` / `dialogExpiry`）等配置键说明；补齐小结结语；`status` 从 draft 改为 updated。
