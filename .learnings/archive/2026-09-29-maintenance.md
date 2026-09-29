# 2026-09-29 经验库维护（`/maintain-learnings`）

从 `digest`（自我学习）转入。判定依据：`.learnings/ERRORS.md`（234 行）与
`.learnings/LEARNINGS.md`（168 行）双双破 100 行压缩阈值，且**不是单纯堆积**——
是「同类错误复发 + `RULES.md` 已有规则仍失效」。按 `digest` Step 1 的分支规则，
停止单纯压缩，改修 skill / 模板 / hook / 项目规则，验证后再归档。

## 维护前审计

| 文件 | 维护前 | 本条维护后 |
| --- | --- | --- |
| `.learnings/ERRORS.md` | 234 行 / 5 条活跃 | 新增 3 条（`-013`/`-014`/`-015`），归档 5 条 |
| `.learnings/LEARNINGS.md` | 168 行 / 4 条活跃 | 新增 2 条（`-020`/`-021`），归档 3 条，挂起 1 条 |
| `.learnings/RULES.md` | 77 行铁律 | 4 处扩写 / 新增 1 条铁律 |

判定为「复发」的证据：

- `RULES.md:34`（`02_deep_research.md` 是中间产物、不是可信终点）本轮仍未拦住：
  3 个真缺陷中 2 个源于该中间件（逐字引文被改动；表格行数把表头与分隔行算进去）。
- `RULES.md:53`（跨章口径比对）只覆盖「可照抄的配置块」，不覆盖「对同一来源的散文式转述」，
  导致第 2 章 L44 的过强概括逃过验收，靠用户读已发布笔记才被发现。
- `ERRORS.md` 头部自述的 `-008`/`-009` 源头修复**尚未落地**，本次补齐。

## 归档块

### 1. `ERR-20260918-008` + `ERR-20260918-009` — 归一层选错 + 归一脚本非幂等

- **原记录摘要**：① 归一 / 清洗动作被放在下游产物层，发布件根本没被归一（`-008`）；
  ② `normalize_chapters.py` 两处缺陷：插入点取「第一条脚注定义」、规则非幂等（`-009`）。
- **根因聚类**：同一根因家族——**变换被放在错误的一层**，且**「发布件 == 源文件」被误当成正确性证明**。
- **修复路径**：`.agents/skills/note-beautifier/SKILL.md` §分册 / 长文档发布 新增四项自检：
  归一 / 清洗只能归属**一个层**且落在**最上游源文件**上（下游只做机械变换；要主动问
  「另一条下游有没有这份规则」）；幂等验收 = **连跑两遍 + `diff` 为空**；插入点用**尾部连续块
  / 最后一个匹配项**而不是「第一个匹配项」；零宽前瞻必须**前置判定**；
  「发布件 == 源文件」只证明变换可逆、**不证明产物正确**；发布后**逐行读一遍成品**。
- **验证方式**：该四项为发布阶段的人工 / 脚本自检门槛，写进 SKILL.md 的检查清单；
  核对每个待归档条目都能对应到新步骤（本项对应「分册 / 长文档发布」四条中的三条）。
- **处理结果**：已归档。全文见 `.learnings/archive/2026-09-29-archived.md`。

### 2. `ERR-20260918-010` — 记录数字取自历史输出

- **原记录摘要**：工作记录（阶段段落 + 最终产出）里的数字直接誊抄上下文里的旧输出，
  与当前产物不一致。
- **根因**：取数动作与记录动作之间隔着若干次改动，**没有绑定「当场重新取数」**。
- **修复路径**：`.codex/workflows/learning-note-flow/state-template.md` 的「最终产出」新增
  取数纪律 blockquote（体积 / 字数 / 章数 / 锚点数 / Callout 数必须**当场重新运行取数或重新计数**，
  不从历史输出誊抄、不手算合计；产物再被改动时 grep 同一数字的**所有**出现处一并更新），
  并新增 `- **取数命令**：` 字段要求把命令留在状态文件里。
- **验证方式**：模板字段存在性检查；本轮成品的复测即按该纪律重跑（锚点 111 / 表格行 70 /
  Callout 26）。
- **处理结果**：已归档。

### 3. `ERR-20260918-011` — 文本模式写盘转 CRLF，静默打穿阶段判定

- **原记录摘要**：某个工具用 `read_text` / `write_text` 重写 workflow state file，
  整篇变成 CRLF；`todo-state.sh` 的行尾锚定正则在 CRLF 下失配，
  报出误导性的 `previous phase is not complete or skipped: P0`。
- **根因**：守卫的**失败模式本身是静默的**——错误信息指向「前一阶段未完成」，
  而不是指向「文件行尾被改了」，排查方向被误导。
- **修复路径**：`.codex/scripts/todo-state.sh` 在解析前新增**行尾守卫**（见下「机制改动」第 5 项）；
  `RULES.md` 相应铁律补一句：出现该告警说明有工具在文本模式下重写了 state file，
  要去查那个工具，而不是手工把文件改回去。
- **验证方式**：**承重对照实验**（bearing test）——把守卫从一份其余完全相同的脚本里去掉，
  用 P0=`{complete}`、P1=`{in_progress}` 的 CRLF 状态文件跑 `complete P1`：
  - 无守卫 + CRLF → exit 1，复现 `previous phase is not complete or skipped: P0`；
  - 有守卫 + CRLF → exit 0，打印 WARNING，CRLF 计数 206 → 0；
  - 有守卫 + LF → exit 0，无告警（无回归）。
