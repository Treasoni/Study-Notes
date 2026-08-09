# 更新报告 — cc02（Claude Code 常用功能）

> 更新日期：2026-08-10 ｜ 依据 source_bank 适用条目 SB-04 / SB-08 / SB-09 / SB-10 / SB-11 / SB-12

## 变更摘要

| 类别 | 数量 | 说明 |
|------|------|------|
| 保留 | 12 处区块 | 未过时，原样保留 |
| 更新 | 8 处 | frontmatter、权限模式、`/doctor`、`/review`、`/code-review`、`/checkup` 去重、CLI 参数 |
| 删除 | 1 处 | 高级功能表中重复的 `/checkup` 行 |
| 新增 | 5 处 | `/fork`、`/subtask`、Slash/Skill 叠加 tip、emoji 补全、`## 更新记录` |

整体改动集中在「CLI 启动模式」与「Slash 命令速查」两个区块，正文其它部分仅 frontmatter 与文末更新记录变化。未整篇重写。

## 关键改动

1. **权限模式命名（SB-04）**：CLI 启动参数新增 `claude --permission-mode manual`，并新增 `[!tip] 权限模式（大白话）`，说明「Default → Manual」改名、`"defaultMode": "manual"` 配置及常用模式。
2. **命令更新（SB-10 / SB-08 / SB-09）**：
   - `/checkup` → `/doctor`（全量环境体检，`/checkup` 为别名），并删除高级功能表中重复行。
   - 新增 `/fork`（复制到新后台会话）、`/subtask`（会话内子代理）。
   - `/review` 标注为 `/code-review` 别名、不再自动运行；`/code-review` 标注为后台子代理运行、需手动触发。
3. **交互细节（SB-11 / SB-12 / SB-10）**：新增「新交互细节」tip——Slash/Skill 叠加（最多 5 个前置）、emoji 短码补全（`:thumbsup:`）、`/status` 显示会话类型。

## 引用来源

- SB-04（v2.1.200）：权限模式 Default→Manual，`--permission-mode manual` / `"defaultMode": "manual"`。
- SB-08（v2.1.212）：`/fork`、`/subtask`。
- SB-09（v2.1.215/218/223）：`/review` = `/code-review` 别名，不再自动运行；`/code-review` 后台子代理运行。
- SB-10（v2.1.205/206/210）：`/doctor`（=`/checkup`）全量环境体检；`/status` 显示会话类型。
- SB-11（v2.1.199）：Slash/Skill 叠加最多 5 个前置；emoji 自动补全。
- SB-12（v2.1.200–225）：`emojiCompletionEnabled` 等 settings 键；`"defaultMode"` 值改为 `manual`。

> 注：本次仅使用 source_bank 中标注适用的 6 条（SB-04/08/09/10/11/12），未做额外联网搜索。官方 docs 如与本文冲突，以 code.claude.com 现行文档为准。

## 未处理风险

1. **快捷键速查未核对**：source_bank 无快捷键变更来源；若官方近期调整快捷键（如 `Ctrl+D` 退出行为），需另核对官方 docs。列为需人工复核项。
2. **`/review-pr` 未验证**：为示例/自定义命令，非内置命令，无来源判定其过时，保留原样。
3. **安装快速参考基于 claude-howto 仓库结构**：该仓库目录不在本次更新范围，未核对，保留原样。
4. **MOC 同步**：`moc_path = none`，交由 P5 统一处理，本次不生成/更新 MOC。
5. **上下文容量描述**：「200K~1M tokens」沿用原文表述，与 SB-20（1M 上下文）方向一致，但 cc02 不在 SB-20 适用列表，未主动改写。

## 是否需要 needs-review

**是**。理由：涉及两处易混淆的行为变更——权限模式命名（Default→Manual）与命令别名关系（`/review`→`/code-review` 别名、不再自动运行），以及 `/doctor` 与 `/checkup` 主/别名互换。建议人工复核确认，尤其是快捷键速查是否有 2026-08 未捕获的变更。
