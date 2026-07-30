---
workflow_id: legacy-note-import-flow
workflow_name: 旧笔记导入工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "{run_id}"
task: "{topic}"
created_from: ".claude/workflows/legacy-note-import-flow/state-template.md"
topic: "{topic}"
project_slug: "{project_slug}"
created_at: "{date}"
last_updated: "{date}"
current_phase: P0
current_status: not_started
mode: standard
confirmed_phases: ""
skippable_phases: "P4"
mode_dependent_skips: ""
allowed_modes: ""
mode_change_phase: ""
blocked_reason: ""
---

# 旧笔记导入工作流 - 执行检查清单

> 工作流：legacy-note-import-flow
> 主题：{topic}
> 运行标识：{run_id}
> 项目标识：{project_slug}
> 创建时间：{date}
> 当前阶段：阶段 0
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：导入意图确认
- [ ] source_path 已确认
- [ ] source_scope/source_glob 已确认
- [ ] 输出策略已确认（项目 output / Obsidian vault / 原地 patch）
- [ ] stale_policy 已确认（skip / flag-only / update-with-note-updater）
- [ ] 覆盖策略已确认
- [ ] 导入意图已保存：`./00_import_intent.md`

> [P0] ⬜ 未开始

---

## 阶段 1：旧笔记盘点
- [ ] 已扫描目标范围内的笔记文件
- [ ] 已记录标题、路径、大小、修改时间和格式特征
- [ ] 已标记非 Markdown、重复标题、附件风险
- [ ] 清单已保存：`./01_inventory.md`
- [ ] 机器清单已保存：`./inventory.csv`

> [P1] ⬜ 未开始

---

## 阶段 2：迁移计划确认
- [ ] 已按主题/目录/状态分组
- [ ] 每篇笔记已标注动作：normalize/update/merge/split/skip
- [ ] 第一批处理列表已生成
- [ ] 风险和需要用户确认的问题已列出
- [ ] 迁移计划已保存：`./02_migration_plan.md`
- [ ] 用户已确认计划后才进入下一阶段

> [P2] ⬜ 未开始

---

## 阶段 3：批量规范化
- [ ] 已按 batch_size 分批读取源文件
- [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [ ] 原始文件未被覆盖，除非用户确认
- [ ] 规范化结果已保存到 `./normalized/` 或用户指定位置
- [ ] 批处理日志已追加：`./03_batch_log.md`

> [P3] ⬜ 未开始

---

## 阶段 4：过时内容处理（可选）
- [ ] 已读取 update 项和最小上下文
- [ ] 已生成 stale map
- [ ] 已按用户确认的策略局部更新
- [ ] 更新报告已保存：`./updates/update_report.md`

> [P4] ⬜ 未开始

---

## 阶段 5：发布与 MOC 同步
- [ ] 已保存到项目 output 或用户指定 vault
- [ ] 已处理同名文件和覆盖确认
- [ ] 如提供 MOC，已同步索引且未复制正文
- [ ] 导入报告已保存：`./04_import_report.md`

> [P5] ⬜ 未开始

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| | | |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| | | | |

---

## 批处理记录

| 时间 | 批次 | 文件数 | 成功 | 需复核 | 输出位置 |
|------|------|--------|------|--------|----------|
| | | | | | |

---

## 最终产出

- **源路径**：
- **处理文件数**：
- **规范化文件数**：
- **跳过文件数**：
- **更新文件数**：
- **输出模式**：
- **文件路径**：
- **Obsidian Vault**：
- **MOC 路径**：
