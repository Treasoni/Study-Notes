---
tags: [ai, 基础概念, skills]
created: 2025-10-01
updated: 2026-04-05
---

# Skills 技能系统

> [!info] 概述
> **Skills 是 Agent 的"培训手册"** - 包含指令、脚本和资源的文件夹，教导 Agent 如何完成特定任务。Agent 根据用户意���自动判断何时使用，就像员工有了操作手册，遇到相关任务自动按流程执行。

## 核心概念

### 什么是 Skills

**定义**：包含指令、脚本和资源的**文件夹**，教导 Agent 如何完成特定任务

**发布信息**：
- 发布方：Anthropic
- 发布时间：2025年10月
- 支持��台：Claude.ai、Claude Code、API
- 遵循标准：[Agent Skills 开放标准](https://agentskills.io)

> [!note] 📢 重要更新
> **Slash Commands 已合并到 Skills** - `.claude/commands/` 文件仍然有效，但推荐新开发使用 Skills。当同路径同时存在 Skills 和 Commands 时，Skills 优先。

**为什么需要 Skills**：
- **专业化能力**：为特定领域任务定�� Agent 能力
- **减少重复**：创建一次，跨对话自动使用
- **能力组合**：组合多个 Skills 构建复杂工作流
- **规模化复用**：跨项目和团队共享
- **渐进式加载**：降低 token 消耗

### Skills 的核心特点

| 特点 | 说明 |
|------|------|
| **🔄 自动触发** | Agent 根据用户意图自动判断何时使用 |
| **📦 渐进式加载** | 启动时只加载名称和描述，需要时才加载完整内容 |
| **🔀 跨平台兼容** | Claude.ai、Claude Code、API 都能用 |
| **📁 文件夹结构** | 简单的文件夹组织，易于管理和共享 |

### Skills 类型与位置

| 类型 | 位置 | 范围 | 可共享 | 最佳用途 |
|------|------|------|--------|----------|
| **Enterprise** | 托管设置 | 所有组织用户 | 是 | 组织级标准 |
| **Personal** | `~/.claude/skills/<name>/SKILL.md` | 个人 | 否 | 个人工作流 |
| **Project** | `.claude/skills/<name>/SKILL.md` | 团队 | 是（通过 git） | 团队标准 |
| **Plugin** | `<plugin>/skills/<name>/SKILL.md` | 启用位置 | 取决于插件 | 与插件捆绑 |

**优先级规则**：当同名 Skills 存在于不同位置时，优先级为：**Enterprise > Personal > Project**

> [!info] 📚 来源
> - [GitHub - Agent Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Skills 类型与位置

### 自动发现机制

- **嵌套目录**：编辑子目录文件时，Claude Code 自动发现嵌套的 `.claude/skills/` 目录
- **`--add-dir` 目录**：通过 `--add-dir` 添加的目录中的 Skills 自动加载，支持实时变更检测
- **描述预算**：Skills 描述（第一层元数据）限制为**上下文窗口的 2%**（备选：16,000 字符）。运行 `/context` 检查警告

### Skills 与其他概念的关系

| 概念 | 与 Skills 的关系 |
|------|------------------|
| [[Prompt提示词]] | Skills 本质是高质量的 Prompt 模块 |
| [[Agent智能体]] | Skills 是 Agent 的"内化知识" |
| [[MCP协议]] | Skills 可以调用 MCP 提供的工具 |
| [[SubAgent子代理]] | Skills 共享上下文，SubAgent 独立上下文 |

---

## 技术细节

### Skills 三层架构（渐进式加载）

Skills 采用**渐进式披露（Progressive Disclosure）**架构，按需加载信息：

| 层级 | 内容 | 加载时机 | Token 消耗 |
|------|------|----------|------------|
| **第一层** | Metadata（name + description） | 始终在上下文中 | ~100 tokens |
| **第二层** | SKILL.md 主体指令 | 技能触发后加载 | <5000 tokens |
| **第三层** | scripts/、references/、assets/ | 按需加载 | 实际上无限制 |

```
┌─────────────────────────────────────────────────────────────┐
│                     Skills 加载流程                          │
│                                                              │
│   ┌─────────────────┐                                       │
│   │  会话启动时      │                                       │
│   └────────┬────────┘                                       │
│            ↓                                                 │
│   ┌─────────────────┐                                       │
│   │ 加载所有 Skills │  ← 只加载第一层（name + description）  │
│   │ 的 Metadata     │    Token 消耗：~100 tokens × Skills数 │
│   └────────┬────────┘                                       │
│            │                                                 │
│            ↓ 用户输入触发                                    │
│   ┌─────────────────┐                                       │
│   │ 匹配到相关 Skill │                                       │
│   └────────┬────────┘                                       │
│            ↓                                                 │
│   ┌─────────────────┐                                       │
│   │ 加载 SKILL.md   │  ← 第二层：完整指令                    │
│   │ 完整内容        │    Token 消耗：<5000 tokens            │
│   └────────┬────────┘                                       │
│            │                                                 │
│            ↓ 需要时                                          │
│   ┌─────────────────┐                                       │
│   │ 按需加载脚本    │  ← 第三层：scripts、references         │
│   │ 和参考资源      │    通过 bash 执行，不占用上下文        │
│   └─────────────────┘                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 自动触发机制

Skills 通过 **description** 字段实现智能触发：

1. **启动阶段**：加载所有 Skills 的 name + description
2. **匹配阶段**：Agent 根据用户输入和 description 判断需要哪个 Skill
3. **加载阶段**：读取对应的 SKILL.md 完整内容
4. **执行阶段**：基于完整指令执行任务

**触发示例**：
```markdown
---
name: code-reviewer
description: 专业的代码审查专家。当用户请求代码审查、检查代码质量、review代码时自动触发。
---
```

当用户说"帮我审查这段代码"时，Agent 会自动识别并触发此 Skill。

### Skills 文件结构

```
my-skill/
├── SKILL.md              # 必填：技能说明（包含 YAML 元数据）
├── templates/            # 可选：模板文件
│   └── output-format.md
├── examples/             # 可选：示例输出
│   └── sample-output.md
├── references/           # 可选：领域知识和规范
│   └── api-spec.md
└── scripts/              # 可选：辅助脚本
    ├── example.py
    └── helper.sh
```

> [!tip] 💡 最佳实践
> 保持 `SKILL.md` 在 **500 行以内**。将详细参考材料、大型示例和规范移至单独文件。

### SKILL.md Frontmatter 字段

#### 必填字段

| 字段 | 说明 |
|------|------|
| `name` | 小写字母、数字、连字符（最多 64 字符），不能包含 "anthropic" 或 "claude" |
| `description` | Skill 功能 + 触发时机（最多 1024 字符），**关键**用于自动触发匹配 |

#### 可选字段

| 字段 | 说明 |
|------|------|
| `argument-hint` | `/` 自动补全菜单中显示的提示，如 `"[filename] [format]"` |
| `disable-model-invocation` | `true` = 仅用户可通过 `/name` 调用，Claude 不会自动触发 |
| `user-invocable` | `false` = 从 `/` 菜单隐藏，仅 Claude 可自动调用 |
| `allowed-tools` | 逗号分隔的工具列表，无需权限提示即可使用 |
| `model` | Skill 激活时的模型覆盖（如 `opus`、`sonnet`） |
| `effort` | 努力级别覆盖：`low`、`medium`、`high`、`max` |
| `context` | `fork` = 在隔离的子代理上下文中运行 Skill |
| `agent` | 当 `context: fork` 时的子代理类型（如 `Explore`、`Plan`、`general-purpose`） |
| `shell` | `!`command`` 替换和脚本使用的 Shell：`bash`（默认）或 `powershell` |
| `hooks` | 限定于此 Skill 生命周期的钩子（格式与全局钩子相同） |

> [!info] 📚 来源
> - [GitHub - Agent Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Frontmatter 字段说明

### SKILL.md 标准结构

```markdown
---
name: skill-name
description: 简短描述，用于触发匹配
allowed-tools: Read, Grep, Bash
---

# Skill 标题

## 职责
- 明确说明这个 Skill 负责什么

## 工作流程
1. 第一步做什么
2. 第二步做什么
3. ...

## 输出规范
- 输出格式要求
- 约束条件

## 注意事项
- 特殊情况处理
- 边界条件
```

### Skills 内容类型

Skills 可包含两种类型的内容：

#### 参考内容（Reference Content）
添加 Claude 应用于当前工作的知识——约定、模式、风格指南、领域知识。在对话上下文中内联运行。

```yaml
---
name: api-conventions
description: 此代码库的 API 设计模式
---
编写 API 端点时：
- 使用 RESTful 命名约定
- 返回一致的错误格式
- 包含请求验证
```

#### 任务内容（Task Content）
特定操作的步骤说明。通常直接用 `/skill-name` 调用。

```yaml
---
name: deploy
description: 将应用部署到生产环境
context: fork
disable-model-invocation: true
---
部署应用程序：
1. 运行测试套件
2. 构建应用程序
3. 推送到部署目标
```

### 调用控制

默认情况下，你和 Claude 都可以调用任何 Skill。两个字段控制三种调用模式：

| Frontmatter | 你可以调用 | Claude 可以调用 |
|-------------|-----------|----------------|
| （默认） | 是 | 是 |
| `disable-model-invocation: true` | 是 | 否 |
| `user-invocable: false` | 否 | 是 |

**使用场景**：
- `disable-model-invocation: true` - 用于有副效应的工作流：`/commit`、`/deploy`、`/send-slack-message`
- `user-invocable: false` - 用于背景知识，不是可执行命令：`legacy-system-context`

### 字符串替换

Skills 支持在内容到达 Claude 之前解析的动态值：

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 调用 Skill 时传递的所有参数 |
| `$ARGUMENTS[N]` 或 `$N` | 按索引访问特定参数（0 起始） |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_SKILL_DIR}` | 包含 Skill 的 SKILL.md 文件的目录 |
| `` !`command` `` | 动态上下文注入 — 运行 shell 命令并内联输出 |

**示例**：
```yaml
---
name: fix-issue
description: 修复 GitHub issue
---
修复 GitHub issue $ARGUMENTS，遵循我们的编码标准。
1. 读取 issue 描述
2. 实现修复
3. 编写测试
4. 创建提交
```

运行 `/fix-issue 123` 会将 `$ARGUMENTS` 替换为 `123`。

### 动态上下文注入

`` `!command` `` 语法在 Skill 内容发送给 Claude 之前运行 shell 命令：

```yaml
---
name: pr-summary
description: 总结 PR 中的更改
context: fork
agent: Explore
---
## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
## Your task
总结此 pull request...
```

命令立即执行；Claude 只看到最终输出。默认使用 `bash`，设置 `shell: powershell` 使用 PowerShell。

### 在子代理中运行 Skills

添加 `context: fork` 在隔离的子代理上下文中运行 Skill。Skill 内容成为专用子代理的任务，拥有独立的上下文窗口。

`agent` 字段指定使用的代理类型：

| 代理类型 | 最佳用途 |
|----------|----------|
| `Explore` | 只读研究、代码库分析 |
| `Plan` | 创建实现计划 |
| `general-purpose` | 需要所有工具的广泛任务 |
| 自定义代理 | 配置中定义的专用代理 |

---

## 内置 Skills

Claude Code 内置了多个开箱即用的 Skills：

| Skill | 说明 |
|-------|------|
| `/simplify` | 审查更改文件的重用性、质量和效率；生成 3 个并行审查代理 |
| `/batch <prompt>` | 使用 git worktrees 在代码库中进行大规模并行更改编排 |
| `/debug [description]` | 通过读取调试日志排查当前会话 |
| `/loop [interval] <prompt>` | 按间隔重复运行提示（如 `/loop 5m check the deploy`） |
| `/claude-api` | 加载 Claude API/SDK 参考；在 `anthropic`/`@anthropic-ai/sdk` 导入时自动激活 |

> [!info] 📚 来源
> - [GitHub - Agent Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Bundled Skills

---

## SKILL.md 完整示例

### 示例 1：代码审查 Skill

```yaml
---
name: code-reviewer
description: 专业的代码审查专家。当用户请求代码审查、检查代码质量、review代码时自动触发。
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## 职责
- 检查代码是否符合规范
- 查找潜在 bug 和安全漏洞
- 提供优化建议

## 审查维度
1. **代码规范**：命名、格式、注释
2. **潜在问题**：空指针、边界条件、类型错误
3. **安全漏洞**：SQL注入、XSS、敏感信息泄露
4. **性能问题**：循环优化、内存使用、算法复杂度

## 工作流程
1. 读取目标文件
2. 使用 Grep 分析代码结构
3. 逐项检查各维度问题
4. 输出审查报告

## 输出格式

### Critical（必须修复）
- [问题描述] 位置：文件:行号
  - 问题原因
  - 修复建议

### Warning（建议改进）
- [问题描述] 位置：文件:行号
  - 改进建议

### Suggestion（可选优化）
- [优化建议]

## 注意事项
- 关注业务逻辑正确性
- 考虑代码可维护性
- 提供具体的修复代码示例
```

### 示例 2：部署 Skill（仅用户调用）

```yaml
---
name: deploy
description: 将应用部署到生产环境
disable-model-invocation: true
allowed-tools: Bash(npm *), Bash(git *)
---
部署 $ARGUMENTS 到生产环境：
1. 运行测试套件：`npm test`
2. 构建应用程序：`npm run build`
3. 推送到部署目标
4. 验证部署成功
5. 报告部署状态
```

### 示例 3：品牌语调 Skill（背景知识）

```yaml
---
name: brand-voice
description: 确保所有沟通符合品牌语调和风格指南。创建营销文案、客户沟通或公开内容时使用。
user-invocable: false
---
## 语调
- **友好但专业** - 亲切但不随意
- **清晰简洁** - 避免行话
- **自信** - 我们知道自己在做什么
- **同理心** - 理解用户需求

## 写作指南
- 使用"你"称呼读者
- 使用主动语态
- 句子保持在 20 词以内
- 以价值主张开头
```

---

## Skills vs 其他功能

| 功能 | 调用方式 | 最佳用途 |
|------|----------|----------|
| **Skills** | 自动或 `/name` | 可复用的专业知识、工作流 |
| **Slash Commands** | 用户发起 `/name` | 快速快捷方式（已合并到 Skills） |
| **Subagents** | 自动委派 | 隔离任务执行 |
| **Memory (CLAUDE.md)** | 始终加载 | 持久的项目上下文 |
| **MCP** | 实时 | 外部数据/服务访问 |
| **Hooks** | 事件驱动 | 自动化副效应 |

---

## Skills vs SubAgent 对比

| 维度 | Skills | SubAgent |
|------|--------|----------|
| **上下文** | 共享主上下文 | **完全独立**的上下文空间 |
| **本质** | 知识注入（内化能力） | 任务外包（独立执行） |
| **触发方式** | 自动/命令触发 | Agent 决策派发 |
| **适合任务** | 轻量任务、需要专业指导 | 复杂任务、需要上下文隔离 |
| **Token 成本** | 低（渐进式加载） | 较高（独立上下文开销） |
| **执行方式** | 在主推理流程中 | 独立推理循环 |

**选择指南**：

| 场景 | 推荐 | 原因 |
|------|------|------|
| 自动格式化、命名检查 | ✅ Skills | 轻量任务，不需要隔离 |
| 代码审查（简单） | ✅ Skills | 需要专业知识指导 |
| 代码审查（复杂项目） | ✅ SubAgent | 需要上下文隔离 |
| 大规模重构 | ✅ SubAgent | 需要独立上下文 |
| 并行处理多个复杂任务 | ✅ 多个 SubAgent | 需要并行执行 |
| 快速共享能力给团队 | ✅ Skills 打包 | 易于分发 |

---

## 最佳实践

### 编写高质量 Skills

1. **清晰的 description**：让 Agent 能准确判断何时触发
2. **明确的工作流程**：步骤清晰，易于执行
3. **具体的输出格式**：定义期望的输出结构
4. **合理的约束**：设置 allowed-tools 限制

### Description 编写指南

- ❌ **模糊**："帮助处理文档"
- ✅ **具体**："从 PDF 文件提取文本和表格、填写表单、合并文档。处理 PDF 文件或用户提及 PDF、表单、文档提取时使用。"

### 命名规范

- ✅ `code-reviewer` - 清晰描述功能
- ✅ `sql-generator` - 明确用途
- ✅ `api-documenter` - 语义明确
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义
- ❌ `test` - 不够具体

### Do's 和 Don'ts

**应该做**：
- 使用清晰、描述性的名称
- 包含全面的指令
- 添加具体示例
- 打包相关脚本和模板
- 用真实场景测试
- 文档化依赖

**不应该做**：
- 为一次性任务创建 Skills
- 复制现有功能
- 让 Skills 太宽泛
- 跳过 description 字段
- 未经审计安装来自不可信来源的 Skills

---

## 常见问题

### Q: Skills 和 MCP 有什么区别？

A: Skills 是**知识层**（教 Agent 怎么做），MCP 是**工具层**（提供可调用的函数）。Skills 可以调用 MCP 工具，但 Skills 的核心是专业知识指导。

### Q: 什么时候应该创建 Skill？

A: 当你发现某个操作需要经常重复执行，且需要专业知识指导时。比如：
- 代码审查（需要审查标准知识）
- 文档生成（需要格式规范）
- 特定领域的任务（需要专业知识）

### Q: description 为什么很重要？

A: description 是 Skills 的"简历"，让 Agent 快速了解 Skill 能力。好的 description 能确保正确触发，避免加载不必要的 SKILL.md 内容。

### Q: 一个 Skill 可以调用另一个 Skill 吗？

A: 可以。Skills 可以在 SKILL.md 中指导 Agent 使用其他 Skills，实现复杂的工作流组合。

### Q: 如何调试 Skill？

A:
1. 检查 SKILL.md 的 YAML 格式是否正确
2. 确认 description 描述是否明确
3. 在 Claude Code 中测试触发
4. 根据输出质量优化 SKILL.md

---

## 故障排除

### 快速参考

| 问题 | 解决方案 |
|------|----------|
| Claude 不使用 Skill | 让 description 更具体，添加触发关键词 |
| Skill 文件未找到 | 验证路径：`~/.claude/skills/name/SKILL.md` |
| YAML 错误 | 检查 `---` 标记、缩进、无制表符 |
| Skills 冲突 | 在 descriptions 中使用不同的触发词 |
| 脚本不运行 | 检查权限：`chmod +x scripts/*.py` |
| Claude 看不到所有 Skills | Skills 太多；运行 `/context` 检查警告 |

### Skill 不触发

如果 Claude 在预期时不使用你的 Skill：
1. 检查 description 是否包含用户自然会说出的关键词
2. 验证询问"What skills are available?"时 Skill 是否出现
3. 尝试重新表述请求以匹配 description
4. 使用 `/skill-name` 直接调用来测试

### Skill 触发太频繁

如果 Claude 在你不想要时使用你的 Skill：
1. 让 description 更具体
2. 添加 `disable-model-invocation: true` 仅限手动调用

### Claude 看不到所有 Skills

Skill descriptions 限制为**上下文窗口的 2%**（备选：**16,000 字符**）。运行 `/context` 检查被排除 Skills 的警告。使用 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖预算。

---

## 安全考虑

**仅使用来自可信来源的 Skills。** Skills 通过指令和代码为 Claude 提供能力——恶意 Skill 可以指导 Claude 以有害方式调用工具或执行代码。

**关键安全考虑**：
- **彻底审计**：审查 Skill 目录中的所有文件
- **外部来源有风险**：从外部 URL 获取的 Skills 可能被篡改
- **工具滥用**：恶意 Skills 可能以有害方式调用工具
- **像安装软件一样对待**：仅使用来自可信来源的 Skills

---

## 相关文档

### 核心概念
- [[01-基础概念/人工智能重要的六大概念体系]] - 六大概念总览
- [[01-基础概念/Prompt提示词]] - Skills 本质是高质量的 Prompt 模块
- [[01-基础概念/Agent智能体]] - Skills 是 Agent 的"内化知识"
- [[01-基础概念/MCP协议]] - Skills 可以调用 MCP 提供的工具
- [[01-基础概念/SubAgent子代理]] - Skills 共享上下文，SubAgent 独立上下文
- [[01-基础概念/Agent Teams智能体团队]] - Skills 可以给 Agent Teams 成员使用

### 实践指南
- [[03-进阶应用/如何编写Skills]] - Skills 编写实战

---

## 参考资料

### 官方资源
- [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills) - 完整技术文档
- [Agent Skills 架构博客](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) - 官方博客
- [Agent Skills 开放标准](https://agentskills.io) - 跨 AI 工具标准

### 社区资源
- [GitHub - claude-howto Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - 详细指南和示例
- [GitHub - Skills 仓库](https://github.com/luongnv89/skills) - 可直接使用的 Skills 集合
