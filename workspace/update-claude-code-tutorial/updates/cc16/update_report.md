# update_report — cc16「CLAUDE.md 使用指南」

## 基本信息

| 字段 | 值 |
|------|-----|
| note_id | cc16 |
| 笔记标题 | CLAUDE.md 使用指南 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\04-高级功能\CLAUDE.md 使用指南.md` |
| 更新版本 | 2026-08-10 |
| 覆盖版本范围 | v2.1.193 ~ v2.1.226（截至 2026-08-10） |
| 适用资料条目 | SB-23（`/doctor` CLAUDE.md 裁剪建议） |
| 过时点数量 | **8**（见 `stale_map.md`） |
| 原文件是否被修改 | **否**（仅写 `updates/cc16/` 产物） |

## 变更摘要

1. **frontmatter**：`updated: 2026-07-27 → 2026-08-10`；`status` 维持 `updated`（已是更新态）。
2. **精简标准（update_goal 1）**：最佳实践 §1 由「保持简洁（200 行以内）」升级为「保持精简（200 行以内 / 25KB 内）」，正文明确单文件建议 200 行以内或 25KB 以内。
3. **可推导内容不写（SB-23）**：最佳实践 §2 补充「不要写代码库或工具本身就能推导出的内容」，并说明 `/doctor` 会删此类冗余。
4. **`/doctor` 诊断项（SB-23）**：诊断命令表中 `/doctor` 更新为「全量环境体检：诊断安装健康、未用 skills/MCP/插件、CLAUDE.md 裁剪建议、慢 hooks 标记」，别名 `/checkup`；表后追加说明 callout（去重、删可推导内容、合并重复记忆文件、标记慢 hooks）。
5. **工作区信任（update_goal 3）**：规则加载优先级后新增 `[!warning]`，说明项目级 `./CLAUDE.md` 仅在目录被标记为可信工作区后才会被读取。
6. **大白话（update_goal 4）**：核心概念新增 `[!tip] 大白话`（"上岗说明书"比喻）；最佳实践 §1、§2 也各加大白话。
7. **模板示例提醒（update_goal 2）**：完整示例前新增 `[!note]`，提示示例仅作结构参考，落地仍应控制在 200 行 / 25KB 内。
8. **更新记录**：追加 `2026-08-10` 条目，保留 `2026-07-27` 旧条目。

## 核对结论（未过时）

- 文件优先级表、7 种定制机制表、`@import` 5 层嵌套、Hooks 30+ 事件、退出码语义、CLAUDE.md/CLAUDE.local.md 提交约定均与 2026-08 现状一致，未改动。
- 仅应用 SB-23（cc16 适用条目），未越界引入其他 SB 条目。

## 风险项

| 风险 | 说明 | 缓解 |
|------|------|------|
| R1 工作区信任表述 | 「项目级 CLAUDE.md 需工作区信任」依据 update_goal 与官方行为，但具体交互（信任确认文案）未逐字对照官方 docs | 已作为 warning callout 标注；如需更精确表述，可对照 code.claude.com「Trust」文档复核 |
| R2 `/doctor` 细节 | 裁剪/去重/合并记忆文件/慢 hooks 行为基于官方 whats-new w28（SB-23） | 若现行 docs 与本文冲突，以 code.claude.com 为准并回填 |
| R3 示例模板未压缩 | 完整示例保持原样，仅加长度提醒，未改动模板内容本身 | 属刻意保守：保留原写作风格，仅局部 patch |
| R4 status 值未变 | `status: updated` 维持原值 | 语义仍正确（已更新态），无歧义 |

## needs-review

**建议：是（轻度）**

理由：`/doctor` 裁剪建议与工作区信任为本次新引入的事实性表述，虽然来自官方 changelog/what's-new，但属于行为描述而非纯文字优化。建议用户快速浏览 `updated_note.md` 中三处新增 callout（§6 信任 warning、诊断命令表后 /doctor note、核心概念大白话），确认与自身 Claude Code 版本体验一致后，再决定是否替换原 vault 文件。

## 产物清单（`updates/cc16/`）

- `stale_map.md` — 8 处过时点定位与依据
- `update_plan.md` — 8 项 patch 明细与验证要点
- `updated_note.md` — 完整更新稿（未写入原 vault）
- `update_report.md` — 本报告
