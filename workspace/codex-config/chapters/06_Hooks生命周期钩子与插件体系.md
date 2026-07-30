---
title: Hooks 生命周期钩子与插件体系
tags: [codex, hooks, lifecycle-hooks, plugins, events, stdin-stdout, claude-code, automation]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# Hooks 生命周期钩子与插件体系

第五章我们介绍了 Agents 和 MCP——它们分别解决了"用独立环境执行任务"和"接入外部工具"的问题。但这两者都是在**功能层面**的扩展。还有一个更深层的问题：当我们需要在 agent 执行过程的**特定时刻**自动触发某些行为时——比如"每次工具调用前检查安全策略""每次会话启动时加载项目简报""每次上下文压缩前保存关键信息"——该怎么做？

这就是本章要解决的课题。

Codex 提供了 **11 种生命周期钩子事件**，覆盖了从会话启动到停止的完整生命周期。它同时还拥有一个**插件体系**，允许将 hooks、skills、MCP 服务器打包为一个可分发、可安装的单元。

> **Claude Code 对照**：Claude Code 也有 hooks 系统，但只有 4 种核心事件。Claude Code 没有独立的插件体系——它的"扩展"完全通过 MCP 服务器实现。本章会逐一对比这些差异，并帮助你理解插件 vs MCP 的适用边界。

---

## Part 1：Hooks 生命周期钩子系统

### 1.1 Hooks 解决什么问题？

先看几个真实场景：

- **安全审计**：每次 agent 要执行 Bash 命令之前，检查命令是否包含敏感操作（如 `rm -rf /`），如果匹配则拒绝执行
- **环境初始化**：每次会话启动时，自动加载一份项目状态报告注入到上下文中，让 agent 从一开始就了解项目结构
- **自动审批**：对特定工具（如只读文件操作）自动批准权限请求，减少不必要的交互确认
- **状态持久化**：每次上下文压缩前，把当前工作状态保存到一个 JSON 文件中，防止信息丢失
- **合规记录**：每次工具调用后，记录操作日志到审计数据库

这些场景的共同点：**它们需要在 agent 执行流程的特定时机自动触发一个外部脚本，并根据脚本的返回值影响后续的执行路径**。这正是 hooks 系统的核心价值。

### 1.2 配置文件与合并规则

#### 配置方式

Hooks 有两种配置方式：

**方式一：独立 `hooks.json` 文件**

```json
// ~/.codex/hooks.json 或 .codex/hooks.json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes...",
            "timeout": 600,
            "additionalContextLimit": 2500
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/pre_tool.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**方式二：内联到 `config.toml`**

```toml
# ~/.codex/config.toml 或 .codex/config.toml
[hooks.SessionStart]
matcher = "startup|resume"
hooks = [
  { type = "command", command = "python3 ~/.codex/hooks/session_start.py",
    statusMessage = "Loading session notes...", timeout = 600, additionalContextLimit = 2500 }
]

