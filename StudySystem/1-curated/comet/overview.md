# Knowledge Map — Comet

## Topic Overview
Comet (`@rpamis/comet`) 是一个将 **OpenSpec**（规格驱动开发）和 **Superpowers**（技能驱动的 TDD 工作流）串联为五阶段自动化流水线的开发工具。它解决了两者独立使用时"提案不够细"和"文档缺乏状态化"的问题，提供从创意到归档的全流程管理。

## Sub-topics and Key Points

### 1. Comet 核心定位
- OpenSpec 处理 WHAT（大纲、提案、spec 生命周期、归档）[来源: 1][来源: 2]
- Superpowers 处理 HOW（技术设计、规划、执行、收尾）[来源: 1][来源: 2]
- Comet 将二者串联为五阶段自动化流水线 [来源: 1][来源: 2]
- 核心价值：状态化管理、断点续传、文档同步自动化 [来源: 1][来源: 2]

### 2. 五阶段工作流
- **Phase 1: Open** — 开启变更（openspec propose）
- **Phase 2: Design** — 深度设计（superpowers brainstorming）
- **Phase 3: Build** — 计划与构建
- **Phase 4: Verify** — 验证与收尾
- **Phase 5: Archive** — 归档变更
[来源: 1][来源: 2]

### 3. 安装与使用
- 前置要求：Node.js 20+, npm, Git, Bash
- 全局安装：`npm install -g @rpamis/comet`
- 初始化：`cd your-project && comet init`
- 主入口：`/comet` 命令，支持状态检测和断点续传 [来源: 1][来源: 2]

### 4. 状态机机制（.comet.yaml）
- 记录 phase、执行模式、验证结果、归档状态
- 支持断点恢复——Agent 无需重新翻文档猜进度
- 多 Spec 选择：多个活跃 Spec 时列出供选择 [来源: 1][来源: 2]

### 5. 守护条件（Guard Conditions）
- `comet-guard.sh`：检查任务完成状态
- `comet-yaml-validate.sh`：验证 YAML 字段
- `comet-state.sh`：检查验证证据和归档条件
- 防止 Agent 在未完成时虚假推进 [来源: 1][来源: 2]

### 6. OpenSpec 基础（Comet 的 WHAT 层）
- 三步工作法：Propose → Apply → Archive
- 核心产物：proposal.md, specs/, design.md, tasks.md
- npm 包：`@fission-ai/openspec`
- 文件结构：`openspec/specs/` 和 `openspec/changes/` [来源: 6][来源: 5]

### 7. Superpowers 基础（Comet 的 HOW 层）
- SDD（Subagent-Driven Development）：Implementer → Spec Reviewer → Quality Reviewer
- TDD 铁律：没有失败测试就不写生产代码
- 技能自动触发：brainstorming → writing-plans → subagent-driven-development → finishing-a-development-branch [来源: 7][来源: 4]

### 8. 双星联动模式
- OpenSpec 负责规格定义（其 `/opsx:apply` 被跳过）
- Superpowers 负责代码实现（利用 TDD 和代码审查能力）
- Comet 作为编排层自动串联两者的产物 [来源: 4][来源: 5]

## Knowledge Graph

```
Comet (编排层)
  ├── OpenSpec (WHAT: 规格管理)
  │     ├── propose → 创建提案/规格/设计/任务
  │     ├── apply → (Comet 中跳过，由 Superpowers 替代)
  │     └── archive → 归档变更
  │
  ├── Superpowers (HOW: 工程执行)
  │     ├── brainstorming → 设计方案
  │     ├── writing-plans → 执行计划
  │     ├── subagent-driven-development → TDD 实现
  │     └── finishing-a-development-branch → 收尾
  │
  └── Comet 自有组件
        ├── .comet.yaml (状态机)
        ├── comet-guard.sh (守护检查)
        ├── 5 阶段流程 (Open → Design → Build → Verify → Archive)
        └── 跨平台安装器
```
