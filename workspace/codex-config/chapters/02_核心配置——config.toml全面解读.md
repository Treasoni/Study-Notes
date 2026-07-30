---
title: 核心配置 —— config.toml 全面解读
tags: [codex, config, toml, sandbox, permissions, profiles, security]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# 核心配置 —— config.toml 全面解读

第一章我们建立了 Codex 配置体系的整体地图。现在，让我们聚焦最核心的部分 —— `config.toml`。这个文件是 Codex 的"控制中心"，几乎所有关于行为、安全、模型、扩展的配置都在这里定义。如果你熟悉 Claude Code 的 `settings.json`，你会发现 Codex 的 `config.toml` 在功能上覆盖了更多维度：安全沙箱、审批策略、权限系统、多环境配置档、多模型提供商……本章将逐区块深入解读，并在最后给出一个完整的配置示例和对照表。

## 1. 五层优先级回顾与合并机制

第一章已经介绍了五层优先级的基本概念。这里我们进一步深入：**当多层配置都存在时，它们是如何合并的？**

### 1.1 优先级总览

| 优先级 | 层级 | 来源 | 典型用途 |
|--------|------|------|---------|
| 1（最高） | 托管配置 | `requirements.toml`（管理员管理） | 企业安全合规强制策略 |
| 2 | CLI 参数 | `codex -c key=value` | 临时调试、一次性覆盖 |
| 3 | Profile | `codex --profile NAME` -> `[profiles.NAME]` | 按场景切换（快速/深度/审查） |
| 4 | 项目配置 | `.codex/config.toml` | 团队共享的项目默认值 |
| 5（最低） | 用户配置 | `~/.codex/config.toml`（或 `$CODEX_HOME`） | 个人偏好 |

### 1.2 合并规则

Codex 的配置合并遵循 **"细粒度覆盖"** 原则：不是整层替换，而是按单个键逐级覆盖。

```toml
# 层级 5（用户配置）：设置了一个低优先级的安全策略
sandbox_mode = "read-only"
approval_policy = "untrusted"

# 层级 4（项目配置）：覆盖了 sandbox_mode，但 approval_policy 保持用户配置的值
# .codex/config.toml
sandbox_mode = "workspace-write"

# 最终生效：
# sandbox_mode = "workspace-write"   ← 来自项目配置（覆盖了用户的 read-only）
# approval_policy = "untrusted"      ← 来自用户配置（项目配置未定义，保留）
```

这个机制与 Claude Code 的 settings.json 合并方式类似，但 Codex 多了两个中间层（Profile 和 CLI 参数），让覆盖更加灵活。

> **Claude Code 对照**：Claude Code 的合并路径是 `settings.local.json` -> `settings.json`（用户级） -> `settings.json`（项目级），只有三层且 `local` 是最低优先级而不是运行时覆盖。Codex 的 `-c` 参数相当于运行时最高优先级的临时覆盖，Claude Code 没有完全对应的机制。

### 1.3 三组互斥配置区块

理解下面三组区块的关系，是正确配置 `config.toml` 的关键：

- **第一组：`sandbox_mode` + `approval_policy`** —— 经典安全模型，三档沙箱 + 三档审批
- **第二组：`[permissions.*]`** —— 新一代权限系统，更细粒度的文件/网络控制
- **第三组：`profiles`** —— 将前两组打包成命名配置档，按场景一键切换

三者关系是：**如果你使用了 `[permissions]` 区块，它会完全覆盖 `sandbox_mode` 和 `approval_policy` 的顶层设置**。而 `profiles` 可以包含前两者的任意组合。

## 2. 安全限定：哪些键只能在用户级设置？

这是 Codex 安全模型的第一道防线，也是与 Claude Code 最显著的差异之一。让我们从原理到实践完整理解。

### 2.1 原理

