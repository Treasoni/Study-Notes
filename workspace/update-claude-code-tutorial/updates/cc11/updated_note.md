---
title: Claude Code 插件系统使用指南
tags: [ai, 进阶应用, 插件]
created: 2025-01-15
updated: 2026-08-10
status: updated
source_project: claude-code-tutorial
---

# Claude Code 插件系统使用指南

> [!info] 为什么需要了解插件？
> 插件是 Claude Code 的核心扩展机制。理解插件系统后，你将能够：
> - 使用他人开发的插件增强 Claude Code 能力
> - 创建自己的插件，定制专属开发助手
> - 理解插件与 MCP 的关系（为什么有些 MCP 是"插件自带的"）

**相关文档**：[[Claude MCP 使用指南]] | [[Claude Code Subagents 完整指南]] | [[如何使用Claude code]] | [[Claude Code Checkpoints 使用指南]]

---

## 1. 什么是插件

### 核心概念

**插件 = Claude Code 的扩展模块**

| 类比 | 说明 |
|------|------|
| **浏览器扩展** | 给浏览器添加新功能 |
| **VS Code 插件** | 给编辑器添加新能力 |
| **Claude Code 插件** | 给 AI 助手添加专业技能 |

> [!tip] 大白话
> 插件就像给 Claude Code 装的「技能包」：装一个代码审查插件，Claude 就多出「审查代码」的专长；装一个数据库插件，它就自带查库的本事。你不用反复教它，装好即用。

### 插件 vs MCP 的关系

```
Claude Code 架构：

┌─────────────────────────────────────────────┐
│           Claude Code 核心                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │   插件系统    │      │   MCP 系统    │   │
│  │  (Plugins)   │      │  (MCP)        │   │
│  └──────────────┘      └──────────────┘   │
│         │                      │           │
│         └──────────┬───────────┘           │
│                    │                       │
│            插件可以自带 MCP 服务器           │
│            (Plugin MCP)                    │
└─────────────────────────────────────────────┘
```

**关键区别**：
- **MCP**：工具通信协议（定义工具如何与 Claude 对话）
- **插件**：功能扩展容器（可以包含多个 Agent、工具、MCP 服务器等）
- **插件 MCP**：插件自带的 MCP 服务器

### 插件能做什么？

| 能力 | 说明 | 示例 |
|------|------|------|
| **自定义 Agent** | 创建专门的 AI 助手 | 代码审查 Agent、测试生成 Agent |
| **自定义命令** | 添加新的 `/` 命令 | `/review`、`/test` |
| **自带 MCP** | 捆绑 MCP 服务器 | 数据库插件自带查询 MCP |
| **事件钩子** | 响应 Claude 操作 | 写完代码自动格式化 |
| **LSP 集成** | 语言服务器协议 | 代码补全、诊断信息 |

---

## 2. 插件结构

### 目录结构

```
my-plugin/
├── .claude-plugin/           # 插件配置目录（必需）
│   └── plugin.json          # 插件元数据（必需）
├── agents/                  # 专门化 Agent（可选）
│   └── specialist.md
├── commands/                # 自定义命令（可选）
│   └── task.md
├── skills/                  # Agent 能力定义（可选）
│   └── skill.md
├── hooks/                   # 事件处理器（可选）
│   └── hooks.json
├── .mcp.json               # MCP 服务器配置（可选）
├── .lsp.json               # LSP 服务器配置（可选）
├── settings.json           # 默认设置（可选）
├── templates/              # 模板文件（可选）
├── scripts/                # 辅助脚本（可选）
└── docs/                   # 文档（推荐）
```

### plugin.json 格式

```json
{
  "name": "my-plugin",
  "description": "我的第一个 Claude Code 插件",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "repository": "https://github.com/user/my-plugin",
  "license": "MIT",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

### Agent 文件格式

```markdown
---
name: code-reviewer
description: 代码审查专家，当用户要求"审查代码"时触发
model: sonnet
tools: ["Read", "Grep", "Glob"]
---

# Code Reviewer Agent

