---
comet_change: study-system-refactor
role: technical-design
canonical_spec: openspec
archived-with: 2026-06-01-study-system-refactor
status: final
---

# Study System Refactor - Technical Design

## 1. 架构概览

采用 **Hub-and-Spoke** 架构，Main Agent 作为协调者，专用 Subagent 执行重计算任务。

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE OVERVIEW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Main Agent (Hub)                                               │
│  ├─ 状态管理：读写 .comet.yaml、TODO.md                         │
│  ├─ 用户交互：AskUserQuestion、结果展示                         │
│  ├─ Subagent 调度：Agent() 工具调用                             │
│  └─ 输出验证：检查文件存在性和非空                               │
│                                                                  │
│  Subagents (Spokes)                                             │
│  ├─ Collect Subagent：读取原始文件，提取关键信息                 │
│  ├─ Curate Subagent：四维度打分，去重分类                       │
│  ├─ Write Subagent：填充模板，生成笔记初稿                      │
│  └─ Beautify Subagent：排版美化，格式优化                       │
│                                                                  │
│  通信方式：文件传递                                              │
│  ├─ 输入：读取指定路径的文件                                     │
│  └─ 输出：写入指定路径的文件                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Subagent 设计

### 2.1 专用 Subagent 定义

每个 Subagent 有明确的职责边界和输入输出规范：

| Subagent | 输入 | 输出 | 上下文预算 |
|----------|------|------|-----------|
| Collect | topic, sources list | `{SYSTEM_ROOT}/0-inbox/{topic}/raw/*` | ≤5k tokens |
| Curate | `{SYSTEM_ROOT}/0-inbox/{topic}/` | `{SYSTEM_ROOT}/1-curated/{topic}/*` | ≤8k tokens |
| Write | `{SYSTEM_ROOT}/1-curated/{topic}/`, note type | `{SYSTEM_ROOT}/2-drafts/{topic}/*` | ≤6k tokens |
| Beautify | `{SYSTEM_ROOT}/2-drafts/{topic}/*` | `{SYSTEM_ROOT}/3-published/{topic}/*` | ≤4k tokens |

### 2.2 Subagent 调用模式

```python
# Main Agent 调用示例
Agent(
    prompt="""
    你是 Collect Subagent。任务：从以下源提取关键信息。
    
    Topic: {topic}
    Sources: {source_list}
    Output Path: {SYSTEM_ROOT}/0-inbox/{topic}/raw/
    
    步骤：
    1. 读取每个源文件
    2. 提取核心概念、代码示例、关键观点
    3. 写入输出目录
    4. 完成后返回状态
    """,
    subagent_type="general-purpose",
    # 不使用 worktree isolation，因为需要访问文件系统
)
```

### 2.3 错误处理

```
Subagent 执行失败
    │
    ├─ 自动重试一次（相同输入）
    │
    └─ 重试成功？
        ├─ 是 → 继续流程
        └─ 否 → 通知用户，提供选项：
            ├─ 手动执行
            ├─ 跳过此阶段
            └─ 终止流程
```

## 3. 自治级别系统

### 3.1 级别定义

| 级别 | 确认点 | 减少确认次数 | 适用场景 |
|------|--------|-------------|---------|
| Level 0 | 每步确认 | 0% | 新用户、重要笔记 |
| Level 1 | 每阶段确认 | 50% | 默认，平衡效率和控制 |
| Level 2 | 关键点确认 | 80% | 熟练用户、大量笔记 |
| Level 3 | 仅最终确认 | 95% | 自动化场景 |

### 3.2 关键点定义

Level 2 的关键点：
- 笔记类型选择（如有）
- 执行计划审批
- 最终结果审查

### 3.3 配置格式

```yaml
# .study-config.yaml
autonomy:
  level: 1  # 全局默认
  overrides:
    - phase: write
      level: 0  # 写笔记时 always 确认
    - phase: beautify
      level: 3  # 美化自动执行
```

### 3.4 实现逻辑

```python
def should_confirm(phase: str, point: str) -> bool:
    """检查当前点是否需要确认"""
    config = load_config()
    level = config.get_override(phase) or config.global_level
    
    if level == 0:
        return True  # 每步确认
    elif level == 1:
        return point == "phase_boundary"  # 仅阶段边界
    elif level == 2:
        return point in CRITICAL_POINTS  # 仅关键点
    else:  # level == 3
        return point == "final_review"  # 仅最终审查
```

## 4. 需求发现系统

### 4.1 自适应问题数量

根据 topic 复杂度动态调整：

