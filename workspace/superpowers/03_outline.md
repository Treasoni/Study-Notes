# 学习笔记大纲：《Superpowers Agentic Skills Framework — 从源码学习搭建 Agent 框架》

> 笔记类型：概念笔记 + 实战笔记（混合）
> 预计总篇幅：中（约 30-40 页）
> 章节数：9 章

---

### 第一章：Superpowers 概览与哲学
- **篇幅**：短
- **覆盖要点**：项目背景、核心哲学（硬门控 vs 软规则、TDD 优先、系统化流程）、项目结构全貌（14 技能 + 4 类）、7 个学习方向的关联图谱
- **素材引用**：方向 1（7 阶段管线总览）、方向 4（14 技能分类）、综合分析（各方向关联图）
- **代码示例**：无

### 第二章：Skills 系统设计 — 可组合的行为约束引擎
- **篇幅**：中
- **覆盖要点**：14 技能四大分类详解、SKILL.md 结构规范（frontmatter + 5 个核心段落）、自动发现与触发机制（Use when... 描述规则）、Token 预算策略、描述优化关键发现（总结流程会破坏技能）
- **素材引用**：方向 4（技能分类与结构规范）、方向 7（描述优化陷阱）
- **代码示例**：有（SKILL.md 模板、正确的 vs 错误的 description 写法）

### 第三章：Workflow Pipeline — 7 阶段硬门控状态机
- **篇幅**：长
- **覆盖要点**：7 阶段管线逐段详解（Brainstorming → Git Worktrees → Writing Plans → SDD/Executing Plans → TDD → Code Review → Finishing Branch）、9 个硬门控表、12 种 Agent 合理化借口预判、指令优先级体系（用户 > 技能 > 默认）、Writing Plans 任务粒度规范（2-5 分钟、禁止 TODO/TBD）
- **素材引用**：方向 1（完整管线、门控表、借口表）、方向 7（反借口表设计）
- **代码示例**：有（Writing Plans 任务模板、Brainstorming 9 步流程中的门控分支）

### 第四章：Subagent Dispatching — 子 Agent 派发与审查引擎
- **篇幅**：长
- **覆盖要点**：SDD 完整派发流程（task-brief → dispatch → implement → review）、四种状态报告协议（DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED）、模型分层策略（Haiku/Sonnet/Opus）、v5 → v6 审查流程演进（两次合并为一次）、审查者只读限制与四级发现报告、Dispatch 上下文隔离原则、Parallel Agent 并行派发场景与限制
- **素材引用**：方向 2（完整派发流程、状态协议、模型分层）、综合分析（Agent 团队模式）
- **代码示例**：有（Dispatch prompt 模板、task-brief 和 review-package 脚本流程、状态处理伪代码）

### 第五章：Git Worktree 隔离执行
- **篇幅**：短
- **覆盖要点**：作为前置门控的 4 步工作流（检测 → 创建 → 安装依赖 → 基线验证）、原生工具优先原则、已知问题与规避方案（静默回退、分支突变）、溯源清理规则（.worktrees/ vs 宿主环境）
- **素材引用**：方向 3（完整流程、已知问题表、清理规则）
- **代码示例**：有（Worktree 创建命令、安全验证命令、清理脚本）

### 第六章：Plugin 架构与跨平台部署
- **篇幅**：中
- **覆盖要点**：Plugin-per-Harness 模式（6+ 个平台插件目录）、三个不变组件（Skills + Tool Mapping + Bootstrap）、两条不变规则（技能命名动作 / 通过平台安装机制发布）、三种集成形态（Shell-hook A / 进程内 B / 说明文件 C）、Claude Code vs Codex 核心差异表
- **素材引用**：方向 5（完整架构分析、三种形态、平台差异）
- **代码示例**：有（plugin.json 对比、hooks.json 配置、session-start 脚本核心逻辑）

### 第七章：启动钩子与自举机制
- **篇幅**：短
- **覆盖要点**：入口链（SessionStart → run-hook.cmd → session-start 脚本 → 注入上下文）、JSON 输出三种形状（Claude Code vs Cursor vs Copilot CLI）、去重与重注入（匹配 startup|clear|compact）、跨平台多语言脚本设计（run-hook.cmd 双平台兼容）
- **素材引用**：方向 6（完整入口链、去重机制、跨平台多语言脚本）
- **代码示例**：有（JSON 输出形状对比、run-hook.cmd 结构、session-start 转义逻辑）

### 第八章：Writing-Skills — 框架的自我扩展机制
- **篇幅**：中
- **覆盖要点**：TDD 驱动文档方法（RED-GREEN-REFACTOR 映射到技能创建）、铁律（无失败测试 = 无技能）、三种技能类型（技术/模式/参考）、指导形式选择矩阵、防弹技能设计（借口表 + 红旗列表）、部署检查清单（25 项）
- **素材引用**：方向 7（完整 TDD-文档映射、形式选择矩阵、防弹技能设计）
- **代码示例**：有（RED-GREEN-REFACTOR 循环示例、借口的正确 vs 错误封堵写法）

### 第九章：总结 — 如何借鉴 Superpowers 搭建自己的 Agent 框架
- **篇幅**：中
- **覆盖要点**：Superpowers 的核心抽象提炼（门控 Pipeline + Subagent 执行 + Skills 约束 → 三层架构）、与主流框架对比（Matt Pocock / Agent Skills / GSD / GSTACK）、可复用的设计模式（硬门控模式、Subagent 隔离模式、自举注入模式）、实际项目效果数据（chardet 41x、Builder.io、电话答录机）、局限与适用边界判断
- **素材引用**：方向 1-7（综合提炼）、综合分析（框架对比表、实际案例数据）
- **代码示例**：有（三种典型场景的决策流程）

---

## 学习路径说明

### 前置要求
- 对 Claude Code / Codex 等 AI 编程工具有基本了解
- 了解 Git 基本操作（分支、worktree 概念）
- 对 TDD（测试驱动开发）有概念性了解
- 有一点点 Agent 工作流的使用经验

### 学完能做什么
- 理解 Superpowers 整套框架的设计思路和实现细节
- 掌握 Workflow Pipeline 的阶段划分和门控设计
- 学会 Subagent 派发模式：如何隔离上下文、分配模型、审查成果
- 掌握 Skills 系统的编写规范：SKILL.md 结构、描述优化、触发设计
- 理解跨平台 Plugin 架构的三种集成形态
- 能借鉴这些模式来设计自己的 Agent 框架或工作流系统

### 建议学习顺序
1. **第 1 章**（全局概览，必读）
2. **第 2 章**（Skills 系统基础，为后续做铺垫，必读）
3. **第 3 章**（Pipeline 核心，必读）
4. **第 4 章**（Subagent 执行引擎，必读）
5. **第 5 章**（环境隔离，可选 — 如果对基础设施感兴趣）
6. **第 6 章**（跨平台，可选 — 如果要做跨平台框架）
7. **第 7 章**（入口设计，可选 — 如果关注自举机制）
8. **第 8 章**（框架扩展性，推荐 — 如果要搭建自己的框架）
9. **第 9 章**（总结与应用，必读）
