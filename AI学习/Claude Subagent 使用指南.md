---
tags: [ai]
---

# Subagent 使用指南

> [!info] 概述
> **Subagent 是 AI 专家助手**，每个专注于特定领域，在独立上下文中运行。就像雇佣不同的专家：代码审查专家、探索专家、规划专家，各司其职，提高效率。

## 核心概念 💡

### 什么是 Subagent

**是什么**：在独立上下文中运行的 AI 代理，专注处理特定任务

**为什么需要**：
- 独立运行不污染主会话 token
- 多轮对话自主迭代优化
- 多个 subagent 可并行运行
- 返回最终结果而非中间过程

**与其他概念关系**：Subagent 是 Task 工具的具体实现，通过插件系统扩展

### 内置 Subagent 类型

| 类型 | 工具 | 用途 | 比喻 |
|------|------|------|------|
| **Bash** | Bash | 命令执行、git、npm | 运维人员 |
| **General Purpose** | 全部 | 复杂研究、多步骤任务 | 全能顾问 |
| **Explore** | 除 Task/Edit/Write | 代码库快速探索 | 侦探 |
| **Plan** | 除 Task/Edit/Write | 架构规划、设计方案 | 架构师 |
| **Claude Code Guide** | 搜索工具 | Claude Code 问题解答 | 技术支持 |

## 操作步骤

### 模式 1：让 Claude 自主探索

```bash
你: 这个项目的路由是怎么配置的？

Claude: (启动 Explore subagent)
    - 搜索路由相关文件
    - 读取配置文件
    - 分析路由规则
    - 返回结果给你
```

### 模式 2：并行搜索多个话题

```bash
你: 我需要同时了解：
    1. 错误处理机制
    2. 认证流程
    3. 数据库配置

Claude: (启动三个并行 subagent)
    - 同时搜索三个话题
    - 汇总结果返回
```

### 使用自定义 Agent

```bash
# 用代码审查 agent 审查代码
"用 code-reviewer agent 审查 src/auth.js"
```

## 注意事项 ⚠️

### 常见错误

**Subagent 不启动**：
- ❌ 任务太简单（直接用工具更快）
- ❌ 触发条件不明确
- ❌ 没有对应的 agent

**输出不符合预期**：
- ❌ agent 描述不清
- ❌ 约束条件不够
- ❌ 缺少具体示例

**自定义 Agent 不工作**：
- ❌ frontmatter 格式错误
- ❌ 插件未正确加载
- ❌ 文件路径不对

### 关键配置点

**Agent 文件格式**：
```markdown
---
name: code-reviewer
description: Use when user asks to "review code"
model: inherit
color: blue
tools: ["Read", "Grep"]
---

你是一个资深的代码审查专家...
```

**命名规范**：
- ✅ `code-reviewer` - kebab-case
- ✅ `test-generator` - 清晰描述
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义

**模型选择**：
```yaml
# 简单任务
model: haiku

# 标准任务
model: inherit   # 或 sonnet

# 复杂推理
model: sonnet

# 最高质量
model: opus
```

**工具权限原则**：
- 只给必要的工具
- 遵循最小权限原则
```yaml
# ❌ 不推荐
tools: ["*"]

# ✅ 推荐
tools: ["Read", "Grep"]
```

## 常见问题 ❓

**Q: 为什么有时候 Claude 不使用 subagent？**

A: Subagent 启动有成本。对于简单操作（如读取一个文件），Claude 会直接使用专用工具更快。

**Q: 如何创建自定义 subagent？**

A: 需要通过插件（Plugin）系统实现：
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── agents/
    └── my-agent.md
```

**Q: Explore 和 General Purpose 有什么区别？**

A:
- **Explore**：快速探索代码库，工具受限（不能编辑）
- **General Purpose**：复杂研究任务，拥有全部工具

**Q: 如何测试我创建的 agent？**

A:
```bash
# 带插件启动
claude --plugin-dir /path/to/my-plugin