你是一位代码审查专家，专注于...
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 唯一标识符 |
| `description` | ✅ | 触发短语，Claude 用于匹配 |
| `model` | ❌ | AI 模型：sonnet/haiku/opus |
| `tools` | ❌ | 允许使用的工具列表 |

---

## 3. 高级配置

### 用户可配置选项 (userConfig)

> [!note] 版本要求：v2.1.83+

插件可以声明用户可配置的选项，敏感信息存储在系统密钥链：

```json
{
  "userConfig": {
    "apiKey": {
      "description": "API 密钥",
      "sensitive": true
    },
    "region": {
      "description": "部署区域",
      "default": "us-east-1"
    }
  }
}
```

> [!warning] 安全变化：不要把 `${user_config.*}` 拼进 shell 命令
> 插件以 shell 形式使用 `headersHelper:${user_config.*}`（在命令字符串里直接引用用户配置）会被 Claude Code 拒绝，这是针对 shell 注入的安全修复（v2.1.224+）。读取 `userConfig` 敏感值时应通过环境变量或对象形式传递，不要拼进命令字符串。详见 §6。

### 持久化数据目录

> [!note] 版本要求：v2.1.78+

通过 `${CLAUDE_PLUGIN_DATA}` 环境变量访问插件专属数据目录：

```json
{
  "hooks": {
    "PostToolUse": [{
      "command": "node ${CLAUDE_PLUGIN_DATA}/track-usage.js"
    }]
  }
}
```

**特点**：
- 目录在插件安装时自动创建
- 每个插件有独立的数据目录
- 数据在会话间持久保存
- 插件卸载时数据会被删除

### 内联插件定义

> [!note] 版本要求：v2.1.80+

可以在配置文件中直接定义插件，无需单独的仓库：

```json
{
  "pluginMarketplaces": [{
    "name": "inline-tools",
    "source": "settings",
    "plugins": [{
      "name": "quick-lint",
      "source": "./local-plugins/quick-lint"
    }]
  }]
}
```

### 插件默认设置

插件可通过 `settings.json` 提供默认配置：

```json
{
  "agent": "agents/specialist-1.md"
}
```

用户可在**用户级**配置中覆盖这些设置。

> [!warning] 行为变化：`pluginConfigs` 不再从项目级 settings 读取（v2.1.207+）
> 插件配置项（`pluginConfigs`）不再从项目级 `.claude/settings.json` 读取。项目层配置无法再直接注入或覆盖插件 config；需要时请在用户级 settings 或插件声明的默认配置中设置。

### LSP 服务器配置

插件可包含 LSP 支持，提供实时代码智能。

**配置位置**：`.lsp.json` 文件或 `plugin.json` 中的 `lsp` 字段

**字段说明**：

| 字段 | 必需 | 说明 |
|------|------|------|
| `command` | ✅ | LSP 服务器二进制文件 |
| `extensionToLanguage` | ✅ | 文件扩展名到语言 ID 的映射 |
| `args` | ❌ | 命令行参数 |
| `transport` | ❌ | 通信方式：`stdio`（默认）或 `socket` |
| `env` | ❌ | 环境变量 |

**常用语言配置**：

