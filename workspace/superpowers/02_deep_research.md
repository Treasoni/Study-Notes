# Superpowers Agentic Skills Framework - 深度素材

> 收集时间：2026-07-23
> 项目：obra/superpowers (v6.1.1, MIT License, 259k+ Stars)
> 作者：Jesse Vincent @ Prime Radiant
> 覆盖方向：7 个

---

## 方向 1：Workflow Pipeline（工作流状态机）

### 7 阶段硬门控状态机

Superpowers 定义一个严格线性的 7 阶段 pipeline，每个阶段之间由二进制门控连接：

```
Phase 1: Brainstorming（头脑风暴）
    │ 门控：设计文档已写 + 用户已审批
    ▼
Phase 2: Git Worktrees（工作区隔离）
    │ 门控：隔离工作区已创建 + 测试基线已通过
    ▼
Phase 3: Writing Plans（编写计划）
    │ 门控：计划文件已保存 + 用户选择执行路径
    ▼
Phase 4a: Subagent-Driven Development（子 Agent 驱动开发，推荐）
    │ 或 Phase 4b: Executing Plans（内联执行，备选）
    │ 门控（每任务）：TDD RED-GREEN-REFACTOR 循环通过
    ▼
Phase 5: TDD（测试驱动开发）—— 内嵌在 Phase 4 的每个任务中
    │ 门控：RED 失败已验证 → GREEN 通过已验证 → REFACTOR 保持绿色
    ▼
Phase 6: Requesting Code Review（代码审查）
    │ 门控：Critical + Important 问题已修复
    ▼
Phase 7: Finishing Branch（分支完成）
    │ 门控：所有测试通过 + 用户选择整合方式
```

### 9 个硬门控（Hard Gates）

| 门控 | 从 → 到 | 条件 |
|------|---------|------|
| G1 | Brainstorming → Writing Plans | 设计文档完成 + 用户审批 |
| G1a | Brainstorming 内 | 每节设计用户审批 → 下一节 |
| G1b | Brainstorming 内 | 书面 spec 用户审批 |
| G2 | Writing Plans → Execution | 计划文件保存 + 用户选路径 |
| G3 | 任务开始 → TDD RED | 无生产代码存在 |
| G4 | RED → GREEN | 测试失败已通过 test runner 验证 |
| G5 | GREEN → REFACTOR | 测试通过已通过 test runner 验证 |
| G6 | 任务完成 → 下一任务 | 代码审查通过（Critical + Important 已修复） |
| G7 | 全部任务完成 → Finishing | 测试通过 |
| G8 | Finishing → Done | 用户选择操作 + merge 后测试通过 |

### 规则强制执行机制

**"1% 规则"**：如果某个技能有 1% 的触发可能，Agent **必须**加载并遵循它。Agent 不能以"太简单"、"让我先看看代码"等理由跳过。

**指令优先级**：用户/项目指令 > Superpowers skills > 默认 system prompt。只有用户明确要求时才能跳过技能流程。

**12 种被预判并屏蔽的合理化借口**：

| Agent 的借口 | 系统的反驳 |
|-------------|-----------|
| "这只是一个简单的问题" | 问题就是任务，先检查技能 |
| "让我先探索代码库" | 技能告诉你如何探索，先检查 |
| "技能是大材小用" | 简单的事情会变得复杂，使用它 |
| "我记得这个技能" | 技能在进化，阅读当前版本 |
| "我知道那是什么意思" | 知道概念≠使用技能，调用它 |

### 关键源码参考

- `skills/brainstorming/SKILL.md` — 9 步严格流程，每步有门控
- `skills/writing-plans/SKILL.md` — 任务粒度 2-5 分钟，禁止 TODO/TBD 占位符
- `skills/test-driven-development/SKILL.md` — 铁律：无失败测试则无生产代码
- `skills/finishing-a-development-branch/SKILL.md` — 合并前验证测试 + 溯源所有权清理

---

## 方向 2：Subagent Dispatching（子 Agent 派发）

### Subagent-Driven-Development (SDD) 核心机制

**每个任务派发全新 subagent + 隔离上下文**，是 Superpowers 的旗舰执行引擎。

### 派发流程

