## 学习笔记大纲：《从零搭建 Agent Harness 工程：项目脚手架与 skills/hooks/subagents/rules/AGENTS 配置实战》

> 笔记类型：实战笔记（动手搭建 + 结构对照）
> 预计总篇幅：约 25 页
> 章节数：9

### 第一章：从空目录开始——先建哪 4 个文件
- **篇幅**：中
- **覆盖要点**：最小入口集合的 4 个文件（根 `CLAUDE.md`、`AGENTS.md`、`.gitignore`、`.claude/settings.json`）；指令加载顺序（托管策略 → `~/.claude/CLAUDE.md` → 项目 `./CLAUDE.md` 或 `./.claude/CLAUDE.md` → `./CLAUDE.local.md`）；`@path` import 机制与递归层级（最深 4 层）；settings 分层（`settings.json` 共享 / `settings.local.json` 个人 / managed 强制）；为什么先建这 4 个文件
- **素材引用**：S1, S2, D
- **代码示例**：有（4 个文件的骨架内容 + 最小目录树）

### 第二章：Skills——往哪放、怎么写
- **篇幅**：中
- **覆盖要点**：skills 放置层级（企业 managed → `~/.claude/skills/` → 项目 `.claude/skills/` → 插件）；目录名即命令名、description 决定自动加载；SKILL.md frontmatter（`allowed-tools`、`context: fork`、`disable-model-invocation`）；按需加载与长参考拆分（`scripts/`、`reference.md`）；manifest.yaml 的一句话职责（本地范本特有）
- **素材引用**：S3, D
- **代码示例**：有（SKILL.md frontmatter 示例 + skills 目录树）

### 第三章：Hooks——事件、退出码与注册
- **篇幅**：中
- **覆盖要点**：注册位置（全局 / 项目 / `settings.local.json` / 插件）；`hooks.<Event>[]` 结构与 handler 键（type/command/args/timeout/async）；生命周期事件（SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/SessionEnd）；退出码语义（0 成功、2 阻塞、其他非零非阻塞）；stdin JSON 输入与 stdout 决策输出；`${CLAUDE_PROJECT_DIR}` 引用与脚本统一放 `.claude/hooks/`
- **素材引用**：S5, D
- **代码示例**：有（settings.json hooks 片段 + 一个极简脚本）

### 第四章：Subagents——收窄工具与上下文隔离
- **篇幅**：中
- **覆盖要点**：agents 层级（托管 settings → `--agents` CLI → 项目 `.claude/agents/` → `~/.claude/agents/` → 插件）；YAML frontmatter + markdown 正文（正文即系统提示词）；name/description/tools/model/permissionMode 字段；子代理上下文干净（只收自身系统提示词，不含完整系统提示词）；调用方式（自然语言 / `@agent-<name>` / `claude --agent` / settings `agent` 字段）
- **素材引用**：S4, D
- **代码示例**：有（一个完整 agent .md 示例）

### 第五章：Rules——一文件一主题与渐进式披露
- **篇幅**：短
- **覆盖要点**：`.claude/rules/` 目录组织；无 `paths` 的常驻加载 vs 带 `paths` frontmatter 的按文件匹配触发；文件命名即主题（如 `testing.md`，可建子目录）；与 CLAUDE.md 的分工；渐进式披露原则（入口只做地图，避免"陈规坟场"）
- **素材引用**：S1, D
- **代码示例**：有（rules 目录树 + frontmatter 片段）

### 第六章：AGENTS.md 体系——canonical source 与跨 runtime 桥接
- **篇幅**：中
- **覆盖要点**：Claude Code 读 CLAUDE.md 不读 AGENTS.md 的矛盾；AGENTS.md 作 canonical source；`@AGENTS.md` import 桥接（Windows 建议 import 而非符号链接）；双套隔离策略；`.codex/` 镜像与 `.agent-sync` 同步的进阶简述
- **素材引用**：S1, D
- **代码示例**：有（CLAUDE.md 中 `@` import AGENTS.md + 双轨目录对照）

