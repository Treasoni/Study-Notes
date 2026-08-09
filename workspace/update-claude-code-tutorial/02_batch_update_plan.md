# 批量更新计划 — Claude Code 教程（同步到 2026-08 最新版）

> 基于 `01_update_inventory.md`（19 篇 ready + 4 篇 skip）
> 计划版本：v1（2026-08-09，待用户确认）

## 1. 更新目标与判断依据

**目标**：逐篇核对 19 篇 Claude Code 教程，同步到 2026-08-09 的 Claude Code 现状，补充 2026-07/08 新功能，修正过时内容。

**判断依据**：
- 14 篇 `updated` 停在 **2026-07-12**，距今近 1 个月，可能缺少 7–8 月发布的新功能与行为变更。
- 3 篇 07-27 ~ 08-07 更新（cc01/cc05/cc16）以低强度核对为主。
- 2 篇 `draft`（cc06 settings.json、cc19 Prompt Caching）需要补全并核对最新规范。
- 9 篇含时效性关键词（已废弃/旧版/即将/beta/不再支持/计划支持），共 20 处，需逐处核实。

## 2. 笔记分组

| 组 | 主题 | 笔记 id | 说明 |
|----|------|---------|------|
| A | 基础功能 | cc01–cc06 | 入门 / 常用功能 / CLI / 会话 / 模型 / settings.json |
| B | 进阶应用 | cc07–cc11 | Checkpoints / Hooks / Memory / Subagents / 插件 |
| C | 高级功能 | cc12–cc19 | 高级总览 / Slash / MCP / Skills / CLAUDE.md / 定时任务 / Dynamic Workflows / Caching |

## 3. 每篇笔记动作

| 动作 | 数量 | 笔记 |
|------|------|------|
| `update` | 19 | cc01–cc19 |
| `flag-only` | 0 | — |
| `needs-review` | 0 | — |
| `skip` | 4 | cc-skip-01~04（MOC / sortspec / 2 遗留报告） |

> 单篇动作细化：由 note-updater 逐篇产出 stale map 后，在 `updates/{note_id}/update_plan.md` 中给出「保留/更新/删除/新增」清单；若单篇范围不清则标记 needs-review 不强行 patch。

## 4. 共享资料包：需要（yes）

所有笔记共享同一更新目标「Claude Code 2026-08 现状」，P3 建立 `shared_research/source_bank.md`，覆盖：

- Claude Code 2026-07/08 版本发布说明与主要行为变更（Changelog / Release Notes）。
- 官方文档关键页：CLI 参考、settings.json、Slash Commands、Skills、Hooks、MCP、Subagents、Memory、Checkpoints、Agent Teams / Dynamic Workflows。
- 每条资料记录 URL、日期、适用笔记范围、100–200 字摘要。

单篇专项资料（如某篇独有命令的细节）仍由 note-updater 逐篇补充，不塞进共享库。

## 5. 第一批处理列表（batch_size = 3）

**批次 1：cc01、cc06、cc12**

| id | 笔记 | 优先级 | 理由 |
|----|------|--------|------|
| cc01 | 如何使用Claude code（入门入口） | 中 | 系列入口，先确认最新安装/入门流程 |
| cc06 | settings.json 配置详解 | **高** | draft 待补全 + 3 处关键词，配置变化最大 |
| cc12 | Claude Code 高级功能（总览） | **高** | 总览新能力，后续批次参考基线 |

批次 2 起按「组 A → B → C」顺序推进，每批 3 篇。

## 6. 输出模式与覆盖风险

- **destination_mode**：`patch-in-place`（直接改原文件）。
- **安全流程**：每篇由 note-updater 输出到 `updates/{note_id}/updated_note.md`，git 记录基线后，**逐篇经用户确认再写回原文件**；未确认前原文件不动。
- **覆盖风险**：
  1. patch-in-place 覆盖 → git 基线 + 逐篇确认，异常暂停。
  2. 20 处时效性关键词多为「旧版 vs 新版」对照，需逐处核实，不机械删除。
  3. 2 篇 draft 补全时保留原结构，仅补缺失内容。
  4. MOC 只在 P5 更新，P4 阶段不触碰。

## 7. 待确认项

- [ ] 用户确认更新清单可信（P1→P2）
- [ ] 用户确认分组、每篇动作、第一批处理列表（P2→P3/4）
- [ ] P3 共享资料完成后，用户确认来源可信（P3→P4）
