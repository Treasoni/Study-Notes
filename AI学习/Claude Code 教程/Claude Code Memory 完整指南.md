---
tags: [claude, ai, 工具使用, memory, claude-md, 持久化上下文]
created: 2026-04-05
updated: 2026-04-05
---

# Claude Code Memory 完整指南

> [!info] 概述
> **一句话定义**：Memory 是 Claude Code 的持久化上下文系统，通过 CLAUDE.md 文件让 Claude 记住项目规范、个人偏好和开发标准。
> **通俗比喻**：就像给 Claude 一本"项目说明书" —— 每次对话它都会先读这本书，知道你的编码风格、项目架构和团队规范。

## 核心概念

### 是什么

Memory 是 Claude Code 的**持久化记忆系统**，通过文件系统中的 CLAUDE.md 文件存储上下文信息，让 Claude 在不同会话间保持对项目的理解。

### 为什么需要

**解决的问题**：
- ❌ 每次对话都要重新解释项目背景
- ❌ Claude 不知道团队的编���规范
- ❌ 重复说明个人的开发偏好
- ❌ 团队成员对 Claude 的指令不一致

**Memory 提供的能力**：
- ✅ 跨会话保持项目上下文
- ✅ 团队共享编码标准
- ✅ 存储个人开发偏好
- ✅ 版本控制记忆文件
- ✅ 导入外部文档内容

### 通俗理解

**🎯 比喻**：
- **CLAUDE.md** = 项目的"入职培训手册"
- **User Memory** = 你的"个人工作习惯卡片"
- **Project Memory** = 团队的"编���规范文档"
- **Auto Memory** = Claude 自动记录的"学习笔记"

**📦 示例**：
```markdown
# CLAUDE.md 示例
## 项目概述
- 技术栈: TypeScript, React, Node.js
- 团队规模: 5 人

## 编码规范
- 使用 2 空格缩进
- 文件名使用 kebab-case
- 提交信息遵循 Conventional Commits

## 常用命令
| 命令 | 用途 |
|------|------|
| npm run dev | 启动开发服务器 |
| npm test | 运行测试 |
```

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Memory 系统概述

---

## Memory 命令快速参考

| 命令 | 用途 | 使用场景 |
|------|------|----------|
| `/init` | 初始化项目记忆 | 新项目首次设置 CLAUDE.md |
| `/memory` | 在编辑器中编辑记忆文件 | 大量更新、重组内容 |
| `# 规则内容` | 快速添加单行规则 | 对话中快速添加规则 |
| `# new rule into memory` | 显式添加记忆 | 添加复杂多行规则 |
| `# remember this` | 自然语言添加记忆 | 对话式记忆更新 |
| `@path/to/file` | 导入外部内容 | 引用现有文档 |

### `/init` 命令

**用途**：快速初始化项目 Memory

```
/init
```

**功能**：
- 在项目根目录创建 CLAUDE.md 文件
- 建立项目约定和指南的基础结构
- 设置跨会话上下文持久化的基础

**增强交互模式**：
```bash
CLAUDE_CODE_NEW_INIT=true claude
/init
```

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - /init 命令

### 快速更新 Memory

**使用 `#` 前缀**：
```
# 这个项目始终使用 TypeScript 严格模式

# 优先使用 async/await 而非 Promise 链

# 每次提交前运行 npm test
```

**工作流程**：
1. 以 `#` 开头输入规则
2. Claude 识别为记忆更新请求
3. 选择更新哪个记忆文件（项目或个人）
4. 规则被添加到相应的 CLAUDE.md

**替代模式**：
```
# new rule into memory
始终使用 Zod schemas 验证用户输入

# remember this
所有版本发布使用语义化版本号

# add to memory
数据库迁移必须是可逆的
```

### `/memory` 命令

**用途**：直接在编辑器中编辑记忆文件

```
/memory
```

**功能**：
- 在系统默认编辑器中打开记忆文件
- 允许大量添加、修改和重组
- 提供对层级中所有记忆文件的访问

