---
tags: [ai]
---

# Claude Subagent 使用指南

> [!info] 概述
> **Subagent 是 AI 专家助手**，每个专注于特定领域，在独立上下文中运行。就像雇佣不同的专家：代码审查专家、探索专家、规划专家，各司其职，提高效率。

---

# 📖 第一部分：快速入门

## 什么是 Subagent

### 核心概念

**定义**：在独立上下文中运行的 AI 代理，专注处理特定任务。

**为什么需要**：
- 独立运行，不污染主会话的 token
- 多轮对话，自主迭代优化
- 多个 subagent 可并行运行
- 返回最终结果，而非中间过程

**工作原理**：Subagent 是 Task 工具的具体实现，通过插件（Plugin）系统扩展。

### 内置 Subagent 类型

| 类型 | 工具权限 | 用途 | 比喻 |
|------|----------|------|------|
| **Bash** | Bash | 命令执行、git、npm | 运维人员 |
| **General Purpose** | 全部工具 | 复杂研究、多步骤任务 | 全能顾问 |
| **Explore** | 除 Task/Edit/Write | 代码库快速探索 | 侦探 |
| **Plan** | 除 Task/Edit/Write | 架构规划、设计方案 | 架构师 |
| **Claude Code Guide** | 搜索工具 | Claude Code 问题解答 | 技术支持 |

## 基础使用方法

### 场景 1：自主探索代码库

当你想了解项目的某个方面时，让 Explore agent 自主工作：

```bash
# 提问示例
"这个项目的路由是怎么配置的？"
"项目是如何处理国际化的？"

# Explore agent 会：
# - 搜索相关文件
# - 读取配置文件
# - 分析实现逻辑
# - 返回完整的分析结果
```

### 场景 2：并行探索多个主题

当需要同时了解多个不相关的话题时：

```bash
# 提问示例
"我需要同时了解：
    1. 错误处理机制
    2. 认证流程
    3. 数据库配置"

# Claude 会启动三个并行的 Explore agent
# 每个独立探索一个主题，最后汇总结果
```

**最佳实践**：
- 确保任务之间真正独立
- 限制并行数量（建议 2-4 个）
- 提供明确的探索范围

### 场景 3：复杂任务规划

当任务涉及多个步骤，不确定如何开始时：

```bash
# 提问示例
"我需要重构认证模块，但不确定从哪里开始"

# Plan agent 会：
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

### 场景 4：使用自定义 Agent

如果你已经创建了自定义 Agent：

```bash
# 直接指定 agent 名称
"用 code-reviewer 审查 src/auth.js"
"用 security-scanner 检查安全问题"
```

## 新手常见问题

**Q: 为什么有时候 Claude 不使用 subagent？**

A: Subagent 启动有成本。对于简单操作（如读取一个文件），Claude 会直接使用专用工具更快。

**Q: Explore 和 General Purpose 有什么区别？**

| 对比项 | Explore | General Purpose |
|--------|---------|-----------------|
| 用途 | 快速探索代码库 | 复杂研究任务 |
| 工具权限 | 受限（不能编辑） | 全部工具 |
| 典型场景 | 了解项目结构 | 多步骤综合任务 |

**Q: 如何测试我创建的 agent？**

```bash
# 带插件启动
claude --plugin-dir /path/to/my-plugin

# 测试触发
"用 code-reviewer 审查这段代码"
```

**Q: plugin-dev 插件是什么？**

A: 官方提供的插件开发工具包，包含 `agent-creator` agent，可以帮你快速生成高质量的 agent 配置。

**Q: 为什么 subagent 没有启动？**

可能原因：
- ❌ 任务太简单（直接用工具更快）
- ❌ 触发条件不明确
- ❌ 没有对应的 agent

---

# 🚀 第二部分：创建自定义 Agent

## Plugin 系统架构

```
Plugin（插件）
├── 元数据配置 (plugin.json)     # 插件信息、Agent 列表
├── Agent 定义 (.md 文件)        # 每个 Agent 的配置和指令
└── 资源文件 (可选)              # 模板、示例等
        ↓