项目级的 `.codex/config.toml` 会提交到 Git 仓库。如果恶意提交者在项目配置中写入了 `sandbox_mode = "danger-full-access"` 和 `approval_policy = "never"`，所有 clone 这个仓库的用户都会在不安全的状态下运行。为此，Codex 规定：**部分安全敏感和系统级的配置键只能在用户级 `~/.codex/config.toml` 中设置，项目级写入会被静默忽略**（不会报错，不会警告，只是不生效）。

### 2.2 完整静默忽略列表

```toml
# ============================================
# 以下键只允许在用户级 ~/.codex/config.toml 设置
# 写在项目级 .codex/config.toml 会被静默忽略
# ============================================

# --- 网络与模型提供商（涉及 API 密钥流向） ---
openai_base_url              # OpenAI API 基础地址
chatgpt_base_url             # ChatGPT 地址
model_provider               # 默认模型提供商
model_providers              # 自定义提供商定义

# --- 安全策略（涉及用户系统安全） ---
approval_policy              # 审批策略
sandbox_mode                 # 沙箱模式
sandbox_workspace_write.*    # 沙箱可写子配置的全部字段

# --- 系统级配置 ---
notify                       # 通知
profile                      # 默认配置档
profiles                     # 多环境配置档定义

# --- 其他 ---
experimental_realtime_ws_base_url  # 实验性实时 WebSocket
otel.*                              # OpenTelemetry 遥测配置
apps_mcp_product_sku                # 产品 SKU
```

### 2.3 与 Claude Code 的对比

| 对比项 | Codex | Claude Code |
|--------|-------|-------------|
| 项目级安全策略 | 静默忽略（不可覆盖） | 可直接写入项目 settings.json |
| 错误提示 | 无（静默忽略，可能让用户困惑） | 无特殊限制 |
| 设计意图 | 防止仓库恶意配置危害用户 | 信任用户对项目的判断 |
| 用户控制力 | 用户级配置永远拥有最终安全控制权 | 项目可覆盖用户级安全设置 |

> **陷阱警示**：因为静默忽略不报错，你可能在项目配置中写了 `sandbox_mode = "danger-full-access"` 却发现始终不生效。排查半天才意识到这个安全限定。请记住：**所有以 `sandbox_`、`approval_`、`model_provider` 开头的键，都请直接写在用户级配置中。**

## 3. sandbox_mode 沙箱模式 —— 安全的第一道防线

沙箱模式控制的是 Codex agent 对**文件系统和网络**的访问权限。这是安全模型的第一道防线，Claude Code 没有直接对应的概念 —— Claude Code 的安全是通过 `allow`/`deny`/`ask` 的细粒度规则实现的。

### 3.1 三种模式

| 模式 | 文件系统 | 网络 | 适用场景 |
|------|---------|------|---------|
| `read-only` | 全局可读，不可写入 | 阻止 | 代码审查、阅读文档 |
| `workspace-write` | 可写入 cwd + `$TMPDIR` + `/tmp` + `writable_roots` | 默认阻止（可开启） | 日常开发、代码编辑 |
| `danger-full-access` | 等同于当前用户权限 | 等同于当前用户权限 | 安装软件包、系统管理 |

配置方式很简单：

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"  # 推荐日常使用
```

### 3.2 workspace-write 的精细控制

`workspace-write` 模式下可以通过 `[sandbox_workspace_write]` 子区块进行更精细的配置：

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = [          # 额外可写目录
    "~/code/oss",           # ~/code/oss 下的文件也可写
    "~/Downloads/temp"
]
network_access = true       # 允许出站 HTTP（pip/npm 安装需要）
exclude_tmpdir_env_var = true   # 排除 $TMPDIR 环境变量指向的目录
exclude_slash_tmp = true        # 排除 /tmp 目录
```

> **实战建议**：如果你的工作流涉及安装 npm 包或 Python 包，记得设置 `network_access = true`，否则包管理器无法下载依赖，运行时会卡死。这是最常见的配置错误之一。

### 3.3 与 Claude Code 的安全模式对比

Claude Code 没有 sandbox_mode 的概念。它的安全控制是通过 `settings.json` 中的 `allow`/`deny`/`ask` 模式逐工具配置的，例如：