```json
// Python (pyright)
{
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": { ".py": "python" }
  }
}

// TypeScript
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    }
  }
}

// Go (gopls)
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

**LSP 功能**：
- 即时诊断 - 编辑后立即显示错误和警告
- 代码导航 - 跳转到定义、查找引用
- 悬停信息 - 显示类型签名和文档
- 符号列表 - 浏览文件或工作区符号

---

## 4. 安装和使用插件

### 安装方法

**从插件市场安装**：
```bash
claude plugin install code-review@anthropics/skills
```

**从本地路径安装**：
```bash
claude plugin install /path/to/my-plugin
```

**从 Git 仓库安装**：
```bash
claude plugin install https://github.com/user/plugin-repo
```

**从归档安装（archive，v2.1.224+）**：
```bash
claude plugin install https://example.com/my-plugin.zip
```

可选 SHA-256 固定，安装前校验归档完整性：
```bash
claude plugin install https://example.com/my-plugin.zip --sha256 <64位十六进制摘要>
```

**运行时加载（开发测试）**：
```bash
claude --plugin-dir ./my-plugin
```

> [!tip] 大白话
> 装插件有四种姿势：市场（应用商店式）、本地路径（直接指文件夹）、Git 仓库（给仓库地址）、归档 zip（给下载链接）。2026 年新增的 archive 方式支持配一个 SHA-256 指纹——安装前先验指纹，防止下载到的包被调包。

### 插件管理命令

| 命令 | 说明 |
|------|------|
| `claude plugin list` | 列出已安装的插件 |
| `claude plugin install <name>` | 安装插件 |
| `claude plugin uninstall <name>` | 卸载插件 |
| `claude plugin enable <name>` | 启用插件 |
| `claude plugin disable <name>` | 禁用插件 |
| `claude plugin update <name>` | 更新插件 |
| `claude plugin validate` | 验证插件配置 |

### 在 Claude Code 中使用

```bash
/agents          # 查看已加载的 Agent
/my-command      # 使用自定义命令
/mcp             # 查看 MCP 工具
```

---

## 5. 创建自己的插件

### 快速开始

**步骤1：创建目录**
```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/agents
cd my-plugin
```

**步骤2：编写 plugin.json**
```json
{
  "name": "my-first-plugin",
  "description": "我的第一个插件",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

**步骤3：创建 Agent**

`agents/code-helper.md`：
```markdown
---
name: code-helper
description: 代码助手
model: sonnet
---

# Code Helper

你是一位友好的代码助手，专注于：
- 解释代码逻辑
- 帮助编写清晰的代码
```

**步骤4：测试**
```bash
claude plugin validate
claude --plugin-dir .
/agents
```

### 高级功能

**自定义命令** - `commands/deploy.md`：
```markdown
---
name: deploy
description: 部署应用到生产环境
---

# 部署命令
1. 运行测试
2. 构建项目
3. 部署到服务器
```

**MCP 服务器** - `.mcp.json`：
```json
{
  "my-api": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/mcp-server.js"],
    "env": { "API_KEY": "${API_KEY}" }
  }
}
```

**事件钩子** - `hooks/hooks.json`：
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
    }]
  }]
}
```

### 开发最佳实践

| 实践 | 说明 |
|------|------|
| **命名规范** | 小写字母+连字符：`my-plugin` |
| **版本管理** | 使用语义化版本：`1.0.0` |
| **权限最小化** | Agent 只给需要的工具权限 |
| **触发词设计** | 提供中英文触发词，明确不模糊 |
| **文档完善** | 包含 README、安装说明、示例 |

---

## 6. 企业管理与安全

### 企业管理设置

管理员可通过托管设置控制插件行为：

| 设置 | 说明 |
|------|------|
| `enabledPlugins` | 默认启用的插件白名单 |
| `deniedPlugins` | 禁止安装的插件黑名单 |
| `extraKnownMarketplaces` | 添加额外的市场源 |
| `strictKnownMarketplaces` | 限制用户可添加的市场 |
| `blockedMarketplaces` | 屏蔽指定的市场源（支持 owner 通配符） |

**市场限制示例**：
```json
{
  "strictKnownMarketplaces": [
    "my-org/*",
    "github.com/trusted-vendor/*"
  ],
  "blockedMarketplaces": [
    "untrusted-org/*"
  ]
}
```

> [!note] owner 通配符
> `strictKnownMarketplaces` 与 `blockedMarketplaces` 都支持 **owner 通配符**（`"owner/*"` 匹配该 owner 下的所有市场/插件），方便按组织统一管控。

> [!warning] 严格模式
> 启用后，用户只能安装白名单市场中的插件。

### 安装同意（来源授权）

> [!note] 行为变化（v2.1.207+）
> 当外部插件**只由项目设置启用**时，每个加载路径都会要求**明确的安装同意**，防止插件「自批准」绕过审核。

实际影响：
- 只配置在项目级 `.claude/settings.json` 的插件，启动时会逐条请求确认。
- 用户确认后该路径才会被加载；静默启用会失败。
- 用户级已明确安装/同意的插件不受影响。

### 插件安全限制

插件子 Agent 在受限沙箱中运行，以下字段**禁止使用**：

| 禁止字段 | 原因 |
|----------|------|
| `hooks` | 子 Agent 不能注册事件处理器 |
| `mcpServers` | 子 Agent 不能配置 MCP 服务器 |
| `permissionMode` | 子 Agent 不能覆盖权限模型 |

> [!warning] Shell 注入修复（v2.1.224+）
> 插件以 shell 形式使用 `headersHelper:${user_config.*}` 会被拒绝执行。不要把 `${user_config.*}` 拼进 shell 命令字符串；敏感配置通过环境变量或对象形式传入（详见 §3 userConfig）。

> [!tip] 大白话
> 这几个安全收紧动作，核心是「不给插件自说自话的权限」：项目配置里引用的外部插件要逐条问你同不同意；`pluginConfigs` 不再认项目级配置；敏感值不许拼进 shell 命令。装插件前多看一眼来源，比事后排查省事。

---

## 7. 常见问题

**Q: 插件和 Agent 有什么区别？**

A:
- **插件**是容器，组织多个相关功能
- **Agent**是执行单元，有特定行为和指令
- 一个插件可以包含多个 Agent

**Q: 插件会一直运行吗？**

A: 不会。插件根据需要加载：
- Agent 只在被触发时启动
- 插件 MCP 在插件启用时运行
- 禁用插件后，相关资源自动释放

**Q: 如何分享我的插件？**

A:
1. 将插件发布到 Git 仓库
2. 用户通过 URL 安装：`claude plugin install https://github.com/user/plugin`
3. 或提交到官方插件市场