# 测试触发
"用 code-reviewer agent 审查这段代码"
```

**Q: plugin-dev 插件是什么？**

A: 官方提供的插件开发工具包，包含 `agent-creator` agent，可以帮你快速生成高质量的 agent 配置。

---

## 从零创建自定义 Agent 🚀

> [!tip] 学习路径
> 创建自定义 Agent → 理解 Plugin 系统 → 调试优化 → 高级使用

### 创建前的准备

**了解 Plugin 系统架构**

```
Plugin（插件）
├── 元数据配置 (plugin.json)
├── Agent 定义 (.md 文件)
└── 资源文件 (可选)
    ↓
Claude Code 加载
├── 解析 plugin.json
├── 注册 Agent
└── 提供触发匹配
```

**确定 Agent 的用途和边界**

在创建之前，问自己：
- 这个 Agent 解决什么具体问题？
- 它需要访问哪些工具？
- 触发条件是什么？
- 输出格式应该是什么样的？

**选择合适的模型和工具权限**

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 简单格式转换 | `haiku` | 快速响应，成本低 |
| 代码分析/审查 | `sonnet` 或 `inherit` | 平衡速度和质量 |
| 复杂架构设计 | `opus` | 最高推理质量 |

### 完整创建步骤

#### 步骤 1：创建 Plugin 目录结构

```bash
# 在合适的位置创建插件目录
mkdir -p my-custom-plugin/.claude-plugin
mkdir -p my-custom-plugin/agents
cd my-custom-plugin
```

**完整目录结构**：
```
my-custom-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin 元数据（必需）
├── agents/
│   ├── code-reviewer.md     # Agent 定义文件
│   ├── test-generator.md    # 另一个 Agent
│   └── doc-writer.md        # 第三个 Agent
└── assets/                  # 可选的资源文件
    ├── templates/
    └── examples/
```

#### 步骤 2：编写 plugin.json 配置

**完整示例**：
```json
{
  "name": "my-custom-plugin",
  "version": "1.0.0",
  "description": "自定义代码审查和测试生成工具集",
  "author": "Your Name <your.email@example.com>",
  "agents": ["code-reviewer", "test-generator", "doc-writer"],
  "keywords": ["code-review", "testing", "documentation"],
  "homepage": "https://github.com/yourname/my-custom-plugin",
  "claude": {
    "minVersion": "1.0.0"
  }
}
```

**字段说明**：
- `name`: 插件唯一标识符，使用 kebab-case
- `version`: 语义化版本号
- `agents`: 列出所有 agent 定义文件（不含 .md 扩展名）
- `keywords`: 帮助用户搜索和发现你的插件

#### 步骤 3：编写 Agent 定义文件

**完整的 Agent 定义结构**：

```markdown
---
name: code-reviewer
description: Use when user asks to "review code", "检查代码", "代码审查", "code review", "审阅"
model: sonnet
color: blue
tools: ["Read", "Grep", "Glob", "Bash"]
---

# Code Reviewer Agent

你是一位资深的代码审查专家，专注于发现代码中的潜在问题并提供改进建议。

## 核心能力
- 识别代码异味和反模式
- 发现潜在的安全漏洞
- 提出性能优化建议
- 确保代码可维护性

## 工作流程

1. **理解上下文**
   - 读取相关文件
   - 了解项目结构
   - 理解代码目的

2. **全面检查**
   - 代码质量（命名、结构、复杂度）
   - 安全性（注入漏洞、敏感信息）
   - 性能（算法效率、资源使用）
   - 可维护性（注释、文档、测试）

3. **输出结果**
   - 按严重程度分类问题
   - 提供具体修复建议
   - 包含代码示例

## 输出格式

使用以下格式输出审查结果：

### 🚨 严重问题
- [问题描述]
  - 位置：`file:line`
  - 原因：[原因说明]
  - 修复：[具体建议]

### ⚠️ 警告
- [问题描述]
  - 位置：`file:line`
  - 建议：[改进建议]

### 💡 优化建议
- [改进点]
  - 位置：`file:line`
  - 当前：[当前代码]
  - 建议：[优化方案]

