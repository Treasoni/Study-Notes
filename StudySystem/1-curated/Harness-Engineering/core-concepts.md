# Harness Engineering - 核心概念

## 1. 术语起源

| 概念 | 来源 | 原文 | 出处 |
|------|------|------|------|
| Engineer the Harness | Mitchell Hashimoto | "anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again" | [doc-02] My AI Adoption Journey (2026-02) |
| Harness engineering (产品化) | OpenAI Codex 团队 | 5个月、百万行代码、0行人工编写的实验报告 | [doc-01] OpenAI Official (2026-02) |
| Mental Model | Martin Fowler | Harness = Guides + Sensors; Computational vs Inferential | [doc-03] Martin Fowler (2026) |
| Agent = Model + Harness | LangChain / Vivek Trivedy | Harness 是模型之外的一切 | [doc-04] LangChain (2026-03) |

## 2. 核心定义

> **Harness Engineering** 是围绕 AI Agent 设计和构建约束机制、反馈回路、工作流控制和持续改进循环的系统工程实践。它不优化模型本身，而是优化模型运行的环境。 — 综合多个来源

### 哲学核心
- **人类掌舵，智能体执行**（Human Steer, Agent Execute）— [doc-01]
- **Agent 的每一次失败，都是环境设计不完善的信号** — 综合
- **纪律没有消失，只是从"写好代码"转移到了"构建好让 Agent 工作的环境"** — [doc-12]

## 3. Feedforward（前馈）vs Feedback（反馈）

Martin Fowler 的核心框架 [doc-03]：

| 类型 | 作用 | 时机 | 示例 |
|------|------|------|------|
| **Feedforward Guides（前馈指南）** | 在 Agent 行动前给出方向 | 生成前 | AGENTS.md, Skills, 架构文档 |
| **Feedback Sensors（反馈传感器）** | 在 Agent 行动后检查结果 | 生成后 | 测试、lint、AI Code Review |

### Computational vs Inferential

| 维度 | Computational（计算型） | Inferential（推理型） |
|------|----------------------|---------------------|
| 执行体 | CPU | GPU/NPU |
| 速度 | 毫秒~秒级 | 较慢 |
| 确定性 | 确定性强 | 概率性 |
| 成本 | 低 | 高 |
| 示例 | Lint, TypeScript, ArchUnit | AI Code Review, "LLM as Judge" |

## 4. 三大调控类型 [doc-03]

| 类型 | 聚焦 | 当前成熟度 |
|------|------|-----------|
| **Maintainability Harness** | 内部代码质量（重复代码、圈复杂度、架构漂移） | 最成熟 |
| **Architecture Fitness Harness** | 架构特性（性能、可观测性、模块边界） | 发展中 |
| **Behaviour Harness** | 功能行为正确性 | 最不成熟（依赖 AI 生成的测试） |

## 5. OpenAI 六大组件体系 [doc-01]

| 组件 | 说明 | 核心实践 |
|------|------|---------|
| **结构化文档系统** | AGENTS.md 作为地图，docs/ 作为记录系统 | ~100 行 AGENTS.md → 指向深层 docs/ |
| **架构约束** | 严格分层 + 自定义 linter | CI 强制验证，错误信息内嵌修复指令 |
| **可观测性** | Chrome DevTools, LogQL, PromQL | Agent 直接接入运行时信号 |
| **反馈回路** | Agent-to-Agent 代码审查 | 多个专门 Agent 相互审查 PR |
| **渐进式披露** | 从小入口点开始 | Agent 被指导"下一步看哪里" |
| **熵与垃圾收集** | doc-gardening Agent 定期扫描 | 自动发现过时文档、架构偏差 |

## 6. Agent Harness 七大组件 [doc-04]

| 组件 | 类比 | 解决什么问题 |
|------|------|-------------|
| Orchestration Loop | 操作系统主循环 | 控制 "思考 → 行动 → 观察" 循环 |
| Tool Management | 驱动程序 | 管理 Agent 可用的工具 |
| Context Engineering | 内存管理 | 决定每次送入哪些信息 |
| State Persistence | 硬盘 | 保存进度、历史、中间结果 |
| Error Recovery | 异常处理 | 自动重试或回退 |
| Safety Guardrails | 防火墙 | 限制行为范围 |
| Verification Loops | 单元测试 | 自我检查输出质量 |

## 7. 常见 Agent 失败模式 [doc-07]

| 失败模式 | 描述 | Harness 对策 |
|---------|------|-------------|
| One-shotting | 试图一步到位，耗尽上下文 | 渐进式披露 + 执行计划拆解 |
| 过早宣布胜利 | 看到部分进展就宣布任务完成 | 验证循环 + 自动化检查 |
| 过早标记功能完成 | 不跑端到端测试就提交 | 反馈传感器 + CI 强制验证 |
| 模式复制放大 | 复制坏模式和架构漂移 | 熵管理 + 定期垃圾回收 |

## 8. Harnessability（可驾驭性）[doc-03]

相同代码库的"可驾驭性"不同：
- 强类型语言 → 天然有 type-checking 传感器
- 清晰模块边界 → 天然可施加架构约束
- Spring 等框架 → 隐式提高 Agent 成功率
- 遗留系统 → 最需要 harness 的地方最难构建
