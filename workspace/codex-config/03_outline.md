## 学习笔记大纲：《Codex 完整配置体系 —— 与 Claude Code 对照》

> 笔记类型：综合笔记（概念对比 + 实操配置）
> 预计总篇幅：中（约 25-35 页）
> 章节数：8 章 + 附录

### 第一章：从 Claude Code 到 Codex —— 配置哲学概览

> 本章帮助读者建立 Codex 配置体系的整体心智模型，理解其与 Claude Code 的对应关系和核心差异。

- **篇幅**：中
- **覆盖要点**：Codex vs Claude Code 整体对照、配置格式差异（TOML vs JSON）、配置层级与优先级、配置文件目录结构对比
- **素材引用**：#1, #9
- **代码示例**：有（配置层级示例 TOML 片段）

### 第二章：核心配置 —— config.toml 全面解读

> 详细解析 Codex 的核心配置文件 config.toml，对照 Claude Code 的 settings.json，涵盖安全模型、模型配置、多环境配置档等关键维度。

- **篇幅**：长
- **覆盖要点**：配置层级与优先级（五层）、sandbox_mode 沙箱模式、approval_policy 审批策略、Permissions 权限系统、Profiles 多环境配置档、Model 配置与多提供商、Features 功能开关、Shell 环境策略、项目信任机制、安全限定（静默忽略规则）
- **素材引用**：#1
- **代码示例**：有（完整的 config.toml 配置示例）

### 第三章：指令与规则 —— AGENTS.md 分层体系

> 深入 Codex 的指令文件系统，对比 Claude Code 的 CLAUDE.md，重点介绍分层级联机制和 Starlark 规则系统。

- **篇幅**：中
- **覆盖要点**：AGENTS.md 发现机制与分层级联、与 CLAUDE.md 的兼容（fallback）、容量限制与最佳实践、特殊段落（Code Review / Working Agreements）、Starlark 规则系统（.codex/rules/*.rules）、验证工具（codex status / --cd）
- **素材引用**：#2, #4, #9
- **代码示例**：有（AGENTS.md 结构、Starlark 规则片段、验证命令）

### 第四章：Skills 技能系统 —— 创建、注册与共享

> 全面对比 Codex 与 Claude Code 的技能系统，讲解 Skills 目录结构、发现路径、加载机制及跨工具共享方案。

- **篇幅**：长
- **覆盖要点**：Skills 目录结构（SKILL.md + scripts/references/assets/agents）、Frontmatter 元数据规范、发现路径（REPO/USER/ADMIN/SYSTEM/Plugin）、渐进式延迟加载机制、启用/禁用配置、agents/openai.yaml 扩展（Codex 特有）、Skill 共享方案（符号链接 + 独立仓库）、Codex vs Claude Code Skills 关键差异
- **素材引用**：#3, #9, #10
- **代码示例**：有（SKILL.md 示例、config.toml 禁用示例、共享方案命令）

### 第五章：Agents 子代理与 MCP 服务配置

> 讲解 Codex 的两种扩展机制：子代理系统（Agents）和模型上下文协议（MCP），对比 Claude Code 的对应实现。

- **篇幅**：中
- **覆盖要点**：Agents 配置路径与 TOML 定义格式、内置代理（default/worker/explorer）、全局代理设置、Codex vs Claude Code Agents 对比、MCP 配置位置与传输方式（STDIO / Streamable HTTP）、MCP 审批模式与参数详解、Codex vs Claude Code MCP 对比
- **素材引用**：#4, #5, #9
- **代码示例**：有（agent.toml 定义、MCP 服务器配置示例）

### 第六章：Hooks 生命周期钩子与插件体系

> 详解 Codex 的 11 种生命周期钩子事件和插件系统，对比 Claude Code 的 4 种核心钩子，展示更精细化的自动化能力。

- **篇幅**：长
- **覆盖要点**：Hooks 配置文件与合并规则、11 种事件类型详解（含触发时机与 Matcher）、钩子决策能力（PreToolUse 放行/拒绝/重写等）、stdin/stdout 协议细节、启用与安全管理、Codex vs Claude Code Hooks 对比、插件体系结构、plugin.json 关键字段、插件 vs MCP 扩展对比
- **素材引用**：#6, #7, #9
- **代码示例**：有（hooks.json 配置、命令行注册、plugin.json 结构）

### 第七章：CLI 与调试 —— 日常操作与故障排查

> 介绍 Codex CLI 的核心命令、环境变量配置以及日常调试技巧，帮助读者高效使用和排查 Codex 配置。

- **篇幅**：短
- **覆盖要点**：核心 CLI 命令（exec / status / profile / mcp add）、交互式命令（/skills /hooks /config）、环境变量（CODEX_HOME / OPENAI_API_KEY / .env）、调试与验证方法、配置审计技巧
- **素材引用**：#8, #10
- **代码示例**：有（CLI 命令使用示例）

### 第八章：完整对照表与从 Claude Code 迁移实战

> 整合所有配置维度的完整对照表，并给出从 Claude Code 到 Codex 的迁移策略与步骤，辅以常见陷阱和最佳实践。

- **篇幅**：中
- **覆盖要点**：Codex vs Claude Code 完整对照表（18+ 配置维度）、迁移四步走策略（指令兼容、技能共享、权限转换、逐个迁移）、常见陷阱 6 条（静默忽略、网络权限、安全组合等）、Skills 最佳实践 5 条、典型项目配置示例
- **素材引用**：#9, #10
- **代码示例**：有（迁移配置示例、完整项目 config.toml 样板）

### 附录：快速参考卡片

> 方便日常速查的配置速查表，包含配置文件路径、常用命令速记、配置项默认值速查。

- **篇幅**：短
- **覆盖要点**：配置文件路径速查、常用 CLI 命令速记、关键配置项默认值一览
- **素材引用**：#1, #8, #9
- **代码示例**：无

## 学习路径说明

### 前置要求
- 熟悉 Claude Code 的基本配置（settings.json、CLAUDE.md、Skills 概念）
- 有至少一次 Claude Code 的实际使用经验
- 了解基本的 JSON / TOML 格式

### 学完能做什么
- 独立完成 Codex 的完整配置，从全局配置到项目级配置
- 理解 Codex 与 Claude Code 每个配置维度的对应关系，能在两者间自如切换
- 编写和注册自定义 Skills，实现 Roo/Claude Code 间的技能共享
- 配置 MCP 服务器和 Hooks 自动化流程
- 安全配置 sandbox 权限和审批策略，避免常见陷阱
- 将已有的 Claude Code 配置体系迁移到 Codex

### 建议学习顺序
1. **第一章**（概览认知，15 分钟）→ **第二章**（核心配置，30 分钟）→ 建立基础
2. **第三章**（指令与规则，20 分钟）→ **第四章**（Skills 系统，30 分钟）→ 掌握行为控制
3. **第五章**（Agents + MCP，20 分钟）→ **第六章**（Hooks + 插件，25 分钟）→ 掌握扩展机制
4. **第七章**（CLI + 调试，15 分钟）→ 日常操作
5. **第八章**（对照表 + 迁移，20 分钟）→ 收尾与综合应用
6. **附录**（速查表，按需使用）

总计约 3-4 小时可完整学完，各章可按需跳跃阅读。