## 审查原则
- 先理解，再评判
- 提供建设性反馈
- 解释"为什么"而不只是"是什么"
- 考虑项目实际情况
```

**Frontmatter 字段详解**：

| 字段 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `name` | ✅ | Agent 唯一标识 | `code-reviewer` |
| `description` | ✅ | 触发描述，支持多语言 | `Use when user asks to "review code", "检查代码"` |
| `model` | ❌ | 使用的模型 | `sonnet`, `haiku`, `opus`, `inherit` |
| `color` | ❌ | UI 显示颜色 | `blue`, `green`, `red`, `yellow`, `purple` |
| `tools` | ❌ | 允许使用的工具列表 | `["Read", "Grep", "Glob"]` |

#### 步骤 4：测试和调试

**启动测试**：
```bash
# 方式1：命令行参数
claude --plugin-dir /path/to/my-custom-plugin

# 方式2：配置文件（推荐）
# 在 ~/.claude/config.json 中添加：
{
  "pluginDir": "/path/to/my-custom-plugin"
}
```

**验证步骤**：

1. **检查 Agent 是否加载**
```bash
# 在 Claude Code 中执行
/agents                    # 列出所有可用的 agents
# 应该看到 code-reviewer, test-generator 等
```

2. **测试触发条件**
```bash
# 直接描述触发
"用 code-reviewer 审查 src/auth.js"

# 自然语言触发（如果 description 配置正确）
"请检查一下这段代码有什么问题"
"帮我审阅这个文件"
```

3. **检查输出**
- Agent 是否正确启动？
- 是否能访问配置的工具？
- 输出格式是否符合预期？

**调试技巧**：

```bash
# 查看详细日志
claude --plugin-dir /path/to/plugin --log-level debug

# 检查 frontmatter 语法
cat agents/code-reviewer.md | head -10

# 验证 JSON 格式
cat .claude-plugin/plugin.json | jq .
```

**常见问题排查**：

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Agent 未出现在列表 | plugin.json 路径错误 | 检查 `.claude-plugin` 目录位置 |
| 无法触发 | description 不匹配 | 确保包含用户常用的表达方式 |
| 工具报错 | tools 权限不足 | 添加所需工具到 frontmatter |
| 输出不符合预期 | 指令不够清晰 | 在 Agent 内容中添加更具体的约束 |

#### 步骤 5：优化和迭代

**性能优化**：
```yaml
# 简单任务使用 haiku
model: haiku

# 限制工具范围减少开销
tools: ["Read"]  # 只给需要的工具
```

**触发优化**：
```yaml
# 添加更多触发短语
description: |
  Use when user asks to "review code", "检查代码", "代码审查",
  "code review", "审阅", "审查代码", "code check", "检查质量"
```

**输出优化**：
```markdown
## 输出要求
- 简洁明了，不超过 200 字
- 使用 emoji 增强可读性
- 关键信息高亮显示
- 提供可执行的命令
```

### 实战示例

#### 示例 1：代码审查 Agent

```markdown
---
name: security-auditor
description: Use when user asks to "security check", "安全检查", "漏洞扫描", "安全审计"
model: sonnet
color: red
tools: ["Read", "Grep", "Glob"]
---

# Security Auditor Agent

你是安全审计专家，专注于发现代码中的安全漏洞。

## 检查清单
- [ ] SQL 注入风险
- [ ] XSS 漏洞
- [ ] 硬编码密钥
- [ ] 不安全的随机数
- [ ] 认证缺陷
- [ ] 授权问题

## 输出格式
```
🔒 安全审计报告

### 高危漏洞
[详细描述]

### 中危问题
[详细描述]

### 修复建议
[具体方案]
```
```

#### 示例 2：文档生成 Agent

```markdown
---
name: doc-generator
description: Use when user asks to "generate docs", "生成文档", "写注释", "document code"
model: inherit
color: green
tools: ["Read", "Glob", "Grep"]
---

# Documentation Generator

你擅长为代码生成清晰的文档。

## 工作原则
1. 保持简洁，避免废话
2. 关注"为什么"而非"是什么"
3. 使用示例说明用法
4. 保持与现有文档风格一致

## 输出格式
```markdown
### [函数/类名]

**用途**：[一句话说明]

**参数**：
- `param1`: [说明]
- `param2`: [说明]

**返回**：[说明]

**示例**：
\`\`\`typescript
// 代码示例
\`\`\`
```
```

#### 示例 3：测试生成 Agent

```markdown
---
name: test-generator
description: Use when user asks to "generate tests", "生成测试", "写测试用例", "create tests"
model: sonnet
color: yellow
tools: ["Read", "Grep", "Glob"]
---

