# LEARNINGS.md

最近一次维护：2026-09-18（`/digest`，后由 `update-hermes-ha-volume` 运行补记 `LRN-20260918-019`）。
本轮新增 `LRN-20260918-017`（Discourse 正文只走 `/t/<id>.json`）、
`LRN-20260918-018`（产物落点用仓库内路径；工具可用性先探测）、
`LRN-20260918-019`（核对 Hermes Skills Hub 必须查中央索引，不能用仓库内 `optional-skills/` 代替）。
三条的处置办法已提炼进 RULES.md。
`LRN-20260912-012`（vault 并发写入，写者身份未定）继续挂起，**不可归档**。
RULES.md 里「拼接式文档生成：追加前先对既有尾部做幂等归一」一条**本轮在真实运行里没拦住**
（见 `ERRORS.md` 的 `-008` / `-009`），按 digest 规定应转 `maintain-learnings` 做源头修复。

上一次维护：2026-09-14（`/maintain-learnings`）。已源头修复或已提升为 RULES 铁律的条目移入
`.learnings/archive/`，本轮归档 `LRN-20260912-011`（→ `note-updater` Workflow 第 6 步「登记
vault / workspace 漂移」）、`LRN-20260914-014` / `-015` / `-016`（处置办法已完整落在 RULES.md），
早前归档 `LRN-20260911-009` / `LRN-20260914-013`（规则已入 RULES.md）。
逐条的修复路径、验证方式与处理结果见 `.learnings/archive/2026-09-14-maintenance.md`（本轮）
与 `.learnings/archive/2026-09-14-archived.md`（digest 压缩）。

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

## [LRN-20260918-017] knowledge_gap — Discourse 论坛的帖子正文只走 `/t/<id>.json`，HTML 路径会漏抓

**Logged**: 2026-09-18T01:21:05+0800
**Priority**: high
**Status**: 已办（已写进 `02_deep_research.md` §5.7 工具坑 + §5.7.1 回填）
**Area**: research-collector / 来源取回

### Summary
以 Discourse 为底座的社区论坛（`community.home-assistant.io`、`community.simon42.com` 等）取**帖子正文**的可靠路径是
`curl 'https://<host>/t/<topic-id>.json'`（多页用 `?page=N`，或看响应的 `post_stream.stream` 拿全部 post id），
走 HTML / crawl4ai 会拿到 403/522 或只有壳而无帖子正文。

### Details
- 事实：本轮两帖（`COM-22` = `…/t/736566.json`、`COM-16` = `…/t/88707.json`）HTML 路径被 Cloudflare 拦住；
  换 `/t/<id>.json` 后均 **HTTP 200**，落盘全文快照分别是 20 帖 / 4 帖，**逐字命中**了此前无法核验的三条引语
  （`1 token is equal to approx 4 characters`、`totalling 0.66$`、`Die Messages schnappen sich aktuell 110k Tokens.`）
  以及 §9.2 表格的四个数字。
- 事实：快照可用普通 `grep` 对引语逐字比对——这就是「可比对字节」，是把证据置信度从「中」升到「高」的唯一凭据。
- 根因：Discourse 的 SPA 壳负责渲染，正文由 API 返回；抓 HTML 的通用工具（crawl4ai）只能拿到壳与首帖摘要，
  **不报错、静默漏抓**，很容易被误判成「来源不可得」。
- 教训（已落进笔记）：漏抓 ≠ 来源不可得。**在把置信度降格、或写「未核验」之前，必须先换取回路径再试一次**；
  本轮就是这样把先前记的「置信度中 / 未核验」闭掉的。

### Suggested Action
- 遇到 `community.*` 且页面像 Discourse（`/t/<slug>/<id>` 结构），直接用 `/t/<id>.json`。
- 把「抓取产物里没有目标段落」先当成**取回方式问题**，而不是来源缺失；换路径重试后再决定是否降格证据。
- 落盘快照到 `workspace/<slug>/sources/`，命名带来源 ID，便于日后逐字复验。

---

## [LRN-20260918-018] best_practice — 沙箱里的产物落点：用仓库内路径 + 仓库相对路径读回

**Logged**: 2026-09-18T01:21:05+0800
**Priority**: medium
**Status**: 已办（本轮照此改法即成功）
**Area**: 工具使用 / 沙箱

### Summary
在 Bash 里 `curl -o /tmp/x.json`，再在**另一次调用**里用 Python 读 `/tmp/x.json`，会 `[Errno 2] No such file or directory`
——shell 的工作目录与沙箱的 `/tmp` 映射在调用之间不保证一致。快照/中间产物应**直接落到仓库内路径**，用仓库相对路径读回。

