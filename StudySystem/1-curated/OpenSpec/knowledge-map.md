---
curated:
  date: 2026-06-01
  topic: OpenSpec
  description: 知识地图 — 展示 OpenSpec 各概念之间的联系
  sources: R01-R16
---

# OpenSpec 知识地图

## 知识结构总览

```
OpenSpec — 规范驱动开发 (SDD) 框架
│
├── 1. 核心理念
│   ├── 1.1 SDD 概念 — 先写规范，再写代码
│   ├── 1.2 设计哲学 — 流动/迭代/简单/棕地优先
│   └── 1.3 问题定位 — 架构漂移/上下文丢失/技术债务/返工
│
├── 2. 基础概念
│   ├── 2.1 规范 (Specs) — 系统当前行为的真相源
│   ├── 2.2 变更 (Changes) — 提议的修改，独立文件夹
│   ├── 2.3 工件 (Artifacts) — 指导工作的文档
│   │   ├── proposal.md — 意图、范围、方法
│   │   ├── specs/ — 增量规范 (ADDED/MODIFIED/REMOVED)
│   │   ├── design.md — 技术方法和架构决策
│   │   └── tasks.md — 实现检查清单
│   ├── 2.4 增量规范 — 核心创新，仅描述变化部分
│   └── 2.5 归档 — 完成变更，合并增量到主规范
│
├── 3. 工作流系统
│   ├── 3.1 Core Profile (5 命令) — propose/explore/apply/sync/archive
│   ├── 3.2 Custom Profile (11 命令) — 新增 new/continue/ff/verify 等
│   ├── 3.3 工件图状态机 — BLOCKED -> READY -> DONE
│   │   └── openspec status 命令提供实时状态
│   └── 3.4 动态指令组装 — Context + Rules + Templates
│
├── 4. 操作界面
│   ├── 4.1 CLI 命令 — init/update/list/show/validate/view/status
│   ├── 4.2 斜杠命令 — 在 AI 工具聊天界面中使用
│   ├── 4.3 Schema 命令 — fork/init/validate/which
│   ├── 4.4 Workspace 命令 — setup/list/link/doctor/open (Beta)
│   └── 4.5 JSON 输出 — 便于脚本化
│
├── 5. 定制化系统
│   ├── 5.1 项目配置 — config.yaml (context, rules, schema)
│   ├── 5.2 自定义 Schema — schema.yaml + templates/
│   ├── 5.3 Schema 解析顺序 — CLI > 变更元数据 > 项目配置 > 默认
│   ├── 5.4 模板系统 — 指导 AI 的 Markdown 模板
│   └── 5.5 全局覆盖 — 跨项目共享 schema
│
├── 6. 高级特性
│   ├── 6.1 多语言支持 — 指令丰富管道
│   ├── 6.2 Workspace (Beta) — 跨仓库协调视图
│   └── 6.3 社区 Schema — superpowers-bridge 等
│
├── 7. 生态系统
│   ├── 7.1 安装方式 — npm/pnpm/yarn/bun/nix/npx
│   ├── 7.2 工具支持 — 29+ AI 编程助手
│   ├── 7.3 集成架构 — Skills 层 + Commands 层
│   ├── 7.4 社区分支 — @studyzy/openspec-cn 等
│   └── 7.5 版本演进 — v1.0.0 → v1.3.1
│
├── 8. 实战示例
│   ├── 8.1 深色模式 (官方) — 完整的 propose→apply→archive 流程
│   ├── 8.2 厨房计时器 (GIGAZINE) — 旧版命令，端到端教程
│   ├── 8.3 Beads 组合 (Reddit) — 真实世界 4 阶段工作流
│   └── 8.4 最佳实践 — 规范编写/变更管理/团队协作
│
└── 9. 工具对比
    ├── 9.1 vs SuperPowers — 规范管理 vs 多代理
    ├── 9.2 vs Spec Kit — 轻量 vs 重量级
    ├── 9.3 vs Kiro — 工具无关 vs IDE 锁定
    └── 9.4 vs 无 SDD — 可预测 vs 不可预测
```

