---
tags:
  - Claude
  - CLI
  - AI工具
  - 开发工具
created: 2026-02-05
---

# Claude Code 常用功能

> [!info] 简介
> Claude Code 是 Anthropic 官方提供的 CLI 工具，让你在终端中直接使用 Claude 进行软件工程任务。它集成了文件操作、代码编辑、Git 管理等功能，是开发者的智能助手。

## 核心特点

- 📁 **直接文件操作** - 读取、编辑、写入代码文件
- 🔍 **强大的搜索** - 使用 Glob 和 Grep 进行文件和内容搜索
- 🖥️ **Shell 集成** - 无缝执行命令行操作
- 📦 **Git 自动化** - 智能创建 commit 和 PR
- 📋 **任务管理** - 追踪复杂任务的进度
- 🎯 **规划模式** - 大型改动前的架构规划

---

## 常用 Slash 命令

| 命令 | 描述 | 使用场景 |
|------|------|----------|
| `/help` | 显示所有可用命令 | 查看帮助信息 |
| `/commit` | 创建 git commit | 提交代码变更 |
| `/review-pr` | 审查 Pull Request | 代码审查 |
| `/plan` | 进入规划模式 | 复杂任务的预先规划 |
| `/remember` | 记住项目信息 | 保存项目上下文 |
| `/tasks` | 查看任务列表 | 检查当前任务状态 |
| `/explain` | 解释代码 | 理解代码逻辑 |

---

## 核心功能

### 📝 代码编辑

> [!abstract] 文件操作
> Claude Code 提供直接的文件操作能力，无需手动编辑

- **Read** - 读取文件内容
- **Edit** - 精确替换文本内容
- **Write** - 创建或覆写文件

```bash
# 示例请求
"读取 src/utils.js 文件"
"将所有的 console.log 替换为 logger.info"
"创建一个新的 config.yaml 文件"
```

### 🔍 文件搜索

> [!summary] 搜索工具
> 快速定位代码和文件

- **Glob** - 按模式匹配文件路径
  ```bash
  # 查找所有 JS 文件
  "**/*.js"
  # 查找特定目录下的文件
  "src/components/**/*.tsx"
  ```

- **Grep** - 在文件内容中搜索
  ```bash
  # 搜索包含 "TODO" 的代码
  grep "TODO"
  # 搜索函数定义
  grep "function\s+\w+"
  ```

### 🖥️ 命令执行

> [!tip] Bash 工具
> 执行任何 shell 命令

```bash
# 安装依赖
npm install
# 运行测试
pytest tests/
# 查看状态
git status
```

### 📦 Git 操作

> [!important] Git 集成
> 自动化代码提交流程

- 创建智能 commit 消息
- 自动添加相关文件
- 支持 PR 创建
- 遵循仓库的提交风格

```bash
# 直接请求提交
"提交当前的修复"
"为这次更改创建 commit"
```

### 📋 计划模式

> [!warning] 何时使用计划模式
> 对于复杂的、需要多步骤的任务，先规划后执行

适合使用计划模式的场景：
- ✅ 添加新功能
- ✅ 重构现有代码
- ✅ 修改多个文件的架构
- ✅ 有多种实现方案的任务

---

## 常用工作流

### 🔧 修复 Bug

```bash
# 步骤
1. 描述问题： "登录功能报错"
2. Claude 会：读取相关代码 → 分析问题 → 提出修复方案 → 实施修复
3. 验证：运行测试确保修复有效
```

### ✨ 添加新功能

```bash
# 步骤
1. 进入规划模式：/plan
2. Claude 分析：探索代码库 → 设计方案 → 提交计划
3. 确认后执行：按照计划逐步实现
4. 创建 commit 提交更改
```

### ♻️ 代码重构

```bash
# 步骤
1. 描述目标："重构用户模块使用 TypeScript"
2. Claude 会：分析依赖 → 制定重构策略 → 逐步迁移
3. 验证：运行测试确保功能不变
```

### 👀 审查代码

```bash
# 步骤
1. 使用 /review-pr 或直接贴代码
2. Claude 会：检查逻辑 → 识别潜在问题 → 建议改进
```

---

## 键盘快捷键

| 按键 | 功能 |
|------|------|
| `Ctrl+C` | 停止当前操作 |
| `Ctrl+D` | 发送空输入结束对话 |

---

## 最佳实践

> [!success] 提升效率的建议

### 1. 提供清晰的上下文

```bash
# ❌ 不够清晰
"修复这个文件"

# ✅ 清晰明确
"修复 auth.js 中的登录 bug，错误信息是 'Invalid token'"
```

### 2. 一步步处理复杂任务

```bash
# 对于大型任务，分解为小步骤
1. "先创建用户数据模型"
2. "然后创建 API 端点"
3. "最后添加前端界面"
```

### 3. 使用 Plan Mode 处理大型改动

```bash
# 对于影响多个文件的改动
/plan
"实现用户权限管理系统"
```

### 4. 充分利用 Git 集成

```bash
# 让 Claude 帮你管理提交
"提交这次 API 更改"
# Claude 会自动分析变更并生成合适的 commit 消息
```

### 5. 信任 Claude 的判断

```bash
# Claude 会自动：
- 选择合适的工具
- 处理依赖关系
- 并行执行独立任务
- 验证操作结果
```

---

## 相关链接

- [[Prompt, Agent, MCP 是什么]]
- [[Skills 是什么]]
- [[如何使用Claude code]]

---

## 参考资源

- [Claude Code Documentation](https://code.claude.ai)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
