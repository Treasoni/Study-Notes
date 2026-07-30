---
title: Agents 子代理与 MCP 服务配置
tags: [codex, agents, mcp, model-context-protocol, subagent, stdio, streamable-http, claude-code, approval-mode, tool-control]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# Agents 子代理与 MCP 服务配置

第四章我们深入了 Skills 技能系统——它让 Codex 具备了按需注入场景化能力的能力。但 Skills 本质上是在**主会话上下文**中执行的指令注入。当任务需要独立运行、使用不同的模型配置、或者需要访问完全不同的工具集时，单一线程的主会话就不够用了。

这时就需要两种核心扩展机制来解决问题：

1. **Agents（子代理）** —— 在主会话之外启动独立的代理实例，拥有自己的模型配置、沙箱策略和技能集，可以并行地、隔离地执行任务。
2. **MCP（Model Context Protocol）** —— 通过标准化的协议连接外部工具服务器，让 agent 能够调用本地文件系统操作、远程 API、数据库查询等能力。

本章将分别深入这两种机制，从配置格式到实战示例，并始终与 Claude Code 的对应实现进行对照。

> **Claude Code 对照**：Claude Code 也有子代理机制（通过 `context: fork`），但它的 Agents 在 SKILL.md frontmatter 中声明，不是独立的配置文件。MCP 方面两者概念相同，但配置格式和 CLI 管理方式差异显著。本章会逐一对比。

---

## Part 1：Agents 子代理系统

### 1.1 配置路径与定义格式

Codex 的 Agent 定义使用 TOML 格式，存放在以下路径中：

```text
# 全局代理（所有项目可用）
~/.codex/agents/<name>.toml

# 项目级代理（仅当前项目可见）
<project>/.codex/agents/<name>.toml
```

每个 `.toml` 文件定义一个代理。文件名 `<name>` 就是代理的标识名。来看一个完整的定义：

```toml
# .codex/agents/code-explorer.toml
description = "执行独立的代码库探索任务，分析项目结构、生成文档"
system_prompt = """
你是一个代码探索专家。你的任务是：
1. 先阅读项目 README 和目录结构，理解整体架构
2. 按模块深入分析关键文件
3. 输出结构化的项目文档
请在分析过程中保持严谨，对不确定的内容标注 [需要确认]。
"""
model = "gpt-5.4"
reasoning_effort = "high"
sandbox_mode = "workspace-write"
skills = ["code-explorer", "doc-generator"]
```

**预期结构**：一个完整的代理定义。每个字段的含义见下文。

#### 字段详解

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `description` | 字符串 | 是 | 代理职责的简短描述。Codex 在决定何时启动该代理时参考此字段 |
| `system_prompt` | 字符串 | 否 | 附加的系统指令。会叠加在默认系统提示词之后 |
| `model` | 字符串 | 否 | 该代理使用的模型。不设置则继承主会话的模型配置 |
| `reasoning_effort` | 枚举 | 否 | `minimal` / `low` / `medium` / `high` / `xhigh`。不设置则继承主会话 |
| `sandbox_mode` | 枚举 | 否 | `read-only` / `workspace-write` / `danger-full-access`。覆盖主会话的沙箱策略 |
| `skills` | 字符串数组 | 否 | 该代理自动加载的技能列表（按 name 引用）。代理启动时预加载这些技能 |

> **设计意图**：Agent 定义的核心价值在于**隔离和专业化**。主会话可能配置了保守的沙箱策略（如 `read-only`），但你可以在 explorer 代理中配置 `workspace-write`，让它能写入文件。主会话用 `gpt-5.4-mini` 处理日常对话，deep-research 代理用 `gpt-5.4` + `high` reasoning 处理复杂分析。

### 1.2 三种内置代理

Codex 内置了三个代理，开箱即用：

