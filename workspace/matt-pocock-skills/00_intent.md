# Matt Pocock Skills - Agent 框架设计深度解析

## 基本信息

- **主题**: Matt Pocock Skills - Agent 框架设计深度解析
- **项目标识**: matt-pocock-skills
- **创建时间**: 2026-07-23
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目/GitHub项目
- **笔记目录**: ./
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
概念笔记 + 实战笔记

### 学习深度
精通（分析架构原理、设计权衡、最佳实践，并应用于构建自己的 Agent 项目框架）

### 用户基础
有了解（了解 Claude Code/Codex 等 AI 编码工具的基本使用，有构建自定义工作流的需求）

### 核心目标
从 Matt Pocock Skills 中提取可复用的设计模式和原则，用于搭建自己的 Agent 项目框架。这不仅是理解，而是要回答：

1. 如果我要设计自己的 Agent 技能系统，目录结构怎么组织？
2. invocation 模式如何选择（用户调用 vs 模型调用）？
3. SKILL.md 的最佳实践是什么，怎么写才清晰可执行？
4. 上下文管理怎么设计（Grill → Handoff → Compact）？
5. 如何设计可组合的 Agent 工作流？

## 研究计划

### 探索方向
1. **项目核心架构与设计哲学**
   - 仓库整体结构（bucketed 组织、双分发机制）
   - 用户调用 vs 模型调用的核心二分法
   - ask-matt 作为中央路由器的设计
   - 四大问题域的对应方案

2. **SKILL.md 编写艺术**
   - 可预测性作为核心美德
   - 信息层级设计（行内步骤 > 行内参考 > 外部引用）
   - Leading words 概念与模型先验
   - 修剪原则（单一真相、相关性、no-op 测试）
   - 失败模式（过早完成、重复、沉积、蔓延、no-op、否定）

3. **Socratic Sparring（对话边界澄清）**
   - grill-me vs grill-with-docs vs grilling 三层抽象
   - 决策树遍历模式
   - 有状态 vs 无状态设计的取舍
   - 单次一问原则

4. **Handoff / Context Compaction（上下文压缩）**
   - 跨会话上下文桥接
   - handoff vs built-in compact 的区别（fork vs continue）
   - 最小化上下文转移的开销设计

### 重点收集
- **核心概念**: Agent Skill 设计模式、Invocation model、Context load vs Cognitive load、Progressive disclosure、Leading words
- **实战代码**: skills/ 目录下各 SKILL.md 的完整内容、CLAUDE.md、AGENTS.md、CONTEXT.md、ADR 文件
- **设计模式**: 分层抽象、链式委托、并行子代理、有状态/无状态分离
- **工具链**: skills.sh 安装器、Claude Code Plugin 分发、ask-matt 路由机制

### 信源偏好
- 官方文档: 是（仓库源码是主要信源）
- 技术博客: 是（Matt Pocock 的博客和演讲）
- 社区讨论: 是（GitHub Issues/Discussions）
- 学术论文: 否

## 备注

- 输出到 Obsidian vault: /Users/zhqznc/Documents/项目/GitHub项目/
- 仓库的 .agents/adr/ 目录记录了重要的架构决策，需重点分析
- writing-great-skills 的 GLOSSARY.md 是理解整个设计语言的关键文件
