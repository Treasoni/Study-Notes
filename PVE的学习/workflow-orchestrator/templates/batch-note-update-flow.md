# 批量旧笔记更新工作流

## 工作流描述

对一个目录、文件列表或 Obsidian vault 子目录中的多篇既有笔记进行批量更新。流程先建立更新清单，再生成批量计划，经用户确认后逐篇调用 `note-updater` 做局部 patch，最后汇总报告并可选同步 MOC。

## 阶段定义

### 阶段 0: 批量更新意图确认
- **负责技能**: /batch-note-updater
- **前置条件**: 用户提供 source_path 和 update_goal
- **检查项**:
  - [ ] source_path/source_scope/source_glob 已确认
  - [ ] update_goal 已确认
  - [ ] destination_mode 已确认
  - [ ] batch_size 已确认
  - [ ] shared_research 策略已确认
  - [ ] 批量更新意图已保存：`./00_batch_update_intent.md`
- **输出文件**: `00_batch_update_intent.md`
- **状态**: [P0] ⬜ 未开始

### 阶段 1: 更新清单
- **负责技能**: /batch-note-updater
- **前置条件**: 阶段 0 完成
- **检查项**:
  - [ ] 已扫描目标范围内的 Markdown 笔记
  - [ ] 已记录 frontmatter、标题、目录、更新时间和关键词命中
  - [ ] 已标记 candidate/ready/needs-review/skip
  - [ ] 更新清单已保存：`./01_update_inventory.md`
  - [ ] 机器清单已保存：`./update_inventory.csv`
- **输出文件**: `01_update_inventory.md`, `update_inventory.csv`
- **状态**: [P1] ⬜ 未开始

### 阶段 2: 批量更新计划
- **负责技能**: /batch-note-updater
- **前置条件**: 阶段 1 完成
- **检查项**:
  - [ ] 已按主题、版本、目录或优先级分组
  - [ ] 每篇笔记已标注动作：update/flag-only/skip/needs-review
  - [ ] 第一批处理列表已生成
  - [ ] 覆盖风险和需用户确认项已列出
  - [ ] 批量更新计划已保存：`./02_batch_update_plan.md`
  - [ ] 用户已确认计划后才进入下一阶段
- **输出文件**: `02_batch_update_plan.md`
- **状态**: [P2] ⬜ 未开始

### 阶段 3: 共享资料收集（可选）
- **负责技能**: /batch-note-updater 或 /research-collector
- **前置条件**: 阶段 2 完成，且 shared_research 为 yes/auto 并判定需要
- **检查项**:
  - [ ] 已确定共享资料适用的笔记范围
  - [ ] 已收集最小必要资料
  - [ ] 每条资料已记录 URL、日期、适用范围和摘要
  - [ ] 来源库已保存：`./shared_research/source_bank.md`
- **输出文件**: `shared_research/source_bank.md`
- **状态**: [P3] ⬜ 未开始 | ⏭️ 跳过

### 阶段 4: 逐篇局部更新
- **负责技能**: /note-updater
- **前置条件**: 阶段 2 完成，阶段 3 完成或跳过
- **检查项**:
  - [ ] 已按 batch_size 分批处理
  - [ ] 每篇笔记已生成 stale map
  - [ ] 每篇笔记已局部更新或标记需复核
  - [ ] 原文未被覆盖，除非 destination_mode 为 patch-in-place 且用户已确认
  - [ ] 批处理日志已追加：`./03_batch_update_log.md`
- **输出文件**: `updates/*/update_report.md`, `03_batch_update_log.md`
- **状态**: [P4] ⬜ 未开始

### 阶段 5: 汇总与 MOC 同步
- **负责技能**: /batch-note-updater + /moc-organizer
- **前置条件**: 阶段 4 完成
- **检查项**:
  - [ ] 已汇总更新、跳过、失败和需复核数量
  - [ ] 已汇总每篇输出路径和风险
  - [ ] 如提供 MOC，已同步索引且未复制正文
  - [ ] 批量更新报告已保存：`./04_batch_update_report.md`
- **输出文件**: `04_batch_update_report.md`, 可选 MOC 文件
- **状态**: [P5] ⬜ 未开始

## 目录结构

```text
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/
├── 00_batch_update_intent.md
├── 01_update_inventory.md
├── update_inventory.csv
├── 02_batch_update_plan.md
├── 03_batch_update_log.md
├── 04_batch_update_report.md
├── todo.md
├── shared_research/
│   └── source_bank.md
└── updates/
    └── {note_id}/
        ├── stale_map.md
        ├── update_plan.md
        ├── updated_note.md
        └── update_report.md
```

## 阶段完成检查点

每阶段结束都必须让用户确认后才进入下一阶段：

| 阶段 | 检查点内容 |
| --- | --- |
| 0 → 1 | 用户确认更新范围、目标、输出模式和批大小 |
| 1 → 2 | 用户确认更新清单可信 |
| 2 → 3/4 | 用户确认批量计划和第一批处理列表 |
| 3 → 4 | 用户确认共享资料足够且来源可信 |
| 4 → 5 | 用户确认逐篇更新结果或需复核项 |
| 5 | 用户确认汇总报告和 MOC |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| source_path 不存在 | 停在阶段 0，请用户提供有效路径 |
| update_goal 不清楚 | 停在阶段 0，请用户明确版本、主题或修正目标 |
| 大量笔记不相关 | 阶段 1 标记 skip，不进入更新 |
| 共享资料来源不可靠 | 阶段 3 等待用户确认或补充资料 |
| 单篇结构异常 | 阶段 4 标记 needs-review，不强行 patch |
| 同名目标文件已存在 | 等待用户确认 copy/overwrite/patch 策略 |
