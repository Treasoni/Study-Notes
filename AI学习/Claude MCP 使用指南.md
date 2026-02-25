---
tags: [ai, 进阶应用]
---

# Claude MCP 使用指南

> [!info] 概述
> **MCP (Model Context Protocol) 是 Claude Code 与外部工具通信的标准化开源协议** - 就像 USB 接口一样，所有工具都能用同一个接口连接。通过 MCP，Claude 可以访问文件系统、数据库、API 等各种外部资源。

**官方资源**：
- [MCP 官方文档](https://code.claude.com/docs/zh-CN/mcp)
- [MCP 协议规范](https://modelcontextprotocol.io)

**MCP 能力示例**：
- 从问题跟踪器实现功能："添加 JIRA 问题 ENG-4521 中描述的功能，并在 GitHub 上创建 PR"
- 分析监控数据："检查 Sentry 和 Statsig 以检查 ENG-4521 中描述的功能的使用情况"
- 查询数据库："根据我们的 PostgreSQL 数据库，找到使用功能 ENG-4521 的 10 个随机用户的电子邮件"
- 集成设计："根据在 Slack 中发布的新 Figma 设计更新我们的标准电子邮件模板"
- 自动化工作流："创建 Gmail 草稿，邀请这 10 个用户参加关于新功能的反馈会议"

---

## 1. MCP 简介

### 什么是 MCP

**MCP** (Model Context Protocol) 是一个用于 AI 工具集成的标准化开源协议。

**核心价值**：
- 统一工具接口格式
- 实现工具可复用、跨语言
- 支持分布式部署
- 降低集成复杂度

### MCP 传输方式

| 传输方式 | 适用场景 | 特点 |
|----------|----------|------|
| **stdio** | 本地工具、NPM 包 | 进程间通信，低延迟 |
| **SSE** | 云端服务、OAuth | 自动授权，令牌刷新 |
| **HTTP** | REST API | 请求/响应模式 |
| **WebSocket** | 实时通信 | 持久连接，双向数据 |

---

## 2. 安装 MCP 服务器

MCP 服务器支持三种传输方式，根据您的需求选择最适合的配置方式。

### 选项 1：远程 HTTP 服务器（推荐）

HTTP 服务器是连接到远程 MCP 服务器的推荐选项，这是云服务最广泛支持的传输方式。

```bash
# 基本语法
claude mcp add --transport http <name> <url>

# 真实示例：连接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 带有 Bearer 令牌的示例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 选项 2：远程 SSE 服务器

```bash
# 基本语法
claude mcp add --transport sse <name> <url>

# 真实示例：连接到 Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# 带有身份验证标头的示例
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### 选项 3：本地 stdio 服务器

Stdio 服务器作为您机器上的本地进程运行，非常适合需要直接系统访问或自定义脚本的工具。

```bash
# 基本语法
claude mcp add [options] <name> -- <command> [args...]

# 真实示例：添加 Airtable 服务器
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server

# 使用环境变量示例
claude mcp add --transport stdio --env DATABASE_URL=postgresql://user:pass@localhost/db db \
  -- npx -y @modelcontextprotocol/server-postgres
```

> [!tip] 旧命令格式
> 如果您看到使用 `--command` 的旧示例，请使用新的 `--transport` 语法：
> ```bash
> # 旧格式（已废弃）
> claude mcp add <name> --command <cmd> --args [...]
>
> # 新格式（推荐）
> claude mcp add --transport stdio <name> -- <cmd> [...]
> ```

---

## 3. 管理服务器

配置后，您可以使用这些命令管理您的 MCP 服务器。

### CLI 命令

```bash
# 列出所有配置的服务器（仅全局）
claude mcp list

# 获取特定服务器的详细信息
claude mcp get github

# 删除服务器
claude mcp remove github

# 重置项目级服务器的批准选择
claude mcp reset-project-choices
```

### 在 Claude Code 中检查

```bash
# 在 Claude Code 中输入（显示所有可用的 MCP，包括项目级）
/mcp
```

> [!warning] 重要区别
> - `/mcp`：显示当前上下文中所有可用的 MCP servers（包括项目级配置、插件配置）
> - `claude mcp list`：仅显示全局 MCP servers，项目级 `.mcp.json` 配置不会出现在此列表中

---

## 4. 插件提供的 MCP 服务器

> [!info] 什么是插件 MCP？
> **插件 MCP = 插件自带的工具包**。想象你安装了一个"数据库插件"（plugin），这个插件自动带了一个"数据库查询工具"（MCP Server）。你启用插件时，工具自动可用；禁用插件时，工具自动消失。
>
> **对比手动 MCP**：
> - **手动 MCP**：你自己买菜、自己做饭（自己配置、自己管理）
> - **插件 MCP**：点外卖套餐（插件自带，启用即用）

### 插件 MCP 服务器的工作原理

- 插件在插件根目录的 `.mcp.json` 中或在 `plugin.json` 中内联定义 MCP 服务器
- 启用插件时，其 MCP 服务器会自动启动
- 插件 MCP 工具与手动配置的 MCP 工具一起出现
- 插件服务器通过插件安装进行管理（不是 `/mcp` 命令）

### 插件 MCP vs 手动 MCP 对比

| 特性 | 插件 MCP 服务器 | 手动 MCP 服务器 |
|------|----------------|----------------|
| **启用时机** | 插件启用时自动启动，插件禁用时自动停止 | 手动添加后持续运行，直到手动删除 |
| **管理方式** | 通过插件安装/启用/禁用管理 | 通过 `claude mcp add/remove` 命令管理 |
| **配置位置** | 插件目录的 `.mcp.json` 或 `plugin.json` | 项目级 `.mcp.json` 或全局 `~/.claude.json` |
| **可见性** | 在 `/mcp` 列表中带有"来自插件"标记 | 在 `/mcp` 列表中正常显示 |
| **更新方式** | 更新插件后自动更新 | 需要手动修改配置 |
| **适用场景** | 分发给团队使用的工具集成 | 个人开发环境配置 |

### 配置方式

**在插件根目录的 `.mcp.json` 中**：

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

**在 `plugin.json` 中内联**：

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

### 插件 MCP 功能

- **自动生命周期**：服务器在插件启用时启动，需要重启 Claude Code 以应用更改
- **环境变量**：使用 `${CLAUDE_PLUGIN_ROOT}` 表示插件相对路径
- **用户环境访问**：访问与手动配置的服务器相同的环境变量
- **多种传输类型**：支持 stdio、SSE 和 HTTP 传输

### 查看插件 MCP 服务器

```bash
# 在 Claude Code 中，查看所有 MCP 服务器，包括插件服务器
/mcp
```

插件服务器在列表中出现，并带有指示它们来自插件的指示符。

### 常见问题

**Q: 插件 MCP 服务器是一直运行的吗？**

A: 不是。插件 MCP 服务器只在插件启用时运行：
- 启用插件 → MCP 服务器自动启动
- 禁用插件 → MCP 服务器自动停止
- 重启 Claude Code → 应用插件状态变化

**Q: 我应该使用插件 MCP 还是手动 MCP？**

A:
- **使用插件 MCP**：当工具需要与团队共享、或作为插件功能的一部分时
- **使用手动 MCP**：当工具只用于个人开发环境、或需要灵活配置时

**Q: 插件 MCP 和手动 MCP 可以共存吗？**

A: 可以。它们会在 `/mcp` 列表中一起显示，插件 MCP 会有特殊标记。

---

## 5. MCP 安装范围

MCP 服务器可以在三个不同的范围级别进行配置，每个级别都有不同的用途。

### 本地范围（Local）

**配置位置**：`~/.claude.json`

**特点**：
- 仅在当前项目目录中工作时可访问
- 对您保持私密
- 适合个人开发服务器、实验配置或包含敏感凭据的服务器

```bash
# 添加本地范围的服务器（默认）
claude mcp add --transport http stripe https://mcp.stripe.com

# 显式指定本地范围
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### 项目范围（Project）

**配置位置**：`项目根目录/.mcp.json`

**特点**：
- 团队共享，可检入版本控制
- 所有团队成员都可以访问相同的 MCP 工具
- 出于安全原因，使用前需要批准

```bash
# 添加项目范围的服务器
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

生成的 `.mcp.json` 文件格式：

```json
{
  "mcpServers": {
    "shared-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

### 用户范围（User）

**配置位置**：`~/.claude.json`

**特点**：
- 跨项目可访问
- 在您机器上的所有项目中可用
- 适合个人实用工具、开发工具或经常使用的服务

```bash
# 添加用户服务器
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### 范围优先级

当具有相同名称的服务器存在于多个范围时，系统按以下优先级解决冲突：

**Local（本地） > Project（项目） > User（用户）**

此设计确保个人配置可以在需要时覆盖共享配置。

### 选择正确的范围

| 场景 | 推荐范围 |
|------|----------|
| 个人服务器、实验配置 | Local |
| 团队共享的服务器、项目特定工具 | Project |
| 跨多个项目的个人实用工具 | User |

### 环境变量扩展

Claude Code 支持 `.mcp.json` 文件中的环境变量扩展。

**支持的语法**：
- `${VAR}` - 扩展为环境变量 `VAR` 的值
- `${VAR:-default}` - 如果设置了 `VAR`，则扩展为 `VAR`，否则使用 `default`

**扩展位置**：
- `command` - 服务器可执行文件路径
- `args` - 命令行参数
- `env` - 传递给服务器的环境变量
- `url` - 对于 HTTP 服务器类型
- `headers` - 对于 HTTP 服务器身份验证

**示例**：

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

---

## 6. 常用 MCP 服务器推荐

### 核心服务器

| 服务器 | 功能 | 传输方式 | 配置 |
|--------|------|----------|------|
| **filesystem** | 文件系统访问 | stdio | `npx -y @modelcontextprotocol/server-filesystem` |
| **postgres** | PostgreSQL 数据库 | stdio | `npx -y @modelcontextprotocol/server-postgres` |
| **git** | Git 操作 | stdio | `npx -y @modelcontextprotocol/server-git` |
| **brave-search** | Brave 搜索 | stdio | `npx -y @modelcontextprotocol/server-brave-search` |
| **github** | GitHub API | HTTP | `https://api.githubcopilot.com/mcp/` |
| **sentry** | 错误监控 | HTTP | `https://mcp.sentry.dev/mcp` |

### 实际示例

#### 使用 Sentry 监控错误

```bash
# 1. 添加 Sentry MCP 服务器
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. 使用 /mcp 对您的 Sentry 帐户进行身份验证
> /mcp

# 3. 调试生产问题
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

#### 连接到 GitHub 进行代码审查

```bash
# 1. 添加 GitHub MCP 服务器
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 2. 在 Claude Code 中，如果需要进行身份验证
> /mcp
# 为 GitHub 选择"身份验证"

# 3. 现在您可以要求 Claude 使用 GitHub
> "Review PR #456 and suggest improvements"
> "Create a new issue for the bug we just found"
> "Show me all open PRs assigned to me"
```

#### 查询 PostgreSQL 数据库

```bash
# 1. 使用您的连接字符串添加数据库服务器
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:password@localhost:5432/analytics"

# 2. 自然地查询您的数据库
> "What's our total revenue this month?"
> "Show me the schema for the orders table"
> "Find customers who haven't made a purchase in 90 days"
```

---

## 7. 高级功能

### 动态工具更新

Claude Code 支持 MCP `list_changed` 通知，允许 MCP 服务器动态更新其可用工具、提示和资源，无需断开连接并重新连接。

### MCP 输出限制

当 MCP 工具产生大量输出时，Claude Code 有助于管理令牌使用：

- **输出警告阈值**：当任何 MCP 工具输出超过 10,000 个令牌时显示警告
- **可配置限制**：使用 `MAX_MCP_OUTPUT_TOKENS` 环境变量调整最大允许的 MCP 输出令牌
- **默认限制**：默认最大值为 25,000 个令牌

```bash
# 为 MCP 工具输出设置更高的限制
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

### MCP 工具搜索

当配置了许多 MCP 服务器时，工具定义可能会消耗大量上下文。MCP 工具搜索通过动态按需加载工具来解决这个问题。

**工作原理**：
1. 当 MCP 工具描述会消耗超过 10% 的上下文窗口时，自动启用工具搜索
2. MCP 工具被延迟而不是预先加载到上下文中
3. Claude 使用搜索工具在需要时发现相关的 MCP 工具
4. 只有 Claude 实际需要的工具才会加载到上下文中

**配置**：

```bash
# 使用自定义 5% 阈值
ENABLE_TOOL_SEARCH=auto:5 claude

# 完全禁用工具搜索
ENABLE_TOOL_SEARCH=false claude

# 始终启用
ENABLE_TOOL_SEARCH=true claude
```

**配置选项**：

| 值 | 行为 |
|---|---|
| `auto` | 当 MCP 工具超过 10% 的上下文时激活（默认） |
| `auto:<N>` | 在自定义阈值激活，其中 `<N>` 是百分比 |
| `true` | 始终启用 |
| `false` | 禁用，所有 MCP 工具预先加载 |

### MCP 资源

MCP 服务器可以公开资源，您可以使用 `@` 提及来引用这些资源，类似于引用文件的方式。

```bash
# 引用 MCP 资源
> "What does @sentry-resource say about the current errors?"
```

### MCP 提示

MCP 服务器可以公开提示，这些提示在 Claude Code 中作为命令可用。

```bash
# 执行 MCP 提示
> /mcp-prompt-name
```

---

## 8. 托管 MCP 配置

对于需要对 MCP 服务器进行集中控制的组织，Claude Code 支持两个配置选项。

### 选项 1：使用 managed-mcp.json 进行独占控制

部署 `managed-mcp.json` 文件时，它对所有 MCP 服务器进行独占控制。用户无法添加、修改或使用除此文件中定义的 MCP 服务器之外的任何 MCP 服务器。

**系统级配置文件位置**：
- **macOS**：`/Library/Application Support/ClaudeCode/managed-mcp.json`
- **Linux 和 WSL**：`/etc/claude-code/managed-mcp.json`
- **Windows**：`C:\Program Files\ClaudeCode\managed-mcp.json`

**配置示例**：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### 选项 2：使用允许列表/拒绝列表进行基于策略的控制

允许用户配置自己的 MCP 服务器，同时对允许的服务器强制限制。

**限制方式**：
1. **按服务器名称** (`serverName`)：匹配服务器的配置名称
2. **按命令** (`serverCommand`)：匹配用于启动 stdio 服务器的确切命令和参数
3. **按 URL 模式** (`serverUrl`)：匹配带有通配符支持的远程服务器 URL

**配置示例**：

```json
{
  "allowedMcpServers": [
    // 按服务器名称允许
    { "serverName": "github" },
    { "serverName": "sentry" },

    // 按确切命令允许（对于 stdio 服务器）
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },

    // 按 URL 模式允许（对于远程服务器）
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // 按服务器名称阻止
    { "serverName": "dangerous-server" },

    // 按确切命令阻止
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // 按 URL 模式阻止
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

**重要说明**：
- 拒绝列表具有绝对优先级
- 每个条目必须恰好具有 `serverName`、`serverCommand` 或 `serverUrl` 之一
- 当允许列表包含 `serverCommand` 条目时，stdio 服务器必须匹配其中一个命令
- 当允许列表包含 `serverUrl` 条目时，远程服务器必须匹配其中一个 URL 模式

---

## 9. 从 Claude Desktop 导入

如果您已在 Claude Desktop 中配置了 MCP 服务器，可以导入它们：

```bash
# 导入 Claude Desktop MCP 配置
claude mcp import-from-claude-desktop
```

---

## 10. 将 Claude Code 用作 MCP 服务器

您可以将 Claude Code 本身用作 MCP 服务器，其他应用程序可以连接到它。

```bash
# 启动 Claude 作为 stdio MCP 服务器
claude mcp serve
```

在 Claude Desktop 中使用的配置示例：

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

---

## 11. 故障排查

### 常见错误

**配置文件格式错误**：
- ❌ JSON 语法不正确
- ❌ 路径使用反斜杠（Windows）
- ❌ 环境变量硬编码

**服务器启动失败**：
- ❌ npx 未安装
- ❌ Node.js 版本不兼容
- ❌ 端口被占用

**OAuth 授权问题**：
- ❌ 浏览器未打开
- ❌ 令牌过期
- ❌ 权限不足

**不兼容的身份验证服务器**：
- ❌ 错误："不支持动态客户端注册"
- **解决方案**：通过服务器的开发者门户注册 OAuth 应用，然后提供预配置的凭据

### 调试方法

```bash
# 1. 调试模式启动
claude --debug

# 2. 查看状态
/mcp

# 3. 手动测试服务器
npx -y @modelcontextprotocol/server-filesystem /test/path
```

### 日志位置

- **macOS**：`~/Library/Logs/ClaudeCode/`
- **Linux**：`~/.config/ClaudeCode/logs/`
- **Windows**：`%APPDATA%\ClaudeCode\logs\`

### Windows 特别注意事项

- 使用正斜杠 `/` 或双反斜杠 `\\` 在路径中
- 为 Python 设置 `PYTHONUNBUFFERED=1`
- 使用 `npx -y` 避免 Y/n 交互提示

---

## 12. CLI 命令速查

```bash
# 添加服务器
claude mcp add --transport http <name> <url>
claude mcp add --transport sse <name> <url>
claude mcp add --transport stdio <name> -- <command> [args...]

# 指定范围
claude mcp add --transport http <name> --scope local|project|user <url>

# 设置环境变量
claude mcp add --transport stdio <name> --env KEY=value -- <command>

# 添加请求头
claude mcp add --transport http <name> <url> --header "X-API-Key: key"

# 管理服务器
claude mcp list
claude mcp get <name>
claude mcp remove <name>
claude mcp reset-project-choices

# 导入
claude mcp import-from-claude-desktop

# 作为服务器运行
claude mcp serve

# 在 Claude Code 中
/mcp
```

---

## 常见问题

**Q: stdio 和 SSE 有什么区别？**

A:
- **stdio**：本地进程，Claude Code 启动和管理服务器
- **SSE**：远程服务，通过 URL 连接，支持 OAuth

**Q: 为什么项目级 .mcp.json 中的配置不出现在 `claude mcp list` 中？**

A: 这是正常行为。`claude mcp list` 仅显示全局 MCP servers。
- 项目级配置（`.mcp.json`）只在项目上下文中生效
- 要查看项目级 MCP，在 Claude Code 中输入 `/mcp`
- 要让配置在所有项目中可用，将其添加到用户范围配置

**Q: 如何在多个项目间共享 MCP 配置？**

A: 将配置放在用户范围（`~/.claude.json`）或使用项目范围（`.mcp.json`）并检入版本控制。

**Q: OAuth 服务需要做什么？**

A: 添加 SSE 类型的 URL 配置，首次使用时 Claude Code 会自动打开浏览器完成 OAuth 授权。

---

## 相关文档

[[Prompt, Agent, MCP 是什么]] | [[Claude Subagent 使用指南]] | [[如何使用Claude code]]
