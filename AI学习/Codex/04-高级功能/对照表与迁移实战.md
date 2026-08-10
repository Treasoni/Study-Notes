---
title: 对照表与迁移实战
tags: [codex, ai, 工具使用, 高级功能, 迁移]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# 对照表与迁移实战

> [!info] 文档定位
> **一句话定位** - 本篇提供 Codex 与 Claude Code 的完整配置对照表（覆盖 21+ 配置维度），以及从 Claude Code 迁移到 Codex 的四步实战策略、六条常见陷阱与五项 Skills 最佳实践。适合已拥有一整套 Claude Code 配置、准备迁移到 Codex 或对照学习两大工具配置体系的进阶用户。

---

## 完整对照表

前七章深入剖析了 Codex 的每一个配置子系统。如果你一路读下来，应该已经对 Codex 的各个部件有了清晰的认知。但有一个问题始终悬而未决：**如果你是个 Claude Code 老用户，手头有一套磨合已久的配置——一套 CLAUDE.md、十几个技能、若干个 MCP 服务器、精心调教的权限规则——怎么把它搬到 Codex 上？**

这一章不做概念分析，只做一件事：**给出手。** 先给一张完整的配置对照表让你看清每个维度的对应关系，再给一套四步迁移策略让你按图索骥，最后用常见陷阱和最佳实践帮你避开坑。

### 文件与路径对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 1 | 配置文件格式 | TOML（主）+ JSON/YAML | JSON | 低 |
| 2 | 全局配置路径 | `~/.codex/config.toml` | `~/.claude/settings.json` | 低 |
| 3 | 项目配置路径 | `.codex/config.toml` | `.claude/settings.json` | 低 |
| 4 | 本地覆盖机制 | `-c key=val` CLI 参数 | `.claude/settings.local.json` | 低 |
| 5 | 环境变量重定向 | `CODEX_HOME` | 无标准变量 | 低 |

### 指令与规则对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 6 | 指令文件名 | AGENTS.md | CLAUDE.md | **零** |
| 7 | 指令层级 | 全局 + 逐级拼接 | 单文件 + 路径作用域 rules/ | 中 |
| 8 | 规则系统 | `.codex/rules/*.rules`（Starlark） | `.claude/rules/*.md`（Markdown） | **高** |
| 9 | 指令容量限制 | 默认 32 KiB | 建议 200-300 行 | 低 |

### 技能系统对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 10 | 技能标准 | Agent Skills Standard | Agent Skills Standard | **零** |
| 11 | 技能发现路径 | `.agents/skills/` | `.claude/skills/` | 低 |
| 12 | 技能调用方式 | `/skills` + description | `/skill-name` + description | 低 |
| 13 | 技能参数传递 | 无 | `$ARGUMENTS` / `$0` / `$1` | **高** |
| 14 | 技能子代理 | 无 | `context: fork` | **高** |
| 15 | 技能禁用 | `[[skills.config]]` + `enabled=false` | 移出目录 | 低 |

### 扩展与安全对照

| # | 配置维度 | Codex | Claude Code | 迁移难度 |
|---|---------|-------|-------------|---------|
| 16 | Agents 格式 | `.codex/agents/*.toml` | `.claude/agents/*.md` | 中 |
| 17 | MCP 配置格式 | `[mcp_servers.<id>]` TOML | `mcpServers` JSON | 低 |
| 18 | MCP 审批模式 | auto / prompt / writes / approve | allow / deny / ask | 中 |
| 19 | Hooks 事件数 | 11 种 | 4 种核心 | 中 |
| 20 | 权限模型 | sandbox_mode + approval_policy | allow / deny / ask 细粒度 | **高** |

### Codex 独有功能

| # | 配置维度 | 说明 |
|---|---------|------|
| 21 | Profiles 多环境配置档 | `[profiles.NAME]` 按场景切换 |
| 22 | 插件系统 | `.codex-plugin/plugin.json` |
| 23 | 多模型提供商 | ollama / lmstudio / OpenRouter / Azure 等 |
| 24 | Sandbox 沙箱模式 | read-only / workspace-write / danger-full-access |

> **核心结论**：约 12 项可零/低成本迁移，4 项需要重写（参数传递、子代理、Starlark 规则、权限模型）。

---

## 迁移四步走策略

### 第一步：指令兼容（5 分钟）

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

### 第二步：技能共享（10 分钟）

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

