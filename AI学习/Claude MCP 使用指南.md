---
tags: [ai]
---

# MCP 使用指南

> [!info] 概述
> **MCP 是 Claude Code 与外部工具通信的标准协议** - 就像 USB 接口一样，所有工具都能用同一个接口连接。通过 MCP，Claude 可以访问文件系统、数据库、API 等各种外部资源。

## 核心概念 💡

### 什么是 MCP

**是什么**：Model Context Protocol，标准化工具通信协议

**为什么需要**：
- 统一工具接口格式
- 实现工具可复用、跨语言
- 支持分布式部署

**配置文件位置**：
| 级别 | 位置 |
|------|------|
| 项目级 | `.mcp.json` |
| 全局级 | `~/.claude/claude_desktop_config.json` |
| 插件级 | `插件根目录/.mcp.json` |

### MCP 服务器类型

| 类型 | 适用场景 | 特点 |
|------|----------|------|
| **stdio** | 本地工具、NPM 包 | 进程间通信，低延迟 |
| **SSE** | 云端服务、OAuth | 自动授权，令牌刷新 |
| **HTTP** | REST API | 请求/响应模式 |
| **WebSocket** | 实时通信 | 持久连接，双向数据 |

## 操作步骤

### 步骤 1：安装 MCP Server

```bash
# 使用 npx（推荐，无需安装）
npx -y @modelcontextprotocol/server-filesystem /path/to/dir

# 或全局安装
npm install -g @modelcontextprotocol/server-filesystem
```

### 步骤 2：配置到 Claude Code

**项目级配置** (`.mcp.json`)：
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  }
}
```

**全局配置** (`~/.claude/claude_desktop_config.json`)：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
```

### 步骤 3：设置环境变量（如需要）

```bash
# 临时设置
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# 永久设置（添加到 ~/.bashrc）
echo 'export DATABASE_URL="postgresql://..."' >> ~/.bashrc
```

### 步骤 4：重启 Claude Code

```bash
claude
```

### 步骤 5：验证配置

```bash
# 在 Claude Code 中输入
/mcp

# 或使用命令行
claude mcp list
```

## 注意事项 ⚠️

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

### 关键配置点

**使用环境变量**：
```json
{
  "env": {
    "DATABASE_URL": "${DATABASE_URL}",
    "API_KEY": "${API_KEY}"
  }
}
```

**使用绝对路径**：
```json
{
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
}
```

**为 Python 设置 UNBUFFERED**：
```json
{
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

**使用 .gitignore 保护敏感信息**：
```bash
# .gitignore
.mcp.json
.env
```

## 常用 MCP Servers

| 服务器 | 功能 | 安装命令 |
|--------|------|----------|
| **filesystem** | 文件系统访问 | `npx -y @modelcontextprotocol/server-filesystem` |
| **postgres** | PostgreSQL 数据库 | `npx -y @modelcontextprotocol/server-postgres` |
| **git** | Git 操作 | `npx -y @modelcontextprotocol/server-git --repository /path` |
| **brave-search** | Brave 搜索 | `npx -y @modelcontextprotocol/server-brave-search` |
| **github** | GitHub API | SSE URL: `https://mcp.githubcopilot.com/mcp/` |

### CLI 管理命令

```bash
# 查看 MCP 列表
/mcp

# 添加服务器
claude mcp add <name> <command> [args...]

# 删除服务器
claude mcp remove <name>

# 启用/禁用
claude mcp enable <name>
claude mcp disable <name>
```

## 常见问题 ❓

**Q: stdio 和 SSE 有什么区别？**

A:
- **stdio**：本地进程，Claude Code 启动和管理服务器
- **SSE**：远程服务，通过 URL 连接，支持 OAuth

**Q: 如何测试 MCP 配置？**

A:
```bash
# 1. 调试模式启动
claude --debug

# 2. 查看状态
/mcp

# 3. 手动测试服务器
npx -y @modelcontextprotocol/server-filesystem /test/path
```

**Q: 如何在多个项目间共享 MCP 配置？**

A: 将配置放在全局配置文件 `~/.claude/claude_desktop_config.json` 中。

**Q: OAuth 服务需要做什么？**

A: 添加 SSE 类型的 URL 配置，首次使用时 Claude Code 会自动打开浏览器完成 OAuth 授权。

**Q: 能在插件中使用 MCP 吗？**

A: 可以！在插件目录创建 `.mcp.json` 或在 `plugin.json` 中添加 `mcpServers` 字段。

## 相关文档
[[Prompt, Agent, MCP 是什么]] | [[Claude Subagent 使用指南]] | [[如何使用Claude code]]