## 概念间的主要关联

### 核心流程关系

```
Proposal ──定义──> Specs (增量) ──指导──> Design ──生成──> Tasks ──驱动──> Apply
    ^              │                                                         │
    │              │                                                         │
    └──────────────┴───────────────── Verify ────────────────────────────────┘
                                                                          │
                                                                          v
                                                                      Archive
                                                                    │
                                                                    v
                                                              主 Specs 更新
```

### 数据流

```
安装 (npm install)
  │
  v
初始化 (openspec init)
  │
  ├──> 创建 openspec/ 目录结构
  ├──> 创建 specs/ + changes/ + config.yaml
  └──> 生成工具特定技能文件
        │
        v
用户通过 AI 工具发起斜杠命令
  │
  ├──> /opsx:propose ──> 生成计划工件 (proposal + specs + design + tasks)
  ├──> /opsx:apply   ──> AI 按 tasks.md 实现代码
  ├──> /opsx:verify  ──> 检查实现匹配规范
  └──> /opsx:archive ──> 增量合并到主 specs，工件归档
```

### 配置影响关系

```
config.yaml
  ├── context ──────────> 影响所有工件的内容
  ├── rules  ──────────> 影响特定工件的内容
  ├── schema ──────────> 决定使用哪个工作流 schema
  │                      │
  │                      v
  │                 schema.yaml
  │                   ├── artifacts ──> 定义可用工件及其依赖
  │                   └── templates/ ──> 指导 AI 的输出格式
  │
  └── delivery ─────────> 决定 Skills/Commands/Both 集成层
```

## 子话题覆盖矩阵

| 子话题 | R01 | R02 | R03 | R04 | R05 | R06 | R07 | R08 | R09 | R10 | R11 | R12 | R13 | R14 | R15 | R16 |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 设计哲学 | Y | - | - | - | Y | Y | - | - | - | - | - | - | Y | Y | - | - |
| 项目结构 | Y | Y | - | - | - | Y | Y | Y | - | - | - | - | Y | Y | - | - |
| 规范格式 | - | Y | - | - | - | Y | - | - | - | - | - | Y | Y | Y | - | - |
| 增量规范 | - | Y | - | - | - | Y | - | - | - | - | - | - | Y | Y | - | - |
| 工件系统 | - | Y | - | - | - | Y | - | - | - | - | - | - | Y | Y | - | - |
| 斜杠命令 | Y | Y | - | Y | Y | - | - | - | - | - | - | Y | Y | - | - | - |
| 工作流状态机 | - | - | - | - | Y | - | - | - | - | - | - | - | - | - | - | - |
| CLI 命令 | Y | Y | Y | - | - | - | Y | Y | - | - | - | - | - | - | - | - |
| 安装 | Y | - | - | - | - | - | - | Y | - | - | - | - | - | Y | - | - |
| 定制化 | - | - | - | - | - | - | Y | - | - | - | - | - | - | - | - | - |
| 自定义 Schema | - | - | Y | - | - | Y | Y | - | - | - | - | - | - | - | - | - |
| 多语言 | - | - | - | - | - | - | - | - | - | Y | - | - | - | - | - | - |
| Workspace | - | - | Y | - | - | Y | - | - | - | - | - | - | - | - | - | - |
| 工具支持 | Y | - | - | Y | - | - | - | - | Y | - | - | - | - | Y | - | - |
| 实战示例 | - | Y | - | - | - | - | - | - | - | - | - | Y | - | - | Y | - |
| 多工具组合 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | Y | - |
| 工具对比 | Y | - | - | - | - | - | - | - | - | - | - | - | Y | - | - | Y |
| 版本历史 | - | - | - | - | - | - | - | - | - | - | Y | - | - | - | - | - |
