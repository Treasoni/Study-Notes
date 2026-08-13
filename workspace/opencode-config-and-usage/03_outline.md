# 配置和使用 opencode - 大纲

> 笔记类型：实战笔记（安装配置 + 常用命令 + 实际操作场景为主）
> 学习深度：精通
> 用户基础：熟悉（熟练使用 Claude Code，正在迁移 opencode）
> 主线：Claude Code → opencode 迁移（大量概念对照，不重复 AI 编码工具常识）
> 结构模式：环境搭建（第 1-3 章）→ 核心功能（第 4-5 章）→ 进阶优化（第 6-8 章）→ 运维排错（第 9 章）
> 预计总篇幅：中长篇（9 章：2 长 / 5 中 / 2 短）
> 章节数：9

## 第一章：opencode 是什么——定位、架构与 Claude Code 全面对比

- **篇幅**：中
- **覆盖要点**：opencode 定位与核心卖点（MIT 开源、模型与框架解耦）、客户端/服务器架构（TUI/桌面/IDE/远程会话）、内置双 Agent（build/plan）与子代理、LSP 回喂 + Git 快照安全网、与 Claude Code 整体对比表逐维度解读、同模型实测数据、"速度 vs 彻底"的取舍、逐步路由控成本思路
- **素材引用**：#1, #2
- **代码示例**：无

### 定位与核心卖点
### 客户端/服务器架构与三种界面（TUI / 桌面 / IDE）
### 内置双 Agent：build（全权限）与 plan（只读）
### 与 Claude Code 的整体对比表与实测结论

## 第二章：安装、升级与认证——从零到能跑

- **篇幅**：中
- **覆盖要点**：一键脚本安装（目录路径优先级）、各平台包管理器矩阵（npm/brew/scoop/choco/pacman/Nix）、升级与卸载（`upgrade`/`uninstall`，保留配置与数据参数）、认证方式（`auth login/list/logout`、凭据存储路径、TUI 内 `/connect`）、服务端认证密码、`opencode models` 查看模型列表、Anthropic OAuth 限定 Claude Code 的提醒
- **素材引用**：#3, #5
- **代码示例**：有（安装命令 + 认证命令）

### 安装：一键脚本与包管理器矩阵
### 升级与卸载（保留配置 / 数据 / dry-run）
### 认证方式与凭据存储
### 模型列表查看与 Anthropic OAuth 限制

## 第三章：配置体系 opencode.json——从 settings.json 迁移

- **篇幅**：长
- **覆盖要点**：JSON/JSONC 格式与 `$schema`、8 层配置优先级（合并而非替换）、核心配置键逐个讲解（`model`/`small_model`、`provider`、`agent`、`command`、`permission`、`tools`、`mcp`、`plugin`、`instructions` 等）、变量替换 `{env:}`/`{file:}`、基础配置示例逐行解读、与 Claude Code `settings.json`/`CLAUDE.md` 的配置映射关系
- **素材引用**：#4
- **代码示例**：有（opencode.json 配置示例）

### 配置格式与 8 层优先级
### 核心配置键逐个讲解
### 变量替换：{env:VAR} 与 {file:path}
### 基础配置示例与 Claude Code 配置迁移映射

## 第四章：常用命令与工作流——Claude Code 命令对照速查

- **篇幅**：长
- **覆盖要点**：TUI 交互模式启动与消息语法（`@` 附加文件 / `!` 执行 shell）、内置 slash 命令速查表（`/init` `/new` `/sessions` `/compact` `/undo` `/models` `/connect` `/share` `/export` 等）、非交互 run 模式（`--format json`/`--agent`/`-m`/`-f`/`--auto` 等）、服务与远程模式（`serve`/`web`/`attach`/`acp`/`github`）、会话与统计（`session`/`stats`/`agent create`）、opencode ↔ Claude Code 完整命令对照表
- **素材引用**：#6, #7
- **代码示例**：有（run 命令、slash 命令、serve/web 命令）

### TUI 交互模式与消息语法（@ / !）
### 内置 slash 命令速查表
### 非交互 run 模式与 CI（--format json / --auto）
### 服务与远程模式（serve / web / attach / acp / github）
### 会话、统计与 agent 管理
### opencode ↔ Claude Code 命令对照表

## 第五章：权限系统——从"默认询问"到"默认允许"

- **篇幅**：中
- **覆盖要点**：三值模型 allow/ask/deny、三层语法（字符串 / 对象 / 带通配符对象）、last matching rule wins 规则、15 个权限键盘点、默认权限基线（宽松、`.env` 默认 deny、`doom_loop`/`external_directory` 默认 ask）、收紧默认权限示例、`--auto` 与 CI 自动批准、Agent 级权限优先级、与 Claude Code 权限模型（数组式、deny 优先）的差异
- **素材引用**：#8
- **代码示例**：有（permission 配置示例）

### 三值模型与三层语法
### 15 个权限键与默认权限基线盘点
### 收紧默认权限与 CI 自动批准
### 与 Claude Code 权限模型的差异

## 第六章：自定义 provider 与模型路由

- **篇幅**：短
- **覆盖要点**：自定义 OpenAI 兼容 provider 配置示例、provider 引用格式（`provider-id/model-id`）、`npm` 与 `baseURL` 关键约束、`/connect` 图形化认证备选、多模型逐步路由控成本（规划/批量编辑/分诊用不同模型）、模型不出现的排查要点
- **素材引用**：#9, #2（成本路由部分）
- **代码示例**：有（自定义 provider 配置示例）