```json
{
  "tools": {
    "Bash": {
      "allow": "always",
      "allowPatterns": ["npm install *"]
    }
  }
}
```

Codex 的 sandbox_mode 是三档预设策略，粒度更粗但更容易理解和配置。如果 sandbox_mode 不够用，可以结合下一节的 approval_policy 和更下一节的 `[permissions]` 系统来实现细粒度控制。

## 4. approval_policy 审批策略 —— 安全的第二道防线

如果 sandbox_mode 是"能不能做"，approval_policy 就是"做之前要不要问我"。两者配合构成 Codex 的安全矩阵。

### 4.1 三档策略

| 策略 | 行为 | 安全等级 | 适用场景 |
|------|------|---------|---------|
| `untrusted` | 几乎每步操作都询问用户 | 最高 | 不信任的代码、新手学习 |
| `on-request` | 仅在沙箱阻止时询问 | 中等 | 日常开发（推荐） |
| `never` | 完全自主执行 | 最低 | 批处理、自动化流水线 |

```toml
# ~/.codex/config.toml
approval_policy = "on-request"  # 推荐的日常使用
```

> **危险组合警告**：`approval_policy = "never"` 配合 `sandbox_mode = "danger-full-access"` 意味着 Codex agent 拥有完全的自主权 —— 它可以自由读写任何文件、访问任何网络、执行任何命令。除非你完全理解你在做什么（例如 CI/CD 流水线中），否则不要在生产环境中使用这个组合。

### 4.2 细粒度控制（granular）

如果你觉得三档策略太粗糙，可以使用 `granular` 子配置来逐项开关审批：

```toml
# ~/.codex/config.toml
approval_policy = "on-request"

[approval_policy.granular]
sandbox_approval     = true    # 沙箱操作需要审批
request_permissions  = true    # 权限请求需要审批
rules                = true    # 规则触发的审批
skill_approval       = true    # 技能调用需要审批
mcp_elicitations     = false   # MCP 工具调用不需要额外审批
```

这个细粒度配置的作用是：**在 `on-request` 大策略基础上，进一步指定哪些类型的操作必须要经过你同意**。例如将 `mcp_elicitations` 设为 `false`，就可以让 MCP 工具调用不受 `on-request` 的限制自动执行。

### 4.3 与 Claude Code 的审批对照

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 预设模式 | 3 档 + 细粒度 | 无预设模式 |
| 逐工具审批 | 通过 granular 子配置 + permissions 系统 | `allow`/`deny`/`ask` + `allowPatterns`/`denyPatterns` |
| 代码执行 | 受 sandbox_mode + approval_policy 双重控制 | 受 tools.Bash 的 allow/ask/deny 控制 |
| 文件操作 | 受 sandbox_mode writable_roots 控制 | 受 allowPatterns/denyPatterns 控制 |
| 灵活度 | 预设模式 + 细粒度覆盖 | 完全的逐项细粒度配置 |

> **迁移提示**：如果你从 Claude Code 迁移，理解 sandbox_mode + approval_policy 的组合是关键。Claude Code 的 `tools.Bash.allow = "always"` 相当于 `sandbox_mode = "workspace-write"` + `approval_policy = "on-request"`（如果只涉及工作区操作）。但 Codex 的权限是"沙箱先过滤、审批再审"的双层架构，不能直接一对一映射。

## 5. Permissions 新一代权限系统

`sandbox_mode` + `approval_policy` 是经典的安全模型，但从 Codex 较新版本开始，引入了一个更强大的权限系统 —— `[permissions]` 区块。**如果你使用了 `[permissions]`，它会完全取代顶层 `sandbox_mode` 的设置。**

### 5.1 基本结构

```toml
# ~/.codex/config.toml
default_permissions = "scoped"  # 使用名为 "scoped" 的权限配置档

[permissions.scoped]            # 定义一个权限配置档
# ... 具体的权限规则
```

