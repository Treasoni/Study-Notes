---
title: "Codex 完整配置体系"
tags: [codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# 第六章：Hooks 生命周期钩子与插件体系
第五章我们介绍了 Agents 和 MCP——它们分别解决了"用独立环境执行任务"和"接入外部工具"的问题。但还有更深层的问题：当我们需要在 agent 执行过程的**特定时刻**自动触发某些行为时——比如"每次工具调用前检查安全策略""每次会话启动时加载项目简报""每次上下文压缩前保存关键信息"——该怎么做？

Codex 提供了 **11 种生命周期钩子事件**，覆盖了从会话启动到停止的完整生命周期。它同时还拥有一个**插件体系**，允许将 hooks、skills、MCP 服务器打包为一个可分发、可安装的单元。

### Part 1：Hooks 生命周期钩子系统

#### 1.1 配置文件与合并规则

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

#### 1.2 11 种事件类型详解

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

#### 1.3 PreToolUse 重写输入示例

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

#### 1.4 退出码约定

| 退出码 | 含义 |
|--------|------|
| **0** | 成功继续。有决策能力的事件：放行/批准 |
| **2** | 阻断/拒绝。停止当前事件的处理流程 |

#### 1.5 启用与安全管理

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

#### 1.6 Codex Hooks vs Claude Code Hooks 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 事件数量 | 11 种 | 4 种核心 |
| 配置格式 | JSON（hooks.json）或 TOML（内联） | settings.json 内联 JSON |
| 合并策略 | 叠加执行 | 叠加执行 |
| Codex 独有事件 | SessionEnd, SubagentStart/Stop, PreCompact, PostCompact, UserPromptSubmit, Stop | — |
| CLI 管理 | `/hooks` 命令（审查/信任/禁用） | `/hooks` 命令 |
| 信任机制 | 首次加载 untrusted，需用户信任 | 无明确信任机制 |
| 托管模式 | `allow_managed_hooks_only`（requirements.toml） | 无 |

### Part 2：插件体系

如果说 Hooks 是"在特定时机触发行为"的机制，那么插件就是"把多种扩展打包为一个可分发单元"的载体。

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

**插件 vs MCP 扩展对比**：

| 维度 | 插件（Plugin） | MCP 服务器 |
|------|---------------|------------|
| 本质 | 聚合容器 | 工具服务器 |
| 包含内容 | skills + hooks + MCP + UI | 只有工具 |
| Claude Code 对应 | 无 | 同 MCP 协议，配置格式不同 |

> **决策指南**：只需要工具调用用 MCP；需要工具+指令+自动化流程用插件；只是 Claude Code 用户不涉及 Codex，MCP 即可。

> **本章小结**：Hooks 系统让 Codex 在 11 个生命周期节点自动触发外部脚本，覆盖完整的 agent 执行流程。钩子拥有六种决策能力，退出码 0 放行，退出码 2 阻断。安全管理通过信任机制和托管模式实现。插件体系是 Codex 的扩展打包机制，通过 `plugin.json` 把 skills、hooks、MCP 服务器聚合为可分发单元。

---


---

> [!note] 导航
> [[05 Agents 与 MCP|← 上一章]] | [[07 CLI 与调试|下一章 →]]



