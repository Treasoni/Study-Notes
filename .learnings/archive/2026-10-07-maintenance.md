# 经验库维护报告（2026-10-07）

**第七次维护**（`/maintain-learnings`）。承接同日的 `/digest`（落盘 `LRN-20261007-031` + `ERR-20261007-023`）立即执行。

范围：审计 → 两处源头修复（退役根守卫接线、主线来源可靠性落地进 3 个 skill）→ 归档 2 条活跃记录。

---

## 一、审计结论（维护前）

| 文件 | 行数 | 活跃记录 |
| --- | ---: | --- |
| `.learnings/LEARNINGS.md` | 72 | 2（`LRN-20260912-012` anomaly 挂起；`LRN-20261007-031`） |
| `.learnings/ERRORS.md` | 42 | 1（`ERR-20261007-023`） |
| `.learnings/RULES.md` | 93 | — |

`audit_learnings.py` 热点簇（active / total）：`general` 3/32、`markdown` 1/36、`research` 1/23、`hook` 1/16、`interaction` 0/41 …

判定：**活跃文件均 <100 行，无重复主题堆积，不需要压缩**；本轮的工作是「修源头 + 归档已修记录」，不是清理。

审计方法论注意：`audit_learnings.py` 的输出里 `general` / `markdown` 这类簇的 active 计数会**把条目标题与正文小标题（`Details` / `Summary` / `Do`）也算成记录**。数「活跃记录条数」以文件头部声明与 `## [LRN-…]` / `## [ERR-…]` 标题为准，不要直接读簇计数。

---

## 二、真缺陷：退役根守卫「写好没接线」，残留靠 gitignore 藏了一个月

**发现**：本轮审计时 `.codex/skills` **在磁盘上仍然存在**——2 个 `__pycache__/*.pyc`（mtime **Jul 30 22:58**）+ 若干空目录。

**证据链**：

- `git ls-files .codex/skills` = **0**，`git status --short .codex/skills` = **空**。原因：`.gitignore:29` 忽略 `__pycache__/`、`*.pyc`——**这份残留对一切基于 git 的检查不可见**。
- 残留成因：2026-09-11 的删除走 `git rm -r`，清掉的是 **242 个受跟踪文件**；未被跟踪的 `__pycache__` 原地留下，`git rm` 之后它所在的目录也不为空、不会被回收。**不是**插件重新建树（pyc 的 mtime 早于删除日，说明是删除前的旧物）。
- 守卫 `.agent-sync/migrate_legacy_skills.py` 本身**能红**：本轮实测 exit 1 并打印正确指引。但 `grep -rn migrate_legacy_skills` 全仓（除 `.learnings/`）**零命中**——它**没有任何调用点**。

**根因**：这是 `RULES.md`「守卫写完要问三件事：谁调用它、它在本仓库能不能变绿、绿是不是空绿」的**复发**。2026-09-11 的维护报告已经写下「该脚本无自动化调用点（仅自引用 + 本档）…守卫变红不会影响 health check 或 CI」——**只记录、没接线**，于是这条守卫白站了一个月，残留也就藏了一个月。两条独立缺陷叠加才让问题不可见：**守卫没有调用点** + **残留被 gitignore**（只有读文件系统的守卫能看见它，而那个守卫没人跑）。

**修复**：

1. canonical `.codex/scripts/workflow-health-check.sh` 在 portability 守卫之后接入墓碑守卫（固定 `.agent-sync` 路径，与 `validate_portability.py` 同一模式，避免同步把它改写成两份分叉的副本）：

   ```bash
   # Tombstone guard for the retired `.codex/skills` root. It had no caller until now,
   # and the 2026-09-11 removal left untracked, gitignored `__pycache__` residue that no
   # git-based check can see; only a filesystem reader catches the path coming back.
   if ! python3 .agent-sync/migrate_legacy_skills.py; then
     fail "The retired .codex/skills root exists again; see the guard's message."
   fi
   ```

