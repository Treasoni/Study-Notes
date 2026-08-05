---
title: "Codex 完整配置体系"
tags: [codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# 第四章：Skills 技能系统 —— 创建、注册与共享
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


---

> [!note] 导航
> [[03 AGENTS.md 分层体系|← 上一章]] | [[05 Agents 与 MCP|下一章 →]]



