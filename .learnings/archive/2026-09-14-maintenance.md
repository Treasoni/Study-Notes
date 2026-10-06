# 维护归档 · 2026-09-14（`/maintain-learnings`）

本轮维护由用户执行 `/maintain-learnings` 触发。审计脚本：
`.claude/skills/maintain-learnings/scripts/audit_learnings.py`（Claude Code profile）。

**维护前活跃文件体量**：LEARNINGS 123 行 / ERRORS 59 行 / RULES 62 行。
**触发判据**：LEARNINGS 超 100 行；审计报告 `general` / `hook` / `research` / `markdown`
四个 high 聚类各有 2–3 条活跃记录。

## 本轮落地的源头修复

| # | 修复对象（canonical） | 变更 | 服务的记录 |
|---|----------------------|------|-----------|
| 1 | `.agents/skills/maintain-learnings/scripts/audit_learnings.py` | 入口处 `sys.stdout/stderr.reconfigure(encoding="utf-8", errors="replace")` | RULES「会打印 `.learnings` 内容的脚本必须自己把输出流设成 UTF-8」——**规则早已存在，违反者是维护工具本身** |
| 2 | `.agents/skills/workflow-todo-state/SKILL.md`（State Rules） | 新增硬约束：阶段行 / `current_phase` / `current_status` 只能由脚本写；编辑 state file 的其他内容时必须把 `> [PN] …` 行排除在编辑之外，并 `grep -n '^> \[P'` 复核 | `ERRORS.md` 手工改写阶段行 |
| 3 | `.agents/skills/note-updater/SKILL.md`（Workflow 新增第 6 步） | 登记 vault / workspace 漂移：写明哪一侧已更新、另一侧停在何时；不默认回写、不默认 vault 权威 | `LRN-20260912-011` |
| 4 | `.agents/skills/note-beautifier/SKILL.md`（美化验证清单新增一节） | 「分册 / 长文档发布」自检：逐字一致、结构小标题计数 == 期望值、生成与校验共用同一个命名函数、导航双链逐条断言存在、发布后逐行读成品 | `ERRORS.md` 发布脚本 4 处自造缺陷 |

**manifest 版本**：`note-beautifier` 1.1.0 → 1.2.0；`note-updater` 1.0.0 → 1.1.0；
`workflow-todo-state` 0.1.0 → 0.2.0；`maintain-learnings` 0.1.0 → 0.1.1。

**验证方式**：

1. 脚本修复后**不设** `PYTHONIOENCODING` 直接运行，报告正文中文可读（修复前为 GBK 乱码）——
   红→绿可复现。
2. `python3 .codex/platform/manifest-registry.py --root . validate` → `Manifest registry validation passed (60 artifacts)`。
3. `python3 .agent-sync/sync_agents.py --root . --check --scope skills` → 恰好 8 个预期文件 `[DRIFT]`，
   无意外漂移；`--apply --scope skills` 后全量 `--check` → `[OK] shared agent configuration is synchronized`（exit 0）。
4. 四个 skill 的 frontmatter 元数据断言通过（`name:` + `description:` + YAML 头完整）。

---

## 归档记录

### 1. `LRN-20260912-011` — 已完成的 workflow 产物被单篇更新后，vault 与 workspace 副本必然漂移

**原记录摘要**：`openlist-webdav-rclone-docker` 已 `done` 后对单篇笔记做内容更新（走 `note-updater`），
只改了 vault 侧，`workspace/<run>/chapters/` 与 `output/` 未动 → 两边必然长期漂移；
`02_deep_research.md` 属「两边都不算产物」的第三种文件。

**修复路径**：`note-updater` Workflow 新增第 6 步「登记 vault / workspace 漂移」，
把「写明哪一侧已更新、另一侧停在何时」和「询问以 vault 为准还是回写 workspace」变成技能的固定动作。

**验证方式**：`note-updater/SKILL.md` 出现该步骤；skills 同步 check/apply 通过；manifest 升 1.1.0。

**处理结果**：归档。规则不再需要单独占一条活跃记录。

---

### 2. `ERRORS.md`（2026-09-14）— learning-note-flow / P6 分册发布：发布脚本自己造出 4 处文本缺陷

**原记录摘要**：`publish_series.py` 在「切片与源文件逐字校对」通过的前提下仍产出 4 类缺陷
（重复 `## 参考来源`、`## 相关笔记` 缺空行、46 条假死链、文件名去空格），且第一版校验对其中 3 类全绿。
根因：改了 `paras` 却让 `core` 保留原尾部；生成侧与校验侧用了两套名字表示；文件名从标题推导。

