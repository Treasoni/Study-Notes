---
title: 完整对照表与从 Claude Code 迁移实战
tags: [codex, claude-code, migration, comparison, best-practices, common-pitfalls]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# 完整对照表与从 Claude Code 迁移实战

前七章我们深入剖析了 Codex 的每一个配置子系统——核心配置、指令系统、技能体系、子代理、MCP、钩子、CLI 调试。如果你一路读下来，应该已经对 Codex 的各个部件有了清晰的认知。但有一个问题始终悬而未决：**如果你是个 Claude Code 老用户，手头有一套磨合已久的配置——一套 CLAUDE.md、十几个技能、若干个 MCP 服务器、精心调教的权限规则——怎么把它搬到 Codex 上？**

这一章不做概念分析，只做一件事：**给出手。** 先给一张完整的配置对照表让你看清每个维度的对应关系，再给一套四步迁移策略让你按图索骥，最后用常见陷阱和最佳实践帮你避开坑。结尾配一个完整的项目配置样板，可以作为你迁移的起点模板。

---

## 1. 完整对照表：Codex vs Claude Code 所有配置维度

以下表格覆盖 21 个配置维度——比大纲所说的 18+ 还多几个，包括了书中讨论过的所有配置面。每一行标注了 "迁移难度" 和 "关键提示"，方便你排优先级。

### 1.1 文件与路径对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 | 关键提示 |
|---|---------|-------|-------------|---------|---------|
| 1 | **配置文件格式** | TOML（主）+ JSON/YAML | JSON | 低 | 格式转换即可，大部分配置项语义一一对应 |
| 2 | **全局配置路径** | `~/.codex/config.toml` | `~/.claude/settings.json` | 低 | 复制后转换格式 |
| 3 | **项目配置路径** | `.codex/config.toml` | `.claude/settings.json` | 低 | 同上，注意路径不同 |
| 4 | **本地覆盖机制** | `-c key=val` CLI 参数 | `.claude/settings.local.json` | 低 | Codex 更灵活，CLI 参数覆盖优先级最高 |
| 5 | **环境变量重定向** | `CODEX_HOME` | 无标准变量 | 低 | Codex 独有 |

### 1.2 指令与规则对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 | 关键提示 |
|---|---------|-------|-------------|---------|---------|
| 6 | **指令文件名** | AGENTS.md | CLAUDE.md | **零** | 设置 `project_doc_fallback_filenames = ["CLAUDE.md"]` 即可直接读取 |
| 7 | **指令层级** | 全局 + 项目根到当前目录逐级拼接 | 单文件 + 路径作用域 rules/ | 中 | 你的 CLAUDE.md 不需要拆分，fallback 原样加载 |
| 8 | **规则系统** | `.codex/rules/*.rules`（Starlark 语言） | `.claude/rules/*.md`（Markdown 描述） | **高** | 语法和机制完全不同，需要重写 |
| 9 | **指令容量限制** | 默认 32 KiB（`project_doc_max_bytes` 控制） | 建议 200-300 行最优 | 低 | 如果 CLAUDE.md 超过 32 KiB，需精简或拆分 |

### 1.3 技能系统对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 | 关键提示 |
|---|---------|-------|-------------|---------|---------|
| 10 | **技能标准** | Agent Skills Standard | Agent Skills Standard | **零** | 完全相同！无需修改 frontmatter |
| 11 | **技能发现路径** | `.agents/skills/` | `.claude/skills/` | 低 | 符号链接即可共享 |
| 12 | **技能调用方式** | `/skills` + description 隐式匹配 | `/skill-name` + description 隐式匹配 | 低 | 调用语法略有不同 |
| 13 | **技能参数传递** | 无 | `$ARGUMENTS` / `$0` / `$1` | **高** | 现有技能用到参数传递需重构 |
| 14 | **技能子代理** | 无 | `context: fork` | **高** | Codex 无对应功能 |
| 15 | **技能禁用** | `[[skills.config]]` + `enabled=false` | 移出目录或 Managed Settings | 低 | Codex 更结构化 |
| 16 | **Codex 扩展元数据** | `agents/openai.yaml`（UI 显示） | 无 | 低 | 可选增强，不影响功能 |

