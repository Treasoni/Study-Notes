# Codex 完整配置体系 — 深度素材

收集时间: 2026-07-31
精读资料: 8 篇核心文档/文章

---

## 1. 核心配置：config.toml 全面解析

### 1.1 文件位置与作用域

| 层级 | 路径 | 说明 |
|------|------|------|
| **托管配置** | requirements.toml | 企业级强制配置，最高优先级 |
| **用户配置** | `~/.codex/config.toml` | 全局默认，`CODEX_HOME` 可重定向 |
| **项目配置** | `.codex/config.toml` | 项目级覆盖 |
| **Profile** | `--profile NAME` | 运行时激活，插入用户和项目之间 |
| **CLI 参数** | `-c key=value` | 运行时覆盖，最高优先级 |

### 1.2 安全限定 — 项目级静默忽略的键

以下键**只能**在用户级 `~/.codex/config.toml` 中设置，项目级写入会被静默忽略：

`openai_base_url`, `chatgpt_base_url`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, `approval_policy`, `sandbox_mode`, `sandbox_workspace_write.*`, `experimental_realtime_ws_base_url`, `otel.*`, `apps_mcp_product_sku`

### 1.3 sandbox_mode（沙箱模式）

| 值 | 文件系统 | 网络 |
|----|---------|------|
| `read-only` | 全局可读，不可写入 | 阻止 |
| `workspace-write` | 可写入 cwd + `$TMPDIR` + `/tmp` + `writable_roots` | 默认阻止，`network_access = true` 开启 |
| `danger-full-access` | 等同于当前用户权限 | 等同于当前用户权限 |

`[sandbox_workspace_write]` 子配置：
- `writable_roots` — 额外可写目录列表
- `network_access` — 允许出站 HTTP（pip/npm 安装需要）
- `exclude_tmpdir_env_var` / `exclude_slash_tmp` — 移除 tmp 目录

### 1.4 approval_policy（审批策略）

| 值 | 行为 |
|----|------|
| `untrusted` | 几乎每步操作都询问 |
| `on-request` | 仅在沙箱阻止时询问 |
| `never` | 完全自主（慎与 danger-full-access 搭配） |

细粒度控制：
```toml
[approval_policy.granular]
sandbox_approval     = true
request_permissions  = true
rules                = true
skill_approval       = true
mcp_elicitations     = false
```

### 1.5 Permissions（新一代权限系统）

使用 `[permissions.NAME]` 定义命名配置档，通过 `default_permissions = "my-profile"` 激活。内置配置档：`:read-only`、`:workspace`、`:danger-full-access`。

```toml
[permissions.scoped.workspace_roots]
"~/code/oss"     = true

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
"api.openai.com" = "allow"
"github.com"     = "allow"
```

### 1.6 Profiles（多环境配置档）

```toml
[profiles.fast]
model                  = "gpt-5.4-mini"
model_reasoning_effort = "low"
approval_policy        = "never"

[profiles.deep]
model                  = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy        = "on-request"
```

激活：`codex --profile fast`

### 1.7 Model 相关

- `model` — 模型选择
- `model_provider` — 提供商（openai/ollama/lmstudio 内置；支持 Azure/OpenRouter/Gemini 等）
- `model_reasoning_effort` — `minimal` / `low` / `medium` / `high` / `xhigh`
- `model_reasoning_summary` — `auto` / `concise` / `detailed` / `none`
- `model_verbosity` — `low` / `medium` / `high`

自定义提供商：
```toml
[model_providers.custom]
name       = "My Provider"
base_url   = "https://api.example.com/v1"
wire_api   = "responses"
env_key    = "MY_API_KEY"
```

### 1.8 Features 功能开关

| 键 | 默认 | 说明 |
|----|------|------|
| `shell_tool` | true | 命令运行工具 |
| `hooks` | true | 生命周期钩子 |
| `multi_agent` | true | 多代理 |
| `unified_exec` | true | PTY exec |
| `shell_snapshot` | true | 快照加速 |
| `network_proxy` | false | 网络代理 |
| `prevent_idle_sleep` | false | 阻止休眠 |
| `memories` | false | 记忆功能 |
| `undo` | false | 撤销 |
| `codex_git_commit` | false | 自动 git commit |

### 1.9 其他重要配置