### 第三步：权限意图转换（需要理解，不能直译）

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

### 第四步：逐个迁移（按优先级顺序）

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

---

## 常见陷阱 6 条

### 陷阱 1：静默忽略 —— 把安全配置放到项目级

```bash
# 正确做法：放用户级
echo '[approval_policy]
granular = { sandbox_approval = true }' >> ~/.codex/config.toml

# 错误做法（被静默忽略，不会报错）
echo '[approval_policy]
granular = { sandbox_approval = true }' >> .codex/config.toml
```

### 陷阱 2：网络权限未开启导致工具安装失败

```toml
[sandbox_workspace_write]
network_access = true  # 允许出站 HTTP（pip/npm/curl 需要）
```

### 陷阱 3：安全组合爆炸 —— "never" + "danger" = 无安全网

```toml
# 避免的组合
approval_policy = "never"
sandbox_mode = "danger-full-access"

# 推荐的折中
sandbox_mode = "workspace-write"
approval_policy = "never"  # 只跳过审批，但沙箱仍在
```

### 陷阱 4：MCP 服务器超时被丢弃

```toml
[mcp_servers.heavy_server]
command = "node"
args    = ["dist/server.js"]
startup_timeout_sec = 30   # 默认 10s 不够
tool_timeout_sec    = 120
```

### 陷阱 5：环境变量泄漏

```toml
[shell_environment_policy]
inherit = "core"  # 只继承 PATH/HOME 等基础变量
```

### 陷阱 6：权限 glob 模式未限定作用域

```toml
# 错误：未限定作用域，全局生效
[permissions.scoped.filesystem]
"**/.env" = "deny"

# 正确：限定到 workspace_roots
[permissions.scoped.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
```

---

## Skills 最佳实践 5 条

### 实践 1：description 前置触发词

```yaml
# 推荐：以场景词开头
description: "React 组件单元测试，使用 Vitest + React Testing Library..."

# 不推荐：以泛化词开头
description: "为 React 组件编写测试用例的工具..."
```

### 实践 2：单一职责

一个技能只做一件事。如果发现 SKILL.md 中有"如果做 A 则...，如果做 B 则..."的段落，说明应该拆分为两个技能。

### 实践 3：指令优先于脚本

能用自然语言描述的步骤，不要写成脚本。脚本只在涉及大量机械操作时才值得提取。

### 实践 4：渐进披露

SKILL.md 保持简洁（建议 50 行以内），详细文档放在 `references/` 目录中。

### 实践 5：相对路径引用

所有路径引用都应基于技能根目录的相对路径，确保技能在不同项目间可复用。

---

## 典型项目配置示例

### 项目级 .codex/config.toml

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

### 用户级 ~/.codex/config.toml

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

---

## 迁移检查清单

### 第一步：指令兼容

- [ ] `.codex/config.toml` 中设置了 `project_doc.fallback_filenames = ["CLAUDE.md"]`
- [ ] `codex status` 输出中可看到 CLAUDE.md 已被加载
- [ ] 自定义指令在 Codex 会话中生效

### 第二步：技能共享

- [ ] `~/.agents/skills/` 已存在（符号链接或目录）
- [ ] `/skills` 命令显示了所有预期技能
- [ ] 使用 `$ARGUMENTS` 或 `context: fork` 的技能已处理

### 第三步：权限意图转换

- [ ] 理解 sandbox_mode 三种模式的差异
- [ ] 理解 approval_policy 三种模式的行为
- [ ] 测试过 `pip install` / `npm install` 能在当前配置下工作
- [ ] 检查了敏感文件（.env、credentials 等）是否被适当保护

### 第四步：逐个迁移

- [ ] MCP 服务器全部迁移完成并验证可用
- [ ] Hooks 配置已迁移（或决定暂时跳过）
- [ ] （可选）CLAUDE.md 已重构为分层 AGENTS.md

### 避坑确认

- [ ] 安全敏感配置放在用户级，不在项目级
- [ ] network_access = true 已设置（如需联网）
- [ ] 没有同时设置 `approval_policy = "never"` + `sandbox_mode = "danger-full-access"`
- [ ] MCP 服务器 `startup_timeout_sec` 足够大
- [ ] Shell 环境策略设置为 `"core"` 或已配置白名单
- [ ] 权限 glob 模式已限定 `:workspace_roots` 作用域

---

## 常见问题