| 代理名 | 用途 | 特点 |
|--------|------|------|
| `default` | 标准执行代理 | 通用代理，与主会话能力一致。未指定代理时使用此类型 |
| `worker` | 轻量后台任务代理 | 用于执行无需深层推理的后台任务。默认使用 `model_reasoning_effort = "low"`，资源消耗更小 |
| `explorer` | 探索/搜索代理 | 专为代码库探索和搜索设计。默认 `sandbox_mode = "workspace-write"`，允许文件读取和写入搜索结果 |

内置代理的定义同样可以通过创建同名 `~/.codex/agents/` 下的 `.toml` 文件来覆盖：

```toml
# ~/.codex/agents/explorer.toml
# 覆盖内置 explorer 代理的默认配置
description = "快速搜索和分析代码库"
model = "gpt-5.4-mini"
reasoning_effort = "medium"
sandbox_mode = "read-only"
```

### 1.3 全局代理设置

除了单个代理的定义，Codex 还提供了 `[agents]` 全局配置区块，控制子代理系统的整体行为：

```toml
# .codex/config.toml
[agents]
max_threads = 4      # 同时运行的最大子代理数量，默认 2
max_depth   = 3      # 子代理嵌套深度（子代理的子代理层级），默认 2
```

**`max_threads`**：控制并行度。如果你的任务需要同时探索多个目录、或同时调用多个 API，提高这个数值可以加速。但要注意，每个子代理都会消耗 token 和 API 配额。

**`max_depth`**：控制嵌套层级。子代理可以在任务中途再次启动子代理，形成"子任务的子任务"链。`max_depth` 限制了这个链的最大深度。深度为 1 表示只有主会话可以直接启动代理（不允许代理再启动代理）。

```text
# max_depth = 3 时的嵌套示意
主会话 → Agent A（第 1 层）
         → Agent B（第 2 层）
                → Agent C（第 3 层，达到上限，不可再启动新代理）
```

### 1.4 Agents 与 Skills 的关系

Agents 和 Skills 不是二选一的关系——它们是协同工作的：

- **Agent 定义中引用的 skills**：代理启动时会预加载这些技能，相当于该代理的"出厂设置"
- **Agent 执行中的技能调用**：代理运行时仍然可以通过 description 隐式匹配或 `/skill` 显式调用其他技能
- **Skills 中的 fork 声明**：Claude Code 的 `context: fork` 可以在 Skill 中声明启动子代理，但 Codex 中 Skills 不自带 fork 能力——Agent 是由主会话手动启动的

这是两个工具的架构差异：**Claude Code 的 Agent 是 Skill 的一个可选特性（`context: fork`），Codex 的 Agent 是第一等配置实体**。

### 1.5 Codex Agents vs Claude Code Agents 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| **配置格式** | TOML（`.codex/agents/*.toml`） | Markdown + frontmatter（`.claude/agents/*.md`） |
| **发现路径** | `.codex/agents/` / `~/.codex/agents/` | `.claude/agents/` |
| **内置类型** | default / worker / explorer（3 种开箱即用） | 无硬编码类型 |
| **自定义字段** | system_prompt, model, reasoning_effort, sandbox_mode, skills | 只有 context: fork + allowed-tools + $ARGUMENTS |
| **模型配置** | 每个 agent 可指定不同 model + reasoning_effort | 继承主会话模型，不能单独指定 |
| **沙箱策略** | 每个 agent 可指定独立 sandbox_mode | 继承主会话权限 |
| **全局控制** | `[agents]` 区块：max_threads / max_depth | settings.json 中配置 |
| **Skills 关系** | Agent 可预加载技能列表 | Agent 本身就是 Skill 的一个变体 |
| **嵌套深度控制** | `max_depth` 参数控制 | 无显式深度控制 |
| **并行度控制** | `max_threads` 参数控制 | 通过 settings.json 有限控制 |
| **关联方式** | Agent 是独立配置实体，Skills 是 Agent 的可选依赖 | Agent 是 Skill 的可选属性（`context: fork`） |

