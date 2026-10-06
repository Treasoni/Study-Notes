# 经验库维护报告（2026-09-30）

**触发**：`/maintain-learnings`（用户显式调用）。审计条件同时命中两项——
`.learnings/LEARNINGS.md`（124 行）与 `.learnings/ERRORS.md`（123 行）均超 100 行阈值，
且「引文纪律」family 已在 `RULES.md` 有规则、仍在 `ERRORS.md` 复发
（`ERR-20260929-013` 就是「规则已有、执行仍靠人肉」的形态）。

**结论**：这一族的问题不是「记性不好」，是**没有可执行的门**。所以本轮没有继续加「下次注意」，
而是把整族判据收进**一个共享校验器**，让它在生成链的每个交接点自动跑。

---

## 一、本轮唯一的机制改动：共享引文校验器

新增（canonical，`.codex/` 下）：

| 文件 | 作用 |
| --- | --- |
| `.codex/scripts/note-citation-check.py` | 三族一次扫完：**V 逐字回源** / **S 引文体例** / **C 多副本一致** |
| `.codex/scripts/note-citation-check-selftest.py` | **可移植负向自测**：自建 fixture，六个用例证明「门禁能红」 |

设计要点（本轮踩出来、写进 docstring 的）：

- **三态判定**：`V` 的引文回源分 `ok` / `weak` / `miss`。`miss` 与
  （除非显式 `--allow-weak`）`weak` 都是硬失败。`weak` 的含义是
  「**只在本项目中间产物里命中**」——即 `ERR-20260929-013` 那一类：
  引文在 `02_deep_research.md` 里对得上、在原始语料里对不上。
- **两套语料**：`primary`（`research/`、`sources/`、`docs/`、`web/`、`--corpus`）与
  `derived`（项目自己的 `0N_*.md` 中间产物）。判定只看 primary，derived 只用于解释 `weak`。
- **weak 自解释**：命中不了时打印「最长可回源 N/M」+「语料最接近处」，
  把「回原料核」从无界搜寻变成一眼判断：提取件标记差异 / 跨项目来源 / 自己的概括被当成引文。
- **反静默通过**：`C` 返回 `compared`（实际比对组数），`compared == 0` 是硬失败——
  「一份副本都没认出来」等于**根本没比**，不能算绿灯。
- **模式**：`all`（V+S+C）/ `text`（V+S，组装前单章）/ `verbatim` / `style` / `copies`。
  组装前单章只有一份副本，跑 `all` 会因 `compared == 0` 自我误判，故用 `text`。
- **两个逃生口**：`--file`（额外 V 文件，用途是核对 `02_deep_research.md` 这类自己的中间产物）
  与 `--corpus`（额外语料，用途是写 `research/04_..._honcho.md` 这种跨项目来源时把对方树加进来）。

### 为什么是「一个共享脚本」而不是「每个项目一个」

历史形态是：每轮在项目工作区里现写 `_lcs.py` / `_bare.py` / `_dup2.py` 之类的临时校验脚本。
它们随项目一起废弃，判据不累积——所以**同一族缺陷每轮都能重犯**。共享脚本把判据变成资产：
缺哪条判据就补进这一个文件，下一轮自动继承。

### 门禁必须能红

`.codex/scripts/note-citation-check-selftest.py` 自建 fixture（不依赖真实项目），六个用例：

| 用例 | 注入的缺陷 | 期望 |
| --- | --- | --- |
| A | 无缺陷基线 | exit 0 |
| B | 合并件被改一个字母（只 C 能抓） | exit 1 |
| C | 三份副本同改一处（只 V 能抓，C 会一致） | exit 1 |
| D | 「出处」列写了产品文件名（`SOUL.md`） | exit 1 |
| E | 引文只在 derived 里命中（weak） | exit 1 |
| F | 同 E + `--allow-weak` | exit 0 |

用例 C 是关键：它证明 `V` 那一层**单独承重**——三份同改时 C 族看不到任何差异，
只有逐字回源能发现。用例 D/E 分别锁住 `S4` 的出处取值域与 `weak → 硬失败`。