- **处理结果**：已归档。

### 4. `ERR-20260924-012` — workflow.md 记载了不存在的 `confirm` / `mode` 动作

- **原记录摘要**：`workflow.md` 的示例命令调用了 `todo-state.sh confirm` / `mode`，
  而脚本里没有这两个动作；同时存在「workflow 定义调用的动作无人校验其真实性」这一更深的缺口。
- **根因**：文档与脚本之间**没有可执行的绑定**；一个只查「脚本自己渲染的那部分」的守卫
  会给出**空绿**（green that carries no load）。
- **修复路径**：**已由 2026-09-23 另一台机器的修复落地**，本次为复核确认：
  `todo-state.sh` 补齐 `mode`（写 frontmatter）+ `confirm`（追加用户确认记录表）；
  `.claude/scripts/workflow-health-check.sh` 新增**探针式动作守卫**——
  逐个探测 workflow 定义里调用的每个 `todo-state.sh` 动作是否真实存在。
- **验证方式**：`workflow-health-check.sh` 输出 `todo-state action guard: 15 invocation(s) probed`，
  无失败项；`manifest-registry.py --root . validate` → 60 个工件，exit 0。
- **处理结果**：已归档（确认为「已在源头修复、只是活跃记录未清理」）。

### 5. `LRN-20260918-017` + `-018` + `-019` — 检索路径与注册表核对

- **原记录摘要**：① Discourse 论坛帖子正文只走 `/t/<id>.json`，HTML 路径会漏抓；
  ② 沙箱产物落仓库内路径并用仓库相对路径读回；③ 核对 Hermes Skills Hub 必须查中央索引。
- **根因聚类**：三者都是**把「一次检索失败」直接当成「来源不可得」**，
  从而错降证据等级或错做普遍否定。
- **修复路径**：`.agents/skills/research-collector/SKILL.md` 新增 `## Retrieval pitfalls` 小节
  （含 Discourse 的 `/t/<id>.json` 路径与静默返回 SPA 外壳的陷阱、产物落
  `${WORKSPACE_PATH}/${PROJECT_SLUG}/sources/…` 且不得用 `/tmp` 做跨调用暂存区、
  「命令存在」≠「命令可用」的可用性探测）；Source policy 新增
  「Verify federal / aggregated registries at their own index, not in a local directory」
  （含「先问检查范围是否等于句子的范围，并把范围写进句子里」）。
- **验证方式**：skill 元数据断言 + 三处条款与三条记录逐条对应；下轮运行由 P1/P2 自检触发。
- **处理结果**：已归档。

## 机制改动（本轮）

| # | 文件 | 改动 |
| --- | --- | --- |
| 1 | `.agents/skills/note-beautifier/SKILL.md` | 分册发布自检节 +4 条（归一层唯一 / 幂等验收 / 插入点 / 发布件==源件不证明正确） |
| 2 | `.codex/workflows/learning-note-flow/workflow.md` | 阶段 4 跨章比对扩到**三类**（配置块 / 同源散文式转述与定性 / 判据句对语义框架自洽）+ 结果写入异常记录 |
| 3 | `.agents/skills/research-collector/SKILL.md` | 新增「中间产物不是权威」段 + 联邦注册表核对 + `## Retrieval pitfalls`；P1 标证据形态、P2 加自检步骤与完成标准 |
| 4 | `.codex/workflows/learning-note-flow/state-template.md` | 最终产出加取数纪律与「取数命令」字段；P4 检查项与 workflow.md 对齐 |
| 5 | `.codex/scripts/todo-state.sh` | 解析前新增行尾守卫：检测到 CRLF 即告警并归一（含承重对照实验） |
| 6 | `.learnings/RULES.md` | 4 处扩写：中间产物（引文逐字 + 数值重数 + 行数只数数据行 + handoff 自述）/ 跨章三类比对 / P1 证据形态 / CRLF 告警的排查方向 |

同步流程（canonical → mirror）：`.agent-sync/sync_agents.py --check --scope <area>` → `--apply`
→ 全量 `--check` → `.claude/scripts/workflow-health-check.sh`；全量 check 结果
`[OK] shared agent configuration is synchronized`（exit 0）。

## 本轮新记（留在活跃文件）

- `ERR-20260929-013` 逐字引文在中间产物里被改动，沿引用链传进正文。
- `ERR-20260929-014` 对照表行数把表头与分隔行算进去（「17 轴」实为 15 行），扩散 12 处。
- `ERR-20260929-015` 判据句措辞与下游术语框架正面冲突，导致已发布章节读不通。
- `LRN-20260929-020` 跨章比对漏掉散文式转述与定义句（本次 `-015` / L44 的共同检测缺口）。
- `LRN-20260929-021` P1 候选须标 `snippet-only` / `fetched`，不得与已抓原文静默混放。

**挂起（未归档）**：`LRN-20260912-012` — vault 被本会话之外的写者改动，写者身份至今未定，
仍留在 `LEARNINGS.md`，不能归档。

以上 5 条新记的状态均为 `pending`（机制已落但尚未在下一轮运行中被验证），
验证通过后的下一次维护再归档。
