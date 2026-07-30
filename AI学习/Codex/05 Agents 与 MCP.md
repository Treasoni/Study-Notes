---
title: "Codex 完整配置体系"
tags: [codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# 第五章：Agents 子代理与 MCP 服务配置
第四章我们深入了 Skills 技能系统——它让 Codex 具备了按需注入场景化能力的能力。但 Skills 本质上是在**主会话上下文**中执行的指令注入。当任务需要独立运行、使用不同的模型配置、或者需要访问完全不同的工具集时，单一线程的主会话就不够用了。

这时就需要两种核心扩展机制：**Agents（子代理）** 和 **MCP（Model Context Protocol）**。本章将分别深入这两种机制，从配置格式到实战示例，并始终与 Claude Code 的对应实现进行对照。

### Part 1：Agents 子代理系统

#### 1.1 配置路径与定义格式

```text
# 全局代理（所有项目可用）
~/.codex/agents/<name>.toml

# 项目级代理（仅当前项目可见）
<project>/.codex/agents/<name>.toml
```

一个完整的代理定义：

```toml
# .codex/agents/code-explorer.toml
description = "执行独立的代码库探索任务，分析项目结构、生成文档"
system_prompt = """
你是一个代码探索专家。你的任务是：
1. 先阅读项目 README 和目录结构，理解整体架构
2. 按模块深入分析关键文件
3. 输出结构化的项目文档
"""
model = "gpt-5.4"
reasoning_effort = "high"
sandbox_mode = "workspace-write"
skills = ["code-explorer", "doc-generator"]
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `description` | 字符串 | 是 | 代理职责的简短描述 |
| `system_prompt` | 字符串 | 否 | 附加的系统指令 |
| `model` | 字符串 | 否 | 该代理使用的模型 |
| `reasoning_effort` | 枚举 | 否 | `minimal` / `low` / `medium` / `high` / `xhigh` |
| `sandbox_mode` | 枚举 | 否 | 沙箱模式，覆盖主会话设置 |
| `skills` | 字符串数组 | 否 | 代理启动时预加载的技能列表 |

#### 1.2 三种内置代理

| 代理名 | 用途 | 特点 |
|--------|------|------|
| `default` | 标准执行代理 | 通用代理，与主会话能力一致 |
| `worker` | 轻量后台任务代理 | 默认 `reasoning_effort = "low"`，资源消耗更小 |
| `explorer` | 探索/搜索代理 | 默认 `sandbox_mode = "workspace-write"` |

#### 1.3 全局代理设置

```toml
# .codex/config.toml
[agents]
max_threads = 4      # 同时运行的最大子代理数量，默认 2
max_depth   = 3      # 子代理嵌套深度，默认 2
```

#### 1.4 Codex Agents vs Claude Code Agents 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 配置格式 | TOML（`.codex/agents/*.toml`） | Markdown + frontmatter（`.claude/agents/*.md`） |
| 发现路径 | `.codex/agents/` / `~/.codex/agents/` | `.claude/agents/` |
| 内置类型 | default / worker / explorer | 无硬编码类型 |
| 模型配置 | 每个 agent 可指定不同 model | 继承主会话模型 |
| 沙箱策略 | 每个 agent 可指定独立 sandbox_mode | 继承主会话权限 |
| 关联方式 | Agent 是独立配置实体 | Agent 是 Skill 的扩展属性（`context: fork`） |

> **一句话总结**：Codex 是"先定义 Agent，再赋予它 Skills"；Claude Code 是"先定义 Skill，再声明它可以作为 Agent 执行"。

### Part 2：MCP 服务配置

#### 2.1 配置位置

```toml
# 可放在 ~/.codex/config.toml（全局）或 .codex/config.toml（项目级）
[mcp_servers.<你的服务器ID>]
# ... 配置参数
```

#### 2.2 STDIO（本地进程）

```toml
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed-dir"]
startup_timeout_sec = 10
tool_timeout_sec    = 60
```

#### 2.3 Streamable HTTP（远程 API）

```toml
[mcp_servers.remote_api]
url                      = "https://api.example.com/mcp"
bearer_token_env_var     = "API_TOKEN"     # 从环境变量读取 token
startup_timeout_sec      = 10
tool_timeout_sec         = 60
```

#### 2.4 审批模式

| 模式 | 行为 | 推荐场景 |
|------|------|----------|
| `auto` | 自动执行，不询问用户 | 只读工具、成熟可信的本地工具 |
| `prompt` | 每次调用都提示用户确认 | 高风险操作或新接入的工具 |
| `writes` | **仅写操作**时提示，读操作自动执行 | 文件系统工具、数据库工具（最常用） |
| `approve` | 始终需要审批 | 对生产环境有影响的工具 |

#### 2.5 工具白名单与黑名单

```toml
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
approval_mode = "writes"
enabled_tools = ["read_file", "read_multiple_files", "search_files", "get_file_info"]
# disabled_tools = ["write_file", "create_directory", "delete_file"]
```

#### 2.6 CLI 管理：codex mcp add

```bash
# 交互式添加 MCP 服务器
codex mcp add
```

#### 2.7 Codex MCP vs Claude Code MCP 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 配置格式 | TOML `[mcp_servers.<id>]` 区块 | JSON `mcpServers` 对象 |
| 传输方式 | STDIO + Streamable HTTP | STDIO + Streamable HTTP |
| 审批模式 | 4 种：auto / prompt / writes / approve | 规则引擎：allow / deny / ask |
| CLI 管理 | `codex mcp add` 交互式向导 | 无，手动编辑 settings.json |
| 工具白名单 | `enabled_tools` 数组 | 无独立字段 |
| 超时控制 | 每个服务器独立设置 | 全局共享 |

> **本章小结**：Agents 是 Codex 的独立子代理系统，支持独立模型、沙箱和技能组合。三个内置代理开箱即用。Codex 将 Agent 设计为"第一等配置实体"，而 Claude Code 的 Agent 是 Skill 的扩展属性。MCP 配置支持 STDIO 和 Streamable HTTP 两种传输方式，四种审批模式和工具白名单/黑名单提供细粒度控制。`codex mcp add` 交互式向导显著降低了 MCP 配置门槛。

---


---

> [!note] 导航
> [[04 Skills 技能系统|← 上一章]] | [[06 Hooks 与插件|下一章 →]]



