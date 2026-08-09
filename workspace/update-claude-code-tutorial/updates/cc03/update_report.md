# cc03 更新报告 — Claude Code CLI 完整参考

## 更新摘要

- **note_id**: cc03
- **过时点数量**: 6（版本行、permission-mode 改名、max-budget-usd 语义、claude agents/status、环境变量缺新项、frontmatter）
- **变更类型**: 局部 patch，保留原文结构与写作风格；未重写未过时段落。
- **变更内容**:
  1. 版本行同步到 v2.1.226（2026-08-10）。
  2. `--permission-mode` 说明 `default` 已改名 `manual`，示例改为 `claude --permission-mode manual`，并加 `[!tip] 大白话` 通俗解释。
  3. `--max-budget-usd` 补充「达到上限停止后台子代理」语义。
  4. 新增 `--forward-subagent-text`（stream-json 透传子代理文本）。
  5. 新增 `--ax-screen-reader`（屏幕阅读器模式）。
  6. `claude agents` 行补充 `/status` 显示会话类型（interactive / attached / unattended），代理配置节加 `[!note]`。
  7. 环境变量表新增 5 项：`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`（默认 20）、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`（=1 禁用嵌套）、`CLAUDE_CODE_DISABLE_1M_CONTEXT`、`CLAUDE_AX_SCREEN_READER`、`CLAUDE_CODE_DISABLE_MOUSE_CLICKS`。
  8. 追加 `## 更新记录`。
  9. frontmatter `updated` 设为 2026-08-10，`status` 保持 `updated`。

## 引用来源（共享来源库）

| 条目 | 来源 | 用途 |
|------|------|------|
| SB-04 | code.claude.com/docs/en/changelog（v2.1.200） | 权限模式 default→manual |
| SB-05 | code.claude.com/docs/en/changelog（v2.1.208–v2.1.223） | 新增 CLI 标志 + 环境变量 |
| SB-06 | code.claude.com/docs/en/changelog（v2.1.198/217/219） | 子代理并发默认 20、嵌套规则 |
| SB-10 | code.claude.com/docs/en/whats-new/2026-w28 | `/status` 会话类型 |
| SB-13 | code.claude.com/docs/en/changelog | `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` |
| SB-15 | code.claude.com/docs/en/changelog（v2.1.208） | 屏幕阅读器 `--ax-screen-reader` / `CLAUDE_AX_SCREEN_READER` |

> 全部变更均来自共享来源库适用条目（SB-04/SB-05/SB-06/SB-07，其中 SB-07 无本笔记相关点）。未做额外联网检索。

## 核对结果（无变更项）

- **管道模式**：`-p` / `--input-format` / `--output-format` 描述与 2026-08 现状一致，无过时。
- **启动参数**：`claude` / `-n` / `-c` / `-r` 等仍有效。
- **退出码**：笔记仅有 `claude auth status`（已登录 0 / 未登录 1），仍有效；笔记无独立退出码章节，无需改动。

## 未处理风险 / 建议

1. **模型表未更新**：「可用模型」表仍列 Opus 4.8 为「最新默认」；SB-02 显示 v2.1.219 起 Opus 5 成为默认 Opus 模型。但共享来源库将该条目仅分配给 cc05/cc12，且本轮 update_goal 未包含模型变化，故未改动。建议后续单独核对。
2. **`--enable-auto-mode` 语义**：SB-03 显示第三方平台（Bedrock/Vertex/AWS）Auto mode 免 opt-in；笔记中 `--enable-auto-mode` 仍按 opt-in 描述。该条目同样未分配到 cc03，未改动。
3. **版本号口径**：以来源库覆盖上限 v2.1.226 为准；若官方 docs 与来源库冲突，以 code.claude.com 现行文档为准并在后续更新中标注。

## needs-review

**建议：需要（needs-review）**。理由：模型表与 Auto mode 描述存在与 2026-08 现状可能不一致的项，但超出本轮 update_goal 范围而未改动，建议人工核对是否纳入后续更新；其余变更均来自共享来源库，可直接采用。
