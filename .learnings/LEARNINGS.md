# LEARNINGS.md

活跃学习记录：当前 **1** 条 —— `LRN-20260912-012`（anomaly，挂起，根因未消除，**不可归档**）。

**归档门槛（2026-10-06 修订）**：**机制在位 + 经一次维护轮复核通过**，即可归档；全文移入
`.learnings/archive/`，`.learnings/RULES.md` 保留铁律。原门槛要求「机制在**下一轮真实运行中
被观察到生效**」——对**低频缺陷**不可证伪（错误不复发就永远观察不到，经验库会无限期堵住），
2026-10-06 由用户拍板改为此条；「是否在真实运行中生效」转为归档块里的**观察项**，不再是归档
前置条件。同一句已同步进 `ERRORS.md` 头部。

新增记录追加到本文件末尾，头格式 `## [LRN-YYYYMMDD-NNN] <category> — 一句话结论`，
正文含 `**Logged**` / `**Priority**` / `**Status**` / `**Area**` 与
`### Summary` / `### Details` / `### Suggested Action`。

最近一次维护 **2026-10-06（第五次，`/maintain-learnings`）**：归档 9 条积压记录并压缩活跃文件，
逐条机制复核与处置见 `.learnings/archive/2026-10-06-maintenance.md` 第七节。
更早的归档见 `.learnings/archive/`（`2026-08-15` / `2026-09-11` / `2026-09-14` / `2026-09-23`
/ `2026-09-29` / `2026-09-30` / `2026-10-06` 各维护报告与 `-archived.md`）。

---

## [LRN-20260912-012] anomaly — vault 被本会话之外的写者改动，先隔离再报告，不要顺手"修回去"

**Logged**: 2026-09-12
**Priority**: high
**Status**: pending（写者身份未确定，根因未消除；不可归档）
**Area**: 项目安全 / 并发写入

### Summary
本轮编辑期间，`docker/OpenList网盘挂载/OpenList网盘挂载-04-Rclone挂载.md` 在**本会话从未触碰**的情况下被重写：`git diff --stat` 显示 509 行变更（231 插入 / 364 删除），HEAD 45049 B → 工作区 31018 B，删掉了脚注 `[^c4-1]`/`[^c4-3]`，标题从 `## 4.1 核心概念` 改成 `## 4.1 概念`、`### FUSE 的三件套` 改成 `### FUSE 三件套与自检`。文件 mtime 23:53:17 正好夹在本轮两次编辑（23:52:27、23:54:15）之间。另有一个瞬时文件 `workspace/openlist-webdav-rclone-docker/sources/docker/OpenList网盘挂载/OpenList网盘挂载-04-Rclone挂载.md`（31018 B，与 vault 第 4 册逐字节相同）出现约 1 分钟后消失。

### Details
- 事实：`.claude/settings.json` 注册的 hooks（SessionStart `read_learnings.py`、Stop `post_conversation.py`、SessionEnd `collect-usage.py`）都不会写笔记正文；`CronList` 为空；因此排除本会话自身机制。
- 事实：`git status --short` 里只有第 2、3、4 册 + `02_deep_research.md` 为 modified，其中第 4 册**不是**本轮的改动。
- 推断（未证实）：另一个 agent 会话或 Obsidian 插件正在编辑同一个 vault。
- 根因：无法从本会话内确定写者身份。
- 下次做法：**不要回滚、不要"修回 HEAD"**（那会覆盖别人未提交的工作）。做法是：把自己改的文件与异常文件在报告里分开列，明确写出"这几处不是我改的"，让用户决定。

### Suggested Action
- 报告疑似并发写入时，附「文件 / 行数 / mtime / 与 HEAD 的差异摘要」四要素，便于用户对照自己的其他会话。
- 若再次发生，升级为需要在会话外解决的并发写入问题（见 `.learnings/archive/2026-09-14-maintenance.md`「下轮维护提示」）。
- 补充（2026-10-06）：本 vault 存在**自动备份**，每 3~6 分钟提交一次（`zhq vault backup: <datetime>`，提交者 `zhq`）。核对「文件是否已被提交 / 是否有人在并发写」时，先把这类自动提交排除在外，不要误判为并发写入。