### 自定义 OpenAI 兼容 provider 示例
### npm 与 baseURL 关键约束
### /connect 认证备选与多模型路由控成本

## 第七章：MCP 集成——把外部工具接进来

- **篇幅**：中
- **覆盖要点**：`mcp` 配置键（对应 Claude Code 的 `mcpServers`）、local（STDIO）与 remote（HTTP/SSE）两种类型配置、`command` 用数组与 `environment` 键、OAuth 三种模式（自动发现 / 预注册 / 禁用）、token 存储位置、`opencode mcp` 子命令族（list/debug/auth/logout）、与 Claude Code MCP 的差异
- **素材引用**：#10
- **代码示例**：有（local / remote MCP 配置示例）

### mcp 配置键与两种类型（local / remote）
### command 数组与 environment 环境变量
### OAuth 三种模式与 token 存储
### mcp CLI 子命令族与 Claude Code 差异

## 第八章：Skills、自定义 Agent 与 AGENTS.md

- **篇幅**：中
- **覆盖要点**：`AGENTS.md` 原生加载（对应 `CLAUDE.md`）、SKILL.md 六个发现位置（项目/全局 × opencode/claude/agents）、SKILL.md frontmatter 字段（name/description/license/compatibility/metadata）、`skill()` 调用语法与权限、自定义 Agent（Markdown 文件定义 / `agent create`）、hooks 仅支持 4 个共享 hook、跨工具复用思路（spine 适配器）
- **素材引用**：#11
- **代码示例**：有（skill 调用语法、SKILL.md 结构）

### AGENTS.md 原生加载（与 CLAUDE.md 对应）
### SKILL.md 发现顺序与 frontmatter
### skill 调用语法与权限
### 自定义 Agent 与 hooks 限制
### 跨工具复用（Claude Code / OpenCode / Cursor / Codex）

## 第九章：常见坑与故障排查

- **篇幅**：短
- **覆盖要点**：认证失败根因（`{env:VAR}` 空串破坏 auth.json 回退，issue #34388）、模型不出现的排查清单、常见配置坑（baseURL/npm 配错、密钥含换行、`{env:}` 与 auth.json 双写冲突、版本回归降级处理）、Anthropic OAuth 限定提醒、从 Claude Code 迁移的典型差异提醒
- **素材引用**：#12
- **代码示例**：无

### 认证失败：{env:VAR} 空串破坏 auth.json 回退
### 模型不出现的排查清单
### 常见配置坑与版本回归
### 从 Claude Code 迁移的差异提醒

---

## 素材缺口提示

以下内容在 02_deep_research.md 中仅有名称/概述，写对应章节时可能需要补充：

- **MCP**：官方 MCP 文档原始 URL 404，素材用 OpenCode-Book 8.4 补充；如需更细的 OAuth 流程细节可再补官方 docs。
- **Skills**：缺少一个完整的最小 SKILL.md 示例文件（只有发现顺序 + frontmatter 字段 + 调用语法），写第 8 章时可补一个最小示例。
- **配置键**：`server`、`shell`、`snapshot`、`autoupdate`、`share`、`formatter`、`lsp`、`compaction`、`experimental` 等仅有键名无展开说明，如用户需要可补充。
- **桌面版**：仅提及是 BETA，未展开桌面 app 用法；如用户会使用桌面端可补充。

## 学习路径说明

### 前置要求
- 熟练使用 Claude Code，理解其 `settings.json`、`CLAUDE.md`、权限弹窗、MCP 与 Skills 的基本概念
- 具备基础终端/命令行操作能力，熟悉环境变量与 shell 配置
- 能阅读 JSON/JSONC 配置文件，理解简单的通配符匹配规则
- 有一个可用的 LLM API key（Anthropic / OpenAI 兼容均可）

### 学完能做什么
- 完成 opencode 的安装、升级、认证与日常维护
- 将现有 Claude Code 配置体系（settings.json / CLAUDE.md / MCP / Skills）系统迁移到 opencode
- 熟练使用 TUI 交互模式与 `opencode run` 非交互模式，并在 CI 中集成
- 按需收紧/定制权限模型，理解并复现 opencode 与 Claude Code 的权限差异
- 接入任意 OpenAI 兼容 provider 与 MCP server，配置多模型路由控制成本
- 编写/复用 Skills 与自定义 Agent，实现跨工具迁移复用
- 能独立诊断认证失败、模型不出现、配置误配等常见问题

### 建议学习顺序
- **第 1-2 章（约 0.5-1 天）**：先建立定位认知，跑通安装与认证，形成可运行环境
- **第 3-4 章（约 1-1.5 天）**：核心迁移——配置体系迁移 + 命令工作流对照，把 Claude Code 的日常操作翻译到 opencode
- **第 5-8 章（约 1-2 天）**：进阶定制——权限、自定义 provider、MCP、Skills/Agent，按实际需求选读
- **第 9 章（约 0.5 天）**：排错清单，建议迁移过程中随用随查，不必一次性读完

> 各章建议按顺序阅读（第 3、4 章依赖第 2 章的可运行环境；第 5-8 章相对独立可穿插）。实际总耗时约 3-5 天，视日常使用节奏而定。
