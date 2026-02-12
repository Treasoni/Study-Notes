---
title: Claude MCP 使用指南
date: 2026-02-12
tags:
  - Claude
  - MCP
  - AI学习
  - CLI
---

# Claude MCP 使用指南

> [!abstract] 概述
> MCP (Model Context Protocol) 是 Claude Code 与外部工具和服务通信的标准协议。通过 MCP，Claude 可以访问文件系统、数据库、API 等各种外部资源。

> [!info] 为什么需要 MCP
> 在 CLI 中，Claude 默认只能访问当前工作目录的文件。通过 MCP，你可以让 Claude 访问：
> - 文件系统（任意目录）
> - 数据库（PostgreSQL、MySQL、SQLite 等）
> - 云服务（GitHub、Asana、Supabase 等）
> - 浏览器（自动化操作）
> - 其他自定义工具

## MCP 配置文件

### 配置文件位置

MCP 配置可以在三个层级创建：

| 级别 | 位置 | 作用范围 |
|------|------|----------|
| **项目级** | `${CLAUDE_PROJECT_DIR}/.mcp.json` | 仅当前项目有效 |
| **全局级** | `~/.claude/claude_desktop_config.json` | 所有项目共享 |
| **插件级** | `插件根目录/.mcp.json` | 插件自带的服务器 |

### 基本配置格式

```json
{
  "server-name": {
    "command": "可执行文件或命令",
    "args": ["命令参数列表"],
    "env": {
      "环境变量名": "值"
    },
    "type": "stdio|sse|http|ws",
    "url": "服务器 URL（SSE/HTTP/WS 类型）",
    "headers": {
      "Header-Name": "值"
    }
  }
}
```

---

# 外部 MCP Server 类型

## 1. stdio 类型（标准输入输出）

> [!tip] 最常用的类型
> 适用于本地工具、自定义脚本、NPM 包。

**特点**：
- 进程间通信，低延迟
- Claude Code 管理服务器生命周期
- 支持环境变量传递

**配置示例**：

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
    "env": {
      "LOG_LEVEL": "info"
    }
  },
  "python-server": {
    "command": "python",
    "args": ["-m", "my_mcp_server"],
    "env": {
      "PYTHONUNBUFFERED": "1",
      "API_KEY": "${API_KEY}"
    }
  }
}
```

### 常用 stdio MCP Servers

| 名称 | 安装命令 | 功能 |
|------|----------|------|
| @modelcontextprotocol/server-filesystem | `npx -y @modelcontextprotocol/server-filesystem` | 文件系统访问 |
| @modelcontextprotocol/server-postgres | `npx -y @modelcontextprotocol/server-postgres` | PostgreSQL 数据库 |
| @modelcontextprotocol/server-git | `npx -y @modelcontextprotocol/server-git` | Git 操作 |
| @modelcontextprotocol/server-brave-search | `npx -y @modelcontextprotocol/server-brave-search` | Brave 搜索 |
| @playwright/mcp | `npx @playwright/mcp@latest` | 浏览器自动化 |

---

## 2. SSE 类型（Server-Sent Events）

> [!tip] 适用于云端服务
> 适用于托管服务、OAuth 认证、需要浏览器授权的服务。

**特点**：
- 自动 OAuth 流程
- 首次使用时自动打开浏览器授权
- 自动令牌刷新和重连
- 适用于官方托管服务

**配置示例**：

```json
{
  "asana": {
    "type": "sse",
    "url": "https://mcp.asana.com/sse"
  },
  "github": {
    "type": "sse",
    "url": "https://mcp.githubcopilot.com/mcp/"
  }
}
```

### 常用 SSE MCP Servers

| 名称 | URL | 功能 |
|------|------|------|
| Asana | `https://mcp.asana.com/sse` | 任务管理 |
| GitHub Copilot | `https://mcp.githubcopilot.com/mcp/` | GitHub 集成 |
| Linear | `https://mcp.linear.app/sse` | 项目管理 |

---

## 3. HTTP 类型（REST API）

> [!tip] 适用于 API 后端
> 适用于 REST API、令牌认证、无状态服务。

