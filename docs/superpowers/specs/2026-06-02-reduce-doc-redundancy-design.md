---
comet_change: reduce-doc-redundancy-and-skill-bloat
role: technical-design
canonical_spec: openspec
archived-with: 2026-06-02-reduce-doc-redundancy-and-skill-bloat
status: final
---

# Design: Reduce Doc Redundancy and Skill Bloat

## Context

Study System 经过多次迭代，文档和 skill 定义产生大量冗余：
- TODO.md 状态机规则分散在 17 个文件中，重复定义 9-12 次
- update-workflow/SKILL.md 与 docs/updating-notes.md 60-70% 重复
- scoring rubric 在 3 个文件中完全相同
- 51 个 skills 全量注入系统提示，其中 37 个是开发时 skills，项目运行时不需要

## Design Decisions

### D1: TODO.md 状态机抽取为独立参考文档

创建 `docs/todo-state-machine.md` 作为唯一权威定义。

**文件结构**：
```
docs/todo-state-machine.md
├── 被引用文件列表（顶部，便于同步维护）
├── 状态定义（create → phase gates → delete）
├── 工具映射（Read/Write/Bash）
├── 三种工作流变体（5-phase / 7-step / REFRESH mini）
└── 路径约定（{SYSTEM_ROOT}/TODO.md）
```

**引用格式**：纯引用 `See docs/todo-state-machine.md`，不内联摘要。

**被引用文件**：
- CLAUDE.md
- docs/phases.md
- docs/experience-notes.md
- docs/updating-notes.md
- .claude/skills/collect/SKILL.md
- .claude/skills/write/SKILL.md
- .claude/skills/beautify/SKILL.md

### D2: 合并 update-workflow 与 updating-notes.md

保留 `docs/updating-notes.md` 为权威文档，`update-workflow/SKILL.md` 精简为路由逻辑。

**update-workflow/SKILL.md 精简后内容**：
- 意图检测逻辑（INSERT/REFRESH 判断表）
- 路由到 /update skill
- 引用 `docs/updating-notes.md` 获取完整工作流

### D3: Scoring Rubric 单一来源

scoring rubric 只在 `collector.md` agent 定义中完整保留。

**变更**：
- collect/SKILL.md → 替换为引用 collector.md
- phases.md Phase 1 → 替换为引用 collector.md

### D4: Skill 分类机制（mode）

Skills 分为两类，互不干扰：

**project（项目运行时）**：
- 核心流程：collect, curate, write, beautify, evaluate, digest
- 更新流程：update, update-workflow, requirement-discovery
- 链接管理：moc, generate-links, fix-broken-links, delete-file
- Obsidian 工具：obsidian-cli, obsidian-markdown

**dev（开发时）**：
- Comet 系列：comet-open/design/build/verify/archive/hotfix/tweak
- OpenCLI 系列：adapter-author/autofix/browser/usage
- Brainstorming 系列
- Openspec 系列
- 开发工具：writing-plans, executing-plans, subagent-driven-development
- 测试调试：test-driven-development, systematic-debugging
- Git 工作流：using-git-worktrees, finishing-a-development-branch
- 协作：dispatching-parallel-agents, using-superpowers
- Code Review：requesting-code-review, receiving-code-review
- 验证：verification-before-completion
- 其他：sortspec-generator, tool-registry, smart-search, defuddle, json-canvas, writing-skills

**配置格式**：
```yaml
skills:
  mode: project  # "project" | "dev" | "all"
```

- `project` → 只加载项目运行时 skills（默认）
- `dev` → 只加载开发时 skills
- `all` → 加载所有（当前行为，兼容）

**过滤时机**：CLAUDE.md 的 Resource Discovery 阶段，Glob 结果后根据 mode 过滤。

**校验**：启动时检查 mode 值是否合法，不合法时 warn 并回退到 `all`。

### D5: Agent 豁免块标注来源

4 个 agent 定义中的重复豁免块添加注释标注共同来源，便于未来同步更新。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 引用断裂（修改 todo-state-machine.md 忘记更新引用） | 文件顶部标注"被引用文件列表" |
| Skill mode 配置错误 | 默认值 project + 启动时校验 |
| 合并 update-workflow 遗漏边缘情况 | 逐行对比后合并，不删除功能逻辑 |
| Agent 豁免块仍需 4 份副本 | 添加注释标注共同来源 |
| 新增 dev skill 时需手动更新 mode 分类 | 在 mode 分类处添加注释说明如何添加新 skill |
