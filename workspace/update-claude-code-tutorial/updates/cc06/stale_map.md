# 过时映射（Stale Map）— cc06 settings.json 配置详解

> 更新目标：同步到 2026-08 现状。来源库适用条目：SB-04、SB-12、SB-13、SB-14、SB-15。

## 保留（Keep）

| 位置 | 理由 |
|------|------|
| 配置文件层级表格与合并规则（全局/项目/本地/托管） | 现行，未过时 |
| §1 模型配置（`model` / `fallbackModel`） | 未过时；SB-01/SB-02 适用笔记不含 cc06 |
| §2 推理努力级别（`effortLevel` 取值表） | 未过时；xhigh/max 的 Opus 版本说明非默认值描述，保守保留 |
| §4 自动压缩（`autoCompactEnabled` + `/autocompact`） | 已在 2026-08-07 同步过（见既有更新记录） |
| §5 环境变量（`env`） | 未过时 |
| §6 Hooks（事件与类型） | 未过时；SB-16 新增事件针对 cc08，不在本笔记适用范围 |
| §7 MCP 服务器配置（`claude mcp add`） | 未过时 |
| §8 其他配置（`$schema` / `plugins` / `verbose` + 已移除字段说明） | 未过时 |
| 场景配置示例 / 常见问题 / 最佳实践 / 相关文档 / 参考资料 | 未过时 |
| 原结构与写作风格、Callout 用法 | 保留 |

## 更新（Update）

| 位置 | 现状 | 改为 |
|------|------|------|
| frontmatter `updated` | 2026-08-07 | 2026-08-10 |
| frontmatter `status` | draft | updated |
| §3 权限控制 | 未提及权限模式字段 | 补充 `defaultMode: "manual"`（原「Default」改名「Manual」） |
| 文章完整性 | 缺结语 | 新增「小结」 |
| 更新记录 | 仅 2026-08-07 一条 | 追加 2026-08-10 条目 |

## 删除（Delete）

无。未发现正文中仍在使用、但已被官方废弃的字段（`maxTokens` / `systemPrompt` / `autoCompactThreshold` 已在原文 §4/§8 标注为废弃）。

## 新增（Add）

| 小节 | 新增配置键 | 来源 |
|------|-----------|------|
| §9 沙盒与安全配置 | `sandbox.filesystem.disabled`、`sandbox.network.strictAllowlist`；附凭据掩码说明（mask/extract/onExtractNoMatch/jwt/awsPairs/sigv4） | SB-12, SB-13 |
| §10 Auto Mode 配置 | `disableAutoMode`、`autoMode.classifyAllShell`；附 Auto mode 行为变化 | SB-12, SB-03, SB-14 |
| §11 无障碍模式 | `axScreenReader`；附 CLI `--ax-screen-reader` 与 `CLAUDE_AX_SCREEN_READER=1` | SB-15, SB-12 |
| §12 输入与工作流体验 | `emojiCompletionEnabled`、`vimInsertModeRemaps`、`workflowSizeGuideline` | SB-12, SB-11 |
| §13 跨会话消息 | `crossSessionInbound`、`dialogExpiry` | SB-12 |
| 小结（结语） | — | 完整性补全 |
