# LEARNINGS.md

活跃学习记录：当前 **4** 条 —— `LRN-20260912-012`（挂起）、`LRN-20260929-020` / `-021`
（2026-09-29 记，状态均 `pending`）、`LRN-20261006-025`（2026-10-06 记，状态 `pending`）。

本次 `/digest`（2026-10-06）：`LEARNINGS.md` 109 行已越过 100 行的压缩阈值，故**先走压缩检查**——
但在册三条均不符合归档条件（`-020` / `-021` 待下轮复核，`-012` 明确挂起），
**压缩为空操作，文件不截断**。

同日 `/maintain-learnings`：把 `LRN-20261006-025` 的机制落到 `note-updater` v1.4.0「配方类内容」
+ `chapter-writer` v1.5.0 同名小节与 Checklist；**因尚未在下一次运行中被观察验证，本轮不归档**，
状态转 `pending（机制已落，下轮复核后归档）`。处置见 `.learnings/archive/2026-10-06-maintenance.md` 第五节。

最近一次维护 2026-10-06（`/maintain-learnings`，第二次，承接同日 `/digest`）：归档当日会话内
就地修复的三条——`LRN-20261006-023` / `-024` 与 `ERR-20261006-018`（夸克口径出错的两族根因）。
机制 = `note-updater` SKILL.md **v1.3.0** 新加的「先判形态，再读最小上下文」与「口径核对（先于改写）」两节；
处置路径与验证方式见 `.learnings/archive/2026-10-06-maintenance.md` 第四节。

最近一次维护 2026-10-06（`/maintain-learnings`）：归档 `LRN-20261006-022`
（「内容校验全绿 ≠ 可渲染」——机制已落 `note-beautifier` Step 4 的「Obsidian 结构自检」小节
与 `.codex/scripts/check-md-structure.py`），处置路径与验证方式见
`.learnings/archive/2026-10-06-maintenance.md`。

上一次 2026-09-30（`/maintain-learnings`）：归档 `LRN-20260930-022`
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

## [LRN-20261006-025] correction — 配方类内容：文档没逐字给出的取值不得用常识补，派生产物必先实测

**Logged**: 2026-10-06T15:55:11+0800
**Priority**: high
**Status**: pending（机制已落 `note-updater` v1.4.0「配方类内容」+ `chapter-writer` v1.5.0 同名小节与 Checklist；下轮复核后归档）
**Area**: 笔记生产 / 内容准确性（`chapter-writer` · `note-updater`）

### Summary
审计成品第 11 章「Dashboard 认证配置」发现两处同源缺陷：① 官方文档只给了字段名、没给示例值，
撰写时用「常识」补了一串 **bcrypt** 哈希（`$2b$12$…`），而 Hermes 实际用的是 **scrypt**（`scrypt$`）；
② 我本轮把该字段转写成 **docker-compose `environment:` 片段**时未实测就落笔，漏了 Compose 会把
`$`+字母当作变量插值、哈希必须写成 `$$` 的坑。两处共同点：**把文档逐字照抄当终点，缺的用常识填、
派生的不过测。**

### Details
- 出处：`AI学习/Hermes Agent/Hermes Docker 部署指南/11-Dashboard认证配置实战.md`。原文 2026-09-01 首建
  （bcrypt 来自上一轮会话，提交 `cdf6678c`），compose 片段由我 2026-10-06 的编辑引入。
- ① 取值编造：官方文档逐字写的是 `password_hash: ""  # scrypt$...`
  （`…/sources/05_hermes-agent_nousresearch_com.md:513`、`…/sources/S11_configuration.md:2639`），
  **从未出现 bcrypt**；写成 `$2b$12$` 属**用常识填补文档空白**。
- ② 派生未测：把「环境变量名 + scrypt 串」翻成 compose YAML 是一个**新产物**，Compose 的 `$` 插值规则
  （`$`+数字→字面量、`$`+字母/下划线→变量、`$$`→字面量 `$`）文档不会替你想。实测（Docker Compose
  v5.0.2）确认：YAML 引号 / `env_file` / `.env` **都挡不住**，只有 `$$` 有效。
- 结构性缺口：该章不在 workflow state 内（`workspace/workflow-runs/hermes-docker-deploy.workflow.md`
  只登记 10 章、P4 已 `complete`），追加章节没有阶段门禁，属「工作流外产物」。

### Suggested Action
- 配方类内容（env / config / command）三分法：① 文档**逐字给出**才直接写；② 未给出就标「待核」或回
  原始载体（源码 / 官方示例 / 实测输出）取；③ 由文档**派生**的新产物（compose / 示例配置 / 命令拼接）
  落笔前**必做最小实测**——「读文档」不等于「跑得通」。
- 同批 `ERR-20261006-019` 记录了具体产物缺陷；防护规则见 `RULES.md` `## Do` 新增条目。

---

