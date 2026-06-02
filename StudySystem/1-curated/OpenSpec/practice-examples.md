---
curated:
  date: 2026-06-01
  topic: OpenSpec
  sources:
    - R02: Getting Started Guide (Official)
    - R12: Gigazine Kitchen Timer Walkthrough (Community)
    - R15: Reddit OpenSpec + Beads Experience (Community)
    - R14: Initial Guide CN (Community)
  category: 实战示例
---

# OpenSpec 实战示例

## 1. 示例一：为应用添加深色模式

**来源:** 官方入门指南 [来源: R02]

这是 OpenSpec 官方文档提供的完整示例，演示从零开始为一个 Web 应用添加深色模式功能。

### 1.1 启动变更（默认路径）

```
You: /opsx:propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — 为什么做、做什么
     ✓ specs/       — 需求和场景
     ✓ design.md    — 技术方法
     ✓ tasks.md     — 实现检查清单
     Ready for implementation! [来源: R02]
```

### 1.2 生成的工件内容

**proposal.md（意图和范围）:**

```markdown
# Proposal: Add Dark Mode

## Intent
用户请求了一个深色模式选项以减少夜间使用时的眼睛疲劳。

## Scope
- 在设置中添加主题切换
- 支持系统偏好检测
- 在 localStorage 中持久化偏好

## Approach
使用 CSS 自定义属性进行主题化，配合 React Context 管理状态。 [来源: R02]
```

**tasks.md（实现检查清单）:**

```markdown
# Tasks

## 1. 主题基础设施
- [ ] 1.1 创建带 light/dark 状态的 ThemeContext
- [ ] 1.2 添加颜色的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换添加到设置页面
- [ ] 2.3 更新 Header 包含快速切换

## 3. 样式
- [ ] 3.1 定义深色主题配色方案
- [ ] 3.2 更新组件使用 CSS 变量 [来源: R02]
```

### 1.3 实现

```
You: /opsx:apply

AI:  Working through tasks...
     ✓ 1.1 Created ThemeContext with light/dark state
     ✓ 1.2 Added CSS custom properties to globals.css
     ✓ 1.3 Implemented localStorage persistence
     ✓ 2.1 Created ThemeToggle component
     ...
     All tasks complete! [来源: R02]
```

实现过程中，如果设计需要调整，只需"更新工件并继续"。

### 1.4 归档

```
You: /opsx:archive

AI:  Archiving add-dark-mode...
     ✓ Merged specs into openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
     Done! Ready for the next feature. [来源: R02]
```

### 1.5 验证和检查

```bash
# 列出活跃变更
openspec list

# 查看变更详情
openspec show add-dark-mode

# 验证规范格式
openspec validate add-dark-mode

# 交互式仪表盘
openspec view [来源: R02]
```

---

## 2. 示例二：厨房计时器应用

**来源:** GIGAZINE 博客（2025-10-26）[来源: R12]

一个完整的端到端示例，使用 OpenSpec 构建一个浏览器端厨房计时器。**注意：本例使用旧版命令语法（`/openspec-proposal` 而非 `/opsx:propose`），适用于 GitHub Copilot Chat。**

### 2.1 编辑 project.md

描述目的和规范：

> Purpose: "通过 Web 浏览器为家庭和商业厨房提供简单且高可见性的计时器。"

功能：1/3/5 分钟按钮、大字体倒计时显示、倒计时中按下按钮重置。

技术栈：HTML5、JavaScript (ES6)、CSS3。

### 2.2 创建变更

```
/openspec-proposal Create a UI
```

这会在 `changes/` 下生成一个 `create-ui` 文件夹，包含：
- **proposal.md** — 摘要、动机、范围、参考
- **design.md** — "最小化的单页 Web 应用，使用纯 HTML/CSS/JS。无框架。"
- **tasks.md** — 6 个任务：脚手架文件、实现 UI、倒计时/重置逻辑、CSS、手动测试、验证 spec.md
- **spec.md** — 需求包括计时器 UI、按钮、倒计时、重置、大字体、可访问性

### 2.3 生成代码

```
/openspec-apply
```

