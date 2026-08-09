# 更新计划 — cc18 Claude Code Dynamic Workflows 使用指南

## 过时点清单

| 序号 | 位置 | 现状 | 过时原因 | 处理方式 |
|------|------|------|---------|---------|
| U1 | frontmatter `updated` | 2026-07-12 | 需同步 2026-08 现状 | `updated: 2026-08-10`；`status: updated` 保持 |
| U2 | §核心概念 · `/deep-research` 触发描述 | 未提自动启动变化 | 官方：v2.1.218 起仅在主动调用时运行 | 触发方式 1 补「Claude 不再自行启动」 |
| U3 | §运行时特征 | 无可观测性信息 | 任务项 2：workflow agent 在 OTel 带 `workflow.run_id`/`workflow.name` | 新增 bullet |
| U4 | §关键限制表 | 缺「不能加载模块」 | 官方：含 `import()` 的脚本 run 前失败 | 新增一行 |
| U5 | §关键限制区 | 缺大型 run 预警 | 官方：v2.1.203+ >25 agent 或 >1.5M token 显示 `Large workflow` | 新增 `[!note]` |
| U6 | §关键要点 4 嵌套规则 | 写「v2.1.172 之前不能派生嵌套」 | SB-06：v2.1.217 默认禁用 → v2.1.219 恢复深度 3 | 改写为 v2.1.217/219 + `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` |
| U7 | §关键要点 4 执行模式 | 未提默认后台 | SB-06：子代理默认后台运行（v2.1.198+） | 新增 bullet |
| U8 | §关键要点 6 嵌套深度 | 写「5 层」 | SB-06：默认深度改为 3 | 5 层 → 3 层 |
| U9 | §关键要点 6 worker 通信 | 未提跨会话消息 | 任务项 3：`SendMessage` 跨会话/跨机器，`ListAgents` 按名称发现 | 新增 bullet |
| U10 | §保存位置 | 未提符号链接保护 | 官方：v2.1.216 起保存前检查 symlink 拒写 | 新增 bullet |
| U11 | 速查清单·监控控制表 | 缺 `f` 键 | 官方 watch run 键位含 `f` | 补一行 |
| U12 | 速查清单·关键限制表 | 嵌套 5 层；缺模块加载/预警 | 同上 U4/U5/U6 | 嵌套 3 层；补两行 |
| U13 | 速查清单·触发方式 `/deep-research` 行 | 只写「需要 WebSearch」 | 同 U2 | 补 v2.1.218 说明 |
| U14 | 版本时间线表 | 止于 2.1.178 | 2026-07/08 多版本行为变更 | 追加 6 行 |
| U15 | 参考资料表 | R1–R9 | 新事实需可追溯 | 追加 R10 |
| U16 | 核心概念·一句话定义 | 已有类比，无 Callout | 任务项 5：核心概念加 `[!tip] 大白话` | 新增 `[!tip] 大白话` |
| U17 | 核心概念 | 无规模设置子节 | 任务项 1：`workflowSizeGuideline` + `/config` Dynamic workflow size | 新增「工作流规模」子节 + `[!tip] 大白话` |
| U18 | 速查清单 | 无规模设置速查 | 任务项 1 | 新增「规模设置速查」子节 |
| U19 | 文末 | 无更新记录 | 本次变更需留痕 | 追加「更新记录」 |

## 关键事实核对（2026-08-10 官方 workflows 文档）

| 事实 | 官方当前说法 | 处理 |
|------|-------------|------|
| 并发上限 | 「Up to 16 concurrent agents, fewer on machines with limited CPU cores」 | **保留 16**（workflow 专属；SB-06 的 20 是普通 subagent 并发，不适用于本笔记 workflow 场景，不照搬） |
| 每 run agent 上限 | 「1,000 agents total per run」 | **保留 1000** |
| 嵌套规则 | v2.1.217 默认禁用 → v2.1.219 恢复深度 3 | 更新为 3 层 |
| size guideline | `unrestricted` / `small`<5 / `medium`<15 / `large`<50；默认 `medium`（v2.1.219+，之前默认 `unrestricted`） | 新增规模子节 |
| Large workflow 预警 | v2.1.203+：>25 agent 或 >1.5M token 时任务面板显示警告（仅提示） | 新增 note |
| 模块加载 | 含 `import()` 的脚本 run 前失败 | 新增限制行 |
| `/deep-research` | v2.1.218 起仅在主动调用时运行 | 补说明 |

## 执行步骤

1. 更新 frontmatter：`updated: 2026-08-10`；追加 `R10` 来源。
2. §核心概念：一句话定义后加 `[!tip] 大白话`；触发方式 1 补 `/deep-research` v2.1.218 行为；运行时特征补 OTel bullet。
3. §核心概念新增「工作流规模（Dynamic workflow size）」子节（含四档表 + 设置方式 + `[!tip] 大白话`）。
4. §关键限制表：并发 16 补「CPU 核少更少」；新增「不能加载模块」行；表后加 `[!note]` Large workflow 预警。
5. §保存位置：补 v2.1.216 symlink 保护。
6. §关键要点 4：补「默认后台运行」bullet；改写嵌套规则为 v2.1.217/219 + env 禁用。
7. §关键要点 6：5 层 → 3 层；补 `SendMessage`/`ListAgents` 跨会话 bullet。
8. 速查清单：监控控制补 `f` 键；触发方式 `/deep-research` 行补 v2.1.218；关键限制表嵌套改 3 层 + 补两行；新增「规模设置速查」子节。
9. 版本时间线：追加 v2.1.198 / v2.1.202 / v2.1.203 / v2.1.217 / v2.1.219 / v2.1.224。
10. 参考资料表：追加 R10。
11. 文末追加「更新记录」2026-08-10 条目。
12. 产出 `updated_note.md` 供用户审阅后写回原文件（原 vault 文件不改）。

## 校验项

- [ ] YAML frontmatter 特殊值加引号（新增 R10 来源行已加引号）
- [ ] 不重写未过时段落，局部 patch
- [ ] 列表内不嵌套表格（规模设置速查 = 独立表格，非列表内嵌）
- [ ] 未修改原 vault 文件，全部产物写入 updates/cc18/