`default_permissions` 指向一个你定义的命名配置档。内置的有三个配置档可以直接使用：
- `:read-only` — 对应 sandbox_mode = "read-only"
- `:workspace` — 对应 sandbox_mode = "workspace-write"  
- `:danger-full-access` — 对应 sandbox_mode = "danger-full-access"

### 5.2 workspace_roots —— 工作区根目录

这是权限系统中最核心的概念。它定义了哪些目录被视为"工作区"，agent 可以自由操作。

```toml
# ~/.codex/config.toml
default_permissions = "scoped"

[permissions.scoped.workspace_roots]
"~/code/my-project"   = true   # 这是一个工作区
"~/code/oss"          = true   # 这也是
"/etc"                = false  # 明确排除
```

`workspace_roots` 的作用是：为后续的 `filesystem` 和 `network` 规则提供一个"根作用域上下文"。在 `filesystem` 规则中引用 `:workspace_roots` 占位符，就可以把规则限定在工作区目录内。

### 5.3 filesystem —— 文件系统规则

```toml
[permissions.scoped.filesystem]
glob_scan_max_depth = 3  # 目录扫描最大深度

".env"            = "deny"          # 全局阻止访问 .env 文件
".git/config"     = "deny"          # 阻止 Git 配置

[permissions.scoped.filesystem.":workspace_roots"]
"."        = "write"                # 工作区内可写
"**/*.env" = "deny"                 # 但工作区内的 .env 文件仍然拒绝
```

这里的规则执行逻辑是：
1. 先在全局级别（无 `:workspace_roots` 的作用域）匹配规则
2. 再在工作区根目录下匹配 `:workspace_roots` 内的规则
3. 更具体的路径匹配优先于通配符

### 5.4 network —— 网络规则

```toml
[permissions.scoped.network]
enabled = true          # 启用网络访问控制
mode    = "limited"     # limited 或 unrestricted

[permissions.scoped.network.domains]
"api.openai.com"    = "allow"      # 允许访问 OpenAI API
"github.com"        = "allow"      # 允许 GitHub
"internal.company"  = "deny"       # 阻止内部网络
"*"                 = "deny"       # 默认拒绝其余所有
```

网络规则的匹配逻辑：
- 域名白名单模式，显式 `allow` 的域名放行
- 显式 `deny` 的域名阻止
- `"*"` 通配符作为默认策略

### 5.5 内置配置档速查

| 内置配置档 | 等价于 | 用途 |
|-----------|--------|------|
| `:read-only` | `sandbox_mode = "read-only"` | 只读审查 |
| `:workspace` | `sandbox_mode = "workspace-write"` | 标准工作模式 |
| `:danger-full-access` | `sandbox_mode = "danger-full-access"` | 完全访问 |

你可以直接用它们：

```toml
# 直接使用内置配置档
default_permissions = ":workspace"

# 或者在其基础上扩展
default_permissions = "my-permissions"

[permissions.my-permissions.filesystem]
"secrets/" = "deny"
```

### 5.6 与 Claude Code 的对照

Claude Code 没有独立的 permissions 系统。它的"权限"是通过三套机制组合实现的：

1. **settings.json 中的工具规则**（allow/deny/ask + 模式匹配）
2. **CLAUDE.md 中的行为约束**（告诉 agent 不要做什么）
3. **系统 prompt 中的安全指令**（内置安全约束）

Codex 的 permission 系统将这些整合为一个结构化的声明式配置，并且通过 `workspace_roots` 实现了基于目录作用域的访问控制 —— 这是 Claude Code 没有的能力。

## 6. Profiles 多环境配置档

Profiles 是 Codex 独有的特色功能 —— Claude Code 没有直接对应的概念。它允许你将一组配置（模型、安全策略、行为设置）打包成一个命名配置档，运行时按需切换。

### 6.1 定义配置档

