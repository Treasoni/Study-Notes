# cc04 — 更新计划（update_goal 对齐）

## 过时点清单

| # | 位置 | 过时内容 | 更新动作 | 来源 |
|---|------|----------|----------|------|
| 1 | frontmatter | `updated: 2026-07-12` | 改为 `2026-08-10`；status 保持 `updated` | — |
| 2 | 会话管理命令 | `/status` 描述不含会话类型 | 补充 `interactive / attached / unattended` | SB-21 |
| 3 | CLI 启动选项 | `claude --model claude-opus-4-8` | 改为 `claude-opus-5` | SB-02 |
| 4 | 配置优先级（Settings） | mermaid 图缺 CLI args 层级 | 补充完整优先级说明 callout | SB-21 语境 / 官方设置文档 |
| 5 | 内置命令列表 | 缺 `/fork` `/rewind` `/subtask` `/tasks` | 新增行并保持字母序；更新 `/status` 行 | SB-06 / SB-08 |
| 6 | 会话管理命令 | 缺 `/fork` `/rewind` 命令块 | 新增命令块 | SB-08 |
| 7 | 会话操作流程 | 缺会话恢复/复制操作 | 新增「会话恢复与复制」小节 | SB-08 / SB-22 |
| 8 | 内置斜杠命令与 Skills | 未提及 Subagents 默认后台运行 | 新增「Subagents 与后台会话」小节 | SB-06 |
| 9 | 内置斜杠命令与 Skills | 未提及 AskUserQuestion 行为 | 新增「交互对话框」说明（默认不自动继续，`/config` 可设 idle timeout） | SB-21 |
| 10 | 注意事项·常见错误 | 缺 transcript/登录过期警告 | 新增警告项 | SB-21 |
| 11 | 常见问题 | 缺子代理运行方式 Q&A | 新增 Q&A | SB-06 |
| 12 | 结尾 | 无更新记录 | 追加 `## 更新记录` | — |

## 核对结论（点6：上下文管理 / 会话恢复 / 配置优先级）
- 上下文管理：Token 管理策略与 `/compact` 描述未过时；`"model": "claude-sonnet-5"` 仍为默认模型，无需改。
- 会话恢复：补 `/fork`、`/rewind`、agent 视图 `/resume`；`claude --continue` / `--resume` / `agents` 保留。
- 配置优先级：补 CLI args 层级；`.claude.local/settings.json` 路径未改（见风险）。

## 不做（刻意排除）
- `.claude.local/settings.json` 路径：source bank 无对应条目，未改，仅标注风险。
- `/doctor` 与 `/checkup` 关系：SB-10 适用笔记不含 cc04，不越界修改。
- `claude agents` 命令形式：无来源支持是否应写 `claude --agents`，保持原样。
