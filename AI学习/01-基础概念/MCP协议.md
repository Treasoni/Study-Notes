---
tags: [ai, 基础概念, mcp]
---

# MCP 协议

> [!info] 概述
> **MCP 是 AI 时代的"USB 接口"** - 不管什么设备（数据库、API、文件系统），只要支持 MCP，就能即插即用。一次开发，所有兼容的 AI 应用都能用。

## 核心概念

### 什么是 MCP

**全称**：Model Context Protocol（模型上下文协议）

**定义**：Agent 与外部工具/数据源之间的**标准化通信协议**

**发布信息**：
- 发布方：Anthropic
- 发布时间：2024年11月
- 开源状态：完全开源

**为什么需要 MCP**：

```
传统方式（碎片化）：
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Claude  │────▶│ 自定义API│────▶│ 数据库   │
└─────────┘     └─────────┘     └─────────┘
┌─────────┐     ┌─────────┐     ┌─────────┐
│  GPT    │────▶│ 另一套API │────▶│ 数据库   │
└─────────┘     └─────────┘     └─────────┘
问题：N 个 AI × M 个数据源 = N×M 种定制开发（噩梦）

MCP 方式（标准化）：
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Claude  │──┐  │         │     │ 数据库   │
├─────────┤  ├──▶   MCP   │────▶│ API     │
│  GPT    │──┘  │  协议   │     │ 文件系统 │
├─────────┤     │         │     │ ...     │
│ Gemini  │     └─────────┘     └─────────┘
└─────────┘
优势：一次开发，所有 MCP 兼容的 AI 都能用
```

### USB 比喻

| USB | MCP |
|-----|-----|
| 统一的硬件接口标准 | 统一的 AI 工具接口标准 |
| 鼠标、键盘、U盘 都用 USB | 数据库、API、文件 都用 MCP |
| 即插即用 | 一次封装，全球可用 |
| USB-C 成为通用标准 | MCP 正在成为 AI 通用标准 |

### 核心特点

| 特点 | 说明 |
|------|------|
| **标准化** | 统一的接口规范，消除碎片化 |
| **即插即用** | 配置即可使用，无需定制开发 |
| **跨平台** | Claude、GPT、Gemini 等都能用 |
| **可扩展** | 任何人都可以开发 MCP Server |

---

## 技术细节

### 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                  MCP Host（主机层）                           │
│                                                              │
│   Claude Desktop / Claude Code / Cursor / Windsurf / IDE    │
│                                                              │
│   职责：接收用户指令，驱动 Agent，协调多个 Client            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ JSON-RPC 2.0
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                 MCP Client（客户端层）                        │
│                                                              │
│   与 Server 建立 1:1 会话，能力协商，请求转发                 │
│                                                              │
│   职责：                                                     │
│   - 与 Server 建立连接                                       │
│   - 协商支持的能力（Tools/Resources/Prompts）                │
│   - 将请求转为 JSON-RPC 格式                                 │
│   - 管理会话状态                                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ JSON-RPC 2.0
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                 MCP Server（服务器层）                        │
│                                                              │
│   文件系统 / PostgreSQL / GitHub / Slack / Jira / 自定义     │
│                                                              │
│   职责：                                                     │
│   - 封装外部能力为标准化接口                                  │
│   - 暴露 Tools、Resources、Prompts                          │
│   - 处理具体业务逻辑                                         │
└─────────────────────────────────────────────────────────────┘
```

### 三类核心能力

MCP Server 可以提供三类能力：

| 类型 | 作用 | 特点 | 示例 |
|------|------|------|------|
| **Tools** | 可执行的函数/操作 | 有副作用，可修改状态 | 读写文件、发送消息、执行命令 |
| **Resources** | 可访问的数据源 | 只读，提供信息 | 文件内容、数据库记录、API 响应 |
| **Prompts** | 预定义的提示词模板 | 可复用，参数化 | 常用任务的标准指令 |

**Tools 示例**：
```json
{
  "name": "read_file",
  "description": "读取指定路径的文件内容",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": { "type": "string", "description": "文件路径" }
    },
    "required": ["path"]
  }
}
```

**Resources 示例**：
```json
{
  "uri": "file:///project/README.md",
  "name": "项目说明文档",
  "mimeType": "text/markdown"
}
```

**Prompts 示例**：
```json
{
  "name": "code_review",
  "description": "代码审查提示词模板",
  "arguments": [
    { "name": "language", "description": "编程语言" }
  ]
}
```

### 通信协议

MCP 使用 **JSON-RPC 2.0** 作为通信协议：

**请求示例**：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/src/main.ts" }
  }
}
```