```python
def get_question_count(topic: str) -> int:
    """根据 topic 复杂度返回问题数量"""
    complexity = assess_complexity(topic)
    
    if complexity == "simple":
        return 4  # 核心问题
    elif complexity == "moderate":
        return 5  # 核心 + 1 扩展
    else:  # complex
        return 6  # 核心 + 2 扩展
```

### 4.2 问题模板

**核心问题（4 个）：**
1. 学习目的：考试准备 / 工作需要 / 兴趣探索
2. 目标读者：自己 / 团队 / 社区
3. 深度要求：入门 / 进阶 / 专家
4. 笔记用途：快速回顾 / 深度学习 / 分享传播

**扩展问题（2 个）：**
5. 特定关注点：（开放题）
6. 已有知识水平：（选择题）

### 4.3 类型推断逻辑

```python
def infer_note_type(answers: dict) -> list[str]:
    """根据答案推断笔记类型组合"""
    types = []
    
    # 学习目的 → 主要类型
    if answers["purpose"] == "exam":
        types.append("concept")
        types.append("cheat_sheet")
    elif answers["purpose"] == "work":
        types.append("practice")
        types.append("compare")
    else:  # interest
        types.append("concept")
    
    # 笔记用途 → 辅助类型
    if answers["usage"] == "sharing":
        if "practice" not in types:
            types.append("practice")
    
    # 限制最多 2 种
    return types[:2]
```

## 5. 混合笔记类型

### 5.1 章节顺序模板

```yaml
hybrid_order:
  concept + practice:
    - "## 核心概念"
    - "## 实战示例"
    - "## 常见模式"
    - "## 思考题"
  
  compare + cheat_sheet:
    - "## 对比分析"
    - "## 速查清单"
    - "## 决策框架"
    - "## 参考资料"
  
  experience + concept:
    - "## 背景上下文"
    - "## 核心概念"
    - "## 学习心得"
    - "## 延伸阅读"
```

### 5.2 章节合并规则

当多种类型有相似章节时：
- 相同标题 → 合并为一个章节
- 不同标题 → 保留各自章节，添加类型前缀
- 内容重叠 → 去重后合并

## 6. 测试策略

### 6.1 分层测试

```
┌─────────────────────────────────────────────────────────────────┐
│                    TESTING PYRAMID                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                     ┌─────────┐                                  │
│                     │  E2E    │  完整流程测试                     │
│                     │ 3 tests │  (5-10 min each)                 │
│                     └─────────┘                                  │
│                    ┌───────────┐                                 │
│                    │ Integration│  Subagent 协作测试              │
│                    │  6 tests  │  (1-2 min each)                 │
│                    └───────────┘                                 │
│                   ┌─────────────┐                                │
│                   │    Unit     │  单个 Subagent 测试             │
│                   │  12 tests   │  (< 30 sec each)               │
│                   └─────────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 测试用例

**单元测试：**
- Collect Subagent：读取不同格式文件，提取关键信息
- Curate Subagent：打分准确性，去重逻辑
- Write Subagent：模板填充，类型组合
- Beautify Subagent：格式优化，排版一致性

**集成测试：**
- Collect → Curate：数据传递正确性
- Curate → Write：资料完整性
- Write → Beautify：格式兼容性

**端到端测试：**
- 完整流程：从需求发现到最终笔记
- 自治级别：不同级别的行为验证
- 错误恢复：Subagent 失败后的重试逻辑

## 7. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| Subagent 调用延迟 | 用户等待时间增加 | 并行执行独立任务，设置超时 |
| 文件传递失败 | 数据丢失 | 验证文件存在性和完整性 |
| 自治级别过高 | 质量下降 | 默认 Level 1，提供质量检查点 |
| 混合类型结构混乱 | 笔记难以阅读 | 预定义章节顺序模板 |
| 需求发现耗时 | 用户体验差 | 支持跳过，使用默认配置 |

## 8. 实施计划

### Phase 1: 配置系统（1-2 天）
- 创建 .study-config.yaml
- 实现配置读取工具

### Phase 2: 需求发现（2-3 天）
- 实现自适应问题生成
- 实现类型推断逻辑

### Phase 3: Subagent 调度（3-4 天）
- 实现 4 个专用 Subagent
- 实现错误处理和重试

### Phase 4: 自治级别（1-2 天）
- 实现级别检查逻辑
- 实现配置覆盖

### Phase 5: 混合笔记（2-3 天）
- 实现章节顺序模板
- 实现章节合并逻辑

### Phase 6: 集成测试（2-3 天）
- 编写单元测试
- 编写集成测试
- 编写端到端测试

**总计：11-17 天**
