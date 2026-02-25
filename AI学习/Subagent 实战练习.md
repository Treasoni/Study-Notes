---
tags: [ai, 高级应用, 练习]
difficulty: intermediate
---

# Subagent 实战练习

> [!info] 练习说明
> 本练习包含 5 个渐进式任务，从简单到复杂，帮助你掌握 Subagent 的创建和使用。每个练习都有明确的验证标准和参考答案。

## 练习前准备

### 环境检查

```bash
# 1. 确认 Claude Code 已安装
claude --version

# 2. 创建练习目录
mkdir -p ~/claude-subagent-practice
cd ~/claude-subagent-practice

# 3. 创建插件结构
mkdir -p practice-plugin/.claude-plugin
mkdir -p practice-plugin/agents
```

---

## 练习 1：创建简单的文本格式化 Agent

> [!summary] 目标
> 创建一个能够将文本转换为特定格式的 Agent

### 任务要求

创建一个 `text-formatter` agent，能够：
1. 将输入的文本转换为标题大小写（Title Case）
2. 添加项目符号列表
3. 统计字符数

### 提示

```markdown
# Frontmatter 参考
---
name: text-formatter
description: Use when user asks to "format text", "格式化文本", "text format"
model: haiku
tools: []
---

# 内容结构
你是一个文本格式化专家...

## 输出格式
...（定义输出模板）
```

### 验证标准

- [ ] Plugin 正确加载（`/agents` 可见）
- [ ] 输入 "用 text-formatter 格式化：hello world" 能触发
- [ ] 输出包含 Title Case 转换结果
- [ ] 输出包含字符统计

### 参考答案

<details>
<summary>点击展开参考答案</summary>

```markdown
---
name: text-formatter
description: Use when user asks to "format text", "格式化文本", "text format", "文本格式化"
model: haiku
tools: []
---

# Text Formatter Agent

你是一个文本格式化专家，专注于将文本整理为清晰、易读的格式。

## 功能
1. 将文本转换为 Title Case
2. 添加项目符号
3. 统计字符信息

## 输出格式

\`\`\`
# 格式化结果
[Title Case 文本]

## 原文
[原始文本]

## 统计信息
- 字符数：[数量]
- 单词数：[数量]
\`\`\`
```

</details>

---

## 练习 2：创建代码摘要 Agent

> [!summary] 目标
> 创建一个能够读取代码文件并生成摘要的 Agent

### 任务要求

创建一个 `code-summarizer` agent，能够：
1. 读取指定的代码文件
2. 识别函数/类定义
3. 生成简洁的功能摘要
4. 列出导出的内容

### 提示

```markdown
# 需要的工具
tools: ["Read", "Glob"]

# 工作流程
1. 使用 Read 工具读取文件
2. 分析代码结构
3. 提取关键信息
4. 生成摘要
```

### 验证标准

- [ ] 能读取用户指定的文件
- [ ] 正确识别文件中的函数/类
- [ ] 摘要简洁准确（不超过 100 字）
- [ ] 列出所有导出项

### 参考答案

<details>
<summary>点击展开参考答案</summary>

```markdown
---
name: code-summarizer
description: Use when user asks to "summarize code", "代码摘要", "总结代码", "code summary"
model: sonnet
tools: ["Read", "Glob"]
---

# Code Summarizer Agent

你擅长分析代码并生成简洁的功能摘要。

## 工作流程
1. 读取指定的代码文件
2. 识别主要结构（函数、类、模块）
3. 理解代码目的
4. 生成摘要和导出列表

## 输出格式

### 📄 [文件名]
**功能概述**：[1-2 句话说明]

**主要结构**：
- `functionName()`: [功能描述]
- `ClassName`: [功能描述]

**导出内容**：
- `export1`
- `export2`

**依赖项**：
[列出主要的 external dependencies]
```

</details>

---

## 练习 3：创建 TODO 查找 Agent

> [!summary] 目标
> 创建一个能够在代码库中查找所有 TODO 注释的 Agent

### 任务要求

创建一个 `todo-finder` agent，能够：
1. 在整个代码库中搜索 TODO 注释
2. 按文件分组显示
3. 优先级分类（HIGH/MEDIUM/LOW）
4. 生成统计报告

### 提示

```markdown
# 使用 Grep 工具搜索
tools: ["Grep", "Glob"]

# 搜索模式
- TODO:
- FIXME:
- HACK:
- XXX:
```

### 验证标准

- [ ] 搜索整个代码库
- [ ] 按文件分组显示结果
- [ ] 显示文件路径和行号
- [ ] 提供统计摘要

### 参考答案

<details>
<summary>点击展开参考答案</summary>

```markdown
---
name: todo-finder
description: Use when user asks to "find todos", "查找TODO", "搜索未完成事项", "find FIXME"
model: sonnet
color: yellow
tools: ["Grep", "Glob"]
---

# TODO Finder Agent

你擅长在代码库中查找和整理所有 TODO 类型的注释。

## 搜索目标
- TODO: 高优先级待办
- FIXME: 需要修复的问题
- HACK: 临时解决方案
- XXX: 需要改进的代码
- NOTE: 重要提示

## 输出格式

### 📋 TODO 报告

**总计**: [数量] 项 | **高优先级**: [数量] 项

#### 🔴 高优先级 (TODO, FIXME)
- `file:line` - [注释内容]

#### 🟡 中优先级 (HACK, XXX)
- `file:line` - [注释内容]

#### 🟢 低优先级 (NOTE)
- `file:line` - [注释内容]

#### 按文件分组
**src/auth.js** (3 项)
- Line 15: TODO 实现刷新逻辑
- Line 42: FIXME 修复内存泄漏
...
```