[hooks.PreToolUse]
matcher = "Bash|Edit"
hooks = [
  { type = "command", command = "python3 ~/.codex/hooks/pre_tool.py", timeout = 5000 }
]
```

两种方式等价，你可以根据偏好选择。

#### 发现路径与合并规则

Hooks 的发现路径遵循多级查找：

```text
# 按优先级从低到高（但合并规则特殊，见下文）
~/.codex/hooks.json         # 全局用户级
~/.codex/config.toml        # 全局用户级（内联）
<repo>/.codex/hooks.json    # 项目级
<repo>/.codex/config.toml   # 项目级（内联）
```

**合并规则**：与其他配置的"下层被上层覆盖"不同，hooks 的合并规则是**叠加运行**。

> 同一事件的所有来源的全部匹配钩子**都会执行**，不会覆盖。

举例说明：

```json
// ~/.codex/hooks.json（全局级）
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "audit_bash.sh" }]
      }
    ]
  }
}
```

```json
// .codex/hooks.json（项目级）
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "project_audit.sh" }]
      }
    ]
  }
}
```

当执行 Bash 命令时，`audit_bash.sh` **和** `project_audit.sh` **都会运行**（先全局后项目）。这与 config.toml 的"下层被上层覆盖"规则完全不同。

> **为什么叠加而不是覆盖？** 安全场景需要。如果全局钩子负责安全合规审计，项目级钩子不能绕过它。叠加执行确保安全基线不会被项目级配置意外关闭。

但如果某个钩子返回了阻止执行的决策（退出码 2），后续钩子是否还会执行？答案是否定的——一旦有钩子返回阻断决策，事件处理链立即终止，后续钩子不再执行。

### 1.3 11 种事件类型详解

Codex 定义了 11 种生命周期事件，覆盖 agent 会话的完整执行流程。以下按"会话生命周期"顺序排列，分为**启动阶段、执行阶段、压缩阶段、停止阶段**四大类。

#### 事件总表

| 阶段 | 事件名称 | 触发时机 | Matcher 支持 | 决策能力 | 常用场景 |
|------|----------|----------|-------------|----------|----------|
| **启动** | **SessionStart** | 主会话或子代理会话启动时 | `source`: startup / resume / clear / compact | 无（只读） | 加载项目简报、检查环境依赖、初始化日志 |
| **启动** | **SubagentStart** | 子代理实例启动时 | `agent_type`（如 default / worker / explorer） | 无（只读） | 记录子代理启动计数、注入子代理专属上下文 |
| **执行** | **PreToolUse** | 任意工具调用之前 | `tool_name`: Bash / Edit / Read / MCP 工具名 | **放行 / 拒绝 / 重写输入** | 安全审计、命令黑名单、参数校验、敏感操作拦截 |
| **执行** | **PermissionRequest** | 即将弹出审批请求时 | `tool_name` | **批准 / 拒绝** | 自动审批特定工具、基于规则的批量授权 |
| **执行** | **PostToolUse** | 工具执行完成之后 | `tool_name` | 阻断 / 增加上下文 | 记录操作日志、保存工具输出快照、触发下游通知 |
| **执行** | **UserPromptSubmit** | 用户提交新的提示词时 | 不支持（忽略） | **阻断** | 输入审核、内容过滤、指令覆盖保护 |
| **执行** | **Stop** | 主线程收到停止信号时 | 不支持（忽略） | **阻断（自动续期）** | 保存工作状态防丢失、优雅关闭前清理 |
| **执行** | **SubagentStop** | 子代理实例停止时 | `agent_type` | **重试子代理** | 子代理失败自动重试、失败原因记录 |
| **压缩** | **PreCompact** | 上下文压缩即将开始时 | `trigger`: manual / auto | 无（只读） | 保存当前工作摘要到文件、标记关键上下文免于压缩 |
| **压缩** | **PostCompact** | 上下文压缩完成之后 | `trigger`: manual / auto | 无（只读） | 验证压缩结果、重新注入必要上下文 |
| **停止** | **SessionEnd** | 主会话正常结束时 | `reason`: other（当前仅此） | 无（只读） | 生成会话摘要、清理临时文件、上报使用统计 |

> **关键设计模式**：有决策能力的事件（PreToolUse、PermissionRequest、Stop、SubagentStop、UserPromptSubmit）是 hooks 的"阀门"——它们可以改变 Codex 的执行路径。无决策能力的事件是"观察者"——它们只能读取状态并执行副作用，不能影响执行流程。

#### 各事件详细说明

**SessionStart** — 最常用的启动时钩子。matcher 通过 `source` 字段区分启动类型：
- `startup`：全新会话启动
- `resume`：从历史恢复的会话
- `clear`：用户执行 `/clear` 后重新开始
- `compact`：压缩后自动重建上下文

典型用途：在 `startup` 和 `resume` 时加载项目状态简报，让 agent 快速恢复上下文。

**PreToolUse** — 最强大的干预钩子。它在 agent 即将调用任何工具时触发，可以：
- **放行**（退出码 0）：允许工具执行
- **拒绝**（退出码 2 + 自定义 message）：阻止工具执行并告知 agent 原因
- **重写输入**（退出码 0 + 修改 stdin 输入）：修改工具调用的参数

**PermissionRequest** — 审批自动化的关键。当 Codex 需要用户审批权限时触发此事件，钩子可以自动批准或拒绝。

**PreCompact / PostCompact** — Codex 独有的上下文压缩事件。Claude Code 没有对等的钩子。当上下文窗口接近满时触发，让你有机会在压缩前保存重要信息。

**Stop** — 特殊的"阻断"事件。当用户请求停止时触发，钩子可以返回 `block` 决策让 Codex 继续运行（例如用于"正在处理关键操作，不要中断"）。Codex 会自动生成一个 continuation prompt 给模型继续执行。

### 1.4 钩子决策能力详解

不同事件拥有不同的决策能力，具体表现为 stdin 输入中的额外字段和 stdout 输出中的特定指令。

#### 决策矩阵

| 事件 | 支持的操作 | 通过什么实现 | 实际效果 |
|------|-----------|-------------|---------|
| **PreToolUse** | 放行 / 拒绝 / 重写输入 | 退出码 0 放行；退出码 2 拒绝；修改 stdin 输入后再退出码 0 实现重写 | 决定工具是否执行以及以什么参数执行 |
| **PermissionRequest** | 批准 / 拒绝 | stdout 中返回 `"approved": true/false` | 自动化审批流程 |
| **PostToolUse** | 阻断 / 增加上下文 | 退出码 2 阻断；stdout 中 `additional_context` 字段增加上下文 | 在工具执行后决定是否阻止后续流程 |
| **Stop** | 阻断（自动续期） | stdout 中 `"block": true` | 阻止会话终止，Codex 自动继续运行 |
| **SubagentStop** | 重试子代理 | stdout 中 `"retry": true` | 自动重启失败的子代理 |
| **UserPromptSubmit** | 阻断 | 退出码 2 | 阻止用户输入被提交给模型 |

#### PreToolUse 重写输入示例

这是钩子系统最强大的能力之一——在工具执行前修改其参数：

```python
#!/usr/bin/env python3
# pre_tool_rewrite.py — PreToolUse 钩子：重写 Bash 命令以防止危险操作
import json, sys

