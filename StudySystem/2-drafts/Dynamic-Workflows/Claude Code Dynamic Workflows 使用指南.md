---
type: hybrid
topic: Claude Code Dynamic Workflows
note_types: [concept, cheat_sheet]
difficulty: intermediate
tags: [claude-code, workflows, subagents, automation, ultracode, multi-agent]
created: 2026-06-18
updated: 2026-06-18
sources:
  - R1: "Orchestrate subagents at scale with dynamic workflows (Anthropic, 2026-05-28) https://code.claude.com/docs/en/workflows.md"
  - R2: "Run agents in parallel (Anthropic, 2026) https://code.claude.com/docs/en/agents.md"
  - R3: "Create custom subagents (Anthropic, 2026) https://code.claude.com/docs/en/sub-agents.md"
  - R4: "Extend Claude with skills (Anthropic, 2026) https://code.claude.com/docs/en/skills.md"
  - R5: "Claude Code changelog (Anthropic, 2026) https://code.claude.com/docs/en/changelog.md"
  - R6: "Automate actions with hooks (Anthropic, 2026) https://code.claude.com/docs/en/hooks-guide.md"
  - R7: "Dynamic Workflows community issues & feedback (GitHub, 2026-06) https://github.com/anthropics/claude-code/issues?q=is%3Aissue+ultracode+workflow"
  - R8: "Claude Code overview (Anthropic, 2026) https://code.claude.com/docs/en/overview.md"
  - R9: "Commands reference (Anthropic, 2026) https://code.claude.com/docs/en/commands.md"
concepts:
  - dynamic-workflow
  - subagent
  - ultracode
  - skill
  - slash-command
  - hook
  - agent-team
  - agent-view
  - worktree
related_notes:
  - "[[Claude Code Subagents 完整指南]]"
  - "[[Claude Code Hooks 使用指南]]"
  - "[[Claude Code Slash Commands 完整参考]]"
  - "[[Claude Code 插件系统使用指南]]"
  - "[[如何编写Skills]]"
  - "[[CLAUDE.md 使用指南]]"
  - "[[Claude Code 高级功能]]"
  - "[[Claude-Code-多Agent流程设计]]"
---

# Claude Code Dynamic Workflows 使用指南

> 一份「概念 + 速查」型混合笔记：先建立心智模型，再给出可随时翻查的速查清单。
> 适用对象：已经会用 Claude Code 基础功能，希望了解如何把"多 agent 编排"从一次性操作升级为可复用脚本的学习者。

## 核心概念

### 一句话定义

**Dynamic Workflow** 是一段由 Claude 帮你写的 JavaScript 脚本，由运行时在后台执行，用来同时编排几十到几百个 [[Claude Code Subagents 完整指南|subagent]] 去完成一项超出单次对话协调能力的任务。[来源: R1]

把它类比成现实世界：**subagent** 就像一个能干活的工人；**workflow** 就像一份由总指挥（Claude）写好、交给项目经理（运行时）执行的项目计划书。计划书里写明谁先干、谁后干、怎么汇总——而不是让每个工人在现场临时决定下一步。

### 它诞生的背景

Dynamic Workflows 在 **Claude Code v2.1.154（2026-05-28）** 正式发布，是一次相对晚近的演进。它要解决的核心矛盾是：

- 现有 [[Claude Code Subagents 完整指南|subagent]] 一次会话只能协调「几个」委派任务 [来源: R2]
- 当任务规模变成"500 个文件迁移"或"全代码库审计"时，再让 Claude 在 turn-by-turn 里临时调度，就力不从心了 [来源: R1]
- 解决办法：**把"计划"从 Claude 的上下文里搬出去，搬进一段可读、可重跑、可 diff 的 JS 脚本** [来源: R1]

### 与其它概念的对比：谁在"编排"？

这是理解 Dynamic Workflows 最关键的一张表。每种机制的"调度者"不同，结果也就不同。

