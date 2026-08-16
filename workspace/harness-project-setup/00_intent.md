# 从零搭建 Agent Harness 工程 - 意图文件

## 基本信息

- **主题**: 从零搭建 Agent Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战
- **项目标识**: harness-project-setup
- **创建时间**: 2026-08-16
- **当前阶段**: 阶段 0
- **输出目标**: obsidian（已确认）
- **Vault 路径**: `D:\Study-Notes`（已确认）
- **笔记目录**: `AI学习/Harness工程实战`（已确认）
- **MOC 路径**: `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`（已确认）

## 学习目标

### 笔记类型
实战笔记（动手搭建 + 结构对照）

### 学习深度
上手（能独立从一个空目录搭建出自己的 harness 工程骨架）

### 用户基础
有了解（已学习 Harness Engineering 概念、DeepSeek-Harness 教程系列；"差不多会了"）

## 研究计划

### 探索方向
1. **Harness 工程目录骨架**：开始一个项目先创建哪些文件（AGENTS.md / .claude/ / .codex/ / docs/ 等），各目录职责与最小集合
2. **Skills 的放置与结构**：skills 放在哪里（`.claude/skills/` vs 项目内）、SKILL.md 契约、跨 runtime 同步
3. **Hooks / Subagents / Rules 配置**：`.claude/settings.json` hooks 注册、subagents（agents）定义、rules 目录与优先级
4. **AGENTS 文件体系**：AGENTS.md 与 .claude/rules 的分工、渐进式披露原则、与 Claude Code 配置的对照

### 重点收集
- **核心概念**: AGENTS.md、Harness 脚手架、skills 契约、hooks 生命周期、subagent 隔离、rules 分层
- **实战代码**: 一个最小可用的 harness 工程骨架（目录树 + 每个关键文件的示例内容）
- **常见坑**: 路径硬编码、全局 vs 项目配置、hooks 注册丢失、skills 目录放错、AGENTS 文件过大
- **工具链**: Claude Code、DeepSeek-Harness、.agent-sync、todo-state.sh、workflow-routing

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户明确要求：**不需要从零开始写，根据现有笔记 + 网上资料**。
- 现有笔记来源（本 vault）：
  - `AI学习/01-基础概念/Harness-Engineering-系统治理工程.md`（Harness 理论框架）
  - `AI学习/01-基础概念/AI工程范式演进-Prompt到Harness.md`（范式演进）
  - `AI学习/DeepSeek-Harness 教程/*`（DeepSeek-Harness 配置实操）
  - 本项目自身就是一个活体 harness 工程范本（`.claude/skills`、`.claude/rules`、`.claude/hooks`、`.claude/agents`、`.codex/`、`workspace/workflow-runs/`）
- 待用户在阶段 0 确认：笔记目录位置、MOC 归属、研究深度。
