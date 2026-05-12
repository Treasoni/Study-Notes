# Harness Engineering - 实战示例汇总

## 1. Mitchell Hashimoto 的 AGENTS.md 累积法 [doc-02]

```
每条 AGENTS.md 规则 = Agent 曾经犯过的一个错误
```

**Ghostty 项目实践**：
- 每当 Agent 出现坏行为（如运行错误命令、调用错误 API），将其记录到 `AGENTS.md`
- 两种形式：
  1. **隐式提示**：AGENTS.md 记录行为规则
  2. **工具化**：编写专用脚本（截图、过滤测试等），配合 AGENTS.md 告知 Agent 可用工具

**关键效果**：几乎完全消除了重复性错误。

## 2. OpenAI 百万行代码工程实践 [doc-01]

### 仓库即记录系统
```
不在仓库里的东西，对 AI 智能体不存在
```
- Slack 讨论、Google Docs、人脑中的知识 → 对 Agent 不可见
- 一切决策、规范、计划 → 版本化提交到仓库

### 知识库结构
```
AGENTS.md       (~100 行，总目录)
ARCHITECTURE.md (架构地图)
docs/
├── design-docs/
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
├── product-specs/
├── references/
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   └── ...
├── DESIGN.md
├── QUALITY_SCORE.md
└── SECURITY.md
```

### 三大核心纪律

| 纪律 | 实践 | 效果 |
|------|------|------|
| **Agent 可读性优化** | 选"无聊"技术、按 git worktree 启动 | Agent 可直接推理领域 |
| **Agent-to-Agent 审查** | 多 Agent 交叉审查 PR | 人工审核从必须→可选 |
| **机械化执行** | 自定义 linter + 结构测试 | 错误信息内嵌修复指令 |

### 效率数据
- 3 人 → 7 人团队
- 5 个月 → 百万行代码
- ~1500 个 PR
- 人均 3.5 PR/天
- 约传统方式的 1/10 时间

## 3. Martin Fowler 的 Steering Loop [doc-03]

```
观察 Agent 出错 → 分析根因 → 增强前馈或反馈 → 验证效果 → 循环
```

### 时机分布
```
                        Feedforward Sensors
                        ───────────────────
提交前:  LSP / AGENTS.md / Skills / How-to 指南
         ↓
         Agent 生成代码
         ↓
首次修正: Code Review Agent / ESLint / 类型检查 / 结构测试
         ↓
         Human Review
         ↓
合入后:  架构适应性测试 / 变异测试 / 详细审查
                        ───────────────────
                        Feedback Sensors
```

### Harness 模板概念
- 企业常见拓扑（业务 API、事件处理、数据面板）
- 预制的指南 + 传感器捆绑包
- 团队选技术栈时可能考虑"该栈的 harness 是否现成"

## 4. HumanLayer 的编码 Agent 配置 [doc-06]

### 配置杠杆体系

| 杠杆 | 说明 | 解决的核心问题 |
|------|------|-------------|
| **System Prompt** | 系统消息 | 基础行为约束 |
| **Tools / MCPs** | 工具接入 | 能力扩展 |
| **Context** | 上下文管理 | 信息组织 |
| **Sub-agents** | 子代理 | 跨 session 一致性 |
| **Hooks** | 集成钩子 | 确定性控制流 |
| **Skills** | 技能模块 | 渐进式知识披露 |

### 子代理 = 上下文防火墙
- 子任务在隔离的上下文窗口中运行
- 中间噪声不会积累到主线程
- 可在超长 session 中保持一致性

### 核心洞察
> "不是模型的问题，是**配置的问题**。模型会变强，但新的更强模型所做的更大更难的任务，会以新方式继续失败。"

## 5. LangChain Terminal Bench 跃升案例 [doc-07]
- 仅改 Harness（文档结构 + 验证回路 + 追踪系统）
- 底层模型未变
- Terminal Bench 2.0: 52.8% → 66.5%
- 全球排名: 30 → 5

## 6. Harness Engineering 入门路径

### 最小可行 Harness
1. **AGENTS.md** — 记录 Agent 的坏行为和修正规则
2. **pre-commit hook** — 基础静态检查
3. **自动化测试** — Agent 自我验证的反馈回路
4. **结构化的 docs/** — Agent 可读的知识库

### 进阶路径
1. 自定义 linter + 结构测试（机械化执行）
2. Agent-to-Agent 审查流程
3. 可观测性工具接入 Agent 运行时
4. 熵管理（定期垃圾回收 Agent）
5. Harness 模板化 + 团队共享
