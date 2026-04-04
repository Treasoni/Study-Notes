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
| **HTTP** | 云端服务、REST API | **推荐**，请求/响应模式，支持 OAuth |
| **SSE** | 云端服务、OAuth | ⚠️ **已废弃**，请使用 HTTP 替代 |
| **WebSocket** | 实时通信 | 持久连接，双向数据 |

> [!warning] SSE 传输已废弃
> Server-Sent Events (SSE) 传输已被废弃，推荐使用 HTTP 传输替代。HTTP 传输提供了更好的兼容性和功能支持。

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

> [!tip] Windows 特别注意事项
> 在原生 Windows（非 WSL）上，使用 `cmd /c` 来执行 npx 命令：
> ```bash
> claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
> ```

### OAuth 2.0 认证

Claude Code 支持 OAuth 2.0 进行 MCP 服务器认证。当连接到启用 OAuth 的服务器时，Claude Code 会自动处理整个认证流程。

```bash
# 连接到启用 OAuth 的 MCP 服务器（交互式流程）
claude mcp add --transport http my-service https://my-service.example.com/mcp

# 预配置 OAuth 凭据（非交互式设置）
claude mcp add --transport http my-service https://my-service.example.com/mcp \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --callback-port 8080
```

**OAuth 功能表**：

| 功能 | 描述 |
|------|------|
| **交互式 OAuth** | 使用 `/mcp` 触发浏览器 OAuth 流程 |
| **预配置 OAuth 客户端** | 内置常用服务（Notion、Stripe 等）的 OAuth 客户端（v2.1.30+） |
| **预配置凭据** | `--client-id`、`--client-secret`、`--callback-port` 标志用于自动设置 |
| **令牌存储** | 令牌安全存储在系统密钥链中 |
| **Step-up 认证** | 支持特权操作的升级认证 |
| **发现缓存** | OAuth 发现元数据缓存以加快重连速度 |

#### 覆盖 OAuth 元数据发现

如果 MCP 服务器在标准 OAuth 元数据端点（`/.well-known/oauth-authorization-server`）返回错误，但暴露了可用的 OIDC 端点，可以指定 OAuth 元数据 URL：

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