```toml
# ~/.codex/config.toml（只能在用户级设置！）
# 注意：profiles 区块也在静默忽略列表中

[profiles.fast]
model                  = "gpt-5.4-mini"  # 快速模型
model_reasoning_effort = "low"           # 低推理强度 → 更快响应
sandbox_mode           = "workspace-write"
approval_policy        = "never"         # 完全自主（适合自动化）

[profiles.deep]
model                  = "gpt-5.4"       # 强大模型
model_reasoning_effort = "high"          # 高推理强度 → 更深入思考
sandbox_mode           = "workspace-write"
approval_policy        = "on-request"    # 重要操作需要确认

[profiles.review]
model                  = "gpt-5.4"
model_reasoning_effort = "xhigh"         # 最高推理强度
sandbox_mode           = "read-only"     # 只读审查
approval_policy        = "untrusted"     # 每一步都确认
```

### 6.2 激活配置档

```bash
# 快速模式：适合简单任务、原型开发
codex --profile fast

# 深度模式：适合复杂分析、代码理解
codex --profile deep

# 审查模式：适合代码审查、安全审计
codex --profile review
```

### 6.3 Profile 的优先级位置

回到五层优先级模型：Profile 的优先级位于 CLI 参数（更高）和项目配置（更低）之间。这意味着：

```toml
# 项目级 .codex/config.toml
model = "gpt-5.4-mini"

# 用户级 ~/.codex/config.toml
[profiles.fast]
model = "gpt-5.4"  # 这个会覆盖项目级的 gpt-5.4-mini
```

但 CLI 参数仍然可以覆盖 Profile：

```bash
# 用 fast profile，但临时换模型
codex --profile fast -c model="gpt-5.4"
```

### 6.4 实战场景

| Profile | 场景 | 模型 | 速度 | 安全 |
|---------|------|------|------|------|
| `fast` | 写测试、修小 bug、问简单问题 | 小模型 | 最快 | 信任工作区 |
| `deep` | 重构代码、系统设计、复杂调试 | 大模型 | 最慢但最深入 | 重要操作确认 |
| `review` | PR 审查、安全审计 | 大模型 | 深入 + 严格 | 只读 + 逐项确认 |

> **最佳实践**：为不同任务创建专属 profile。笔者日常常驻 `workspace-write` + `on-request`，遇到需要批处理的场景临时切换到 fast profile，遇到需要深入分析的场景切换到 deep profile。全程不需要手工修改配置文件。

## 7. Model 配置与多提供商

Codex 在模型配置上比 Claude Code 灵活得多。它原生支持多提供商，并且可以通过自定义提供商接入几乎任何兼容 OpenAI API 的服务。

### 7.1 基础模型配置

```toml
# 选择模型
model = "gpt-5.4"

# 推理强度（影响模型思考深度和响应时间）
model_reasoning_effort = "medium"
# 可选值：minimal | low | medium | high | xhigh

# 推理摘要模式
model_reasoning_summary = "auto"
# 可选值：auto | concise | detailed | none

# 输出详细程度
model_verbosity = "medium"
# 可选值：low | medium | high
```

### 7.2 多提供商配置

Codex 内置支持以下提供商：
- `openai` — OpenAI 系列模型
- `ollama` — 本地 Ollama 部署
- `lmstudio` — 本地 LM Studio 部署

```toml
# ~/.codex/config.toml（项目级写入会被静默忽略！）
model_provider = "openai"  # 默认提供商
```

### 7.3 自定义提供商

通过 `[model_providers]` 区块，你可以接入任何兼容 OpenAI API 的服务：

```toml
# ~/.codex/config.toml
model_providers = [
    { name = "Azure", base_url = "https://xxx.openai.azure.com", wire_api = "chat" },
    { name = "OpenRouter", base_url = "https://openrouter.ai/api/v1", env_key = "OPENROUTER_API_KEY" },
    { name = "Gemini", base_url = "https://generativelanguage.googleapis.com/v1beta/openai/", env_key = "GEMINI_API_KEY" }
]
```

或者使用更易读的完整格式：

```toml
# ~/.codex/config.toml
[model_providers.custom]
name       = "My Provider"
base_url   = "https://api.example.com/v1"
wire_api   = "responses"       # chat / completions / responses
env_key    = "MY_API_KEY"      # 从环境变量读取 API 密钥
```

