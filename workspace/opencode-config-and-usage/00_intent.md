# 配置和使用 opencode - 意图文件

## 基本信息

- **主题**: 配置和使用 opencode（AI 编码工具）
- **项目标识**: opencode-config-and-usage
- **创建时间**: 2026-08-13
- **当前阶段**: 阶段 0
- **输出目标**: Obsidian vault（具体路径待阶段 6 确认）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记（以安装配置 + 常用命令 + 实际场景操作为主）

### 学习深度
精通（深入配置细节、权限模型、高级定制）

### 用户基础
熟悉（熟练使用 Claude Code，深入了解其配置与使用，正在转向 opencode）

## 研究计划

### 探索方向
以「Claude Code → opencode 迁移」为主线，突出概念对照：
1. opencode 是什么、核心概念与架构（CLI、provider、Agent 模式），与 Claude Code 的整体定位对比
2. 安装与初始化配置：opencode 的配置文件体系，与 Claude Code（settings.json / CLAUDE.md）的对应关系
3. 常用命令与日常工作流：交互/非交互模式、Slash 命令、模型选择、多文件编辑，映射 Claude Code 常用命令
4. 高级定制与进阶：自定义 provider/模型、权限系统、MCP、Skills/AGENTS 等机制与 Claude Code 的差异
5. 常见坑与故障排查：认证、token 消耗、权限误配，以及从 Claude Code 迁移时的典型差异与坑

### 重点收集
- **核心概念**: opencode CLI、provider 配置、agent 模式、权限模型、config 文件体系
- **实战代码**: 安装命令、配置文件示例（opencode.json / config）、常用命令速查
- **常见坑**: 模型 API 认证失败、token 消耗控制、权限误配、与 Claude Code/Codex 的差异
- **工具链**: opencode 生态（LSP、MCP 集成、TUI、Git 工作流）

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户非常熟悉 Claude Code 的配置与使用，笔记主线是「Claude Code → opencode 迁移」，大量使用概念对照，帮助快速上手。
- 学习深度为精通，但重点放在 opencode 特有机制与和 Claude Code 的差异上，不重复讲解已有 AI 编码工具常识。
- 目标输出为 Obsidian 笔记，阶段 6 前需确认 vault_path 与 note_folder。
