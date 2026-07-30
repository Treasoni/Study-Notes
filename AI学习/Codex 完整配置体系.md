---
title: Codex 完整配置体系 —— 与 Claude Code 对照
tags: [codex, claude-code, configuration, migration, toml, starlark, mcp, hooks, skills, agents]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# Codex 完整配置体系 —— 与 Claude Code 对照

> 从 Claude Code 出发，系统掌握 Codex 的配置哲学、核心机制与迁移策略。

如果你熟悉 Claude Code 的配置方式——`settings.json`、`CLAUDE.md`、`.claude/skills/`——那么你已经拥有了理解 Codex 配置的绝佳参照系。但 Codex 并非 Claude Code 的简单复制：它在配置格式、层级结构、安全模型和扩展机制上都做出了截然不同的设计选择。这份笔记将带你从初识 Codex 的配置哲学开始，一路深入到 `config.toml` 的每个区块、`AGENTS.md` 的分层级联、Skills 技能系统的创建与共享、Agents 子代理与 MCP 服务配置、Hooks 生命周期钩子与插件体系、CLI 调试技巧，最后以一份完整的配置对照表和迁移实战收尾。

> 笔记类型：综合笔记（概念对比 + 实操配置）
> 预计阅读时间：3-4 小时
> 前置要求：熟悉 Claude Code 的基本配置，了解 JSON / TOML 格式

---

## 目录