**修复路径**：机制加在 `note-beautifier` 的「分册 / 长文档发布」自检节 ——
逐字一致断言、结构小标题出现次数 == 期望值、生成与校验共用同一个命名函数、
导航双链逐条断言存在、发布后逐行读成品。该节对应「美化 → 发布」这一步，
本项目的分册发布正是由 `note-beautifier`（阶段 6）负责，落点正确。

**验证方式**：`note-beautifier/SKILL.md` 出现该节；skills 同步 check/apply 通过；manifest 升 1.2.0。

**处理结果**：归档。具体修复代码仍留在 `workspace/music-tag-web/_verify/publish_series.py`（脚本即产物）。

---

### 3. `ERRORS.md`（2026-09-14）— workflow state file：手工改写阶段状态行，绕过 `todo-state.sh`

**原记录摘要**：P6 收尾时在同一次 Edit 中顺手把 `> [P6] 🔲 进行中 {in_progress}` 改成
`✅ 已完成 {complete}`，违反「阶段状态只能通过 `todo-state.sh` 变更」；发现后自纠并改走脚本。

**修复路径**：`workflow-todo-state/SKILL.md` 的 State Rules 增加硬约束 ——
脚本是阶段状态的唯一写者；编辑 state file 的其他内容时必须把 `> [PN] …` 行排除在编辑之外，
改完 `grep -n '^> \[P'` 复核。该 skill 是状态机的定义方，本项目的 `.claude/scripts/todo-state.sh`
即由它的 `scripts/` 提供，因此约束加在这里能被所有 workflow 继承。

**验证方式**：`workflow-todo-state/SKILL.md` State Rules 出现该条；同步 check/apply 通过；manifest 升 0.2.0。

**处理结果**：归档。

---

### 4. `LRN-20260914-014` — Stop hook 反复报「Background subagents are still running」

**原记录摘要**：Claudian 插件的子代理注册表每标签页、纯内存；被取消的异步子代理永久占位，
`hasRunningSubagents()` 无超时，`data.json` 无相关字段 → 每次 Stop 阻断，只能重载插件。

**修复路径**：**项目侧无法修复**（第三方插件内部实现）。
处置办法已完整提炼为 RULES.md「Watch For」铁律：先用 `TaskOutput task_id=<id> block=false` 证伪、
给出用户侧动作、绝不编造或预测未到达的结果、不要反复刷屏。

**验证方式**：RULES.md 现有该条（2026-09-14 digest 写入），本轮逐字复核仍在。

**处理结果**：归档（规则已在 RULES；无未决的项目内动作，唯一外行动作「向 Claudian 提 issue」仍写在 RULES 与本节）。

---

### 5. `LRN-20260914-015` — 偏离「已批准的具体方案」可以，但必须在报告里显式声明

**原记录摘要**：P7 用户批准的是具体落点（网盘聚合节），执行时发现主题不符，
改为新建 `### 音乐标签与整理` 小节并在报告中显式声明偏离。

**修复路径**：属交互纪律，不需改工具；已提炼为 RULES.md「Watch For」铁律
（原方案 / 实际做法 / 理由三要素，放在显眼处）。

**验证方式**：RULES.md 现有该条，本轮逐字复核仍在。

**处理结果**：归档。

---

### 6. `LRN-20260914-016` — vault 路径上 `rm -rf` 被拒时，把清理逻辑移进脚本并加外来文件保护

**原记录摘要**：`rm -rf` 在 vault 路径被拒；改为脚本内「前缀白名单删除 + 外来文件即失败退出」。

**修复路径**：RULES.md「Do」新增铁律（前缀白名单 + 外来文件即失败退出，不用 shell `rm -rf`；
被拒绝时不要找绕过手段），模式本身已实现在 `publish_series.py` 的 `prep_target_dirs()`。

**验证方式**：RULES.md 现有该条；`publish_series.py` 中 `prep_target_dirs()` 的 `SystemExit` 分支仍在。

**处理结果**：归档。

---

## 未归档（继续观察）

| 记录 | 原因 |
|------|------|
| `LRN-20260912-012` vault 被本会话之外的写者改动 | 写者身份未确定，根因未消除；只能靠「先隔离再报告」的行为约束，**不能**归档 |

## 下轮维护提示

- ERRORS.md 归档后回到空态；若同一「发布脚本自造缺陷」主题再出现一次，
  说明 `note-beautifier` 的自检节没有被实际执行 —— 届时应转向检查**该节点是否可被跳过**
  （例如把断言提进脚本模板），而不是再补一条规则。
- `LRN-20260912-012` 若再次发生，应升级为需要在会话外解决的并发写入问题。