```
Controller (主 Agent)
    │
    ├─ Step 1: scripts/task-brief PLAN_FILE N  →  提取任务 N 到独立文件
    ├─ Step 2: 组装 dispatch prompt（项目上下文 1 行 + brief 路径 + 接口/决策）
    ├─ Step 3: 指定模型（Haiku / Sonnet / Opus）
    └─ Step 4: 派发 subagent
                │
                ▼
            Implementer Subagent
                │
                ├─ DONE → 生成 review package → dispatch reviewer
                ├─ DONE_WITH_CONCERNS → 阅读 concerns，先验证正确性
                ├─ NEEDS_CONTEXT → 补充上下文重新派发
                └─ BLOCKED → 评估原因（上下文缺口/推理缺口/任务太大/计划错误）
```

### 模型分层

| 模型 | 用途 | 成本 |
|------|------|------|
| **Haiku** | 机械性 1-2 文件任务（如"转写 + 测试"） | 最便宜 |
| **Sonnet** | 多文件集成、审查者角色 | 性价比最高 |
| **Opus** | 架构/设计/最终整个分支审查 | 最贵，仅关键环节使用 |

每次派发必须显式指定模型，省略会默认使用会话的昂贵模型。

### v5 → v6 审查流程演进

- **v5**: 每个任务后两次独立审查（spec 合规 + 代码质量）
- **v6**: 合并为一次 diff 通读，同时返回合规性和质量判定
- **v6 新增**: 预飞行计划冲突检查、通过文件传递 diff（减少上下文成本）、最终整个分支审查用最强模型

### Subagent 状态报告协议

| 状态 | 含义 | Controller 动作 |
|------|------|----------------|
| DONE | 任务完成 | 生成 review package，dispatch reviewer |
| DONE_WITH_CONCERNS | 完成但有关注点 | 先读 concerns；正确性疑虑先处理，观察性备注暂记 |
| NEEDS_CONTEXT | 缺少信息 | 补充信息后重新派发 |
| BLOCKED | 无法继续 | 评估缺口类型：上下文→补发；推理→升模型；太大→拆分；计划错→上报人类 |

### 审查者限制

- **审查者只读**：不能修改代码（工具限制：Read, Grep, Glob, LS 等）
- 审查者不能被说服跳过发现的问题
- 审查者以四级报告：Critical / Important / Minor / 计划冲突（上报人类）

### v6.0 架构变化

- 前置冲突检查：派发前检查是否与已有计划冲突
- 持久化进度账本：`.superpowers/sdd/progress.md` 记录已完成任务及其 commit 范围
- 断点恢复：检查账本 + git log 而非内存

### 并行 Agent 派发

特定场景（3+ 个测试文件因不同根因失败）使用 `dispatching-parallel-agents` skill：

- 多个 subagent 在同一响应中并行派发
- 每个 subagent 有独立 scope，不得共享状态或互相干扰
- 全部完成后汇总 + 检查冲突 + 运行完整测试套件

### 关键源码参考

- `skills/subagent-driven-development/SKILL.md` — SDD 完整流程
- `skills/dispatching-parallel-agents/SKILL.md` — 并行派发条件与限制
- `skills/receiving-code-review/SKILL.md` — 6 步审查接收模式
- `scripts/task-brief` — 提取任务的工具脚本
- `scripts/review-package` — 生成审查 diff 包

---

## 方向 3：Git Worktree 隔离执行

### 作为前置门控

`using-git-worktrees` skill 在写生产代码前创建隔离工作区：

```
Step 0: 检测是否已在隔离环境中
  ├─ 已 worktree 中 → 跳过，直接用
  ├─ submodule 中 → 视为普通仓库
  └─ 普通 checkout → 请求用户同意创建
Step 1: 创建隔离工作区
  ├─ 优先使用平台原生工具 (EnterWorktree / WorktreeCreate)
  └─ 回退到 git worktree add
Step 2: 自动检测安装依赖 (package.json / Cargo.toml / requirements.txt...)
Step 3: 运行测试验证基线通过
Step 4: 报告就绪
```

### 已知问题与规避