2. 删除残留：先核对「2 个文件、全部是 `*/__pycache__/*.pyc`、受跟踪 0 条」，再 `find … -name "*.pyc" -path "*/__pycache__/*" -delete` + `find … -type d -empty -delete`（**不用 `rm -rf`**，与 `RULES` 的前缀白名单原则一致）。
3. 同步：`sync_agents.py --scope scripts` 报 `[DRIFT] updated: .claude/scripts/workflow-health-check.sh` → `--apply` → 全量 `--check` = synchronized。

**双向验证**：

| 场景 | 结果 |
| --- | --- |
| 清理后直接跑守卫 | exit **0**，`nothing to do; migration complete, canonical root is .agents/skills` |
| 注入 `mkdir -p .codex/skills/fake-skill` | exit **1**（能红） |
| 撤除注入目录 | exit **0** |
| 伞形健康检查 | 新增行 `migrate-legacy-skills: nothing to do…`，不再只靠人工记得跑 |

---

## 三、源头修复二：`LRN-20261007-031` 的机制落地（3 个入口 skill）

**学习内容**：写工具 / 部署类笔记前先核「主线来源是否仍在维护」——本次 8 篇「小雅 fnOS 单容器部署」因主线取自已停维护的 `monlor` 社区镜像（最后提交 2025-03-27）而**整套重写**；且须分清**官方**（镜像 `xiaoyaliu/alist`）与**社区整合脚本**（`xiaoyaDev/xiaoya-alist`，DDSRem）——两者是不同项目，不是版本差异。

**落地（canonical `.agents/skills/`，判据可执行）**：

| Skill | 版本 | 落点 |
| --- | --- | --- |
| `research-collector` | 2.4.0 → **2.5.0** | `## Source policy` 新增「A repository's upkeep is part of its source tier」段；P1 候选字段加 `pushed_at` / `archived` |
| `note-updater` | 1.6.0 → **1.7.0** | `## 口径核对（先于改写）` 新增「先核上游项目还在不在维护，再定改法」条（停维护 → 换源重写，而非局部更新） |
| `batch-note-updater` | 1.0.0 → **1.1.0** | `Step 2 生成批量更新计划` 新增「上游维护状态核对（定动作的依据）」条：停维护的上游**不能只写 `update`**，标为换源重写并单列 |

判据（三处一致）：`curl -s https://api.github.com/repos/{owner}/{repo}` → `pushed_at` 距今 **>12 个月**或 `archived: true` → **不作主线**；笔记里要写清官方还是社区整合脚本。

**为什么放三个入口而不是写进项目总规则**：新笔记走 `research-collector`、单篇旧笔记走 `note-updater`、多篇旧笔记走 `batch-note-updater`——三条路径各自读自己的 SKILL.md，任一入口缺失都会让该路径静默漏掉；而它对非笔记类任务是无关细节，**不**提升为 `CLAUDE.md` 级铁律。

---

## 四、归档记录（2 条）

### [ERR-20261007-023] → 已归档（机制 = 共享校验器两处修正 + 自测用例 G）

- **摘要**：`note-citation-check.py` 报 S4「出处列非法」72 处 + 「管道数 != 5」4 处，**全为校验器误报**——`CITE_FULL` 不认 `.sh`（本主题逐字引文出自 `sources/xiaoyaDev/all_in_one.sh`）；S4 按**原始** `|` 计数，把正确转义的 `\|` 当分隔符。
- **修复路径**：`CITE_FULL` 扩展 `(?:md|txt|html|json|sh)`；S4 只计未转义竖线 `(?<!\\)\|` 并按其切列。改 canonical `.codex/scripts/` → `sync_agents.py --scope scripts --apply` → 全量 `--check` synchronized。
- **验证方式（本轮复核）**：`python3 .codex/scripts/note-citation-check-selftest.py` → **A–G 七例全 PASS**（含新增的 G：引文含转义竖线 → exit 0），清理自证 `workspace/_citecheck_selftest 已删除 = True`。门禁仍能红（B/C/D/E 均 exit 1）。
- **处理结果**：从 `ERRORS.md` 移出；机制（两条判据 + 用例 G）留在共享校验器里。

### [LRN-20261007-031] → 已归档（机制 = 3 个 skill + manifest 版本 + RULES 铁律）