Claude Code 加载流程
├── 解析 plugin.json
├── 注册所有 Agent
└── 提供触发匹配
```

### 创建前的思考

在创建之前，问自己：
- 这个 Agent 解决什么具体问题？
- 它需要访问哪些工具？
- 触发条件是什么？
- 输出格式应该是什么样的？

### 模型选择指南

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 简单格式转换 | `haiku` | 快速响应，成本低 |
| 代码分析/审查 | `sonnet` 或 `inherit` | 平衡速度和质量 |
| 复杂架构设计 | `opus` | 最高推理质量 |

## 完整创建步骤

### 步骤 1：创建 Plugin 目录结构

```bash
# 创建插件目录
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
│   └── test-generator.md    # 另一个 Agent
└── assets/                  # 可选的资源文件
    ├── templates/
    └── examples/
```

### 步骤 2：编写 plugin.json 配置

```json
{
  "name": "my-custom-plugin",
  "version": "1.0.0",
  "description": "自定义代码审查和测试生成工具集",
  "author": "Your Name <your.email@example.com>",
  "agents": ["code-reviewer", "test-generator"],
  "keywords": ["code-review", "testing", "documentation"],
  "homepage": "https://github.com/yourname/my-custom-plugin",
  "claude": {
    "minVersion": "1.0.0"
  }
}
```

**字段说明**：
| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 插件唯一标识符，使用 kebab-case |
| `version` | ✅ | 语义化版本号 |
| `agents` | ✅ | 列出所有 agent 名称（不含 .md 扩展名） |
| `keywords` | ❌ | 帮助用户搜索和发现插件 |

### 步骤 3：编写 Agent 定义文件

**完整的 Agent 定义结构**：

```markdown
---
name: code-reviewer
description: Use when user asks to "review code", "检查代码", "代码审查", "code review"
model: sonnet
color: blue
tools: ["Read", "Grep", "Glob", "Bash"]
---

# Code Reviewer Agent

你是一位资深的代码审查专家...

## 工作流程
1. 理解代码上下文
2. 检查代码质量
3. 识别潜在问题
4. 提供改进建议

## 输出格式
（定义输出的具体格式）
```

**Frontmatter 字段详解**：

| 字段 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `name` | ✅ | Agent 唯一标识 | `code-reviewer` |
| `description` | ✅ | 触发描述，支持多语言 | `"检查代码", "review code"` |
| `model` | ❌ | 使用的模型 | `sonnet`, `haiku`, `opus`, `inherit` |
| `color` | ❌ | UI 显示颜色 | `blue`, `green`, `red`, `yellow` |
| `tools` | ❌ | 允许使用的工具列表 | `["Read", "Grep", "Glob"]` |

**命名规范**：
- ✅ `code-reviewer` - kebab-case，清晰描述
- ✅ `test-generator` - 明确功能
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义

**工具权限原则**：
```yaml
# ❌ 不推荐：给所有权限
tools: ["*"]

# ✅ 推荐：最小权限原则
tools: ["Read", "Grep"]
```

### 步骤 4：测试和调试

**启动测试**：
```bash
# 方式1：命令行参数（临时）
claude --plugin-dir /path/to/my-custom-plugin

# 方式2：配置文件（永久）
# 在 ~/.claude/config.json 中添加：
{
  "pluginDir": "/path/to/my-custom-plugin"
}
```

**验证步骤**：

1. **检查 Agent 是否加载**
```bash
/agents  # 列出所有可用的 agents
```

2. **测试触发条件**
```bash
# 直接描述触发
"用 code-reviewer 审查 src/auth.js"