**核心差异解读**：

Codex 将 Agents 设计为**独立的配置维度**——你可以为不同任务定义完全不同的执行环境（模型 + 推理强度 + 沙箱策略 + 技能组合）。这适合需要严格任务隔离的场景，比如让一个只读的 review 代理和一个可写的 refactor 代理在同一个项目中并行工作。

Claude Code 的 Agents 则更像是 Skills 的一个**扩展属性**——通过在 SKILL.md 中声明 `context: fork`，将特定 Skill 提升为子代理执行。这种方式更轻量，更适合"偶发性的子任务委派"。

> **一句话总结**：Codex 是"先定义 Agent，再赋予它 Skills"；Claude Code 是"先定义 Skill，再声明它可以作为 Agent 执行"。

---

## Part 2：MCP 服务配置

如果说 Agents 解决了"任务执行环境隔离"的问题，MCP（Model Context Protocol）解决的就是"外部工具接入"的问题。MCP 是一个开放的、语言无关的协议，让 LLM agent 能够通过标准化的接口调用外部工具和数据源。

Codex 和 Claude Code 都支持 MCP，理解 Codex 的 MCP 配置方式对于将 Claude Code 配置迁移到 Codex 至关重要。

### 2.1 配置位置

Codex 的 MCP 服务器配置在 `config.toml` 的 `[mcp_servers.<id>]` 区块中定义：

```toml
# 可放在 ~/.codex/config.toml（全局）或 .codex/config.toml（项目级）
[mcp_servers.<你的服务器ID>]
# ... 配置参数
```

`<服务器ID>` 是 MCP 服务器的唯一标识，用于日志和工具命名空间。

### 2.2 传输方式一：STDIO（本地进程）

STDIO 是最常用的传输方式。Codex 启动一个本地子进程，通过标准输入/输出与 MCP 服务器通信。适用于本地安装的工具服务，如文件系统操作、代码分析工具等。

```toml
# .codex/config.toml — STDIO 模式
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed-dir"]
startup_timeout_sec = 10    # 首次启动等待时间，默认 10s
tool_timeout_sec    = 60    # 单个工具调用超时，默认 60s
```

**字段说明**：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `command` | 字符串 | 是 | — | 启动服务器的可执行文件路径 |
| `args` | 字符串数组 | 否 | `[]` | 传递给命令的参数 |
| `startup_timeout_sec` | 整数 | 否 | `10` | 服务器启动超时（秒）。慢服务器需调大 |
| `tool_timeout_sec` | 整数 | 否 | `60` | 每次工具调用的超时（秒）。长任务需调大 |
| `env` | 对象 | 否 | `{}` | 传递给子进程的额外环境变量 |

#### 实战示例：filesystem MCP 服务器

```toml
# .codex/config.toml
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", 
           "/home/user/projects", 
           "/home/user/shared-data"]
startup_timeout_sec = 15
```

启动后，agent 可以调用 `filesystem` 服务器提供的工具来读取、写入、搜索指定目录中的文件。`args` 中的路径限制了该服务器能访问的文件范围——这本身就是一种安全边界。

#### 实战示例：开发者工具组合

```toml
# 多个 STDIO MCP 服务器组合示例
[mcp_servers.github]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-github"]

[mcp_servers.sqlite]
command = "uvx"
args    = ["mcp-server-sqlite", "--db-path", "./dev.db"]
startup_timeout_sec = 15
tool_timeout_sec    = 120  # SQL 查询可能较慢

[mcp_servers.sequential-thinking]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-sequential-thinking"]
startup_timeout_sec = 5
```

### 2.3 传输方式二：Streamable HTTP（远程 API）

Streamable HTTP 是 MCP 的另一传输方式，通过 HTTP 请求连接到远程 MCP 服务器。适用于连接 SaaS 工具、内部 API 或云服务。

