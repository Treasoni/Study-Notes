# 更新计划 — cc06 settings.json 配置详解

## 过时点清单

| 序号 | 位置 | 现状 | 过时原因 | 处理方式 |
|------|------|------|---------|---------|
| U1 | frontmatter `status` / `updated` | `draft` / 2026-08-07 | 需同步 2026-08 现状 | `status: updated`、`updated: 2026-08-10` |
| U2 | §3 权限控制 | 未含 `defaultMode` | SB-04：权限模式「Default」全面改名「Manual」 | 新增 `defaultMode: "manual"` 说明（含 CLI `--permission-mode manual`） |
| U3 | §8 之后缺少 2026-07/08 新增键 | 无 | SB-12：settings.json 新增 9 类配置键 | 新增 §9–§13 五个小节 |
| U4 | 文章完整性 | 无结语 | draft 完整性 | 新增「小结」 |
| U5 | 更新记录 | 仅 2026-08-07 | 本次变更需留痕 | 追加 2026-08-10 条目 |

## 新增配置键与来源核对

| 配置键 | 来源 | 说明 |
|--------|------|------|
| `defaultMode: "manual"` | SB-04 | 「Default」改名「Manual」，settings 用 `"defaultMode": "manual"` |
| `emojiCompletionEnabled` | SB-12, SB-11 | emoji 短码自动补全（如 `:thumbsup:`） |
| `vimInsertModeRemaps` | SB-12 | Vim 插入模式按键映射，如 `jj`→Esc |
| `axScreenReader` | SB-15, SB-12 | 屏幕阅读器模式，配合 `claude --ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` |
| `sandbox.filesystem.disabled` | SB-12 | 跳过文件系统隔离，但保留网络出口控制 |
| `sandbox.network.strictAllowlist` | SB-12 | 沙盒网络严格白名单 |
| `disableAutoMode` | SB-12, SB-03 | 关闭 Auto mode（第三方平台已免 opt-in） |
| `workflowSizeGuideline` | SB-12 | 动态工作流规模建议 small/medium/large |
| `crossSessionInbound` / `dialogExpiry` | SB-12 | 跨会话消息 |
| `autoMode.classifyAllShell` | SB-12 | 所有 Bash/PowerShell 命令走 auto 分类器 |
| 凭据掩码扩展（mask/extract/onExtractNoMatch/decode:jwt/maskClaims/awsPairs/sigv4） | SB-13 | 沙盒凭据掩码新增能力 |

## 执行步骤

1. 更新 frontmatter：`updated: 2026-08-10`、`status: updated`。
2. §3 权限控制：JSON 示例加 `"defaultMode": "manual"`，补充权限模式说明表 + `[!tip] 大白话`。
3. 在 §8 之后新增 §9–§13 五个小节（沙盒 / Auto mode / 无障碍 / 输入与工作流体验 / 跨会话消息）。
4. 在最佳实践后新增「小结」结语，补齐文章完整性。
5. 追加「更新记录」2026-08-10 条目。
6. 产出 `updated_note.md` 供用户审阅后写回原文件。

## 校验项

- [ ] YAML frontmatter 特殊值（`[]`/`:`）加引号；本次 tags 为纯词，无需引号
- [ ] 不重写未过时段落，局部 patch
- [ ] 列表内不嵌套表格
- [ ] 未修改原 vault 文件，全部产物写入 updates/cc06/
