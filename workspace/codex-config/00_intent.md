# Codex 配置笔记 - 意图文件

## 基本信息

- **主题**: Codex 完整配置体系 — 与 Claude Code 的对照
- **项目标识**: codex-config
- **创建时间**: 2026-07-31
- **当前阶段**: 阶段 0
- **输出目标**: Obsidian vault
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: AI学习/
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
综合笔记（概念对比 + 实操配置）

### 学习深度
上手（能独立配置 Codex 的各项能力，理解与 Claude Code 的对应关系）

### 用户基础
熟悉 Claude Code 的配置方式，想知道 Codex 如何做到类似效果

## 研究计划

### 核心问题
1. **全局配置**: Codex 的 settings.json / codex.json 等配置文件结构是怎样的？与 Claude Code 的 settings.json 有何对应？
2. **Rules 配置**: Codex 的 rules 机制如何工作？与 CLAUDE.md / 项目规则文件有何对应？
3. **Skills 配置**: Codex 的 skills 如何创建、注册、调用？与 Claude Code skills 有何异同？
4. **Agents 配置**: Codex 的 agent 如何定义和配置？subagent 机制是怎样的？
5. **MCP 配置**: Codex 的 MCP 服务器如何配置？与 Claude Code MCP 配置有何差异？
6. **Workflows 配置**: Codex 的工作流如何定义和编排？状态管理机制？
7. **Hooks 配置**: Codex 的自动化钩子/事件系统如何配置？
8. **Platform / Manifest**: manifest.yaml 注册体系和平台配置？
9. **环境变量与路径**: .env、路径解析、运行时环境配置？
10. **CLI 与调试**: Codex CLI 配置命令、调试工具和开发体验？

### 重点收集
- **配置维度对照**: Codex vs Claude Code 每项配置的完整对照表
- **文件结构**: 配置文件目录结构、命名规范、格式差异
- **实战示例**: 一个完整项目的 Codex 配置（含多项配置的综合示例）
- **常见坑**: 各配置维度的易错点和限制
- **调试方法**: 配置验证、日志、故障排查

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- GitHub 示例、配置样板: 是

## 备注

- 笔记面向有 Claude Code 使用经验的读者，重点在配置体系的对照和迁移
- 需要兼顾概念解释和可运行的配置示例
- 配置维度可能包含：settings / rules / skills / agents / MCP / workflows / hooks / platform / env / CLI