### 1.4 扩展与安全对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 | 关键提示 |
|---|---------|-------|-------------|---------|---------|
| 17 | **Agents 格式** | `.codex/agents/*.toml` | `.claude/agents/*.md` | 中 | 语义相近，格式不同 |
| 18 | **MCP 配置格式** | `[mcp_servers.<id>]` TOML | `mcpServers` JSON | 低 | 语义完全对应，格式转换即可 |
| 19 | **MCP 审批模式** | auto / prompt / writes / approve | allow / deny / ask | 中 | 需要做意图映射 |
| 20 | **Hooks 事件数** | 11 种 | 4 种核心 | 中 | 核心钩子可迁移，额外事件可选 |
| 21 | **权限模型** | sandbox_mode + approval_policy | allow / deny / ask 细粒度 | **高** | 两套范式完全不同，不能直译 |

### 1.5 Codex 独有功能（Claude Code 无对应）

| # | 配置维度 | 说明 | 迁移关注点 |
|---|---------|------|-----------|
| 22 | **Profiles 多环境配置档** | `[profiles.NAME]` 按场景切换 | 不需要迁移，直接新增 |
| 23 | **插件系统** | `.codex-plugin/plugin.json` | 不需要迁移，可选增强 |
| 24 | **多模型提供商** | ollama / lmstudio / OpenRouter / Azure 等 | 不需要迁移，按需配置 |
| 25 | **Sandbox 沙箱模式** | read-only / workspace-write / danger-full-access | 需要理解范式差异 |

> **核心结论**：迁移难度可以分为三档——
> - **零/低难度（约 12 项）**：格式转换、路径调整、符号链接即可完成
> - **中难度（约 5 项）**：需要理解语义差异并做意图映射
> - **高难度（约 4 项）**：参数传递、子代理、规则系统、权限模型，需要重写

---

## 2. 迁移四步走策略

不要试图一次性把整套配置搬过去。以下是四步渐进策略，每步完成后你都可以停下来正常使用 Codex，再进入下一步。

### 第一步：指令兼容（5 分钟）

这是最高性价比的一步——**不需要修改任何现有文件**。

```toml
# .codex/config.toml — 一行配置让 Codex 读取你的 CLAUDE.md
[project_doc]
fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
max_bytes = 32768
```

加上这行配置后，Codex 会在遍历 AGENTS.md 找不到时自动回退到 CLAUDE.md。你的所有现有指令直接生效。

**验证**：运行以下命令确认加载状态：

```bash
codex status
codex --cd . "请列出所有已加载的指令文件"
```

预期输出应该包含你的 CLAUDE.md 路径。如果看不到，检查文件名拼写和文件位置（必须是 Git 仓库根目录）。

### 第二步：技能共享（10 分钟）

利用 Agent Skills Standard 的兼容性，通过符号链接让两个工具共享同一套技能。

**如果你维护了独立技能仓库**（推荐方案）：

```bash
# 假设你的技能仓库在 ~/shared-skills/
# 为 Codex 创建符号链接
ln -s ~/shared-skills ~/.agents/skills/

# 为 Claude Code 创建符号链接（如果还没做）
ln -s ~/shared-skills ~/.claude/skills/
```

**如果技能散落在 Claude Code 目录中**：

```bash
# 方案 A：把整个 .claude/skills/ 链接到 Codex
ln -s ~/.claude/skills ~/.agents/skills/

# 方案 B：逐个链接特定技能
ln -s ~/.claude/skills/my-skill ~/.agents/skills/my-skill
```

**验证**：

```bash
# 启动 Codex 交互式会话后输入
/skills
```

应该能看到所有技能出现在列表中。

**注意事项**：
- 使用了 `$ARGUMENTS` 参数传递的技能需要重构——Codex 不支持参数传递
- 使用了 `context: fork` 子代理的技能需要简化——去掉 frontmatter 中的 `context` 字段
- 使用了 `allowed-tools` 限制的技能——Codex 无此概念，但可以通过 Starlark 规则实现类似效果

### 第三步：权限意图转换（需要理解，不能直译）

这是最容易出错的步骤。Claude Code 和 Codex 的权限模型是**两种不同的设计哲学**：

| Claude Code 哲学 | Codex 哲学 |
|------------------|-----------|
| 工具级细粒度控制（每个工具 allow/deny/ask） | 环境级沙箱控制（读/写/全权限） |
| 你控制 agent 能用什么工具 | 你控制 agent 能访问什么资源 |
| 审批粒度：工具调用级别 | 审批粒度：操作类型级别 |

