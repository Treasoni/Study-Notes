---
tags: [claude, ai, 工具使用, 斜杠命令]
created: 2026-02-28
---

# Claude Code 自定义斜杠命令教程

> [!info] 概述
> **斜杠命令（Slash Commands）是可复用的工作流模板** - 将复杂的提示词封装成简单命令，用 `/命令名` 快速触发。让 AI 真正"懂"你的项目。

## 核心概念 💡

### 什么是斜杠命令

**通俗理解**：就像给 AI 设置"快捷键"——把一套复杂的操作流程存成一个文件，下次只需要输入一个命令就能自动执行。

**举个例子**：
```
❌ 传统方式：每次都要解释一大堆
"请帮我检查这个文件的代码规范：
1. 变量命名要清晰
2. 函数不能超过50行
3. 要有错误处理
4. TypeScript类型要准确
5. 注意性能问题..."

✅ 斜杠命令：
/review src/Button.tsx
```

### 两种命令范围

| 类型 | 位置 | 作用域 | 适用场景 |
|------|------|--------|----------|
| **项目级** | `.claude/commands/` | 当前项目 | 团队规范、项目特定流程 |
| **用户级** | `~/.claude/commands/` | 所有项目 | 个人习惯、通用模板 |

**优先级**：项目级 > 用户级（同名命令时项目级优先）

### 命令 vs Skills vs Agents

```
┌─────────────────────────────────────────────────────────┐
│              三者的区别与联系                              │
├─────────────────────────────────────────────────────────┤
│  Command（命令）  →  手动触发，单次执行                   │
│  Skills（技能）   →  AI自动判断何时调用                   │
│  Agents（代理）   →  独立进程，可多轮迭代                  │
└─────────────────────────────────────────────────────────┘
```

## 操作步骤 🚀

### 步骤 1：创建命令目录

```bash
# 项目级命令（推荐用于团队共享）
mkdir -p .claude/commands

# 用户级命令（推荐用于个人习惯）
mkdir -p ~/.claude/commands
```

### 步骤 2：创建命令文件

**命令文件格式**：
```markdown
---
description: "命令的简短描述"
argument-hint: "参数提示"
allowed-tools: ["工具1", "工具2"]
---

这里写具体的提示词内容，用 $ARGUMENTS 代表传入的参数
```

**字段说明**：
| 字段 | 必填 | 说明 | 示例 |
|------|:----:|------|------|
| `description` | ✅ | 命令描述，输入 `/` 时显示 | "代码审查" |
| `argument-hint` | ❌ | 参数提示 | "文件路径" |
| `allowed-tools` | ❌ | 允许使用的工具列表 | ["Read", "Edit"] |
| `model` | ❌ | 指定使用的模型 | "claude-opus-4-6" |

### 步骤 3：编写你的第一个命令

**示例：代码审查命令**

创建文件 `.claude/commands/review.md`：

```markdown
---
description: "检查代码规范和潜在问题"
argument-hint: "文件路径"
allowed-tools: ["Read", "Grep"]
---

请帮我审查这个文件的代码：$ARGUMENTS

检查要点：
- [ ] 变量命名是否清晰（避免 a、b、c 这种）
- [ ] 函数是否过长（超过50行考虑拆分）
- [ ] 是否有错误处理
- [ ] TypeScript类型定义是否正确
- [ ] 是否有潜在的性能问题

别太严格，重点问题指出来就行。
```

### 步骤 4：重启 Claude Code

```bash
# 退出当前会话
exit

# 重新启动
claude
```

### 步骤 5：使用命令

```bash
# 输入斜杠后会自动提示可用命令
/review src/components/Button.tsx
```

## 实用示例 📚

### 示例 1：单元测试生成器

**文件**：`.claude/commands/test.md`

```markdown
---
description: "为文件生成单元测试"
argument-hint: "文件路径"
allowed-tools: ["Read", "Write", "Grep"]
---

请为这个文件编写完整的单元测试：$ARGUMENTS

要求：
1. 使用我们项目的测试框架（查看 package.json 确认）
2. 覆盖正常情况和边界情况
3. 包含错误处理测试
4. 添加必要的 mock
5. 测试文件命名为 *.test.ts 或 *.spec.ts

先读取文件内容，然后生成测试代码。
```

**用法**：`/test src/utils/formatter.ts`

### 示例 2：文档生成器

**文件**：`.claude/commands/api-docs.md`

