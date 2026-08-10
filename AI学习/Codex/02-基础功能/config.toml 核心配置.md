---
title: config.toml 核心配置
tags: [codex, ai, 工具使用, 基础功能, 配置]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# config.toml 核心配置

> [!info] 文档定位
> **一句话定位** - 本篇逐区块解读 Codex 的 `config.toml` 核心配置：五层优先级合并机制、用户级安全限定、沙箱与审批策略、新一代 Permissions 权限系统、Profiles 多环境配置档、模型多提供商、功能开关与 Shell 环境策略，并在最后给出完整配置示例。适合想要精确掌控 Codex 行为与安全边界的用户。

---

## 配置合并与优先级

`config.toml` 是 Codex 的"控制中心"，几乎所有关于行为、安全、模型、扩展的配置都在这里定义。相比 Claude Code 的 `settings.json`，Codex 的 `config.toml` 覆盖了更多维度：安全沙箱、审批策略、权限系统、多环境配置档、多模型提供商。下面先回顾五层优先级，再深入合并机制与三组互斥配置区块。

### 优先级总览

| 优先级 | 层级 | 来源 | 典型用途 |
|--------|------|------|---------|
| 1（最高） | 托管配置 | `requirements.toml`（管理员管理） | 企业安全合规强制策略 |
| 2 | CLI 参数 | `codex -c key=value` | 临时调试、一次性覆盖 |
| 3 | Profile | `codex --profile NAME` -> `[profiles.NAME]` | 按场景切换（快速/深度/审查） |
| 4 | 项目配置 | `.codex/config.toml` | 团队共享的项目默认值 |
| 5（最低） | 用户配置 | `~/.codex/config.toml`（或 `$CODEX_HOME`） | 个人偏好 |

当多层配置都存在时，它们是如何合并的？Codex 的配置合并遵循 **"细粒度覆盖"** 原则：不是整层替换，而是按单个键逐级覆盖。

### 合并规则

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

> **Claude Code 对照**：Claude Code 的合并路径是 `settings.local.json` -> `settings.json`（用户级） -> `settings.json`（项目级），只有三层且 `local` 是最低优先级而不是运行时覆盖。Codex 的 `-c` 参数相当于运行时最高优先级的临时覆盖，Claude Code 没有完全对应的机制。

### 三组互斥配置区块

- **第一组：`sandbox_mode` + `approval_policy`** —— 经典安全模型，三档沙箱 + 三档审批
- **第二组：`[permissions.*]`** —— 新一代权限系统，更细粒度的文件/网络控制
- **第三组：`profiles`** —— 将前两组打包成命名配置档，按场景一键切换

三者关系：**如果你使用了 `[permissions]` 区块，它会完全覆盖 `sandbox_mode` 和 `approval_policy` 的顶层设置**。而 `profiles` 可以包含前两者的任意组合。

---

## 安全限定：用户级专属键

这是 Codex 安全模型的第一道防线，也是与 Claude Code 最显著的差异之一。项目级的 `.codex/config.toml` 会提交到 Git 仓库。如果恶意提交者在项目配置中写入了危险的安全策略，所有 clone 这个仓库的用户都会在不安全的状态下运行。为此，Codex 规定：**部分安全敏感和系统级的配置键只能在用户级 `~/.codex/config.toml` 中设置，项目级写入会被静默忽略**。

```toml
# 以下键只允许在用户级 ~/.codex/config.toml 设置
# --- 网络与模型提供商 ---
openai_base_url, chatgpt_base_url, model_provider, model_providers
# --- 安全策略 ---
approval_policy, sandbox_mode, sandbox_workspace_write.*
# --- 系统级配置 ---
notify, profile, profiles
# --- 其他 ---
experimental_realtime_ws_base_url, otel.*, apps_mcp_product_sku
```