- **Shell 环境策略** — `inherit`：`all` / `core` / `none`；`include_only` / `exclude` 过滤
- **TUI** — 动画、主题、vim 模式、快捷键、状态栏
- **Telemetry** — OTLP 导出、分析上报
- **项目信任** — `[projects."/path"].trust_level = "trusted" | "untrusted"`

---

## 2. 指令/Rules：AGENTS.md 分层体系

### 2.1 发现机制

每次会话启动时构建指令链：

1. **全局层**：`~/.codex/AGENTS.override.md` > `~/.codex/AGENTS.md`（取第一个非空文件）
2. **项目层**：从 Git 根目录向下遍历到当前目录，每级检查：
   - `AGENTS.override.md` > `AGENTS.md` > `project_doc_fallback_filenames`（如 `CLAUDE.md`、`TEAM_GUIDE.md`）
3. **合并**：从根到叶拼接，越靠近当前目录的文件越靠后 ≡ 覆盖效果

### 2.2 容量限制

- 默认上限：**32 KiB**（`project_doc_max_bytes`）
- 超过上限停止添加
- 空文件跳过

### 2.3 特殊段落

- **Code Review Rules** — GitHub PR 审查的定制规则
- **Working Agreements** — 标准工作协议（如"修改 JS 后运行 npm test"）

### 2.4 验证命令

```bash
codex status                            # 检查 workspace 根
codex --cd subdir "显示当前指令文件"     # 审计已加载指令
```

### 2.5 Codex AGENTS.md vs Claude CLAUDE.md

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 文件名 | AGENTS.md | CLAUDE.md |
| 兼容 | 可通过 fallback 读取 CLAUDE.md | 不读取 AGENTS.md |
| 分层 | 全局 + 项目根 → 当前目录逐级拼接 | 单文件，路径作用域 rules/ |
| 容量 | 默认 32 KiB | 约 200-300 行最佳 |
| 风格 | 偏可执行约束和自动化 | 偏行为风格和个性化指南 |
| 令牌效率 | 每次启动重建，无需清缓存 | 类似，按需加载 |

---

## 3. Skills：技能系统深度解析

### 3.1 Skills 目录结构

```
my-skill/
├── SKILL.md              # 必选：指令 + frontmatter
├── scripts/              # 可选：可执行脚本
├── references/           # 可选：参考文档
├── assets/               # 可选：模板和资源
└── agents/
    └── openai.yaml       # 可选：UI 元数据和 MCP 依赖
```

### 3.2 SKILL.md Frontmatter

```yaml
---
name: skill-name          # 必填，1-64 字符，小写+数字+连字符
description: "..."        # 必填，隐式匹配的关键！前置触发词
---
```

### 3.3 发现路径

| 作用域 | Codex 路径 | Claude Code 路径 |
|--------|-----------|-----------------|
| REPO | `.agents/skills/`（当前目录→父目录→仓库根） | `.claude/skills/<name>/` |
| USER | `$HOME/.agents/skills/` | `~/.claude/skills/<name>/` |
| ADMIN | `/etc/codex/skills/` | Enterprise managed |
| SYSTEM | 内置（skill-creator 等） | N/A |
| Plugin | `<plugin>/skills/<name>/` | `<plugin>/skills/<name>/` |

### 3.4 加载机制 — 渐进式延迟加载

1. **索引阶段**：仅扫描 frontmatter 的 `name` + `description` + 文件路径
2. **Token 预算**：初始列表最多 **2% 上下文窗口** 或 **8000 字符**
3. **触发加载**：用户 `/skill` 显式调用 或 description 隐式匹配
4. **完整加载**：Codex 决定使用后读取完整 SKILL.md
5. **描述截断**：skills 过多时先截断描述，仍超标则从列表省略并警告

### 3.5 启用/禁用

```toml
# ~/.codex/config.toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

### 3.6 agents/openai.yaml 扩展（Codex 特有）

| 字段 | 说明 |
|------|------|
| `interface.display_name` | UI 显示名 |
| `interface.short_description` | UI 简短描述 |
| `interface.icon_small/large` | Logo 资源路径 |
| `interface.brand_color` | 品牌色 `#3B82F6` |
| `policy.allow_implicit_invocation` | 布尔值，false 时只能显式调用 |
| `dependencies.tools[]` | MCP 工具依赖声明 |