# Test Generator Agent

你专注于生成全面且可维护的测试用例。

## 测试原则
- Arrange-Act-Assert 模式
- 每个测试只验证一件事
- 使用描述性测试名称
- Mock 外部依赖

## 输出格式
\`\`\`typescript
describe('[功能名称]', () => {
  describe('[正常流程]', () => {
    it('应该 [期望结果]', () => {
      // Arrange
      // Act
      // Assert
    });
  });

  describe('[边界情况]', () => {
    it('应该处理 [特殊情况]', () => {
      // 测试代码
    });
  });

  describe('[错误处理]', () => {
    it('应该抛出 [错误类型] 当 [条件]', () => {
      // 测试代码
    });
  });
});
\`\`\`
```

---

## 高级使用技巧 🎯

### 场景 1：并行探索

当你需要同时了解多个不相关的概念时，可以并行启动多个 Explore agent：

```bash
# 你可以这样问
"我需要同时了解：1. 错误处理机制 2. 认证流程 3. 数据库配置"

# Claude 会启动三个并行的 Explore agent
# 每个独立探索一个主题
# 最后汇总结果给你
```

**最佳实践**：
- 确保任务之间真正独立
- 限制并行数量（建议 2-4 个）
- 提供明确的探索范围

### 场景 2：复杂任务分解

当任务涉及多个步骤时，使用 Plan agent 先设计方案：

```bash
"我需要重构认证模块，但不确定从哪里开始"

# Claude 启动 Plan agent
# 1. 分析现有代码
# 2. 识别重构点
# 3. 制定分步计划
# 4. 提出验证方法
```

**使用 Plan agent 的时机**：
- 架构调整
- 大规模重构
- 功能模块新增
- 性能优化方案

### 场景 3：自主研究

当问题需要深入代码库探索时，让 Explore agent 自主工作：

```bash
"这个项目是如何处理国际化的？"

# Explore agent 会：
# - 搜索 i18n 相关代码
# - 找到配置文件
# - 理解实现机制
# - 返回完整的分析
```

**设置探索深度**：
```bash
# 快速概览
"简单介绍一下 [主题]"

# 深入分析
"详细分析 [主题] 的实现，包括配置、使用、边界情况"
```

### 场景 4：使用自定义 Agent

**启动方式**：

1. **通过 --plugin-dir 参数**（临时）
```bash
claude --plugin-dir /path/to/my-plugin
```

2. **通过配置文件设置**（永久）
```json
// ~/.claude/config.json
{
  "pluginDir": "/path/to/my-plugin"
}
```

3. **验证 Agent 是否加载**
```bash
/agents  # 查看所有可用 agents
```

**触发方式**：

1. **直接描述**
```bash
"用 code-reviewer 审查这段代码"
"使用 security-auditor 检查安全问题"
```

2. **自然触发**（推荐）
```bash
# 如果 description 配置得当，这些都能触发：
"请检查代码质量"
"帮我看看有没有安全问题"
"生成一些测试用例"
```

3. **显式指定**
```bash
# 当有多个 agent 可能匹配时
"请用 doc-generator agent 为这个函数生成文档"
```

**组合使用**：
```bash
# 先用 Explore 了解代码
"探索一下认证模块的实现"

# 再用 custom agent 处理
"用 code-reviewer 审查 src/auth/login.js"
```

### 性能优化建议

| 场景 | 推荐配置 | 说明 |
|------|----------|------|
| 快速格式化 | `model: haiku` | 简单任务用轻量模型 |
| 代码审查 | `model: sonnet` | 平衡质量和速度 |
| 架构设计 | `model: opus` | 复杂推理用最强模型 |
| 文本搜索 | 限制 tools | 只给必要的工具 |

---

## 相关文档
[[Prompt, Agent, MCP 是什么]] | [[Claude Code 常用功能]] | [[Claude MCP 使用指南]] | [[Subagent 实战练习]]