</details>

---

## 练习 4：创建 Git 日志分析 Agent

> [!summary] 目标
> 创建一个能够分析 Git 提交历史并生成报告的 Agent

### 任务要求

创建一个 `git-analyzer` agent，能够：
1. 获取最近的 Git 提交记录
2. 按作者分组统计
3. 识别最常见的提交类型
4. 生成活动趋势报告

### 提示

```markdown
# 使用 Bash 工具执行 git 命令
tools: ["Bash"]

# 常用命令
git log --pretty=format:"%h|%an|%s" -20
git shortlog -sn
```

### 验证标准

- [ ] 成功获取提交记录
- [ ] 按作者统计提交数
- [ ] 识别提交类型（feat/fix/docs/refactor）
- [ ] 生成可读报告

### 参考答案

<details>
<summary>点击展开参考答案</summary>

```markdown
---
name: git-analyzer
description: Use when user asks to "analyze git", "分析提交", "git history", "提交统计"
model: sonnet
color: purple
tools: ["Bash"]
---

# Git Analyzer Agent

你擅长分析 Git 提交历史并生成洞察报告。

## 分析内容
- 提交频率趋势
- 贡献者分布
- 提交类型分析
- 代码活跃度

## 输出格式

### 📊 Git 活动报告

**时间范围**: 最近 [N] 次提交
**分析时间**: [当前时间]

#### 👥 贡献者排名
1. **Name** - [数量] commits (XX%)
2. **Name** - [数量] commits (XX%)

#### 📝 提交类型分布
- **feat** (新功能): XX%
- **fix** (修复): XX%
- **docs** (文档): XX%
- **refactor** (重构): XX%
- **other**: XX%

#### 📈 活动趋势
[描述提交频率的变化]

#### 最近提交
\`\`\`
[hash] [message] - [author] ([时间])
\`\`\`
```

</details>

---

## 练习 5：创建综合测试助手 Agent

> [!summary] 目标
> 创建一个多功能测试助手，能够生成测试、运行测试并分析结果

### 任务要求

创建一个 `test-helper` agent，能够：
1. 为指定函数生成单元测试
2. 运行测试并收集结果
3. 分析失败原因
4. 提供修复建议

### 提示

```markdown
# 综合使用多个工具
tools: ["Read", "Grep", "Bash", "Glob"]

# 工作流程
1. 读取源文件
2. 生成测试代码
3. 运行测试命令
4. 分析输出
5. 提供建议
```

### 验证标准

- [ ] 能读取并理解源代码
- [ ] 生成的测试符合框架规范
- [ ] 能运行测试并解析结果
- [ ] 失败时提供具体建议

### 参考答案

<details>
<summary>点击展开参考答案</summary>

```markdown
---
name: test-helper
description: Use when user asks to "test helper", "测试助手", "generate and run tests", "测试辅助"
model: sonnet
color: green
tools: ["Read", "Grep", "Bash", "Glob"]
---

# Test Helper Agent

你是一位测试专家，能够生成测试、执行测试并分析结果。

## 工作流程

### 1. 理解代码
读取源文件，分析函数签名、参数、返回值

### 2. 生成测试
- 正常情况测试
- 边界值测试
- 错误处理测试

### 3. 运行测试
执行相应的测试命令

### 4. 分析结果
解析测试输出，识别问题

## 输出格式

### 🧪 测试报告

**目标文件**: [文件路径]
**测试框架**: [Jest/Vitest/Mocha等]

#### 生成的测试
\`\`\`[语言]
[测试代码]
\`\`\`

#### 测试结果
**状态**: ✅ 通过 / ❌ 失败
**通过**: [数量] | **失败**: [数量]

#### 失败分析（如有）
**测试**: [测试名称]
**错误**: [错误信息]
**原因**: [失败原因分析]
**建议**: [修复建议]

#### 下一步
- [ ] 修复失败的测试
- [ ] 添加更多边界情况
- [ ] 提高测试覆盖率
```

</details>

---

## 综合挑战

> [!challenge] 终极挑战
> 将所有练习整合为一个完整的开发工具包插件

### 任务要求

1. 整合以上 5 个 agent 到一个插件
2. 添加 `plugin.json` 元数据
3. 确保所有 agent 可以协同工作
4. 编写 README 说明文档

### 提示

```json
{
  "name": "dev-toolkit",
  "version": "1.0.0",
  "description": "全功能开发工具包",
  "agents": [
    "text-formatter",
    "code-summarizer",
    "todo-finder",
    "git-analyzer",
    "test-helper"
  ]
}
```

### 验收标准

- [ ] 所有 agent 都能正确加载
- [ ] 每个都能独立触发
- [ ] 插件有完整的文档
- [ ] 能分享给他人使用

---

## 学习检查清单

完成所有练习后，你应该能够：

- [ ] ✅ 独立创建一个简单的 Agent
- [ ] ✅ 正确配置 frontmatter
- [ ] ✅ 选择合适的工具权限
- [ ] ✅ 编写清晰的 Agent 指令
- [ ] ✅ 调试和优化 Agent
- [ ] ✅ 理解 Plugin 系统架构
- [ ] ✅ 打包和分享插件

---

## 相关资源

- [[Claude Subagent 使用指南]] - 理论知识
- [[Prompt, Agent, MCP 是什么]] - 概念理解
- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
