# Superpowers - Practices

## 1. 安装方式

### Claude Code（官方市场）

```bash
/plugin install superpowers@claude-plugins-official
```

### Claude Code（Superpowers 市场）

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Gemini CLI

```bash
gemini extensions install https://github.com/obra/superpowers
```

### Cursor

```text
/add-plugin superpowers
```

### 其他平台

详见 README.md 安装章节。每个 Harness 需要单独安装。

## 2. Brainstorming 实践

### 提问策略

- **一次只问一个问题**，不要一次丢多个问题
- **优先选择题**，开放题次之
- 先了解目的、约束、成功标准
- 如果项目太大（多个独立子系统），先帮用户分解

### 设计展示

- 按复杂度缩放每段长度（简单的几句话，复杂的 200-300 字）
- 每段展示后询问"这部分看起来对吗？"
- 覆盖：架构、组件、数据流、错误处理、测试

### 设计隔离原则

- 每个单元有单一职责、明确定义的接口
- 能独立理解和测试
- 文件太大 = 做了太多事 = 需要拆分

## 3. Writing Plans 实践

### 文件结构映射

先列出所有要创建/修改的文件及其职责，再定义任务。

### 无占位符规则

**计划失败**的标志：
- "TBD"、"TODO"、"稍后实现"
- "添加适当的错误处理"
- "为上面写测试"（没有实际测试代码）
- "类似 Task N"（重复代码——执行者可能乱序阅读）
- 描述做什么但没展示怎么做的步骤

### Self-Review

写完计划后自查：
1. **Spec 覆盖**：每个需求都有对应任务？
2. **占位符扫描**：搜索红旗模式
3. **类型一致性**：前后任务的类型/方法签名/属性名一致？

## 4. Subagent-Driven Development 实践

### 任务提取

从计划文件中提取所有任务的**完整文本**，创建 TodoWrite 跟踪。

### 上下文构造

控制器（主代理）为每个子代理精确构造所需上下文：
- **不**让子代理读计划文件——直接提供完整文本
- **不**让子代理继承会话上下文/历史
- 提供场景设置（这个任务在整体中的位置）

### 审查循环

```
规范审查不通过 → 实现者修复 → 重新规范审查 → 通过
  ↓
质量审查不通过 → 实现者修复 → 重新质量审查 → 通过
  ↓
标记完成
```

**关键**：不能跳过任何一个审查。不能在规范审查通过前开始质量审查。

### 效率收益

- 无文件读取开销（控制器提供完整文本）
- 子代理获得完整信息（问题在工作开始前浮现）
- 自审在交接前捕获问题
- 但：每个任务需要更多子代理调用（实现者 + 2 审查者）

## 5. TDD 实践

### 验证清单

- [ ] 每个新函数/方法都有测试
- [ ] 每个测试在实现前看过它失败
- [ ] 每个测试因预期原因失败（功能缺失，不是拼写错误）
- [ ] 写了最小代码让每个测试通过
- [ ] 所有测试通过
- [ ] 输出干净（无错误、无警告）
- [ ] 测试用真实代码（只在必要时 mock）
- [ ] 边界情况和错误都覆盖了

### 测试质量标准

| 维度 | 好的测试 | 坏的测试 |
|------|---------|---------|
| 最小化 | 一件事。名字里有"和"？拆分 | `test('验证邮箱和域名和空格')` |
| 清晰 | 名字描述行为 | `test('test1')` |
| 意图明确 | 展示期望的 API | 隐藏代码应该做什么 |

## 6. Systematic Debugging 实践

### 多组件系统证据收集

在每个组件边界添加诊断：
```
对每个组件边界：
  - 记录进入组件的数据
  - 记录离开组件的数据
  - 验证环境/配置传播
  - 检查每层状态
```

### 3 次失败规则

```
修复次数 < 3 → 回到阶段 1，用新信息重新分析
修复次数 ≥ 3 → 停止！质疑架构
```

### 人为信号

当用户说以下话时，你在做错：
- "不是这样发生的？" → 你假设了没验证
- "停下猜测" → 你在没理解的情况下提议修复
- "ultrathink 这个" → 质疑根本，不只是症状

## 7. Writing Skills 实践

### CSO（Claude Search Optimization）要点

**Description 写法**：

```yaml
# ❌ 错误：总结了流程 — Claude 可能按此执行而非读完整 Skill
description: Use when executing plans - dispatches subagent per task with code review

# ✅ 正确：只写触发条件
description: Use when executing implementation plans with independent tasks in the current session
```

### Token 效率

| Skill 类型 | 目标字数 |
|------------|---------|
| 入门工作流 | <150 词 |
| 高频加载 Skill | <200 词 |
| 其他 Skill | <500 词 |

技巧：交叉引用其他 Skill 而非重复内容，用 `--help` 代替完整文档。

### 测试方法

1. **RED**：在没有 Skill 的情况下运行压力场景，记录基线行为
2. **GREEN**：编写针对具体违规的最小 Skill
3. **REFACTOR**：发现新的合理化借口 → 堵住 → 重新验证

### 压力类型（用于测试）

- 时间压力
- 沉没成本
- 权威压力
- 疲劳/倦怠