```markdown
---
description: "生成 API 文档"
argument-hint: "API 文件路径"
---

请为这个 API 文件生成文档：$ARGUMENTS

文档格式：
## 接口名称
简要描述

### 请求
- **方法**：GET/POST/PUT/DELETE
- **路径**：/api/path
- **参数**：
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|:----:|------|
  | id | string | ✅ | 用户ID |

### 响应
```json
{
  "code": 200,
  "data": {}
}
```

### 错误码
| 代码 | 说明 |
|------|------|
| 400 | 参数错误 |
```

**用法**：`/api-docs src/api/user.ts`

### 示例 3：Git 提交信息生成

**文件**：`.claude/commands/commit.md`

```markdown
---
description: "生成规范的 Git 提交信息"
allowed-tools: ["Bash"]
---

!git diff --cached --name-only

!git diff --cached --stat

根据以上更改生成一个符合 Conventional Commits 规范的提交信息：

格式：<type>(<scope>): <subject>

类型（type）：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具变更

要求：
1. subject 不超过50字符
2. 使用中文
3. 简洁描述做了什么
```

**用法**：`/commit`

### 示例 4：数据库迁移助手

**文件**：`.claude/commands/migration.md`

```markdown
---
description: "创建数据库迁移文件"
argument-hint: "变更描述"
allowed-tools: ["Bash", "Read", "Write"]
---

!ls -la migrations/ | tail -5

为这个变更创建数据库迁移：$ARGUMENTS

参考现有迁移文件的格式：
- UP 迁移（如何执行）
- DOWN 迁移（如何回滚）
- 记住添加必要的索引

生成的 SQL 要能安全地多次执行。
```

**用法**：`/migration 添加用户头像字段`

### 示例 5：README 生成器

**文件**：`.claude/commands/readme.md`

```markdown
---
description: "生成项目 README"
allowed-tools: ["Read", "Grep"]
---

请为这个项目生成一个专业的 README.md

先查看 package.json 了解项目信息，然后生成包含以下部分的 README：

# 项目名称
一句话简介

## 功能特点
- 核心功能列表

## 安装
```bash
安装命令
```

## 使用
基本用法示例

## 配置
必要的配置说明

## 开发
- 启动项目
- 运行测试
- 构建部署

## 许可证
MIT
```

**用法**：`/readme`

## 高级技巧 🎯

### 技巧 1：用 `!` 执行 Shell 命令

在命令中先用 Shell 获取信息，再让 AI 处理：

```markdown
---
description: "检查代码健康度"
allowed-tools: ["Bash"]
---

!npm run lint
!npm run test -- --coverage

根据上面的输出，分析代码健康度并给出改进建议。
```

### 技巧 2：用 `@` 读取文件

让 AI 直接读取文件内容：

```markdown
---
description: "解释代码"
argument-hint: "文件路径"
---

请用通俗的语言解释这段代码的作用：@$ARGUMENTS

包括：
1. 代码的整体功能
2. 关键部分的作用
3. 可能存在的问题
```

**用法**：`/explain src/utils/auth.ts`

### 技巧 3：用目录组织命令

```
.claude/commands/
├── git/
│   ├── commit.md      # /git/commit
│   └── pr.md          # /git/pr
├── test/
│   ├── unit.md        # /test/unit
│   └── e2e.md         # /test/e2e
└── docs/
    ├── api.md         # /docs/api
    └── readme.md      # /docs/readme
```

**用法**：`/git/pr` 或 `/test/unit`

### 技巧 4：参数占位符 `$ARGUMENTS`

```markdown
# 单参数
---
description: "删除文件"
argument-hint: "文件路径"
---
删除这个文件：$ARGUMENTS

# 多参数（空格分隔）
---
description: "重命名文件"
argument-hint: "旧路径 新路径"
---
将 $ARGUMENTS 重命名（第一个是旧路径，第二个是新路径）
```

### 技巧 5：多语言命令

```markdown
---
description: "翻译代码注释"
argument-hint: "文件路径 目标语言"
---

请将这个文件的注释翻译成指定语言：$ARGUMENTS

只翻译注释内容，不要修改代码逻辑。
```

**用法**：`/i18n src/utils.ts English`

## 命令模板 📝

### 模板 1：通用代码审查

```markdown
---
description: "代码质量检查"
argument-hint: "文件路径"
allowed-tools: ["Read", "Grep"]
---

审查以下代码：$ARGUMENTS

检查项：
- 代码可读性
- 潜在 bug
- 性能问题
- 安全隐患
- 测试覆盖

给出具体改进建议，不要泛泛而谈。
```

### 模板 2：重构建议

