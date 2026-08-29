# Hermes 的规则配置 - 意图文件

## 基本信息

- **主题**: Hermes 的规则配置（rules / CLAUDE.md 这类如何配置）
- **项目标识**: hermes-rules-config
- **创建时间**: 2026-08-30
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: AI学习/Hermes Agent/
- **MOC 路径**: AI学习/Hermes Agent/Hermes Agent MOC.md

## 学习目标

### 笔记类型
实战笔记（实战配置指南）

### 学习深度
上手（能实际在 Hermes 中配置好 rules / CLAUDE.md 这类规则文件并验证生效）

### 用户基础
有了解（用过 Claude Code，熟悉 CLAUDE.md、.claude/rules、settings.json、hooks 分层配置）

## 研究计划

### 探索方向
1. Hermes 的规则配置入口文件（类似 Claude Code CLAUDE.md 的对应物，如 AGENTS.md / config 文件）
2. rules 分层与加载机制（项目级、用户级、目录级规则如何组织与合并）
3. 与 Claude Code 配置体系的对照迁移（CLAUDE.md → ?、.claude/rules/ → ?、settings.json → ?、hooks → ?）
4. 实战配置示例与验证方法（如何在 Hermes 中确认规则已加载生效）

### 重点收集
- **核心概念**: Hermes 规则系统、规则文件命名与格式、加载优先级/合并顺序、作用域
- **实战代码**: 具体规则配置示例、目录结构、验证命令
- **常见坑**: 规则未生效、路径作用域、覆盖顺序、与内置默认规则冲突
- **工具链**: Hermes CLI 相关命令、配置文件位置、生态工具

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户已用过 Claude Code，讲解时以 CLAUDE.md / .claude/rules 为对照锚点效率更高。
- 可复用已有笔记：`AI学习/Hermes Agent/Hermes Agent 上手实战.md`、`AI学习/Hermes Agent/Hermes Tool 配置指南/`。
- 最终按 Obsidian 规范发布到 `AI学习/Hermes Agent/` 并同步 Hermes Agent MOC。
