---
type: practice
topic: CodeGraph 代码语义分析工具
difficulty: 入门
tags:
  - AI工具
  - 代码分析
  - Claude-Code
  - MCP
created: 2026-05-24
updated:
sources:
  - https://github.com/colbymchenry/codegraph
  - https://codegraph.ru/docs/en/index.html
concepts:
  - MCP Server
  - 知识图谱
  - tree-sitter
  - SQLite FTS5
---

# CodeGraph 实战笔记

## 目标

快速上手 CodeGraph，为 AI 编程助手（Claude Code、Cursor 等）配置代码语义分析能力，实现：
- 减少 ~70% 工具调用
- 降低 ~35% 成本
- 提升代码探索效率

## 前置知识

- AI 编程助手（Claude Code / Cursor / Codex CLI 等）的基本使用
- 命令行终端操作
- MCP (Model Context Protocol) 概念 [待补充]

## 环境准备

### 支持的平台
- macOS (x64, arm64)
- Linux (x64, arm64)
- Windows (x64, arm64)

### 支持的 Agent
- Claude Code
- Cursor
- Codex CLI
- opencode
- Hermes Agent

### 支持的语言（19+）
TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Scala, Dart, Svelte, Vue, Liquid, Pascal/Delphi, Lua, Luau

## 安装步骤

### 步骤 1：安装 CodeGraph

**方式一：curl 一键安装（推荐）**

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex
```

> 特点：CodeGraph 自带运行时，无需 Node.js 环境

**方式二：npm 安装**

```bash
npx @colbymchenry/codegraph        # 零安装运行
npm i -g @colbymchenry/codegraph   # 全局安装
```

### 步骤 2：运行交互式安装器

```bash
npx @colbymchenry/codegraph
```

安装器会依次询问：
1. **选择要配置的 Agent** — 自动检测已安装的 Agent
2. **安装位置** — 全局或项目本地
3. **写入配置** — MCP 服务器配置 + Agent 指令文件
4. **设置权限** — 为 Claude Code 配置自动允许列表

**非交互式安装（CI/脚本）**：

```bash
# 自动检测 agent，全局安装
codegraph install --yes

# 指定 agent 列表
codegraph install --target=cursor,claude --yes

# 检测 agent，项目本地安装
codegraph install --target=auto --location=local
```

### 步骤 3：重启 Agent

安装完成后，重启你的 AI 编程助手（Claude Code / Cursor / Codex CLI），让 MCP 服务器加载生效。

### 步骤 4：初始化项目

```bash
cd your-project
codegraph init -i
```

这会在项目目录创建 `.codegraph/` 文件夹并构建代码索引。

> 索引完成后，Agent 会自动使用 CodeGraph 工具（当 `.codegraph/` 目录存在时）

## 常用命令

### 项目管理

| 命令 | 说明 |
|------|------|
| `codegraph init [path]` | 初始化项目（加 `--index` 同时索引） |
| `codegraph uninit [path]` | 移除项目本地索引 |
| `codegraph index [path]` | 完整索引（加 `--force` 重新索引） |
| `codegraph sync [path]` | 增量更新索引 |
| `codegraph status [path]` | 查看索引状态 |

### 符号查询

| 命令 | 说明 |
|------|------|
| `codegraph query <search>` | 搜索符号 |
| `codegraph callers <symbol>` | 查找谁调用了这个函数 |
| `codegraph callees <symbol>` | 查找这个函数调用了什么 |
| `codegraph impact <symbol>` | 分析符号变更的影响范围 |
| `codegraph context <task>` | 为 AI 任务构建代码上下文 |

### 代码影响分析（CI 集成）

```bash
# 查找受变更影响的测试文件
codegraph affected src/utils.ts src/api.ts

# 从 git diff 获取变更文件
git diff --name-only | codegraph affected --stdin

# CI/hook 集成示例
#!/usr/bin/env bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
if [ -n "$AFFECTED" ]; then
  npx vitest run $AFFECTED
