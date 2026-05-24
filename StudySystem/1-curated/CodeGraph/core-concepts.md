# CodeGraph 核心概念

## 什么是 CodeGraph

CodeGraph 是为 AI 编码助手设计的代码语义分析工具，通过预索引知识图谱提供符号关系、调用图谱和代码结构查询。

**核心定位**：给 AI 编程助手装一个"本地代码导航仪"

**核心优势**：
- ~35% 更低成本
- ~70% 更少工具调用
- 100% 本地运行，无需 API Key

## 核心概念

### 1. 知识图谱 (Knowledge Graph)

CodeGraph 构建的代码知识图谱包含：

| 元素 | 说明 |
|------|------|
| **节点 (Nodes)** | 函数、类、方法、变量等符号 |
| **边 (Edges)** | 调用关系、导入关系、继承关系 |
| **路由 (Routes)** | Web 框架 URL 模式到处理器的映射 |

**存储方式**：本地 SQLite 数据库 + FTS5 全文搜索

### 2. MCP Server 架构

CodeGraph 作为 MCP (Model Context Protocol) 服务器运行，为 AI Agent 提供工具调用接口：

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│                                                                  │
│  "Implement user authentication"                                 │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐      ┌─────────────────┐                   │
│  │  Explore Agent  │ ──── │  Explore Agent  │                   │
│  └────────┬────────┘      └────────┬────────┘                   │
└───────────┼────────────────────────┼─────────────────────────────┘
            │                        │
            ▼                        ▼
┌───────────────────────────────────────────────────────────────────┐
│                     CodeGraph MCP Server                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │   Search    │  │   Callers   │  │   Context   │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                          ▼                                        │
│              ┌───────────────────────┐                            │
│              │   SQLite Graph DB     │                            │
│              └───────────────────────┘                            │
└───────────────────────────────────────────────────────────────────┘
```

### 3. tree-sitter AST 解析

CodeGraph 使用 tree-sitter 解析源码为 AST（抽象语法树），然后通过语言特定查询提取：
- **节点**：函数、类、方法
- **边**：调用、导入、扩展、实现

### 4. Auto-Sync 机制

文件监视器使用原生 OS 事件：
- macOS: FSEvents
- Linux: inotify
- Windows: ReadDirectoryChangesW

**特点**：
- 2秒防抖窗口
- 仅监控源文件变更
- 增量同步

### 5. Framework-aware Routes

CodeGraph 识别 14 种 Web 框架的路由文件，将 URL 模式与处理器关联：

| 框架 | 路由模式 |
|------|----------|
| Django | `path()`, `re_path()`, `url()`, `include()` |
| Flask | `@app.route()` |
| FastAPI | `@app.get()`, `@router.post()` |
| Express | `app.get()`, `router.post()` |
| NestJS | `@Controller` + `@Get/@Post` |
| Rails | `get '/x', to: 'users#index'` |
| Spring | `@GetMapping`, `@PostMapping` |
| Gin | `r.GET()`, `router.HandleFunc()` |

## 关键设计理念

### 零配置 (Zero-Config)

- 自动索引所有支持语言的文件
- 遵守 `.gitignore` 规则
- 无需配置文件

### 智能上下文构建 (Smart Context Building)

单次工具调用返回：
- 入口点
- 相关符号
- 代码片段

### 影响分析 (Impact Analysis)

追踪符号的：
- 调用者 (callers)
- 被调用者 (callees)
- 完整影响半径

## 数据来源

- [GitHub 官方仓库](https://github.com/colbymchenry/codegraph)
- [CodeGraph Documentation](https://codegraph.ru/docs/en/index.html)
