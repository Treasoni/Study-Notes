# Sources for CodeGraph 代码语义分析工具

| # | Title | URL | Author | Date | Type | Authority | Recency | Completeness | Readability | Total |
|---|-------|-----|--------|------|------|-----------|---------|--------------|-------------|-------|
| 01 | CodeGraph GitHub Repository | https://github.com/colbymchenry/codegraph | colbymchenry | 2024-2026 | official | 5 | 5 | 5 | 5 | **20** |
| 02 | CodeGraph Documentation | https://codegraph.ru/docs/en/index.html | CodeGraph Team | - | official | 5 | 4 | 5 | 5 | **19** |
| 03 | How I Simplified Project Dev Using Code Graph | https://medium.com/@learn-simplified/how-i-simplified-project-dev-using-code-graph-f94fefb84648 | Aniket Hingane | 11 months ago | blog | 3 | 4 | 2 | 4 | **13** |
| 04 | GitHub今日第一CodeGraph：给AI装上代码导航仪 | https://www.bilibili.com/video/BV1UwGq6SEiL | MIP耀 | - | video | 2 | 3 | 2 | 3 | **10** |
| 05 | 三大知识图谱CodeGraph，GitNexus，graphify横向对比 | https://www.bilibili.com/video/BV1S4G66FEoB | 君哥聊编程 | - | video | 2 | 3 | 3 | 3 | **11** |
| 06 | Turn Any Codebase Into an Interactive Knowledge Graph | https://dev.to/arshtechpro/understand-anything-turn-any-codebase-into-an-interactive-knowledge-graph-37ed | arshtechpro | - | blog | 3 | 4 | 4 | 4 | **15** |

## Scoring Criteria

| Dimension | 5 | 4 | 3 | 2 | 1 |
|-----------|---|---|---|---|---|
| **Authority** | 官方文档 | 知名作者 | 社区/博客 | 普通内容 | 未知来源 |
| **Recency** | 半年内 | 1年内 | 2年内 | 3年内 | 3年+ |
| **Completeness** | 全面覆盖 | 覆盖要点 | 部分覆盖 | 碎片化 | 残缺 |
| **Readability** | 清晰易读 | 基本清晰 | 基本清晰 | 难以理解 | 难以理解 |

## Knowledge Map

```
CodeGraph 代码语义分析工具
├── 核心概念
│   ├── 知识图谱 (Knowledge Graph)
│   ├── MCP Server 架构
│   ├── tree-sitter AST 解析
│   └── SQLite 存储 + FTS5 全文搜索
├── 安装部署
│   ├── curl 一键安装 (macOS/Linux/Windows)
│   ├── npm 安装
│   └── 交互式安装器
├── 项目初始化
│   ├── codegraph init -i
│   ├── codegraph install
│   └── .codegraph/ 目录结构
├── CLI 命令
│   ├── init/index/sync/status
│   ├── query/search
│   ├── callers/callees/impact
│   └── affected
├── MCP 工具
│   ├── codegraph_search
│   ├── codegraph_context
│   ├── codegraph_callers/callees
│   ├── codegraph_impact
│   ├── codegraph_node
│   ├── codegraph_explore
│   └── codegraph_files/status
├── 性能基准
│   ├── 7个开源项目测试结果
│   ├── 平均 35% 成本降低
│   └── 平均 70% 工具调用减少
├── 支持范围
│   ├── 支持的 Agent (Claude Code/Cursor/Codex/opencode/Hermes)
│   ├── 支持的语言 (19+)
│   └── 支持的框架路由 (14种)
└── 竞品对比
    ├── GitNexus
    ├── Graphify
    └── Understand Anything
```

## Category Classification

### 核心概念 (Core Concepts)
- doc-01: 完整官方文档，包含所有核心概念

### 实战示例 (Practices)
- doc-01: 安装命令、初始化步骤、CLI 参考
- doc-02: 官方文档结构

### 进阶原理 (Advanced)
- doc-01: 工作原理 (tree-sitter → SQLite → Auto-Sync)
- doc-01: Benchmark 方法论
- doc-06: Understand Anything 多 Agent 管道对比

### 竞品对比 (Comparison)
- doc-04: B站介绍视频
- doc-05: 三大工具横向对比
- doc-06: Understand Anything 详细介绍
