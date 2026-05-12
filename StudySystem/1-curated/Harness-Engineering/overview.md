# Harness Engineering - 知识地图

## 主题层级

```
Harness Engineering（系统治理工程）
├── 1. 概念起源与定义
│   ├── 1.1 Mitchell Hashimoto 的 6 阶段进化论 [doc-02]
│   ├── 1.2 OpenAI Codex 百万行实验 [doc-01]
│   └── 1.3 Martin Fowler 的 mental model [doc-03]
│
├── 2. 核心概念与框架
│   ├── 2.1 Agent = Model + Harness [doc-04]
│   ├── 2.2 Feedforward（前馈）vs Feedback（反馈）[doc-03]
│   ├── 2.3 Computational（计算型）vs Inferential（推理型）[doc-03]
│   ├── 2.4 三范式演进：Prompt → Context → Harness [doc-07]
│   └── 2.5 三大调控类型 [doc-03]
│       ├── Maintainability Harness（可维护性）
│       ├── Architecture Fitness Harness（架构适应性）
│       └── Behaviour Harness（行为正确性）
│
├── 3. 六大组件体系
│   ├── 3.1 结构化文档系统（AGENTS.md + docs/）[doc-01]
│   ├── 3.2 架构约束与自定义 linter [doc-01]
│   ├── 3.3 可观测性与工具（Chrome DevTools, LogQL, PromQL）[doc-01]
│   ├── 3.4 反馈回路（Agent-to-Agent 审查）[doc-01]
│   ├── 3.5 渐进式披露（从小入口开始）[doc-01]
│   └── 3.6 熵与垃圾收集（doc-gardening）[doc-01]
│
├── 4. Agent Harness 架构解剖 [doc-04]
│   ├── 4.1 Orchestration Loop（编排循环）
│   ├── 4.2 Tool Management（工具管理）
│   ├── 4.3 Context Engineering（上下文工程）
│   ├── 4.4 State Persistence（状态持久化）
│   ├── 4.5 Error Recovery（错误恢复）
│   ├── 4.6 Safety Guardrails（安全护栏）
│   └── 4.7 Verification Loops（验证循环）
│
├── 5. 实战方法
│   ├── 5.1 AGENTS.md 规则累积法 [doc-02]
│   ├── 5.2 编码 Agent 配置点优化 [doc-06]
│   ├── 5.3 仓库即记录系统 [doc-01]
│   ├── 5.4 Harness 模板化 [doc-03]
│   ├── 5.5 智能体可读性优化 [doc-01]
│   └── 5.6 子代理充当上下文防火墙 [doc-06]
│
├── 6. 企业治理视角 [doc-09]
│   ├── 6.1 Agent 部署与治理差距
│   ├── 6.2 软件组合治理 = Harness
│   └── 6.3 从启动到规模化的路径
│
└── 7. 争议与未来方向
    ├── 7.1 SDD vs Harness Engineering [doc-12]
    ├── 7.2 技术栈收敛趋势 [doc-05]
    ├── 7.3 Harnessability（可驾驭性）[doc-03]
    └── 7.4 旧系统改造挑战 [doc-05]
```

## 核心关系图

```
                      ┌──────────────────┐
                      │     Human        │
                      │    (Steer)       │
                      └────────┬─────────┘
                               │ 设计/迭代
                               ▼
              ┌────────────────────────────────┐
              │        Harness (缰绳)          │
              │  ┌──────┐  ┌──────┐  ┌──────┐ │
              │  │Guides│  │Agent │  │Sensor│ │
              │  │前馈  │──►│ 模型 ├──►│ 反馈 │ │
              │  └──────┘  └──────┘  └──────┘ │
              │           ▲           │        │
              │           └──自修正───┘        │
              └────────────────────────────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │    Codebase      │
                      │   (输出产物)      │
                      └──────────────────┘
```
