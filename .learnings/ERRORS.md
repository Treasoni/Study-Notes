# ERRORS.md

活跃错误记录：当前 **1** 条（`ERR-20261006-021`）。本文件里的 E 编号与 `LEARNINGS.md` 的 L 编号各自独立计数。

**归档门槛（2026-10-06 修订）**：同 `LEARNINGS.md` —— **机制在位 + 经一次维护轮复核通过**
即可归档，全文移入 `.learnings/archive/`；「机制是否在真实运行中生效」是归档块里的**观察项**，
不再是归档前置条件。（原门槛「须在下一轮真实运行中被观察到生效」对低频缺陷不可证伪。）

新增错误追加到本文件末尾（错误 / 触发场景 / 根因 / 修复 / 预防措施）；
修复落到机制并验证通过后，才可移入 `.learnings/archive/`。

最近一次维护 **2026-10-06（第五次，`/maintain-learnings`）**：归档 `ERR-20260929-014` / `-015`、
`ERR-20261006-019` / `-020` 四条，活跃文件清空；逐条机制复核与处置见
`.learnings/archive/2026-10-06-maintenance.md` 第七节。
更早的归档见 `.learnings/archive/`（各维护报告与 `-archived.md`）。

---

## [ERR-20261006-021] note-updater：把模板注释的半个子句当权威取值，结论写反

**错误**：小雅 fnOS 部署笔记第 3 章 §3.3.2 与第 4 章自检把 WebDAV 默认用户写成「用户名固定是 `dav`，不是 `guest`」（并配同向 `[!warning]`），与实际相反；用户实战反证默认账号是 `guest`。

**触发场景**：从 `env` / compose 模板落凭据类取值时，模板里字段旁自带一行注释。

**根因**：注释 `# webdav用户名为dav，设置密码。默认用户密码：guest/guest_Api789` 两个子句自相矛盾，只取前半句即落盘；且把「注释」误当「文档逐字给出的取值」（既有规则的「文档逐字给出 / 实测得到」两个合法来源未涵盖它）。附带：出处行号 `:32` 未核实（注释实为 `:31`，`:32` 是 `WEBDAV_PASSWORD=`）。

**修复**：
- 第 3、4 章就地修正为 `用户 guest / 密码 guest_Api789 / 路径 /dav`；monlor 注释**逐字留档**，改写为「`dav` 是**路径**不是用户名」；补 3 个独立来源回源（引文对照新增 3 行）；出处 `:32` → `:31`。
- `publish_copies.py --apply`（03/04）+ `assemble_final.py --apply` 重建三副本与合并件；`publish_copies.py --check`（7/7 `output==`/`vault==`）、`assemble_final.py --check`（0 章需更新）、`note-citation-check.py`（✅ 无硬失败、C 族 0 差异）、`check-md-structure.py`（0 处）全通过。

**预防措施**：
- 落「模板 / 字段注释」里的取值前**通读整条注释**；子句互相矛盾、或与多个独立来源 / 实测冲突时，以后者为准，注释原文逐字留档。
- 引 `:行号` 前先 `rg -n` 定位一次。
- 反思链：`LRN-20261006-028`（同批）；机制**已落** canonical `.agents/skills/note-updater/SKILL.md` v1.5.0「配方类内容」小节（2026-10-06 经 `.agent-sync` 同步 + `manifest-registry validate` 通过）。

---