**Q: 插件安全吗？**

A: 插件可以访问你允许的工具权限和环境变量。建议：
- 只安装可信来源的插件
- 从归档（archive）安装时校验 SHA-256 摘要
- 审查 `plugin.json` 和 Agent 配置
- 使用最小权限原则
- 留意安装同意提示：外部插件只由项目设置启用时会逐条请求确认，不要盲目点「允许」

---

## 8. 故障排除

| 问题 | 检查项 |
|------|--------|
| **插件无法安装** | Claude Code 版本兼容性、`plugin.json` 语法、网络连接、文件权限 |
| **组件未加载** | 路径匹配、文件权限 `chmod +x scripts/`、语法检查、`/plugin debug` |
| **MCP 连接失败** | 环境变量、MCP 服务器状态、`/mcp test`、配置文件 |
| **命令不可用** | `/plugin list --installed`、插件状态、重启 Claude Code、命名冲突 |
| **钩子执行问题** | 执行权限、钩子语法、事件名称、日志检查 |

---

## 参考资料

### 官方资源
- [Claude Code 官方文档](https://docs.anthropic.com/claude-code) - 完整技术文档
- [Claude Code Changelog](https://code.claude.com/docs/en/changelog) - 版本变更记录（插件安全修复见 v2.1.207 / v2.1.224）
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) - 官方插件仓库

### 社区资源
- [Claude HowTo - 插件系统](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - 可视化教程和示例
- [Claude HowTo 仓库](https://github.com/luongnv89/claude-howto) - 从基础到高级的完整指南

### 相关文档
- [[Claude MCP 使用指南]] - MCP 协议详解
- [[Claude Code Subagents 完整指南]] - Agent 系统详解

---

## 更新记录

- **2026-08-10**：同步 2026-07/08 插件系统安全与来源变化（SB-19）。
  - 安全（breaking）：shell 形式 `headersHelper:${user_config.*}` 被拒绝（注入修复）；`pluginConfigs` 不再从项目级 `.claude/settings.json` 读取。
  - 安装来源：新增 `archive`（HTTPS zip + 可选 SHA-256 固定）。
  - 安装同意：外部插件只由项目设置启用时，每个加载路径要求明确安装同意。
  - 企业管理：补充 `blockedMarketplaces` 与 owner 通配符说明。
  - 核心概念补充 `[!tip] 大白话`（§1/§4/§6）。
