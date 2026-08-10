---
title: Hooks 与插件
tags: [codex, ai, 工具使用, 进阶应用, hooks]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# Hooks 与插件

> [!info] 文档定位
> **一句话定位** - 本篇覆盖 Codex 的 11 种生命周期钩子事件与插件体系，介绍如何在 agent 执行的特定时刻自动触发外部脚本，以及如何将 hooks、skills、MCP 服务器打包为可分发插件。适合已了解 Codex 基础配置、需要做自动化与扩展的进阶用户。

---

## Hooks 生命周期钩子系统

Agents 和 MCP 分别解决了"用独立环境执行任务"和"接入外部工具"的问题。但还有更深层的问题：当我们需要在 agent 执行过程的**特定时刻**自动触发某些行为时——比如"每次工具调用前检查安全策略""每次会话启动时加载项目简报""每次上下文压缩前保存关键信息"——该怎么做？

Codex 提供了 **11 种生命周期钩子事件**，覆盖了从会话启动到停止的完整生命周期。它同时还拥有一个**插件体系**，允许将 hooks、skills、MCP 服务器打包为一个可分发、可安装的单元。

### 配置文件与合并规则

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
[hooks.SessionStart]
matcher = "startup|resume"
hooks = [
  { type = "command", command = "python3 ~/.codex/hooks/session_start.py",
    statusMessage = "Loading session notes...", timeout = 600 }
]
```

**合并规则**：与其他配置的"下层被上层覆盖"不同，hooks 的合并规则是**叠加运行**——同一事件的所有来源的全部匹配钩子**都会执行**，不会覆盖。但一旦有钩子返回阻断决策，事件处理链立即终止。

### 11 种事件类型详解

| 阶段 | 事件名称 | 触发时机 | Matcher 支持 | 决策能力 |
|------|----------|----------|-------------|----------|
| **启动** | **SessionStart** | 主会话或子代理会话启动时 | `source`: startup / resume / clear / compact | 无（只读） |
| **启动** | **SubagentStart** | 子代理实例启动时 | `agent_type` | 无（只读） |
| **执行** | **PreToolUse** | 任意工具调用之前 | `tool_name` | **放行 / 拒绝 / 重写** |
| **执行** | **PermissionRequest** | 即将弹出审批请求时 | `tool_name` | **批准 / 拒绝** |
| **执行** | **PostToolUse** | 工具执行完成之后 | `tool_name` | 阻断 / 增加上下文 |
| **执行** | **UserPromptSubmit** | 用户提交新的提示词时 | 不支持 | **阻断** |
| **执行** | **Stop** | 主线程收到停止信号时 | 不支持 | **阻断（自动续期）** |
| **执行** | **SubagentStop** | 子代理实例停止时 | `agent_type` | **重试子代理** |
| **压缩** | **PreCompact** | 上下文压缩即将开始时 | `trigger`: manual / auto | 无（只读） |
| **压缩** | **PostCompact** | 上下文压缩完成之后 | `trigger`: manual / auto | 无（只读） |
| **停止** | **SessionEnd** | 主会话正常结束时 | `reason`: other | 无（只读） |

### PreToolUse 重写输入示例

```python
#!/usr/bin/env python3
# pre_tool_rewrite.py — PreToolUse 钩子
import json, sys

input_data = json.loads(sys.stdin.read())
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name == "Bash":
    command = tool_input.get("command", "")

    if command.strip().startswith("rm"):
        print(json.dumps({
            "stopReason": "dangerous_command",
            "systemMessage": f"Blocked dangerous command: {command}"
        }))
        sys.exit(2)  # 退出码 2 = 拒绝

    if "pip install" in command and "--quiet" not in command:
        safe_command = command.replace("pip install", "pip install --quiet")
        tool_input["command"] = safe_command
        print(json.dumps({"tool_input": tool_input}))
        sys.exit(0)  # 退出码 0 = 放行（用修改后的参数）

sys.exit(0)
```

### 退出码约定

| 退出码 | 含义 |
|--------|------|
| **0** | 成功继续。有决策能力的事件：放行/批准 |
| **2** | 阻断/拒绝。停止当前事件的处理流程 |

### 启用与安全管理

```bash
# 在交互式会话中管理钩子
/hooks

# 输出示例：
Known Hooks:
  1. SessionStart — ~/.codex/hooks.json → python3 ~/.codex/hooks/session_start.py
     Status: ENABLED   Trust: trusted
  2. PreToolUse — .codex/hooks.json → python3 .codex/hooks/audit.py
     Status: ENABLED   Trust: untrusted  [Pending your approval]

