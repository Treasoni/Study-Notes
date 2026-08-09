# 更新计划 — cc02（Claude Code 常用功能）

> 依据 `stale_map.md` 生成。执行顺序：先 meta（frontmatter）后正文，先删后增，逐项局部 patch。

## 过时点清单

1. frontmatter：`updated` 日期过时；`tags` 未加引号。
2. CLI 启动参数缺权限模式示例（Default→Manual 命名变更）。
3. `/checkup` 主/别名颠倒（主名应为 `/doctor`），且在系统监控与高级功能两处重复。
4. `/review` 未注明「`/code-review` 别名 + 不再自动运行」。
5. `/code-review` 未注明「后台子代理运行、需手动触发」。
6. Slash 速查缺 `/fork`、`/subtask` 两个新命令。
7. 缺 Slash/Skill 叠加、emoji 短码补全、`/status` 会话类型等交互细节。

## 执行步骤

| 步骤 | 操作 | 影响区块 |
|------|------|----------|
| 1 | 改 frontmatter：`updated: 2026-08-10`；`tags` 元素加双引号；`status: updated` | frontmatter |
| 2 | CLI 启动参数块加 `claude --permission-mode manual`；其后新增「权限模式（大白话）」tip | CLI 启动模式 |
| 3 | 系统与监控表：`/checkup` → `/doctor`（别名标注） | Slash 命令速查 |
| 4 | 高级功能表：删重复 `/checkup` 行；改 `/code-review` 描述；新增 `/fork`、`/subtask` | Slash 命令速查 |
| 5 | 代码与 Git 表：改 `/review` 描述 | Slash 命令速查 |
| 6 | Slash 命令速查段首新增「新交互细节」tip | Slash 命令速查 |
| 7 | 文末追加 `## 更新记录` | 文末 |
| 8 | 校验：无列表内嵌套表格；YAML 特殊字符已加引号；未整篇重写 | 全篇 |

## 校验清单

- [ ] YAML frontmatter：`tags` 值含 `[]`，元素已用双引号包裹。
- [ ] 无「列表内嵌套表格」结构（tip 内仅使用无序列表，未放表格）。
- [ ] 只改过时项：快捷键、文件操作、Git、代码搜索等无来源变更处未动。
- [ ] 保留原结构（标题层级、表格列、写作风格、emoji 标题）。
- [ ] 原 vault 文件未修改，产物全部写入 `updates/cc02/`。

## 未改动项（明确排除）

- 快捷键速查、Checkpoint/Rewind、Extended Thinking、CLAUDE.md、文件操作、代码搜索、Git 集成、功能对比表、常见问题、概念辨析、最佳实践：无过时来源，保留原样。
- `/review-pr`、安装快速参考、参考资料：不在本次更新范围。
