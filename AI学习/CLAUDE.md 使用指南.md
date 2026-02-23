---
tags: [claude, ai, config]
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

### 文件优先级

| 文件 | 位置 | 作用域 | 共享 |
|------|------|--------|------|
| `CLAUDE.md` | 项目根目录 | 项目级 | 是（提交到 Git） |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | 否（本地配置） |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | 否（所有项目） |

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

## 最佳实践

### 1. 保持简洁

Claude 可靠遵循约 150-200 条指令。过长会导致内容被随机忽略。

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

聚焦项目独特之处，不要解释通用知识。

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

```markdown
## 状态管理
使用 Pinia 而非 Vuex。
原因：Pinia 支持 TypeScript，API 更简洁，
      且是 Vue 3 官方推荐的状态管理方案。
```

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

## 相关文档
[[如何使用Claude code]] | [[Claude Code 会话管理]] | [[Claude Code 常用功能]]
