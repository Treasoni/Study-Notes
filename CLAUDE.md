# Study System

学习笔记自动化生产系统。

## Codex / Claude Code 同步

本项目同时维护 `.codex/` 与 `.claude/` 两套配置。当前约定是：

1. 新增或修改工作流能力时，优先改 `.codex/`。
2. 改完后运行：
   ```bash
   .codex/scripts/sync-codex-to-claude.sh
   ```
3. 同步脚本会把可迁移的 skills、agents、rules、scripts 复制到 `.claude/`，并把路径从 `.codex` 转成 `.claude`。
4. Claude Code 专属 hooks 不由 Codex hooks 覆盖；详见 `.claude/rules/common/hooks.md`。

## 可用工作流

每个工作流由「planner + orchestrator + 模板文件对」组成：

| 工作流 | 对应 planner | 模板文件对 | 用途 |
|-------|-------------|-----------|------|
| learning-note-flow | `/research-planner` | learning-note-flow.md / learning-note-todo.md | 完整学习笔记生产 + Obsidian 发布 + MOC 同步 |
| legacy-note-import-flow | `/legacy-note-importer` | legacy-note-import-flow.md / legacy-note-import-todo.md | 已有旧笔记批量导入、规范化、可选更新与 MOC 同步 |
| batch-note-update-flow | `/batch-note-updater` | batch-note-update-flow.md / batch-note-update-todo.md | 多篇既有笔记批量更新、逐篇局部 patch 与 MOC 同步 |

> 新增工作流：在 `.claude/skills/workflow-orchestrator/templates/` 创建说明书 + todo 模板文件对，并新建对应 planner 或入口 skill。
> orchestrator 通常不直接面向用户，由各 planner 或入口 skill 调用。上游负责领域特定的意图澄清，orchestrator 负责生成 todo.md。

## 核心原则

### 必须执行 todo.md

**每个技能/Agent 启动时必须:**
1. 读取项目目录下的 `todo.md`
2. 确认当前阶段状态
3. 不可跳步，不可不做

**状态流转（[PN] 标记精准定位，不跨阶段污染）**:
```
[PN] ⬜ 未开始 → [PN] 🔲 进行中 → [PN] ✅ 已完成
```

### 断点恢复机制

1. **读取状态**: 每个技能启动时读取 todo.md
2. **验证前置**: 检查前置阶段是否为 ✅
3. **更新状态**: 开始时改为 🔲，完成后改为 ✅
4. **阶段推进**: 更新 `当前阶段` 字段

## 文件结构

```
${WORKSPACE_PATH:-./workspace}/
├── {topic-slug}/
│   ├── 00_intent.md
│   ├── 01_explore_result.md
│   ├── 02_deep_research.md
│   ├── 03_outline.md
│   ├── todo.md
│   ├── chapters/
│   └── output/
└── ...
```

## 技能依赖关系

完整编排流程见 `.claude/skills/workflow-orchestrator/SKILL.md`，各工作流的阶段执行流见 `templates/` 下对应说明书。核心链路：

```
research-planner → workflow-orchestrator（生成 todo.md）
→ research-collector → outline-generator → chapter-writer
→ note-assembler → note-beautifier → moc-organizer
```

## 工作流执行规则

### 阶段完成检查点

每阶段结束都必须让用户确认后才进入下一阶段:

| 阶段 | 检查点内容 |
|------|-----------|
| 0 → 1 | 用户确认意图文件和研究计划 |
| 1 → 2 | 用户确认素材质量 |
| 2 → 3 | 用户确认大纲顺序和深度 |
| 3 → 4 | 用户确认大纲（大纲模式） |
| 4 → 5 | 所有章节写作完成 |
| 5 → 6 | 用户确认组装结果和 Obsidian 输出位置 |
| 6 → 7 | 用户确认是否同步 MOC |

### 错误处理

| 情况 | 处理方式 |
|------|---------|
| 缺少意图文件 | 重新调用 `/research-planner` |
| 缺少素材文件 | 重新调用 `/research-collector` |
| 缺少大纲文件 | 重新调用 `outline-generator` |
| 缺少章节文件 | 重新调用 `chapter-writer` |
| 缺少输出位置 | 先保存到项目 `output/`，等待用户指定 Obsidian 位置 |
| 已有一批旧笔记要接入项目 | 调用 `legacy-note-importer`，先盘点和生成迁移计划 |
| 多篇旧笔记过时 | 调用 `batch-note-updater`，先生成更新清单和批量计划 |
| 旧笔记过时 | 调用 `note-updater`，不要重跑完整新笔记流程 |
