# cc01 更新报告（update_report）

> 笔记：Claude Code 使用指南（入门篇）· note_id：cc01
> 更新日期：2026-08-10

## 更新摘要

对入门篇《Claude Code 使用指南》做 2026-08 现状同步。共定位 **11 处过时/待更新点 + 4 处新增**，全部按共享来源库局部 patch，未删除任何段落。主要变更：

1. **模型**：默认模型更新为 Claude Sonnet 5（原生 1M 上下文，促销价 $2/$10 每 Mtok 至 2026-08-31）；默认 Opus 更新为 Opus 5。新增「2026-08 模型现状」`[!tip]` callout；`/model claude-opus-4.8` → `claude-opus-5`。
2. **权限模式**：Default 改名 Manual；新增启动命令 `claude --permission-mode manual`；settings 可选值 `"default"` → `"manual"`（方式四 primaryApiKey 段内同步）。
3. **命令**：`/checkup` 行改为 `/doctor`（`/checkup` 为别名，全量环境体检）；`/fork` 描述改为「复制当前对话到新后台会话」；新增 `/subtask` 行（会话内子代理）；`/code-review` 注明 `/review` 是别名、不再自动运行、需手动调用；2026 新增命令 tip 同步更新。
4. **版本**：latest v2.1.224 → v2.1.226（2026-08-10）；allow-scripts FAQ 两处示例版本同步；stable 改为模糊描述「通常滞后约一周」。
5. **frontmatter**：`updated` → 2026-08-10，`status` 保持 `updated`；追加 2026-08-10 更新记录行。

## 引用来源

| 条目 | 来源 | 用途 |
|------|------|------|
| SB-01 | code.claude.com/docs/en/changelog | Sonnet 5 默认模型、原生 1M 上下文、促销价 $2/$10 至 2026-08-31 |
| SB-02 | code.claude.com/docs/en/changelog | Claude Opus 5 成为默认 Opus 模型 |
| SB-04 | code.claude.com/docs/en/changelog | 权限模式 Default → Manual（CLI `--permission-mode manual` / settings `"defaultMode": "manual"`） |
| SB-08 | code.claude.com/docs/en/changelog | `/fork` 复制到新后台会话、`/subtask` 取代 in-session 子代理 |
| SB-09 | dev.classmethod.jp/en/articles/20260806-cc-updates-v2-1-223/ · changelog | `/review` 是 `/code-review` 别名、不再自动运行 |
| SB-10 | code.claude.com/docs/en/whats-new/2026-w28 | `/doctor`（= `/checkup`）全量环境体检 |

## 未处理风险 / 需人工复核项

1. **stable 具体版本号未核实**：source_bank 仅给覆盖范围 v2.1.193~v2.1.226，未给 stable 精确号；已将原文「stable v2.1.220」改为「stable 通常滞后约一周」。如需精确号，需查官方 releases。
2. **`/review-pr` 示例未动**：Skills 使用示例中的 `/review-pr 123` 不在 source_bank 覆盖范围，保留原样；如确认废弃可后续清理。
3. **`/status` 会话类型显示未补充**：SB-10 提到 `/status` 现显示会话类型（interactive / attached / unattended）；本笔记已在免登录章用 `/status` 确认认证方式，未额外补充会话类型显示，属可选增强。
4. **历史更新记录行保持原样**：2026-08-07 行仍写 v2.1.224（历史事实），与正文当前版本不一致属预期，避免篡改历史。
5. **CC-Switch 版本未更新**：v3.16.1 为笔记既有记录，source_bank 未覆盖该第三方工具，未改动。

## 结论

过时点已全部按 source_bank 处理，未引入未覆盖的新事实，无阻断风险。

**是否需要 needs-review：是** —— 建议用户审阅 `updated_note.md` 后写回原 vault 文件。重点关注：模型促销价与版本号属时效信息（促销至 2026-08-31），且 stable 精确版本需人工核实。