**响应示例**：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "文件内容..." }
    ]
  }
}
```

### 2025 生态发展

#### 厂商支持情况

| 厂商 | 支持状态 | 时间 |
|------|----------|------|
| **Anthropic** | 原生支持（创始方） | 2024.11 |
| **OpenAI** | 官方支持 | 2025.03 |
| **Google** | 官方支持 | 2025.03 |
| **Microsoft** | 官方支持 | 2025.04 |
| **Apple** | 计划支持 | 2025 |

#### 标准化管理

2025年，MCP 移交给 **Linux Foundation** 的 **AAIF（AI Agent Interoperability Foundation）** 管理：
- 确保标准的中立性
- 促进跨厂商协作
- 推动生态系统发展

#### 热门 MCP Server

| Server | 功能 | 使用场景 |
|--------|------|----------|
| **filesystem** | 文件系统访问 | 读写本地文件 |
| **postgres** | PostgreSQL 数据库 | 数据查询 |
| **github** | GitHub API | 仓库管理、PR 操作 |
| **slack** | Slack 集成 | 消息发送、频道管理 |
| **puppeteer** | 浏览器自动化 | 网页抓取、截图 |
| **memory** | 持久化记忆 | 跨会话知识存储 |

---

## 与其他概念的关系

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent 智能体                          │
│                     (需要调用外部能力)                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ 通过 MCP 协议
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      MCP 协议层                              │
│                                                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │   Tools      │  │  Resources   │  │   Prompts    │     │
│   │  (执行操作)  │  │  (读取数据)  │  │  (提示模板)  │     │
│   └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ 文件系统 │    │ 数据库   │    │  API     │
    └──────────┘    └──────────┘    └──────────┘
```

| 概念 | 与 MCP 的关系 |
|------|---------------|
| [[Agent智能体]] | Agent 通过 MCP 调用外部工具 |
| [[Skills是什么]] | Skills 可以调用 MCP 提供的工具 |
| [[SubAgent子代理]] | SubAgent 可配置专属的 MCP 工具集 |

---

## 最佳实践

### MCP Server 选择原则

1. **按需配置**：只启用必要的 Server
2. **权限最小化**：只给必要的访问权限
3. **安全优先**：敏感操作需要确认
4. **版本管理**：锁定 Server 版本避免兼容问题

### 配置示例

**Claude Desktop 配置**（`claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
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

### 常见陷阱

| 陷阱 | 问题 | 解决方案 |
|------|------|----------|
| **权限过大** | 给了不必要的访问权限 | 使用路径限制、权限白名单 |
| **Server 过多** | 启动慢、资源占用高 | 只启用必要的 Server |
| **版本不兼容** | Server 更新导致问题 | 锁定版本号 |
| **安全暴露** | 敏感信息泄露 | 使用环境变量、限制访问范围 |

---

## 常见问题

### Q1: MCP 和传统 API 有什么区别？

| 对比 | 传统 API | MCP |
|------|----------|-----|
| **接口格式** | 各自定义 | 统一标准 |
| **一次开发** | 只能一个应用用 | 所有 MCP 兼容应用都能用 |
| **维护成本** | 高（N×M 种对接） | 低（一次封装） |
| **生态共享** | 无 | 有（社区 Server 可复用） |

### Q2: 如何开发自己的 MCP Server？

开发步骤：
1. 选择语言（Python/TypeScript）
2. 实现标准接口（Tools/Resources/Prompts）
3. 处理 JSON-RPC 请求
4. 测试并发布

推荐框架：
- Python：`fastmcp`
- TypeScript：`@modelcontextprotocol/sdk`

### Q3: MCP 会成为行业标准吗？

趋势非常明确：
- OpenAI、Google、微软已宣布支持
- Linux Foundation 接管标准化管理
- 社区生态快速发展

MCP 正在成为 **AI 时代的 HTTP** —— 基础设施级别的标准。

### Q4: MCP Server 部署在哪里？

常见部署方式：
- **本地进程**：作为本地服务运行（最常见）
- **Docker 容器**：隔离环境，便于管理
- **远程服务**：云端部署，团队共享

---

## 相关文档

- [[01-基础概念/人工智能重要的六大概念体系]] - 六大概念总览
- [[01-基础概念/Agent智能体]] - MCP 的主要使用者
- [[03-进阶应用/Claude MCP 使用指南]] - 实践配置指南

---

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP GitHub 仓库](https://github.com/modelcontextprotocol)
- [Anthropic MCP 公告](https://www.anthropic.com/news/model-context-protocol)
- [OpenAI MCP 支持](https://platform.openai.com/docs/mcp)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
