## Context

Study System 的文档体系经过多次迭代，产生了大量重复：
- TODO.md 状态机规则分散在 17 个文件中，同一指令重复 9-12 次
- update-workflow/SKILL.md 与 docs/updating-notes.md 60-70% 重复
- scoring rubric 在 3 个文件中完全相同
- 51 个 skills 全量注入系统提示，其中 37 个与 study-system 无关

当前每次会话的系统提示包含 ~381KB SKILL.md 内容 + ~10,000 tokens 文档冗余。

## Goals / Non-Goals

**Goals:**
- 消除文档冗余，预计每次会话减少 ~10,000+ tokens
- 实现 skill 过滤机制，减少 ~300KB+ 无用 skill 上下文
- 建立单一权威来源模式，防止未来再次出现冗余
- 保持所有现有功能不变（纯重构，无行为变更）

**Non-Goals:**
- 不改变 TODO.md 状态机的运行时行为
- 不重命名或重新组织 skills 目录结构
- 不修改任何 skill 的执行逻辑
- 不影响非 study-system 的 skills（comet、opencli 等保留原位）

## Decisions

### D1: TODO.md 状态机抽取为独立参考文档

**选择**：创建 `docs/todo-state-machine.md` 作为唯一权威定义，其他文件改为引用。

**替代方案**：
- 方案 B：在 CLAUDE.md 中保留完整定义 → 仍然分散，且 CLAUDE.md 已接近 160 行上限
- 方案 C：用脚本强制执行 → 过度工程化，状态机本质是线性的

**理由**：
- 线性状态机的规则简单（Read→Write→Bash），问题只是分散
- 抽取后 CLAUDE.md 只需一行引用，phases.md/experience-notes.md 各减少 ~500 tokens
- 17 个文件的引用改为指向同一来源

**实现**：
```
docs/todo-state-machine.md  ← 唯一权威定义
├─ 状态定义（create → phase gates → delete）
├─ 工具映射（Read/Write/Bash）
├─ 三种工作流变体（5-phase / 7-step / REFRESH mini）
└─ 路径约定（{SYSTEM_ROOT}/TODO.md）

CLAUDE.md  → 一行引用：See docs/todo-state-machine.md
phases.md  → Phase Gate 改为引用，不再重复定义
experience-notes.md → 同上
updating-notes.md → 同上
```

### D2: 合并 update-workflow 与 updating-notes.md

**选择**：保留 `docs/updating-notes.md` 作为权威文档，`update-workflow/SKILL.md` 精简为路由逻辑（如何调用 /update skill）。

**替代方案**：
- 方案 B：删除 updating-notes.md，全部移入 SKILL.md → 不符合现有模式（docs/ 是权威来源）
- 方案 C：创建新的合并文档 → 不必要的新文件

**理由**：
- 现有模式是 docs/ 存放规范，skills/ 存放执行逻辑
- updating-notes.md 已包含完整的 INSERT/REFRESH 工作流定义
- SKILL.md 只需保留：意图检测 + 路由到 /update skill + 读取 docs/updating-notes.md 的引用

### D3: Scoring rubric 单一来源

**选择**：scoring rubric 只在 `collector.md` agent 定义中完整保留，`collect/SKILL.md` 和 `phases.md` 改为引用。

**理由**：
- collector.md 是实际执行评分的 agent，是自然的权威来源
- collect/SKILL.md 是调度逻辑，不需要内联评分标准
- phases.md 是概览文档，引用即可

### D4: Skill 过滤机制

**选择**：在 `.study-config.yaml` 中新增 `skills.include` / `skills.exclude` 配置项，主 Agent 在 Resource Discovery 阶段根据配置过滤 skill 列表。

**替代方案**：
- 方案 B：按目录分组（study-system/ vs shared/）→ 需要移动文件，影响 comet 等 skill 的发现
- 方案 C：用文件名前缀标记 → 脆弱，依赖命名约定
- 方案 D：完全不改，依赖 Claude Code 的 lazy-loading → 当前不支持

**理由**：
- 配置驱动最灵活，用户可按需调整
- 不移动文件，不影响现有 skill 的发现路径
- 实现简单：主 Agent 读取配置后过滤 Glob 结果

**配置格式**：
```yaml
skills:
  include: []  # 空 = 不过滤（默认加载所有）
  exclude: []  # 排除特定 skill 名
```

**过滤时机**：CLAUDE.md 的 Resource Discovery 阶段，Glob 结果后增加过滤步骤。

### D5: Agent 豁免块精简

**选择**：将 4 个 agent 中的重复豁免块提取为共享指令片段，通过 agent 定义的 `shared_context` 字段引用（如果 Claude Code 支持），否则保留但标注来源。

**现实约束**：Claude Code 的 agent 定义是独立 markdown 文件，不支持 import/include。因此保留 4 份副本，但添加注释标注共同来源，便于未来同步更新。

## Risks / Trade-offs

- **[引用断裂风险]** → 抽取 TODO.md 规则后，如果未来修改了 docs/todo-state-machine.md 但忘记更新引用文件 → 缓解：在 TODO-state-machine.md 顶部添加 "此文件被以下文件引用" 列表
- **[Skill 过滤配置错误]** → 用户配置 exclude 排除了必要 skill → 缓解：配置验证 + 默认值为空（不过滤）
- **[合并 update-workflow 可能遗漏边缘情况]** → 60-70% 重复意味着 30-40% 是独特的 → 缓解：逐行对比后合并，不删除任何功能逻辑
- **[Agent 豁免块仍需 4 份副本]** → 无法从根本上消除 → 可接受，已标注来源
