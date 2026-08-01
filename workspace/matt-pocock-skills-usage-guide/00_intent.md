# 如何使用 Matt Pocock Skills（Agent Skills 实操使用指南） - 意图文件

## 基本信息

- **主题**: 如何使用 Matt Pocock Skills（Agent Skills 实操使用指南）
- **项目标识**: matt-pocock-skills-usage-guide
- **创建时间**: 2026-08-01
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: GitHub项目
- **MOC 路径**: 未指定（P7 跳过）

## 学习目标

### 笔记类型
实战笔记（实操使用指南）

### 学习深度
精通

### 用户基础
熟悉

## 研究计划

### 探索方向

1. **安装与接入**：skills.sh 安装方式、Claude Code Plugin / Marketplace 分发、符号链接机制、AGENTS.md 跨平台契约
2. **调用与触发**：user-invoked vs model-invoked 的实际触发方式；逐个核心 skill 的用法与参数（/ask-matt、/grill-me、/grill-with-docs、/grilling、/to-spec、/to-tickets、/implement、/tdd、/code-review、/handoff、/compact 等）
3. **配置与定制**：CLAUDE.md / AGENTS.md / CONTEXT.md / ADR 的实际配置方法；如何把自定义 skill 接入本框架（SKILL.md 模板、调用边界、context pointer）
4. **工作流实战**：从 idea 到 ship 的完整流程演练；原型分支、多会话构建、context hygiene 的分窗策略
5. **常见问题与排错**：安装失败、skill 不触发（description 触发词）、调用边界违规、上下文过载、与 Codex 同步差异

### 重点收集

- **核心概念**: 安装步骤、触发命令、配置项、每个核心 skill 的逐个用法
- **实战代码**: skills.sh 安装命令、SKILL.md 实例、Claude Code 配置命令、handoff 文档模板
- **常见坑**: 安装路径/符号链接问题、description 缺少触发词、context load 过载、User-invoked 互相调用违规
- **工具链**: Claude Code、Codex、skills.sh、Claude Code Plugin、Marketplace

### 信源偏好

- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户已有深度解析笔记 [[GitHub项目/Matt Pocock Skills — Agent 框架设计深度解析.md]]，本篇为互补的**实操使用指南**，重点讲"怎么做"（安装、触发、配置、演练），不重复"为什么"的设计原理。
- 本地无 repo clone；素材以 GitHub 仓库实际文件（README、skills.sh、SKILL.md、CLAUDE.md、ADR）+ 官方/社区安装文档为主，可复用上一轮 `workspace/matt-pocock-skills/02_deep_research.md` 中的本地仓库文件素材。
- 输出到 Obsidian `GitHub项目/` 目录，与深度解析笔记相邻。
- MOC 不同步，阶段 7 跳过。
