# cc13 — 更新报告

## 更新摘要
- 过时点：17 处（7 处更新 + 10 处新增/补充）。
- 全部为局部 patch，未重写未过时段落，保留原结构和写作风格。
- 命令变更：新增 `/fork`（复制对话到新后台会话）、`/subtask`（in-session 子代理）、`/code-review`（后台子代理运行，复用上次 effort 等级）、`/review`（`/code-review` 别名，不再自动运行）、`/doctor`（全量体检，`/checkup` 改为别名）；`/status` 显示会话类型；`/rewind` 可恢复到 `/clear` 之前。
- 全部内置命令分类表按命令字母序整理。
- 补充 Slash/Skill 叠加调用（最多 5 个前置 skill）与 emoji 短码自动补全（`:thumbsup:`，`emojiCompletionEnabled`）。
- 核心概念新增 `[!tip] 大白话`（Slash Commands、`/fork`、`/subtask`）。
- 列表内不嵌套表格；frontmatter 无含 `[]`/`:` 的 YAML 值，无需加引号。

## 引用来源
- SB-08（`/fork`、`/subtask`、`/resume` agent 视图后台恢复、`/rewind` 恢复到 `/clear` 之前）→ 会话管理命令更新与新增。
- SB-09（`/review` → `/code-review` 别名；不再自动运行；后台子代理 + 复用 effort）→ 代码审查命令、命令类型表示例、版本历史。
- SB-10（`/doctor` 全量体检、`/checkup` 为别名、`/status` 会话类型）→ 信息与调试命令表。
- SB-11（Slash/Skill 叠加最多 5 个、emoji 自动补全）→ 交互细节 tip。
- SB-12（`emojiCompletionEnabled` 等 settings 键）→ emoji 补全由该设置控制。
- 官方 changelog：https://code.claude.com/docs/en/changelog

## 未处理风险
1. **内置命令总数「55+」**：新增多个命令后实际数量更高，但 source bank 无权威新数字，保留「55+」下限表述；如需精确数字建议对照官方文档。
2. **Bundled Skills 数量（5 个）**：当前实际捆绑技能可能已多于 5 个（如 `/run`、`/keybindings-help` 等），但 source bank 未提供清单，未改动；建议后续单独核对。
3. **`/branch` 与 `/fork` 关系**：SB-08 只描述 `/fork` 复制对话到新后台会话，未说明 `/branch` 是否保留；本更新保留 `/branch` 并新增 `/fork` 独立行，未删除。
4. **`/verify` 命令**：SB-09 提到 Claude 不再自动运行 `/verify`，但命令表中原无此命令，仅版本历史提及，未新增行。
5. **`/code-review` 参数形式**：SB-09 未给出参数规范，示例仅写 `/code-review`（无参），未发明参数形式。

## 结论
- **是否需要 needs-review：是**。核心命令变更均有 SB-08/09/10/11/12 支撑，但内置命令总数、Bundled Skills 清单、`/branch` 去留等细节无法从 source bank 完全确认，建议人工复核后再写回 vault。