```toml
# .codex/config.toml — Streamable HTTP 模式
[mcp_servers.remote_api]
url                      = "https://api.example.com/mcp"
bearer_token_env_var     = "API_TOKEN"     # 从环境变量读取 token
startup_timeout_sec      = 10
tool_timeout_sec         = 60
```

**关键区别**：

| 维度 | STDIO | Streamable HTTP |
|------|-------|-----------------|
| 连接方式 | 本地子进程 stdin/stdout | HTTP 请求（SSE 或流式响应） |
| 部署位置 | 本地安装的工具 | 远程服务器 |
| 认证方式 | 无需认证（本地进程） | Bearer Token（从环境变量读取） |
| 延迟 | 低（进程间通信） | 较高（网络延迟） |
| 适用场景 | 本地开发工具、文件操作 | 远程 API、SaaS 集成 |

> **安全提示**：`bearer_token_env_var` 指定的是**环境变量名**，不是 token 值本身。Codex 在启动时从环境变量中读取实际 token。你的 token 应该放在 `.env` 文件或 shell profile 中，绝不硬写在 config.toml 里。

### 2.4 审批模式

Codex 提供了四种 MCP 审批模式，控制 agent 调用 MCP 工具时是否需要用户确认：

```toml
[mcp_servers.database]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-sqlite", "./prod.db"]
approval_mode = "writes"  # 写操作时需要审批
```

| 模式 | 行为 | 推荐场景 |
|------|------|----------|
| `auto` | 自动执行，不询问用户 | 只读工具、成熟可信的本地工具 |
| `prompt` | 每次调用都提示用户确认 | 高风险操作或新接入的工具 |
| `writes` | **仅写操作**时提示，读操作自动执行 | 文件系统工具、数据库工具（最常用的折中方案） |
| `approve` | 始终需要审批，无论读写 | 对生产环境有影响的工具 |

**审批模式的作用域**：`approval_mode` 是针对单个 MCP 服务器实例设置的，不是针对所有服务器统一设置。这意味着你可以让 `filesystem` 服务器使用 `writes` 模式（读文件自动，写文件审批），同时让 `github` 服务器使用 `auto` 模式（完全自动）。

### 2.5 工具白名单与黑名单

你可以进一步细粒度控制单个 MCP 服务器的工具可见性：

```toml
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
approval_mode = "writes"

# 工具白名单：只开放 read 相关工具
enabled_tools = [
    "read_file",
    "read_multiple_files",
    "search_files",
    "get_file_info"
]

# 或者使用黑名单：禁用危险工具
# disabled_tools = ["write_file", "create_directory", "delete_file"]
```

```toml
[mcp_servers.database]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-sqlite", "./dev.db"]

# 只允许 SELECT 类工具
enabled_tools = ["read_query", "list_tables"]
disabled_tools = ["execute_query"]  # 也可用黑名单叠加
```

**`enabled_tools` vs `disabled_tools`**：

- **白名单模式**（使用 `enabled_tools`）：只列出允许的工具，其他全部禁用。更安全，推荐新接入时使用。
- **黑名单模式**（使用 `disabled_tools`）：禁用特定工具，其他全部允许。灵活但风险较高。
- **两者同时使用**：`enabled_tools` 优先。一个工具只有在白名单中且不在黑名单中时才可用。

#### `required` 参数

```toml
[mcp_servers.essential-service]
command = "node"
args    = ["server.js"]
required = true  # 如果此服务器启动失败，终止整个 Codex 会话
```

`required = true` 表示该 MCP 服务器是会话的关键依赖。如果启动超时或启动后进程退出，Codex 会终止当前会话并报错。对于非关键的 MCP 服务器（如一个可选的天气查询工具），保持默认的 `required = false`。

### 2.6 CLI 管理：codex mcp add

Codex 提供了命令行工具来交互式地添加 MCP 服务器，无需手动编辑 config.toml：