| 问题 | 影响 | 规避方案 |
|------|------|---------|
| Claude Code worktree 静默回退到父仓库 | 隔离失效 | 基于 clone 的隔离（--dissociate --reference --single-branch） |
| Subagent 分支切换改变父仓库 HEAD | 父仓库状态污染 | 每个 subagent 独立 worktree |
| Worktree 文件被误提交 | git 历史污染 | 创建前必须 git check-ignore 验证 |
| macOS 环境差异（BSD date, PID 管理） | 测试环境差异 | 跳出工作流单独处理环境问题 |

### 清理与溯源规则

- `.worktrees/` 或 `worktrees/` 下的 worktree 是 agent 拥有的，可以删除
- 其他位置的 worktree 是宿主环境拥有的，不能删除
- 清理顺序：merge 成功 → 测试通过 → 删除 worktree → 删除分支
- 清除后必须运行 `git worktree prune`

### 关键源码参考

- `skills/using-git-worktrees/SKILL.md` — 4 步工作流 + 清理规则
- [Claude Code Worktrees 官方文档](https://code.claude.com/docs/en/worktrees)
- [Known issue #55708](https://github.com/anthropics/claude-code/issues/55708)
- [Known issue #47548](https://github.com/anthropics/claude-code/issues/47548)

---

## 方向 4：Skills 系统设计

### 14 个技能分类

| 类别 | 技能 | 角色 |
|------|------|------|
| **协作** | brainstorming | 头脑风暴，通过提问细化需求 |
| | writing-plans | 将 spec 分解为 2-5 分钟的可执行任务 |
| | executing-plans | 内联执行计划（备选路径） |
| | subagent-driven-development | 子 Agent 驱动开发（推荐路径） |
| | dispatching-parallel-agents | 多 Agent 并行处理独立问题 |
| | requesting-code-review | 请求代码审查 |
| | receiving-code-review | 接收和处理审查反馈 |
| | finishing-a-development-branch | 测试验证 + 分支完成/合并/PR |
| | using-git-worktrees | 工作区隔离 |
| **测试** | test-driven-development | RED-GREEN-REFACTOR 强制 |
| **调试** | systematic-debugging | 4 阶段根因分析 |
| | verification-before-completion | 修复后验证 |
| **元** | using-superpowers | 引导程序，入口自举 |
| | writing-skills | 如何编写新技能（元技能） |

### SKILL.md 结构规范

每个技能是一个目录，包含 `SKILL.md` 作为入口：

```markdown
---
name: skill-name           # 仅字母、数字、连字符
description: Use when...   # 触发条件，非技能总结
---

## 概述（1-2 句核心原则）

## 何时使用（症状 / use cases / 小流程图）

## 核心模式（before/after 代码对比）

## 快速参考（常用操作表）

## 实现细节（或链接到单独文件）

## 常见错误（什么会出错 + 修复）

## 真实影响（可选，为何重要）
```

### 自动发现与触发

- Claude Code 自动扫描项目 `.claude/` 目录下的 skills/
- 描述字段的 **`Use when...`** 前缀是触发条件的关键
- 描述只写**触发条件**，不总结技能流程——总结流程会使 Agent 直接走捷径而不读完整内容

### Token 预算

| 技能类型 | 目标大小 |
|---------|---------|
| 入门工作流 | 每技能 <150 词 |
| 频繁加载的技能 | 总计 <200 词 |
| 其他技能 | <500 词 |

### 关键源码参考

- `skills/` 目录下全部 14 个 skill 目录
- `writing-skills/SKILL.md` — 技能编写的完整方法论

---

## 方向 5：Plugin 架构（跨平台）

### Plugin-per-Harness 模式

每个支持的 Agent 平台有独立的插件目录：

```
superpowers/
├── .claude-plugin/plugin.json      # Claude Code
├── .codex-plugin/plugin.json       # Codex CLI
├── .cursor-plugin/plugin.json      # Cursor
├── .kimi-plugin/plugin.json        # Kimi Code
├── .opencode/plugins/superpowers.js # OpenCode
├── .pi/extensions/superpowers.ts   # pi
├── gemini-extension.json           # Gemini CLI
├── .github/                        # Copilot CLI 共享
└── skills/                         # 共享技能（平台无关）
```

### 三个不变的组件

1. **Skills（平台无关）**：`skills/` 中的代码在每平台上完全共享。技能描述**动作**（"调用一个技能"、"读取文件"、"派发子代理"），从不命名具体工具。
2. **Tool Mapping（每平台）**：动作词汇翻译为平台的真实工具名称。存放在 `references/<harness>-tools.md` 或引导注入器中。
3. **Bootstrap（每平台）**：每会话开始时将完整的 `using-superpowers/SKILL.md` 注入模型上下文。

### 两种不变的规则

1. **技能命名动作，不命名工具**：适应不同平台不用编辑技能主体
2. **通过平台自身安装机制发布**：不编辑用户文件，通过插件/扩展/市场发布

### 三种集成形态

| 形态 | 机制 | 示例 |
|------|------|------|
| **A (Shell-hook)** | 会话启动时运行 shell 命令，读取 stdout 注入上下文 | Claude Code, Cursor, Copilot CLI |
| **B (进程内)** | JS/TS 插件，具有会话/消息生命周期回调 | OpenCode, pi |
| **C (说明文件)** | 扩展声明的上下文文件，平台始终加载 | Gemini |

### 核心差异：Claude Code vs Codex

| 维度 | Claude Code | Codex |
|------|-------------|-------|
| 技能发现 | 自动扫描 skills/ 目录 | 需在 plugin.json 显式声明 skills 路径 |
| 钩子系统 | hooks/hooks.json 触发 session-start | 空 hooks 对象，不触发钩子 |
| 子 Agent 派发 | Task 工具 + 命名 agent 类型 | spawn_agent + worker 角色 |
| 注册表 | 有命名 Agent 注册表 | 需手动映射 |

### 关键源码参考

- `.claude-plugin/plugin.json` — Claude Code 插件注册
- `.codex-plugin/plugin.json` — Codex 插件注册，有 interface 块
- `hooks/hooks.json` — session-start 钩子（匹配 startup|clear|compact）
- `hooks/session-start` — 自举脚本（核心入口）
- `docs/porting-to-a-new-harness.md` — 移植到新平台的完整指南
- `references/` — 各平台工具映射

---

## 方向 6：启动钩子与自举机制

### 入口链

```
用户启动会话
    │
    ▼
Claude Code 触发 SessionStart Hook（匹配 startup|clear|compact）
    │
    ▼
hooks/run-hook.cmd 定位 bash
    │
    ▼
hooks/session-start 脚本执行
    ├─ 读取 skills/using-superpowers/SKILL.md 全文
    ├─ 转义内容为 JSON 字符串
    ├─ 用 <EXTREMELY-IMPORTANT> 标签包装
    └─ 输出 JSON 到 stdout
        │
        ▼
钩子系统将内容注入模型 system prompt / 上下文
    │
    ▼
模型现在拥有完整的 using-superpowers 技能指令
    │
    ▼
模型每次行动前检查是否有技能匹配
```

### 自举脚本关键逻辑

`hooks/session-start` 脚本：
1. 读取 `skills/using-superpowers/SKILL.md`
2. 通过 bash 参数替换进行转义（比字符级循环快得多）
3. 包装在 `<EXTREMELY-IMPORTANT>` 标签中
4. 附加上下文："你有超能力...所有技能通过 Skill 工具调用"
5. 根据检测到的平台输出三种不同 JSON 形状之一

### 去重与重注入

- 钩子匹配 `startup|clear|compact` — 每次上下文重置时重新触发
- 确保引导内容在模型压缩上下文时不丢失
- 进程内插件有自己的去重保护（检查引导标记是否存在）

### 多语言钩子脚本

`hooks/run-hook.cmd` 是单个文件同时作为 Windows .cmd 和 Unix shell 脚本有效：
- Windows 端：在标准路径找 bash.exe，运行钩子脚本
- Unix 端：`: << 'CMDBLOCK'` 使批处理块成为 no-op

### 关键源码参考

- `hooks/hooks.json` — 钩子配置
- `hooks/session-start` — 核心自举脚本
- `hooks/run-hook.cmd` — 跨平台多语言包装器
- `skills/using-superpowers/SKILL.md` — 引导程序内容

---

## 方向 7：元技能 writing-skills（框架扩展性）

### TDD 驱动文档方法

Superpowers 的技能编写方法本身使用 TDD 工作流：

| TDD 概念 | 技能创建等价物 |
|---------|--------------|
| 测试用例 | 压力场景（3+ 种组合） |
| 生产代码 | SKILL.md |
| RED（观察失败） | 无技能时 Agent 违反规则，记录基线行为 |
| GREEN（观察通过） | 有技能时 Agent 合规 |
| REFACTOR（堵漏洞） | 找到新借口 → 堵上 → 重新验证 |

### 铁律

```
无技能，无失败测试优先 = 无技能
```

在编写任何技能文档之前，先编写一个测试（压力场景）。如果在测试之前写了技能——**删除它，重新开始**。没有例外。

### 技能类型

| 类型 | 描述 | 示例 |
|------|------|------|
| **技术技能** | 有步骤的具体方法 | TDD, systematic-debugging |
| **模式技能** | 思考问题的方式 | flatten-with-flags, test-invariants |
| **参考技能** | API 文档/语法指南 | office docs |

### RED-GREEN-REFACTOR 循环

**RED（编写失败测试）**：
1. 创建压力场景（纪律技能需要 3+ 种压力组合）
2. 无技能时运行场景，逐字记录基线行为
3. 识别 Agent 借口的模式

**GREEN（编写最小技能）**：
1. 命名验证（仅字母、数字、连字符）
2. Frontmatter 验证（必须有 name 和 description，Use when... 开头）
3. 关键词覆盖率
4. 清晰的概述
5. 一个有说服力的示例
6. 有技能时运行场景，验证 Agent 合规

**REFACTOR（堵漏洞）**：
1. 识别测试中的新借口
2. 添加明确的计数器（纪律技能）
3. 从所有测试构建借口表
4. 创建红旗列表
5. 重新测试直到防弹

### 描述优化的关键发现

测试中发现：如果 description 总结技能的工作流，Agent 会按照描述走捷径而**不读完整的 SKILL.md**。

| 错误示例 | 正确示例 |
|---------|---------|
| "在任务之间进行代码审查，包括 spec 合规和代码质量两次审查" | "在实现任务后，在新代码被整合之前使用" |
| Agent 行为：只做一次审查 | Agent 行为：读 SKILL.md，正确做两次审查 |

**规则**：Description 只写触发条件，不写技能做了什么。

### 指导形式选择

| 基线失败 | 正确形式 | 错误形式 |
|---------|---------|---------|
| 压力下跳过/违反规则 | 禁止 + 借口表 + 红旗 | 软指导（"最好..."、"考虑..."） |
| 输出形状错误 | 正面配方：陈述输出是什么 | 禁止列表 |
| 遗漏必需元素 | 结构化：模板中必需字段 | 模板附近散文提醒 |
| 行为取决于条件 | 以可观察谓词为条件的条件语句 | 无条件规则 + 豁免条款 |

### 部署清单

每项技能必须满足的部署检查：
- RED 阶段（3 项）
- GREEN 阶段（10 项）
- REFACTOR 阶段（5 项）
- 质量检查（5 项）
- 部署（2 项）

### 关键源码参考

- `skills/writing-skills/SKILL.md` — 完整技能编写方法论
- `skills/using-superpowers/SKILL.md` — 引导条件与触发规则

---

## 综合分析

### 7 个方向的关联

```
                     ┌──────────────────┐
                     │  Plugin 架构      │ ← 跨平台部署能力
                     │  (方向 5)         │
                     └────────┬─────────┘
                              │ 支撑
                     ┌────────▼─────────┐
                     │  启动钩子/自举     │ ← 入口，每次会话触发
                     │  (方向 6)         │
                     └────────┬─────────┘
                              │ 注入
                     ┌────────▼─────────┐
                     │  1% 规则 +        │
                     │  Skills 系统设计   │ ← 行为约束引擎
                     │  (方向 4)         │
                     └────────┬─────────┘
                              │ 编排
              ┌───────────────┼───────────────┐
              │               │               │
     ┌────────▼──────┐ ┌─────▼──────┐ ┌──────▼────────┐
     │Workflow       │ │Subagent    │ │Git Worktree   │
     │Pipeline       │ │Dispatching │ │隔离执行        │
     │(方向 1)       │ │(方向 2)    │ │(方向 3)       │
     │阶段流转+门控   │ │执行引擎     │ │基础设施保障    │
     └───────────────┘ └────────────┘ └───────────────┘
                              │
                     ┌────────▼─────────┐
                     │  writing-skills   │ ← 框架如何扩展自身
                     │  (方向 7)         │
                     └──────────────────┘
```

### 与主流框架的对比

| 维度 | Superpowers | Matt Pocock Skills | Agent Skills (Addy Osmani) |
|------|-------------|-------------------|--------------------------|
| **核心假设** | 模型会偷懒找借口 | 模型大体上会做正确的事 | 需要多角色并行审查 |
| **触发方式** | 自动（1% 规则） | 手动斜杠命令（12/18 对模型隐藏） | 混合 |
| **Token 成本** | 高 | 低 | 中 |
| **门控强度** | 硬门控，禁止跳过 | 软锚点，可跳过 | 硬门控 + 并行审查 |
| **最佳场景** | 纪律化长时间执行 | 快速需求澄清 | 广泛的企业级验证 |
| **签名特征** | Subagent-Driven-Development | Grilling（逐个问题质询） | /ship 并行 4 角色审查 |

### Superpowers 在实际项目中的效果

- **chardet v7.0.0**: 41 倍性能提升，准确率 94.5% → 96.8%（2,161 测试文件，99 种编码）
- **Builder.io 告警守护进程**: 424 行规范 → 17 文件 26 任务 → TDD 实现
- **电话答录机系统**: 第一晚完成 brainstorm + spec + plan + scaffold + 3 CDK stacks + 4 Lambda + 测试 + CI
- **效率数据**: 需求确认从"直接写方向跑偏" → "先问关键问题"；返工从 3-4 轮 → 1 次；单模块 40 分 → 15 分

### 适用场景与局限

**适用**：
- 大型项目需要严格质量控制
- 多人/多 Agent 协作
- 需要可复现、可审计的开发流程
- 需要长时间免监督执行

**局限**：
- Token 消耗大（v6 正在改善）
- 小改动走完整流程过度设计
- 线性流程可能感觉繁重
- Claude Code worktree 隔离有已知 bug
- 跨平台需额外映射工作

### 关键资源索引

| 资源 | URL |
|------|-----|
| GitHub 仓库 | https://github.com/obra/superpowers |
| Claude Code 插件市场 | .claude-plugin/plugin.json |
| v6.0 Release Notes | 仓库 RELEASE-NOTES.md |
| 移植指南 | docs/porting-to-a-new-harness.md |
| Claude Code Agents 文档 | https://code.claude.com/docs/en/agents |
| Claude Code Subagents 文档 | https://code.claude.com/docs/en/sub-agents |
| Claude Code Worktrees 文档 | https://code.claude.com/docs/en/worktrees |
| Superpowers 深度分析(腾讯云) | https://cloud.tencent.com.cn/developer/article/2665629 |
| Superpowers 实战教程(腾讯云) | https://cloud.tencent.com/developer/article/2676405 |
| 12行 vs 689行对比(腾讯云) | https://cloud.tencent.com/developer/article/2706290 |
| 高级技能详解(腾讯云) | https://cloud.tencent.com/developer/article/2668310 |
| 三种哲学对比(Dev.to) | https://dev.to/jamilxt/superpowers-vs-agent-skills-vs-pocock-three-philosophies-of-ai-coding-workflows-e6n |
| Superpowers+Gstack+GSD 三层栈 | https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3 |
| Builder.io 真实案例 | https://site.builder.io/blog/claude-code-superpowers-plugin |
| Simon Willison 评测 | https://simonwillison.net/2025/Oct/10/superpowers/ |
| DevelopersIO 头脑风暴评测 | https://dev.classmethod.jp/en/articles/2026-03-17-superpowers-brainstorming/ |
| Pulumi 对比分析 | https://www.pulumi.com/blog/claude-code-orchestration-frameworks/ |
| agent-skills 官方对比 | https://github.com/addyosmani/agent-skills/blob/main/docs/comparison.md |
