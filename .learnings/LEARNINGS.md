# LEARNINGS.md

活跃学习记录。**当前无活跃记录** —— 最近一次维护：2026-09-23（`/maintain-learnings`）。

本轮把 7 条「教训已进 `RULES.md`、记录仍留在活跃文件」的记录逐条追回源头，落到可执行机制后
归档；原文摘要、修复路径、验证方式与遗留项见 `.learnings/archive/2026-09-23-maintenance.md`：

- `LRN-20260912-011` workflow — vault 与 workspace 副本漂移未登记 → `note-updater` 新增漂移登记步骤
- `LRN-20260923-014` workflow — 并行写作跨章口径未冻结 → `learning-note-flow` 阶段 4 新增口径表检查点
- `LRN-20260923-015` workflow — workflow 定义调用了未实现的动作 → `workflow-health-check.sh` 新增动作守卫
- `LRN-20260923-017` correction — 逐字引文串成引文墙 → `chapter-writer` 摆放规范与验收清单已在位

更早一批（`digest` 于同日压缩）见 `.learnings/archive/2026-09-23-archived.md`。

新增记录请按 `digest` 的格式追加到本文件末尾：

```markdown
## [LRN-YYYYMMDD-NNN] area — 一句话结论

**Logged**: YYYY-MM-DD
**Priority**: high | medium | low
**Status**: pending | in_progress | resolved
**Area**: 受影响的 skill / agent / workflow

### Summary
### Details
### Suggested Action
```

只有**已落到机制并被验证**的记录才可归档（`.learnings/archive/YYYY-MM-DD-maintenance.md`）；
未修复、未验证或仍需观察的记录继续留在本文件。

---