| 维度 | [[Claude Code Subagents 完整指南\|Subagents]] | [[如何编写Skills\|Skills]] | Agent Teams | **Dynamic Workflows** |
|---|---|---|---|---|
| 它是什么 | Claude 派生的工人 | 加载到上下文里的指令 | 主 agent 监督的同伴会话 | 运行时执行的脚本 |
| 决定下一步的人 | Claude（turn by turn） | Claude（按提示执行） | 主 agent（turn by turn） | **脚本** |
| 中间结果存哪 | Claude 上下文 | Claude 上下文 | 共享任务列表 | **脚本变量** |
| 可重复的对象 | 工人定义 | 指令本身 | 团队定义 | **编排本身** |
| 规模 | 每轮几个 | 同 subagent | 几个长跑同伴 | **几十到几百个 agent/次** |
| 中断后 | 重启整个 turn | 重启整个 turn | 队友继续跑 | **同一 session 内可恢复** |

[来源: R1][来源: R2]

> 关键洞察：在前三种模式里，**Claude 是编排者**；而 Workflow 把编排权交给了**一段脚本**。Claude 的上下文里只剩下最终答案——所有循环、分支、中间状态都活在脚本里。[来源: R1]

### 核心触发方式

有四种触发方式，由"你希望 Claude 主动多大程度参与规划"决定 [来源: R1][来源: R9]：

1. **运行内置 workflow**：`/deep-research <问题>` —— 内置的 workflow 之一，会扇出多个 web 搜索 agent、交叉验证后输出带引用的报告 [来源: R1][来源: R9]
2. **用关键词触发**：在 prompt 前面加 `ultracode:`（v2.1.160 前叫 `workflow`，现在改为 `ultracode`），输入框里这个关键词会高亮成紫色；Mac 按 `Option+W` / Windows/Linux 按 `Alt+W` 可以取消高亮 [来源: R1][来源: R5]
3. **让 Claude 自己做决定**：`/effort ultracode` —— 开启后每个实质性任务 Claude 都会自动规划一个 workflow；它是会话级开关，新开会话会重置 [来源: R1][来源: R9]
4. **运行已保存的 workflow**：保存到 `.claude/workflows/` 或 `~/.claude/workflows/` 后，会自动出现在 `/` 自动补全里 [来源: R1]

### 运行时特征：隔离、可恢复

Workflow 脚本运行在一个**与你的对话隔离的运行时**里 [来源: R1]：

- 中间结果存在脚本变量里，不进入你的上下文
- 每次运行都会把脚本写到 `~/.claude/projects/` 下
- 运行时跟踪每个 agent 的结果——所以一次失败的 run 可以在同一 session 内恢复
- 在 `/workflows` 视图里能看到每个 phase 的 agent 数量、token 用量、耗时

[来源: R1]

### 关键限制（务必记住）

| 限制 | 原因 |
|---|---|
| **不支持运行中用户输入** | 唯一能暂停 run 的是 agent 权限弹窗；如需阶段间签收，把每个阶段写成独立 workflow [来源: R1] |
| **workflow 本身不能直接读写文件或执行 shell** | 这些都让 agent 做，脚本只负责协调 [来源: R1] |
| **最多 16 个并发 agent** | 约束本地资源 [来源: R1] |
| **每次 run 最多 1000 个 agent** | 防止失控循环 [来源: R1] |

### 保存位置（这是"重跑性"的来源）