**转换规则**：

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

假设你的 Claude Code 配置是：agent 可以读写 workspace，能联网，但不能读 `.env`，不能写 `/etc/`。对应的 Codex 配置是：

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = true  # 允许联网

[permissions.scoped]
# 拒绝访问 .env 文件

[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
"**/.env.*" = "deny"
```

> **关键原则**：不要试图找到"一一对应"的配置项。Claude Code 的细粒度工具权限 vs Codex 的环境级沙箱是两套不同的安全模型，**理解意图再做转换**，而不是逐行直译。

### 第四步：逐个迁移（按优先级顺序）

前面的三步已经让你的项目在 Codex 上"能用"了。第四步的价值在于：把你原有的整套配置体系完整地迁移到 Codex 原生方案上，充分利用 Codex 独有的能力。

**推荐优先级顺序**：

```
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

**第一步：迁移 MCP 服务器**

这是性价比最高的迁移，纯格式转换，不需要理解新概念。

```bash
# 查看你当前的 Claude Code MCP 配置
cat ~/.claude/settings.json | jq '.mcpServers'

# 用 codex mcp add 逐条添加
codex mcp add filesystem --cmd "npx -y @modelcontextprotocol/server-filesystem /path"

# 或直接编辑 .codex/config.toml 添加
```

TOML 格式对照（Claude Code JSON → Codex TOML）：

```toml
# Claude Code（原配置）
# "mcpServers": {
#   "filesystem": {
#     "command": "npx",
#     "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
#   }
# }

# Codex（迁移后）
[mcp_servers.filesystem]
command = "npx"
args    = ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
startup_timeout_sec = 10
tool_timeout_sec    = 60
```

**第二步：迁移 Hooks**

Claude Code 的 4 种核心钩子（PreToolUse, PostToolUse, SessionStart, UserPromptSubmit）在 Codex 上都有对应。直接复制 JSON 配置即可：

```json
// hooks.json — 与 Claude Code 格式几乎相同
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
            "timeout": 600
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/pre_bash.py",
            "timeout": 100
          }
        ]
      }
    ]
  }
}
```

> **注意**：Codex hooks 的 matcher 用正则匹配工具名，Claude Code 是直接指定事件名。如果原配置中没有复杂的匹配逻辑，直接复制即可。

**第三步：重构 CLAUDE.md 为 AGENTS.md（可选，但推荐）**

分层的 AGENTS.md 让你能做 CLAUDE.md 做不到的事：项目根目录放通用规则，子目录放局部规则。

```
# 项目根目录 .codex/AGENTS.md — 全局约束
## 全局规则
- 使用 pnpm 管理依赖
- 代码提交前运行 lint
- API 密钥从 .env 读取

# src/api/ 目录 .codex/AGENTS.md — 局部规则
## API 开发规则
- 所有 API 路由使用 async handler
- 请求参数使用 zod 校验
- 返回统一格式 { code, data, message }
```

**第四步和第五步**：Starlark 规则和 Profiles/插件是高难度或纯 Codex 独有，建议等你对 Codex 足够熟悉后再深入。第一次迁移做到前三步就够了。

---

## 3. 常见陷阱 6 条

以下陷阱来自实际迁移经验，每一条我都见过有人踩过。

### 陷阱 1：静默忽略 —— 把安全配置放到项目级

**症状**：`approval_policy`、`sandbox_mode`、`model_provider` 等配置项写在 `.codex/config.toml` 中，但完全不起作用。

**原因**：Codex 有一份静默忽略列表（silent ignore list），以下键**只能**设在用户级 `~/.codex/config.toml`，写在项目级会被静默忽略：

```
openai_base_url, chatgpt_base_url, model_provider, model_providers,
notify, profile, profiles, approval_policy, sandbox_mode,
sandbox_workspace_write.*, experimental_realtime_ws_base_url,
otel.*, apps_mcp_product_sku
```

**对策**：
```bash
# 正确做法：放用户级
echo '[approval_policy]
granular = { sandbox_approval = true }' >> ~/.codex/config.toml

# 错误做法（被静默忽略，不会报错）
echo '[approval_policy]
granular = { sandbox_approval = true }' >> .codex/config.toml
```

### 陷阱 2：网络权限未开启导致工具安装失败

**症状**：使用 pip / npm 安装包时卡住或失败，agent 无法完成任务。

**原因**：`workspace-write` 沙箱模式下 `network_access` 默认为 false，阻止所有出站连接。

**对策**：
```toml
[sandbox_workspace_write]
network_access = true  # 允许出站 HTTP（pip/npm/curl 需要）
```

### 陷阱 3：安全组合爆炸 —— "never" + "danger" = 无安全网

**症状**：agent 意外删除了重要文件或执行了危险命令，造成实际损失。

**原因**：以下组合形同虚设：

```toml
approval_policy = "never"     # 从不询问
sandbox_mode = "danger-full-access"  # 完全访问
```

两个配置单独看都有合理用途，但组合起来意味着 agent 可以做任何事情而不需要任何审批。

**对策**：如果你要让 agent 访问更多资源，**优先扩展 `writable_roots`**，而不是提到 `danger-full-access`。即使 `approval_policy = "never"`，也至少保持沙箱限制：

```toml
sandbox_mode = "workspace-write"
approval_policy = "never"  # 只跳过审批，但沙箱仍在

[sandbox_workspace_write]
network_access = true
writable_roots = ["~/code/oss", "~/projects"]
```

### 陷阱 4：MCP 服务器超时被丢弃

**症状**：MCP 服务器配置似乎正确，但 tools 经常不可用，报超时错误。

**原因**：`startup_timeout_sec` 默认只有 10 秒，某些重 MCP 服务器（需要编译、下载依赖的）启动超过 10 秒就被 Codex 认为启动失败并丢弃。

**对策**：
```toml
[mcp_servers.heavy_server]
command = "node"
args    = ["dist/server.js"]
startup_timeout_sec = 30   # 调大到 30 秒
tool_timeout_sec    = 120   # 工具执行超时也适当调大
```

### 陷阱 5：环境变量泄漏

**症状**：子进程或 MCP 服务器意外访问到了不应该有的环境变量（如 `AWS_SECRET_ACCESS_KEY`）。

**原因**：默认 `shell_environment_policy.inherit = "all"`，当前 shell 的所有环境变量都传递给子进程。

**对策**：
```toml
[shell_environment_policy]
inherit = "core"  # 只继承 PATH/HOME 等基础变量

# 或使用白名单模式
inherit = "none"
include_only = ["PATH", "HOME", "NODE_ENV"]
```

### 陷阱 6：权限 glob 模式未限定作用域

**症状**：设置的权限规则意外影响了整个文件系统，而非预期的项目目录。

**原因**：`[permissions.scoped]` 中的 glob 模式未限定 `:workspace_roots` 作用域，导致全局匹配。

```toml
# 错误：未限定作用域，全局生效
[permissions.scoped.filesystem]
"**/.env" = "deny"  # 整个文件系统的 .env 都被拒绝

# 正确：限定到 workspace_roots
[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
```

---

## 4. Skills 最佳实践 5 条

这五条实践适合 Codex 和 Claude Code **共用**，它们基于 Agent Skills Standard，与工具无关。

### 实践 1：description 前置触发词

隐式匹配机制依靠的是 SKILL.md 的 `description` 字段。把最可能触发场景的词语放到描述的开头：

```yaml
---
name: react-unit-test
description: "React 组件单元测试，使用 Vitest + React Testing Library 为 React 组件编写测试用例"
---
```

而不是：

```yaml
---
name: react-unit-test
description: "为 React 组件编写测试用例的工具，使用 Vitest 和 React Testing Library"
---
```

前者以 "React 组件单元测试" 开头，agent 在处理测试任务时更容易匹配到。后者以 "工具" 开头，匹配粒度更粗。

### 实践 2：单一职责

一个技能只做一件事。如果发现你的 SKILL.md 中有 "如果做 A 则...，如果做 B 则..." 的段落，说明应该拆分为两个技能。

```
# 反例：一个技能做两件事
code-review-and-deploy/
├── SKILL.md  # "代码审查和部署"

# 正例：拆分为两个技能
code-review/
├── SKILL.md  # "代码审查，检查代码质量和安全问题"
deploy/
├── SKILL.md  # "项目部署，构建和发布到生产环境"
```

单一职责的好处：技能更容易被隐式匹配到，description 更聚焦，SKILL.md 更简短。

### 实践 3：指令优先于脚本

技能的职责是指引 agent 行为，而不是替代 agent。能用自然语言描述的步骤，不要写成脚本：

```
# 推荐的 SKILL.md
## 使用方法
当你需要配置新的 API 路由时，按照以下步骤：
1. 在 src/routes/ 下创建新文件
2. 使用 async handler 包装
3. 用 zod 校验请求参数
4. 在 src/routes/index.ts 注册路由
```

而不是：

```
# 不推荐的 SKILL.md
## 使用方法
运行以下命令创建一个新路由：
bash script/create-route.sh $name
```

**什么时候该用脚本**：当步骤涉及大量机械操作（批量重命名、格式化、数据转换），指令描述会很长时，才值得提取为脚本放在 `scripts/` 目录下。

### 实践 4：渐进披露

SKILL.md 保持简洁（建议 50 行以内），详细文档放在 `references/` 目录中，用 SKILL.md 中的链接指引。

```
my-skill/
├── SKILL.md           # 简洁的指令 + 场景描述
├── references/
│   ├── API.md         # 详细的 API 参考
│   ├── config.md      # 配置选项详解
│   └── examples.md    # 常见场景示例
```

SKILL.md 中通过相对路径引用：

```markdown
## 详细参考

- [API 文档](./references/API.md) — 所有可用接口的详细说明
- [配置选项](./references/config.md) — 配置参数详解
- [常见场景](./references/examples.md) — 典型使用案例
```

这利用了 Codex 的渐进式加载机制：agent 先读到 SKILL.md，只有在需要时才去读取 `references/` 中的详细文档，节省上下文空间。

### 实践 5：相对路径引用

SKILL.md 中所有路径引用都应基于技能根目录的相对路径。这样技能才能在不同项目间复用：

```markdown
# 正确：相对路径
查看 ./references/API.md  获取接口文档
运行 ./scripts/lint.sh    检查代码风格
```

```markdown
# 错误：绝对路径
查看 /home/user/skills/my-skill/references/API.md
```

相对路径确保了技能通过符号链接共享时，文件引用仍然有效。

---

## 5. 典型项目配置示例

以下是一个完整的 `.codex/config.toml`，覆盖了本章讨论的所有核心配置维度。你可以把它作为迁移起点，按需删减注释和调整值。

```toml
# ============================================
# .codex/config.toml — 项目级配置示例
# 适用于从 Claude Code 迁移到 Codex 的项目
# ============================================

# --- 项目标识 ---
name = "my-project"
description = "迁移示例项目"

# --- 模型配置 ---
model = "gpt-5.4"
model_reasoning_effort = "medium"
model_verbosity = "medium"

# --- 指令兼容 CLAUDE.md（迁移第一步） ---
[project_doc]
fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
max_bytes = 32768

# --- 沙箱模式（迁移第三步：权限意图转换后） ---
# 对应 Claude Code 的 "多数工具 allow + 高风险工具 ask"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = true          # 允许 pip/npm 安装
writable_roots = ["dist", "build", "node_modules"]

# --- 权限细粒度控制 ---
[permissions.scoped]

[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
"**/.git/" = "deny"
"node_modules/" = "read"

[permissions.scoped.network]
enabled = true
mode = "limited"

[permissions.scoped.network.domains]
"api.openai.com" = "allow"
"github.com" = "allow"
"registry.npmjs.org" = "allow"
"pypi.org" = "allow"

# --- MCP 服务器配置（迁移第四步第一步） ---
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "."]
startup_timeout_sec = 10
tool_timeout_sec = 60

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
startup_timeout_sec = 15
tool_timeout_sec = 120
# 审批模式：写操作时提示
approval_mode = "writes"

# --- 功能开关 ---
[features]
hooks = true
multi_agent = true
undo = true
codex_git_commit = false
prevent_idle_sleep = false

# --- Shell 环境策略（防止环境泄漏，陷阱 5） ---
[shell_environment_policy]
inherit = "core"
exclude = ["AWS_*", "SECRET_*", "TOKEN_*"]

# --- 项目信任（针对嵌套仓库） ---
[projects]
"../other-repo" = { trust_level = "trusted" }

# --- 技能禁用示例 ---
[[skills.config]]
path = "/path/to/outdated-skill/SKILL.md"
enabled = false
```

**同时在用户级 `~/.codex/config.toml` 中设置（因为静默忽略规则）：**

```toml
# ~/.codex/config.toml — 用户级配置
# 安全相关配置只能放这里！

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

[profiles.debug]
model = "gpt-5.4-mini"
model_reasoning_effort = "minimal"
model_verbosity = "high"
hooks = false  # 调试时跳过 hooks
```

> **项目级 + 用户级说明**：项目级的 `.codex/config.toml` 放业务相关配置（MCP 服务器、权限作用域、项目描述），用户级的 `~/.codex/config.toml` 放安全敏感配置（沙箱模式、审批策略、提供商）和全局偏好（profiles、模型选择）。这个分离本身就是一种最佳实践——你可以在不同项目中安全地切换，而不会因为忘记删除某个项目的 `approval_policy` 导致安全问题。

---

## 6. 迁移检查清单

完成了本章的所有步骤后，用以下清单逐一确认：

### 第一步：指令兼容
- [ ] `.codex/config.toml` 中设置了 `project_doc.fallback_filenames = ["CLAUDE.md"]`
- [ ] `codex status` 输出中可看到 CLAUDE.md 已被加载
- [ ] 你的自定义指令在 Codex 会话中生效

### 第二步：技能共享
- [ ] `~/.agents/skills/` 已存在（符号链接或目录）
- [ ] `/skills` 命令显示了所有预期技能
- [ ] 使用 `$ARGUMENTS` 参数传递的技能已重构或标记
- [ ] 使用 `context: fork` 的技能已移除该字段

### 第三步：权限意图转换
- [ ] 理解 sandbox_mode 三种模式的差异
- [ ] 理解 approval_policy 三种模式的行为
- [ ] 测试过 `pip install` / `npm install` 能在当前配置下正常工作
- [ ] 检查了敏感文件（.env、credentials 等）是否被适当保护

### 第四步：逐个迁移
- [ ] MCP 服务器全部迁移完成并验证可用
- [ ] Hooks 配置已迁移（或决定暂时跳过）
- [ ] （可选）CLAUDE.md 已重构为分层 AGENTS.md
- [ ] （可选）Starlark 规则已开始使用

### 避坑确认
- [ ] 安全敏感配置（sandbox_mode 等）放在用户级，不在项目级
- [ ] network_access = true 已设置（如需联网）
- [ ] 没有同时设置 `approval_policy = "never"` + `sandbox_mode = "danger-full-access"`
- [ ] MCP 服务器 `startup_timeout_sec` 足够大
- [ ] Shell 环境策略设置为 `"core"` 或已配置白名单
- [ ] 权限 glob 模式已限定 `:workspace_roots` 作用域

---

## 本章小结

- **完整对照表覆盖 21+ 配置维度**：包括文件路径、指令规则、技能系统、扩展机制、安全模型。核心结论是约 12 项可零/低成本迁移，4 项需要重写（参数传递、子代理、Starlark 规则、权限模型）。
- **四步迁移策略**：指令兼容（5 分钟，最高性价比）→ 技能共享（10 分钟，符号链接）→ 权限意图转换（需要理解范式差异，不能直译）→ 逐个迁移（按 MCP → Hooks → AGENTS.md → Starlark → Profiles 的优先级顺序）。三到四步后你的配置就完整可用。
- **六条常见陷阱有规律**：静默忽略键只能放用户级、网络权限默认关闭、never+danger 组合无安全网、MCP 超时需手动调大、环境变量需限制继承、权限 glob 需限定作用域。
- **五项 Skills 最佳实践**：description 前置触发词（提高隐式匹配率）、单一职责（技能聚焦）、指令优先于脚本（用自然语言描述步骤）、渐进披露（SKILL.md 简洁+references 详细）、相对路径引用（技能可复用）。
- **完整配置样板可作为迁移起点**：项目级放业务配置（MCP、权限作用域），用户级放安全敏感配置（沙箱、审批策略、提供商），这个分离本身就是一项关键最佳实践。

## 下一章预告

至此，所有章节都已完结。附录中有一份速查参考卡片——配置文件路径、常用 CLI 命令、关键配置项默认值——方便你日常翻阅，按需使用。
