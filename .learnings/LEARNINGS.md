# LEARNINGS.md

活跃学习记录：当前 **3** 条 —— `LRN-20260912-012`（挂起）、`LRN-20260929-020` / `-021`
（2026-09-29 记，状态 `pending`）。

最近一次维护 2026-09-30（`/maintain-learnings`）：归档 `LRN-20260930-022`
（该偏好的四条判据已全部机器化，改由共享引文校验器的 `S1` / `S2` / `S3` / `S4` 与 `C` 强制），
条目全文见 `.learnings/archive/2026-09-30-archived.md`，
处置路径与验证方式见 `.learnings/archive/2026-09-30-maintenance.md`。
再上一次 2026-09-29 归档 3 条已落机制且经验证的记录（`LRN-20260918-017` / `-018` / `-019`），
见同目录对应文件。

`LRN-20260912-012`（vault 被本会话之外的写者改动，写者身份未定）**不可归档**，继续挂起。

新增记录追加到本文件末尾，头格式 `## [LRN-YYYYMMDD-NNN] <category> — 一句话结论`，
正文含 `**Logged**` / `**Priority**` / `**Status**` / `**Area**` 与
`### Summary` / `### Details` / `### Suggested Action`。

只有**已落到机制并被验证**的记录才可归档；未修复、未验证或仍需观察的继续留在本文件。

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

---

## [LRN-20260929-020] correction — 跨章一致性比对只查「可照抄的配置块」，漏掉散文式转述与定义句

**Logged**: 2026-09-29T23:35:00+0800
**Priority**: high
**Status**: pending（机制已落 workflow 阶段 4，下轮复核后归档）
**Area**: learning-note-flow / chapter-writer

### Summary
`workflow.md` 阶段 4 的跨章比对只覆盖「可照抄的配置块」（且只比冻结标签），不覆盖
**对同一份来源的散文式转述**与**定义 / 判据句**。第 2 章 L44 把 Hermes 文档的 4 条 profile
用途概括成「示例用途是「同一个人的多个 agent」」，而同一份文档 `:14` 是「每个家庭成员一个」
——两章对同一份清单做了相反定性，靠用户读已发布笔记才被发现。

### Details
- 事实：`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:9` 是
  多 profile / 多实例路径，`:14` 是「每个家庭成员一个」。L44 的「示例用途是」把一个**并列清单
  中的一条**说成了全部。
- 根因：比对规则的作用面是「可照抄的配置块」，而这类漂移发生在**散文**里；验收只看
  「有没有引到原文」，不看「同一来源在别处是怎么被定性的」。
- 同轮的第二例（同一根因家族、不同检测目标）：上游判据句与下游术语框架冲突，见
  `ERRORS.md` 的 `ERR-20260929-015`。
- 下次做法：三类全覆盖——① 可照抄的配置块 ② 同一来源的转述与定性并排读 ③ 定义 / 判据句
  对冻结语义框架自洽。并列清单要说「其中一条」，不说「就是」。

### Suggested Action
- `workflow.md` 阶段 4「并行写作的跨章口径」已扩到三类，新增第 ④ 条要求把比对结果
  （命中处 / 归一结果 / 判定为合法异体的理由）写进 state file 的异常记录。
- 该比对属**父流程 P4 关卡**：单章写作代理看不到其他章，不要下放成逐章自检。

---

## [LRN-20260929-021] knowledge_gap — P1 的搜索摘要级候选与已抓原文混放，须标注证据形态

**Logged**: 2026-09-29T23:20:00+0800
**Priority**: medium
**Status**: pending（机制已落 research-collector，下轮复核后归档）
**Area**: research-collector / P1

### Summary
P1 的候选记录（标题 / URL / tier / 相关性 / 分数）本身不区分**证据形态**：一条只是搜索结果
摘要，一条已取回正文，两者在 `01_explore_result.md` 里外观相同。本轮只把这件事写在了
该文件 §3.1 的说明文字里，没有变成字段或校验。

### Details
- 事实：搜索摘要级信息与已抓取原文在同一个候选表里，下游无法从记录本身判断某条能否当证据用。
- 根因：与「转述带引用」同属一类——**把弱形态的证据当强形态用**，且没有任何字段拦住它。
- 下次做法：每个候选标注 `snippet-only` 或 `fetched`；P2 只把 `snippet-only` 当线索去取，
  不当证据。

### Suggested Action
- `research-collector` SKILL.md 的 P1 第 3 步已要求标注证据形态，完成标准已加断言。

---

