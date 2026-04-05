---
tags: [claude, ai, 工具使用, 斜杠命令, slash-commands]
created: 2026-04-05
updated: 2026-04-05
---

# Claude Code Slash Commands 完整参考

> [!info] 概述
> **一句话定义**：斜杠命令是以 `/` 开头的快捷指令，用于控制 Claude Code 会话行为、执行预定义工作流。
> **通俗比喻**：就像命令行的快捷键 —— 输入 `/help` 就像按 F1 查看帮助，输入 `/commit` 就像一键执行 git 提交流程。

## 核心概念

### 是什么

Slash Commands 是 Claude Code 交互会话中的**快捷指令系统**，通过输入 `/命令名` 快速触发预定义操作。

### 命令类型

| 类型 | 来源 | 示例 | 说明 |
|------|------|------|------|
| **内置命令** | Claude Code 内置 | `/help`, `/clear`, `/model` | 55+ 个开箱即用 |
| **Bundled Skills** | Claude Code 内置技能 | `/simplify`, `/batch`, `/debug` | 5 个捆绑技能 |
| **自定义 Skills** | 用户创建 | `/review`, `/commit` | 存放在 `.claude/skills/` |
| **Legacy Commands** | 旧版命令格式 | `.claude/commands/*.md` | 仍支持，推荐迁移到 Skills |
| **Plugin Commands** | 插件提供 | `/plugin-name:command` | 安装插件后可用 |
| **MCP Prompts** | MCP 服务器提供 | `/mcp__github__list_prs` | 连接 MCP 后可用 |

> [!important] 📢 重要更新
> **自定义 Slash Commands 已合并到 Skills** - `.claude/commands/` 文件仍然有效，但推荐新开发使用 Skills（`.claude/skills/<name>/SKILL.md`）。当同路径同时存在 Skills 和 Commands 时，**Skills 优先**。

### 通俗理解

**🎯 比喻**：
- **内置命令** = 手机自带的系统功能（设置、相机、闹钟）
- **Skills** = 你下载安装的 App（可扩展、可自定义）
- **MCP Prompts** = 连接外部服务的插件（如 GitHub、Slack）

**📦 示例**：
```
# 查看帮助（内置命令）
/help

# 清除对话（内置命令）
/clear

# 代码审查（自定义 Skill）
/review src/auth.ts

# 列出 GitHub PR（MCP 命令）
/mcp__github__list_prs
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - 命令类型说明

---

## 内置命令完整参考

### 如何查看可用命令

在 Claude Code 中输入 `/` 即可看到所有可用命令，或输入 `/` + 字母进行筛选。

> [!tip] 提示
> `/` 菜单同时显示内置命令和捆绑 Skills（如 `/simplify`）。部分命令可能因平台或订阅计划而异。

### 会话管理命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/clear` | 清除对话 | 别名：`/reset`, `/new` |
| `/branch [name]` | 分支对话到新会话 | 别名：`/fork`（v2.1.77 重命名） |
| `/resume [session]` | 恢复对话 | 别名：`/continue` |
| `/rename [name]` | 重命名会话 | 便于会话管理 |
| `/export [filename]` | 导出对话 | 导出到文件或剪贴板 |
| `/rewind` | 回滚对话/代码 | 别名：`/checkpoint` |
| `/compact [instructions]` | 压缩对话 | 可指定焦点指令 |

### 系统配置命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/config` | 打开设置 | 别名：`/settings` |
| `/model [model]` | 选择模型 | 左右箭头切换 effort 级别 |
| `/effort [level]` | 设置努力级别 | `low`/`medium`/`high`/`max`/`auto`，`max` 需要 Opus 4.6 |
| `/fast [on\|off]` | 切换快速模式 | 加速响应 |
| `/theme` | 更改颜色主题 | 自定义界面外观 |
| `/color [color\|default]` | 设置提示栏颜色 | 个性化配色 |
| `/vim` | 切换 Vim 模式 | 启用 Vim 风格编辑 |
| `/keybindings` | 打开快捷键配置 | 自定义键盘操作 |
| `/terminal-setup` | 配置终端快捷键 | 终端交互优化 |