> [!warning] 陷阱警示
> 因为静默忽略不报错，你可能在项目配置中写了 `sandbox_mode = "danger-full-access"` 却发现始终不生效。请记住：**所有以 `sandbox_`、`approval_`、`model_provider` 开头的键，都请直接写在用户级配置中。**

---

## 沙箱模式 sandbox_mode

沙箱模式控制的是 Codex agent 对**文件系统和网络**的访问权限。这是安全模型的第一道防线，Claude Code 没有直接对应的概念。

| 模式 | 文件系统 | 网络 | 适用场景 |
|------|---------|------|---------|
| `read-only` | 全局可读，不可写入 | 阻止 | 代码审查、阅读文档 |
| `workspace-write` | 可写入 cwd + `$TMPDIR` + `/tmp` + `writable_roots` | 默认阻止（可开启） | 日常开发、代码编辑 |
| `danger-full-access` | 等同于当前用户权限 | 等同于当前用户权限 | 安装软件包、系统管理 |

`workspace-write` 模式下可以通过 `[sandbox_workspace_write]` 子区块进行更精细的配置：

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = ["~/code/oss", "~/Downloads/temp"]
network_access = true       # 允许出站 HTTP（pip/npm 安装需要）
exclude_tmpdir_env_var = true
exclude_slash_tmp = true
```

> [!tip] 实战建议
> 如果你的工作流涉及安装 npm 包或 Python 包，记得设置 `network_access = true`，否则包管理器无法下载依赖。这是最常见的配置错误之一。

---

## 审批策略 approval_policy

如果 sandbox_mode 是"能不能做"，approval_policy 就是"做之前要不要问我"。两者配合构成 Codex 的安全矩阵。

| 策略 | 行为 | 安全等级 | 适用场景 |
|------|------|---------|---------|
| `untrusted` | 几乎每步操作都询问用户 | 最高 | 不信任的代码、新手学习 |
| `on-request` | 仅在沙箱阻止时询问 | 中等 | 日常开发（推荐） |
| `never` | 完全自主执行 | 最低 | 批处理、自动化流水线 |

```toml
# ~/.codex/config.toml
approval_policy = "on-request"

[approval_policy.granular]
sandbox_approval     = true
request_permissions  = true
rules                = true
skill_approval       = true
mcp_elicitations     = false   # MCP 工具调用无需逐项审批
```

> [!warning] 危险组合
> `approval_policy = "never"` 配合 `sandbox_mode = "danger-full-access"` 意味着 Codex agent 拥有完全的自主权。除非你完全理解你在做什么（例如 CI/CD 流水线中），否则不要在生产环境中使用这个组合。

---

## Permissions 新一代权限系统

`sandbox_mode` + `approval_policy` 是经典的安全模型，但从 Codex 较新版本开始，引入了一个更强大的权限系统 —— `[permissions]` 区块。**如果你使用了 `[permissions]`，它会完全取代顶层 `sandbox_mode` 的设置。**

```toml
# ~/.codex/config.toml
default_permissions = "scoped"

[permissions.scoped.workspace_roots]
"~/code/my-project"   = true
"~/code/oss"          = true
"/etc"                = false

[permissions.scoped.filesystem]
glob_scan_max_depth = 3
".env"            = "deny"

[permissions.scoped.filesystem.":workspace_roots"]
"."        = "write"
"**/*.env" = "deny"

[permissions.scoped.network]
enabled = true
mode    = "limited"

