# 更新报告 — cc09 Claude Code Memory 完整指南

## 基本信息

| 项 | 值 |
|----|----|
| note_id | cc09 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\03-进阶应用\Claude Code Memory 完整指南.md` |
| 输出目录 | `C:\note\Study-Notes\workspace\update-claude-code-tutorial\updates\cc09\` |
| 原状态 | updated（updated 2026-07-12） |
| 新状态 | updated（updated 2026-08-10） |
| MOC | none（P5 统一处理） |

## 更新摘要

- **CLAUDE.md 最佳实践（update_goal #1）**：单个 CLAUDE.md 目标由「500 行以内」改为官方现行「**200 行以内**」；新增 `[!tip]` `/doctor` 健康体检说明（v2.1.206+）——裁剪已提交 CLAUDE.md、删除可由代码库推导的内容、合并重复记忆文件、标记慢 hooks；FAQ 新增「CLAUDE.md 太长或重复怎么办」问答。
- **三层记忆体系核对（update_goal #2）**：逐段核对 CLAUDE.md / Auto Memory / 参考文档相关内容。修正 Auto Memory 加载行为（前 200 行 **或 25KB**）、`autoMemoryDirectory` 作用域（任意 settings 层级 + 项目级工作区信任）、导入深度（5 层 → **4 层**）。
- **Auto Memory 开关/命名规范（update_goal #3）**：控制方式改为官方现行三种——`/memory` 会话内开关、`autoMemoryEnabled` 设置、`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`；删除旧 `=0 强制开启` 描述（未见于官方文档）并转 `[!warning]` 说明；补充 `modified` 时间戳字段（v2.1.214+）与 `MEMORY.md` 索引定位。
- **核心概念大白话（update_goal #4）**：通俗理解新增 `[!tip] 大白话`——三层记忆体系比喻（CLAUDE.md 项目说明书 / Auto Memory 工作笔记本 / 参考文档资料柜）。
- **命令与 FAQ 同步**：命令参考新增 `/context`、`/doctor`；`/memory` 小节更新为列出记忆位置、开关 Auto Memory、打开 Auto Memory 文件夹（GUI 编辑器 v2.1.216+）；FAQ 调试第一步改用 `/context`。
- **顺带修复**：原文件 3 处乱码（第 26/42/491 行，`编���规范` → `编码规范`、`��终记录错误` → `始终记录错误`）。
- **frontmatter**：`updated: 2026-07-12 → 2026-08-10`，`status: updated` 保持。
- **更新记录**：文末追加 2026-08-10 条目。
- 未重写未过时段落：Memory 架构层级表、模块化规则系统、安装配置、实用示例、`claudeMdExcludes` 等章节已核对，2026-08 描述仍准确，未改动。

## 引用来源

| 来源 | 用途 |
|------|------|
| SB-23（CLAUDE.md 维护建议） | `/doctor` 提议裁剪、合并重复记忆文件、标记慢 hooks、「可推导内容不写」 |
| SB-10（/doctor 全量体检） | `/doctor` 别名 `/checkup`，慢 hooks 标记佐证 |
| 官方 Memory 文档（code.claude.com/docs/en/memory，2026-08-10 抓取） | 加载 200 行/25KB、`autoMemoryDirectory` 作用域、`autoMemoryEnabled` 开关、`modified` 字段（v2.1.214+）、导入深度 4 层、CLAUDE.md 200 行、`/context`、`/memory` 行为 |

> 以 code.claude.com 现行文档为准（来源库约定：若与本文冲突，以官方文档为准）。本次主动抓取官方 Memory 文档核对，而非仅依赖来源库摘要。

## 未处理风险

1. **`CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` 语义移除**：旧笔记写「`=0` 强制开启 Auto Memory」，官方文档仅明确 `=1` 关闭，未见 `=0` 行为说明；社区报告 `=0` 只停用自动记忆写入而非完整功能。本次按官方文档修正并转 `[!warning]` 说明。若团队环境实际依赖 `=0` 强制开启行为，写回前需确认。
2. **来源库适用性标注差异**：SB-23 在 `source_bank.md` 的「适用笔记」标为 cc16，但本任务参数明确指定 cc09 适用。按任务参数执行（`/doctor` 维护建议对 Memory 篇同样成立），已在报告中说明。
3. **3 处乱码修复为额外改动**：原文件存在编码损坏（U+FFFD），本次修复为显然的预期文本。此改动超出「同步 2026-08」范围，写回前建议用户确认。
4. **版本号精确性**：`/doctor` trim check（v2.1.206+）、`modified` 字段（v2.1.214+）、GUI 编辑器 `/memory`（v2.1.216+）等版本号来自官方文档单句，未逐条回 changelog 原文交叉验证。
5. **未大范围联网**：本次以官方 Memory 文档 + 来源库核对为主，未逐一抓取 changelog 全文与社区三层架构文。

## 结论

- 发现过时点：**13 处**（frontmatter 日期、Auto Memory 加载行为、`autoMemoryDirectory` 作用域、Auto Memory 开关、导入深度 2 处、最佳实践行数、`/doctor` 缺失、`/memory` 行为、命令参考 2 行、FAQ 调试、FAQ 比较表、乱码 3 处）+ 1 处 `[!tip] 大白话` 增强 + 更新记录。
- **是否需要 needs-review：否**。核心变更有官方 Memory 文档与来源库明确支持，无需要推断的精确结构；两处判断性改动（`=0` 语义移除、乱码修复）建议用户写回前快速审阅 `updated_note.md`。