### 工具与集成命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/add-dir <path>` | 添加工作目录 | 扩展代码库范围 |
| `/agents` | 管理 Agent 配置 | Agent 设置 |
| `/chrome` | 配置 Chrome 集成 | 浏览器集成 |
| `/ide` | 管理 IDE 集成 | IDE 连接设置 |
| `/mcp` | 管理 MCP 服务器 | MCP 配置和 OAuth |
| `/plugin` | 管理插件 | 插件安装和管理 |
| `/reload-plugins` | 重新加载插件 | 刷新插件状态 |
| `/hooks` | 查看 Hook 配置 | 事件驱动自动化 |

### 权限与安全命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/permissions` | 查看/更新权限 | 别名：`/allowed-tools` |
| `/sandbox` | 切换沙盒模式 | 安全隔离执行 |
| `/security-review` | 安全漏洞分析 | 分析分支安全问题 |
| `/privacy-settings` | 隐私设置 | 仅 Pro/Max 可用 |
| `/login` | 切换账户 | 切换 Anthropic 账户 |
| `/logout` | 退出登录 | 退出当前账户 |

### Git 与 GitHub 命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/diff` | 交互式差异查看器 | 查看未提交更改 |
| `/pr-comments [PR]` | 获取 PR 评论 | GitHub PR 评论 |
| `/install-github-app` | 设置 GitHub Actions | GitHub 集成 |

### 信息与调试命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/help` | 显示帮助 | 命令帮助信息 |
| `/status` | 显示状态 | 版本、模型、账户 |
| `/cost` | Token 使用统计 | 费用分析 |
| `/context` | 可视化上下文使用 | 彩色网格显示 |
| `/stats` | 可视化使用统计 | 每日使用、会话、连续天数 |
| `/doctor` | 诊断安装健康 | 排查问题 |
| `/insights` | 生成会话分析报告 | 使用洞察 |
| `/release-notes` | 查看更新日志 | 版本更新信息 |

### 任务与调度命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/tasks` | 列出/管理后台任务 | 后台任务管理 |
| `/schedule [description]` | 创建/管理定时任务 | 定时执行 |
| `/plan [description]` | 进入规划模式 | 任务规划 |

### 多平台命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/desktop` | 在桌面应用中继续 | 别名：`/app` |
| `/mobile` | 移动端二维码 | 别名：`/ios`, `/android` |
| `/remote-control` | 从 claude.ai 远程控制 | 别名：`/rc` |
| `/remote-env` | 配置远程环境 | 远程开发设置 |

