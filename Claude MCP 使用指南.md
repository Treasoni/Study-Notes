# Claude MCP 使用指南

> 最后更新：2025年8月 | 基于 Claude Code 0.48+ 和 MCP 协议 v2.0

## 目录

1. [MCP 简介](#1-mcp-简介)
2. [方式一：通过配置文件添加 MCP](#2-方式一通过配置文件添加-mcp)
3. [方式二：通过 Claude CLI 添加 MCP](#3-方式二通过-claude-cli-添加-mcp)
4. [常用 MCP 服务器推荐](#4-常用-mcp-服务器推荐)
5. [故障排查](#5-故障排查)
6. [参考资料](#6-参考资料)

---

## 1. MCP 简介

### 1.1 什么是 MCP

**MCP (Model Context Protocol)** 是 Anthropic 提出的开放标准协议，用于让 AI 模型安全、可控地连接外部工具和数据源。

### 1.2 MCP 的作用和优势

```
默认 Claude Code：只能读写本地文件 + 执行命令
        ↓
      添加 MCP
        ↓
扩展能力：连接数据库、调用 API、访问第三方服务...
```

**核心优势**：
- 🔒 **安全可控**：所有操作需要用户明确批准
- 🔌 **即插即用**：通过简单配置即可扩展能力
- 🔄 **标准化**：统一协议，不同服务使用相同配置方式
- 📦 **丰富生态**：社区提供数百种 MCP 服务器

### 1.3 官方资源

- 官方文档：https://modelcontextprotocol.io/
- 快速入门：https://modelcontextprotocol.io/quickstart/user
- GitHub：https://github.com/modelcontextprotocol

---

## 2. 方式一：通过配置文件添加 MCP

### 2.1 Claude Desktop 配置

#### 配置文件位置

| 操作系统 | 配置文件路径 |
|---------|------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

#### 基本配置格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-xxx"]
    }
  }
}
```

#### 完整配置示例

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token-here"
      }
    }
  }
}
```

### 2.2 Claude Code 配置

Claude Code 支持多层级配置系统，按优先级从高到低加载：

| 配置层级 | 文件位置 | 作用范围 | 是否提交 Git |
|---------|---------|---------|-------------|
| **项目本地级** | `.claude/settings.local.json` | 仅本地项目 | ❌ 否 |
| **项目级** | `.mcp.json` 或 `.claude/mcp.json` | 整个项目，团队共享 | ✅ 是 |
| **用户级** | `~/.claude.json` | 该用户所有项目 | ❌ 否 |

#### 项目级配置（推荐）

在项目根目录创建 `.mcp.json` 文件：

```json
{
  "mcpServers": {
    "mysql-dev": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/mydb"
      }
    },
    "redis-cache": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-redis"],
      "env": {
        "REDIS_URL": "redis://localhost:6379"
      }
    }
  }
}
```

#### 用户级配置

编辑 `~/.claude.json` 文件：

```json
{
  "mcpServers": {
    "global-filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    }
  }
}
```

### 2.3 配置文件字段详解

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `mcpServers` | Object | ✅ | 服务器配置集合 |
| `type` | String | ❌ | 通信协议类型，通常为 `"stdio"` |
| `command` | String | ✅ | 启动 MCP 服务器的命令 |
| `args` | Array | ✅ | 命令参数列表 |
| `env` | Object | ❌ | 环境变量（连接信息、Token 等） |
| `disabled` | Boolean | ❌ | 是否禁用该服务器 |

### 2.4 Windows 特别注意事项

⚠️ **Windows 用户必读**：Windows 平台的 MCP 配置失败率较高，需特别注意以下事项：

#### 路径格式问题

```json
// ❌ 错误：单反斜杠
"C:\Users\name\project"

// ✅ 正确：双反斜杠或正斜杠
"C:\\Users\\name\\project"
"C:/Users/name/project"

// WSL 环境使用 /mnt/c/ 格式
"/mnt/c/Users/name/project"
```

#### CMD 包装器要求

Windows 必须使用 `cmd /c` 包装命令：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "PATH": "C:\\Program Files\\nodejs;%PATH%"
      }
    }
  }
}
```

#### 权限问题避免

❌ 避免安装在需要管理员权限的目录：
- `Program Files`
- `Windows\System32`

✅ 推荐安装路径：
- `C:/Users/[username]/AppData/Local/claude-mcp/`

### 2.5 中文路径解决方案

如果路径中包含中文字符，可采用以下策略：

#### 方案一：环境变量设置

```bash
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
chcp 65001  # Windows 切换到 UTF-8 代码页
```

#### 方案二：符号链接

创建英文路径的符号链接指向中文目录：

```bash
# Windows
mklink /D C:\mcp-workspace "C:\工作空间\项目"