# 自然语言触发
"请检查一下这段代码有什么问题"
```

3. **检查输出质量**
- Agent 是否正确启动？
- 是否能访问配置的工具？
- 输出格式是否符合预期？

**调试技巧**：
```bash
# 查看详细日志
claude --plugin-dir /path/to/plugin --log-level debug

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

### 步骤 5：优化和迭代

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
  "code review", "审阅", "审查代码", "code check"
```

**输出优化**：
```markdown
## 输出要求
- 简洁明了，不超过 200 字
- 使用 emoji 增强可读性
- 关键信息高亮显示
- 提供可执行的命令
```

## 实战示例

### 示例 1：代码审查 Agent

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

### 🔴 高危漏洞
[详细描述]

### 🟡 中危问题
[详细描述]

### 修复建议
[具体方案]
```

### 示例 2：文档生成 Agent

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

### [函数/类名]

**用途**：[一句话说明]

**参数**：
- `param1`: [说明]
- `param2`: [说明]

**返回**：[说明]

**示例**：
```typescript
// 代码示例
```
```

### 示例 3：测试生成 Agent

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

## 输出模板

```typescript
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
```
```

---

# 🎯 第三部分：高级使用与最佳实践

## 高级使用场景

### 场景 1：设置探索深度

根据需要调整 Explore agent 的分析深度：

```bash
# 快速概览
"简单介绍一下 [主题]"

# 深入分析
"详细分析 [主题] 的实现，包括配置、使用、边界情况"
```

### 场景 2：组合使用多个 Agent

先了解，再处理：

```bash
# 步骤1：用 Explore 了解代码结构
"探索一下认证模块的实现"

# 步骤2：用 custom agent 处理
"用 code-reviewer 审查 src/auth/login.js"
```

### 场景 3：自定义 Agent 触发技巧

**三种触发方式**：

1. **直接指定**
```bash
"用 code-reviewer 审查这段代码"
```

2. **自然触发**（推荐，需要 description 配置得当）
```bash
"请检查代码质量"
"帮我看看有没有安全问题"
```

3. **显式指定**（当多个 agent 可能匹配时）
```bash
"请用 doc-generator agent 为这个函数生成文档"
```

## Plugin 组织策略

根据你的使用场景选择合适的组织方式。

### 策略 A：全局通用插件（推荐）

将通用工具放在全局目录，所有项目共享。

**目录结构**：
```bash
~/.claude/plugins/
├── code-review/          # 通用代码审查工具
├── documentation/        # 文档生成工具
└── testing/              # 测试辅助工具
```

**配置方式**：
```bash
# ~/.claude/config.json
{
  "pluginDir": "~/.claude/plugins"
}
```

**适用场景**：
- 跨项目通用的工具
- 个人开发助手
- 团队共享的标准工具

### 策略 B：项目特定插件

为特定项目创建专属插件。

**目录结构**：
```bash
my-project/
├── .claude-plugins/
│   └── project-specific/
│       ├── .claude-plugin/
│       └── agents/
├── src/
└── package.json
```

**启动方式**：
```bash
cd my-project
claude --plugin-dir .claude-plugins/project-specific
```

**适用场景**：
- 业务特定的规则验证
- 项目特定的文档生成
- 团队内部专用工具

### 策略 C：混合方式（最佳实践）

结合全局和项目插件。

**配置方式**：
```bash
# 配置文件设置全局插件
# ~/.claude/config.json
{
  "pluginDir": "~/.claude/plugins"
}

# 命令行添加项目插件
claude --plugin-dir ~/.claude/plugins --plugin-dir .claude-plugins
```

## 多插件配置详解

### 方式 1：命令行指定多个目录

```bash
# 指定两个插件目录
claude --plugin-dir ~/.claude/plugins --plugin-dir ./project-plugins

# 指定三个或更多
claude \
  --plugin-dir ~/.claude/global-tools \
  --plugin-dir ./company-plugins \
  --plugin-dir ./project-specific
```

### 方式 2：使用统一的父目录

将所有插件放在一个父目录下，自动发现所有子目录。