### 其他实用命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `/copy [N]` | 复制助手响应 | `w` 参数写入文件 |
| `/btw <question>` | 旁注问题 | 不添加到历史记录 |
| `/memory` | 编辑 CLAUDE.md | 切换自动记忆 |
| `/init` | 初始化 CLAUDE.md | 设置 `CLAUDE_CODE_NEW_INIT=true` 启用交互式流程 |
| `/voice` | 切换语音听写 | 按住说话 |
| `/feedback` | 提交反馈 | 别名：`/bug` |
| `/passes` | 分享免费周 | 邀请功能 |
| `/extra-usage` | 配置额外用量 | 速率限制配置 |
| `/install-slack-app` | 安装 Slack 应用 | Slack 集成 |
| `/exit` | 退出 REPL | 别名：`/quit` |

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Built-in Commands Reference
> - [Claude Code Interactive Mode Docs](https://code.claude.com/docs/en/interactive-mode) - 官方交互模式文档

---

## Bundled Skills（捆绑技能）

Claude Code 内置了 5 个捆绑技能，像斜杠命令一样调用：

| Skill | 用途 | 说明 |
|-------|------|------|
| `/batch <instruction>` | 大规模并行更改 | 使用 worktrees 编排批量修改 |
| `/claude-api` | 加载 Claude API 参考 | 项目语言相关 API 文档 |
| `/debug [description]` | 启用调试日志 | 读取调试日志排查问题 |
| `/loop [interval] <prompt>` | 重复运行提示 | 按间隔执行（如 `/loop 5m check the deploy`） |
| `/simplify [focus]` | 审查代码质量 | 检查更改文件的可重用性、质量和效率 |

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Bundled Skills

---

## 自定义命令（Skills）

### 为什么要用 Skills

相比旧版 Commands，Skills 提供更多功能：

| 特性 | Skills | Legacy Commands |
|------|--------|-----------------|
| **目录结构** | ✅ 支持脚本、模板、资源 | ❌ 单文件 |
| **自动触发** | ✅ AI 可自动调用 | ❌ 仅手动调用 |
| **调用控制** | ✅ 灵活配置 | ❌ 无 |
| **子代理执行** | ✅ 支持 `context: fork` | ❌ 无 |
| **渐进式加载** | ✅ 按需加载 | ❌ 完整加载 |

### 文件位置

```
# 推荐方式：Skills
.claude/skills/<name>/SKILL.md     # 项目级（团队共享）
~/.claude/skills/<name>/SKILL.md   # 用户级（个人）

# 旧版方式（仍支持）
.claude/commands/<name>.md         # 项目级
~/.claude/commands/<name>.md       # 用户级
```

### 创建自定义 Skill

```bash
# 创建目录
mkdir -p .claude/skills/my-command

# 创建 SKILL.md 文件
```

**SKILL.md 示例**：

```markdown
---
name: my-command
description: 命令描述，用于触发匹配
argument-hint: [可选参数提示]
allowed-tools: Bash(npm *), Read, Grep
---

# 命令标题

## 上下文
- 当前分支: !`git branch --show-current`
- 相关文件: @package.json

## 执行步骤
1. 第一步
2. 第二步: $ARGUMENTS
3. 第三步
```

### Frontmatter 字段参考

| 字段 | 用途 | 默认值 |
|------|------|--------|
| `name` | 命令名称（变成 `/name`） | 目录名 |
| `description` | 简短描述（触发匹配用） | 第一段 |
| `argument-hint` | 参数提示（自动补全） | 无 |
| `allowed-tools` | 免权限提示的工具 | 继承 |
| `model` | 指定模型 | 继承 |
| `disable-model-invocation` | 仅用户调用 | `false` |
| `user-invocable` | 从 `/` 菜单隐藏 | `true` |
| `context` | 设为 `fork` 在隔离子代理运行 | 无 |
| `agent` | 子代理类型（`context: fork` 时） | `general-purpose` |
| `hooks` | Skill 作用域钩子 | 无 |

### 参数处理

```markdown
# 所有参数
Fix issue #$ARGUMENTS

# 单个参数
Review PR #$0 with priority $1

# 用法：/review-pr 456 high
# 结果：$0 = "456", $1 = "high"
```

### 动态上下文注入

```markdown
---
name: commit
description: 创建 git commit
allowed-tools: Bash(git *)
---

## 上下文
- 当前 git 状态: !`git status`
- 当前 git diff: !`git diff HEAD`
- 当前分支: !`git branch --show-current`
- 最近提交: !`git log --oneline -5`

## 任务
根据以上更改创建一个 git commit。
```

### 文件引用

```markdown
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Creating a Custom Command as a Skill

---

## Plugin 命令

插件可以提供自定义命令：

```
/plugin-name:command-name
```

或无命名冲突时简化为：

```
/command-name
```

**示例**：
```
/frontend-design:frontend-design
/commit-commands:commit
```

---

## MCP Prompts 作为命令

MCP 服务器可暴露 prompts 作为斜杠命令：

```
/mcp__<server-name>__<prompt-name> [arguments]
```

**示例**：
```
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug title" high
```

### MCP 权限语法

在权限配置中控制 MCP 服务器访问：

- `mcp__github` - 访问整个 GitHub MCP 服务器
- `mcp__github__*` - 通配符访问所有工具
- `mcp__github__get_issue` - 特定工具访问

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - MCP Prompts as Commands

---

## 命令架构与生命周期

### 命令架构图

```
graph TD
    A["用户输入: /command-name"] --> B{"命令类型?"}
    B -->|内置| C["执行内置命令"]
    B -->|Skill| D["加载 SKILL.md"]
    B -->|Plugin| E["加载插件命令"]
    B -->|MCP| F["执行 MCP Prompt"]

    D --> G["解析 Frontmatter"]
    G --> H["变量替换"]
    H --> I["执行 Shell 命令"]
    I --> J["发送给 Claude"]
    J --> K["返回结果"]
```

### 命令生命周期

```
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant FS as 文件系统
    participant CLI as Shell/Bash

    User->>Claude: 输入 /optimize
    Claude->>FS: 搜索 .claude/skills/ 和 .claude/commands/
    FS-->>Claude: 返回 optimize/SKILL.md
    Claude->>Claude: 解析 frontmatter
    Claude->>CLI: 执行 !`command` 替换
    CLI-->>Claude: 命令输出
    Claude->>Claude: 替换 $ARGUMENTS
    Claude->>User: 处理提示词
    Claude->>User: 返回结果
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Command Architecture

---

## 实用自定义命令示例

### 1. `/commit` - 智能提交

```markdown
---
name: commit
description: 创建规范的 git commit
allowed-tools: Bash(git *)
---

## 上下文
- Git 状态: !`git status`
- Git 差异: !`git diff --cached`
- 当前分支: !`git branch --show-current`
- 最近提交: !`git log --oneline -5`

## 任务
根据以上更改创建 Conventional Commits 规范的提交：
- feat: 新功能
- fix: 修复 bug
- docs: 文档
- refactor: 重构
- test: 测试
- chore: 构建/工具

要求：
1. subject 不超过 50 字符
2. 简洁描述做了什么
```

### 2. `/push-all` - 安全推送

```markdown
---
name: push-all
description: 暂存、提交并推送（含安全检查）
allowed-tools: Bash(git *)
---

执行以下操作：

1. 暂存所有更改
2. 创建提交
3. 推送到远程

**安全检查**：
- ❌ 敏感文件：`.env*`, `*.key`, `*.pem`, `credentials.json`
- ❌ API 密钥：检测真实密钥 vs 占位符
- ❌ 大文件：`>10MB` 无 Git LFS
- ❌ 构建产物：`node_modules/`, `dist/`, `__pycache__/`
```

### 3. `/pr` - PR 准备

```markdown
---
name: pr
description: PR 准备清单
allowed-tools: Bash(git *), Bash(npm *)
---

## PR 准备清单

1. ✅ 代码检查 (lint)
2. ✅ 测试通过
3. ✅ 提交格式规范
4. ✅ 无敏感信息
5. ✅ 文档更新

请逐一检查并报告结果。
```

### 4. `/optimize` - 代码优化

```markdown
---
name: optimize
description: 代码优化分析
---

分析代码的以下方面：

1. **性能问题**：循环、算法复杂度
2. **内存泄漏**：未释放资源
3. **代码质量**：重复代码、可读性
4. **最佳实践**：设计模式、SOLID 原则

提供具体的优化建议和示例代码。
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Available Commands in This Folder

---

## 安装自定义命令

### 作为 Skills（推荐）

```bash
# 创建 skills 目录
mkdir -p .claude/skills

# 为每个命令创建 skill 目录
for cmd in optimize pr commit; do
  mkdir -p .claude/skills/$cmd
  cp 01-slash-commands/$cmd.md .claude/skills/$cmd/SKILL.md
done
```

### 作为 Legacy Commands

```bash
# 项目级（团队共享）
mkdir -p .claude/commands
cp 01-slash-commands/*.md .claude/commands/

# 用户级（个人）
mkdir -p ~/.claude/commands
cp 01-slash-commands/*.md ~/.claude/commands/
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Installation

---

## 最佳实践

### Do ✅

| 实践 | 说明 |
|------|------|
| 使用清晰的命令名称 | `code-review` > `cr` |
| 包含 description | 帮助 AI 判断何时触发 |
| 保持命令聚焦 | 一个命令一个任务 |
| 使用 `disable-model-invocation` | 有副作用的命令 |
| 使用 `!` 获取动态上下文 | 不要假设当前状态 |
| 组织相关文件在 skill 目录 | 便于维护 |

### Don't ❌

| 避免 | 原因 |
|------|------|
| 为一次性任务创建命令 | 过度设计 |
| 在命令中硬编码敏感信息 | 安全风险 |
| 跳过 description 字段 | AI 无法正确触发 |
| 复杂逻辑全放一个文件 | 难以维护 |

---

## 故障排除

### 命令找不到

**解决方案**：
1. 检查文件是否在 `.claude/skills/<name>/SKILL.md` 或 `.claude/commands/<name>.md`
2. 验证 frontmatter 中的 `name` 字段与预期命令名匹配
3. 重启 Claude Code 会话
4. 运行 `/help` 查看可用命令

### 命令执行不符合预期

**解决方案**���
1. 添加更具体的指令
2. 在 skill 文件中包含示例
3. 检查 `allowed-tools` 是否正确配置
4. 先用简单输入测试

### Skill vs Command 冲突

如果同时存在同名，**Skill 优先**。删除其中一个或重命名。

### 从 Commands 迁移到 Skills

```
# 迁移前（Command）
.claude/commands/optimize.md

# 迁移后（Skill）
.claude/skills/optimize/SKILL.md
```

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Troubleshooting

---

## 版本更新历史

### 近期变更

| 版本 | 变更 |
|------|------|
| v2.1.77 | `/fork` 重命名为 `/branch`，保留 `/fork` 作为别名 |
| v2.1.73 | `/output-style` 废弃 |
| - | `/review` 废弃，替换为 `code-review` 插件 |
| - | `/effort` 命令添加，`max` 级别需要 Opus 4.6 |
| - | `/voice` 命令添加（按住说话语音听写） |
| - | `/schedule` 命令添加（定时任务） |
| - | `/color` 命令添加（提示栏自定义） |
| - | `/model` 选择器显示人类可读标签（如 "Sonnet 4.6"） |
| - | `/resume` 支持 `/continue` 别名 |
| - | MCP prompts 可作为 `/mcp__<server>__<prompt>` 命令使用 |

> [!info] 📚 来源
> - [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - Recent Changes

---

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[01-基础概念/Skills 是什么]] | Slash Commands 已合并到 Skills，Skills 是当前标准 |
| [[02-工具使用/Claude Code Hooks 使用指南]] | Hooks 是事件驱动，Commands 是用户/主动触发 |
| [[04-高级应用/Claude Subagent 使用指南]] | Subagent 独立上下文，Skill 共享上下文 |
| [[03-进阶应用/Claude MCP 使用指南]] | MCP 提供 prompts 作为斜杠命令 |
| [[03-进阶应用/如何编写Skills]] | Skills 编写实战指南 |

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[01-基础概念/Skills 是什么]] - Skills 概念详解
- [[02-工具使用/Claude Code 自定义斜杠命令教程]] - 自定义命令教程
- [[03-进阶应用/如何编写Skills]] - Skills 编写实战
- [[02-工具使用/Claude Code 常用功能]] - 常用功能速查
- [[02-工具使用/Claude Code Hooks 使用指南]] - 事件驱动自动化

---

## 参考资料

### 官方资源
- [Claude Code Interactive Mode Docs](https://code.claude.com/docs/en/interactive-mode) - 官方交互模式文档
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills) - Skills 完整参考
- [Claude API - Slash Commands](https://platform.claude.com/docs/en/agent-sdk/slash-commands) - SDK 中的斜杠命令

### 社区资源
- [GitHub - claude-howto Slash Commands](https://github.com/luongnv89/claude-howto/tree/main/01-slash-commands) - 详细指南和示例
- [GitHub - odbo Ball Team claude-commands](https://github.com/oddballteam/claude-commands) - 工程工作流命令

### 相关技能
- [Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Skills 完整参考
- [Hooks Guide](https://code.claude.com/docs/en/hooks) - 事件驱动自动化
- [Plugins Guide](https://code.claude.com/docs/en/plugins) - 插件系统
