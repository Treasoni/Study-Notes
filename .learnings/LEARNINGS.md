# LEARNINGS.md

最近一次维护：2026-09-11（`/maintain-learnings`）。已源头修复的条目移入
`.learnings/archive/`，其中 `LRN-20260911-008`（`todo-state.sh` 命令集与
`quality_gate`）、`LRN-20260911-010`（双链目标与锚点校验）已落到
workflow state template、`workflow-health-check.sh` 与 `note-beautifier`；
`LRN-20260905-007` 经核实已在 `chapter-writer.md` 落地。

## [LRN-20260911-009] best_practice — 超大笔记的组装/校验在父进程用 python 做，别指望子 agent 写入

**Logged**: 2026-09-11
**Priority**: medium
**Status**: pending
**Area**: workflow / 学习笔记生产

### Summary
本次成品 43k 汉字 / 228KB，note-assembler 直接拒写。父进程用 python 合并 + 校验可一次做对；但**反向扫描定位插入点时必须同时跳过空行和 `---` 分隔线**，否则扫描停错位置、改动静默不生效。

### Details
- 事实：组装脚本要「把每章末尾的过渡句从『本章来源对照』表格之前移到表格之后」。第一版从 `### 本章来源对照` 反向扫描找第一个非空行，结果撞上 `---` 分隔线，判定「无事可做」，4 条过渡句 0 条被移动且无报错；改为跳过空行 + `---` 后 4 条全部移动。
- 事实：中文字数统计用 `grep -o '[一-龥]' | wc -l` 在 C locale 下按字节匹配，给出 34,855 这类明显失真的数字；改用 `python3 -c "re.findall(r'[一-鿿]', t)"` 才准。
- 根因：反向扫描的终止条件写得太窄；`grep` 的字符类在 C locale 下按字节解释。
- 下次做法：文本组装/统计一律走 python；任何「扫描到某标记就动手」的脚本，先打印「本次改动 N 处」并在 N=0 时人工复核，不要静默通过。

### Suggested Action
- 把「改动计数 + N=0 需复核」作为所有批量文本改写脚本的固定自检项。

---

## [LRN-20260912-011] workflow — 已完成的 workflow 产物被单篇更新后，vault 与 workspace 副本必然漂移，要显式登记

**Logged**: 2026-09-12
**Priority**: medium
**Status**: pending
**Area**: workflow / 学习笔记生产

### Summary
`learning-note-flow` 运行 `openlist-webdav-rclone-docker` 已 `done` / `quality_gate: passed`。此后对单篇笔记做内容更新（走 `note-updater`，**不是**重开 workflow）时，发布到 vault 的正文变了，但工作区 `chapters/`、`output/` 里的副本不会跟着变 —— 两边**必然**长期漂移。本轮按用户确认的默认只改 vault，因此需要把漂移本身登记下来，避免下次有人拿 workspace 副本当"权威稿"回写。

### Details
- 事实：本轮只编辑 vault 侧 `docker/OpenList网盘挂载/OpenList网盘挂载-02-网盘聚合.md`（+3 行）与 `-03-WebDAV服务.md`（新增 §3.6 等，约 83 行变更），`workspace/openlist-webdav-rclone-docker/chapters/` 与 `output/` **未改动**。
- 事实：新增来源登记进 `workspace/openlist-webdav-rclone-docker/02_deep_research.md` §2（该文件是**来源总登记**，不是笔记产物），因此它是"两边都不算产物"的第三种文件：workspace 里、却应当随 vault 更新一起改。
- 事实：第 6 册文末的来源清单是**当册作用域**（开头写明「本章全部条目均回源核对后写成」），因此新来源只登记到 `02_deep_research.md` §2，不往第 6 册清单里塞跨册条目。
- 根因：workflow 的 `current_phase: done` 表示**生产流程结束**，不表示"笔记从此冻结"；后续单篇更新没有回写 workspace 的机制。
- 下次做法：单篇更新 vault 后，(1) 在 `.learnings/` 或 workflow state file 里记一句"vault 已更新，workspace 副本停留在 <日期>"；(2) 若用户希望两边一致，明确询问是"重跑 note-assembler 同步 workspace"还是"以 vault 为准、弃用 workspace 副本"，不要默认后者。

### Suggested Action
- 在 `note-updater` / `note-beautifier` 的收尾检查里加一项：本次是否改动了 vault 而 workspace 有同名副本，是则提示漂移。

---

## [LRN-20260912-012] anomaly — vault 被本会话之外的写者改动，先隔离再报告，不要顺手"修回去"

**Logged**: 2026-09-12
**Priority**: high
**Status**: pending
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

---

## [LRN-20260914-013] guard — 只校验「自己渲染的那部分」的守卫会给出空绿：hook 注册表指向已删脚本，bootstrap --check 仍报 OK

**Logged**: 2026-09-14
**Priority**: high
**Status**: pending
**Area**: Agent 平台配置 / bootstrap 校验

### Summary
`.claude/settings.json` 的 `Stop` 注册指向 `.claude/hooks/post_conversation.py`，而该脚本早在 2026-08-15（提交 `f0f8f8a5`）就被删除 —— 于是每次 Stop 都报一次 `can't open file ... [Errno 2] No such file or directory`。但 `.agent-sync/bootstrap.py --check` 全程报 `[OK] host-local hook settings are current`（exit 0）。根因：bootstrap 只校验**模板自己渲染出来的**脚本是否存在，而 `merge_managed_hooks` 会**原样保留**它不管理的本地条目 —— 「注册表里有、脚本却不存在」这一类恰恰落在校验盲区里。

### Details
- 事实：三处独立信号表明只有 SessionStart 是登记在册的 hook —— 模板 `.agent-sync/hook-templates/claude.json` 只有 SessionStart；`.codex/hooks.json` 只有 SessionStart；hook manifest 只有 `read-learnings` 一个。故「删脚本」方向对，「留下注册」才是残留。
- 事实：`git show --stat f0f8f8a5` 显示 `.claude/hooks/post_conversation.py` 与 `.codex/hooks/post_conversation.py` 各删 98 行、两侧对称 → 是一次干净退役，注册表没跟上。
- 根因：**守卫只覆盖自己产出的子集**。`merge_managed_hooks` 的存在意义就是保留本地条目，而这条保留路径没有任何校验，等价于「保留 = 免检」。
- 修法：在 `desired_outputs` 里对 **merge 之后**的完整配置跑 `missing_hook_scripts()`，缺失即 `ValueError` → exit 2（不静默删、不静默过）。
- 验证（红→绿双向）：加守卫后 `--check` 立刻 `[ERROR] claude: .claude/settings.json registers hook scripts that do not exist: .claude/hooks/post_conversation.py`（exit 2）；摘掉退役注册后恢复 `[OK]`（exit 0）。另向 `.codex/hooks.json` 瞬时注入一条死注册，`--check` 同样 exit 2 且点名 codex，注入后文件 sha256 逐字节还原。

### Suggested Action
- 凡是「合并 / 保留外部条目」的生成器，校验必须跑在**合并结果**上，而不是只跑本次渲染的子集；否则保留路径天然免检。
- 退役一个 hook 时，删脚本与删注册必须同时做：脚本在 git 里被删，不会让注册表自动更新。

---