**比较：`/memory` vs `/init`**

| 方面 | `/memory` | `/init` |
|------|-----------|---------|
| **用途** | 编辑现有记忆文件 | 初始化新 CLAUDE.md |
| **使用时机** | 更新/修改项目上下文 | 开始新项目 |
| **操作** | 打开编辑器进行更改 | 生成启动模板 |

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Memory Commands

---

## Memory 架构

### 层级结构

Claude Code 使用**多层级记忆系统**，不同范围的记忆文件服务不同目的：

```
graph TD
    A["Managed Policy<br/>/Library/.../ClaudeCode/CLAUDE.md"] -->|最高优先级| A2["Managed Drop-ins<br/>managed-settings.d/"]
    A2 --> B["Project Memory<br/>./CLAUDE.md"]
    B --> C["Project Rules<br/>./.claude/rules/*.md"]
    C --> D["User Memory<br/>~/.claude/CLAUDE.md"]
    D --> E["User Rules<br/>~/.claude/rules/*.md"]
    E --> F["Local Project Memory<br/>./CLAUDE.local.md"]
    F --> G["Auto Memory<br/>~/.claude/projects/.../memory/"]
```

### 完整层级（按优先级排序）

| 优先级 | 位置 | 范围 | 共享 | 最佳用途 |
|--------|------|------|------|----------|
| 1 (最高) | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Managed Policy | 组织级 | 公司级策略 |
| 1 (最高) | `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Managed Policy | 组织级 | 组织标准 |
| 1 (最高) | `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows) | Managed Policy | 组织级 | 企业规范 |
| 1.5 | `managed-settings.d/*.md` | Managed Drop-ins | 组织级 | 模块化策略 (v2.1.83+) |
| 2 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | Project Memory | 团队 | 团队标准、共享架构 |
| 3 | `./.claude/rules/*.md` | Project Rules | 团队 | 路径特定的模块化规则 |
| 4 | `~/.claude/CLAUDE.md` | User Memory | 个人 | 个人偏好（所有项目） |
| 5 | `~/.claude/rules/*.md` | User Rules | 个人 | 个人规则（所有项目） |
| 6 | `./CLAUDE.local.md` | Project Local | 个人 | 个人项目特定偏好 |
| 7 (最低) | `~/.claude/projects/<project>/memory/` | Auto Memory | 个人 | Claude 自动记录的学习笔记 |

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Memory Hierarchy

---

## 模块化规则系统

### 目录结构

```
your-project/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── code-style.md
│       ├── testing.md
│       ├── security.md
│       └── api/                  # 支持子目录
│           ├── conventions.md
│           └── validation.md

~/.claude/
├── CLAUDE.md
└── rules/                        # 用户级规则（所有项目）
    ├── personal-style.md
    └── preferred-patterns.md
```

### 路径特定规则（YAML Frontmatter）

定义仅适用于特定文件路径的规则：

```markdown
---
paths: src/api/**/*.ts
---

# API 开发规则

- 所有 API 端点必须包含输入验证
- 使用 Zod 进行 schema 验证
- 记录所有参数和响应类型
- 包含所有操作的错误处理
```

**Glob 模式示例**：
- `**/*.ts` - 所有 TypeScript 文件
- `src/**/*` - src/ 下的所有文件
- `src/**/*.{ts,tsx}` - 多种扩展名
- `{src,lib}/**/*.ts, tests/**/*.test.ts` - 多个模式

### 子目录和符号链接

- **子目录**：规则递归发现，可组织为主题文件夹
- **符号链接**：支持跨项目共享规则

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Modular Rules System

---

## Auto Memory

### 是什么

Auto Memory 是 Claude **自动记录**学习笔记和项目洞察的持久化目录，与手动维护的 CLAUDE.md 不同。

### 工作原理