**特点**：
- 请求/响应模式
- 支持自定义请求头
- 需要手动管理令牌

**配置示例**：

```json
{
  "rest-api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}",
      "Content-Type": "application/json",
      "X-API-Version": "2024-01-01"
    }
  }
}
```

---

## 4. WebSocket 类型

> [!tip] 适用于实时通信
> 适用于需要持久连接、双向通信、实时数据推送的场景。

**特点**：
- 持久连接
- 双向通信
- 实时数据推送
- 自动重连

**配置示例**：

```json
{
  "realtime-service": {
    "type": "ws",
    "url": "wss://mcp.example.com/ws",
    "headers": {
      "Authorization": "Bearer ${TOKEN}"
    }
  }
}
```

---

# 如何配置外部 MCP Server

## 步骤 1：安装依赖

### 使用 NPM（推荐）

```bash
# 全局安装
npm install -g @modelcontextprotocol/server-filesystem

# 使用 npx 直接运行（推荐，无需安装）
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
```

### 使用 Python

```bash
# 安装
pip install mcp-server

# 运行
python -m mcp_server
```

## 步骤 2：创建 .mcp.json 文件

在项目根目录创建 `.mcp.json`：

```bash
# 方法 1：直接创建
cat > .mcp.json << 'EOF'
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  }
}
EOF

# 方法 2：使用 echo
echo '{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  }
}' > .mcp.json
```

## 步骤 3：设置环境变量（如需要）

```bash
# 方法 1：临时设置（仅当前会话）
export API_TOKEN="your-token-here"
claude

# 方法 2：.env 文件
echo "API_TOKEN=your-token-here" >> .env
source .env
claude

# 方法 3：命令行参数
API_TOKEN=your-token-here claude

# 方法 4：Shell 配置文件（永久）
echo 'export API_TOKEN="your-token-here"' >> ~/.bashrc
source ~/.bashrc
```

## 步骤 4：重启 Claude Code

配置完成后，重启 Claude Code 使配置生效。

---

# 完整配置示例

## 示例 1：文件系统访问

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  }
}
```

**使用场景**：让 Claude 访问和操作项目文件

---

## 示例 2：PostgreSQL 数据库

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "postgresql://user:password@localhost:5432/dbname"
    }
  }
}
```

**使用场景**：让 Claude 查询和操作数据库

---

## 示例 3：GitHub 集成（SSE + OAuth）

```json
{
  "github": {
    "type": "sse",
    "url": "https://mcp.githubcopilot.com/mcp/"
  }
}
```

**使用步骤**：
1. 添加配置到 `.mcp.json`
2. 重启 Claude Code
3. 首次使用时，浏览器会自动打开 GitHub OAuth 页面
4. 授权后即可使用 GitHub 工具

---

## 示例 4：自定义 API 服务（HTTP）

```json
{
  "my-api": {
    "type": "http",
    "url": "https://api.my-service.com/mcp",
    "headers": {
      "Authorization": "Bearer ${MY_API_TOKEN}",
      "X-API-Key": "${MY_API_KEY}"
    }
  }
}
```

**使用场景**：连接自建的后端 API

---

## 示例 5：浏览器自动化

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest"],
    "env": {
      "HEADLESS": "true"
    }
  }
}
```

**使用场景**：让 Claude 自动化浏览器操作（截图、点击、填表单）

---

## 示例 6：Git 操作

```json
{
  "git": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "${CLAUDE_PROJECT_DIR}"]
  }
}
```

**使用场景**：让 Claude 执行 Git 操作（提交、分支、标签）

---

## 示例 7：Brave 搜索

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"]
  }
}
```

**使用场景**：让 Claude 使用 Brave 进行网页搜索

---

## 示例 8：多个 MCP Server 组合

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  },
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  },
  "github": {
    "type": "sse",
    "url": "https://mcp.githubcopilot.com/mcp/"
  },
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest"]
  }
}
```

---

# 环境变量详解

## ${CLAUDE_PLUGIN_ROOT}

> [!info] 提件根目录
> 在插件中使用时，表示插件安装的根目录。使用它可以保持路径可移植性。

```json
{
  "server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

## ${CLAUDE_PROJECT_DIR}

> [!info] 当前项目目录
> 表示当前 Claude Code 工作的项目目录。

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
  }
}
```

## 自定义环境变量

```bash
# 设置
export MY_VAR="value"