### 3.7 Codex Skills vs Claude Code Skills 关键差异

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 内置创建器 | `$skill-creator` + `$skill-installer` | 无（手工/IDE） |
| 调用方式 | `/skills` + 隐式匹配 | `/skill-name` + description 自动加载 |
| 渐进加载 | ✅ metadata-first, full load on use | description 自动加载 |
| 子代理 | 无 | `context: fork` fork 子代理 |
| 参数传递 | 无 | `$ARGUMENTS` / `$0` / `$1` |
| 工具限制 | 无 | `allowed-tools` 字段 |
| Shell 注入 | 无 | `` !`command` `` 动态上下文 |
| 禁用不掉 | `[[skills.config]]` + `enabled=false` | 移出目录或 managed settings |
| **共享** | 两者基于同一 Agent Skills Standard，**可通过符号链接共享** | 同左 + monorepo 嵌套支持 |

### 3.8 共享 Skills 方案

1. 维护一个**独立技能仓库**
2. 符号链接到两个工具的发现路径：
   - `ln -s ~/shared-skills/my-skill ~/.agents/skills/my-skill`（Codex）
   - `ln -s ~/shared-skills/my-skill ~/.claude/skills/my-skill`（Claude）
3. 共享内容：标准 frontmatter + Markdown 指令 + 相对路径引用
4. Codex 特有：可选的 `agents/openai.yaml`
5. Claude 特有：扩展 frontmatter（`context: fork`、`allowed-tools`、`$ARGUMENTS`）

---

## 4. Agents：子代理系统

### 4.1 配置路径

`$CODEX_HOME/agents/<name>.toml` 或 `<project>/.codex/agents/<name>.toml`

### 4.2 代理定义格式

```toml
description = "执行独立代码探索任务"
system_prompt = ""  # 可选附加指令
model = "gpt-5.4"
reasoning_effort = "high"
sandbox_mode = "workspace-write"
skills = ["code-explorer"]  # 自动使用的技能
```

### 4.3 内置代理

| 代理 | 说明 |
|------|------|
| `default` | 标准执行代理 |
| `worker` | 轻量后台任务代理 |
| `explorer` | 探索/搜索代理 |

### 4.4 Codex Agents vs Claude Code Agents

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 格式 | TOML | Markdown + frontmatter |
| 路径 | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| 内置类型 | default / worker / explorer | 无硬编码类型 |
| 全局设置 | `[agents]` 区块：`max_threads`, `max_depth` | settings.json |

### 4.5 执行规则（Starlark .rules）

`.codex/rules/*.rules` — Starlark 语言控制工具审批策略：

```
allow | prompt | forbidden
```

控制哪些工具操作需要审批、自动允许或禁止。

---

## 5. MCP：Model Context Protocol 配置

### 5.1 配置位置

`~/.codex/config.toml` 或 `.codex/config.toml` 中的 `[mcp_servers.<id>]` 区块

### 5.2 两种传输方式

**STDIO（本地进程）**：
```toml
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
startup_timeout_sec = 10
tool_timeout_sec    = 60
```

**Streamable HTTP（远程 URL）**：
```toml
[mcp_servers.remote_api]
url                  = "https://api.example.com/mcp"
bearer_token_env_var = "API_TOKEN"
```

### 5.3 审批模式

| 模式 | 说明 |
|------|------|
| `auto` | 自动执行 |
| `prompt` | 提示用户 |
| `writes` | 写操作时提示 |
| `approve` | 始终需要审批 |

### 5.4 关键参数

- `startup_timeout_sec` — 默认 10s，慢服务器需调大
- `tool_timeout_sec` — 默认 60s
- `enabled_tools` / `disabled_tools` — 工具白名单/黑名单
- `required` — true 时启动失败终止会话
- 命令行安装：`codex mcp add`

### 5.5 Codex MCP vs Claude Code MCP

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 配置格式 | TOML `[mcp_servers.<id>]` | JSON `mcpServers` |
| 审批模式 | auto/prompt/writes/approve (4 种) | allow/deny/ask 规则 |
| CLI 命令 | `codex mcp add` | 手工编辑 settings.json |
| 工具控制 | `enabled_tools`/`disabled_tools` | `mcp__servername__toolname` 模式 |
| 超时控制 | startup + tool 分别设置 | 类似 |

---

## 6. Hooks：生命周期钩子系统

### 6.1 配置文件