- **位置**：`~/.claude/projects/<project>/memory/`
- **入口点**：`MEMORY.md` 作为主文件
- **主题文件**：可选的特定主题文件（如 `debugging.md`）
- **加载行为**：启动时加载 `MEMORY.md` 前 200 行；主题文件按需加载

### 目录结构

```
~/.claude/projects/<project>/memory/
├── MEMORY.md              # 入口点（启动时加载前 200 行）
├── debugging.md           # 主题文件（按需加载）
├── api-conventions.md     # 主题文件（按需加载）
└── testing-patterns.md    # 主题文件（按需加载）
```

### 版本要求

Auto Memory 需要 **Claude Code v2.1.59 或更高版本**

### 自定义 Auto Memory 目录

```json
// 在 ~/.claude/settings.json 或 .claude/settings.local.json
{
  "autoMemoryDirectory": "/path/to/custom/memory/directory"
}
```

> [!note] 注意
> `autoMemoryDirectory` 只能在用户级或本地设置中配置，不能在项目或托管策略设置中配置。

### 控制 Auto Memory

通过环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY` 控制：

| 值 | 行为 |
|----|------|
| `0` | 强制**开启** Auto Memory |
| `1` | 强制**关闭** Auto Memory |
| (未设置) | 默认行为（Auto Memory 启用） |

```bash
# 禁用 Auto Memory
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude

# 强制启用 Auto Memory
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0 claude
```

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Auto Memory

---

## 导入外部内容

### @ 导入语法

CLAUDE.md 支持 `@path/to/file` 语法包含外部内容：

```markdown
# 项目文档
参见 @README.md 了解项目概述
参见 @package.json 了解可用的 npm 命令
参见 @docs/architecture.md 了解系统设计

# 使用绝对路径从主目录导入
@~/.claude/my-project-instructions.md
```

### 导入特性

- ✅ 支持相对路径和绝对路径
- ✅ 支持递归导入（最大深度 5 层）
- ✅ 首次从外部位置导入会触发安全审批对话框
- ✅ Markdown 代码块中的导入语法不会被解析
- ✅ 避免重复，引用现有文档

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Import Syntax

---

## 排除 CLAUDE.md 文件

### 使用 `claudeMdExcludes`

在大型 monorepo 中，可使用此设置跳过不相关的 CLAUDE.md 文件：

```json
// 在 ~/.claude/settings.json 或 .claude/settings.json
{
  "claudeMdExcludes": [
    "packages/legacy-app/CLAUDE.md",
    "vendors/**/CLAUDE.md"
  ]
}
```

**适用场景**：
- Monorepo 中只有部分子项目相关
- 包含第三方或供应商的 CLAUDE.md 文件
- 减少上下文窗口噪音

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - claudeMdExcludes

---

## 实用示例

### 示例 1：项目 Memory 结构

```markdown
# 项目配置

## 项目概述
- **名称**: E-commerce Platform
- **技术栈**: Node.js, PostgreSQL, React 18, Docker
- **团队规模**: 5 人
- **截止日期**: Q4 2025

## 架构
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 开发标准

### 代码风格
- 使用 Prettier 格式化
- 使用 ESLint + airbnb 配置
- 最大行宽：100 字符
- 使用 2 空格缩进

### 命名约定
- **文件**: kebab-case (user-controller.js)
- **类**: PascalCase (UserService)
- **函数/变量**: camelCase (getUserById)
- **常量**: UPPER_SNAKE_CASE (API_BASE_URL)
- **数据库表**: snake_case (user_accounts)

### Git 工作流
- 分支名: `feature/description` 或 `fix/description`
- 提交信息: 遵循 Conventional Commits
- 合并前需要 PR
- 所有 CI/CD 检查必须通过
- 至少需要 1 个批准

## 常用命令

| 命令 | 用途 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试套件 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 生产构建 |
```

### 示例 2：目录特定 Memory

**文件**: `./src/api/CLAUDE.md`

```markdown
# API 模块标准

此文件覆盖 /src/api/ 的根 CLAUDE.md

