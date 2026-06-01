## 设计决策

### 问题根因

CLAUDE.md 中的 Resource Discovery、Pre-Task Init、Mandatory Triggered Reads 三段指令设计时只考虑了主 Agent，但没有明确排除 subagent。由于 Claude Code 的系统提示注入机制，所有 subagent 都会继承这些全局指令，导致启动时执行大量无意义的搜索和读取。

### 方案选型

| 方案 | 优点 | 缺点 | 选择 |
|------|------|------|------|
| A: Agent 定义加 skip 指令 | 最小改动，精准控制 | 每个 agent 都要改 | ✅ |
| B: CLAUDE.md 分离 main-only | 从源头解决 | 影响面大，需要验证所有 agent | ❌ |
| C: 修复 wikilink 验证路径 | 解决具体症状 | 不解决全局继承问题 | ✅ 补充 |

**选择 A + C 组合**：A 解决全局继承问题（根源），C 解决 agent 内部的低效搜索（症状）。

### 架构变更

```
修改前:
┌──────────────┐     继承 CLAUDE.md     ┌──────────────┐
│   CLAUDE.md  │ ──────────────────────▶│  Subagent    │
│  (全局指令)   │     Resource Discovery │  (执行任务)   │
│              │     Pre-Task Init      │              │
│              │     Mandatory Reads    │  → 先做 5-10  │
│              │                        │    次 Glob/Read│
│              │                        │  → 再干活     │
└──────────────┘                        └──────────────┘

修改后:
┌──────────────┐    被 skip 指令阻断    ┌──────────────┐
│   CLAUDE.md  │ ──✗───────────────────▶│  Subagent    │
│  (全局指令)   │                        │  (执行任务)   │
│  MAIN ONLY   │                        │              │
│              │                        │  → 直接干活   │
└──────────────┘                        └──────────────┘
       │                                       │
       │  TODO.md 中记录                        │
       │  每个 phase 的                         │
       │  输入/输出路径                          │
       └───────────────────────────────────────┘
```

### 跨阶段路径传递

在 TODO.md 中扩展格式，为每个 phase 记录输入/输出路径：

```markdown
## Phase 1: Collect
- [x] 完成收集
  - input: N/A (用户输入)
  - output: {SYSTEM_ROOT}/0-inbox/{topic}/raw/

## Phase 2: Curate
- [ ] 整理资料
  - input: {SYSTEM_ROOT}/0-inbox/{topic}/raw/
  - output: {SYSTEM_ROOT}/1-curated/{topic}/
```

这样下一个 phase 的 subagent 可以从 TODO.md 精确获取需要读取的路径，而不需要自己搜索。

### Wikilink 验证优化

修改前（writer.md / beautifier.md）：
```
Glob **/目标名.md  → 扫描整个 vault，返回大量无关结果
```

修改后：
```
Glob {OUTPUT_PATH}/目标名.md  → 只在目标目录搜索
Glob {SYSTEM_ROOT}/**/目标名.md  → 只在系统目录搜索
```

搜索范围从整个 vault 缩小到 1-2 个目录，减少 80%+ 的 Glob 结果。