fi
```

### 卸载

```bash
# 移除所有 agent 的配置
codegraph uninstall

# 移除项目本地索引
codegraph uninit

# 指定移除特定 agent
codegraph uninstall --target=cursor,claude --yes
```

## MCP 工具集

当作为 MCP 服务器运行时，CodeGraph 提供以下工具：

| 工具 | 用途 |
|------|------|
| `codegraph_search` | 按名称搜索符号 |
| `codegraph_context` | 为任务构建代码上下文 |
| `codegraph_callers` | 查找函数调用者 |
| `codegraph_callees` | 查找函数被调用者 |
| `codegraph_impact` | 分析符号变更影响 |
| `codegraph_node` | 获取符号详情（可含源码） |
| `codegraph_explore` | 返回相关符号源码和关系图 |
| `codegraph_files` | 获取索引文件结构 |
| `codegraph_status` | 检查索引健康状态 |

## 性能基准

官方测试结果（7 个开源项目，4 次运行中位数）：

| 项目 | 语言 | 文件数 | 成本降低 | Token 减少 | 时间加快 | 工具调用减少 |
|------|------|--------|----------|-----------|----------|-------------|
| VS Code | TypeScript | ~10k | 35% | 73% | 41% | 72% |
| Excalidraw | TypeScript | ~600 | 47% | 73% | 60% | 86% |
| Django | Python | ~2.7k | 34% | 64% | 59% | 81% |
| Tokio | Rust | ~700 | 52% | 81% | 63% | 89% |
| OkHttp | Java | ~640 | 17% | 41% | 36% | 64% |
| Gin | Go | ~150 | 22% | 23% | 34% | 19% |
| Alamofire | Swift | ~100 | 38% | 59% | 51% | 77% |

> **平均**：35% 更便宜 · 59% 更少 Token · 49% 更快 · 70% 更少工具调用

测试条件：Claude Opus 4.7, Claude Code v2.1.145，`claude -p` 模式

## 工作原理

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│  "How does the auth system work?"                                │
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
│                          ▼                                        │
│              ┌───────────────────────┐                            │
│              │   SQLite Graph DB     │                            │
│              │   (FTS5 全文搜索)     │                            │
│              └───────────────────────┘                            │
└───────────────────────────────────────────────────────────────────┘
```

1. **解析**：tree-sitter 将源码解析为 AST
2. **提取**：语言特定查询提取节点（函数、类）和边（调用、导入）
3. **存储**：存入本地 SQLite 数据库
4. **同步**：文件监视器监听变更，增量同步

## Framework-aware Routes

CodeGraph 识别 14 种 Web 框架的路由模式：

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

## 踩坑记录

> [!warning] 坑点 1：CodeGraph not initialized
> **现象**：Agent 提示 "CodeGraph not initialized"
> **原因**：项目目录没有 `.codegraph/` 文件夹
> **解决**：在项目目录运行 `codegraph init -i`

> [!warning] 坑点 2：数据库锁定
> **现象**：`database is locked` 错误
> **原因**：WAL 模式未启用（常见于网络共享和 WSL2）
> **解决**：确认使用最新版本，项目放在本地磁盘

> [!warning] 坑点 3：索引慢
> **现象**：首次索引很慢
> **原因**：`node_modules` 等大目录可能未被排除
> **解决**：确保 `.gitignore` 正确配置，使用 `--quiet` 减少输出

## 延伸

- 这篇笔记让你能做什么：为你的 AI 编程助手配置 CodeGraph，在大型代码库中快速定位符号、追踪调用链、分析影响范围
- 下一步可以学什么：[待补充]
- 相关实战：[待补充]

## 数据来源

- [GitHub 官方仓库](https://github.com/colbymchenry/codegraph) [来源: R1]
- [CodeGraph Documentation](https://codegraph.ru/docs/en/index.html) [来源: R2]