# 配置中使用 C:\mcp-workspace
```

---

## 3. 方式二：通过 Claude CLI 添加 MCP

Claude CLI（命令行界面）提供了更便捷的 MCP 管理方式。

### 3.1 基本命令

#### 添加 MCP 服务器

```bash
# 基本用法
claude mcp add <server-name>

# 示例：添加 Filesystem MCP
claude mcp add filesystem --command "npx" --args "-y" "@modelcontextprotocol/server-filesystem" "/path/to/allow"

# 示例：添加带环境变量的服务器
claude mcp add postgres --command "npx" --args "-y" "@modelcontextprotocol/server-postgres" --env DATABASE_URL="postgresql://localhost:5432/mydb"
```

#### 列出已配置的 MCP 服务器

```bash
claude mcp list
```

输出示例：
```
配置的 MCP 服务器：
• filesystem (项目级) - 已连接 ✅
• postgres (用户级) - 已连接 ✅
• redis (项目级) - 连接失败 ❌
```

#### 移除 MCP 服务器

```bash
claude mcp remove <server-name>

# 示例
claude mcp remove redis
```

#### 获取 MCP 服务器详细信息

```bash
claude mcp get <server-name>

# 示例
claude mcp get postgres
```

#### 测试 MCP 服务器

```bash
claude mcp test <server-name>

# 示例：测试 postgres 连接
claude mcp test postgres
```

### 3.2 高级命令

#### 通过 JSON 添加服务器

```bash
claude mcp add-json '{
  "name": "custom-server",
  "command": "node",
  "args": ["path/to/server.js"],
  "env": {
    "API_KEY": "your-key"
  }
}'
```

#### 从 Claude Desktop 导入配置

```bash
claude mcp add-from-claude-desktop
```

此命令会自动读取 Claude Desktop 的配置文件并迁移到 Claude Code。

#### 添加特定传输类型的服务器

```bash
claude mcp add-transport --type <transport-type> <server-name>
```

支持的传输类型：
- `stdio` - 标准输入输出（最常用）
- `sse` - Server-Sent Events
- `websocket` - WebSocket 连接

### 3.3 作用域选项

#### 全局安装（用户级）

```bash
claude mcp add <server-name> --scope user
```

配置写入 `~/.claude.json`，对所有项目生效。

#### 项目级安装

```bash
# 默认即为项目级
claude mcp add <server-name>
claude mcp add <server-name> --scope project
```

配置写入项目根目录的 `.mcp.json` 或 `.claude/mcp.json`。

### 3.4 交互式添加

直接通过对话添加 MCP 服务器：

```
你：请帮我在 .mcp.json 中新增一个 Redis MCP 服务，地址是 192.168.85.73:6379

AI：好的，我将为你添加 Redis MCP 服务配置...
[AI 自动编辑 .mcp.json 文件]
```

更多提示词示例：

```bash
# 添加 MySQL MCP
帮我配置一个 MySQL 的 MCP 服务，连接信息如下：
- 主机：192.168.85.73
- 端口：3310
- 用户名：os_user
- 密码：xxx
- 数据库：stt9900010001

# 添加 Fetch MCP（用于调用外部 API）
帮我添加一个 Fetch MCP 服务，我需要让 AI 能发送 HTTP 请求测试接口