### Details
- 事实：`curl -o /tmp/com16.json` 成功，紧接着的 Python 读 `/tmp/com16.json` 报 `[Errno 2]`；改成
  直接写 `workspace/hermes-home-assistant/sources/COM-16-simon42-88707.json`、再用同一相对路径读，一次通过。
- 事实（同一轮的相邻教训）：「能不能用 API 落这项配置」要先探测可用性——本机 `obsidian` 可执行文件**存在**，
  但 **CLI 未启用**，因此「改 Obsidian 忽略目录」这件事根本无法用 API 落，最终决定不改用户配置。
  探测动作很小（读 `.obsidian/app.json`），但结论改变了决策。
- 根因：把宿主 `/tmp` 当作跨调用稳定的暂存区；把「命令存在」当作「命令可用」。

### Suggested Action
- 落盘产物一律用仓库内相对路径（`workspace/<slug>/sources/…`），不要用 `/tmp` 当跨调用中转。
- 判断某工具/配置项能否落地，先做一次最小可用性探测（读配置文件 / `--help` / 退出码），再决定要不要写进方案。

---

## [LRN-20260918-019] research-collector — 核对 Hermes Skills Hub 必须查中央索引，不能用仓库内目录代替

**Logged**: 2026-09-18T02:40:00+0800
**Priority**: high
**Status**: 已办（本轮据此推翻并更正了已发布分册里的一处事实性错误结论）
**Area**: research-collector / source policy / 已发布笔记更正

### Summary
把「Hermes Skills Hub」当成 Hermes 仓库里的 `optional-skills/` 目录去核对，会得到与事实相反的结论。
Hub 是**联邦注册表**，它的检索由一份**中央索引**回答；仓库内目录只是其中的 `official` 一支
（150 条，占索引 97,986 条的一支）。本轮据此发现已发布分册里「Hub 里没有现成的 Home Assistant skill」是错的
——明示 Home Assistant 的 skill 实为 **64 条**。

### Details
- 事实：中央索引 `https://nousresearch.github.io/hermes-agent/docs/api/skills.json`（单行 JSON，约 60.8 MB）。
  截至 2026-09-18 的快照：97,986 条记录；明示 Home Assistant 的 **64 条**（ClawHub 52 + skills.sh 12）；
  `category: smart-home` 但未点名 HA 的 13 条；`official` 支 150 条。索引支持 8 类来源：
  `official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh`。
- 事实：**这一层错本可以被自己的来源拦住**——该册自己的来源 `HMS-05`（`skills.md`）就写着 Hub 是联邦索引、
  并列出了这 8 类来源。所以错误不是「缺来源」，而是**没读全已有的来源**。
- 根因：把「本仓库里有什么」当成了「整个注册表里有什么」。联邦制系统里本地目录只是其中一个 source，
  用它的结果去下全称结论（「不存在」「没有可装的」）几乎必然出错。
- 连带的第二层错：同一册还断言「HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI」。`hass-cli`
  （`home-assistant-ecosystem/home-assistant-cli`，596★，2026-08-04 pushed，未归档）存在，Hub 里也有封装它的条目；
  但它是 **Home Assistant Ecosystem 组织**的社区事实标准，**不是 HA core 官方出品**——Hub 条目自述里的 "official"
  措辞不精确，不能沿用。
- 教训：「skill 不存在」与「CLI 不存在」是**两个各自独立**的核对项，不能互相推出，也不能一并结案。
- 方法论收获：两个错误都被**同一句正确洞察**兜住——「skill 是知识，不是能力」。结论错的地方，洞察是对的；
  更正时保留了洞察、只修事实与作用域，避免把对的部分一起推翻。

### Suggested Action
- 核对任何**联邦 / 聚合式**注册表（Skills Hub、插件市场、包索引、模型仓库）时，先找到它自己的
  **中央索引或 API 端点**并在索引上检索；**不要**用「本仓库内的目录清单」代替。
- 写全称否定结论（「没有 X」「不存在 Y」）之前先自问：**我核对的这个范围，是不是就是这句话的作用范围？**
  并把作用域写进句子本身——「`official` 支里只有 `openhue`」而不是「Hub 里只有 `openhue`」。
- 索引类证据必须带时点限定（「截至 YYYY-MM-DD 的快照」），并把快照落盘到 `workspace/<slug>/sources/` 以便逐字复验。
- 更正依赖否定结论的旧笔记时**分两层**处理：范围错（查错了地方）与事实错（断言本身为假）分开写、
  分开改，不要混成一次「补充说明」——两层的原因与修法都不同。

---
