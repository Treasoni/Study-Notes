# cc13 — 更新计划（update_goal 对齐）

## 过时点清单

| # | 位置 | 过时内容 | 更新动作 | 来源 |
|---|------|----------|----------|------|
| 1 | frontmatter | `updated: 2026-07-12` | 改为 `2026-08-10`；status 保持 `updated` | — |
| 2 | 命令类型表 | 自定义 Skills 示例含 `/review` | 改为 `/commit`, `/optimize` | SB-09 |
| 3 | 通俗理解示例 | `/review src/auth.ts` 标注为自定义 Skill | 改为 `/code-review`（内置，后台子代理运行） | SB-09 |
| 4 | 会话管理命令表 | `/branch` 说明写 `/fork` 仅为其别名 | 新增 `/fork` 独立行；`/branch` 保留为分支会话 | SB-08 |
| 5 | 会话管理命令表 | 缺 `/fork` 行 | 新增：复制当前对话到新后台会话 | SB-08 |
| 6 | 会话管理命令表 | `/resume` 说明未提后台恢复 | 补充 agent 视图历史会话选择器、以后台会话恢复 | SB-08 |
| 7 | 会话管理命令表 | `/rewind` 未提 `/clear` 恢复 | 补充可恢复到 `/clear` 之前的对话 | SB-08 |
| 8 | 信息与调试命令表 | `/checkup` 为主、`/doctor` 为别名（方向反了） | 改为 `/doctor` 全量体检，`/checkup` 为别名 | SB-10 |
| 9 | 信息与调试命令表 | `/status` 未含会话类型 | 补充 interactive / attached / unattended | SB-10 |
| 10 | 内置命令表 | 缺 `/subtask`、`/code-review`、`/review` | 新增命令行 + 新「代码审查命令」分类 | SB-08 / SB-09 |
| 11 | 全部内置命令表 | 各分类表非字母序 | 按命令字母序整理（新增命令插入正确位置） | update_goal |
| 12 | 内置命令参考末尾 | 缺叠加调用与 emoji 补全说明 | 新增 tip：Slash/Skill 叠加（最多 5 个前置）、emoji 短码自动补全（`:thumbsup:`，`emojiCompletionEnabled` 控制） | SB-11 / SB-12 |
| 13 | 版本更新历史 | `/review` 行「废弃，替换为 code-review 插件」已过时 | 改为 `/review` 是 `/code-review` 别名、不再自动运行 | SB-09 |
| 14 | 版本更新历史 | 缺 2026-07/08 条目 | 新增 v2.1.212、v2.1.205-210、v2.1.199 条目 | SB-08/09/10/11 |
| 15 | Frontmatter 字段参考 | `disable-model-invocation` 说明可补充 | 补充「禁止模型自动调用时 Claude 会请你手动运行」 | SB-18 语境 |
| 16 | 核心概念 | 缺大白话 | 新增 `[!tip] 大白话`（Slash Commands、`/fork`、`/subtask`） | — |
| 17 | 结尾 | 无更新记录 | 追加 `## 更新记录` | — |

## 核对结论
- 全部内置命令表按字母序整理；新增 `/fork`、`/subtask`、`/code-review`、`/review`、`/doctor`（主命令）。
- `/checkup` 与 `/doctor` 关系：以 SB-10 为准，`/doctor` 为主、`/checkup` 为别名（本笔记原写法方向相反）。
- `/review`：不再是自定义 Skill，而是内置 `/code-review` 的别名；不再自动运行，需手动调用。
- Bundled Skills 数量（5 个）与内置命令数量（55+）source bank 无新数字，未改动（见报告风险）。

## 不做（刻意排除）
- Bundled Skills 列表与数量：source bank 无对应更新，未越界修改。
- 内置命令数量「55+」：无权威新数字，保留下限表述。
- Plugin / MCP / 命令架构 / 生命周期 / 故障排除：未过时，不触碰。