# 添加 Filesystem MCP（扩展文件访问范围）
帮我配置一个 Filesystem MCP，允许访问 D:/共享文档 目录

# 一次添加多个
帮我在 .mcp.json 中同时添加 Redis 和 Fetch 两个 MCP 服务
```

### 3.5 MCP 管理

在 Claude Code 对话中使用 `/mcp` 命令：

```bash
/mcp          # 查看所有 MCP 服务的连接状态
```

如果发现某个 MCP 服务状态异常：

```
你：mysql-goods-service 连接失败了，帮我检查一下配置是否正确

AI：让我检查配置...
[AI 诊断问题并修复]
```

---

## 4. 常用 MCP 服务器推荐

基于 2025 年使用统计，以下 MCP 服务器覆盖 90% 的日常需求：

### 4.1 核心服务器

| 服务器名称 | NPM 包名 | 用途 | 适用场景 |
|-----------|---------|------|---------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | 文件系统访问 | 读写项目外文件、搜索文件 |
| **GitHub** | `@modelcontextprotocol/server-github` | GitHub API | PR 管理、Issue 查看、仓库操作 |
| **PostgreSQL** | `@modelcontextprotocol/server-postgres` | PostgreSQL 数据库 | 数据验证、表结构查询、SQL 调试 |
| **MySQL** | `@modelcontextprotocol/server-mysql` | MySQL 数据库 | 同上（MySQL 项目） |
| **Redis** | `@modelcontextprotocol/server-redis` | Redis 缓存 | 缓存数据查看、Key 排查 |
| **Fetch** | `@modelcontextprotocol/server-fetch` | HTTP 请求 | 调用外部 API、测试接口 |

### 4.2 开发工具服务器

| 服务器名称 | NPM 包名 | 用途 |
|-----------|---------|------|
| **Sequential Thinking** | `@modelcontextprotocol/server-sequential-thinking` | 顺序思考推理 |
| **Chrome DevTools** | `@modelcontextprotocol/server-chrome-devtools` | 浏览器开发工具 |
| **Puppeteer** | `@modelcontextprotocol/server-puppeteer` | 浏览器自动化 |
| **Slack** | `@modelcontextprotocol/server-slack` | Slack 团队协作 |
| **Kubernetes** | `@modelcontextprotocol/server-kubernetes` | K8s 容器管理 |

### 4.3 LSP 语言服务器

LSP MCP 让 AI 获得与 IDE 相同的代码语义理解能力：

| 服务器名称 | 项目地址 | 能力 |
|-----------|---------|------|
| **mcp-language-server** | https://github.com/isaacphi/mcp-language-server | Go to Definition、Find References、Diagnostics |
| **lsp-mcp** | https://github.com/jonrad/lsp-mcp | 多语言 LSP 代理 |

LSP MCP 提供的能力：
- **Go to Definition**：精确跳转到符号定义
- **Find References**：查找所有引用点
- **Diagnostics**：实时获取编译错误
- **Hover Info**：查看变量精确类型
- **Rename**：语义重命名

### 4.4 一键安装脚本

```bash
# 安装核心 MCP 服务器
npm install -g @modelcontextprotocol/server-filesystem \
  @modelcontextprotocol/server-github \
  @modelcontextprotocol/server-postgres \
  @modelcontextprotocol/server-redis \
  @modelcontextprotocol/server-fetch
```

---

## 5. 故障排查

### 5.1 连接失败诊断

#### 快速诊断步骤

```bash
# 1. 检查 MCP 连接状态
claude-code --mcp-status

# 2. 查看详细日志
claude-code --mcp-debug