关键字段说明：
- `name` — 显示名称
- `base_url` — API 基础地址
- `wire_api` — API 协议格式（`chat` / `completions` / `responses`），默认为 `chat`
- `env_key` — 从哪个环境变量读取 API 密钥，不设置则使用默认的 `OPENAI_API_KEY`

### 7.4 与 Claude Code 对照

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 默认模型 | GPT 系列（可配置） | Claude 系列 |
| 多提供商 | 内置 openai/ollama/lmstudio + 自定义 | 主要仅 Anthropic |
| 自定义提供商 | 支持（兼容 OpenAI API 即可） | 不支持 |
| 推理强度 | 支持（5 档） | 通过 system prompt 间接控制 |
| verbose 控制 | 支持（3 档） | 无内置 |
| 模型自动切换 | 通过 Profile | 无内置 |

> **迁移提示**：Claude Code 用户切到 Codex 后，最直观的差异就是模型选择。如果你习惯了 Anthropic 的模型，可以考虑通过自定义提供商接入 Anthropic API。但需要注意 `wire_api` 参数的选择 —— Anthropic 的消息格式与 OpenAI 不完全兼容，可能需要使用代理层（如 OpenRouter）做格式转换。

## 8. Features 功能开关

Codex 提供了多个功能开关，用于启用或禁用特定能力。这些开关的默认值已经考虑了大多数使用场景，一般不需要修改，但了解它们有助于排查问题。

### 8.1 完整列表

```toml
[features]
shell_tool           = true    # 命令执行工具（建议保持开启）
hooks                = true    # 生命周期钩子（不需要可关闭）
multi_agent          = true    # 多代理支持
unified_exec         = true    # PTY 统一执行
shell_snapshot       = true    # 快照加速（提升重复执行效率）
network_proxy        = false   # 网络代理（需要时开启）
prevent_idle_sleep   = false   # 阻止系统休眠
memories             = false   # 记忆功能（实验性）
undo                 = false   # 撤销操作
codex_git_commit     = false   # 自动 git commit
```

### 8.2 重点说明

- **`shell_tool`**：最基础的功能。如果关闭，Codex 就无法在终端执行任何命令。确定不需要时再关闭。
- **`hooks`**：如果你没有配置任何 hooks，可以关闭以节省一点点性能，但通常没这个必要。
- **`multi_agent`**：是否允许 Codex 启动子代理。如果你有复杂的并行任务，保持开启。
- **`shell_snapshot`**：会缓存之前执行过的命令结果，如果重复执行相同命令，直接从缓存取结果，大幅提升效率。但如果命令涉及外部状态变化（如数据库查询），建议关闭。
- **`codex_git_commit`**：开启后 Codex 会在每次修改后自动 commit。方便但不一定符合你的工作习惯。需要 `shell_tool = true` 配合。

### 8.3 与 Claude Code 对照

Claude Code 没有集中的 features 开关。它的功能是通过 settings.json 中的特定字段控制的，例如 `allowedTools`、`disableHooks` 等分散在不同位置。Codex 将这组开关集中到 `[features]` 区块中，一目了然。

## 9. Shell 环境策略与项目信任

这两个配置维度涉及 Codex 如何与你的系统环境交互。

### 9.1 Shell 环境策略

控制 Codex agent 执行命令时继承哪些环境变量：

```toml
[shell_environment_policy]
inherit = "core"  # 可选值：all | core | none
```

| 策略 | 行为 |
|------|------|
| `all` | 继承所有环境变量（可能泄漏 API 密钥等敏感信息） |
| `core` | 只继承 PATH、HOME 等核心环境变量（推荐） |
| `none` | 不继承任何环境变量（最安全，但可能导致命令找不到） |

还可以用白名单或黑名单进一步过滤：

```toml
[shell_environment_policy]
inherit = "custom"
include_only = ["PATH", "HOME", "NODE_ENV"]  # 只继承这些
# 或
exclude = ["AWS_SECRET_KEY", "DB_PASSWORD"]  # 排除敏感变量
```

