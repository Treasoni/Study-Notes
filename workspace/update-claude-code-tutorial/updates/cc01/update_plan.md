# cc01 更新计划（update_plan）

> 笔记：Claude Code 使用指南（入门篇）· note_id：cc01
> 更新目标：同步到 2026-08 现状

## 过时点与处理计划

| # | 过时点 | 证据 | 处理动作 | 影响范围 |
|---|--------|------|---------|---------|
| 1 | 默认模型 / 版本描述过时（latest v2.1.224、`/model claude-opus-4.8` 示例、缺默认模型上下文） | SB-01、SB-02、changelog v2.1.226 | 版本号更新至 v2.1.226；`/model claude-opus-4.8` → `claude-opus-5`；补「2026-08 模型现状」callout（Sonnet 5 原生 1M、促销 $2/$10 至 08-31、Opus 5 默认） | 一·安装、五·速查 |
| 2 | 权限模式名 Default → Manual（settings 值 `"default"`、缺 CLI 入口） | SB-04 | CLI 新增 `claude --permission-mode manual` 启动行；settings 可选值 `"default"` → `"manual"` | 二·免登录、五·速查 |
| 3 | 新命令缺失 / 描述过时（`/doctor`、`/subtask`、`/fork` 行为、`/review` 别名与不再自动运行） | SB-08、SB-09、SB-10 | `/checkup` 行改为 `/doctor`（`/checkup` 别名）；`/fork` 描述改为「复制到新后台会话」；新增 `/subtask` 行；`/code-review` 注明 `/review` 别名、不再自动运行；更新 2026 新增命令 tip | 五·速查 |
| 4 | allow-scripts FAQ 示例版本号过时 | changelog v2.1.226 | `@anthropic-ai/claude-code@2.1.224` → `@2.1.226`（2 处示例；历史更新记录行保持 2.1.224） | 一·安装 FAQ |
| 5 | frontmatter `updated` / `status` | 任务要求 | `updated: 2026-08-10`；`status: updated` | frontmatter |

## 更新原则

- **局部 patch**：只改过时段落，不重写未过时内容；保持原结构和写作风格。
- **历史记录不回溯**：更新记录 2026-08-07 行仍写 v2.1.224，仅新增 2026-08-10 行。
- **不修改原 vault 文件**：全部产物写入 `updates/cc01/`，供用户审阅后写回。
- **不引入 source_bank 未覆盖的新事实**：stable 具体版本未核实，改用模糊描述。
- **Obsidian 规范**：新增 callout 使用 `[!tip]`；不在列表内嵌套表格；frontmatter 特殊值已加引号。