# 3. 清除缓存重启
rm -rf ~/.claude/cache/*
```

#### 常见错误及解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `spawn ENOENT` | 路径问题 | 检查 command 和 args 中的路径是否正确 |
| `protocol mismatch` | 版本冲突 | 运行 `npm update @modelcontextprotocol/sdk@latest` |
| `permission denied` | 权限错误 | 避免使用系统目录，使用用户目录 |
| `port already in use` | 端口占用 | 更换端口或清理占用进程 |

### 5.2 配置文件冲突

**问题**：同时存在多个配置文件导致冲突

**解决方案**：按优先级只保留一个配置

```bash
# 删除旧配置
rm ~/claude_desktop_config.json

# 仅保留项目级配置
.mcp.json
```

### 5.3 紧急修复脚本

一键解决 80% 的常见问题：

```bash
#!/bin/bash
# MCP 快速修复脚本

pkill -f "claude-mcp-server"  # 清理残留进程
rm -rf ~/.claude/cache/*       # 清除缓存
claude-code --reset-mcp        # 重置 MCP 配置
claude-code --mcp-init         # 重新初始化
```

### 5.4 Windows 验证脚本

```powershell
# PowerShell 验证脚本
Test-Path $env:USERPROFILE.claude\mcp.json
Get-Process | Where-Object {$_.ProcessName -like "*claude-mcp*"}
netstat -an | findstr "3000"
```

### 5.5 检查 MCP 服务器状态

```bash
# Unix/Linux/macOS
ps aux | grep mcp

# Windows
tasklist | findstr mcp

# 检查端口监听
lsof -i :3000  # Unix
netstat -an | findstr "3000"  # Windows
```

### 5.6 启用详细日志

在配置文件中添加调试选项：

```json
{
  "mcpServers": {
    "debug": {
      "logLevel": "debug",
      "logFile": "./mcp-debug.log",
      "verboseErrors": true
    }
  }
}
```

**关键日志位置**：

| 操作系统 | 日志文件位置 |
|---------|------------|
| Windows | `%APPDATA%\Claude\logs\mcp.log` |
| macOS | `~/Library/Logs/Claude/mcp.log` |
| Linux | `~/.config/claude/logs/mcp.log` |

### 5.7 企业环境代理配置

```bash
# 设置环境变量
export HTTP_PROXY=http://proxy:port
export NO_PROXY=localhost,127.0.0.1

# 在 MCP 配置中添加
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-xxx"],
      "env": {
        "proxy": "http://proxy:port"
      }
    }
  }
}
```

---

## 6. 参考资料

### 6.1 官方资源

- **MCP 官方文档**：https://modelcontextprotocol.io/
- **快速入门指南**：https://modelcontextprotocol.io/quickstart/user
- **MCP 规范**：https://spec.modelcontextprotocol.io/
- **GitHub 仓库**：https://github.com/modelcontextprotocol

### 6.2 社区资源

- **掘金 - Claude Code MCP 配置完整指南（2025年8月）**：https://juejin.cn/post/7540879173180473380
- **博客园 - 项目配置：CLAUDE.md、MCP、Skill 与 Hooks**：https://www.cnblogs.com/hyxf/articles/19597313

### 6.3 常用 MCP 服务器仓库

- **官方服务器列表**：https://github.com/modelcontextprotocol/servers
- **社区服务器索引**：https://github.com/modelcontextprotocol/awesome-mcp-servers

### 6.4 版本要求

- **Claude Code**：0.48+ （要求 MCP 协议 v2.0）
- **Node.js**：18.0+ （推荐 LTS 版本）
- **MCP SDK**：2.0.0+

检查版本：

```bash
claude --version
node --version
npm ls @modelcontextprotocol/sdk
```

---

## 附录：快速参考卡

### 配置文件模板

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host:port/db"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

### CLI 常用命令速查

```bash
# 添加服务器
claude mcp add <name> --command "npx" --args "-y" "@package/name"

# 列出服务器
claude mcp list

# 测试连接
claude mcp test <name>

# 移除服务器
claude mcp remove <name>

# 查看详情
claude mcp get <name>
```

---

> **文档维护**：本指南将随 Claude Code 版本更新而同步维护
> **最后更新**：2025年8月
> **适用版本**：Claude Code 0.48+ | MCP Protocol v2.0