- `hooks.json` 或 `config.toml` 内联 `[hooks]`
- 发现路径：`~/.codex/hooks.json`、`~/.codex/config.toml`、`<repo>/.codex/hooks.json`、`<repo>/.codex/config.toml`
- **合并规则**：多个来源的匹配钩子全部运行（不覆盖，叠加执行）

### 6.2 事件类型（11 种）

| 事件 | 触发时机 | Matcher |
|------|----------|---------|
| **SessionStart** | 会话/子代理启动 | `source`: startup/resume/clear/compact |
| **SessionEnd** | 主线程结束 | `reason`: other（当前仅此） |
| **SubagentStart** | 子代理启动 | `agent_type` |
| **SubagentStop** | 子代理停止 | `agent_type` |
| **PreToolUse** | 工具调用前 | `tool_name`：Bash/Edit/MCP 工具名 |
| **PermissionRequest** | 即将请求审批 | `tool_name` |
| **PostToolUse** | 工具执行后 | `tool_name` |
| **PreCompact** | 上下文压缩前 | `trigger`: manual/auto |
| **PostCompact** | 上下文压缩后 | `trigger`: manual/auto |
| **UserPromptSubmit** | 用户提交提示词 | 不支持（忽略） |
| **Stop** | 主线程停止 | 不支持（忽略） |