1. [第一章：从 Claude Code 到 Codex —— 配置哲学概览](#第一章从-claude-code-到-codex--配置哲学概览)
   - [1. 两种配置哲学](#1-两种配置哲学)
   - [2. 配置格式差异：TOML vs JSON](#2-配置格式差异toml-vs-json)
   - [3. 配置层级与优先级](#3-配置层级与优先级)
   - [4. 配置文件目录结构对比](#4-配置文件目录结构对比)
2. [第二章：核心配置 —— config.toml 全面解读](#第二章核心配置--configtoml-全面解读)
   - [1. 五层优先级回顾与合并机制](#1-五层优先级回顾与合并机制)
   - [2. 安全限定：哪些键只能在用户级设置？](#2-安全限定哪些键只能在用户级设置)
   - [3. sandbox_mode 沙箱模式](#3-sandbox_mode-沙箱模式)
   - [4. approval_policy 审批策略](#4-approval_policy-审批策略)
   - [5. Permissions 新一代权限系统](#5-permissions-新一代权限系统)
   - [6. Profiles 多环境配置档](#6-profiles-多环境配置档)
   - [7. Model 配置与多提供商](#7-model-配置与多提供商)
   - [8. Features 功能开关](#8-features-功能开关)
   - [9. Shell 环境策略与项目信任](#9-shell-环境策略与项目信任)
   - [10. 完整配置示例](#10-完整配置示例)
3. [第三章：指令与规则 —— AGENTS.md 分层体系](#第三章指令与规则--agentsmd-分层体系)
   - [1. AGENTS.md 是什么？](#1-agentsmd-是什么)
   - [2. 发现机制与分层级联](#2-发现机制与分层级联)
   - [3. 与 CLAUDE.md 的兼容：fallback 机制](#3-与-claudemd-的兼容fallback-机制)
   - [4. 容量限制与最佳实践](#4-容量限制与最佳实践)
   - [5. 特殊段落](#5-特殊段落)
   - [6. Starlark 规则系统](#6-starlark-规则系统)
   - [7. 验证工具](#7-验证工具)
4. [第四章：Skills 技能系统 —— 创建、注册与共享](#第四章skills-技能系统--创建注册与共享)
   - [1. Skills 是什么？](#1-skills-是什么)
   - [2. Skills 目录结构](#2-skills-目录结构)
   - [3. SKILL.md 深度解析](#3-skillmd-深度解析)
   - [4. 发现路径：五层作用域](#4-发现路径五层作用域)
   - [5. 渐进式延迟加载机制](#5-渐进式延迟加载机制)
   - [6. 启用与禁用 Skill](#6-启用与禁用-skill)
   - [7. agents/openai.yaml：Codex 特有的扩展层](#7-agentsopenaiyamlcodex-特有的扩展层)
   - [8. 内置创建工具：skill-creator 与 skill-installer](#8-内置创建工具skill-creator-与-skill-installer)
   - [9. Skill 共享方案](#9-skill-共享方案)
5. [第五章：Agents 子代理与 MCP 服务配置](#第五章agents-子代理与-mcp-服务配置)
   - [Part 1：Agents 子代理系统](#part-1agents-子代理系统)
   - [Part 2：MCP 服务配置](#part-2mcp-服务配置)
6. [第六章：Hooks 生命周期钩子与插件体系](#第六章hooks-生命周期钩子与插件体系)
   - [Part 1：Hooks 生命周期钩子系统](#part-1hooks-生命周期钩子系统)
   - [Part 2：插件体系](#part-2插件体系)
7. [第七章：CLI 与调试 —— 日常操作与故障排查](#第七章cli-与调试--日常操作与故障排查)
   - [1. 核心 CLI 命令](#1-核心-cli-命令)
   - [2. 交互式命令](#2-交互式命令)
   - [3. 环境变量](#3-环境变量)
   - [4. 调试与验证方法](#4-调试与验证方法)
   - [5. 配置审计技巧](#5-配置审计技巧)
8. [第八章：完整对照表与从 Claude Code 迁移实战](#第八章完整对照表与从-claude-code-迁移实战)
   - [1. 完整对照表](#1-完整对照表)
   - [2. 迁移四步走策略](#2-迁移四步走策略)
   - [3. 常见陷阱 6 条](#3-常见陷阱-6-条)
   - [4. Skills 最佳实践 5 条](#4-skills-最佳实践-5-条)
   - [5. 典型项目配置示例](#5-典型项目配置示例)
   - [6. 迁移检查清单](#6-迁移检查清单)
9. [附录：快速参考卡片](#附录快速参考卡片)

---

## 第一章：从 Claude Code 到 Codex —— 配置哲学概览

如果你熟悉 Claude Code 的配置体系 —— `settings.json`、`CLAUDE.md`、`.claude/skills/` —— 那么你已经拥有了理解 Codex 配置的绝佳参照系。但 Codex 并非 Claude Code 的简单复制：它在配置格式、层级结构、安全模型和扩展机制上都做出了截然不同的设计选择。本章作为全篇的开篇导览，将帮助你建立一个整体的心智模型，理解这两套配置体系的哲学差异和核心对应关系。

### 1. 两种配置哲学

Claude Code 的配置设计偏"应用惯例"：JSON 格式、扁平的目录结构、单文件指令系统。它追求的是**低门槛、快速上手**。

Codex 的配置设计则偏"工程体系"：TOML 格式带来的更强可读性、五层优先级带来的灵活覆盖、分层级联的指令系统和 Starlark 规则引擎。它追求的是**可维护性、安全可控、细粒度扩展**。

> [!abstract] 核心认知
> 这两种哲学的差异并非优劣之分，而是面向不同场景的设计权衡。理解为"Codex 比 Claude Code 更复杂"是片面的——更准确的理解是"Codex 给了你更多主动控制权，但这也意味着你需要做更多的配置决策"。

这两种哲学的差异并非优劣之分，而是面向不同场景的设计权衡。下表从宏观维度给出全景对照：

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 配置格式 | TOML（也支持 YAML/JSON） | JSON |
| 全局配置 | `~/.codex/config.toml` | `~/.claude/settings.json` |
| 项目配置 | `.codex/config.toml` | `.claude/settings.json` |
| 运行时覆盖 | `-c key=val` CLI 参数 | `.claude/settings.local.json` 文件 |
| 指令文件 | AGENTS.md（分层级联，从全局到当前目录逐级拼接） | CLAUDE.md（单文件，路径作用域 rules/） |
| 规则系统 | `.codex/rules/*.rules`（Starlark 语言） | `.claude/rules/*.md`（路径作用域） |
| Skills 目录 | `.agents/skills/` | `.claude/skills/` |
| Skills 标准 | Agent Skills Standard（**完全相同**） | Agent Skills Standard（**完全相同**） |
| 子代理配置 | `.codex/agents/*.toml`（TOML 格式） | `.claude/agents/*.md`（Markdown + frontmatter） |
| MCP 配置 | `[mcp_servers]` TOML 区块 | `mcpServers` JSON 字段 |
| Hooks 事件 | 11 种事件（含 PreCompact、SubagentStart 等） | 4 种核心事件 |
| 权限模型 | sandbox_mode + approval_policy + permissions 区块 | allow/deny/ask 细粒度 |
| 多环境配置档 | 内置 `[profiles]` 支持 | 无内置 |
| 插件系统 | 独立 `.codex-plugin/` 体系 | 无 |
| 多模型提供商 | 内置 openai/ollama/lmstudio + 自定义 | 主要 Anthropic |

> 这张表是全篇的"地图"。后续每章将深入其中一个或几个维度，逐一展开细节和实操。你现在不需要记住所有行，只需建立"Codex 的配置维度比 Claude Code 更丰富"的认知即可。

### 2. 配置格式差异：TOML vs JSON

#### 2.1 为什么是 TOML？

如果你打开过 Claude Code 的 `settings.json`，你会发现它是一份典型的 JSON 配置文件 —— 机器友好，但对于人类来说，缺少注释支持、结尾逗号严格、层级一深可读性就下降。

Codex 选择 TOML 作为主配置格式，核心原因有三：

1. **原生支持注释**：TOML 使用 `#` 注释，可以直接在配置文件中写说明文档
2. **隐式表结构**：`[section]` 语法让配置分节一目了然
3. **更宽松的语法**：允许尾部逗号、多行字符串、多种数据类型

#### 2.2 基本语法对照

来看一个直接对比。Claude Code 的 JSON 配置：

```json
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 8192,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'running bash'"
          }
        ]
      }
    ]
  }
}
```

对应的 Codex TOML 配置：

```toml
model = "gpt-5.4"

[hooks.PreToolUse]
matcher = "Bash"

  [[hooks.PreToolUse.hooks]]
  type = "command"
  command = "echo 'running bash'"
```

差异很明显：
- JSON 的嵌套通过花括号和缩进表达，TOML 通过**节头（section header）** 表达
- TOML 使用 `[section]` 表示一个节，`[[array]]` 表示一个数组元素
- TOML 不需要在最后一个键值对后面加逗号，JSON 严格禁止尾部逗号
- TOML 的键值对使用 `=` 而非 `:`

#### 2.3 TOML 常用数据类型速览

如果你是第一次接触 TOML，下面这张速查表可以帮助你快速上手：

```toml
# 字符串
name = "Codex"
path = 'raw string'  # 单引号不转义

# 整数 / 浮点数
timeout = 60
rate = 3.14

# 布尔值
enabled = true
debug_enabled = false

# 日期时间
created = 2026-07-31T10:00:00Z

# 数组（方括号）
skills = ["code-review", "testing"]

# 表/节
[permissions.network]
enabled = true

# 数组表（多个相同结构的节）
[[skills.config]]
path = "/path/to/skill1"
enabled = true

[[skills.config]]
path = "/path/to/skill2"
enabled = false
```

### 3. 配置层级与优先级

这是 Codex 配置体系中最核心的设计之一 —— **五层优先级**。理解它，你就理解了"一个配置项最终取什么值"的决策路径。

#### 3.1 五层优先级（从高到低）

```toml
# 层级 1：托管配置（requirements.toml）
# 企业级强制配置，由管理员管理，写入后不可被下层覆盖

# 层级 2：CLI 运行时参数
# 临时覆盖，只对当前会话生效
# 用法：codex -c sandbox_mode="danger-full-access"

# 层级 3：Profile 配置档（--profile NAME）
# 按场景切换的命名配置集

# 层级 4：项目配置（.codex/config.toml）
# 仓库级默认配置，团队成员共享

# 层级 5：用户全局配置（~/.codex/config.toml）
# 个人偏好默认值，优先级最低
```

> 层级数字越小优先级越高。层级 1（托管配置）最高，层级 5（用户配置）最低。

这里有一个 Claude Code 用户会感到熟悉但又不同的设计：

- **Claude Code** 用 `.claude/settings.local.json` 做本地覆盖，**不参与层级**，而是直接合并
- **Codex** 用 `-c` 参数做运行时覆盖，**明确属于优先级层级**，且是第二高的层级

#### 3.2 安全限定：哪些配置只能在用户级设置？

Codex 有一个重要的安全机制：**部分敏感配置键只能写在用户级 `~/.codex/config.toml` 中**，如果写在项目级 `.codex/config.toml`，会被静默忽略。这是为了防止仓库中的恶意配置文件危害你的系统。

这些受限制的键包括：

```toml
# 以下配置只能在用户级 ~/.codex/config.toml 中设置
openai_base_url       # OpenAI API 地址
chatgpt_base_url      # ChatGPT 地址
model_provider        # 模型提供商
model_providers       # 多提供商配置（自定义提供商）
approval_policy       # 审批策略（untrusted / on-request / never）
sandbox_mode          # 沙箱模式
sandbox_workspace_write.*  # 沙箱可写目录配置
notify                # 通知
profile               # 默认 profile
profiles              # 多环境配置档定义
otel.*                # 遥测配置
```

> 这一点与 Claude Code 差异很大。Claude Code 的项目级 settings.json 和用户级 settings.json 在安全策略上没有硬性隔离，而 Codex 做了明确的**静默忽略** —— 项目配置写了也不生效，且不会给出错误提示。

### 4. 配置文件目录结构对比

#### 4.1 顶层对比

```
Claude Code 项目结构                  Codex 项目结构
======================                ==================

.claude/                              .codex/
├── settings.json                     ├── config.toml        ← 核心配置
├── settings.local.json               ├── agents/            ← 子代理定义
├── skills/                           │   └── *.toml
│   └── <name>/                      ├── rules/             ← Starlark 规则
├── agents/                           │   └── *.rules
│   └── *.md                         ├── hooks.json         ← 生命周期钩子
├── rules/                            └── plugins/          ← 插件目录
│   └── *.md
└── CLAUDE.md                         .agents/              ← Skills 目录
                                      └── skills/
```

#### 4.2 用户级全局目录对比

```
~/.claude/                            ~/.codex/（或 $CODEX_HOME）
├── settings.json                     ├── config.toml
├── skills/                           ├── AGENTS.override.md
│   └── <name>/                      ├── AGENTS.md
├── agents/                           ├── agents/
│   └── *.md                         │   └── *.toml
└── CLAUDE.md                         ├── hooks.json
                                      └── skills/
```

从目录结构可以直观感受到两套体系的差异：

| 对比项 | Claude Code | Codex |
|--------|-------------|-------|
| 顶层目录名 | `.claude/` | `.codex/` |
| 核心配置格式 | JSON 文件（settings.json） | TOML 文件（config.toml） |
| 指令文件 | `CLAUDE.md`（项目根，单文件） | `AGENTS.md`（全局+多级级联） |
| 规则机制 | `.claude/rules/*.md`（Markdown 说明） | `.codex/rules/*.rules`（Starlark 编程语言） |
| Skills 发现 | `.claude/skills/` | `.agents/skills/` |
| 子代理定义 | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| 钩子配置 | 内嵌在 settings.json 中 | 独立 `hooks.json` 或内嵌 TOML |
| 多环境配置 | 无内置 | `[profiles]` 配置档 |
| 插件系统 | 无 | `.codex/plugins/` 独立体系 |

> **本章小结**：Codex 的配置体系比 Claude Code 更丰富和工程化，覆盖了配置格式、层级优先级、安全限制、多环境配置档等更多维度。TOML 提供原生注释、更直观的节结构、更宽松的语法。五层优先级机制是 Codex 配置的骨架，安全敏感配置只能在用户级设置。`.codex/` 对应 `.claude/`、`AGENTS.md` 对应 `CLAUDE.md`、`.agents/skills/` 对应 `.claude/skills/`，但每个维度在 Codex 中都有延伸和增强。

---

## 第二章：核心配置 —— config.toml 全面解读

第一章我们建立了 Codex 配置体系的整体地图。现在，让我们聚焦最核心的部分 —— `config.toml`。这个文件是 Codex 的"控制中心"，几乎所有关于行为、安全、模型、扩展的配置都在这里定义。如果你熟悉 Claude Code 的 `settings.json`，你会发现 Codex 的 `config.toml` 在功能上覆盖了更多维度：安全沙箱、审批策略、权限系统、多环境配置档、多模型提供商……本章将逐区块深入解读，并在最后给出一个完整的配置示例和对照表。

### 1. 五层优先级回顾与合并机制

第一章已经介绍了五层优先级的基本概念。这里我们进一步深入：**当多层配置都存在时，它们是如何合并的？**

#### 1.1 优先级总览

| 优先级 | 层级 | 来源 | 典型用途 |
|--------|------|------|---------|
| 1（最高） | 托管配置 | `requirements.toml`（管理员管理） | 企业安全合规强制策略 |
| 2 | CLI 参数 | `codex -c key=value` | 临时调试、一次性覆盖 |
| 3 | Profile | `codex --profile NAME` -> `[profiles.NAME]` | 按场景切换（快速/深度/审查） |
| 4 | 项目配置 | `.codex/config.toml` | 团队共享的项目默认值 |
| 5（最低） | 用户配置 | `~/.codex/config.toml`（或 `$CODEX_HOME`） | 个人偏好 |

#### 1.2 合并规则

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

> **Claude Code 对照**：Claude Code 的合并路径是 `settings.local.json` -> `settings.json`（用户级） -> `settings.json`（项目级），只有三层且 `local` 是最低优先级而不是运行时覆盖。Codex 的 `-c` 参数相当于运行时最高优先级的临时覆盖，Claude Code 没有完全对应的机制。

#### 1.3 三组互斥配置区块

- **第一组：`sandbox_mode` + `approval_policy`** —— 经典安全模型，三档沙箱 + 三档审批
- **第二组：`[permissions.*]`** —— 新一代权限系统，更细粒度的文件/网络控制
- **第三组：`profiles`** —— 将前两组打包成命名配置档，按场景一键切换

三者关系：**如果你使用了 `[permissions]` 区块，它会完全覆盖 `sandbox_mode` 和 `approval_policy` 的顶层设置**。而 `profiles` 可以包含前两者的任意组合。

### 2. 安全限定：哪些键只能在用户级设置？

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

> **陷阱警示**：因为静默忽略不报错，你可能在项目配置中写了 `sandbox_mode = "danger-full-access"` 却发现始终不生效。请记住：**所有以 `sandbox_`、`approval_`、`model_provider` 开头的键，都请直接写在用户级配置中。**

### 3. sandbox_mode 沙箱模式

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

> **实战建议**：如果你的工作流涉及安装 npm 包或 Python 包，记得设置 `network_access = true`，否则包管理器无法下载依赖。这是最常见的配置错误之一。

### 4. approval_policy 审批策略

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

### 5. Permissions 新一代权限系统

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

### 6. Profiles 多环境配置档

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

> **最佳实践**：为不同任务创建专属 profile。笔者日常常驻 `workspace-write` + `on-request`，遇到需要批处理的场景临时切换到 fast profile，遇到需要深入分析的场景切换到 deep profile。

### 7. Model 配置与多提供商

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

### 8. Features 功能开关

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

### 9. Shell 环境策略与项目信任

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

### 10. 完整配置示例

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

> **本章小结**：五层优先级与细粒度逐键覆盖的合并机制是 Codex 配置的骨架。部分敏感键只能在用户级配置中设置，项目级写入会被静默忽略。sandbox_mode + approval_policy 构建双层安全模型，新版的 `[permissions]` 系统提供更细粒度的控制。Profiles 多环境配置档是 Codex 独有功能。模型配置灵活度远超 Claude Code，支持多提供商和自定义提供商。

---

## 第三章：指令与规则 —— AGENTS.md 分层体系

前两章我们分别建立了 Codex 配置体系的全局图景，并深入解读了 `config.toml` 的每个区块。但是，`config.toml` 控制的是"骨架"——安全策略、模型选择、功能开关。真正决定 Codex agent **如何理解你的项目、遵循什么工作规范、使用什么工作协议**的，是指令与规则系统。本章将深入 Codex 的指令文件 `AGENTS.md` 的分层级联机制——这是它与 Claude Code 的 `CLAUDE.md` 最核心的差异之一——以及独特的 `Starlark` 规则引擎。

### 1. AGENTS.md 是什么？

`AGENTS.md` 是 Codex 的指令文件，相当于 Claude Code 的 `CLAUDE.md`。它的作用是告诉 Codex agent：这个项目是什么、有什么规范、应该遵循什么工作方式。

但 Codex 在设计上做了一个关键的差异化选择：**`AGENTS.md` 不是单文件，而是一套分层级联的指令链**。这意味着，你可以为整个组织设定一套全局指令，为每个项目设定一套项目指令，甚至为项目中的不同子目录设定更细粒度的指令——所有指令最终会被拼接合并，形成一个完整的上下文。

> **Claude Code 对照**：Claude Code 的 `CLAUDE.md` 是单文件，放在项目根目录。虽然可以通过 `.claude/rules/` 目录添加额外规则，但这些规则是通过路径作用域加载的，而不是分层级联拼接。这是两种完全不同的设计哲学。

### 2. 发现机制与分层级联

#### 2.1 发现路径

构建过程分为两个阶段：

```
阶段 1：全局层
  ~/.codex/AGENTS.override.md  ── 如果存在，优先使用
  ~/.codex/AGENTS.md            ── 否则使用此文件

阶段 2：项目层（从 Git 根目录向下遍历到当前目录）
  每级目录检查（按优先级从高到低）：
    1. AGENTS.override.md ── 如果存在，使用此文件
    2. AGENTS.md           ── 否则检查此文件
    3. 回退文件名          ── project_doc_fallback_filenames 中配置的文件
```

#### 2.2 合并规则：从根到叶拼接

找到所有指令文件后，Codex 按照**从根到叶**的顺序拼接：

```text
最终指令文档的内容顺序：
┌──────────────────────────────────┐
│  ~/.codex/AGENTS.md              │  ← 全局指令
│  /repo/AGENTS.md                 │  ← 项目根指令
│  /repo/src/AGENTS.md             │  ← 子目录指令
│  /repo/src/components/AGENTS.md  │  ← 当前目录指令（最后加载，优先覆盖）
└──────────────────────────────────┘
```

#### 2.3 文件优先级

在每个目录层级，Codex 按照以下优先级查找指令文件：

| 优先级 | 文件名 | 说明 |
|--------|--------|------|
| 1（最高） | `AGENTS.override.md` | 强制覆盖级指令 |
| 2 | `AGENTS.md` | 标准指令文件 |
| 3（回退） | `project_doc_fallback_filenames` 中的文件名 | 兼容其他工具的指令文件 |

### 3. 与 CLAUDE.md 的兼容：fallback 机制

对于从 Claude Code 迁移过来的用户，Codex 提供了兼容性机制：**通过 `project_doc_fallback_filenames` 配置，让 Codex 在找不到 `AGENTS.md` 时回退读取 `CLAUDE.md`**。

```toml
# .codex/config.toml
project_doc_fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
```

```text
每级目录的查找顺序：
         ┌─────────────┐
         │ AGENTS      │
         │ .override   │ ← 最高优先级
         │ .md         │
         └──────┬──────┘
                │ 不存在？
         ┌──────v──────┐
         │             │
         │ AGENTS.md   │ ← 标准指令
         └──────┬──────┘
                │ 不存在？
         ┌──────v──────┐
         │ fallback 列表 │ ← CLAUDE.md / TEAM_GUIDE.md
         │             │
         └─────────────┘
```

### 4. 容量限制与最佳实践

Codex 对 AGENTS.md 链有硬性的容量限制：

- **默认上限**：**32 KiB**（`project_doc_max_bytes` 配置项控制）
- **超过上限**：超过的部分会被截断，不会加载
- **空文件跳过**：找到的指令文件如果是空文件，直接跳过

分层策略的最佳实践：

```text
~/.codex/AGENTS.md           ← 全局指令：不超过 8 KiB
  ├── 通用行为规范
  ├── 默认编码规范
  └── 工具使用规则

<repo>/AGENTS.md             ← 项目指令：不超过 16 KiB
  ├── 项目描述和技术栈
  ├── 架构约定和命名规范
  ├── 测试要求
  └── 工作流程

<repo>/src/AGENTS.md         ← 模块指令：不超过 8 KiB
  ├── 模块特定规范
  └── 注意事项
```

### 5. 特殊段落

`AGENTS.md` 支持两种具有特殊含义的段落：

**Code Review Rules** —— 针对 GitHub PR 审查的定制规则：

```markdown
# Code Review Rules

- 每次审查最多加载 400 行代码，超过时分批审查
- 重点检查：安全漏洞、性能问题、类型错误
- 每个问题必须标注严重等级（critical / major / minor）
```

**Working Agreements** —— 标准工作协议，自动化行为约定：

```markdown
# Working Agreements

- 修改 JavaScript 文件后运行 `npm test`
- 修改 Go 文件后运行 `go vet ./...`
- 在提交前运行 `npx prettier --write .`
```

> **区分建议**：Code Review Rules 仅在代码审查场景触发；Working Agreements 在任何会话中都可能触发，是日常行为约束。

### 6. Starlark 规则系统

如果说 `AGENTS.md` 是 Codex 的"宪法"，那么 **Starlark 规则系统**就是它的"刑法"——可执行的低层级工具行为控制。

```text
<project>/.codex/rules/
├── safety.rules
├── network.rules
└── file-access.rules
```

三种操作类型：

| 操作 | 含义 | 效果 |
|------|------|------|
| `allow` | 自动允许 | agent 可以直接执行，不通知用户 |
| `prompt` | 提示用户 | agent 执行前询问用户是否批准 |
| `forbidden` | 禁止执行 | agent 无法执行该操作 |

一个完整的 Starlark 规则文件示例：

```python
# .codex/rules/safety.rules
def evaluate(ctx):
    tool = ctx.tool_name
    args = ctx.tool_args

    if tool == "Read" and ".env" in args.get("path", ""):
        return {"decision": "forbidden", "reason": "禁止读取 .env 文件"}

    if tool == "Edit" and "package.json" in args.get("path", ""):
        return {"decision": "prompt", "reason": "修改 package.json 需要确认"}

    if tool == "Bash" and "npm test" in args.get("command", ""):
        return {"decision": "allow", "reason": "测试命令自动放行"}

    return {"decision": "allow"}
```

规则评估逻辑：`forbidden` > `prompt` > `allow`

| 维度 | Codex `.rules`（Starlark） | Claude Code `.claude/rules/*.md` |
|------|---------------------------|----------------------------------|
| 语言 | Starlark（Python 子集，可编程） | Markdown（自然语言描述） |
| 执行方式 | 自动评估 + 决策执行 | 作为上下文提供给 agent，由 agent 自行判断 |
| 决策类型 | `allow` / `prompt` / `forbidden` | 无结构化决策 |
| 确定性 | 高（规则逻辑明确） | 低（依赖 LLM 理解） |

> **核心差异一句话总结**：Codex 的 `.rules` 是**可编程的自动化决策引擎**，而 Claude Code 的 `.claude/rules/` 是**自然语言的行为指南**。

### 7. 验证工具

```bash
# 查看当前工作区状态
codex status

# 审计指令加载
codex --cd src/api "请列出你加载的所有指令文件"
```

> **本章小结**：AGENTS.md 是分层级联的指令链，从全局到子目录逐级拼接。fallback 机制实现了与 CLAUDE.md 的单向兼容。容量限制为 32 KiB。Starlark 规则系统是 Codex 独有的确定性自动化决策引擎。验证工具 `codex status` + `codex --cd` 可以审计指令加载情况。

---

## 第四章：Skills 技能系统 —— 创建、注册与共享

第三章我们深入了 AGENTS.md 的分层级联机制和 Starlark 规则引擎——它们定义了 agent 如何理解项目规范。但指令文件有容量限制（32 KiB），不可能也不应该把所有操作指南塞进 AGENTS.md。真正强大的行为扩展方式是创建**可复用的 Skill（技能）包**：一个 Skill 封装了让 agent 完成特定任务所需的所有指令、脚本和参考文档，可以被跨项目甚至跨工具共享。

本章将全面解析 Codex 的 Skills 系统。> [!note] 关键发现：Skills 可跨工具共享
> Codex 和 Claude Code 共享同一套 **Agent Skills Standard**。只要遵循标准 frontmatter 和目录结构，同一个 Skill 目录可以被两个工具同时发现和加载。这是目前两套配置体系之间**最无缝的桥梁**，也是从 Claude Code 迁移时成本最低的配置维度。

### 1. Skills 是什么？

Skills 是一套**标准化的可复用能力包**。每个 Skill 是一个目录，包含让 agent 完成特定任务的指令（SKILL.md）、可选的辅助脚本（scripts/）、参考文档（references/）和模板资源（assets/）。

**Skill 和 AGENTS.md 的区别**：

| | AGENTS.md | Skill |
|--|-----------|-------|
| 作用范围 | 整个项目/会话 | 特定任务场景 |
| 触发方式 | 自动加载 | 显式调用或 description 隐式匹配 |
| 容量 | 32 KiB 上限 | 无硬性上限（按需加载） |
| 复用性 | 项目内或全局 | 跨项目、跨工具 |

### 2. Skills 目录结构

```
my-skill/
├── SKILL.md              # 必选：技能定义，含 frontmatter + 指令正文
├── scripts/              # 可选：agent 可调用的可执行脚本
│   └── setup.sh
├── references/           # 可选：参考文档、规范、示例
│   └── api-docs.md
├── assets/               # 可选：模板文件、代码样板、资源
│   └── template.py
└── agents/
    └── openai.yaml       # 可选：Codex 特有的 UI 元数据和 MCP 依赖声明
```

### 3. SKILL.md 深度解析

SKILL.md 包含两个部分：YAML frontmatter（元数据）和 Markdown 正文（指令）。

```yaml
---
name: go-test-runner           # 必填。1-64 字符，小写字母+数字+连字符
description: "Run Go tests..." # 必填。隐式匹配的关键
---
```

> **最佳实践**：把最关键的场景词放在 description 开头。Codex 会在 token 预算不足时从尾部截断 description。

Claude Code 的扩展字段可以与 Codex 共存：

```yaml
---
name: code-explorer
description: "Explore unfamiliar codebases..."
context: fork                # Claude Code 特有——Codex 会忽略
allowed-tools:              # Claude Code 特有——Codex 会忽略
  - Read
  - Write
---
```

### 4. 发现路径：五层作用域

```
REPO  >  USER  >  ADMIN  >  SYSTEM  >  Plugin
```

| 作用域 | Codex 路径 | Claude Code 路径 |
|--------|-----------|-----------------|
| **REPO** | `.agents/skills/`（当前目录 → 父目录 → 仓库根） | `.claude/skills/<name>/` |
| **USER** | `$HOME/.agents/skills/` | `~/.claude/skills/<name>/` |
| **ADMIN** | `/etc/codex/skills/` | Enterprise managed |
| **SYSTEM** | 内置（`skill-creator` 等） | N/A |
| **Plugin** | `<plugin>/skills/<name>/` | `<plugin>/skills/<name>/` |

REPO 作用域支持向父目录向上遍历：

```
project-root/
├── .agents/skills/          # 仓库级技能，整个项目可见
├── src/
│   └── .agents/skills/      # 模块级技能，仅 src/ 下可见
└── docs/
    └── .agents/skills/
```

### 5. 渐进式延迟加载机制

Codex 采用五阶段渐进式加载，这是它在工程实现上最精妙的设计之一：

1. **索引阶段（Index Phase）**：启动时仅读取每个 SKILL.md 的 `name` 和 `description`
2. **Token 预算约束（Token Budget）**：技能列表受 2% 上下文窗口或 8000 字符约束
3. **触发加载（Trigger Load）**：显式 `/skill-name` 或隐式 description 匹配时触发
4. **完整加载（Full Load）**：触发后才读取完整的 SKILL.md 内容
5. **执行引用（Execute）**：引用的 `scripts/`、`references/` 文件按需读取

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 加载策略 | 五阶段渐进式加载 | description 自动加载 |
| 索引阶段 | 仅读 frontmatter | 无独立索引阶段 |
| Token 预算 | 2% 或 8000 字符 | 无硬性预算 |
| 触发方式 | 显式 `/skills` + 隐式 | 显式 `/skill-name` + description 自动 |

### 6. 启用与禁用 Skill

```toml
# ~/.codex/config.toml
[[skills.config]]
path = "/home/user/.agents/skills/legacy-formatter/SKILL.md"
enabled = false
```

> **Claude Code 对照**：Claude Code 没有类似的禁用机制，要么移出目录，要么通过 Managed Settings 控制。

### 7. agents/openai.yaml：Codex 特有的扩展层

```yaml
# my-skill/agents/openai.yaml
interface:
  display_name: "Go Test Runner"
  short_description: "Run Go tests"
  icon_small: "assets/icons/test-16.png"
  icon_large: "assets/icons/test-32.png"
  brand_color: "#3B82F6"

policy:
  allow_implicit_invocation: false    # 禁止隐式调用，仅显式 /skill 可用

dependencies:
  tools:
    - filesystem
    - github
```

### 8. 内置创建工具：skill-creator 与 skill-installer

```bash
# 交互式创建技能
/codex> /skill-creator

# 从远程仓库安装技能
/codex> /skill-installer https://github.com/my-org/skills/go-test-runner
```

### 9. Skill 共享方案

由于 Codex 和 Claude Code 共享同一套 Agent Skills Standard，它们的 Skill 目录结构完全兼容，区别仅在于发现路径不同。共享的核心思路是：**维护一份源文件，同时在两个工具各自的发现路径下建立引用**。

**方案一：符号链接共享（推荐）**

```bash
# 1. 创建独立技能目录
mkdir -p ~/shared-skills/go-test-runner

# 2. 链接到 Codex 发现路径
ln -s ~/shared-skills/go-test-runner ~/.agents/skills/go-test-runner

# 3. 链接到 Claude Code 发现路径
ln -s ~/shared-skills/go-test-runner ~/.claude/skills/go-test-runner
```

**方案二：独立技能仓库（团队级）**

```bash
git clone https://github.com/my-org/shared-skills.git ~/shared-skills

for skill_dir in ~/shared-skills/*/; do
    skill_name=$(basename "$skill_dir")
    ln -s "$skill_dir" ~/.agents/skills/"$skill_name"
    ln -s "$skill_dir" ~/.claude/skills/"$skill_name"
done
```

| 要素 | 兼容性 |
|------|--------|
| SKILL.md frontmatter | 完全兼容 |
| SKILL.md 正文 | 完全兼容 |
| `context: fork` 字段 | Claude 特有（Codex 忽略） |
| `agents/openai.yaml` | Codex 特有（Claude Code 忽略） |
| Shell 注入 `` !`command` `` | Claude 特有（Codex 不支持） |

> **本章小结**：Skills 是标准化的可复用能力包，核心是 SKILL.md（frontmatter + 指令正文）。发现路径覆盖五层作用域：REPO > USER > ADMIN > SYSTEM > Plugin。渐进式延迟加载是 Codex 的核心优化，在拥有大量 Skills 时效率远高于 Claude Code。`skill-creator` 和 `skill-installer` 是 Codex 内置的管理工具。最关键的是，Codex 和 Claude Code 共享 Agent Skills Standard，通过符号链接即可实现"一次编写，处处运行"。

---

## 第五章：Agents 子代理与 MCP 服务配置

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

## 第六章：Hooks 生命周期钩子与插件体系

第五章我们介绍了 Agents 和 MCP——它们分别解决了"用独立环境执行任务"和"接入外部工具"的问题。但还有更深层的问题：当我们需要在 agent 执行过程的**特定时刻**自动触发某些行为时——比如"每次工具调用前检查安全策略""每次会话启动时加载项目简报""每次上下文压缩前保存关键信息"——该怎么做？

Codex 提供了 **11 种生命周期钩子事件**，覆盖了从会话启动到停止的完整生命周期。它同时还拥有一个**插件体系**，允许将 hooks、skills、MCP 服务器打包为一个可分发、可安装的单元。

### Part 1：Hooks 生命周期钩子系统

#### 1.1 配置文件与合并规则

Hooks 有两种配置方式：

**方式一：独立 `hooks.json` 文件**

```json
// ~/.codex/hooks.json 或 .codex/hooks.json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes...",
            "timeout": 600,
            "additionalContextLimit": 2500
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/pre_tool.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**方式二：内联到 `config.toml`**

```toml
[hooks.SessionStart]
matcher = "startup|resume"
hooks = [
  { type = "command", command = "python3 ~/.codex/hooks/session_start.py",
    statusMessage = "Loading session notes...", timeout = 600 }
]
```

**合并规则**：与其他配置的"下层被上层覆盖"不同，hooks 的合并规则是**叠加运行**——同一事件的所有来源的全部匹配钩子**都会执行**，不会覆盖。但一旦有钩子返回阻断决策，事件处理链立即终止。

#### 1.2 11 种事件类型详解

| 阶段 | 事件名称 | 触发时机 | Matcher 支持 | 决策能力 |
|------|----------|----------|-------------|----------|
| **启动** | **SessionStart** | 主会话或子代理会话启动时 | `source`: startup / resume / clear / compact | 无（只读） |
| **启动** | **SubagentStart** | 子代理实例启动时 | `agent_type` | 无（只读） |
| **执行** | **PreToolUse** | 任意工具调用之前 | `tool_name` | **放行 / 拒绝 / 重写** |
| **执行** | **PermissionRequest** | 即将弹出审批请求时 | `tool_name` | **批准 / 拒绝** |
| **执行** | **PostToolUse** | 工具执行完成之后 | `tool_name` | 阻断 / 增加上下文 |
| **执行** | **UserPromptSubmit** | 用户提交新的提示词时 | 不支持 | **阻断** |
| **执行** | **Stop** | 主线程收到停止信号时 | 不支持 | **阻断（自动续期）** |
| **执行** | **SubagentStop** | 子代理实例停止时 | `agent_type` | **重试子代理** |
| **压缩** | **PreCompact** | 上下文压缩即将开始时 | `trigger`: manual / auto | 无（只读） |
| **压缩** | **PostCompact** | 上下文压缩完成之后 | `trigger`: manual / auto | 无（只读） |
| **停止** | **SessionEnd** | 主会话正常结束时 | `reason`: other | 无（只读） |

#### 1.3 PreToolUse 重写输入示例

```python
#!/usr/bin/env python3
# pre_tool_rewrite.py — PreToolUse 钩子
import json, sys

input_data = json.loads(sys.stdin.read())
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name == "Bash":
    command = tool_input.get("command", "")

    if command.strip().startswith("rm"):
        print(json.dumps({
            "stopReason": "dangerous_command",
            "systemMessage": f"Blocked dangerous command: {command}"
        }))
        sys.exit(2)  # 退出码 2 = 拒绝

    if "pip install" in command and "--quiet" not in command:
        safe_command = command.replace("pip install", "pip install --quiet")
        tool_input["command"] = safe_command
        print(json.dumps({"tool_input": tool_input}))
        sys.exit(0)  # 退出码 0 = 放行（用修改后的参数）

sys.exit(0)
```

#### 1.4 退出码约定

| 退出码 | 含义 |
|--------|------|
| **0** | 成功继续。有决策能力的事件：放行/批准 |
| **2** | 阻断/拒绝。停止当前事件的处理流程 |

#### 1.5 启用与安全管理

```bash
# 在交互式会话中管理钩子
/hooks

# 输出示例：
Known Hooks:
  1. SessionStart — ~/.codex/hooks.json → python3 ~/.codex/hooks/session_start.py
     Status: ENABLED   Trust: trusted
  2. PreToolUse — .codex/hooks.json → python3 .codex/hooks/audit.py
     Status: ENABLED   Trust: untrusted  [Pending your approval]

# 信任钩子
/hooks trust 2
```

#### 1.6 Codex Hooks vs Claude Code Hooks 对比

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 事件数量 | 11 种 | 4 种核心 |
| 配置格式 | JSON（hooks.json）或 TOML（内联） | settings.json 内联 JSON |
| 合并策略 | 叠加执行 | 叠加执行 |
| Codex 独有事件 | SessionEnd, SubagentStart/Stop, PreCompact, PostCompact, UserPromptSubmit, Stop | — |
| CLI 管理 | `/hooks` 命令（审查/信任/禁用） | `/hooks` 命令 |
| 信任机制 | 首次加载 untrusted，需用户信任 | 无明确信任机制 |
| 托管模式 | `allow_managed_hooks_only`（requirements.toml） | 无 |

### Part 2：插件体系

如果说 Hooks 是"在特定时机触发行为"的机制，那么插件就是"把多种扩展打包为一个可分发单元"的载体。

```text
.codex-plugin/              # 插件根目录
├── plugin.json             # 必选：插件清单文件
├── hooks/
│   └── hooks.json          # 可选：插件自带的钩子配置
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md        # 可选：插件包含的技能
│   └── skill-b/
│       └── SKILL.md
└── assets/                 # 可选：插件资源文件
```

```json
{
  "name": "project-helper",
  "version": "0.2.1",
  "description": "项目开发辅助插件",
  "skills": ["skills/scaffolder", "skills/doc-generator"],
  "mcp_servers": {
    "template-renderer": {
      "command": "npx",
      "args": ["-y", "@project/template-mcp"]
    }
  },
  "hooks": "hooks/hooks.json"
}
```

**插件 vs MCP 扩展对比**：

| 维度 | 插件（Plugin） | MCP 服务器 |
|------|---------------|------------|
| 本质 | 聚合容器 | 工具服务器 |
| 包含内容 | skills + hooks + MCP + UI | 只有工具 |
| Claude Code 对应 | 无 | 同 MCP 协议，配置格式不同 |

> **决策指南**：只需要工具调用用 MCP；需要工具+指令+自动化流程用插件；只是 Claude Code 用户不涉及 Codex，MCP 即可。

> **本章小结**：Hooks 系统让 Codex 在 11 个生命周期节点自动触发外部脚本，覆盖完整的 agent 执行流程。钩子拥有六种决策能力，退出码 0 放行，退出码 2 阻断。安全管理通过信任机制和托管模式实现。插件体系是 Codex 的扩展打包机制，通过 `plugin.json` 把 skills、hooks、MCP 服务器聚合为可分发单元。

---

## 第七章：CLI 与调试 —— 日常操作与故障排查

前六章我们把 Codex 的配置体系拆了个遍——从 config.toml 到 AGENTS.md，从 skills 到 hooks，每个子系统都有自己的配置文件和加载规则。但配置再多，最终你每天打交道的是 CLI。本章不做命令参考手册，只聚焦高频的日常操作命令、环境变量管理和配置验证技巧。

### 1. 核心 CLI 命令

```bash
# 交互式 REPL（最常用）
codex

# 单次执行，输出结果后退出
codex exec "解释这个项目的 .gitignore"

# 指定工作目录启动
codex --cd /path/to/project

# 指定模型
codex --model gpt-5.4-mini

# 指定审批模式
codex --approval-mode on-request
```

`--cd` 的重要性：它在会话初始化前就设置了工作目录，确保 AGENTS.md 发现、`.codex/config.toml` 加载、技能索引等工作都基于正确的目录上下文。

```bash
# 查看当前 workspace 状态（加载了哪些配置、指令、技能）
codex status

# 临时覆盖单个配置项
codex -c model=gpt-5.4-mini -c approval_policy=never

# 使用特定配置档
codex --profile fast

# 管理 MCP 服务器
codex mcp add
```

一条经验法则：
- **长期变更** → 修改 `config.toml` 或创建新 profile
- **临时实验** → `-c key=value`
- **按场景切换** → `--profile NAME`

### 2. 交互式命令

```bash
# 技能管理
/skills

# 钩子管理
/hooks

# 交互式配置（仅当前会话生效）
/config
/config set model=gpt-5.4-mini
/config get sandbox_mode

# 提交反馈
/feedback
```

### 3. 环境变量

```bash
# CODEX_HOME — 重定向全局配置目录
export CODEX_HOME=/path/to/custom/codex-home

# API 认证
export OPENAI_API_KEY=sk-...

# .env 自动加载（会话启动时自动加载项目根目录的 .env 文件）
echo "OPENAI_API_KEY=sk-..." > .env
```

`.env` 加载规则：
- 只在项目根目录搜索，不遍历子目录
- 不会覆盖已存在的环境变量
- 加载时机在 AGENTS.md 发现和 config.toml 加载之前

### 4. 调试与验证方法

```bash
# 验证指令加载
codex status
codex exec --cd /path/to/project "请列出你当前加载的所有指令文件和规则"

# 验证技能发现（在交互式会话中）
/skills

# 验证 hook 注册（在交互式会话中）
/hooks

# 审计 session JSONL
ls ~/.codex/transcripts/
head -100 ~/.codex/transcripts/session_20240731_001.jsonl

# 查看日志
export CODEX_LOG_LEVEL=debug
codex
```

### 5. 配置审计技巧

快速诊断清单：

```text
1. 配置文件在哪层？   → codex status | findstr "Config"
2. 配置项生效了吗？   → 检查是否写入了项目级但该键是"静默忽略"键
3. 指令文件加载了吗？ → codex exec "请列出所有加载的指令文件"
4. 技能发现了吗？     → /skills
5. Hook 注册了吗？    → /hooks
6. MCP 服务器能连吗？ → codex status 中查看 MCP 状态
```

常见故障案例：

| 案例 | 症状 | 根因 | 对策 |
|------|------|------|------|
| 模型提供商配置不生效 | 设了 ollama 但仍调 OpenAI | `model_provider` 是静默忽略键 | 移到用户级配置 |
| 技能没有被自动加载 | description 匹配不上 | 触发词不够精准 | 调整 description 措辞 |
| SessionStart hook 没执行 | 启动时无效果 | 新 hook 默认 untrusted | 执行 `/hooks trust` |
| 配置文件变更后无效果 | 重启后配置未生效 | `CODEX_HOME` 指向了别处 | 确认正在修改的是正确路径 |

> **本章小结**：四条核心 CLI 命令覆盖日常操作——`codex`、`codex exec`、`codex status`、`codex --cd`。`/skills`、`/hooks`、`/config` 三个交互式命令管理运行时状态。CODEX_HOME、OPENAI_API_KEY、.env 三个环境变量控制运行时行为。调试优先用 `codex status` + 直接询问 agent。常见故障按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序排查，覆盖 90% 场景。

---

## 第八章：完整对照表与从 Claude Code 迁移实战

前七章我们深入剖析了 Codex 的每一个配置子系统。如果你一路读下来，应该已经对 Codex 的各个部件有了清晰的认知。但有一个问题始终悬而未决：**如果你是个 Claude Code 老用户，手头有一套磨合已久的配置——一套 CLAUDE.md、十几个技能、若干个 MCP 服务器、精心调教的权限规则——怎么把它搬到 Codex 上？**

这一章不做概念分析，只做一件事：**给出手。** 先给一张完整的配置对照表让你看清每个维度的对应关系，再给一套四步迁移策略让你按图索骥，最后用常见陷阱和最佳实践帮你避开坑。

### 1. 完整对照表

#### 文件与路径对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 1 | 配置文件格式 | TOML（主）+ JSON/YAML | JSON | 低 |
| 2 | 全局配置路径 | `~/.codex/config.toml` | `~/.claude/settings.json` | 低 |
| 3 | 项目配置路径 | `.codex/config.toml` | `.claude/settings.json` | 低 |
| 4 | 本地覆盖机制 | `-c key=val` CLI 参数 | `.claude/settings.local.json` | 低 |
| 5 | 环境变量重定向 | `CODEX_HOME` | 无标准变量 | 低 |

#### 指令与规则对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 6 | 指令文件名 | AGENTS.md | CLAUDE.md | **零** |
| 7 | 指令层级 | 全局 + 逐级拼接 | 单文件 + 路径作用域 rules/ | 中 |
| 8 | 规则系统 | `.codex/rules/*.rules`（Starlark） | `.claude/rules/*.md`（Markdown） | **高** |
| 9 | 指令容量限制 | 默认 32 KiB | 建议 200-300 行 | 低 |

#### 技能系统对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 10 | 技能标准 | Agent Skills Standard | Agent Skills Standard | **零** |
| 11 | 技能发现路径 | `.agents/skills/` | `.claude/skills/` | 低 |
| 12 | 技能调用方式 | `/skills` + description | `/skill-name` + description | 低 |
| 13 | 技能参数传递 | 无 | `$ARGUMENTS` / `$0` / `$1` | **高** |
| 14 | 技能子代理 | 无 | `context: fork` | **高** |
| 15 | 技能禁用 | `[[skills.config]]` + `enabled=false` | 移出目录 | 低 |

#### 扩展与安全对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 16 | Agents 格式 | `.codex/agents/*.toml` | `.claude/agents/*.md` | 中 |
| 17 | MCP 配置格式 | `[mcp_servers.<id>]` TOML | `mcpServers` JSON | 低 |
| 18 | MCP 审批模式 | auto / prompt / writes / approve | allow / deny / ask | 中 |
| 19 | Hooks 事件数 | 11 种 | 4 种核心 | 中 |
| 20 | 权限模型 | sandbox_mode + approval_policy | allow / deny / ask 细粒度 | **高** |

#### Codex 独有功能

| # | 配置维度 | 说明 |
|---|---------|------|
| 21 | Profiles 多环境配置档 | `[profiles.NAME]` 按场景切换 |
| 22 | 插件系统 | `.codex-plugin/plugin.json` |
| 23 | 多模型提供商 | ollama / lmstudio / OpenRouter / Azure 等 |
| 24 | Sandbox 沙箱模式 | read-only / workspace-write / danger-full-access |

> **核心结论**：约 12 项可零/低成本迁移，4 项需要重写（参数传递、子代理、Starlark 规则、权限模型）。

### 2. 迁移四步走策略

#### 第一步：指令兼容（5 分钟）

最高性价比的一步——**不需要修改任何现有文件**。

```toml
# .codex/config.toml — 一行配置让 Codex 读取你的 CLAUDE.md
[project_doc]
fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
max_bytes = 32768
```

**验证**：

```bash
codex status
codex --cd . "请列出所有已加载的指令文件"
```

#### 第二步：技能共享（10 分钟）

利用 Agent Skills Standard 的兼容性，通过符号链接让两个工具共享同一套技能。

```bash
# 方案 A：维护独立技能仓库（推荐）
ln -s ~/shared-skills ~/.agents/skills/
ln -s ~/shared-skills ~/.claude/skills/

# 方案 B：链接现有 Claude Code 技能到 Codex
ln -s ~/.claude/skills ~/.agents/skills/
```

**注意事项**：
- 使用了 `$ARGUMENTS` 参数传递的技能需要重构
- 使用了 `context: fork` 的技能需要移除 `context` 字段
- 使用了 `allowed-tools` 的技能——Codex 无此概念，但可通过 Starlark 规则实现

#### 第三步：权限意图转换（需要理解，不能直译）

```text
Claude Code "allow" 大多数工具 + "ask" 高风险工具
→ Codex sandbox_mode = "workspace-write" + approval_policy = "on-request"

Claude Code "ask" 每个操作
→ Codex approval_policy = "untrusted"

Claude Code 全局信任 + 少量限制
→ Codex sandbox_mode = "workspace-write" + [permissions.scoped] 限制敏感路径

Claude Code 完全信任（罕见）
→ Codex sandbox_mode = "danger-full-access" + approval_policy = "never"（慎用！）
```

**典型迁移示例**：

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = true

[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
"**/.env.*" = "deny"
```

#### 第四步：逐个迁移（按优先级顺序）

```text
第一优先级：MCP 服务器 → CLI 随手迁移，直接受益
  ↓
第二优先级：Hooks → 保留核心钩子，可选增强
  ↓
第三优先级：CLAUDE.md 重构为 AGENTS.md → 利用分层能力
  ↓
第四优先级：Starlark 规则系统 → 替换原有的 .claude/rules/*.md
  ↓
第五优先级：Profiles + 插件 → Codex 独有能力，按需添加
```

### 3. 常见陷阱 6 条

**陷阱 1：静默忽略 —— 把安全配置放到项目级**

```bash
# 正确做法：放用户级
echo '[approval_policy]
granular = { sandbox_approval = true }' >> ~/.codex/config.toml

# 错误做法（被静默忽略，不会报错）
echo '[approval_policy]
granular = { sandbox_approval = true }' >> .codex/config.toml
```

**陷阱 2：网络权限未开启导致工具安装失败**

```toml
[sandbox_workspace_write]
network_access = true  # 允许出站 HTTP（pip/npm/curl 需要）
```

**陷阱 3：安全组合爆炸 —— "never" + "danger" = 无安全网**

```toml
# 避免的组合
approval_policy = "never"
sandbox_mode = "danger-full-access"

# 推荐的折中
sandbox_mode = "workspace-write"
approval_policy = "never"  # 只跳过审批，但沙箱仍在
```

**陷阱 4：MCP 服务器超时被丢弃**

```toml
[mcp_servers.heavy_server]
command = "node"
args    = ["dist/server.js"]
startup_timeout_sec = 30   # 默认 10s 不够
tool_timeout_sec    = 120
```

**陷阱 5：环境变量泄漏**

```toml
[shell_environment_policy]
inherit = "core"  # 只继承 PATH/HOME 等基础变量
```

**陷阱 6：权限 glob 模式未限定作用域**

```toml
# 错误：未限定作用域，全局生效
[permissions.scoped.filesystem]
"**/.env" = "deny"

# 正确：限定到 workspace_roots
[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
```

### 4. Skills 最佳实践 5 条

**实践 1：description 前置触发词**

```yaml
# 推荐：以场景词开头
description: "React 组件单元测试，使用 Vitest + React Testing Library..."

# 不推荐：以泛化词开头
description: "为 React 组件编写测试用例的工具..."
```

**实践 2：单一职责** — 一个技能只做一件事。如果发现 SKILL.md 中有"如果做 A 则...，如果做 B 则..."的段落，说明应该拆分为两个技能。

**实践 3：指令优先于脚本** — 能用自然语言描述的步骤，不要写成脚本。脚本只在涉及大量机械操作时才值得提取。

**实践 4：渐进披露** — SKILL.md 保持简洁（建议 50 行以内），详细文档放在 `references/` 目录中。

**实践 5：相对路径引用** — 所有路径引用都应基于技能根目录的相对路径，确保技能在不同项目间可复用。

### 5. 典型项目配置示例

**项目级 `.codex/config.toml`**：

```toml
# ============================================
# .codex/config.toml — 项目级配置示例
# 适用于从 Claude Code 迁移到 Codex 的项目
# ============================================

name = "my-project"
model = "gpt-5.4"

# --- 指令兼容 CLAUDE.md（迁移第一步） ---
[project_doc]
fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
max_bytes = 32768

# --- 权限细粒度控制 ---
[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
"**/.git/" = "deny"

[permissions.scoped.network]
enabled = true
mode = "limited"
[permissions.scoped.network.domains]
"api.openai.com" = "allow"
"github.com" = "allow"

# --- MCP 服务器配置 ---
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "."]

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
approval_mode = "writes"

# --- 功能开关 ---
[features]
hooks = true
multi_agent = true
undo = true

# --- Shell 环境策略 ---
[shell_environment_policy]
inherit = "core"
```

**用户级 `~/.codex/config.toml`**：

```toml
# ~/.codex/config.toml — 安全相关配置只能放这里！
model_provider = "openai"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[profiles.fast]
model = "gpt-5.4-mini"
model_reasoning_effort = "low"
approval_policy = "never"

[profiles.deep]
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
```

### 6. 迁移检查清单

**第一步：指令兼容**
- [ ] `.codex/config.toml` 中设置了 `project_doc.fallback_filenames = ["CLAUDE.md"]`
- [ ] `codex status` 输出中可看到 CLAUDE.md 已被加载
- [ ] 自定义指令在 Codex 会话中生效

**第二步：技能共享**
- [ ] `~/.agents/skills/` 已存在（符号链接或目录）
- [ ] `/skills` 命令显示了所有预期技能
- [ ] 使用 `$ARGUMENTS` 或 `context: fork` 的技能已处理

**第三步：权限意图转换**
- [ ] 理解 sandbox_mode 三种模式的差异
- [ ] 理解 approval_policy 三种模式的行为
- [ ] 测试过 `pip install` / `npm install` 能在当前配置下工作
- [ ] 检查了敏感文件（.env、credentials 等）是否被适当保护

**第四步：逐个迁移**
- [ ] MCP 服务器全部迁移完成并验证可用
- [ ] Hooks 配置已迁移（或决定暂时跳过）
- [ ] （可选）CLAUDE.md 已重构为分层 AGENTS.md

**避坑确认**
- [ ] 安全敏感配置放在用户级，不在项目级
- [ ] network_access = true 已设置（如需联网）
- [ ] 没有同时设置 `approval_policy = "never"` + `sandbox_mode = "danger-full-access"`
- [ ] MCP 服务器 `startup_timeout_sec` 足够大
- [ ] Shell 环境策略设置为 `"core"` 或已配置白名单
- [ ] 权限 glob 模式已限定 `:workspace_roots` 作用域

> **本章小结**：完整对照表覆盖 21+ 配置维度，约 12 项可零/低成本迁移，4 项需要重写。四步迁移策略从指令兼容到逐个迁移渐进推进。六条常见陷阱按规律可循，五项 Skills 最佳实践帮助你构建更高质量的技能库。项目级配置放业务配置，用户级配置放安全敏感配置——这个分离本身就是一项关键最佳实践。

---

## 附录：快速参考卡片

### 配置文件路径速查

| 配置类型 | Codex 路径 | Claude Code 路径 |
|---------|-----------|-----------------|
| 用户全局配置 | `~/.codex/config.toml` | `~/.claude/settings.json` |
| 项目配置 | `<repo>/.codex/config.toml` | `<repo>/.claude/settings.json` |
| 用户全局指令 | `~/.codex/AGENTS.md` | — |
| 项目指令 | `<repo>/AGENTS.md`（分层级联） | `<repo>/CLAUDE.md`（单文件） |
| 规则文件 | `.codex/rules/*.rules`（Starlark） | `.claude/rules/*.md` |
| Skills 目录 | `.agents/skills/` | `.claude/skills/` |
| 用户 Skills | `~/.agents/skills/` | `~/.claude/skills/` |
| Agent 定义 | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Hooks 配置 | `.codex/hooks.json` 或 config.toml 内联 | settings.json 内联 |
| 插件目录 | `.codex/plugins/` | — |
| 环境变量文件 | `<project>/.env` | — |

### 常用 CLI 命令速记

| 命令 | 用途 | 示例 |
|------|------|------|
| `codex` | 启动交互式 REPL | `codex` |
| `codex exec` | 单次执行 | `codex exec "解释这个项目"` |
| `codex status` | 查看工作区状态 | `codex status` |
| `codex --cd DIR` | 指定工作目录启动 | `codex --cd /path/to/proj` |
| `codex --profile NAME` | 使用特定配置档 | `codex --profile fast` |
| `codex -c key=val` | 临时覆盖配置项 | `codex -c model=gpt-5.4-mini` |
| `codex mcp add` | 交互式添加 MCP 服务器 | `codex mcp add` |
| `/skills` | 列出可用技能 | `/skills` |
| `/hooks` | 管理钩子 | `/hooks trust 1` |
| `/config` | 查看/修改配置 | `/config get sandbox_mode` |
| `/feedback` | 提交反馈 | `/feedback` |

### 关键配置项默认值一览

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `sandbox_mode` | `workspace-write` | 沙箱模式 |
| `approval_policy` | `on-request` | 审批策略 |
| `shell_environment_policy.inherit` | `all` | 环境变量继承策略 |
| `project_doc_max_bytes` | 32768（32 KiB） | 指令容量上限 |
| `[agents].max_threads` | 2 | 最大并行子代理数 |
| `[agents].max_depth` | 2 | 子代理最大嵌套深度 |
| `[features].hooks` | `true` | 钩子系统开关 |
| `[features].multi_agent` | `true` | 多代理开关 |
| `[features].shell_snapshot` | `true` | 快照加速开关 |
| MCP `startup_timeout_sec` | 10 | MCP 服务器启动超时 |
| MCP `tool_timeout_sec` | 60 | MCP 工具调用超时 |
| MCP `approval_mode` | `auto` | MCP 审批模式 |
| MCP `required` | `false` | MCP 服务器必要性 |

---

> **笔记完成于 2026-07-31**
>
> 本笔记由 Codex 配置学习项目自动生成，面向 Obsidian 发布。
>
> 项目来源：workspace/codex-config
