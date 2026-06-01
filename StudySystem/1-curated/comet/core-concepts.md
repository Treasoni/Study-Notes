# Core Concepts — Comet

## 1. 双星架构 (Dual-Star Architecture)

Comet 的核心设计理念是将 OpenSpec 和 Superpowers 两个独立项目的能力组合成一个统一工作流。

| 角色 | 工具 | 职责 |
|------|------|------|
| WHAT 层 | OpenSpec | 大纲、提案、spec 生命周期、归档 |
| HOW 层 | Superpowers | 技术设计、规划、执行、收尾 |
| 编排层 | Comet | 状态管理、阶段流转、文档同步、断点续传 |

[来源: 1][来源: 2]

## 2. 五阶段流水线 (5-Phase Pipeline)

Comet 将开发流程组织为 5 个阶段，从创意到归档一条命令完成：

1. **Open** — `/comet-open`: 开启 change，生成 proposal/spec/design/tasks
2. **Design** — `/comet-design`: 深度设计，brainstorming 产出 Design Doc
3. **Build** — `/comet-build`: 计划与构建，subagent 执行
4. **Verify** — `/comet-verify`: 验证与收尾
5. **Archive** — `/comet-archive`: 归档变更

主入口 `/comet` 自动检测当前阶段，支持断点续传。

[来源: 1][来源: 2]

## 3. 状态化 Spec 生命周期

传统工作流中，Spec 文档只是静态 Markdown，依赖用户提醒 Agent 更新状态。Comet 通过 `.comet.yaml` 实现状态化管理：

- 记录当前 phase、执行模式
- 记录验证结果和归档状态
- Agent 中断后可自动恢复，无需重新检查代码和文档

核心文件：
- `.comet.yaml` — 状态机核心文件，跟踪阶段和进度
- `docs/superpowers/specs/` — 工作目录
- `docs/superpowers/plans/` — 计划目录

[来源: 1][来源: 2]

## 4. 守护条件机制 (Guard Conditions)

Comet 通过 shell 脚本实现阶段退出的验证，防止 Agent 虚假推进：

- `comet-guard.sh` — 检查任务是否全部完成
- `comet-yaml-validate.sh` — 验证 `.comet.yaml` 字段完整性
- `comet-state.sh` — 检查验证证据和归档条件是否满足

设计原则：不信任 Agent 说"完成了"，只有脚本验证通过才允许推进。

[来源: 1][来源: 2]

## 5. 嵌套 Skill 触发

Comet 的核心技术挑战之一是如何稳定触发嵌套 Skill：
- 从 Comet 触发 OpenSpec 的 propose/archive
- 从 Comet 触发 Superpowers 的 brainstorming
- 确保 CC 上显示 Skill 触发打印（真正触发，而非模拟）

[来源: 1][来源: 2]

## 6. OpenSpec 核心概念

- **三步工作法**: Propose → Apply → Archive
- **Propose**: 生成 proposal.md, specs/, design.md, tasks.md
- **Apply**: 按任务清单实现代码
- **Archive**: 归档 change，更新主 spec
- **设计哲学**: fluid not rigid, iterative not waterfall, built for brownfield

[来源: 5][来源: 6]

## 7. Superpowers 核心概念

- **SDD (Subagent-Driven Development)**: 三个角色协作
  - Implementer（实现者）— 写代码、写测试、跑测试
  - Spec Compliance Reviewer（规格审查员）— 逐行对比代码和规格
  - Code Quality Reviewer（质量审查员）— 审查代码质量
- **TDD 铁律**: 无失败测试则不写生产代码
- **技能自动触发链**: brainstorming → writing-plans → subagent-driven-development → finishing-a-development-branch

[来源: 7][来源: 4]

## 8. Comet vs 单独使用 OpenSpec + Superpowers

| 维度 | 单独使用 | 使用 Comet |
|------|----------|------------|
| 状态管理 | 文档无状态，依赖人工更新 | .comet.yaml 自动跟踪 |
| 断点续传 | Agent 需重读代码和文档猜进度 | 自动恢复 |
| 文档同步 | 人工提醒"记得更新" | 脚本自动化 |
| 阶段退出 | 依赖 Agent 自觉 | Guard 脚本强制执行 |
| 技能触发 | 手动切换 | 自动串联 |

[来源: 1][来源: 2]