- **摘要**：主线来源维护状态核验；来源选错 = 整套笔记返工。
- **修复路径**：见第三节。
- **验证方式（`maintain-learnings` Step 5）**：
  - `python3 .codex/platform/manifest-registry.py --root . validate` → `Manifest registry validation passed (60 artifacts)`。
  - 3 个 SKILL.md 元数据断言（`---` 起首、含 `name:` / `description:`）→ `skill metadata ok` ×3。
  - `sync_agents.py --check --scope skills` 报 6 处 drift（3×SKILL.md + 3×manifest.yaml，与本次编辑**一一对应**，无额外漂移）→ `--apply` → 全量 `--check` = synchronized；镜像侧 grep 三个新段落各 1 命中。
- **处理结果**：从 `LEARNINGS.md` 移出；铁律留在 `RULES.md`（Do 区）。

---

## 五、未归档（继续留在活跃文件）

- **`LRN-20260912-012`**（anomaly，priority high）：vault 被本会话之外的写者改动，**写者身份未确定、根因未消除** → 不可归档。本轮无新证据，原样保留。

归档后活跃计数：`LEARNINGS.md` **1** 条（`LRN-20260912-012`）、`ERRORS.md` **0** 条。

---

## 六、验证（`maintain-learnings` Step 5 汇总）

| 项 | 命令 | 结果 |
| --- | --- | --- |
| 校验器自测 | `note-citation-check-selftest.py` | ✅ 七例全 PASS |
| 校验器实跑 | `note-citation-check.py workspace/xiaoya-fnos-deploy` | ✅ 无硬失败（P5 已跑，未因本轮改动受影响） |
| manifest 注册 | `manifest-registry.py --root . validate` | ✅ 60 artifacts |
| skill 元数据 | 3 个 SKILL.md 断言 | ✅ ok ×3 |
| 配置同步 | `sync_agents.py --check` | ✅ synchronized |
| 守卫双向 | 注入 / 撤除 `.codex/skills` | ✅ exit 1 / 0 各如预期 |
| 伞形健康检查 | `PYTHON=$HOME/.local/bin/python3.12 workflow-health-check.sh` | ✅ 除 prompt-cache 旋钮漂移（见下节，设计如此）外全绿；新增墓碑守卫行 |

---

## 七、下轮维护提示

1. **prompt-cache 旋钮漂移会一直报 FAIL，这是设计如此，别去改守卫**：`.llm/prompt-cache/cache-guard.py` 中 `if knob_problems: actionable = True` **与数据量无关**（注释说的「≥10 contexts 前保持安静」只作用于回归判定）。现状：会话 `effortLevel`/`thinkingBudget` = `high`/`max` ≠ 基线冻结的 `medium`（本轮两次观测即从 `high` 变到 `max`，是**活的会话配置**，不是仓库产物；`git status` 中 `.llm/` 干净）。处置三选一，**先问用户**：恢复旋钮 / 按当前旋钮重冻基线 / 明确接受该 FAIL。
2. **本机 `python3` 是 macOS 自带 3.9.6**，`sync-workflow-routing.sh` 要求 3.10+，直接跑健康检查会**假报**「routing 表过期」。跑之前先 `export PYTHON=$HOME/.local/bin/python3.12`（已入 `RULES.md`）。
3. `RULES.md` 本轮在「守卫三问」条上补了复发证据（见第八节），下轮若再发现「脚本/守卫没有调用点」，按同一条**当场接线**，不要只记进本档。
4. `.codex/skills` 的**消费者仍在**：Claudian 插件新建 skill 的弹窗默认根是该退役路径（`main.js` 的 `targetRootId ?? "vault-codex"`），且无持久化默认根设置。若再次出现，先判断是不是插件 UI 建出来的孤儿 skill，而不是急着删。

---

## 八、本轮对 `RULES.md` 的改动

- 「守卫写完要问三件事」条追加复发证据：
  > （2026-10-07 复发：退役根墓碑守卫写好**一个月没接线**，残留因 gitignore 藏了一个月——**发现「没有调用点」必须当场接线**，不能只记进档案。）

- Do 区新增「动笔前先核主线来源还在不在维护」条；Don't 区新增「命令/程序输出用带语言标注的代码块、不要写成行内反引号引文」条（两条均由本轮 `/digest` 写入，此处一并登记）。