[permissions.scoped.network.domains]
"api.openai.com"    = "allow"
"github.com"        = "allow"
"*"                 = "deny"
```

内置配置档速查：

| 内置配置档 | 等价于 | 用途 |
|-----------|--------|------|
| `:read-only` | `sandbox_mode = "read-only"` | 只读审查 |
| `:workspace` | `sandbox_mode = "workspace-write"` | 标准工作模式 |
| `:danger-full-access` | `sandbox_mode = "danger-full-access"` | 完全访问 |

---

## Profiles 多环境配置档

Profiles 是 Codex 独有的特色功能 —— Claude Code 没有直接对应的概念。它允许你将一组配置打包成一个命名配置档，运行时按需切换。

```toml
# ~/.codex/config.toml（只能在用户级设置！）
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
```

激活配置档：

```bash
codex --profile fast   # 快速模式：适合简单任务、原型开发
codex --profile deep   # 深度模式：适合复杂分析、代码理解
codex --profile review # 审查模式：适合代码审查、安全审计
```

> [!tip] 最佳实践
> 为不同任务创建专属 profile。笔者日常常驻 `workspace-write` + `on-request`，遇到需要批处理的场景临时切换到 fast profile，遇到需要深入分析的场景切换到 deep profile。

---

## 模型配置与多提供商

Codex 在模型配置上比 Claude Code 灵活得多。它原生支持多提供商，并且可以通过自定义提供商接入几乎任何兼容 OpenAI API 的服务。

```toml
# 基础模型配置
model = "gpt-5.4"
model_reasoning_effort = "medium"  # minimal | low | medium | high | xhigh
model_reasoning_summary = "auto"
model_verbosity = "medium"         # low | medium | high

# 多提供商
model_provider = "openai"  # openai / ollama / lmstudio

# 自定义提供商
[model_providers.custom]
name       = "My Provider"
base_url   = "https://api.example.com/v1"
wire_api   = "responses"       # chat / completions / responses
env_key    = "MY_API_KEY"      # 从环境变量读取 API 密钥
```

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 默认模型 | GPT 系列（可配置） | Claude 系列 |
| 多提供商 | 内置 openai/ollama/lmstudio + 自定义 | 主要仅 Anthropic |
| 自定义提供商 | 支持（兼容 OpenAI API 即可） | 不支持 |
| 推理强度 | 支持（5 档） | 通过 system prompt 间接控制 |

---

## Features 功能开关

```toml
[features]
shell_tool           = true    # 命令执行工具
hooks                = true    # 生命周期钩子
multi_agent          = true    # 多代理支持
unified_exec         = true    # PTY 统一执行
shell_snapshot       = true    # 快照加速
network_proxy        = false   # 网络代理
prevent_idle_sleep   = false   # 阻止系统休眠
memories             = false   # 记忆功能（实验性）
undo                 = false   # 撤销操作
codex_git_commit     = false   # 自动 git commit
```

---

## Shell 环境策略与项目信任

```toml
[shell_environment_policy]
inherit = "core"  # 可选值：all | core | none
```

| 策略 | 行为 |
|------|------|
| `all` | 继承所有环境变量（可能泄漏 API 密钥） |
| `core` | 只继承 PATH、HOME 等核心环境变量（推荐） |
| `none` | 不继承任何环境变量（最安全） |

项目信任机制：

```toml
[projects."~/code/work-project"]
trust_level = "trusted"

[projects."~/code/community-project"]
trust_level = "untrusted"
```

---

## 完整配置示例

```toml
# ============================================
# ~/.codex/config.toml — Codex 完整配置示例
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
network_access = true
exclude_slash_tmp = true

# ---------- 审批策略 ----------
approval_policy = "on-request"
[approval_policy.granular]
sandbox_approval     = true
request_permissions  = true
rules                = true
skill_approval       = true
mcp_elicitations     = false

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
inherit = "core"

