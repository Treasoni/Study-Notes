---
title: CLAUDE.md 使用指南
tags: [claude, ai, 进阶应用, 配置]
created: 2026-04-05
updated: 2026-08-10
status: updated
source_project: claude-code-tutorial
---

# CLAUDE.md 使用指南

> [!info] 概述
> **CLAUDE.md 是项目的"指令手册"** - Claude Code 每次启动时自动读取，作为项目的持久化记忆系统和规则来源。

## 核心概念 💡

### 什么是 CLAUDE.md

**是什么**：项目级配置文件，作为 Claude 的系统提示词

**为什么需要**：
- 为 Claude 提供项目上下文
- 定义项目特定的开发规范
- 记录团队约定和工作流程
- 作为项目的"记忆系统"

> [!tip] 大白话
> CLAUDE.md 就是给 Claude Code 的"上岗说明书"：每次开工前它都会先读一遍，记住这个项目怎么构建、怎么运行、有什么约定，免得你每句话都得重新交代一遍。

### 文件优先级（2026）

| 文件/目录 | 位置 | 作用域 | 共享 |
|-----------|------|--------|------|
| Managed Policy | 管理员部署 | 组织级 | 是（强制，不可覆盖） |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | 否（所有项目） |
| `CLAUDE.md` | 项目根目录 | 项目级 | 是（提交到 Git） |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | 否（本地配置） |
| 子目录 `CLAUDE.md` | 项目子目录 | 目录级 | 是（仅当读取该目录文件时加载） |
| `.claude/rules/` | 项目目录 | 路径范围 | 是（提交到 Git） |
| `.claude/output-styles/` | 项目目录 | 系统提示词 | 是（人格/语气切换） |

### 工作原理

```
启动 Claude Code
    ↓
扫描项目目录
    ↓
读取 CLAUDE.md → 构建语义上下文图
    ↓
应用规则 → 作为系统提示词
    ↓
开始会话
```

## 扩展定制机制（2026）

> [!note] 不止 CLAUDE.md
> Claude Code 提供 **7 种定制机制**，各自在不同时机加载、拥有不同权威级别。CLAUDE.md 只是其中之一。

| 机制 | 位置 | 加载时机 | 权威性 | 最佳用途 |
|------|------|----------|--------|----------|
| **CLAUDE.md** | `./CLAUDE.md`, `~/.claude/` | 会话启动，持久化 | 建议性 | 项目规范、构建命令、架构约定 |
| **Rules** | `.claude/rules/*.md` | 全会话或路径匹配 | 建议性 | 文件特定约束 |
| **Skills** | `.claude/skills/*/SKILL.md` | 按需调用 | 建议性 | 流程、检查清单、部署 |
| **Subagents** | `.claude/agents/*.md` | 按需委派 | 隔离执行 | 复杂子任务隔离运行 |
| **Hooks** | `settings.json` | 生命周期事件 | **强制执行** | 自动格式化、危险命令拦截 |
| **Output Styles** | `.claude/output-styles/` | 注入系统提示词 | 高 | 人格切换、教学模式 |
| **Append System Prompt** | CLI 参数 `--system-prompt` | 单次调用 | 中等 | 临时标准 |

> [!tip] 2026 年趋势
> Anthropic 已从 CLAUDE.md 移除了 **80%+ 的冗余指令**给新模型。模型判断力越强，越不需要死板规则。关键是设计清晰接口而非堆砌例子。

## 最佳实践

### 1. 保持精简（200 行以内 / 25KB 内）

单个 `CLAUDE.md` 建议控制在 **200 行以内或 25KB 以内**。超过这个规模，Claude 的依从性会明显下降——过长内容会被随机忽略，还白白占用上下文预算。

> [!tip] 大白话
> CLAUDE.md 不是越厚越好。写成一整本说明书，Claude 反而抓不住重点；写成一张"要点速查卡"，它才会真正照着执行。

**❌ 不推荐**：
```markdown
## 什么是组件
组件是可复用的 UI 元素...
（解释基本概念，浪费 tokens）
```

**✅ 推荐**：
```markdown
## 组件规范
- 所有组件放在 /src/components
- 使用 TypeScript + 组合式 API
- 导出时添加 JSDoc 注释
```

### 2. 项目特异性

聚焦项目独特之处，**不要写代码库或工具本身就能推导出的内容**（函数签名、框架文档、命令帮助）。能被工具自动发现的信息写进 CLAUDE.md 纯属浪费——`/doctor` 也会专门建议删掉这类冗余。

> [!tip] 大白话
> 能自己查到的东西别写。源码里的注释、`git log`、`npm help`，Claude 自己会看。CLAUDE.md 只写"这个项目里人定的特殊规矩"。