---

## 二、验证（Step 5）

技能元数据断言：

```
skill metadata ok: note-beautifier
skill metadata ok: research-collector
```

负向自测：

```
A 基线（无缺陷）                 exit=0（期望 0）  PASS
B 合并件被改一个字母              exit=1（期望 1）  PASS
C 三份同改（只靠 V 红）           exit=1（期望 1）  PASS
D 出处列写了产品文件名            exit=1（期望 1）  PASS
E 只在中间产物命中（weak）         exit=1（期望 1）  PASS
F 同 E + --allow-weak           exit=0（期望 0）  PASS
总判定：✅ 六个用例全部符合预期（门禁能红）
```

两个真实项目（**非空跑**——副本组数与引文数都核实过）：

| 项目 | V 逐字回源 | S4 | C 多副本 | 退出码 |
| --- | --- | --- | --- | --- |
| `ai-agent-platform-selection` | 380 处：380 命中 / 0 仅中间产物 / 0 未命中 | 0 不合格 | 10 份副本，比对 **21** 组，0 差异 | 0 |
| `ai-agent-platform-selection`（不带 `--vault-note`） | 同上 | 0 | 9 份副本，比对 **14** 组，0 差异 | 0 |
| `music-tag-web` | 2 处：2 命中 / 0 / 0 | 0 不合格 | 9 份副本，比对 **8** 组，0 差异 | 0 |

两处数字差异是**预期的**：不带 `--vault-note` 时链上少一份副本（vault 成品），
比对数自然从 21 降到 14。这本身就是 `C` 按副本对计数的证据。

### weak 判定的准确率（本轮实测）

`--file 02_deep_research.md` 一开始报 8 处 weak。逐条查证：

- 2 处是**引用式标题**（`#### 1. Secondary profiles…`、`# Paths that bypass JWT…`）——
  笔记侧保留了引文里的 `#` 标记，语料侧把标题标记剥掉了。**校验器假报** → 改 `check_verbatim`
  的笔记侧归一（用 `corpus_norm`）后消失。
- 1 处是**LaTeX 泄漏**：语料里 `\mathcal{L}` 与真符号 `ℒ` 一起被打出来
  （`…settings,LLadditionally…` vs 笔记 `…settings,Ladditionally…`）。**校验器假报** →
  新增 `_latex_cmd`（符号与它的 LaTeX 同时出现时整条命令丢弃）+ `norm` 加 NFKC 后消失。
- 剩余 5 处**全部是真判定**：4 处引文来自**另一个项目**的抓取件
  （`workspace/hermes-agent/research/04_hermes-agent_nousresearch_com.md`），
  1 处是笔记里**自己声明过无法核验**的引文（`⚠️ 中间件本体 … 未抓落盘`）。
  用 `--corpus workspace/hermes-agent/research` 复跑，weak 5 → 1，与声明一致。

教训已写进脚本 docstring 与 `RULES.md`：**校验器报出批量告警，先怀疑校验器自己**
（3 个假报全部是归一化不足，不是引文有问题）。

---

## 三、机制落点（本轮改了哪些工件）