代码自动生成。"仅需一条指令"就完成了厨房计时器。错误可以通过 AI 聊天纠正。

### 2.4 归档

```
/openspec-archive
```

归档标记提案完成。未来的规范变更需要新的提案。

### 2.5 关键洞察

"你可以只在想要保留历史记录的部分使用 OpenSpec"，其余部分继续使用常规方法，"这可以提高整个项目的效率和质量。" [来源: R12]

---

## 3. 示例三：OpenSpec + Beads 组合工作流

**来源:** Reddit r/ClaudeCode，作者 nicoracarlo（高级开发者）[来源: R15]

一个真实世界的工作流，将 OpenSpec 与 Beads（Steve Yegge 的作品）结合使用。

### 3.1 为什么同时使用两者

| 工具单独使用 | 问题 |
|------------|------|
| OpenSpec 单独 | 生成了好的计划但"当计划变得太大时，它会开始产生幻觉" |
| Beads 单独 | 对于大型功能需要太多手动跟踪 |

组合后："两全其美"。 [来源: R15]

### 3.2 4 阶段工作流

**第 1 阶段：分析**
用 `ultrathink` 提示 Claude Code，在规划前彻底分析代码。

**第 2 阶段：OpenSpec 提案**
分析满意后，要求 Claude Code 创建 OpenSpec 提案。

**第 3 阶段：OpenSpec 验证**
"我会彻底验证它们。跳过这个验证部分就像自找麻烦。"
阅读并修复规范直到完全满意。

**第 4 阶段：Beads 创建和执行**
命令："Import the tasks from MY-OPENSPEC OpenSpec change into Beads"

### 3.3 CLAUDE.md 配置（节选）

**OpenSpec 指令：**
当请求涉及规划、提案、新功能、破坏性变更或模糊情况时，打开 `@/openspec/AGENTS.md`。

**工作风格："Think First, Code Once"**
7 步流程：彻底分析 → 映射系统 → 澄清需求 → 设计完整方案 → 展示计划 → 仔细实现 → 坚持计划。

**Beads/问题追踪规则：**
- 始终使用 `bd`（Beads）进行问题追踪
- 每个 `bd create` 必须包含 `-d`（完整上下文标志）
- 描述必须包含：规范文件引用、相关需求、验收标准、技术上下文

**AGENTS.md 中的 Beads 使用表：**

| 场景 | 工具 | 操作 |
|------|------|------|
| 新功能 | OpenSpec | 先提案 |
| 已批准的规范 | 两者 | 将任务导入 Beads |
| Bug/小任务 | Beads | 直接 `bd create` |
| 发现问题 | Beads | `bd create --discovered-from` |
| 准备开始工作 | Beads | `bd ready` |
| 功能完成 | OpenSpec | 归档 [来源: R15] |

### 3.4 工作流优势

- 清晰的功能定义
- 代码匹配作者的个人风格
- 更少的幻觉
- "更少的骂人" [来源: R15]

---

## 4. 最佳实践汇总

### 4.1 规范编写

| 正确的做法 | 错误的做法 |
|------------|------------|
| 关注"做什么"而非"怎么做" | 描述实现细节 |
| 使用 GIVEN-WHEN-THEN 场景 | 使用模糊的需求描述 |
| 确保可测试性 | 编写不可验证的需求 |
| 保持简洁，一次一个变更 | 一次做太多事情 [来源: R14] |

### 4.2 变更管理

1. 保持每个变更作为一个逻辑单元
2. 使用清晰名称如 `add-dark-mode`，避免 `feature-1`
3. 及时归档已完成的变更
4. 初始规范不需要完美；边进行边迭代 [来源: R14]

### 4.3 团队协作

- 在代码仓库中共享 `.openspec/` 目录
- 在实现前审查 `proposal.md` 和 `design.md`
- 定期使用 `/opsx:sync` [来源: R14]

### 4.4 可用性注意事项

- OpenSpec 最适合**结构化功能和修复**，不适合修改单行 CSS 或修复打字错误 [来源: R13]
- 可以只在需要保留历史的项目部分使用 OpenSpec [来源: R12]
- 验证步骤不可跳过 [来源: R15]