```bash
~/.claude/plugins/
├── code-review/      # 插件1
├── testing/          # 插件2
└── docs/             # 插件3
```

配置：
```bash
# 只需配置一次父目录
claude --plugin-dir ~/.claude/plugins
# Claude 会自动扫描所有子插件
```

### 方式 3：Plugin 管理系统

```bash
# 列出已安装插件
claude plugin list

# 安装插件
claude plugin install username/repo
claude plugin install /path/to/local/plugin

# 启用/禁用插件
claude plugin enable code-review
claude plugin disable testing

# 更新插件
claude plugin update code-review

# 删除插件
claude plugin remove code-review
```

## Plugin vs Project 对比

| 维度 | Plugin | Project |
|------|--------|---------|
| **作用域** | 可跨项目复用 | 特定项目 |
| **位置** | 独立目录或共享目录 | 项目内部 |
| **内容** | Agent 定义、资源文件 | 业务代码 |
| **版本控制** | 独立仓库或共享 | 跟随项目 |
| **更新频率** | 较低（稳定后） | 持续更新 |

**内容划分建议**：

| 类型 | 放哪里 | 示例 |
|------|--------|------|
| 通用能力 | Plugin | 代码风格检查、安全扫描、测试生成模式 |
| 业务逻辑 | Project | 业务规则验证、API 文档生成、领域特定工具 |

## 性能优化建议

| 场景 | 推荐配置 | 说明 |
|------|----------|------|
| 快速格式化 | `model: haiku` | 简单任务用轻量模型 |
| 代码审查 | `model: sonnet` | 平衡质量和速度 |
| 架构设计 | `model: opus` | 复杂推理用最强模型 |
| 文本搜索 | 限制 tools | 只给必要的工具 |

## 进阶常见问题

**Q: 如何避免插件冲突？**

A: 使用独特的 Agent 名称和描述：

```yaml
# ❌ 容易冲突
name: reviewer
description: Review code

# ✅ 明确独特
name: security-focused-reviewer
description: Use when user asks for "security review", "安全审查"
```

**Q: 如何调试插件加载问题？**

A: 使用详细日志模式：
```bash
claude --plugin-dir /path/to/plugin --log-level debug
```

**Q: 插件可以依赖其他插件吗？**

A: 目前不支持插件间依赖。每个插件应保持独立。

**Q: 如何分享插件给团队？**

三种方式：

1. **Git 仓库**
   ```bash
   git clone https://github.com/company/plugins.git ~/.claude/plugins
   ```

2. **npm 包**
   ```bash
   npm install -g @company/claude-plugins
   ```

3. **直接复制**
   ```bash
   cp -r /shared/plugins ~/.claude/
   ```

**Q: 如何管理插件版本？**

使用语义化版本：
```json
{
  "version": "2.1.3"
  //        │ │ │
  //        │ │ └── 补丁版本（bug 修复）
  //        │ └── 次版本（新功能，向后兼容）
  //        └── 主版本（破坏性变更）
}
```

**Q: 如何声明兼容性？**

```json
{
  "claude": {
    "minVersion": "1.0.0",
    "maxVersion": "2.0.0"
  }
}
```

---

## 学习路径建议

```
入门阶段
  ├── 阅读"第一部分：快速入门"
  ├── 尝试使用内置 Explore agent
  └── 完成 [[Subagent 实战练习]] 的练习 1-2

进阶阶段
  ├── 阅读"第二部分：创建自定义 Agent"
  ├── 创建你的第一个自定义 Agent
  └── 完成练习 3-4

高级阶段
  ├── 阅读"第三部分：高级使用与最佳实践"
  ├── 优化你的 Agent 配置
  └── 完成练习 5 和综合挑战
```

---

## 相关文档

[[Prompt, Agent, MCP 是什么]] | [[Claude Code 常用功能]] | [[Claude MCP 使用指南]] | [[Subagent 实战练习]]