# 在配置中引用
{
  "server": {
    "env": {
      "MY_VAR": "${MY_VAR}"
    }
  }
}
```

---

# CLI 管理命令

```bash
# 查看所有已配置的 MCP 服务器
/mcp

# 查看服务器详情和可用工具
/mcp
# 然后选择一个服务器查看

# 添加服务器（快速方式）
claude mcp add <name> <command> [args...]

# 删除服务器
claude mcp remove <name>

# 调试模式
claude --debug
```

---

# 最佳实践

> [!tip] 配置建议

1. **使用 ${CLAUDE_PROJECT_DIR} 保持可移植性**
   ```json
   "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
   ```

2. **环境变量不要硬编码**
   ```json
   // ❌ 不推荐
   "env": { "TOKEN": "sk-abc123..." }

   // ✅ 推荐
   "env": { "TOKEN": "${API_TOKEN}" }
   ```

3. **使用安全连接（HTTPS/WSS）**
   ```json
   // ✅ 使用 HTTPS
   "url": "https://api.example.com/mcp"

   // ✅ 使用 WSS（WebSocket Secure）
   "url": "wss://mcp.example.com/ws"
   ```

4. **为 Python 设置 PYTHONUNBUFFERED**
   ```json
   {
     "command": "python",
     "args": ["-m", "my_server"],
     "env": {
       "PYTHONUNBUFFERED": "1"
     }
   }
   ```

5. **使用 .gitignore 保护敏感信息**
   ```bash
   # .gitignore
   .mcp.json
   .env
   ```

6. **文档化环境变量需求**
   ```markdown
   # README.md
   ## 环境变量
   - `API_TOKEN`: 你的 API 密钥
   - `DATABASE_URL`: 数据库连接字符串
   ```

---

# 常见问题

> [!faq] Q: MCP 配置文件在哪里？
> A:
> - 项目级：项目根目录的 `.mcp.json`
> - 全局级：`~/.claude/claude_desktop_config.json`
> - 插件级：插件目录的 `.mcp.json`

> [!faq] Q: stdio 和 SSE 有什么区别？
> A:
> - **stdio**：本地进程，Claude Code 启动和管理服务器
> - **SSE**：远程服务，通过 URL 连接，支持 OAuth

> [!faq] Q: 如何测试 MCP 配置是否正确？
> A:
> ```bash
> # 1. 使用调试模式启动
> claude --debug
>
> # 2. 在 Claude Code 中输入 /mcp 查看状态
>
> # 3. 手动测试服务器命令
> npx -y @modelcontextprotocol/server-filesystem /test/path
> ```

> [!faq] Q: 如何在多个项目间共享 MCP 配置？
> A: 将配置放在全局配置文件 `~/.claude/claude_desktop_config.json` 中。

> [!faq] Q: OAuth 服务需要做什么？
> A: 添加 SSE 类型的 URL 配置，首次使用时 Claude Code 会自动打开浏览器完成 OAuth 授权流程。

> [!faq] Q: 能在插件中使用 MCP 吗？
> A: 可以！在插件目录创建 `.mcp.json` 或在 `plugin.json` 中添加 `mcpServers` 字段。

---

# 调试技巧

```bash
# 1. 启动调试模式
claude --debug

# 2. 查看 MCP 连接状态
# 在 Claude Code 中输入：
/mcp

# 3. 检查环境变量
echo $API_TOKEN
echo $DATABASE_URL

# 4. 手动测试 MCP 服务器
npx -y @modelcontextprotocol/server-filesystem /test/path

# 5. 测试 HTTP 端点
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/mcp/health
```

---

# 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Code MCP 文档](https://docs.anthropic.com/claude-code/mcp)
- [MCP GitHub 仓库](https://github.com/modelcontextprotocol)

## 相关概念

[[Claude Code 基础]] | [[Claude Subagent 使用指南]] | [[Agent Skills]]