> [!info] 📚 来源
> - [Claude Code 官方文档 - OAuth](https://docs.anthropic.com/en/docs/claude-code/mcp#oauth-authentication) - OAuth 配置说明

> [!tip] 旧命令格式
> 如果您看到使用 `--command` 的旧示例，请使用新的 `--transport` 语法：
> ```bash
> # 旧格式（已废弃）
> claude mcp add <name> --command <cmd> --args [...]
>
> # 新格式（推荐）
> claude mcp add --transport stdio <name> -- <cmd> [...]
> ```

> [!info] 📚 来源
> - [Claude Code 官方文档 - MCP 安装](https://docs.anthropic.com/en/docs/claude-code/mcp#installing-mcp-servers) - 传输方式说明

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

插件可以捆绑 MCP 服务器，在启用插件时自动提供工具和集成。

### 插件 MCP 服务器的工作原理

- 插件在插件根目录的 `.mcp.json` 中或在 `plugin.json` 中内联定义 MCP 服务器
- 启用插件时，其 MCP 服务器会自动启动
- 插件 MCP 工具与手动配置的 MCP 工具一起出现
- 插件服务器通过插件安装进行管理（不是 `/mcp` 命令）

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

> [!info] 📚 来源
> - [Claude Code 官方文档 - MCP 安装范围](https://docs.anthropic.com/en/docs/claude-code/mcp#mcp-installation-scopes) - 范围层级与优先级

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

#### 添加文件系统 MCP 服务器（详细步骤）

文件系统 MCP 服务器允许 Claude Code 访问您指定的目录，进行读取、写入、搜索等操作。

**🎯 比喻**：就像给 Claude Code 配一把"钥匙"，让它能进入您指定的文件夹工作。

**方法一：使用 CLI 命令添加（推荐）**

```bash
# 基本语法
claude mcp add --transport stdio <名称> --scope <范围> -- npx -y @modelcontextprotocol/server-filesystem <目录1> <目录2> ...

# 实际示例：添加用户范围的文件系统访问
claude mcp add --transport stdio filesystem --scope user -- npx -y @modelcontextprotocol/server-filesystem ~/Desktop ~/Downloads

# 项目范围示例：仅当前项目可用
claude mcp add --transport stdio filesystem --scope project -- npx -y @modelcontextprotocol/server-filesystem ./src ./docs

# 本地范围示例（默认，仅当前项目且私有）
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem /Users/username/Desktop /Users/username/Downloads
```

**命令解析**：

| 部分 | 说明 |
|------|------|
| `--transport stdio` | 使用标准输入输出通信（本地服务器） |
| `filesystem` | 服务器名称（可自定义） |
| `--scope user` | 范围：user（全局）/ project（项目）/ local（本地） |
| `--` | 分隔符，后面是实际的启动命令 |
| `npx -y` | 使用 npx 运行，-y 自动确认 |
| `@modelcontextprotocol/server-filesystem` | 官方文件系统 MCP 包 |
| `~/Desktop ~/Downloads` | 允许访问的目录路径 |

**方法二：使用 JSON 配置添加**

如果您有现成的 JSON 配置，可以使用 `add-json` 命令：

```bash
# 基本语法
claude mcp add-json <名称> '<json配置>'

# 添加 stdio 类型服务器（文件系统）
claude mcp add-json filesystem --scope user '{"type":"stdio","command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","/Users/username/Desktop","/Users/username/Downloads"]}'

# 添加 HTTP 类型服务器
claude mcp add-json weather-api --scope user '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer your-token"}}'
```

> [!tip] JSON 格式说明
> - `type`: 传输类型，可选 `stdio`、`http`、`sse`
> - `command`: stdio 类型的可执行命令
> - `args`: 命令行参数数组
> - `url`: http/sse 类型的服务器地址
> - `headers`: HTTP 请求头（可选）
> - `env`: 环境变量（可选）

**验证安装**：

```bash
# 方法 1：CLI 查看
claude mcp list

# 方法 2：在 Claude Code 中查看
/mcp

# 方法 3：获取详细信息
claude mcp get filesystem
```

**使用示例**：

```bash
# 在 Claude Code 中使用文件系统 MCP
> "读取 Desktop 下的 README.md 文件"
> "在 Downloads 文件夹中搜索包含 'report' 的文件"
> "创建一个新文件 test.txt 在 Desktop 目录"
```

> [!warning] 安全提示
> - 仅添加您信任的目录
> - 避免添加包含敏感信息的目录（如 ~/.ssh, ~/.config 等）
> - 使用最小权限原则，只添加必要的目录

> [!info] 📚 来源
> - [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp) - 安装与配置
> - [MCP GitHub - server-filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - 源码与文档

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

### MCP Elicitation（交互式输入）

MCP 服务器可以通过交互式对话框请求用户的结构化输入（v2.1.49+）。这允许 MCP 服务器在工作流程中请求额外信息——例如，提示确认、从选项列表中选择或填写必填字段——为 MCP 服务器交互增加了交互性。

### 工具描述和指令上限

从 v2.1.84 开始，Claude Code 对每个 MCP 服务器的工具描述和指令实施 **2 KB 上限**。这可以防止单个服务器消耗过多上下文，减少上下文膨胀，保持交互高效。

> [!info] 📚 来源
> - [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp) - 高级功能说明

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

### MCP 提示（作为斜杠命令）

MCP 服务器可以公开提示，这些提示在 Claude Code 中作为斜杠命令可用。提示使用以下命名规范：

```
/mcp__<server>__<prompt>
```

例如，如果名�� `github` 的服务器公开了一个名为 `review` 的提示，您可以这样调用：

```bash
/mcp__github__review
```

> [!info] 📚 来源
> - [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp#mcp-prompts-as-slash-commands) - 斜杠命令格式

---

## 8. Subagent-Scoped MCP

MCP 服务器可以在 agent frontmatter 中使用 `mcpServers:` 键内联定义，将其范围限制为特定的 subagent，而不是整个项目。这对于需要访问特定 MCP 服务器的 agent 非常有用，而工作流程中的其他 agent 不需要该服务器。

```yaml
---
mcpServers:
  my-tool:
    type: http
    url: https://my-tool.example.com/mcp
---

You are an agent with access to my-tool for specialized operations.
```

Subagent-scoped MCP 服务器仅在该 agent 的执行上下文中可用，不会与父 agent 或兄弟 agent 共享。

> [!info] 📚 来源
> - [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp#subagent-scoped-mcp) - Subagent 配置说明

---

## 9. 托管 MCP 配置

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

## 10. 从 Claude Desktop 导入

如果您已在 Claude Desktop 中配置了 MCP 服务器，可以导入它们：

```bash
# 导入 Claude Desktop MCP 配置
claude mcp import-from-claude-desktop
```

---

## 11. 将 Claude Code 用作 MCP 服务器

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

## 12. 故障排查

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

# 从 JSON 配置添加
claude mcp add-json <名称> --scope user|project|local '<json配置>'

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

## 最佳实践

### 安全考虑

#### ✅ 应该做的

- 使用环境变量存储所有凭据
- 定期轮换令牌和 API 密钥（建议每月）
- 尽可能使用只读令牌
- 将 MCP 服务器访问范围限制为最低所需权限
- 监控 MCP 服务器使用情况和访问日志
- 可用时使用 OAuth ���行外部服务认证
- 对 MCP 请求实施速率限制
- 生产使用前测试 MCP 连接
- 记录所有活动的 MCP 连接
- 保持 MCP 服务器包更新

#### ❌ 不应该做的

- 不要在配置文件中硬编码凭据
- 不要将令牌或密钥提交到 git
- 不要在团队聊天或电子邮件中共享令牌
- 不要在团队项目中使用个人令牌
- 不要授予不必要的权限
- 不要忽略身份验证错误
- 不要公开暴露 MCP 端点
- 不要以 root/管理员权限运行 MCP 服务器
- 不要在日志中缓存敏感数据
- 不要禁用身份验证机制

### 配置最佳实践

1. **版本控制**：将 `.mcp.json` 保留在 git 中，但使用环境变量存储密钥
2. **最小权限**：为每个 MCP 服务器授予所需的最低权限
3. **隔离**：尽可能在不同的进程中运行不同的 MCP 服务器
4. **监控**：记录所有 MCP 请求和错误以进行审计跟踪
5. **测试**：在部署到生产环境之前测试所有 MCP 配置

### 性能技巧

- 在应用层缓存频繁访问的数据
- 使用特定的 MCP 查询以减少数据传输
- 监控 MCP 操作的响应时间
- 考虑对外部 API 进行速率限制
- 执行多个操作时使用批处理

> [!info] 📚 来源
> - [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp#best-practices) - 最佳实践指南

---

## 参考资料

### 官方资源
- [Claude Code MCP 官方文档](https://docs.anthropic.com/en/docs/claude-code/mcp) - 完整技术文档
- [MCP 协议规范](https://modelcontextprotocol.io) - 协议标准说明
- [MCP GitHub 组织](https://github.com/modelcontextprotocol) - 官方服务器实现
- [claude-howto MCP 指南](https://github.com/luongnv89/claude-howto/blob/main/05-mcp/README.md) - 社区维护的详细指南

### 社区资源
- [Claude Code 添加 MCP 服务器完整指南](https://www.tinyash.com/blog/claude-code-mcp/) - 中文教程
- [开发者必看：三大 CLI 工具 MCP 配置详解](http://juejin.im/entry/7590593682584502335) - 掘金文章

---

## 相关文档

[[01-基础概念/人工智能重要的六大概念体系]] | [[04-高级应用/Claude Subagent 使用指南]] | [[02-工具使用/如何使用Claude code]]
