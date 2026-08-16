## 学习笔记大纲：《从零搭建 DeepSeek-Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战》

> 笔记类型：实战笔记（动手搭建 + dsh ↔ Claude Code 结构对照）
> 预计总篇幅：约 22-26 页
> 章节数：8
> 目标读者：已会 Claude Code 扩展、已读 dsh 插件开发/配置体系/Subagent 教程的"有了解"用户

### 第一章：先从心智模型开始——dsh 工程和 Claude Code 工程差在哪
- **篇幅**：中
- **覆盖要点**：dsh = `Model + Harness = Agent` 的可组装运行时；"一切皆插件"、无特权核心（vs Claude Code 单体核心+扩展）；写能力 = 写 TypeScript 代码，`cordis.yml` patch 只是装载手段；"使用 dsh" vs "开发 dsh 插件" 两条路线的分野（决定后面所有文件放哪）
- **素材引用**：D5（是什么）、B1
- **代码示例**：无（心智对照表 + 路线决策表）

### 第二章：开始一个项目——先创建哪些文件
- **篇幅**：中
- **覆盖要点**：两条路线的最小文件集
  - 只用 dsh：`npx @deepseek-ai/dsh web` + Web UI 首配（API Key + workspace），项目根只需一个 `AGENTS.md`（或直接复用 CLAUDE.md）
  - 要写插件/自定义 hooks/mcp：源码路径（clone → `pnpm install` → `pnpm run build`）+ 最小插件 2 文件（`src/index.ts` + `dev-cordis.patch.yml`）
  - 目录职责总览：`AGENTS.md`/`CLAUDE.md`（指令）、`.dsh/skills/`（项目技能）、`cordis.yml`（hooks/mcp/自定义插件配置）、`~/.dsh/`（用户级 harness home：AGENTS.md/skills/profiles/.agent-presets）
- **素材引用**：D5（安装/最小骨架）、B3、D1
- **代码示例**：有（最小目录树 + 两个文件的骨架内容）

### 第三章：Rules/指令体系——AGENTS.md、CLAUDE.md 与 workspaceContext
- **篇幅**：中
- **覆盖要点**：`instructionFileCandidates` 默认 `['AGENTS.md','CLAUDE.md']` 零迁移；项目根 = 最近含 `.git` 的祖先，逐目录向上加载；本地覆盖 `AGENTS.local.md`/`CLAUDE.local.md`；用户级 `~/.dsh/AGENTS.md`；`workspaceContext` 配置（`maxBytes` 字节预算、`projectRootMarkers`、设 `false` 关闭 = hermetic prompts）；官方仓库自身 `CLAUDE.md` symlink `AGENTS.md` 的惯例
- **素材引用**：B3、D1、B1
- **代码示例**：有（cordis.yml workspaceContext 片段 + AGENTS.md 最小样例）

### 第四章：Skills——往哪放、怎么写、扫描优先级
- **篇幅**：中
- **覆盖要点**：六个扫描根 rank 表（`.dsh/skills` 100 → `.agents/skills` 200 → custom 300 → user-dsh 400 → user-agents 500 → bundled 600），first-wins；目录 bundle `<name>/SKILL.md` 或单文件 `<name>.md`，kebab-case 命名，不支持嵌套递归发现；frontmatter 只强两键（`disable-model-invocation`/`user-invocable`）；热加载（watcher + 模型侧 `skill({name})` 工具按需读正文，渐进式披露）；把现成 Claude Code skills 复制过来的迁移清单
- **素材引用**：B2、D1
- **代码示例**：有（最小 SKILL.md + 迁移命令 `cp -r ~/.claude/skills/* .dsh/skills/`）

### 第五章：Hooks——桥接复用 vs 原生插件
- **篇幅**：中
- **覆盖要点**：hook ⊂ 插件的心智；桥接插件 `@deepseek-ai/dsh-hooks-claude-code`（`configPath` 指向 hooks.json、`projectDir` 注入 `${CLAUDE_PROJECT_DIR}`、支持 SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/SubagentStart/SubagentStop；**只跑 shell command**、`configPath` 进程级两个坑）；原生 cordis 插件监听 `tools/pre-execute` 等扩展点（返回 deny/next、更强大）；选择建议 + cordis.yml 落点三层（试跑 `--patch` / profile / home）
- **素材引用**：D1、B3
- **代码示例**：有（桥接插件 cordis.yml 片段 + 原生 hook 的 `ctx.on` 代码）

### 第六章：Subagents——ctx.subagents 与 SubagentProvider（指路+关键契约）
- **篇幅**：短-中
- **覆盖要点**：Claude Code `.claude/agents/*.md` 自动发现 vs dsh `ctx.subagents.registerProvider` 显式注册；provider 契约五块（name/capabilities 四 flag/inheritsParentContext/start/prepareContinuable）；现成 provider 选型（spawn/fork/acp/dsh-sdk）；`dsh-tool-subagent` 暴露给模型 + maxDepth 默认 3；3 个核心坑（UNSUPPORTED_CAPABILITY、outputSchema 不保证、inheritsParentContext 名不副实）；**指向 vault 既有 Subagent 分册**做深度展开
- **素材引用**：D4、D1（桥接表）
- **代码示例**：有（注册 provider 最小代码 + provider 选型速查表）

