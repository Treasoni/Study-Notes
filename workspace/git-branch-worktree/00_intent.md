# git branch 与 worktree — 意图文件

## 基本信息

- **主题**: git branch 与 worktree 的区别、使用场景，以及 AI 开发项目时该用哪个
- **项目标识**: git-branch-worktree
- **创建时间**: 2026-08-05
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目
- **笔记目录**: 项目实战/git实战
- **MOC 路径**: 项目实战/项目实战 MOC.md

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手

### 用户基础
有了解（会用 add/commit/branch/checkout 等基本命令，做过分支开发）

## 研究计划

### 探索方向
1. branch 与 worktree 的核心概念与底层机制差异（分支引用、HEAD、工作树、索引）
2. 各自适用场景与取舍（并行任务、隔离环境、多任务切换、磁盘占用）
3. AI 开发项目实战：何时用 branch、何时用 worktree，具体命令与推荐工作流

### 重点收集
- **核心概念**: branch（分支指针）、worktree（额外工作目录）、HEAD、checkout/switch、git worktree add/list/lock/remove
- **实战代码**: 创建与切换 branch；创建/管理多个 worktree 的命令示例；AI 并行任务典型流程
- **常见坑**: worktree 与分支绑定规则、重复 checkout 同一分支、stash 与未跟踪文件处理、忘记 `git worktree prune`
- **工具链**: git 版本要求（worktree 需 2.5+）、与 IDE / AI 工具配合、常用 alias

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户用 AI 开发项目，笔记最终需要给出「用 branch 还是 worktree」的可执行结论与判断依据。
- Vault 路径、笔记目录、MOC 路径待用户补充（阶段 6/7 前确认即可）。