```bash
# 交互式添加 MCP 服务器
codex mcp add

# 或者通过参数直接指定
codex mcp add --name filesystem \
  --command npx \
  --args "-y","@modelcontextprotocol/server-filesystem","/path"
```

**交互式添加的典型流程**：

```text
$ codex mcp add

? What type of MCP server would you like to add? (Use arrow keys)
> STDIO (local process)
  Streamable HTTP (remote URL)

? Enter the server name (ID): filesystem

? Enter the command to run: npx

? Enter arguments (comma-separated): -y,@modelcontextprotocol/server-filesystem,/data

? Startup timeout in seconds (default: 10): 15

? Tool timeout in seconds (default: 60): 60

? Approval mode (auto/prompt/writes/approve): (default: auto) writes

? Enable specific tools only? (leave empty for all): read_file,search_files

? Is this server required? (y/N): n

MCP server 'filesystem' added to ~/.codex/config.toml
```

执行后，Codex 会自动在 config.toml 中生成对应的 `[mcp_servers.filesystem]` 配置区块。

> **Claude Code 对照**：Claude Code 没有等效的 `codex mcp add` 命令。添加 MCP 服务器需要手动编辑 `~/.claude/settings.json` 的 `mcpServers` JSON 块，没有交互式引导。

```bash
# 列出已配置的 MCP 服务器
codex status
```

输出示例：

```text
MCP Servers:
  filesystem    running     STDIO      npx @modelcontextprotocol/server-filesystem
  github        not started STDIO      npx @modelcontextprotocol/server-github
  remote_api    running     HTTP       https://api.example.com/mcp
```

### 2.7 Codex MCP vs Claude Code MCP 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| **配置格式** | TOML `[mcp_servers.<id>]` 区块 | JSON `mcpServers` 对象 |
| **配置文件** | `~/.codex/config.toml` / `.codex/config.toml` | `~/.claude/settings.json` / `.claude/settings.json` |
| **传输方式** | STDIO + Streamable HTTP | STDIO + Streamable HTTP |
| **审批模式** | 4 种：auto / prompt / writes / approve | 规则引擎：allow / deny / ask |
| **CLI 管理** | `codex mcp add` （交互式向导） | 无，手动编辑 settings.json |
| **工具白名单** | `enabled_tools` 数组 | 无独立字段 |
| **工具黑名单** | `disabled_tools` 数组 | `mcp__servername__toolname` 命名约定的 disabledTools |
| **启动超时** | `startup_timeout_sec`（独立设置） | 无独立配置，共享超时 |
| **工具超时** | `tool_timeout_sec`（独立设置） | 无独立配置，共享超时 |
| **必须服务器** | `required = true` 终止失败会话 | 无等效机制 |
| **环境变量传递** | `env` 对象 + `bearer_token_env_var`（环境变量引用） | 通过 shell 环境变量传递 |
| **认证方式** | Bearer Token 从环境变量读取 | 通过 env 字段或 shell 环境 |
| **项目级覆盖** | 可放项目 config.toml 覆盖全局 | 可放项目 settings.json 覆盖全局 |

**核心差异解读**：

1. **审批范式不同**：Codex 的审批模式是针对单个 MCP 服务器实例的"粗粒度开关"（auto/prompt/writes/approve），而 Claude Code 是规则引擎（allow/deny/ask），可以对单个工具设置规则。Codex 的 `enabled_tools`/`disabled_tools` 部分弥补了这种细粒度控制的缺失。

2. **CLI 体验差异**：`codex mcp add` 是 Codex 的显著优势。交互式向导降低了 MCP 配置的认知负担，尤其适合刚接触 MCP 的用户。Claude Code 需要手动编辑 JSON，虽然有 `>` 引导帮助，但容错性不如交互式向导。