> **安全提示**：如果你使用 `inherit = "all"`，注意你的 API 密钥、数据库密码等环境变量可能会被 agent 看到。推荐日常使用 `core`。

### 9.2 项目信任机制

你可以将特定目录标记为"受信任"或"不受信任"，这会影响到该目录下的项目配置是否被采纳：

```toml
[projects."~/code/work-project"]
trust_level = "trusted"

[projects."~/code/community-project"]
trust_level = "untrusted"
```

当一个项目被标记为 `untrusted` 时，Codex 会对该项目目录下的 `.codex/config.toml` 中的某些配置项采取更严格的限制。这是防止"你 clone 了一个包含恶意配置的仓库"的第二道防线。

### 9.3 与 Claude Code 对照

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| Shell 继承 | 3 档策略 + 白名单/黑名单 | 无内置，通过系统 shell 配置 |
| 项目信任 | `[projects]` 区块标记信任等级 | 无内置 |
| 安全模型 | 系统化（sandbox → approval → permissions → trust） | 分散在工具规则和 prompt 中 |

## 10. 完整配置示例

下面是本章所有核心配置的综合示例。你可以直接使用或修改后保存到 `~/.codex/config.toml` 作为起点。

```toml
# ============================================
# ~/.codex/config.toml — Codex 完整配置示例
# 适用于日常开发 + 多种场景切换
# ============================================

# ---------- 基础模型 ----------
model = "gpt-5.4"
model_reasoning_effort = "medium"
model_reasoning_summary = "auto"
model_verbosity = "medium"

# ---------- 安全沙箱 ----------
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = ["~/code/oss"]
network_access = true          # 允许包管理器下载
exclude_slash_tmp = true       # 排除 /tmp

# ---------- 审批策略 ----------
approval_policy = "on-request"

[approval_policy.granular]
sandbox_approval     = true
request_permissions  = true
rules                = true
skill_approval       = true
mcp_elicitations     = false   # MCP 工具调用无需逐项审批

# ---------- 新一代权限系统（可选，开启后覆盖 sandbox_mode） ----------
# default_permissions = "scoped"
# [permissions.scoped.workspace_roots]
# "~/code" = true
# [permissions.scoped.filesystem]
# glob_scan_max_depth = 3
# [permissions.scoped.filesystem.":workspace_roots"]
# "." = "write"
# "**/*.env" = "deny"
# [permissions.scoped.network]
# enabled = true
# mode = "limited"
# [permissions.scoped.network.domains]
# "api.openai.com" = "allow"
# "github.com" = "allow"
# "*" = "deny"

# ---------- 多环境配置档 ----------
[profiles.fast]
model                  = "gpt-5.4-mini"
model_reasoning_effort = "low"
sandbox_mode           = "workspace-write"
approval_policy        = "never"

[profiles.deep]
model                  = "gpt-5.4"
model_reasoning_effort = "xhigh"
sandbox_mode           = "workspace-write"
approval_policy        = "on-request"

[profiles.review]
model                  = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode           = "read-only"
approval_policy        = "untrusted"

# ---------- 功能开关 ----------
[features]
shell_tool         = true
hooks              = true
multi_agent        = true
shell_snapshot     = true
network_proxy      = false
prevent_idle_sleep = false
memories           = false
undo               = false
codex_git_commit   = false

# ---------- Shell 环境策略 ----------
[shell_environment_policy]
inherit = "core"   # 只继承 PATH、HOME 等核心变量

# ---------- 项目信任 ----------
# [projects."~/code/work-project"]
# trust_level = "trusted"
```

## 11. config.toml vs Claude Code settings.json 核心对照

现在可以基于本章的所有讨论，给出一个逐项的完整对照表了。这是本章重点，也是迁移时的实操参考。