Workflow 保存为脚本后，等同于一个可重用的 [[Claude Code Slash Commands 完整参考|slash command]：

- `.claude/workflows/`：项目级，团队共享 [来源: R1]
- `~/.claude/workflows/`：个人级，所有项目可用 [来源: R1]
- v2.1.178 之后：项目级会沿"工作目录到 repo 根"路径上查找最接近的 `.claude/workflows/` [来源: R5]
- 同名冲突时，项目级优先于个人级 [来源: R9]

## 关键要点

这一节把社区和官方文档里最容易被踩的坑、最高的成本信号总结出来。

### 1. 成本风险是真实的（社区共识）

动态编排的本质就是"用 token 换时间和质量"，社区有大量"翻车"案例 [来源: R7]：

- Issue #68285：一次 fan-out 默认继承高价位模型、且无 per-agent 成本上限，造成约 **$1k** 自动续费 [来源: R7]
- Issue #66023：一次调用扇出 46 个 Opus subagent，约 **3M tokens**，且无任何成本确认 [来源: R7]
- Issue #66762：ultracode 模式静默消耗完整 5 小时用量窗口 [来源: R7]
- Issue #67636 / #66867：单次重构任务扇出成百个并行 agent [来源: R7]

### 2. 成本控制的三个明确手段

官方文档里给出了三种应对方法 [来源: R1]：

1. 跑大型 run 前先看 `/model` 确认模型
2. **主动要求 Claude 在不需要最强模型的阶段用更小的模型**（默认会继承父模型，浪费严重）
3. 先在**小切片**上跑一遍再扩大

### 3. Workflow 与相关概念的边界

为了避免和 [[Claude Code Subagents 完整指南|subagents]] / [[如何编写Skills|skills]] / [[Claude Code Hooks 使用指南|hooks]] 混淆，下面这张关系图是关键 [来源: R4][来源: R6][来源: R8]：

| 功能 | 它做什么 | 和 workflow 的关系 |
|---|---|---|
| [[Claude Code Subagents 完整指南\|Subagents]] | 隔离上下文里跑委派任务 | **被编排的对象**（worker primitive）[来源: R3] |
| [[如何编写Skills\|Skills]] | 把可复用提示词装进上下文 | **静态能力注入**，不参与运行时调度 [来源: R4] |
| [[Claude Code Hooks 使用指南\|Hooks]] | 在生命周期事件触发确定性命令 | **控制层**，`PreToolUse` 仍能强制策略 [来源: R6] |
| [[Claude Code Slash Commands 完整参考\|Slash Commands]] | 触发器（`/workflows`、`/deep-research`、`/effort ultracode`） | **入口** [来源: R9] |
| [[CLAUDE.md 使用指南\|CLAUDE.md]] | 持久化项目说明 | **上下文源**，workflow 内的 agent 会读 [来源: R8] |
| Plugins | 打包扩展 | workflow 和 skill 都可来自插件 [来源: R4] |

> 关键边界：[[如何编写Skills|skills]] 跑在前台（在主上下文或 forked subagent 里）；workflow 跑在后台（独立运行时 + 隔离脚本）。**`/deep-research` 是个 workflow，不是 skill**——这是初学者最常踩的分类错误。[来源: R4][来源: R9]

### 4. Workflow 内 agent 的执行模式

无论你当前 session 在什么权限模式：

- workflow 派生的 subagent **始终运行在 `acceptEdits` 模式**[来源: R1]
- 派生 agent **继承 session 的工具白名单**[来源: R1]
- 文件编辑**自动批准**，但 shell / web fetch / 未在白名单的 MCP 工具仍可能中途弹权限 [来源: R1]
- 在 v2.1.172 之前，workflow 内的 subagent **不能**派生嵌套 subagent [来源: R7]

### 5. 关闭 workflow 的三种方法

| 方法 | 作用范围 |
|---|---|
| `/config` 里关 Dynamic workflows | 个人，跨 session 持久 |
| `~/.claude/settings.json` 设 `"disableWorkflows": true` | 个人 |
| `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | 当前环境变量范围 |
| 托管设置里设 `"disableWorkflows": true` | 整个组织 |

关掉后：`ultracode` 关键词失效、`/effort` 菜单里看不到 ultracode、内置 `/deep-research` 不可用 [来源: R1]

### 6. 怎么选正确的"并行方式"？

文档给的决策框架 [来源: R2]：

- **谁协调？**
  - Claude 在对话内调度 → subagents
  - 你自己 hand off 独立任务 → agent view
  - Claude 当 lead 拆项目 → agent teams
  - **脚本持有计划** → dynamic workflows
- **worker 之间要不要对话？**
  - subagent：只回主对话
  - agent view：只回你
  - agent team：共享 task list + 直接互发消息
- **是否改同一批文件？**
  - 必须用 worktree 隔离；subagent / agent view / 5 层嵌套 subagent 都支持
  - agent team 的队友不隔离在 worktree，需要划分"每人管不同文件" [来源: R2]

### 7. 一个实操示例

把 workflow 保存后，它通过 `args` 全局变量接收调用参数（结构化对象，无需自己 parse）[来源: R1]：

```text
> Run /triage-issues on issues 1024, 1025, and 1030
```

脚本里直接用：

```javascript
// args 此时是结构化对象，不是字符串
for (const id of args) {
  await agent({ prompt: `triage GitHub issue #${id}` });
}
```

> 注意：早期版本里 `args` 是 JSON 字符串，社区提供了一个 workaround [来源: R7]：
> `const args = typeof args === 'string' ? JSON.parse(args) : args;`

## 速查清单

> 想快速翻查时看这一节。命令、参数、位置、快捷键都列在这里。

### 触发方式一览

| 触发方式 | 用法 | 备注 |
|---|---|---|
| 内置 workflow | `/deep-research <问题>` | 需要 WebSearch 工具 [来源: R1] |
| 关键词触发 | `ultracode: <任务描述>` | v2.1.160 后；旧版用 `workflow` [来源: R5] |
| 自动模式 | `/effort ultracode` | 会话级；`xhigh` + 自动编排 [来源: R9] |
| 自然语言 | "请用 workflow 做……" | 两个版本都支持 [来源: R1] |
| 已保存 workflow | `/<workflow名> [args...]` | 出现在 `/` 自动补全 [来源: R1] |
| 取消关键词高亮 | `Option+W`（Mac）/ `Alt+W`（Win/Linux） | 取消紫高亮 [来源: R1] |
| 在编辑器里看脚本 | `Ctrl+G` | run 启动前的权限弹窗里 [来源: R1] |

### 监控与控制

| 操作 | 怎么用 |
|---|---|
| 打开 workflow 监控视图 | `/workflows` [来源: R1] |
| 看 subagent | `/agents` [来源: R2] |
| 看后台任务 | `/tasks` [来源: R2] |
| 看后台 session | `claude agents`（agent view）[来源: R2] |
| 进入某个 phase | 在 `/workflows` 里 `Enter` 或 `→` [来源: R1] |
| 返回上一层 | `Esc` [来源: R1] |
| 上下移动 | `↑` / `↓` [来源: R1] |
| 在 phase 内滚动 | `j` / `k` [来源: R1] |
| 暂停 / 恢复 | `p` [来源: R1] |
| 停止 agent（焦点在 agent） | `x` [来源: R1] |
| 停止整个 workflow（焦点在 run） | `x` [来源: R1] |
| 重启选中的运行中 agent | `r` [来源: R1] |
| 把 run 的脚本存为 command | `s` [来源: R1] |
| 调整启动前 prompt | `Tab` [来源: R1] |

### 保存位置速查

| 路径 | 范围 | 适合存什么 |
|---|---|---|
| `.claude/workflows/` | 项目（可提交） | 团队共享 [来源: R1] |
| `~/.claude/workflows/` | 个人 | 跨项目私人脚本 [来源: R1] |
| `~/.claude/projects/` | 每次 run | 脚本副本 + 运行时 journal（可调试缓存 key）[来源: R1][来源: R7] |

### 关键限制

| 限制 | 数值 / 行为 |
|---|---|
| 并发 agent | 16 [来源: R1] |
| 单次 run agent 数 | 1000 [来源: R1] |
| 运行中用户输入 | **不支持**（仅 agent 权限弹窗可暂停）[来源: R1] |
| workflow 自身 IO | **不允许**直接读写文件 / 执行 shell [来源: R1] |
| 派生 agent 模式 | 固定 `acceptEdits` [来源: R1] |
| 嵌套 subagent | 5 层（v2.1.172+）[来源: R5] |

### 关闭 workflow

| 方法 | 范围 | 持久性 |
|---|---|---|
| `/config` 关 | 个人 | 跨 session [来源: R1] |
| `~/.claude/settings.json` 设 `disableWorkflows: true` | 个人 | 文件持久 [来源: R1] |
| `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | 当前 | 临时 [来源: R1] |
| 托管设置 `disableWorkflows: true` | 组织 | 管理员控制 [来源: R1] |

### 版本时间线

| 版本 | 日期 | 变化 |
|---|---|---|
| 2.1.152 | 2026-05-27 | 简化 workflow 行内进度展示 [来源: R5] |
| 2.1.154 | 2026-05-28 | **正式发布 Dynamic Workflows** [来源: R5] |
| 2.1.157 | 2026-05-29 | plugin 在 `.claude/skills` 自动加载 [来源: R5] |
| 2.1.160 | 2026-06-02 | 关键词从 `workflow` 改为 `ultracode` [来源: R5] |
| 2.1.172 | 2026-06-10 | subagent 可派生嵌套 subagent（5 层）[来源: R5] |
| 2.1.178 | — | 项目 workflow 沿"工作目录到根"路径解析 [来源: R5] |

### 与其它功能的关系（一句话版本）

| 相关功能 | 一句话关系 |
|---|---|
| [[Claude Code Subagents 完整指南\|Subagents]] | 被编排的工人 [来源: R3] |
| Agent view | 你手动 hand off 的后台 session [来源: R2] |
| Agent teams | lead 监督 + 共享 task list（实验性，默认关）[来源: R2] |
| [[如何编写Skills\|Skills]] | 提示词注入，跑在前台 [来源: R4] |
| [[Claude Code Hooks 使用指南\|Hooks]] | 生命周期事件，强制策略 [来源: R6] |
| Worktrees | git 隔离，避免并行改同一批文件 [来源: R2] |
| `/batch` | 5–30 个 worktree-isolated subagent 的 skill，不是 workflow [来源: R2][来源: R9] |
| [[CLAUDE.md 使用指南\|CLAUDE.md]] | 上下文源，workflow 内的 agent 也会读 [来源: R8] |

## 思考题

1. **调度者差异**：同样是"派多个 agent 同时做事"，subagents、agent teams、dynamic workflows 在"谁决定下一步"上有什么根本不同？这种差异如何影响"上下文占用"和"可重跑性"？[来源: R1][来源: R2]

2. **成本失控的根因**：为什么一个 workflow 默认会"无意识地烧 token"？从派生 agent 的模式（`acceptEdits` + 继承工具白名单 + 继承父模型）三个角度分析，并给出你作为使用者能采取的三个具体动作。[来源: R1][来源: R7]

3. **workflow vs skill 的本质区别**：明明 `/deep-research` 在 `/` 菜单里、也是 `/xxx` 形式启动，为什么它不是 skill？如果让你把一个"前端代码 review 模板"封装成 skill 还是 workflow，你的判断标准是什么？[来源: R4][来源: R9]

4. **中间结果归属**：workflow 的"中间结果在脚本变量里，不进入 Claude 上下文"这一设计，给你的工作流设计带来什么好处？又带来什么限制（比如"运行中无法用户输入"）？[来源: R1]

5. **错误恢复与可重复性**：v2.1.160 之后 `ultracode` 改名、加上"agent prompt 必须是确定性纯函数以保持 cache key 稳定"这条社区经验，这两件事对"工作流可重跑"这件事意味着什么？[来源: R5][来源: R7]

---

## 参考资料

| # | 标题 | URL | 类型 |
|---|------|-----|------|
| R1 | Orchestrate subagents at scale with dynamic workflows | https://code.claude.com/docs/en/workflows.md | 官方文档 |
| R2 | Run agents in parallel | https://code.claude.com/docs/en/agents.md | 官方文档 |
| R3 | Create custom subagents | https://code.claude.com/docs/en/sub-agents.md | 官方文档 |
| R4 | Extend Claude with skills | https://code.claude.com/docs/en/skills.md | 官方文档 |
| R5 | Claude Code changelog | https://code.claude.com/docs/en/changelog.md | 官方更新日志 |
| R6 | Automate actions with hooks | https://code.claude.com/docs/en/hooks-guide.md | 官方文档 |
| R7 | Dynamic Workflows community issues & feedback | https://github.com/anthropics/claude-code/issues?q=is%3Aissue+ultracode+workflow | 社区反馈 |
| R8 | Claude Code overview | https://code.claude.com/docs/en/overview.md | 官方文档 |
| R9 | Commands reference | https://code.claude.com/docs/en/commands.md | 官方文档 |

## 文档元信息

- **笔记类型**：hybrid (concept + cheat_sheet)
- **章节顺序**（per `templates/hybrid-sections.yaml` 的 `concept + cheat_sheet` 组合）：核心概念 → 关键要点 → 速查清单 → 思考题
- **难度等级**：intermediate（需要先理解 subagent / skill / slash command / hook 的基础概念）
- **学习目的**：兴趣探索 + 入门 + 快速回顾
- **目标读者**：自己