# 读取标准输入的 JSON 事件数据
input_data = json.loads(sys.stdin.read())

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name == "Bash":
    command = tool_input.get("command", "")
    
    # 如果涉及 rm 命令，拒绝执行
    if command.strip().startswith("rm"):
        print(json.dumps({
            "stopReason": "dangerous_command",
            "systemMessage": f"Blocked dangerous command: {command}"
        }))
        sys.exit(2)  # 退出码 2 = 拒绝
    
    # 如果涉及 pip install，添加 --quiet 参数
    if "pip install" in command and "--quiet" not in command:
        safe_command = command.replace("pip install", "pip install --quiet")
        tool_input["command"] = safe_command
        # 重写输入：输出修改后的 tool_input
        print(json.dumps({
            "tool_input": tool_input
        }))
        sys.exit(0)  # 退出码 0 = 放行（但用修改后的参数）

# 默认放行
sys.exit(0)
```

> **预期行为**：当 agent 执行 `rm -rf /data/logs` 时，钩子拒绝并告知原因。当 agent 执行 `pip install requests` 时，钩子自动修改为 `pip install --quiet requests` 后再放行。其他工具调用则直接放行。

### 1.5 stdin/stdout 协议细节

Codex 与 hook 脚本之间通过标准的 stdin/stdout 进行全双工通信。**脚本启动时，Codex 通过 stdin 发送事件数据；脚本通过 stdout 返回决策结果**。

#### 通用输入字段

每次事件触发时，Codex 通过 stdin 发送以下通用字段：

```json
// stdin 通用字段 — 所有事件都包含
{
  "session_id": "abc-123-def",          // 当前会话的唯一标识
  "transcript_path": "/path/to/transcript",  // 会话转录文件路径
  "cwd": "/home/user/project",          // agent 的当前工作目录
  "hook_event_name": "PreToolUse",      // 当前触发的事件名称
  "model": "gpt-5.4"                    // 当前使用的模型
}
```

#### 事件特有输入字段

不同事件在通用字段之上附加特有字段：

| 事件 | 额外字段 |
|------|---------|
| SessionStart | `source`: "startup" / "resume" / "clear" / "compact" |
| SessionEnd | `reason`: "other" |
| SubagentStart | `agent_type`: "default" / "worker" / "explorer" / "<custom>" |
| SubagentStop | `agent_type`, `exit_code`, `duration_ms` |
| PreToolUse | `tool_name`, `tool_input`（包含该工具的全部参数）, `tool_type` |
| PermissionRequest | `tool_name`, `tool_input`, `request_message`（审批提示消息） |
| PostToolUse | `tool_name`, `tool_input`, `tool_output`（工具执行结果）, `exit_code`, `duration_ms` |
| PreCompact | `trigger`: "manual" / "auto", `current_tokens` |
| PostCompact | `trigger`: "manual" / "auto", `tokens_after`, `tokens_before` |
| UserPromptSubmit | `prompt`（用户输入） |
| Stop | `reason`（停止原因） |

#### 通用输出字段

脚本通过 stdout 返回 JSON，Codex 根据字段和退出码决定后续行为：

```json
// stdout 通用字段
{
  "continue": true,              // 是否继续执行（不再支持，用退出码替代）
  "stopReason": "custom_reason", // 如果拒绝/阻断，提供原因标识
  "systemMessage": "说明文字"     // 给模型的提示信息
}
```

#### 决策类事件的特殊输出字段

| 事件 | 特殊输出字段 | 配合退出码 |
|------|-------------|-----------|
| PreToolUse（重写） | `tool_input`：修改后的工具输入参数 | 0 |
| PermissionRequest | `approved`: true / false | 0 或 2 |
| PostToolUse（增加上下文） | `additional_context`：字符串，追加到当前上下文 | 0 |
| Stop（阻止终止） | `block`: true | 0 |
| SubagentStop（重试） | `retry`: true | 0 |

#### 退出码约定

| 退出码 | 含义 |
|--------|------|
| **0** | 成功继续。无决策能力的事件：正常执行；有决策能力的事件：放行/批准 |
| **2** | 阻断/拒绝。停止当前事件的处理流程，后续钩子不再执行 |

> **为什么用 2 而不是 1？** 退出码 1 通常表示通用错误，Codex 不将其视为明确的决策信号。退出码 2 被定义为"我明确作出了阻断决策"。如果你的 hook 脚本遇到内部错误，也应该用退出码 2 表示"无法安全放行"，而非 1。

#### 完整交互示例

以下是一个 PreToolUse 钩子的完整通信流程：

```text
=== Codex → 脚本（stdin） ===
{
  "session_id": "sess_20240731_001",
  "transcript_path": "/home/user/.codex/transcripts/sess_20240731_001.jsonl",
  "cwd": "/home/user/project",
  "hook_event_name": "PreToolUse",
  "model": "gpt-5.4",
  "tool_name": "Bash",
  "tool_input": {
    "command": "curl -X POST https://internal-api.local/delete-all"
  }
}