3. **超时控制粒度**：Codex 允许为每个 MCP 服务器独立设置 startup timeout 和 tool timeout，而 Claude Code 的 timeout 是全局共享的。这在连接多个不同特性的 MCP 服务器时非常有用——一个慢速的 SQL 数据库服务器不会因为全局 timeout 设置而频繁断连。

4. **环境变量安全**：Codex 的 `bearer_token_env_var` 设计更安全——配置文件中只存变量名，不存值。Claude Code 通常通过 `env` 字段直接传递，或者依赖 shell 环境变量注入。

### 2.8 常见陷阱

1. **startup_timeout_sec 默认 10s 过短**：对于需要编译或下载依赖的 MCP 服务器（特别是 npx 首次运行需要下载包时），10s 可能不够。遇到"服务器启动失败"错误，先尝试调大这个值。

2. **enabled_tools 拼写错误**：MCP 工具名是区分大小写的。如果配置了 `enabled_tools` 但 agent 无法调用任何工具，检查工具名是否与 MCP 服务器暴露的工具名完全一致（可以通过 `codex status` 查看）。

3. **token 泄露风险**：不要直接把 API token 写在 config.toml 中。使用 `bearer_token_env_var` 引用环境变量，或者将敏感值放入 `.env` 文件（Codex 会自动加载项目根目录的 `.env` 文件，但不会显示在日志中）。

4. **required = true 导致会话无法启动**：如果将某个不稳定或需要手动启动的 MCP 服务器设为 `required = true`，该服务器启动失败时会直接终止整个 Codex 会话。谨慎使用 `required = true`，建议仅用于核心基础设施类 MCP 服务器。

---

## 本章小结

- **Agents 是 Codex 的独立子代理系统**，通过 `.codex/agents/<name>.toml` 定义。每个 Agent 可以配置独立的模型、推理强度、沙箱策略和技能组合，实现任务执行环境的完全隔离和专业化。三个内置代理（default/worker/explorer）开箱即用。
- **全局 `[agents]` 配置区块**通过 `max_threads` 和 `max_depth` 控制子代理系统的并行度和嵌套深度。默认为 2 线程 / 2 层深，可根据任务复杂度调整。
- **Codex 将 Agent 设计为"第一等配置实体"**，而 Claude Code 的 Agent 是 Skill 的扩展属性（`context: fork`）。这是两者在代理架构上的根本差异：Codex 先定义 Agent 再赋予它 Skills，Claude Code 先定义 Skill 再声明它可作为 Agent 执行。
- **MCP 配置位于 config.toml 的 `[mcp_servers.<id>]` 区块**，支持两种传输方式：STDIO（本地子进程）和 Streamable HTTP（远程 API）。STDIO 适用于本地安装的工具，Streamable HTTP 适用于远程 SaaS 集成。
- **四种审批模式**（auto / prompt / writes / approve）控制 MCP 工具的调用确认策略。`writes` 模式（写操作时提示）是最实用的折中方案。工具白名单（`enabled_tools`）和黑名单（`disabled_tools`）提供进一步的细粒度控制。
- **`codex mcp add` CLI 命令**提供了交互式 MCP 添加向导，大幅降低配置门槛——这是与 Claude Code（需手动编辑 JSON）在 MCP 管理体验上的核心差异。
- **额外超时控制和安全机制**是 Codex MCP 的显著优势：独立的 `startup_timeout_sec` 和 `tool_timeout_sec`、环境变量引用式的 token 管理（`bearer_token_env_var`）、以及 `required` 参数控制关键性。

## 下一章预告

Agents 和 MCP 解决了"谁来做"和"用什么工具做"的问题。但工具调用前后的自动化流程——比如"每次文件写入后自动运行 linter"或"每次会话启动时加载项目状态报告"——则需要更精细的生命周期钩子系统来处理。下一章我们将深入 Codex 的 **Hooks 生命周期钩子和插件体系**，对比它们与 Claude Code hooks 的 11 种事件 vs 4 种事件的巨大差异。
