# 旧笔记导入工作流

## 工作流描述

将已有 Markdown/Obsidian 笔记批量接入 Study System。流程先盘点旧笔记，再生成迁移计划，经用户确认后按批次规范化、可选更新过时内容，最后发布到项目 output 或 Obsidian vault 并同步 MOC。

## 阶段定义

### 阶段 0: 导入意图确认
- **负责技能**: /legacy-note-importer
- **前置条件**: 用户提供旧笔记目录或文件
- **检查项**:
  - [ ] source_path 已确认
  - [ ] source_scope/source_glob 已确认
  - [ ] 输出策略已确认（项目 output / Obsidian vault / 原地 patch）
  - [ ] stale_policy 已确认（skip / flag-only / update-with-note-updater）
  - [ ] 覆盖策略已确认
  - [ ] 导入意图已保存：`./00_import_intent.md`
- **输出文件**: `00_import_intent.md`
- **状态**: [P0] ⬜ 未开始

### 阶段 1: 旧笔记盘点
- **负责技能**: /legacy-note-importer
- **前置条件**: 阶段 0 完成
- **检查项**:
  - [ ] 已扫描目标范围内的笔记文件
  - [ ] 已记录标题、路径、大小、修改时间和格式特征
  - [ ] 已标记非 Markdown、重复标题、附件风险
  - [ ] 清单已保存：`./01_inventory.md`
  - [ ] 机器清单已保存：`./inventory.csv`
- **输出文件**: `01_inventory.md`, `inventory.csv`
- **状态**: [P1] ⬜ 未开始

### 阶段 2: 迁移计划确认
- **负责技能**: /legacy-note-importer
- **前置条件**: 阶段 1 完成
- **检查项**:
  - [ ] 已按主题/目录/状态分组
  - [ ] 每篇笔记已标注动作：normalize/update/merge/split/skip
  - [ ] 第一批处理列表已生成
  - [ ] 风险和需要用户确认的问题已列出
  - [ ] 迁移计划已保存：`./02_migration_plan.md`
  - [ ] 用户已确认计划后才进入下一阶段
- **输出文件**: `02_migration_plan.md`
- **状态**: [P2] ⬜ 未开始

### 阶段 3: 批量规范化
- **负责技能**: /legacy-note-importer + /note-beautifier
- **前置条件**: 阶段 2 完成
- **检查项**:
  - [ ] 已按 batch_size 分批读取源文件
  - [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
  - [ ] 原始文件未被覆盖，除非用户确认
  - [ ] 规范化结果已保存到 `./normalized/` 或用户指定位置
  - [ ] 批处理日志已追加：`./03_batch_log.md`
- **输出文件**: `normalized/*.md`, `03_batch_log.md`
- **状态**: [P3] ⬜ 未开始

### 阶段 4: 过时内容处理（可选）
- **负责技能**: /note-updater
- **前置条件**: 阶段 3 完成，且迁移计划存在 update 项
- **检查项**:
  - [ ] 已读取 update 项和最小上下文
  - [ ] 已生成 stale map
  - [ ] 已按用户确认的策略局部更新
  - [ ] 更新报告已保存：`./updates/update_report.md`
- **输出文件**: `updates/update_report.md`
- **状态**: [P4] ⬜ 未开始（如无 update 项，先启动 P4，再用 `todo-state.sh skip P4 "无 update 项"` 记录用户确认后跳过）

### 阶段 5: 发布与 MOC 同步
- **负责技能**: /legacy-note-importer + /moc-organizer
- **前置条件**: 阶段 3 完成，阶段 4 完成或跳过
- **检查项**:
  - [ ] 已保存到项目 output 或用户指定 vault
  - [ ] 已处理同名文件和覆盖确认
  - [ ] 如提供 MOC，已同步索引且未复制正文
  - [ ] 导入报告已保存：`./04_import_report.md`
- **输出文件**: `04_import_report.md`, 可选 MOC 文件
- **状态**: [P5] ⬜ 未开始

## 目录结构

```text
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/
├── 00_import_intent.md
├── 01_inventory.md
├── inventory.csv
├── 02_migration_plan.md
├── 03_batch_log.md
├── 04_import_report.md
├── workflow-runs/import-{source}.workflow.md
├── normalized/
└── updates/
```

## 阶段完成检查点

每阶段结束都必须让用户确认后才进入下一阶段：

| 阶段 | 检查点内容 |
| --- | --- |
| 0 → 1 | 用户确认导入范围、输出位置和覆盖策略 |
| 1 → 2 | 用户确认盘点结果可信 |
| 2 → 3 | 用户确认迁移计划和第一批处理列表 |
| 3 → 4 | 用户确认规范化样例符合预期 |
| 4 → 5 | 用户确认过时内容处理结果，或确认跳过 |
| 5 | 用户确认发布位置和 MOC |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| source_path 不存在 | 停在阶段 0，请用户提供有效路径 |
| 大量非 Markdown 文件 | 阶段 1 标记为 non-markdown，等待转换策略 |
| 重复标题 | 阶段 2 给出重命名或目录分组方案 |
| 附件缺失 | 阶段 2 标记风险，不自动删除链接 |
| 同名目标文件已存在 | 阶段 5 等待用户确认 copy/overwrite/patch |
| 笔记内容过时 | 阶段 4 调用 note-updater，不在导入阶段整篇重写 |