=== 脚本 → Codex（stdout，退出码 2） ===
{
  "stopReason": "blocked_network_command",
  "systemMessage": "Blocked: curl POST to internal API is not allowed without approval. Use the project's API client instead."
}
```

交互结果：agent 收到阻断消息，停止调用 curl，并尝试使用替代方案。

### 1.6 启用与安全管理

#### 默认启用

Hooks 功能默认是开启的：

```toml
# config.toml
[features]
hooks = true   # 默认即为 true，无需显式设置
```

如果你需要完全禁用 hooks 系统（例如在性能测试环境中），显式设置为 `false`：

```toml
[features]
hooks = false  # 所有钩子事件不再触发
```

#### `/hooks` 命令

Codex 提供了交互式命令来管理钩子：

```bash
# 在交互式会话中
/hooks

# 输出示例：
Known Hooks:
  1. SessionStart — ~/.codex/hooks.json → python3 ~/.codex/hooks/session_start.py
     Status: ENABLED   Trust: trusted
  2. PreToolUse — .codex/hooks.json → python3 .codex/hooks/audit.py
     Status: ENABLED   Trust: untrusted  [Pending your approval]
  
  Commands: trust <id> | untrust <id> | disable <id> | enable <id> | status
```

通过 `/hooks` 命令你可以：
- **审查**已注册的钩子和它们的来源
- **信任/取消信任**特定钩子（未信任的钩子不会执行）
- **启用/禁用**特定钩子

#### 信任机制

首次加载一个钩子时，Codex 会在 `/hooks` 中以 `untrusted` 状态显示该钩子。你需要明确执行信任操作后，钩子才会生效。这是防止恶意钩子的第一道防线。

```bash
# 在 /hooks 交互中信任钩子
/hooks trust 2
```

#### 托管钩子（Managed Hooks）

在企业环境中，管理员可能需要强制部署安全钩子且不允许用户绕过。这通过 `requirements.toml` 实现：

```toml
# requirements.toml — 企业托管配置
allow_managed_hooks_only = true
```

当 `allow_managed_hooks_only = true` 时：
- 只有 `requirements.toml` 中定义的钩子被允许执行
- 用户级和项目级的所有自定义钩子**被忽略**
- 用户无法通过 `/hooks` 命令添加或信任其他钩子

这是安全合规场景的关键特性——确保安全审计类钩子始终在线，不能被绕过。

### 1.7 Codex Hooks vs Claude Code Hooks 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| **事件数量** | 11 种 | 4 种核心 |
| **配置格式** | JSON（hooks.json）或 TOML（config.toml 内联） | settings.json 内联 JSON |
| **合并策略** | 叠加执行（所有来源都运行） | 叠加执行 |
| **匹配器** | matcher 正则 / 枚举匹配 | 无（每种事件直接注册一组处理程序） |
| **事件清单** | SessionStart / SessionEnd / SubagentStart / SubagentStop / PreToolUse / PermissionRequest / PostToolUse / PreCompact / PostCompact / UserPromptSubmit / Stop | Notification / PreToolUse / PostToolUse / SessionStart |
| **Codex 独有事件** | SessionEnd, SubagentStart, SubagentStop, PreCompact, PostCompact, UserPromptSubmit, Stop | — |
| **决策能力** | PreToolUse（放行/拒绝/重写）、PermissionRequest（批准/拒绝）、Stop（阻止终止）、SubagentStop（重试）、UserPromptSubmit（阻断） | PreToolUse（放行/拒绝/重写） |
| **CLI 管理** | `/hooks` 命令（审查/信任/禁用） | `/hooks` 命令（审查/暂停/恢复/禁用） |
| **信任机制** | 首次加载 untrusted，需用户信任后执行 | 无明确信任机制 |
| **托管模式** | `allow_managed_hooks_only`（requirements.toml） | 无 |
| **动态上下文注入** | `additionalContextLimit` / `additional_context` | 类似 |
| **退出码含义** | 0 = 继续，2 = 阻断/拒绝 | 类似 |

#### 关键差异解读

1. **事件数量差异巨大**：Codex 的 11 种事件 vs Claude Code 的 4 种，主要增量来自：
   - **上下文压缩生命周期**（PreCompact / PostCompact）— 这是 Codex 独有的，因为没有对应的 Claude Code 事件
   - **子代理生命周期**（SubagentStart / SubagentStop）— 因为 Codex 的 Agent 是第一等配置实体，所以需要对应的钩子事件
   - **会话边界**（SessionEnd / Stop / UserPromptSubmit）— 覆盖了更多会话交互场景

2. **匹配器**：Codex 的 matcher 机制允许更精细的事件过滤。Claude Code 对每种事件直接注册处理程序，没有独立的匹配层。

3. **信任与托管**：Codex 的"首次 untrusted + 用户信任"机制提供了更好的安全保障。托管钩子是 Codex 独有，适合企业合规场景。

4. **审批自动化**：Codex 的 PermissionRequest 钩子可以实现自动审批，而 Claude Code 没有对等的事件——意味着所有权限请求都需要用户手动处理。

---

## Part 2：插件体系

如果说 Hooks 是"在特定时机触发行为"的机制，那么插件就是"把多种扩展打包为一个可分发单元"的载体。一个 Codex 插件可以包含 hooks、skills、MCP 服务器，甚至 UI 组件。

### 2.1 插件结构

插件是一个遵循特定目录结构的文件夹：

```text
.codex-plugin/              # 插件根目录
├── plugin.json             # 必选：插件清单文件
├── hooks/
│   └── hooks.json          # 可选：插件自带的钩子配置
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md        # 可选：插件包含的技能
│   └── skill-b/
│       └── SKILL.md
└── assets/                 # 可选：插件资源文件
```

关键点在于：**插件不仅仅是 hooks 的容器**。它把多种扩展类型聚合在一起，通过一个 `plugin.json` 清单文件统一声明和管理。

### 2.2 plugin.json 关键字段

```json
{
  "name": "my-extension",              // 必填：插件唯一标识名
  "version": "1.0.0",                  // 推荐：语义化版本号
  "description": "项目开发辅助插件",     // 推荐：简短描述
  "skills": [                          // 可选：插件包含的技能路径
    "skills/skill-a",
    "skills/skill-b"
  ],
  "mcp_servers": {                     // 可选：插件自带的 MCP 服务器配置
    "my-db": {
      "command": "node",
      "args": ["mcp-server.js"],
      "approval_mode": "writes"
    }
  },
  "hooks": "hooks/hooks.json",         // 可选：覆盖 hooks.json 路径（默认搜索 hooks/）
  "apps": []                           // 可选：UI 组件（面向 ChatGPT/Codex UI）
}
```

**字段详解**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | 字符串 | 是 | 插件名。1-64 字符，小写字母、数字、连字符。用于标识和去重 |
| `version` | 字符串 | 推荐 | 语义化版本号。遵循 semver 规范 |
| `description` | 字符串 | 推荐 | 插件的简短描述。显示在插件市场中 |
| `skills` | 字符串数组 | 否 | 插件的技能路径。相对于插件根目录。Codex 自动将这些技能注册到 Plugin 作用域的技能发现路径 |
| `mcp_servers` | 对象 | 否 | MCP 服务器定义。与 `[mcp_servers]` config.toml 配置格式完全相同 |
| `hooks` | 字符串 | 否 | hooks.json 路径。相对于插件根目录。默认搜索 `hooks/hooks.json` |
| `apps` | 对象数组 | 否 | UI 组件配置。在 ChatGPT/Codex UI 中渲染自定义界面 |

#### 完整插件示例

```json
// .codex-plugin/plugin.json
{
  "name": "project-helper",
  "version": "0.2.1",
  "description": "提供项目脚手架、自动文档生成和代码审查辅助",
  "skills": [
    "skills/scaffolder",
    "skills/doc-generator",
    "skills/code-reviewer"
  ],
  "mcp_servers": {
    "template-renderer": {
      "command": "npx",
      "args": ["-y", "@project/template-mcp"],
      "approval_mode": "auto"
    }
  },
  "hooks": "hooks/hooks.json"
}
```

```json
// .codex-plugin/hooks/hooks.json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "node .codex-plugin/hooks/check-project-health.js",
            "timeout": 3000
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node .codex-plugin/hooks/shell-audit.js",
            "timeout": 2000
          }
        ]
      }
    ]
  }
}
```

#### 安装和注册

插件通过文件系统放置即可生效：

```bash
# 全局安装
cp -r my-plugin ~/.codex/plugins/my-plugin/

