---
title: "实战：写 hook 扩展点插件（分册）"
tags: [deepseek-harness, ai, agent, 插件, 教程, 开发]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
---

# 实战：写 hook 扩展点插件

> [!info] 分册信息
> - **系列位置**：插件开发教程第 11 章
> - **定位**：是 01 章 3.5「hook 扩展点」速览的教学落地；与 03 章配置实战区分——03 搬配置、本篇写代码
> - **版本锚点**：dsh master，2026-08
> - **素材基础**：9 源（5 官方 + 4 社区）

## 章节目录

| 章 | 笔记 | 一句话定位 |
|----|------|-----------|
| 1 | [[11-实战-写hook扩展点插件/01-导读与定位|第 1 章：导读与定位]] | 本章在系列中的坐标：插件开发教程第 11 章，是 01 章 3.5「hook 扩展点」速览的教学落地；01 只给目录表格，本篇把 5 个扩展点逐个写给你看 |
| 2 | [[11-实战-写hook扩展点插件/02-语义模型|第 2 章：语义模型]] | 固定流水线顺序（引用 S3 权威顺序）：`tools/pre-execute` → 单调 guard →（ask 经 `ctx.approval`）→ `tools/execute` → 工具体 → `tools/post-execute` → 归一化 → `finalizeContent` → `tools/result` → durable `tool/result` 事件 |
| 3 | [[11-实战-写hook扩展点插件/03-扩展点拆解|第 3 章：扩展点拆解]] | `tools/pre-execute`：权限门决策点，`PreToolDecision` allow/deny/ask；**不能改写 `exec.arguments`**（记录/渲染参数会与实际运行脱同步，与 CC `updatedInput` 的关键差异） |
| 4 | [[11-实战-写hook扩展点插件/04-permission-gate|第 4 章：permission-gate]] | 官方唯一 hook 插件示例逐行拆解：`ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`（引用 S2 权威代码） |
| 5 | [[11-实战-写hook扩展点插件/05-实战进阶|第 5 章：实战进阶]] | guard 单调否决示例：`ctx.tools.guard()` 返回 string=拒绝、undefined=弃权；agent-scoped 用 `agent.ctx`；演示「后面监听者无法翻案」 |
| 6 | [[11-实战-写hook扩展点插件/06-验证命令链|第 6 章：验证命令链]] | 复用 08 章验证四连（S1–S9 无验证链，需显式标注从本教程 08 章复用）：`pnpm dsh web --patch` 验加载 → `--dump-config` 验配置层 → `--dump-default-config` 验 bundle 默认 → `pnpm dsh --profile headless` 验端到端 |
| 7 | [[11-实战-写hook扩展点插件/07-迁移对照|第 7 章：迁移对照]] | 官方映射表（引用 S5）：`PreToolUse → tools/pre-execute`、`PostToolUse → tools/post-execute`、`UserPromptSubmit → agent/pre-step`、`Stop → agent/turn-stopping`、`SessionStart → agent/session-start`、`SubagentStart/SubagentStop → subagent/start\|end` |
| 8 | [[11-实战-写hook扩展点插件/08-小结与下一步|第 8 章：小结与下一步]] | 五扩展点选型口诀收口：权限门→`pre-execute`；单调最终拒绝→`guard()`；超时/重试/指标→`execute`；改结果/附 context→`post-execute`；只看不改→`result` |

> 建议从第 1 章开始顺序通读，第 2–3 章是语义地基，第 4–6 章动手写码，第 7 章迁移对照按需精读。

## 前置要求

- 已读《插件开发核心》01 章 3.5「hook 扩展点」速览（本篇的教学基线，不重复目录表格）
- 已读系列实战分册 04–10 章，特别是 08 章验证命令链（本篇验证直接复用）与 01 章 `apply(ctx)` / fiber / inject 心智模型
- 熟悉 Claude Code 扩展体系：hooks / `settings.json` / `hookSpecificOutput`
- 本地 dsh 源码仓库就绪（clone → `pnpm install` → `pnpm run build`），命令统一在仓库根目录执行

## 学完能做什么

- 说清 dsh 工具执行流水线的固定顺序与 5 个扩展点的职责边界（含 guard 单调否决、post-execute 替换 vs result 只读的取舍）
- 从零手写一个带权限门 + guard 一票否决 + post-execute 改汇报 + result 审计的 hook 插件，并用 08 章验证命令链跑通
- 读懂官方 `dsh-hooks-claude-code` 桥的映射表与限制，判断「搬现有 CC hooks 配置」还是「在 dsh 代码里手写插件」

## 建议学习顺序

- 顺序通读第 1–8 章：第 2–3 章语义模型是地基（约 45 分钟），第 4–6 章动手落地（约 1–1.5 小时），第 7 章迁移对照按需精读（约 30 分钟）
- 动手节奏：先照抄跑通 permission-gate（第 4 章），再逐个叠加 guard / post-execute / result（第 5 章），每加一个跑一次验证链（第 6 章），不要攒到最后一次验证
- 迁移对照（第 7 章）建议读完立刻做一次「你现有 CC hooks 配置 → dsh」的映射练习，沉淀成迁移笔记
- 预估总时间：通读约 2 小时；动手写第一个 hook 插件另加 1–2 小时

---

[[DeepSeek-Harness 插件开发教程/README|系列首页]] · [[DeepSeek-Harness MOC|教程 MOC]]
