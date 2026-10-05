# 经验库维护报告（2026-10-06）

**触发**：`/maintain-learnings`（用户显式调用，承接同日 `/digest`）。审计命中——
`.learnings/LEARNINGS.md`（126 行）与 `.learnings/ERRORS.md`（174 行）均超 100 行阈值；
`note-beautifier` 在审计里是 hotspot（Active 1 / Total 12 / Rules 0）；且
「校验绿灯 ≠ 产物正确」在 `RULES.md` 已有规则却**仍复发**（`ERR-20261006-016`）。

**结论**：这一族的问题不是「记性不好」，而是**内容门与结构门是两套正交的检查，后者一直缺失**。
本轮没有再写「下次注意」，而是把结构判据做成**一个可执行脚本 + 一条格式规则 + 一个 Step 4 清单项**，
让「内容校验全绿的成品仍可能渲染散架」这一类缺陷第一次有了门。

---

## 一、本轮机制改动：Obsidian 结构自检

新增 / 修改（canonical 在 `.codex/`、`.agents/skills/`）：

| 文件 | 改动 | 作用 |
| --- | --- | --- |
| `.codex/scripts/check-md-structure.py` | 新增 | 查三类「合法 Markdown 却渲染异常」：① 表格行前缺空行 ② callout 内表格未用 `>` 续接 ③ 缩进表格（疑似嵌进列表） |
| `.codex/rules/obsidian/note-system.md` | 加第 6 条 | **生成阶段**就写对：callout 内每个空行（含表格前后）必须写 `>` |
| `.agents/skills/note-beautifier/SKILL.md` | Step 4 + Callout 规范 | 发布前跑结构自检，退出码非 0 即**停止发布** |
| `.agents/skills/note-beautifier/manifest.yaml` | 1.4.0 → 1.5.0 | 版本 + description 登记新依赖 |

**同步与校验**：`sync_agents.py --apply --scope scripts|rules|skills` → 全量 `--check` 通过；
`manifest-registry.py --root . validate` → 60 artifacts 通过；`workflow-health-check.sh`
的结构守卫全过（todo-state action 15 / routing up-to-date / manifest 60 / portability OK），
仅 prompt-cache knob drift（`effortLevel`/`thinkingBudget`，运行时模型档位，与本轮改动无关）
按既往归入 workflow state file 的异常记录。

### 门禁能红（双向夹具）

`check-md-structure.py` 在植入三类缺陷的夹具上报 **4 处**（类 1 ×1、类 2 ×2、类 3 ×1，EXIT=1），
在已发布的 8 个 vault 成品与 workspace 的 9 个 `output/` 文件上均为 **0**（EXIT=0）。
设计取舍：只查**已确认**的渲染形态，不做通用 Markdown lint——窄判据误报少，
避免把门变成人人忽略的噪音（`RULES.md` 反复出现的教训）。

---

## 二、归档记录

### [ERR-20261006-016] → 已归档（机制 = 结构自检脚本 + 格式规则 + Step 4 清单）

- **原记录摘要**：已发布第 3 章 callout 续行缺 `>`——引导句与表格之间的空行没带 `>`，
  Obsidian 在此终止 callout、表格掉出框外；内容校验（V/S/C + 8 副本逐字一致）全绿，
  用户读**已发布**笔记才报「渲染有问题」。
- **修复路径**：最上游 `chapters/03_动手前准备.md` 改 1 个 ASCII 字符 → 下游机械重生成 →
  重新发布 → 复验 8/8 逐字一致。
- **机制化**：新增 `check-md-structure.py`（本文档第一节），写进 `note-system.md` 第 6 条与
  `note-beautifier` Step 4 / Callout 规范。
- **验证**：双向夹具（植入三类缺陷能红、正常成品为 0）+ 全量同步 `--check` 通过。
- **结果**：**归档**。

### [LRN-20261006-022] → 已归档（机制 = note-beautifier Step 4「Obsidian 结构自检」）

- **原记录摘要**：内容校验全绿 ≠ 可渲染；内容门与结构门是**两套正交的检查**，缺一边就会漏。
  与 `ERR-20260929-015`「引文对 ≠ 论述通」同族。
- **修复路径**：`note-beautifier` Step 4 新增「Obsidian 结构自检（渲染 well-formedness）」小节，
  固化 `check-md-structure.py`；并在 `note-system.md` 把规则提到生成阶段。
- **验证**：同上（同一机制、同一夹具）。
- **结果**：**归档**。

### [ERR-20261006-017] → 已归档（机制 = 共享校验器 FOOTER 判据）

- **原记录摘要**：分册导航尾行 `> 📖` 被 `note-citation-check.py` 当正文，`--vault-note` 逐章
  误报 1 处差异（**校验器假阳性**，产物本身正确）。
- **修复路径**：canonical `FOOTER = re.compile(r"^(?:## (参考文档|相关文档|参考资料)|>\s*📖)")`，
  `.agent-sync --apply --scope scripts` + 全量 `--check` 通过。
- **机制化**：判据已收进共享校验器——即 `RULES.md`「Do」第 38 条「判据缺哪条就补进这个脚本」的实例。
- **验证**：复跑 7 章 `--vault-note` 全 EXIT=0（C 0 差异，compared 8 组）。
- **结果**：**归档**。

---

## 三、未归档（继续留在活跃文件）

- `LRN-20260912-012`（anomaly，`high`，挂起）：vault 被本会话之外的写者改动，写者身份未定、
  根因未消除，**不可归档**。
- `LRN-20260929-020` / `-021`、`ERR-20260929-014` / `-015`：机制已落地，**尚未在下一轮运行中验证**，
  继续留待下轮复核后归档。