**❌ 不推荐**：
```markdown
# Git 分支管理
Git 是分布式版本控制系统...
main 是主分支...
```

**✅ 推荐**：
```markdown
# 分支策略
- main: 生产环境
- develop: 开发环境
- feature/*: 功能分支
- hotfix/*: 紧急修复

合并前必须通过 PR review。
```

### 3. 说明"为什么"

解释规则背后的原因，Claude 表现更好。

### 4. 使用 @import 引入外部文件

> [!tip] @import 语法
> 在 CLAUDE.md 中使用 `@import` 可拉入其他文件（最多 5 层嵌套），适合将详细规范拆分到独立文件。

```markdown
# CLAUDE.md

## 项目概述
...

## 编码规范
@import ./docs/coding-standards.md

## 架构决策
@import ./docs/adr/001-auth-flow.md
```

### 5. 子目录 CLAUDE.md（Monorepo 友好）

> [!tip] 子目录规则
> 子目录中的 `CLAUDE.md` 仅当 Claude 读取该目录内的文件时才会加载——非常适合 monorepo。

```
repo/
├── CLAUDE.md              # 始终加载（根级规则）
├── frontend/
│   ├── CLAUDE.md          # 仅在处理 frontend/ 文件时加载
│   └── src/
└── backend/
    ├── CLAUDE.md          # 仅在处理 backend/ 文件时加载
    └── src/
```

### 6. `.claude/rules/` 路径范围规则

> [!tip] 路径范围规则（2026 Q2 新增）
> `.claude/rules/` 目录支持通过 `paths:` 元数据定义路径范围，触及时才加载——节省上下文预算。

```bash
.claude/rules/
├── common/
│   ├── env.md              # 始终加载的通用规则
│   └── hooks.md            # Hook 规范
└── frontend/
    └── rules.md            # 仅当处理 frontend/ 目录时加载
        paths: frontend/
```

**规则加载优先级**（高→低）：
1. Managed Policy（管理策略，强制覆盖）
2. `~/.claude/CLAUDE.md`（用户级全局）
3. `CLAUDE.md`（项目根）
4. `CLAUDE.local.md`（本地个人覆盖）
5. 子目录 `CLAUDE.md`
6. `.claude/rules/`（路径匹配）
7. `.claude/output-styles/`（输出风格）
8. 内置规则

> [!warning] 项目级 CLAUDE.md 需要工作区信任
> `./CLAUDE.md` 只有在**项目目录被标记为可信工作区**后才会被读取。首次进入新目录时若出现信任确认，须先授权；未被信任的工作区不会加载项目级 CLAUDE.md 及其规则，也不会读取 `.claude/` 下的配置。

```markdown
## 状态管理
使用 Pinia 而非 Vuex。
原因：Pinia 支持 TypeScript，API 更简洁，
      且是 Vue 3 官方推荐的状态管理方案。
```

## Hooks 确定性自动化

> [!warning] 唯一强制机制
> Hooks 是 Claude Code **唯一真正确定性**的定制机制——它们在生命周期事件触发时无条件执行，不受上下文压缩影响，始终生效。

### 配置方式

Hooks 注册在 `.claude/settings.json` 中，不在 CLAUDE.md 里：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx eslint --fix $CLAUDE_FILE_PATH 2>/dev/null || true"
      }
    ]
  }
}
```

### Hook 类型

| 类型 | 说明 | 典型用途 |
|------|------|----------|
| `command` | Shell 命令 | 格式化、lint 检查、拦截操作 |
| `http` | HTTP POST 请求 | Webhook、Slack 通知 |
| `mcp_tool` | 调用 MCP 工具 | 复用已有 MCP 集成 |
| `prompt` | 单轮 LLM 判断 | 安全评估（"这个命令安全吗？"） |
| `agent` | 多轮子代理 | 复杂验证任务 |

### 关键生命周期事件

Hooks 支持 **30+ 个生命周期事件**，常用包括：

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `PreToolUse` | 工具执行前 | 验证/拦截危险操作 |
| `PostToolUse` | 工具执行后 | 自动格式化文件 |
| `UserPromptSubmit` | 用户提交消息 | 注入上下文 |
| `SessionStart` / `SessionEnd` | 会话启停 | 初始化/清理 |
| `PreCompact` / `PostCompact` | 上下文压缩前后 | 保留状态 |

### 退出码语义

| 退出码 | 含义 | 行为 |
|--------|------|------|
| `0` | 成功 | 继续执行，stdout 解析为 JSON |
| `2` | **阻止** | stderr 作为错误反馈给 Claude |
| `1` | 非阻止错误 | 仅记录日志，继续执行 |

> [!tip] 拦截模式
> 需要阻止操作时，用 `exit 2` 而非 `exit 1`。管道 stdin 到子 shell 会静默吞掉阻止信号（已知陷阱）。

### 适用场景

- **自动格式化**：编辑文件后自动运行 linter
- **保护敏感文件**：阻止修改 `.env`、`package-lock.json`
- **分支保护**：检查当前分支是否允许推送
- **合规检查**：提交前扫描密钥泄露
- **通知**：构建完成后通知 Slack

## 模板与示例

### 最小模板

```markdown
# CLAUDE.md

