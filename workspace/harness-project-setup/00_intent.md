# 从零搭建 DeepSeek-Harness 工程 - 意图文件

## 基本信息

- **主题**: 从零搭建 DeepSeek-Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战（专门针对 dsh）
- **项目标识**: harness-project-setup
- **创建时间**: 2026-08-16
- **当前阶段**: 阶段 2（方向调整后）
- **输出目标**: obsidian（已确认）
- **Vault 路径**: `D:\Study-Notes`（已确认）
- **笔记目录**: `AI学习/DeepSeek-Harness 教程/Harness工程实战`（已确认，发布前按用户要求移入 DeepSeek-Harness 教程）
- **MOC 路径**: `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`（已确认）

## 学习目标

### 笔记类型
实战笔记（动手搭建 + 结构对照）

### 学习深度
上手（能独立从一个空目录搭建出自己的 DeepSeek-Harness 工程骨架）

### 用户基础
有了解（已学习 DeepSeek-Harness 插件开发/配置体系/Subagent 教程系列；"差不多会了"）

## 研究计划

### 探索方向
1. **dsh 工程目录骨架**：开始一个项目先创建哪些文件（AGENTS.md / CLAUDE.md / .dsh/skills/ / cordis.yml / ~/.dsh/ 用户级），各目录职责与最小集合
2. **Skills 的放置与结构**：skills 放在哪里（`.dsh/skills/` vs `.agents/skills/` vs custom/user/bundled）、SKILL.md 契约、热加载与扫描优先级
3. **Hooks / Subagents / Rules 配置**：cordis.yml hooks 桥接 vs 原生插件、ctx.subagents + SubagentProvider、AGENTS.md/CLAUDE.md 指令体系与 workspaceContext
4. **配置体系**：补丁树（bundle → profile → home → --patch）、Profile vs Agent Preset、bundle 打包

### 重点收集
- **核心概念**: AGENTS.md/CLAUDE.md 指令加载、.dsh/.agents 扫描根、cordis.yml 补丁树、hook 桥接、SubagentProvider、Agent Preset、workspaceContext
- **实战代码**: 一个最小可用的 dsh 工程骨架（目录树 + 每个关键文件的示例内容）
- **常见坑**: patch name 绝对路径、--patch 仓库根解析、hooks 桥接只跑 shell、configPath 进程级、MCP 只桥接 Tools、内置 preset 只读、subagent UNSUPPORTED_CAPABILITY
- **工具链**: DeepSeek-Harness（dsh）、pnpm、Web UI / headless、cordis.yml、@deepseek-ai/dsh-hooks-claude-code、dsh-mcp-client、dsh-tool-subagent

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户明确要求：**不需要从零开始写，根据现有笔记 + 网上资料**；**专门针对 DeepSeek-Harness**（方向调整）。
- 现有笔记来源（本 vault）：
  - `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 与ClaudeCode对照迁移.md`（dsh ↔ Claude Code 对照）
  - `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/{02-配置体系,03-配置实战,05-最小骨架}.md`（配置/骨架实操）
  - `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness Subagent 教程/*`（subagent 开发）
  - `AI学习/DeepSeek-Harness 教程/{是什么,安装与快速上手,常见坑与速查}.md`
- 官方源：deepseek-ai/deepseek-harness 仓库 `AGENTS.md` / `docs/subsystems/skills.md` / `docs/config-catalog.md`。