### 第七章：常见坑清单
- **篇幅**：短
- **覆盖要点**：7 个坑——CLAUDE.md vs AGENTS.md 双份维护；settings 不随祖先继承（monorepo 每个子包必须自包含）；版本依赖（import v2.1.213+、/subtask v2.1.212+ 等）；强制策略必须 exit 2；skills 命令名来自目录名而非 name；SessionEnd 共享 1.5s 预算；自动记忆（机器本地） vs 项目文件（版本控制）互补
- **素材引用**：S1, S2, S3, S4, S5（对应 §四）
- **代码示例**：无（避坑清单为主）

### 第八章：最小可运行骨架总览
- **篇幅**：短
- **覆盖要点**：完整目录树（从 D 提取精简版）；每个文件一句话职责；从空目录到跑起来的验证步骤；渐进式扩展顺序（实际搭建按 rules → skills → agents → hooks 按需添加，与章节学习顺序不同）；进阶扩展方向（workflow 状态机、manifest 平台注册）
- **素材引用**：D, S1, S2
- **代码示例**：有（最终目录树 + 验证命令）

### 第九章：发布到 Obsidian
- **篇幅**：短
- **覆盖要点**：frontmatter（title/tags/created/updated/status/sources）；Callout 与双链规范；保存位置 `AI学习/Harness工程实战/`；挂载到既有 `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`；不硬编码路径、sources 含特殊字符需加引号
- **素材引用**：D（本 vault 范本 + 意图文件确认的 vault 路径）；此章内容主要来自 Obsidian 输出规范，而非 S1-S5 深度素材
- **代码示例**：无

## 设计决策与待确认点

深度素材 §六 的 4 个开放问题，按"实战笔记 + 上手深度"给出如下建议，请在确认大纲时逐项敲定：

| # | 开放问题 | 建议 | 理由 |
|---|---------|------|------|
| 1 | 纯 Claude Code 还是跨 runtime（.codex/.agent-sync）？ | 以纯 Claude Code 为主干（第 1-7 章）；跨 runtime 只作为第 6 章"进阶延伸"简述，不展开镜像同步脚本细节 | 官方文档 S1-S5 全是 Claude Code；跨 runtime 是本 vault 特有复杂度，与"上手"深度不符 |
| 2 | 是否包含 workflow 状态机（.claude/workflows/ + todo-state.sh）？ | 不纳入正文主体，只在第 8 章"进阶扩展方向"一句话提及 | 属本 vault 自研、官方无对应；任务标题聚焦 skills/hooks/subagents/rules/AGENTS |
| 3 | 是否深入 manifest.yaml（agent-platform/v1）？ | 第 2 章与第 4 章各用一小段说明其职责（声明入口/能力/权限/依赖），不深入 schema | 官方无对应；对纯 Claude Code 骨架非必需 |
| 4 | 笔记粒度？ | 清单 + 每文件骨架级示例内容，不做长参考文档；长参考链接官方文档 | 匹配"上手"深度（能独立搭出骨架） |

## 学习路径说明

### 前置要求
- 已了解 Harness Engineering 基本概念（可先读本 vault `AI学习/01-基础概念/Harness-Engineering-系统治理工程.md`）
- 会用 Claude Code 基础操作（会话、授权、CLAUDE.md 作用）
- 准备一个空的测试目录用于动手搭建；Claude Code 版本满足最低要求（import 需 v2.1.213+，详见第 7 章）
- 对照阅读本 vault `AI学习/DeepSeek-Harness 教程/` 系列

### 学完能做什么
- 从空目录独立搭出最小可用的 harness 工程骨架（CLAUDE.md + AGENTS.md + .claude/settings.json + rules/skills/agents/hooks）
- 能正确放置并编写 SKILL.md、subagent、hooks 配置
- 能识别并避开 7 类常见坑（版本依赖、exit 2、settings 不继承等）
- 能把骨架发布到 Obsidian 并挂载到既有 MOC

### 建议学习顺序
- 按第 1→9 章顺序学习；建议先扫一眼第 8 章的"目标骨架树"再回头逐章搭建
- 第 2-4 章按 skills → hooks → subagents 顺序阅读；实际搭建子目录时按第 8 章提示的 rules → skills → agents → hooks 按需添加
- 每章结束在测试目录动手验证；预计总耗时 3-5 小时（含动手）