## 项目概述
一句话描述项目功能

## 目录结构
- /src - 源代码
- /tests - 测试文件
- /docs - 文档

## 常用命令
- npm install - 安装依赖
- npm run dev - 启动开发服务器
- npm run build - 构建生产版本
- npm test - 运行测试

## 代码规范
- 使用 ESLint + Prettier
- 组件命名采用 PascalCase
- 工具函数命名采用 camelCase

## 禁止事项
- 不要修改 package-lock.json
- 不要直接修改 dist 目录
- 避免使用 any 类型

## 完成标准
- 所有测试通过
- 代码通过 ESLint 检查
- 功能经人工验证
```

> [!note] 示例仅作结构参考
> 完整示例偏长，**仅作章节结构参考**。实际落地仍建议把 CLAUDE.md 控制在 200 行 / 25KB 内，按需裁剪示例中的子项。

### 完整示例

```markdown
# CLAUDE.md

## 项目概述
企业级 CRM 系统，基于 Vue 3 + TypeScript + Vite

## 技术栈
- 前端：Vue 3, TypeScript, Vite, Pinia, Vue Router
- UI：Element Plus
- 样式：SCSS
- 测试：Vitest

## 目录结构
```
/src
  /api       # API 接口
  /assets    # 静态资源
  /components# 通用组件
  /views     # 页面组件
  /stores    # Pinia stores
  /router    # 路由配置
  /utils     # 工具函数
  /types     # TypeScript 类型
```

## 开发工作流

### 启动项目
```bash
npm install
npm run dev
```

### 构建部署
```bash
npm run build     # 构建
npm run preview   # 预览
```

### 代码检查
```bash
npm run lint      # ESLint 检查
npm run format    # Prettier 格式化
npm run type-check # TypeScript 类型检查
```

### 测试
```bash
npm run test      # 单元测试
npm run test:ui   # 测试 UI
npm run test:coverage # 覆盖率
```

## 代码规范

### 组件规范
- 单文件组件使用 `<script setup lang="ts">`
- 组件文件名使用 PascalCase
- Props 必须定义类型
- Emit 事件使用 kebab-case

### 命名规范
- 组件：PascalCase (UserProfile.vue)
- 文件夹：kebab-case (/user-management/)
- 变量/函数：camelCase (getUserData)
- 常量：UPPER_SNAKE_CASE (API_BASE_URL)
- 接口：PascalCase + I 前缀 (IUserProfile)

### Git 提交规范
遵循 Conventional Commits：
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具配置

## 架构约定

### 状态管理
- 全局状态使用 Pinia
- 组件本地状态使用 ref/reactive
- 避免在组件中直接访问 localStorage

### API 调用
- 所有 API 调用放在 /src/api 目录
- 使用统一的请求拦截器处理错误
- 敏感信息通过环境变量配置

### 路由管理
- 路由配置放在 /src/router/index.ts
- 懒加载页面组件
- 使用路由守卫处理权限

## 禁止事项

❌ 不要修改的文件：
- package-lock.json
- dist/ 目录下的所有文件
- public/vite.svg

❌ 不要使用的依赖：
- moment.js（使用 dayjs 替代）
- lodash（按需引入 lodash-es）
- any 类型（必须有明确类型定义）

❌ 不要做的事情：
- 在组件中直接写样式（使用 scoped）
- 硬编码字符串（使用 i18n）
- 绕过 TypeScript 类型检查

## 自定义命令

### /refactor
"重构这段代码，保持功能不变，提高可读性"

### /review
"按项目规范审查这段代码，指出问题并给出修改建议"

### /test
"为这段代码编写单元测试，覆盖主要场景"

## 完成标准

任务完成需满足：
1. ✅ 所有测试通过（npm test）
2. ✅ 代码通过 ESLint 检查（npm run lint）
3. ✅ TypeScript 类型检查通过（npm run type-check）
4. ✅ 功能经人工验证
5. ✅ 必要时更新文档
```

## 任务沟通公式

有效任务委托的结构化方式：

```
目标：你想要的结果
约束：不做什么 / 必须遵循什么
验收：如何证明完成了
```

### 示例 - Bug 修复
```
目标：修复登录流程中的认证错误
约束：不修改用户表结构；不引入新依赖
验收：运行 npm test 全部通过；使用测试账号可正常登录
```

### 示例 - 新功能
```
目标：添加用户导出 Excel 功能
约束：使用 xlsx 库；支持筛选；前端处理
验收：可导出当前筛选结果；格式正确；无性能问题
```

## 高级技巧

### 多层配置策略

```bash
# 全局配置（所有项目共享）
~/.claude/CLAUDE.md           # 个人编码风格、常用工具