### 6.3 hooks.json 结构

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes",
            "timeout": 600,
            "additionalContextLimit": 2500
          }
        ]
      }
    ]
  }
}
```

### 6.4 钩子决策能力

| 事件 | 支持的操作 |
|------|-----------|
| PreToolUse | 放行、拒绝、重写输入、增加上下文 |
| PermissionRequest | 批准、拒绝 |
| PostToolUse | 阻断、增加上下文 |
| Stop | 让 Codex 继续（block 决策，自动生成 continuation prompt） |
| SubagentStop | 重试子代理（block 决策） |
| UserPromptSubmit | 阻断（block 决策） |

### 6.5 stdin/stdout 协议

stdin JSON 通用字段：`session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`
stdout JSON 通用字段：`continue`, `stopReason`, `systemMessage`
退出码：`0` = 成功继续，`2` = 阻断/拒绝

### 6.6 启用与安全

- 默认启用：`[features] hooks = true`
- `/hooks` CLI 命令审查/信任/禁用钩子
- 托管钩子：`requirements.toml` 中 `allow_managed_hooks_only = true`

### 6.7 Codex Hooks vs Claude Code Hooks

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 配置格式 | JSON/TOML | JSON |
| 事件数 | 11 种 | 4 种核心 |
| Codex 独有 | PreCompact, PostCompact, SubagentStart, SubagentStop, UserPromptSubmit, SessionEnd | 无 |
| 匹配器 | matcher 正则 | 无（每种事件直接注册） |
| 合并 | 叠加运行（不覆盖） | 叠加运行 |
| 工具覆盖 | PreToolUse 可观测 Bash/Edit/MCP/spawn | 类似 |

---

## 7. 插件体系

### 7.1 插件结构

```
.codex-plugin/plugin.json  # manifest
hooks/hooks.json           # 钩子
skills/                    # 技能
```

### 7.2 plugins.json 关键字段

| 字段 | 说明 |
|------|------|
| `name` | 插件名 |
| `version` | 版本号 |
| `skills` | 技能路径数组 |
| `mcp_servers` | MCP 服务器定义 |
| `hooks` | hooks.json 路径覆盖 |
| `apps` | UI 组件 |

### 7.3 与 Claude Code 对比

Codex 有独立插件系统和市场，Claude Code 通过 MCP 服务器实现类似扩展。ChatGPT 和 Codex 共享统一插件目录。

---

## 8. CLI 与调试

### 8.1 核心命令

| 命令 | 说明 |
|------|------|
| `codex exec "prompt"` | 单次执行 |
| `codex` | 交互式 REPL |
| `codex status` | 查看 workspace 状态 |
| `codex --profile NAME` | 切换配置档 |
| `codex -c key=value` | 临时覆盖配置 |
| `codex mcp add` | 添加 MCP 服务器 |
| `codex --cd DIR` | 指定工作目录 |
| `codex --model MODEL` | 指定模型 |
| `codex --approval-mode MODE` | 审批模式 |
| `/skills` | 列出可用技能 |
| `/hooks` | 管理钩子 |
| `/config` | 交互式配置 |
| `/feedback` | 提交反馈 |

### 8.2 环境变量

| 变量 | 说明 |
|------|------|
| `CODEX_HOME` | 全局配置目录（默认 `~/.codex`） |
| `OPENAI_API_KEY` | API 认证 |
| `.env` | 项目根目录自动加载 |

---

## 9. 配置体系完整对照表：Codex vs Claude Code

| 配置维度 | Codex | Claude Code | 兼容性 |
|---------|-------|-------------|--------|
| **格式** | TOML（也支持 YAML/JSON） | JSON | 格式不同，需转换 |
| **全局配置** | `~/.codex/config.toml` | `~/.claude/settings.json` | 路径不同 |
| **项目配置** | `.codex/config.toml` | `.claude/settings.json` | 路径不同 |
| **本地覆盖** | `-c key=val` CLI 参数 | `.claude/settings.local.json` | 方式不同 |
| **指令文件** | AGENTS.md（分层级联） | CLAUDE.md（单文件） | AGENTS.md 可 fallback 到 CLAUDE.md |
| **规则系统** | `.codex/rules/*.rules`（Starlark） | `.claude/rules/*.md`（路径作用域） | 语法和机制完全不同 |
| **Skills 路径** | `.agents/skills/` | `.claude/skills/` | 可通过符号链接共享 |
| **Skills 标准** | Agent Skills Standard | Agent Skills Standard | **完全相同！** |
| **Skills 子代理** | 无 | `context: fork` | Claude 独有 |
| **Skills 参数** | 无 | `$ARGUMENTS` | Claude 独有 |
| **Agents 配置** | `.codex/agents/*.toml` | `.claude/agents/*.md` | 格式不同 |
| **MCP 配置** | `[mcp_servers]` TOML 区块 | `mcpServers` JSON | 格式不同，语义相近 |
| **Hooks 事件** | 11 种事件 | 4 种核心事件 | Codex 更多事件 |
| **Hooks 配置** | `hooks.json` 或内联 TOML | settings.json 内联 JSON | 结构类似 |
| **权限** | sandbox_mode + approval_policy | allow/deny/ask 细粒度 | 范式不同，需意图转换 |
| **Profiles** | `[profiles.NAME]` TOML 配置档 | 无内置 | Codex 独有 |
| **插件系统** | `.codex-plugin/plugin.json` | 无 | Codex 独有 |
| **CLI 配置命令** | `/config`, `/skills`, `/hooks`, `/feedback` | `/config`, `/hooks` | Codex 更丰富 |
| **多提供商** | 内置 openai/ollama/lmstudio + 自定义 | 主要 Anthropic | Codex 更灵活 |

---

## 10. 常见陷阱与最佳实践

### 10.1 配置陷阱

1. **`model_provider` 放在项目级 config.toml** → 被静默忽略，必须放用户级
2. **`network_access = false`** → pip/npm 安装卡死，记得开
3. **`approval_policy = "never"` + `sandbox_mode = "danger-full-access"`** → 无安全网
4. **`startup_timeout_sec` 默认 10s** → 慢 MCP 服务器被丢弃
5. **`shell_environment_policy.inherit = "all"`** → 泄漏所有环境变量
6. **权限 glob 模式未限定 `":workspace_roots"`** → 全局生效

### 10.2 Skills 最佳实践

1. **description 前置触发词** — 隐式匹配依赖 description，把关键场景词放前面
2. **聚焦单一职责** — 一个技能只做一件事
3. **指令优先于脚本** — 技能是指导 agent 行为，不是替代它
4. **references/ 渐进披露** — 详细文档放 references/，保持 SKILL.md 简洁
5. **相对路径引用** — 从技能根目录相对引用

### 10.3 从 Claude Code 迁移到 Codex 的建议

1. **先确认 AGENTS.md fallback** — 设置 `project_doc_fallback_filenames = ["CLAUDE.md"]`，让 Codex 读取 Claude 规则
2. **Skills 符号链接** — `ln -s ~/shared-skills ~/.agents/skills/ && ln -s ~/shared-skills ~/.claude/skills/`
3. **权限意图转换** — Claude 的细粒度 allow/deny/ask → Codex 的 sandbox + approval_policy，不能直译
4. **逐个迁移** — 先迁移核心 Skills，再迁移 Hooks，最后配置