```markdown
---
description: "代码重构建议"
argument-hint: "文件路径"
---

分析这段代码并给出重构建议：$ARGUMENTS

重点关注：
1. 是否符合 SOLID 原则
2. 是否有重复代码
3. 职责是否单一
4. 是否易于测试
5. 命名是否清晰

给出重构后的示例代码。
```

### 模板 3：性能分析

```markdown
---
description: "性能优化分析"
argument-hint: "文件或代码片段"
---

分析这段代码的性能问题：$ARGUMENTS

检查：
- 时间复杂度
- 空间复杂度
- 是否有不必要的计算
- 是否有内存泄漏风险
- 是否可以并行处理

给出优化建议和性能对比。
```

## 常见问题 ❓

**Q: 命令创建后找不到？**

A: 检查以下几点：
1. 文件是否在正确的目录（`.claude/commands/` 或 `~/.claude/commands/`）
2. 文件名是否以 `.md` 结尾
3. 是否重启了 Claude Code
4. 文件名是否正确（命令名 = 文件名去掉 .md）

**Q: 参数 `$ARGUMENTS` 不生效？**

A:
1. 确认拼写正确（注意大小写）
2. 确认用户确实输入了参数
3. 在命令中测试：`echo "参数是：$ARGUMENTS"`

**Q: 如何调试命令？**

A:
```markdown
---
description: "调试命令"
argument-hint: "测试参数"
---

第一步：显示参数
参数内容：$ARGUMENTS

第二步：执行操作
...（你的命令逻辑）
```

然后运行命令，观察输出。

**Q: 可以在一个命令中调用另一个命令吗？**

A: 不可以直接调用，但可以：
1. 将共同逻辑提取到 Skills 中
2. 复制命令内容
3. 使用 Agent 实现复杂流程

**Q: 命令可以用中文命名吗？**

A: 可以！文件名可以是中文，如 `代码审查.md`，用法：`/代码审查`

**Q: 如何让团队共享命令？**

A:
```bash
# 1. 将项目级命令提交到 Git
git add .claude/commands/
git commit -m "Add custom commands"

# 2. 团队成员拉取后自动可用
git pull
```

**Q: allowed-tools 有哪些可用工具？**

A: 常用工具包括：
| 工具 | 说明 |
|------|------|
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件 |
| `Grep` | 搜索内容 |
| `Glob` | 查找文件 |
| `Bash` | 执行命令 |
| `WebSearch` | 网络搜索 |

## 最佳实践 ⭐

### 命令命名

| ✅ 推荐 | ❌ 避免 |
|---------|---------|
| `/review-code` | `/cmd1` |
| `/test-unit` | `/helper` |
| `/docs-api` | `/stuff` |
| `/git/commit` | `/do-it` |

### 命令描述

```markdown
# ✅ 好的描述
description: "检查代码规范和潜在bug"

# ❌ 不好的描述
description: "命令"
description: "做一个事情"
```

### 命令维护

1. **定期清理**：删除不常用的命令
2. **版本控制**：项目命令提交到 Git
3. **添加文档**：在命令中添加使用说明
4. **团队协作**：定期 review 和优化共享命令

### 团队协作建议

```
项目级命令（共享）
├── .claude/commands/
│   ├── review.md      # 团队代码规范
│   ├── test.md        # 团队测试规范
│   └── docs.md        # 团队文档规范
└── CLAUDE.md          # 项目配置

用户级命令（个人）
└── ~/.claude/commands/
    ├── my-review.md   # 个人审查习惯
    └── my-notes.md    # 个人笔记习惯
```

## 注意事项 ⚠️

### 安全建议

```markdown
# ❌ 避免在命令中硬编码敏感信息
---
description: "部署到生产"
---
API_KEY="sk-xxx" deploy
```

```markdown
# ✅ 使用环境变量
---
description: "部署到生产"
allowed-tools: ["Bash"]
---
!deploy $DEPLOY_ENV
```

### 性能建议

1. **避免过度使用 `!` 命令**：每次执行都会消耗 tokens
2. **限制 `allowed-tools`**：只列出必要的工具
3. **保持命令简洁**：复杂逻辑考虑用 Agent

## 相关文档
- [官方文档 - 斜杠命令](https://docs.anthropic.com/zh-CN/docs/claude-code/slash-commands)
- [Claude Code 使用指南](./如何使用Claude%20code.md)
- [如何编写 Skills](../03-进阶应用/如何编写Skills.md)
- [Claude Code 会话管理](./Claude%20Code%20会话管理.md)