### 第七章：配置体系与常见坑清单
- **篇幅**：中
- **覆盖要点**：补丁树四层（bundle → profile `cordis.patch.yml` → home `$DSH_HOME/cordis.patch.yml` → `--patch`），"Later layers win per row"整行替换不做深合并，`--dump-config` 排查；Profile（装哪些 bundle）vs Agent Preset（会话用什么能力），preset 即目录（`~/.dsh/.agent-presets/<id>/`）、内置 standard/code/cordis/minimal、自定义=复制改；MCP 每 server 一实例（`mcp__<serverName>__<tool>`，只桥接 Tools）；坑清单汇总（patch name 绝对路径、--patch 仓库根解析、hooks 桥接只跑 shell、configPath 进程级、内置 preset 只读、同名第三方包、developer preview 破坏性变更）
- **素材引用**：D2、D3、B3、D5
- **代码示例**：有（补丁树图示 + cordis.yml 配置片段 + preset 目录树）

### 第八章：最小可运行骨架总览 + 发布到 Obsidian
- **篇幅**：短
- **覆盖要点**：完整目录树（从 D1-D5 提取精简版）+ 每文件一句话职责 + 从空目录到跑起来的验证步骤（`pnpm dsh web` → Web UI 首配 → 会话跑通 / headless 退出码 0/1）+ 渐进式扩展顺序；Obsidian 发布：frontmatter（title/tags/created/updated/status/sources）、Callout/双链规范、保存位置 `AI学习/Harness工程实战/`、挂载到 `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`
- **素材引用**：D5、D1-D3；本章发布部分来自 Obsidian 输出规范 + 意图文件确认的 vault 路径
- **代码示例**：有（最终目录树 + 验证命令）

## 设计决策与待确认点

深度素材 §六 的 4 个开放问题，按"实战笔记 + 上手深度 + dsh 专属"给出如下建议，请在确认大纲时逐项敲定：

| # | 开放问题 | 建议 | 理由 |
|---|---------|------|------|
| 1 | 笔记定位是"使用 dsh 的工程脚手架"还是"写 dsh 插件"？ | **以"使用 dsh 的工程脚手架"为主干**（项目里建 AGENTS.md/.dsh/skills/cordis.yml 配 hooks/mcp/subagent）；写插件只作为第二章"要自定义时的分支"简述，深挖指路既有插件开发分册 | 你的问题问的是"开始一个项目先建哪些文件"，是工程脚手架视角；写插件细节 vault 已有完整分册 |
| 2 | subagent 是否单独成章展开？ | **第六章"短-中篇幅"**，讲清 dsh 版契约与选型速查 + 指路 vault Subagent 分册，不重复深挖 | 你的问题点名要 subagent；但 vault 已有 7 章分册，笔记做"工程骨架怎么挂 + 关键契约"即可 |
| 3 | 是否保留"对照 Claude Code 迁移表"贯穿？ | **保留为每章的小节/速查**（每节 dsh 配置 ↔ Claude Code 等价物），体现你 vault 笔记的风格 | 你是从 Claude Code 迁移过来的用户，对照表是最大加速器 |
| 4 | 笔记粒度？ | 清单 + 每文件骨架级示例内容，不做长参考文档；长参考指路既有 dsh 分册与官方 docs | 匹配"上手"深度（能独立搭出 dsh 骨架） |

## 学习路径说明

### 前置要求
- 已了解 Harness Engineering 基本概念（可先读本 vault `AI学习/01-基础概念/Harness-Engineering-系统治理工程.md`）
- 熟悉 Claude Code 扩展体系（`.claude/skills`、hooks、`.claude/agents`、CLAUDE.md）
- 已读 dsh 基础（`AI学习/DeepSeek-Harness 教程/`：是什么、安装与快速上手、插件开发 01-05、配置实战 03）
- 准备一个空测试目录用于动手搭建；Node `^22.19 || >=24` + pnpm

### 学完能做什么
- 从空目录独立搭出最小可用的 dsh 工程骨架（AGENTS.md + .dsh/skills/ + cordis.yml 配 hooks/mcp）
- 能正确放置并编写 dsh 版 SKILL.md、接入现成 hooks、挂载 subagent provider、理解补丁树配置
- 能识别并避开 dsh 专属常见坑（patch 绝对路径、--patch 仓库根、hooks 桥接限制等）
- 能把骨架发布到 Obsidian 并挂载到既有 DeepSeek-Harness MOC

### 建议学习顺序
- 按第 1→8 章顺序学习；建议先扫一眼第 8 章的"目标骨架树"再回头逐章搭建
- 第 4-6 章按 skills → hooks → subagents 顺序阅读；实际搭建子目录时按第 8 章提示按需添加
- 每章结束在测试目录动手验证；预计总耗时 3-4 小时（含动手）