| # | 文件 | 改动 |
| --- | --- | --- |
| 1 | `.codex/scripts/note-citation-check.py` | 新建（三族校验器；`--mode` / `--file` / `--corpus` / `--vault-note`） |
| 2 | `.codex/scripts/note-citation-check-selftest.py` | 新建（可移植负向自测，六用例） |
| 3 | `.agents/skills/note-beautifier/SKILL.md` | Step 4 新增「引文纪律（跑统一校验器，不现写）」5 条 |
| 4 | `.agents/skills/note-beautifier/manifest.yaml` | 1.3.0 → 1.4.0；`subprocess: none` → `allow` |
| 5 | `.codex/agents/chapter-writer.md` | Quality Checklist 新增「交章前跑 `--mode text`」 |
| 6 | `.codex/agents/chapter-writer/manifest.yaml` | 1.3.0 → 1.4.0 |
| 7 | `.agents/skills/research-collector/SKILL.md` | P2 第 3 步（自检产物）与第 4 步（跨项目来源可达）改为**调用共享校验器**；完成标准加断言 |
| 8 | `.agents/skills/research-collector/manifest.yaml` | 2.3.0 → 2.4.0 |
| 9 | `.codex/workflows/learning-note-flow/workflow.md` | 阶段 4 交章前 `--mode text`；阶段 5 组装后 `--mode all`（含 `实际比对 N 组 > 0`）；阶段 6 发布前带 `--vault-note` |
| 10 | `.codex/workflows/learning-note-flow/manifest.yaml` | 1.3.0 → 1.4.0 |
| 11 | `.learnings/RULES.md` | 新增 `Do` 一条「引文只用共享校验器，不要为单个项目再写一个」（含「门禁必须能红」与「N > 0」两条反静默通过）；`Watch For` 两条：可移植性校验器的正则字面量假阳性、生成物（`__pycache__`）不参与同步 |
| 12 | `.agent-sync/sync_agents.py` | 同步时忽略 `__pycache__/` 与 `*.pyc`/`*.pyo`（见下方「验收时顺手发现的两个真问题」） |
| 13 | `.codex/scripts/note-citation-check.py` | 分隔行的正则字符类改写（消除 `validate_portability.py` 的假阳性，见同节） |

同步流程（canonical → mirror）：`.agent-sync/sync_agents.py --check --scope <area>` → `--apply`
→ 全量 `--check` → `.claude/scripts/workflow-health-check.sh`。

### 验收时顺手发现的两个真问题

跑同步与健康检查时，机制自身暴露出两个缺陷。两条都不是「本次改动的副作用」，而是**一直存在、
只是这轮第一次被跑到**：

1. **同步器会把字节码缓存当源文件镜像。** `python` 在 canonical 脚本目录里留下
   `__pycache__/note-citation-check.cpython-314.pyc` 后，`--check --scope scripts` 报
   `[DRIFT] created: .claude\scripts\…pyc`：`--apply` 会把这个构建产物复制进镜像，
   而下次 check 又追不平。已在 `source_files()` 加 `IGNORED_PARTS = {"__pycache__"}` 与
   `IGNORED_SUFFIXES = {".pyc", ".pyo"}`，并把这个说明写成注释放在常量旁边
   （**生成物不参与同步**）。修完复跑：scripts 作用域只剩两个真实新增文件，`--check` 退出码由 1 转 0。
