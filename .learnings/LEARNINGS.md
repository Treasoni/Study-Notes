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

---

## [LRN-20261006-028] correction — 字段/模板旁的注释是线索，不是权威取值；注释自相矛盾时要取独立来源 + 实测一致的读法

**Logged**: 2026-10-06
**Priority**: high
**Status**: pending（机制待落 canonical `note-updater` SKILL.md「配方类内容」小节）
**Area**: 学习笔记内容正确性 / 出处纪律

### Summary
小雅单容器部署笔记把 WebDAV 默认用户写成「用户名固定是 `dav`，不是 `guest`」，还配了同向的 `[!warning]`——**正好写反**。用户实战反证：该密码（`guest_Api789`）对应的默认账号是 `guest`。根因是把 monlor `env` 模板里一行**自相矛盾**的注释（`# webdav用户名为dav，设置密码。默认用户密码：guest/guest_Api789`）的**前半句**当成权威取值；它其实是把挂载**路径** `/dav` 误写成了「用户名」。

### Details
- 事实：多个独立来源一致给出 `用户 guest / 密码 guest_Api789 / 路径 /dav`——官方 hub 页（`sources/01_hub_docker_com.md:18`：`webdav 账号密码 用户: guest 密码: guest_Api789`）、论坛楼主实测答复（`sources/forum/tid-9690.md:280`：`用户名： guest 密码：guest_Api789 路径：/dav`）、社区教程（`sources/p3/z-addone/01_www_cnblogs_com.md:44`：`账户：guest`）。
- 根因：把「**字段旁边的注释**」等同于「文档逐字给出的取值」——既有规则（配方类内容：「只写文档逐字给出 / 实测得到的取值」）只列了这两个来源，未把「模板自带注释」单列出来质疑。注释原文自身两个子句互相矛盾，却被只取其一当结论；同一条注释还误导过论坛用户往 `WEBDAV_PASSWORD` 里塞整串账号（`tid-9690.md:259`、`:283`）。
- 附带缺陷：出处行号未核实——注释在第 31 行，笔记却一直引 `:32`（`WEBDAV_PASSWORD=` 字段行）。
- 下次做法：注释只当**线索**；注释与多个独立来源 / 实测冲突时**以后者为准**，并把注释原文**逐字留档**（不静默删），在旁解释它为何易误读；写「注释里的 X 其实是 Y」这类纠正句前，先问「这句注释有没有可能把两个概念混写了」。

### Suggested Action
- 把「字段旁注释 ≠ 权威取值；注释自相矛盾时取独立来源 + 实测一致的读法，并逐字留档」补进 canonical `note-updater` SKILL.md 的「配方类内容」小节，再走 `.agent-sync` 同步 + `workflow-health-check.sh` 收口（`.claude/` 为生成目录，不手工编辑）。
- 引 `:行号` 前先 `rg -n` 定位一次，不凭上一轮转录誊抄。
- 本次落地见 `ERR-20261006-021`；修正产物：`流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`、`04 部署实战.md`。

---