# 项目级安装
cp -r my-plugin .codex/plugins/my-plugin/

# 验证
codex status  # 应能看到插件及其注册的技能和钩子
```

Codex 会自动扫描 `plugins/` 目录下的 `plugin.json`，注册其中的技能到 Plugin 作用域的发现路径，加载 MCP 服务器配置，并合并 hooks。

#### 内置插件与市场

Codex 与 ChatGPT 共享统一的插件目录和市场生态。内置插件包括：

- **codex-core**：核心插件，提供 skill-creator、workflow-orchestrator 等内置技能
- 其他通过插件市场安装的社区或官方插件

### 2.3 插件 vs MCP 扩展对比

一个常见的困惑是：**插件和 MCP 都是"扩展"，它们有什么区别？什么时候该用哪个？**

| 维度 | 插件（Plugin） | MCP 服务器 |
|------|---------------|------------|
| **本质** | 一个**聚合容器**，可以包含多种扩展类型 | 一个**工具服务器**，提供一组工具调用接口 |
| **包含内容** | skills + hooks + MCP 服务器 + UI 组件 | 只有工具（tools） |
| **安装方式** | 放置到 `plugins/` 目录 | 在 `config.toml` 中配置 `[mcp_servers]` |
| **行为影响** | 可以注入指令（skills）、自动化流程（hooks）、工具（MCP） | 只提供工具调用能力 |
| **UI 组件** | 可以包含 `apps` 字段渲染 UI | 无 |
| **发现方式** | Codex 自动扫描 `plugins/` 目录 | `config.toml` 中声明 |
| **共享生态** | Codex + ChatGPT 统一插件市场 | MCP 标准协议，跨工具通用 |
| **生命周期** | 插件可携带 hooks 参与 session 生命周期 | 无生命周期钩子 |
| **可分发性** | 一个文件夹 + `plugin.json`，可打包分享 | 每个 MCP 服务器独立，需单独配置 |
| **Claude Code 对应** | 无 | 同 MCP 协议，配置格式不同 |

#### 决策指南

```
你需要扩展 Codex 的能力...
│
├─ 只需要提供工具调用（API、数据库、文件操作）
│   → 用 MCP 服务器。轻量、标准、跨工具通用。
│
├─ 需要同时提供工具 + 指令 + 自动化流程
│   → 用插件。把 MCP 服务器放进插件里一起打包。
│
├─ 需要注入技能（指令文件）
│   → 用插件。插件可以包含多个技能。
│
├─ 需要在特定时机自动执行脚本（hooks）
│   → 用插件。把 hooks 放进插件里。
│
└─ 只是 Claude Code 用户，不涉及 Codex
    → MCP 服务器即可，无需插件。
