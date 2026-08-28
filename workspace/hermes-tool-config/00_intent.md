# hermes 的 tool 如何配置 - 意图文件

## 基本信息

- **主题**: hermes 的 tool 如何配置（Hermes Agent 工具/技能配置）
- **项目标识**: hermes-tool-config
- **创建时间**: 2026-08-28
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目
- **笔记目录**: AI学习/Hermes Agent
- **MOC 路径**: AI学习/Hermes Agent/Hermes Agent MOC.md

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手实战

### 用户基础
有了解（已用 Docker 跑过 Hermes，已有《Hermes Agent 上手实战》分册）

## 研究计划

### 探索方向
1. Hermes 内置工具体系（web 搜索、代码执行、文件操作等）与启用/禁用
2. Tool Gateway 与工具权限配置
3. 自定义工具开发与注册
4. 技能（Skills）与工具的关系、MCP 接入

### 重点收集
- **核心概念**: tool vs skill 边界、Tool Gateway、工具权限、tool-call 迭代
- **实战代码**: 配置 yaml 示例、自定义 tool 注册代码、Docker 场景命令
- **常见坑**: 工具未启用、权限不足、context_length、MCP 配置错误
- **工具链**: MCP、agentskills.io 开放标准、OpenClaw 技能可迁移

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 备注

- 与现有《Hermes Agent 上手实战》第 5 章《技能体系》区分定位：第 5 章讲"技能是什么、生命周期"；本笔记专讲"工具怎么配、怎么接"。
- 独立成册，输出到 `AI学习/Hermes Agent/`，最终同步 `Hermes Agent MOC.md`。