## API 特定标准

### 请求验证
- 使用 Zod 进行 schema 验证
- 始终验证输入
- 返回 400 和验证错误

### 响应格式
所有响应必须遵循此结构：
{
  "success": true,
  "data": { /* 实际数据 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}

### 分页
- 使用基于游标的分页
- 包含 `hasMore` 布尔值
- 最大页大小 100
- 默认页大小 20
```

### 示例 3：个人 Memory

**文件**: `~/.claude/CLAUDE.md`

```markdown
# 我的开发偏好

## 关于我
- **经验水平**: 8 年全栈开发
- **首选语言**: TypeScript, Python
- **沟通风格**: 直接，带示例
- **学习风格**: 视觉图解 + 代码

## 代码偏好

### 错误处理
我更喜欢使用 try-catch 块和有意义的错误消息进行显式错误处理。
避免通用错误。��终记录错误以便调试。

### 注释
使用注释解释"为什么"，而不是"什么"。代码应该自文档化。
注释应解释业务逻辑或不明显的决策。

### 测试
我更喜欢 TDD（测试驱动开发）。
先写测试，再实现。
关注行为，而非实现细节。

## 沟通
- 用图解解释复杂概念
- 在解释理论之前展示具体示例
- 包含前后代码片段
- 最后总结关键点
```

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Practical Examples

---

## 最佳实践

### ✅ 应该做的

| 实践 | 说明 |
|------|------|
| **具体详细** | 使用清晰、详细的指令而非模糊指导 |
| **保持组织** | 使用清晰的 markdown 章节和标题结构 |
| **使用适当的层级** | Managed Policy → Project → User → Directory |
| **利用导入** | 使用 `@path/to/file` 引用现有文档 |
| **记录常用命令** | 包含重复使用的命令 |
| **版本控制项目记忆** | 将项目级 CLAUDE.md 提交到 git |
| **定期审查** | 随着项目发展更新记忆 |
| **提供具体示例** | 包含代码片段和具体场景 |

### ❌ 不应该做的

| 避免 | 原因 |
|------|------|
| **存储机密** | 永远不要包含 API 密钥、密码、令牌 |
| **包含敏感数据** | 无 PII、私人信息或专有机密 |
| **重复内容** | 使用导入引用现有文档 |
| **过于模糊** | 避免"遵循最佳实践"等通用语句 |
| **太长** | 保持单个记忆文件聚焦，500 行以内 |
| **过度组织** | 策略性使用层级 |
| **忘记更新** | 过时的记忆会导致困惑 |

### 选择正确的记忆级别

| 使用场景 | 记忆级别 | 原因 |
|----------|----------|------|
| 公司安全策略 | Managed Policy | 适用于组织所有项目 |
| 团队代码风格指南 | Project | 通过 git 与团队共享 |
| 你的编辑器快捷键 | User | 个人偏好，不共享 |
| API 模块标准 | Directory | 仅适用于该模块 |

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Best Practices

---

## 安装配置

### 设置项目 Memory

**方法 1：使用 `/init`（推荐）**

```bash
# 在项目目录中
cd /path/to/your/project

# 在 Claude Code 中运行
/init

# Claude 创建 CLAUDE.md 并填充模板结构

# 提交到 git
git add CLAUDE.md
git commit -m "使用 /init 初始化项目记忆"
```

**方法 2：手动创建**

```bash
# 创建 CLAUDE.md
cd /path/to/your/project
touch CLAUDE.md

# 添加内容
cat > CLAUDE.md << 'EOF'
# 项目配置

## 项目概述
- **名称**: Your Project Name
- **技术栈**: 列出你的技术
- **团队规模**: 开发者数量

## 开发标准
- 你的编码标准
- 命名约定
- 测试要求
EOF

# 提交到 git
git add CLAUDE.md
git commit -m "添加项目记忆配置"
```

### 设置个人 Memory

```bash
# 创建 ~/.claude 目录
mkdir -p ~/.claude

# 创建个人 CLAUDE.md
touch ~/.claude/CLAUDE.md

# 添加你的偏好
cat > ~/.claude/CLAUDE.md << 'EOF'
# 我的开发偏好

## 关于我
- 经验水平: [你的水平]
- 首选语言: [你的语言]
- 沟通风格: [你的风格]

## 代码偏好
- [你的偏好]
EOF
```

### 验证设置

```bash
# 检查记忆位置
# 项目根目录记忆
ls -la ./CLAUDE.md

# 个人记忆
ls -la ~/.claude/CLAUDE.md
```

> [!info] 📚 来源
> - [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - Installation Instructions

---

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[AI学习/02-工具使用/Claude Code Slash Commands 完整参考]] | Memory 通过 `/init`、`/memory` 命令管理 |
| [[AI学习/03-进阶应用/Claude MCP 使用指南]] | MCP 提供实时数据访问，Memory 提供静态上下文 |
| [[AI学习/01-基础概念/Skills 是什么]] | Skills 可利用 Memory 中的项目上下文 |
| [[AI学习/02-工具使用/Claude Code Hooks 使用指南]] | Hooks 是事件驱动，Memory 是静态持久化 |

---

## 常见问题

### Q: CLAUDE.md 和 Auto Memory 有什么区别？

| 特性 | CLAUDE.md | Auto Memory |
|------|-----------|-------------|
| **创建方式** | 手动编写 | Claude 自动生成 |
| **内容类型** | 项目规范、个人偏好 | 学习笔记、模式发现 |
| **加载时机** | 启动时完整加载 | MEMORY.md 前 200 行 + 按需加载 |
| **版本控制** | 建议提交到 git | 存储在用户目录 |

### Q: 项目级和用户级 Memory 如何协调？

- **项目级** (`./CLAUDE.md`): 团队共享，提交到 git
- **用户级** (`~/.claude/CLAUDE.md`): 个人偏好，不共享
- 两者合并加载，用户级作为个人定制的补充

### Q: 导入深度限制是多少？

最大支持 **5 层递归导入**。

### Q: 如何调试 Memory 加载问题？

1. 使用 `/status` 查看当前配置
2. 检查文件路径是否正确
3. 验证 YAML frontmatter 格式
4. 查看 Claude Code 日志

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

- [[AI学习/02-工具使用/Claude Code Slash Commands 完整参考]] - 斜杠命令完整参考
- [[AI学习/03-进阶应用/Claude MCP 使用指南]] - MCP 集成指南
- [[AI学习/01-基础概念/Skills 是什么]] - Skills 概念详解
- [[AI学习/02-工具使用/Claude Code Hooks 使用指南]] - 事件驱动自动化
- [[Claude Code Checkpoints 使用指南]] - 会话快照与回滚（Memory 与 Checkpoints 都是会话持久化机制）

---

## 参考资料

### 官方资源
- [Claude Code Overview](https://code.claude.com/docs/en/overview) - 官方文档
- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory) - Memory 官方文档

### 社区资源
- [GitHub - claude-howto Memory Guide](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md) - 详细 Memory 指南
- [Claude Code Memory Management: The Complete Guide (2026)](https://medium.com/data-science-collective/claude-code-memory-management-the-complete-guide-2026-b0df6300c4e8) - 完整指南
- [The Complete Guide to Claude Code: CLAUDE.md](https://ai.gopubby.com/the-complete-guide-to-claude-code-claude-md-743d4cbac757) - CLAUDE.md 完整指南
- [Claude Memory Guide: 3-Layer Architecture](https://www.shareuhack.com/en/posts/claude-memory-feature-guide-2026) - 三层架构说明

### 相关技能
- [Skills Guide](https://github.com/luongnv89/claude-howto/tree/main/03-skills) - Skills 完整参考
- [Hooks Guide](https://code.claude.com/docs/en/hooks) - 事件驱动自动化