| 配置维度 | Codex config.toml | Claude Code settings.json | 备注 |
|---------|-------------------|--------------------------|------|
| **格式** | TOML（带注释，节结构） | JSON（无注释，嵌套结构） | 结构完全不同，需转换 |
| **配置位置** | 用户：`~/.codex/config.toml`<br>项目：`.codex/config.toml` | 用户：`~/.claude/settings.json`<br>项目：`.claude/settings.json` | 路径不同但层级结构对应 |
| **运行时覆盖** | `-c key=val`（CLI 参数） | `.claude/settings.local.json`（文件） | 方式完全不同 |
| **沙箱模式** | `sandbox_mode` + `[sandbox_workspace_write]` | 无直接对应 | Codex 独有 |
| **审批策略** | `approval_policy` + `[approval_policy.granular]` | `tools.<name>.allow: always/ask/never` | 范式不同 |
| **权限系统** | `[permissions]` 区块（文件 + 网络 + 工作区根） | 无直接对应 | Codex 独有 |
| **多环境配置** | `[profiles.NAME]` | 无内置 | Codex 独有 |
| **模型选择** | `model`（字符串） | `model`（字符串） | 语义相同 |
| **推理强度** | `model_reasoning_effort`（5 档） | 无直接字段（间接控制） | Codex 更显式 |
| **多提供商** | `model_provider` + `[model_providers]` | 不支持 | Codex 独有 |
| **功能开关** | `[features]` 区块（10+ 开关） | 分散在各字段 | Codex 更集中 |
| **Shell 策略** | `[shell_environment_policy]` | 无内置 | Codex 独有 |
| **项目信任** | `[projects."/path"]` trust_level | 无内置 | Codex 独有 |
| **安全限定** | 项目级静默忽略敏感键 | 无硬性隔离 | Codex 更安全 |
| **MCP 配置** | `[mcp_servers.<id>]` TOML | `mcpServers` JSON | 格式不同，语义相近 |
| **Hooks 配置** | `[hooks]` 内联或 `hooks.json` | `hooks` JSON 内嵌 | 结构类似，事件数不同 |
| **注释支持** | 原生支持 `#` | 不支持（JSON 标准） | Codex 更友好 |
| **自定义提供商** | `[model_providers.custom]` 区块 | 不支持 | Codex 独有 |

> 这张表是"配置维度的完整映射"，后续章节还会讨论 skills、agents、MCP 等更深层的配置。但 `config.toml` 本身已经覆盖了安全、模型、场景切换、环境策略等最核心的维度。

## 本章小结

- **五层优先级与合并机制**：Codex 的配置从托管配置到用户配置分五层，细粒度逐键覆盖。理解合并规则是避免"配置不生效"的第一步。
- **安全静默忽略**：部分敏感键（sandbox_mode、approval_policy、model_provider 等）只能在用户级配置中设置，项目级写入不报错也不生效。这是与 Claude Code 最显著的安全设计差异。
- **双层安全模型**：sandbox_mode（文件/网络控制） + approval_policy（审批控制）构建安全矩阵。新版的 `[permissions]` 系统提供更细粒度的文件系统 + 网络规则，使用它会完全覆盖 sandbox_mode。
- **Profiles 多环境配置**：Codex 独有的特色功能，允许你将模型、安全、行为打包成命名配置档（fast/deep/review），通过 `--profile` 一键切换。Claude Code 没有直接对应的概念。
- **模型配置灵活度远超 Claude Code**：支持多提供商（openai/ollama/lmstudio）、自定义提供商（兼容 OpenAI API 的服务）、推理强度 5 档控制、verbosity 控制。
- **功能开关与 Shell 策略**：`[features]` 区块集中管理 10+ 功能开关，`[shell_environment_policy]` 控制环境变量继承范围，推荐日常使用 `inherit = "core"`。

## 下一章预告

`config.toml` 控制的是 Codex 的行为骨架，但真正决定 Codex agent 如何理解你的项目、遵循什么规则、保持什么样的工作习惯的，是**指令与规则系统**。下一章我们将深入 `AGENTS.md` 的分层级联机制、它与 `CLAUDE.md` 的兼容关系，以及独特的 Starlark 规则引擎 —— 这将是 Codex 与 Claude Code 在"行为定义"维度上最有趣的一组对比。