### Q: 为什么我把 approval_policy 等安全配置写进项目级 `.codex/config.toml` 后不生效？
**回答**：因为安全相关配置放在项目级会被**静默忽略**，不会报错。正确做法是把 `[approval_policy]`、`sandbox_mode` 等安全敏感配置写入用户级 `~/.codex/config.toml`。这是「本地覆盖机制」「权限模型」维度迁移时的关键坑点（见常见陷阱 1）。

### Q: 从 Claude Code 迁移 Starlark 规则系统难吗？
**回答**：难度很高。Codex 的规则系统是 `.codex/rules/*.rules`（Starlark），与 Claude Code 的 `.claude/rules/*.md`（Markdown）完全不同，对照表中该维度迁移难度标记为「高」。在四步迁移策略中，Starlark 规则系统属于第四优先级（替换原有 rules），与技能参数传递、技能子代理、权限模型并列，是需要重写而非直译的 4 项之一。

### Q: 迁移后执行 pip install / npm install 失败怎么办？
**回答**：通常是沙箱未开启网络权限。在 `[sandbox_workspace_write]` 中设置 `network_access = true`（允许出站 HTTP，pip/npm/curl 需要）；更细粒度可在 `[permissions.scoped.network]` 中开启 `mode = "limited"` 并按域名配置白名单（如 `api.openai.com`、`github.com` = `"allow"`）。

---

## 最佳实践

### Do's
- 遵循「项目级放业务配置、用户级放安全敏感配置」的分离原则，把 `approval_policy`、`sandbox_mode` 等写进 `~/.codex/config.toml`。
- 迁移第一步用 `[project_doc] fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]` 一行兼容旧指令，实现零改动迁移，再通过 `codex status` 验证加载。
- Skills 遵循五项最佳实践：description 以场景触发词开头、单一职责、指令优先于脚本、渐进披露（SKILL.md 50 行以内）、相对路径引用。
- 利用 Agent Skills Standard 兼容性，通过符号链接（方案 A：独立技能仓库）让两个工具共享同一套技能，迁移前处理 `$ARGUMENTS`、`context: fork`、`allowed-tools` 差异。
- 需要联网时显式设置 `network_access = true`，并给 MCP 服务器调大 `startup_timeout_sec`（默认 10s 不够）。

### Don'ts
- 不要把安全配置放项目级 `.codex/config.toml`——会被**静默忽略**且不报错，排查困难。
- 不要设置 `approval_policy = "never"` + `sandbox_mode = "danger-full-access"` 组合——完全无安全网；需要免审批时也应保留 `workspace-write` 沙箱。
- 不要忘记开启网络权限就尝试 pip/npm/curl 安装工具——会因无出站网络而失败。
- 权限 glob 模式不要未限定作用域——必须用 `[permissions.scoped.filesystem.":workspace_roots"]` 限定范围，否则 `**/.env` 之类规则全局生效。
- 不要忽略 MCP 服务器启动超时——`startup_timeout_sec` 默认 10s 不够，重服务需调大（如 30s）。
- 除非必要，不要把 `[shell_environment_policy] inherit` 设为宽松值——用 `"core"` 只继承 PATH/HOME 等基础变量，避免环境变量泄漏。

---

## 小结

完整对照表覆盖 21+ 配置维度，约 12 项可零/低成本迁移，4 项需要重写（参数传递、子代理、Starlark 规则、权限模型）。四步迁移策略从指令兼容、技能共享、权限意图转换到逐个迁移渐进推进；六条常见陷阱按规律可循，五项 Skills 最佳实践帮助构建更高质量的技能库。核心原则一句话：项目级配置放业务配置，用户级配置放安全敏感配置。

> [!note] 本章小结
> 完整对照表覆盖 21+ 配置维度，约 12 项可零/低成本迁移，4 项需要重写。四步迁移策略从指令兼容到逐个迁移渐进推进。六条常见陷阱按规律可循，五项 Skills 最佳实践帮助你构建更高质量的技能库。项目级配置放业务配置，用户级配置放安全敏感配置——这个分离本身就是一项关键最佳实践。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Codex 配置哲学概览]] | 配置体系全景与哲学 |
| [[AGENTS.md 分层体系]] | CLAUDE.md → AGENTS.md 迁移 |
| [[Skills 技能系统]] | Skills 跨工具共享 |
| [[快速参考卡片]] | 路径/命令/默认值速查 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