# 信任钩子
/hooks trust 2
```

### Codex Hooks vs Claude Code Hooks 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 事件数量 | 11 种 | 4 种核心 |
| 配置格式 | JSON（hooks.json）或 TOML（内联） | settings.json 内联 JSON |
| 合并策略 | 叠加执行 | 叠加执行 |
| Codex 独有事件 | SessionEnd, SubagentStart/Stop, PreCompact, PostCompact, UserPromptSubmit, Stop | — |
| CLI 管理 | `/hooks` 命令（审查/信任/禁用） | `/hooks` 命令 |
| 信任机制 | 首次加载 untrusted，需用户信任 | 无明确信任机制 |
| 托管模式 | `allow_managed_hooks_only`（requirements.toml） | 无 |

---

## 插件体系

如果说 Hooks 是"在特定时机触发行为"的机制，那么插件就是"把多种扩展打包为一个可分发单元"的载体。

### 插件目录结构

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

### 插件清单 plugin.json

```json
{
  "name": "project-helper",
  "version": "0.2.1",
  "description": "项目开发辅助插件",
  "skills": ["skills/scaffolder", "skills/doc-generator"],
  "mcp_servers": {
    "template-renderer": {
      "command": "npx",
      "args": ["-y", "@project/template-mcp"]
    }
  },
  "hooks": "hooks/hooks.json"
}
```

### 插件 vs MCP 扩展对比

| 维度 | 插件（Plugin） | MCP 服务器 |
|------|---------------|------------|
| 本质 | 聚合容器 | 工具服务器 |
| 包含内容 | skills + hooks + MCP + UI | 只有工具 |
| Claude Code 对应 | 无 | 同 MCP 协议，配置格式不同 |

> **决策指南**：只需要工具调用用 MCP；需要工具+指令+自动化流程用插件；只是 Claude Code 用户不涉及 Codex，MCP 即可。

---

## 常见问题

### Q: Hook 与插件有什么区别？
**回答**：Hooks 是"在特定时机触发行为"的机制，通过 `hooks.json` 或内联 `config.toml` 配置，在 11 种生命周期事件节点自动触发外部脚本。插件是"把多种扩展打包为一个可分发单元"的载体，通过 `plugin.json` 聚合 skills、hooks、MCP 服务器（以及 UI）并支持分发安装。决策指南：只需要工具调用用 MCP；需要工具+指令+自动化流程用插件。

### Q: 钩子返回的退出码 0 和 2 分别代表什么？
**回答**：退出码 **0** 表示成功继续，对有决策能力的事件（如 PreToolUse、PermissionRequest）即为放行/批准；退出码 **2** 表示阻断/拒绝，会停止当前事件的处理流程。例如 PreToolUse 钩子检测到以 `rm` 开头的危险命令时，输出 `stopReason` 并 `sys.exit(2)` 即可拒绝执行；改写参数（如 `pip install` 自动加 `--quiet`）后返回 0 则放行修改后的输入。

### Q: 为什么新钩子首次加载时显示 untrusted？
**回答**：这是 Codex 的安全信任机制。新钩子首次加载默认为 untrusted（未信任）状态，需要通过 `/hooks` 命令审查来源，再用 `/hooks trust <编号>` 显式信任后才会以 trusted 状态启用。托管模式下可通过 `allow_managed_hooks_only`（配置于 requirements.toml）限制只运行托管钩子。

---

## 最佳实践

### Do's
- 使用 `/hooks` 命令审查、信任、禁用钩子，首次加载时先确认 untrusted 钩子的来源再执行信任。
- 用 PreToolUse 在工具调用前做安全校验：检测危险命令（如 `rm`）返回退出码 2 阻断，改写参数（如 `pip install` 自动加 `--quiet`）后返回退出码 0 放行。
- 利用 hooks 的叠加合并特性，把多个来源（`~/.codex/hooks.json`、`.codex/hooks.json`）的匹配钩子组合使用，同一事件的全部钩子都会执行。
- 需要工具+指令+自动化流程时用插件打包，通过 `plugin.json` 声明 skills、hooks、MCP 服务器，便于分发与安装。

### Don'ts
- 不要假设 hooks 的合并遵循"下层被上层覆盖"——hooks 是**叠加运行**，所有匹配钩子都会执行，且一旦有钩子返回阻断决策，事件处理链立即终止。
- 不要使用退出码 0 / 2 之外的语义——约定只有 **0**（成功继续/放行批准）与 **2**（阻断/拒绝）两种。
- 不要跳过信任确认直接运行 untrusted 钩子，避免未审查代码被自动执行。
- 如果只需要工具调用，不要引入插件——直接用 MCP 服务器即可。

---

## 小结

Codex 通过 11 种生命周期钩子事件，在 agent 从启动到停止的完整执行过程中自动触发外部脚本，并借助插件体系将 hooks、skills、MCP 服务器打包为可分发单元。

> [!note] 本章小结
> Hooks 系统让 Codex 在 11 个生命周期节点自动触发外部脚本，覆盖完整的 agent 执行流程。钩子拥有六种决策能力，退出码 0 放行，退出码 2 阻断。安全管理通过信任机制和托管模式实现。插件体系是 Codex 的扩展打包机制，通过 `plugin.json` 把 skills、hooks、MCP 服务器聚合为可分发单元。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Agents 与 MCP]] | 子代理与 MCP 服务配置 |
| [[Codex CLI 与调试]] | 命令行与故障排查 |
| [[对照表与迁移实战]] | Hooks 迁移对照 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