```

**一句话总结**：MCP 是"工具协议"——让 agent 能干活；插件是"扩展打包"——把技能、工具、自动化流程打包在一起方便分发和安装。

---

## 本章小结

- **Hooks 系统让 Codex 在 11 个生命周期节点自动触发外部脚本**，覆盖会话启动、工具调用、上下文压缩、审批请求、会话停止等完整的 agent 执行流程。事件通过 matcher 机制支持细粒度过滤，多个来源的同一事件钩子叠加执行（不覆盖）。
- **钩子拥有六种决策能力**：PreToolUse 可以放行/拒绝/重写工具输入；PermissionRequest 可以自动批准/拒绝审批请求；Stop 可以阻止会话终止；SubagentStop 可以自动重试子代理；UserPromptSubmit 可以阻断用户输入。退出码 0 表示放行，退出码 2 表示阻断/拒绝。
- **stdin/stdout 协议规定了通信格式**：Codex 通过 stdin 发送事件数据（含通用字段 + 事件特有字段），脚本通过 stdout 返回决策结果（含停止原因、系统消息、审批状态等），退出码决定最终行为。
- **安全管理分层**：默认启用的 hooks 可通过 `/hooks` 命令审查/信任/禁用；"首次 untrusted"机制防止恶意钩子自动执行；`allow_managed_hooks_only`（requirements.toml）用于企业合规场景，只允许托管钩子运行。
- **Codex 的 11 种 hooks 事件远多于 Claude Code 的 4 种**，主要增量来自上下文压缩生命周期、子代理生命周期和更多会话边界事件。PermissionRequest 事件的大模型自动化审批能力是 Codex hooks 独有。
- **插件体系是 Codex 的扩展打包机制**，通过 `plugin.json` 清单文件把一个或多个 skills、hooks、MCP 服务器、UI 组件聚合为可分发单元。插件通过 `plugins/` 目录自动发现，与 ChatGPT 共享统一插件市场。
- **插件与 MCP 的核心区别**：MCP 是工具协议，只提供工具调用能力；插件是聚合容器，可以包含 MCP 服务器 + skills + hooks + UI 组件。如果你只需要工具，用 MCP；如果需要打包多个扩展一起分发，用插件。

## 下一章预告

至此，我们已经完整覆盖了 Codex 的配置哲学（第一章）、核心配置（第二章）、指令与规则（第三章）、技能系统（第四章）、子代理与 MCP（第五章）、以及 hooks 与插件（第六章）。但学完理论配置之后，一个更实际的问题来了：**如何验证配置是否正确？如何排查问题？** 下一章将进入日常操作层面——**CLI 命令与调试技巧**，涵盖 `codex status` 配置审计、`/config` 交互式配置、环境变量管理以及常见问题的排查方法。
