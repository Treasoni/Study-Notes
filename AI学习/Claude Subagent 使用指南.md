---
title: Claude Subagent 使用指南
date: 2026-02-12
tags:
  - Claude
  - AI学习
  - Agent
---

# Claude Subagent 使用指南

> [!abstract] 概述
> Subagent（子代理）是 Claude Code 中用于处理复杂、多步骤任务的自主代理。它们就像「AI 专家助手」，每个 subagent 专注于特定领域的任务，可以独立工作并返回结果。

## 什么是 Subagent

> [!info] 核心概念
> Subagent 是 Claude 的专业化助手，具有以下特点：
> - **专注领域**：每个 subagent 擅长特定类型的任务
> - **独立工具**：拥有特定的工具集（如 Bash、Glob、Grep 等）
> - **自主执行**：可以自主规划和执行复杂任务
> - **返回结果**：完成任务后将结果返回给主会话

## 可用的 Subagent 类型

### 1. Bash
> [!tip] 命令执行专家
> 擅长运行 bash 命令，用于：
> - Git 操作
> - 包管理（npm, pip, cargo 等）
> - 文件系统操作
> - 终端任务

**可用工具**：仅 `Bash`

### 2. General Purpose
> [!tip] 通用问题解决者
> 擅长处理复杂的研究、代码搜索和多步骤任务：
> - 研究复杂问题
> - 搜索代码库
> - 执行多步骤任务

**可用工具**：所有工具（`*`）

### 3. Statusline Setup
> [!tip] 状态栏配置专家
> 专门用于配置 Claude Code 状态栏设置。

**可用工具**：`Read`、`Edit`

### 4. Explore
> [!tip] 代码库快速探索者
> 专门用于快速探索代码库结构：
> - 查找文件模式（如 `src/**/*.tsx`）
> - 搜索代码关键词（如 "API endpoints"）
> - 理解代码库架构

**可用工具**：除 `Task`、`ExitPlanMode`、`Edit`、`Write`、`NotebookEdit` 外的所有工具

**探索级别**：
- `quick` - 基础搜索
- `medium` - 适度探索
- `very thorough` - 全面深入分析

### 5. Plan
> [!tip] 软件架构师
> 专门用于设计实现方案：
> - 规划实现策略
> - 识别关键文件
> - 考虑架构权衡

**可用工具**：除 `Task`、`ExitPlanMode`、`Edit`、`Write`、`NotebookEdit` 外的所有工具

### 6. Claude Code Guide
> [!tip] Claude Code 专家
> 专门回答关于 Claude Code 的问题：
> - Claude Code CLI 特性
> - 钩子（hooks）和斜杠命令
> - MCP 服务器配置
> - IDE 集成
> - Agent SDK

**可用工具**：`Glob`、`Grep`、`Read`、`WebFetch`、`WebSearch`

## Task 工具参数

使用 `Task` 工具启动 subagent 时，需要以下参数：

| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `description` | ✅ | string | 简短的任务描述（3-5词） |
| `prompt` | ✅ | string | 详细的任务提示词 |
| `subagent_type` | ✅ | string | subagent 类型（见上表） |
| `model` | ❌ | string | 使用的模型（sonnet/opus/haiku） |
| `resume` | ❌ | string | 恢复已运行的 agent ID |
| `run_in_background` | ❌ | boolean | 在后台运行 |
| `max_turns` | ❌ | integer | 最大轮次限制 |

## 使用场景

### 1. 何时使用 Subagent

> [!success] 应该使用 Subagent 的情况
> - **开放式搜索**：需要多轮搜索才能找到匹配
> - **代码库理解**：理解代码库如何工作
> - **复杂多步骤任务**：需要协调多个操作
> - **并行执行**：同时启动多个 agent 并行工作

> [!warning] 不应该使用 Subagent 的情况
> - **读取特定文件**：直接使用 `Read` 工具更快
> - **搜索特定类定义**：使用 `Glob` 更快
> - **特定文件内容搜索**：使用 `Read` 或 `Grep` 更快

### 2. 并行执行示例

```python
# 同时启动多个并行任务
Task(
    subagent_type="general-purpose",
    description="搜索认证逻辑",
    prompt="查找处理用户认证的代码文件"
)

Task(
    subagent_type="explore",
    description="探索 API 结构",
    prompt="探索 API 端点的实现"
)
```

### 3. 后台运行示例

```python
# 在后台运行任务
Task(
    subagent_type="general-purpose",
    description="分析代码质量",
    prompt="分析整个代码库的代码质量问题",
    run_in_background=True
)
```

使用 `TaskOutput` 检查后台任务的结果。

## 最佳实践

> [!tip] 并行执行
> - 尽可能同时启动多个 agent 以最大化性能
> - 将多个工具调用放在单个消息中
- 依赖任务需串行执行，独立任务可并行执行

> [!tip] 描述和提示词
> - **描述**：保持简短（3-5词），清晰总结任务
> - **提示词**：提供详细上下文，明确告诉 agent 只做研究还是写代码
> - **恢复**：使用 `resume` 参数继续之前的 agent 会话

> [!tip] 选择合适的 subagent
> - 简单命令 → Bash
> - 快速探索 → Explore（指定 thoroughness）
> - 实现规划 → Plan
> - Claude Code 问题 → Claude Code Guide
> - 复杂研究 → General Purpose

## 常见模式

### 模式 1：探索代码库

````markdown
```python
Task(
    subagent_type="explore",
    description="探索项目结构",
    prompt="探索这个项目的代码库结构，找出主要目录和关键文件",
    model="haiku"  # 快速任务使用 haiku
)
```
````

### 模式 2：搜索特定功能

````markdown
```python
Task(
    subagent_type="general-purpose",
    description="搜索错误处理逻辑",
    prompt="在整个代码库中搜索错误处理相关的代码",
    model="sonnet"
)
```
````

### 模式 3：规划实现

````markdown
```python
Task(
    subagent_type="plan",
    description="设计认证系统",
    prompt="为用户认证系统设计实现方案，考虑安全性和可扩展性",
    model="opus"  # 复杂规划使用 opus
)
```
````

## 注意事项

> [!warning] 重要提示
> - Subagent 的输出对用户不可见，需要你将结果返回给用户
> - 使用 `resume` 时，agent 会保留完整的上下文
> - 如果需要多个不同的搜索结果，考虑使用多个并行 agent
> - 对于简单的文件操作，优先使用专用工具而非 Task

## 相关概念

[[Agent Skills]] | [[MCP 服务器]] | [[Claude Code 基础]]
