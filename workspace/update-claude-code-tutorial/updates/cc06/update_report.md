# 更新报告 — cc06 settings.json 配置详解

## 基本信息

| 项 | 值 |
|----|----|
| note_id | cc06 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\02-基础功能\settings.json 配置详解.md` |
| 输出目录 | `C:\note\Study-Notes\workspace\update-claude-code-tutorial\updates\cc06\` |
| 原状态 | draft（updated 2026-08-07） |
| 新状态 | updated（updated 2026-08-10） |
| MOC | none（P5 统一处理） |

## 更新摘要

- **权限模式**：§3 权限控制补充 `defaultMode: "manual"`（原「Default」改名「Manual」，SB-04），并新增权限模式取值表 + `[!tip] 大白话`。
- **新增 5 个小节（§9–§13）覆盖 9 类新配置键**（SB-12）：
  - `sandbox.filesystem.disabled`、`sandbox.network.strictAllowlist`（§9，附凭据掩码说明 SB-13）
  - `disableAutoMode`、`autoMode.classifyAllShell`（§10，附 Auto mode 行为变化 SB-14）
  - `axScreenReader`（§11，附 CLI `--ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` 等效方式，SB-15）
  - `emojiCompletionEnabled`、`vimInsertModeRemaps`、`workflowSizeGuideline`（§12，SB-11）
  - `crossSessionInbound`、`dialogExpiry`（§13）
- **完整性补全**：新增「小结」结语；FAQ 增补「权限模式怎么选」一问；最佳实践 Do's 增加权限模式建议。
- **frontmatter**：`status: draft → updated`、`updated: 2026-08-07 → 2026-08-10`。
- **更新记录**：追加 2026-08-10 条目。
- 未重写未过时段落（模型、推理级别、自动压缩、环境变量、Hooks、MCP、其他配置、常见问题、场景示例等均保留原文）。

## 引用来源

| 来源 | 用途 |
|------|------|
| SB-04（权限模式重命名） | `defaultMode: "manual"` 改名说明 |
| SB-11（Slash/Skill 叠加、emoji 自动补全） | `emojiCompletionEnabled` |
| SB-12（settings.json 新增配置键） | §9–§13 新增键清单主依据 |
| SB-13（沙盒与安全配置） | §9 凭据掩码说明 |
| SB-14（Auto mode 行为变化） | §10 Auto mode 行为说明 |
| SB-15（无障碍 Screen reader） | §11 `axScreenReader` 及等效方式 |

> 以 code.claude.com 现行文档为准（来源库约定：若与本文冲突，以官方文档为准）。

## 未处理风险

1. **精确 JSON 结构待校验**：`vimInsertModeRemaps`、`crossSessionInbound`、`dialogExpiry` 的精确 schema（键名、取值格式，如 `"jj": "Esc"`、`"24h"`）未在来源库给出，文中以说明性描述 + 示意值呈现，正式写回前建议对照官方 settings schema 确认。
2. **`acceptEdits` / `plan` / `bypassPermissions` 取值**：权限模式表其余取值属既有常识，来源库仅确认 `manual` 改名；写回时可再核对一次官方文档。
3. **未大范围联网**：本次仅用共享来源库核对，未逐一抓取官方 settings 页面；`workflowSizeGuideline` 的触发行为描述较简。
4. **effortLevel 中 xhigh/max 的 Opus 版本标注**（Opus 4.7/4.8+、Opus 4.6+）：SB-01/02 不适用 cc06，未改动；若需同步 Opus 5 可另行处理。

## 结论

- 发现过时点：2 处（frontmatter 状态/日期、权限模式改名缺失）+ 9 类新增配置键 + 缺结语。
- **是否需要 needs-review：是**。新增配置键的精确结构为草拟描述，建议用户审阅 `updated_note.md` 并对照官方 schema 后，再写回原 vault 文件。