# 项目配置（团队共享）
./CLAUDE.md                   # 项目规范、架构约定

# 本地配置（个人覆盖）
./CLAUDE.local.md             # 本地开发配置、调试信息
```

### 使用 /init 自动生成

```bash
# 在项目目录运行
claude
/init

# Claude 分析代码库并生成初始 CLAUDE.md
# 你可以审查和修改生成的内容
```

### 与 .gitignore 配合

```gitignore
# 共享的项目配置
CLAUDE.md

# 个人本地配置（不提交）
CLAUDE.local.md
```

### 诊断命令

| 命令 | 用途 |
|------|------|
| `/doctor`（=`/checkup`） | 全量环境体检：诊断安装健康、未用 skills/MCP/插件、CLAUDE.md 裁剪建议、慢 hooks 标记 |
| `/memory` | 验证 CLAUDE.md 是否已加载 |
| `/hooks` | 查看已注册的 Hooks |
| `/context` | 查看上下文使用情况 |

> [!note] /doctor 的 CLAUDE.md 裁剪（2026）
> `/doctor`（别名 `/checkup`）会主动提议**裁剪已提交的 CLAUDE.md**：删除可由代码库/工具推导的内容、跨文件去重、合并重复的记忆文件，并标记运行缓慢的 hooks。建议定期跑一次，保持记忆文件精简。

## 决策框架：什么时候用什么

> [!summary] 选择指南
> 别把所有东西都塞进 CLAUDE.md——不同问题用不同机制解决。

| 如果你在 CLAUDE.md 里写... | 改用 |
|---------------------------|------|
| "每次 X 时都做 Y" | **Hook**（注册在 settings.json） |
| "永远不要做这个" | **Hook + 权限**（确定性护栏） |
| 30 行的流程步骤 | **Skill**（按需加载，不占上下文） |
| 特定 API 的规则 | **路径范围 Rule**（加 `paths:`） |
| 个人偏好 | **`~/.claude/CLAUDE.md`**（用户级文件） |
| 安全/合规规则 | **Managed Policy**（管理员部署，不可覆盖） |

## 常见问题 ❓

**Q: CLAUDE.md 会被提交到 Git 吗？**

A: `CLAUDE.md` 应该提交，让团队共享配置。`CLAUDE.local.md` 不应提交。

**Q: 文件太长怎么办？**

A: 精简内容，只保留真正重要的项目特定规则。详细文档放在 /docs 目录。

**Q: 如何测试 CLAUDE.md 是否有效？**

A: 启动新会话，执行典型任务，观察 Claude 是否遵循你的规范。

**Q: 可以动态修改 CLAUDE.md 吗？**

A: 可以，修改后重启 Claude Code 或使用 `/clear` 清理会话后重新开始。

**Q: CLAUDE.md 和 Comments 有什么区别？**

A: CLAUDE.md 是项目级指导，影响所有操作。代码注释针对特定代码片段。

**Q: CLAUDE.md 和 Hooks 有什么区别？**

A: CLAUDE.md 是建议性规则，受上下文压缩影响可能被忽略；Hooks 是确定性机制，每次事件触发时无条件执行。需要"一定发生"的行为用 Hooks。

**Q: Skills 和 CLAUDE.md 如何选择？**

A: 多步骤流程（部署、代码审查等）写成 Skill，按需加载不占上下文。项目常识（构建命令、目录结构）留在 CLAUDE.md。

**Q: 如何知道自己用了多少上下文？**

A: 在 Claude Code 中使用 `/context` 查看当前上下文使用情况，`/memory` 查看已加载的配置。

## 更新记录

- **2026-08-10**: 更新 CLAUDE.md 精简标准（200 行 / 25KB 内）；补充 `/doctor`（=`/checkup`）裁剪建议（删可推导内容、去重、合并记忆文件、标记慢 hooks）；新增项目级 CLAUDE.md 工作区信任说明；核心概念补充大白话。
- **2026-07-27**: 补充七种定制机制概览、Hooks 确定性自动化、决策框架；更新文件优先级表（新增 Managed Policy、Output Styles）；更新 @import 嵌套深度 4→5 层。

## 相关文档
[[如何使用Claude code]] | [[Claude Code 会话管理]] | [[Claude Code 常用功能]]
