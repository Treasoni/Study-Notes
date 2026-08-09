# 更新计划 — cc09 Claude Code Memory 完整指南

> 输出目录：`workspace/update-claude-code-tutorial/updates/cc09/`。原文件未改动，产物写入本目录。

## 过时点清单

| 序号 | 位置 | 现状 | 过时原因 | 处理方式 |
|------|------|------|---------|---------|
| U1 | frontmatter `updated` | 2026-07-12 | 需同步 2026-08 现状 | `updated: 2026-08-10`（`status: updated` 保持） |
| U2 | Auto Memory「加载行为」/ 目录结构注释 | 前 200 行 | 官方现行：前 200 行 **或前 25KB**（取先到者） | 补充 25KB 限制与 `MEMORY.md` 索引定位 |
| U3 | `autoMemoryDirectory` 作用域 | 只能在用户级/本地配置 | 官方现行：可从任意 settings 层级读取 | 更新 JSON 注释 + `[!note]` 作用域说明（项目级需工作区信任） |
| U4 | 控制 Auto Memory | env `0/1/未设置`（含 `=0 强制开启`） | 官方现行：默认开启，三种控制方式；`=0` 未见官方文档 | 重写控制表为 `/memory` / `autoMemoryEnabled` / `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`，`=0` 改 `[!warning]` |
| U5 | 导入深度（导入特性 + FAQ） | 最大 5 层 | 官方现行：最大 4 层递归导入 | 两处 5 → 4 |
| U6 | 最佳实践「太长」 | 500 行以内 | 官方现行：单个 CLAUDE.md 目标 200 行以内 | 改为 200 行以内 |
| U7 | 最佳实践 / 常见问题 | 无 `/doctor` 维护说明 | SB-23 + 官方 troubleshooting：`/doctor` 提议裁剪、合并重复记忆文件、标记慢 hooks | 新增 `[!tip]` 健康体检说明 + FAQ 新问答 |
| U8 | `/memory` 命令 | 仅「编辑记忆文件」 | 官方现行：列出记忆位置、开关 Auto Memory、打开 Auto Memory 文件夹 | 更新用途与功能列表 |
| U9 | Memory 命令快速参考 | 缺 `/context`、`/doctor` | 官方：`/context` 核对已加载记忆、`/doctor` 维护 | 表格新增两行 |
| U10 | FAQ「调试 Memory 加载」 | 用 `/status` | 官方：`/context` 下核对 Memory files | 步骤改用 `/context` + `/memory` |
| U11 | 核心概念 | 无 `[!tip] 大白话` | 用户偏好 | 通俗理解后新增三层记忆体系大白话 |
| U12 | 原文件乱码 3 处 | `编���规范` 等 | 原文编码损坏 | 修正为 `编码规范` / `编码规范文档` / `始终记录错误` |
| U13 | 文末 | 无本次变更留痕 | 流程要求 | 追加「更新记录」2026-08-10 条目 |

## 新增/更新内容与来源核对

| 变更 | 来源 | 说明 |
|------|------|------|
| `MEMORY.md` 前 200 行或 25KB | 官方 Memory 文档 | 启动加载取先到者；`MEMORY.md` 为索引 |
| `autoMemoryDirectory` 任意层级 + 工作区信任 | 官方 Memory 文档 | 项目级 `.claude/settings.json` 需信任对话框；值须绝对路径或 `~/` |
| `autoMemoryEnabled` / `/memory` 开关 | 官方 Memory 文档 | 开关写入 `~/.claude/settings.json`；env 仅 `=1` 关闭 |
| `modified` 时间戳（v2.1.214+） | 官方 Memory 文档 | 带 frontmatter 的记忆文件写入时记录 ISO 8601 |
| 导入深度 4 层 | 官方 Memory 文档 | "maximum depth of four hops" |
| CLAUDE.md 200 行目标 | 官方 Memory 文档 | "target under 200 lines per CLAUDE.md file" |
| `/doctor` 裁剪/合并/慢 hooks | SB-23 + 官方 Memory 文档 troubleshooting | 剪掉可推导内容，保留踩坑/理由/非默认约定；trim check 需 v2.1.206+ |
| `/context` 核对 Memory files | 官方 Memory 文档 troubleshooting | 替代 `/status` 作为调试第一步 |
| `/memory` 列位置 / 开关 / GUI 行为 | 官方 Memory 文档 | GUI 编辑器 v2.1.216+ 不阻塞会话 |
| 三层记忆体系大白话 | 用户偏好 + 官方「CLAUDE.md vs auto memory」 | CLAUDE.md / Auto Memory / 参考文档三层 |

## 执行步骤

1. 更新 frontmatter：`updated: 2026-08-10`。
2. 核心概念·通俗理解比喻列表后新增 `[!tip] 大白话`（三层记忆体系）。
3. 修正 3 处原文件乱码。
4. Memory 命令快速参考新增 `/context`、`/doctor` 两行；更新 `/memory` 行用途。
5. `/memory` 命令小节更新用途与功能列表。
6. Auto Memory：加载行为补 25KB；目录结构注释补 25KB；版本要求补 `modified` 字段；自定义目录更新作用域 `[!note]`；控制 Auto Memory 重写（表格 + 示例 + `[!warning]` 说明 `=0` 不官方）。
7. 导入特性 + FAQ 导入深度 5 → 4。
8. 最佳实践「太长」500 → 200 行；❌ 表后新增 `/doctor` `[!tip]`。
9. FAQ：比较表加载时机补 25KB；调试步骤改用 `/context`；新增「CLAUDE.md 太长或重复怎么办」问答。
10. 文末追加「更新记录」。
11. 产出 `updated_note.md` 供用户审阅后写回原文件。

## 校验项

- [ ] YAML frontmatter 特殊值加引号：本次 title/tags/created/updated 均无 `:`、`[]` 内逗号等特殊字符，无需引号
- [ ] 不重写未过时段落，仅局部 patch
- [ ] 列表内不嵌套表格（新增表格均置于段落顶层）
- [ ] 未修改原 vault 文件，全部产物写入 `updates/cc09/`
- [ ] 三层记忆体系（CLAUDE.md / Auto Memory / 参考文档）相关章节已核对，过时描述已修正
- [ ] Auto Memory 开关与记忆文件命名规范以官方文档为准
- [ ] 原文件乱码修复已列入更新记录，供用户确认