2. **可移植性校验器有一个假阳性类：源码里的正则字面量。**
   `validate_portability.py` 的 `ABSOLUTE_PATH = /Users/|/home/|[A-Za-z]:[\\/]` 会把
   **一行合法正则**里的「单个字母 + 冒号 + 反斜杠」读成盘符路径
   （本例是分隔行判定的字符类，`: ` 紧挨 `\` 的那一段），于是整个共享资产被判「不可移植」。
   已改的是**被检文件**（字符类换个等价写法，语义完全相同）而**不是校验器**——
   放宽 `ABSOLUTE_PATH` 会削弱一条有真实战功的守卫（它抓到过提交进 Windows 检出的 macOS
   解释器路径）。代价是这类字面量在源码与注释里都不能写，已写进代码注释。
   **这类假阳性会复发**，见「下轮维护提示」。

---

## 四、本轮归档（2 条）

### `ERR-20260929-013` — 中间产物里的逐字引文被改动，沿引用链传进正文

- **原文**：见 `2026-09-30-archived.md`。
- **根因**：这类错误能骗过所有「有没有挂来源 ID」的检查，只有逐字比对才抓得到；
  此前只有「落盘前逐字比对」这条**要靠人执行的**规则。
- **修复路径**：`research-collector` P2 自检改为调用
  `note-citation-check.py … --mode verbatim --file 02_deep_research.md`。
- **验证方式**：① 自测用例 E/F 证明「只在中间产物命中」是硬失败、`--allow-weak` 才放行；
  ② 该 gate 在真实项目上跑过并**报出过真缺陷**（见上面 weak 判定一节：连归一化修完后，
  仍准确报出 4 处跨项目来源 + 1 处自声明不可核验），不是空绿。
- **处理结果**：已归档。

### `LRN-20260930-022` — 「引文中译 + 逐字留档」的规则要落在生成侧

- **原文**：见 `2026-09-30-archived.md`（状态行保留原 `pending`，变更记在该文件的维护批注里）。
- **根因**：把「验收条目」当「生成约束」用——只证明这次改对了，下次照样返工。
- **修复路径**：生成侧三处落地（`chapter-writer.md` 写作要求 + Quality Checklist、
  `workflow.md` 阶段 4/5 检查项、`rules/obsidian/note-system.md` 默认要求），
  美化侧只留验收条目。
- **验证方式**：该偏好的四条判据**全部已机器化**——
  ① 留档表存在与结构 → `S4`（表结构 + 出处取值域）；
  ② 出处宁空不猜 → `S4` + 自测用例 D；
  ③ 引导语 / 括注与中译撞车 → `S2`（LCS ≥ 5）与 `S1`（短引文边界叠字）；
  ④ 「该译没译」→ `S3`（反引号外 ≥2 个 ASCII 词串）。
  生成侧落地本身按文件 grep 核对。
- **处理结果**：已归档。

### 留在活跃文件（未归档）

| 记录 | 为什么不能归档 |
| --- | --- |
| `LRN-20260912-012` | vault 被本会话之外的写者改动，**写者身份至今未定**，根因未消除（挂起中） |
| `ERR-20260929-014` | 「数值 / 计数」纪律：**校验器明确不覆盖数字**（docstring 与 `research-collector` 都已写明「中文引文与所有数值仍是人工逐字比对」）。机制仍是 prose，未机器化 |
| `ERR-20260929-015` | 「判据句与下游术语框架冲突」：落在 `workflow.md` 阶段 4 第 ③ 类**人工对读**清单，无脚本判据 |
| `LRN-20260929-020` | 同 `-015` 的机制（跨章比对三类），同为人工清单 |
| `LRN-20260929-021` | P1 候选标 `snippet-only` / `fetched`：`SKILL.md` 的字段与完成标准是 prose，无校验器 |

> `-014` / `-015` / `-020` / `-021` 留在活跃文件不是遗漏，是**纪律**：
> 「不要归档未修复的问题」。它们的下一步是各自找到可执行的判据
> （数字：按行号回原文重数；跨章一致性：至少把「同一来源在多章被引用」列成表强制走查）。

---

## 四·五、收口结果与遗留

**同步 / 注册 / 路由 / 可移植性**（本轮全绿）：

| 检查 | 结果 |
| --- | --- |
| `sync_agents.py --check --scope {skills,agents,workflows,scripts}` | 差异符合预期 → `--apply` 四个作用域全部 `[OK]` |
| `sync_agents.py --check`（全量） | `[OK] shared agent configuration is synchronized`，exit 0 |
| `.codex/platform/manifest-registry.py --root . validate` | `passed (60 artifacts)` |
| `.claude/scripts/sync-workflow-routing.sh --check` | `up to date` |
| `.agent-sync/validate_portability.py --root .` | `[OK] shared agent sources are portable` |
| todo-state 动作守卫（health check 内） | `15 invocation(s) probed` 全部存在 |

**`workflow-health-check.sh` 仍 exit 1，唯一失败项是 prompt-cache guard**，与本轮改动无关：

```
KNOB DRIFT: effortLevel='high' expected 'medium'
KNOB DRIFT: thinkingBudget='xhigh' expected 'medium'
KNOB DRIFT: savedProviderEffort.claude='high' expected 'medium'
subagent … 1.461x REGRESS
```

- 该守卫的两个输入都是**运行时而外的文件**：冻结基线
  `.llm/prompt-cache/baseline-2026-09-14.json`（2026-09-14 冻结，未改动）与
  `.claudian/claudian-settings.json`（mtime **2026-09-30 00:41**，早于本轮文件编辑；
  `.claudian/` 未进 git 索引）。本轮改的是 skill / agent / workflow / 脚本，不在其输入里。
- 也就是说：**是本地运行时的 effort 旋钮被调高了**（medium → high / xhigh），
  守卫按设计如实报警；`subagent 1.461x` 是同一批事件的落后指标。
- **没有自动重冻基线。** 重冻等于把这次旋钮漂移洗成「新常态」，守卫从此失效；
  正确处置是用户二选一：① 认可高 effort 就**有意**重冻（`cache-guard.py --freeze`）并说明；
  ② 想回到基线就把旋钮调回 `medium`。见「下轮维护提示」第 5 条。

**工作区卫生（已做）**：删掉本轮产生的 9 个临时产物
（`workspace/_paths.txt`、`_weak_diag.txt`、`_c1/_c2/_file/_st/_text.log`、
项目下 `_one_diag.py`、`_weak_diag.py`）。其中 4 个已被自动化 `vault backup` 提交
（`a5fd84ef vault backup: 2026-09-30 01:03:40`）扫进版本库，因此它们的删除会以
「删除已跟踪文件」的形式出现在 `git status` 里。

两个**刻意保留**的：

- `workspace/ai-agent-platform-selection/_verify_assembly.py`：被 workflow state file
  第 110 / 129 行引为**组装保真度的实测工具**，删掉会让已记录的证据不可复现。它是
  `_verify/*` 这一族「项目内一次性校验器」的又一个例子，属下一轮考虑收编的对象。
- `workspace/ai-agent-platform-selection/_quote_rework/`（13 个 `.py`，含 `_lcs.py` /
  `_bare.py` / `_dup2.py`）：**这正是本轮 RULES 新条目的物证**——历史上每轮都现写一个
  校验脚本丢在项目工作区。本轮起不再新增同类脚本；这批历史脚本是否清理由用户决定。

## 五、下轮维护提示

1. **优先级最高的候选**：把「数值 / 计数」也机器化一部分——至少能自动列出
   「`0N_*.md` 里所有出现的数字 + 其上下文」，逼着每次落盘都回原文重数。
   这是 `-014` 至今无法归档的唯一原因。
2. 跨章一致性（`-015` / `-020`）能否部分脚本化：现有 `C` 族只比**同一章的副本**，
   不比**跨章对同一来源的转述**。可考虑：把被 ≥2 章引用过的来源 ID 列出来，
   强制父流程逐条走查（先做提示，不急着判定）。
3. 校验器新增判据时，**必须同时补一个负向用例**进 selftest——
   「一个从没红过的门禁不是门禁」。
4. 若引文形态再变（例如引入非英文来源），先看 `--corpus` / `--file` 两个逃生口够不够，
   再考虑改判定本身。
5. **prompt-cache guard 的旋钮漂移需要一个决定**（见「收口结果与遗留」）：要么有意重冻基线
   并记录原因，要么把旋钮调回 `medium`。在决定之前，`workflow-health-check.sh` 会一直 exit 1——
   注意这会让**其它检查的失败被这条噪音淹没**，属于该优先处理的项。
6. **可移植性校验器的假阳性类**（源码里的正则字面量）值得治本：现在的规避方式
   （源码和注释里都不写那段字面量）靠人记。若再撞一次，考虑给 `ABSOLUTE_PATH` 加一个
   「命中处在正则字面量/字符类内则跳过」的判定，**但要先写一个能红的用例**证明放宽后
   仍能抓到真盘符路径，再改。
7. `workspace/` 下的 `_*` 临时产物会被自动化 `vault backup` 一并提交。本轮不新增忽略规则
   （`workspace/*/_*.py` 会误伤 `research/**/__init__.py` 与各项目 `_verify/`、`_split_*.py`
   这类**有意保留**的工作脚本）；更好的做法是**不产生**临时产物——判据进共享校验器，
   一次性文件用完即删。