# ---------- 项目信任 ----------
# [projects."~/code/work-project"]
# trust_level = "trusted"
```

> [!summary] 本章小结
> 五层优先级与细粒度逐键覆盖的合并机制是 Codex 配置的骨架。部分敏感键只能在用户级配置中设置，项目级写入会被静默忽略。sandbox_mode + approval_policy 构建双层安全模型，新版的 `[permissions]` 系统提供更细粒度的控制。Profiles 多环境配置档是 Codex 独有功能。模型配置灵活度远超 Claude Code，支持多提供商和自定义提供商。

---

## 常见问题

### Q: 我在项目配置 `.codex/config.toml` 里写了 `sandbox_mode`，为什么始终不生效？

**回答**：因为 `sandbox_mode`、`approval_policy`、`model_provider` 等安全敏感和系统级键**只允许在用户级 `~/.codex/config.toml` 中设置**，项目级写入会被**静默忽略**且不报错。你看起来"写了但不生效"其实是安全机制在起作用：项目配置会提交到 Git，如果恶意提交者写入危险策略，所有 clone 仓库的用户都会在不安全状态下运行。请把以 `sandbox_`、`approval_`、`model_provider` 开头的键直接写到用户级配置。

### Q: `sandbox_mode` 和 `approval_policy` 有什么区别？

**回答**：两者构成 Codex 的安全矩阵。`sandbox_mode` 回答"**能不能做**"——控制 agent 对文件系统和网络的访问权限（`read-only` / `workspace-write` / `danger-full-access` 三档）；`approval_policy` 回答"**做之前要不要问**"——控制操作的审批粒度（`untrusted` / `on-request` / `never` 三档）。注意：如果使用了 `[permissions]` 区块，它会**完全取代**顶层 `sandbox_mode` 的设置。

### Q: 为什么设置了 `workspace-write` 后 npm / pip 装不上依赖？

**回答**：`workspace-write` 模式下**网络默认阻止**。如果工作流涉及安装 npm 包或 Python 包，需要在 `[sandbox_workspace_write]` 子区块中设置 `network_access = true` 允许出站 HTTP。这是最常见的配置错误之一。

---

## 最佳实践

### Do's（推荐）

- 把 `sandbox_`、`approval_`、`model_provider` 等安全敏感键**直接写在用户级 `~/.codex/config.toml`**，避免项目级静默忽略的坑
- 日常开发常驻 `workspace-write` + `on-request` 组合，兼顾自由度与安全
- 为不同任务创建专属 profile（如 fast / deep / review），按场景一键切换
- 涉及包安装时在 `[sandbox_workspace_write]` 设置 `network_access = true`
- 需要细粒度文件/网络控制时，使用新一代 `[permissions]` 系统替代顶层沙箱
- 使用 `[shell_environment_policy]` 的 `inherit = "core"`，只继承 PATH、HOME 等核心环境变量

### Don'ts（避免）

- ❌ 不要在项目级 `.codex/config.toml` 写 `sandbox_mode` / `approval_policy`（会被静默忽略）
- ❌ 不要在生产环境使用 `approval_policy = "never"` + `sandbox_mode = "danger-full-access"` 的组合（agent 拥有完全自主权）
- ❌ 不要用 `shell_environment_policy.inherit = "all"`（可能泄漏 API 密钥）
- ❌ 不要在使用 `[permissions]` 的同时还在顶层设置 `sandbox_mode`（前者会完全覆盖后者）

---

## 小结

`config.toml` 是 Codex 的"控制中心"。五层优先级（托管 > CLI > Profile > 项目 > 用户）配合"细粒度逐键覆盖"的合并机制构成配置骨架；部分安全敏感键只能在用户级设置，项目级写入会被静默忽略。`sandbox_mode` + `approval_policy` 是经典双层安全模型，新版 `[permissions]` 系统提供更细粒度的控制且完全取代顶层沙箱设置。Profiles 多环境配置档是 Codex 独有的特色，模型配置支持多提供商与自定义提供商，灵活度远超 Claude Code。日常推荐 `workspace-write` + `on-request` 组合，并用 `network_access = true` 解决包安装的网络问题。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Codex 配置哲学概览]] | 配置体系全景与五层优先级 |
| [[Codex CLI 与调试]] | CLI 命令与配置审计技巧 |
| [[Agents 与 MCP]] | 子代理与 MCP 服务配置 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
