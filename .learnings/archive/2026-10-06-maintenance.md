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

---

## 四、第二次维护（同日，承接本轮 `/digest` 的就地修复）

**触发**：同日 `/digest`（用户三点反馈）→ 用户紧接 `/maintain-learnings`。审计命中 `note-updater`
簇——正是本轮「小雅夸克口径」出错的两个缺陷族。上一节（第一/二/三次维护）已把结构类缺陷封口；
本节处理的是**交互与读取纪律**类缺陷。

| 记录 | 缺陷 | 落到的机制 |
| --- | --- | --- |
| `LRN-20261006-023` | 改「拆分笔记集合」时逐文件增量读，漏读成员、留下未处理项 | `note-updater` SKILL.md Step 1「**先判形态，再读最小上下文**」：先列齐集合成员 → 通读总览与各章标题/小结 → 定「受影响文件集」→ 再改写；结束时对未改成员说明「为何没动」 |
| `LRN-20261006-024` | 回答澄清问题从既有笔记 / 自己上一轮结论外推，答成邻接问题 | `note-updater` SKILL.md 顶部「**口径核对（先于改写）**」：回一手来源 + 用户实际处境；作用范围写进句子 |
| `ERR-20261006-018` | 绝对否定抹掉作用范围（「小雅不能转夸克」只对**本体库**成立） | 同上「口径核对」+「无来源的数字/比例不写」；并把「作用范围」升为 `RULES.md` 铁律 |

**为什么这三条能归档**（`maintain-learnings` Step 5 的验证）：

1. **skill 元数据校验通过**：`note-updater` SKILL.md frontmatter 的 `name:` / `description:` / 定界符齐全。
2. **每条记录都能对应到新的步骤或规则**（上表右列）——不是「下次注意」，是写进 skill 的**前置动作**。
3. **机制同步并校验**：`sync_agents.py --apply --scope skills` → 全量 `--check` 通过；
   `manifest-registry.py --root . validate` → 60 artifacts 通过；`note-updater` manifest `1.2.0 → 1.3.0`。

> 说明：本轮归档依据是「**机制已落地并验证**」（skill 元数据 + 步骤映射 + 同步/清单校验），
> 这正是 `maintain-learnings` Step 5 的定义。至于「下一次处理拆分笔记时行为是否真的变好」，
> 属**未来运行观察项**，不阻塞归档——拦阻复发的是**新步骤（写前必读、定作用范围）**，而不是这条记录本身。
> RULES.md 已有同类铁律却仍复发（「规则存在但未执行」）——本轮把铁律从「RULES 段落」提升为
> skill 里的**强制前置步**，正是针对这一点。

**保留的 RULES 铁律**（本轮的浓缩产物，`RULES.md`「Do」）：

1. 改「多文件（拆分）笔记」前先列齐整套、定「受影响文件集」再动手；
2. 回答澄清问题 / 下定性结论前回一手来源 + 用户实际处境，作用范围写进句子；无来源的数字 / 比例不写。

**结果**：`LRN-20261006-023` / `-024`、`ERR-20261006-018` 三条 **归档**；
活跃文件回到 `LEARNINGS.md` 3 条、`ERRORS.md` 2 条。

---

## 五、第三次维护（同日，`/maintain-learnings`）—— 配方类内容机制落地

承接同日 `/digest` 记录的 `LRN-20261006-025` / `ERR-20261006-019`（第 11 章 Dashboard 认证配置：
bcrypt 取值编造 + compose `$` 未转义）。上一轮只写了 `RULES.md` 铁律，**没有源头机制**；
本轮把它提升为**写作 / 更新环节的强制步骤**。

### 机制改动

| 工件 | 版本 | 新增内容 |
| --- | --- | --- |
| `note-updater` SKILL.md（`.agents/skills/`） | `1.3.0` → `1.4.0` | 新增「**配方类内容：只写『文档逐字给出』或『实测得到』的取值**」小节（在「口径核对」之后） |
| `chapter-writer` agent（`.codex/agents/`） | `1.4.0` → `1.5.0` | `#### 配方类内容要求（env / config / command）` 小节 + `Quality Checklist` 新增一条 |

三句要点：① 文档只给**字段名** ≠ 有取值，缺值标「待核」或回原始载体（源码 / 官方示例 / 容器内实跑输出）取，
**不要用常识补**；② 把文档**转写成派生产物**（compose 片段 / 示例配置 / 命令拼接）落笔前**必做最小实测**
（`docker compose config`）——「读文档」不等于「跑得通」；③ 已知高危点：Compose 的 `$`+字母/下划线会被
当变量插值（`$`+数字反而安全），含 `$` 的哈希须逐段写成 `$$`。

### 验证（`maintain-learnings` Step 5）

1. **skill 元数据校验通过**：`note-updater` SKILL.md frontmatter 的 `name:` / `description:` / 定界符齐全。
2. **记录 → 步骤映射**：两条记录都对应上表的**新小节 + Checklist**，不是「下次注意」。
3. **同步与清单校验**：`sync_agents.py --apply --scope skills|agents` → 全量 `--check` 通过；
   `manifest-registry.py --root . validate` → 60 artifacts 通过；`workflow-health-check.sh` 除既有
   prompt-cache knob drift 外无新问题（routing 检查需 `PYTHON=python3.12`——PATH 上的 `python3` 是 3.9.6，
   属环境问题，已复跑确认 routing 实为 up to date）。

### 未归档（继续留在活跃文件）

`LRN-20261006-025` / `ERR-20261006-019` 机制已落，但**尚未在下一次写作 / 更新运行中被观察验证**。
按活跃文件头部策略（「只有已落到机制**并被验证**的记录才可归档」），本轮**保守不归档**，
状态改为 `pending（机制已落 …，下轮复核后归档）`，保留在活跃文件。

**结果**：本轮**无新增归档**；活跃文件仍为 `LEARNINGS.md` 4 条、`ERRORS.md` 3 条。
（与 2026-09-29 批次 `-020` / `-021` / `ERR-014` / `-015` 同处「机制已落、待下轮复核」状态。）

## 六、第四次维护（同日，`/maintain-learnings`）—— 取证纪律升为跨路径规则

承接同日第二次 `/digest` 新增的 `LRN-20261006-026` / `-027` 与 `ERR-20261006-020`（复现上游产物
时以搜索摘要覆盖官方原文）。

### 为什么是复发（而非新错）

`RULES.md` 的「P1 候选必须标证据形态，`snippet-only` 只当线索、不当证据」条已存在，机制落在
`research-collector` 的 P1/P2。本轮失败**不在该流程内**——直接写一篇 Docker 搭建笔记时把 WebSearch
摘要当成落笔依据，且在一手原文（官方 README）与二手摘要冲突时选了二手。**失败模式与流程无关，
旧规则的作用面按流程划得太窄。**

### 机制改动

`.codex/rules/research-tools.md`（canonical）新增 **「取证纪律（落进产物的取值必须可回一手）」** 一节：

- 「定位信息 vs 一手原文」两形态对照表，明确摘要只能定位、不能定值；
- 4 条铁律：① 落进产物的取值必须能指到一手原文或实测命令 ② 一手与二手冲突以一手为准、不取一次一手
  就在两个二手之间投票 ③ 复现上游产物前先取权威原文再动笔 ④ 与上游的任何出入必须逐条显式列出并给出处。

落点选择：该纪律跨 skill（`research-collector` / `note-updater` / `chapter-writer` / 直写笔记），
故不放单个 SKILL.md，而落项目规则文件。

### 验证（`maintain-learnings` Step 5）

1. **同步与清单校验**：`sync_agents.py --check --scope rules` → 命中 `.claude/rules/research-tools.md`
   （DRIFT）→ `--apply --scope rules` → 全量 `--check` → `[OK] shared agent configuration is synchronized`。
2. **伞形健康检查**：`workflow-health-check.sh` → routing up to date、manifest registry 60 artifacts 通过、
   `shared agent sources are portable` `[OK]`、todo-state action guard 15 处通过；唯一 `FAIL` 为
   **既有** prompt-cache knob drift（`effortLevel` / `thinkingBudget` / `savedProviderEffort`），
   与本次 rules 改动无关（第五节已记录同一现象），非本轮引入。
3. **记录 → 机制映射**：`-026` / `-027` / `ERR-020` 三条均对应到上表新小节的具体条款，非「下次注意」。

### 未归档（继续留在活跃文件）

`LRN-20261006-026` / `-027`、`ERR-20261006-020` 机制已落，但**尚未在下一次写作运行中被观察验证**
（本次修复即发生在触发它的那次会话内，不构成独立观察）。按活跃文件头部策略保守**不归档**，
状态改为 `pending（机制已落 …，下轮复核后归档）`，保留在活跃文件。

**结果**：本轮**无新增归档**；活跃文件为 `LEARNINGS.md` 6 条、`ERRORS.md` 4 条。

### 下轮维护提示

本轮**未做压缩**——用户 2026-10-06 决定「与下轮一起做」。下轮 `/maintain-learnings` 应一次性处理：

- **复核并在通过后归档**在册「机制已落、下轮复核后归档」的 **9 条**：
  `LRN-20260929-020` / `-021`、`LRN-20261006-025` / `-026` / `-027`；
  `ERR-20260929-014` / `-015`、`ERR-20261006-019` / `-020`。
  判据：该机制在下一轮真实运行中**被观察到生效**；未观察到的继续留在活跃文件。
- **归档后做一次真正的压缩去重**（不是清空）：当前三点均偏长——`LEARNINGS.md` 212 行、
  `ERRORS.md` 194 行、`RULES.md` 87 行。压缩时注意 `RULES.md` 的多条长句铁律可合并同族项。
- **`LRN-20260912-012`**（vault 被本会话之外的写者改动、写者身份未定）继续**挂起、不归档**。
- 另记：本 vault 有**自动备份**在每 3~6 分钟提交一次（`zhq vault backup: …`）。本轮
  `docker/如何搭建漫画库.md` 的改动即被 16:10:07 那次提交带走。核对「文件是否已提交」时，
  先把这类自动提交排除在外，不要误判为并发写入。

---

## 七、第五次维护（同日，`/maintain-learnings`）—— 归档 9 条积压记录 + 压缩活跃文件

**触发**：用户显式 `/maintain-learnings`。审计（2026-10-06T16:13）显示三份活跃文件仍超阈值
（`LEARNINGS.md` 212 行 / `ERRORS.md` 194 行 / `RULES.md` 87 行），且 **9 条记录**自 2026-09-29
起一直卡在「机制已落、下轮复核后归档」，第四节的「下轮维护提示」所指的那一轮即本节。

### 门槛修订（本节的核心决定）

原策略要求「机制在**下一轮真实运行中被观察到生效**」才可归档。这 9 条的触发条件**全是罕见错误**
（跨章口径漂移、表格计数把表头算进去、`$` 未转义、二手摘要覆盖一手原文……）——**错误不复发就
永远观察不到**，门槛对低频缺陷**不可证伪**，经验库会无限期堵住。用户 2026-10-06 拍板改为：

> **机制在位 + 经一次维护轮复核通过**，即可归档；全文移入归档文件，`RULES.md` 铁律保留。
> 「是否在真实运行中生效」转为**归档块里的观察项**，不再是归档前置条件。

两句活跃文件头部的策略句已同步改写（`LEARNINGS.md` / `ERRORS.md`）。

### 逐条机制在位复核（`maintain-learnings` Step 5）

| 机制 | 落点 | 复核方式 | 结果 |
| --- | --- | --- | --- |
| 阶段 4 三类跨章比对 | `.codex/workflows/learning-note-flow/workflow.md`（+镜像） | grep 三类判据 | 8 处命中 ✅ |
| P1 证据形态 + 数值重新计数 | `.agents/skills/research-collector/SKILL.md`（+镜像） | `evidence form` `snippet-only`/`fetched`（`:55`/`:61`/`:88`）、recount（`:26`） | 在位 ✅ |
| 配方类内容取值纪律 | `.agents/skills/note-updater` **v1.4.0**（`SKILL.md:16`）+ `.codex/agents/chapter-writer` **v1.5.0**（`:190` + Checklist `:259`） | 版本读 `manifest.yaml`；小节 grep | 在位 ✅ |
| 取证纪律（跨路径） | `.codex/rules/research-tools.md`（+镜像） | grep「取证纪律」 | 在位 ✅ |
| manifest 注册 | `.codex/platform/manifest-registry.py --root . validate` | — | 60 artifacts 通过 ✅ |

> 过程记录：首轮 grep 用中文「证据形态」在 `research-collector` 上得 0，一度像「机制从没落地」；
> 实为该 SKILL.md 是**英文文件**，措辞是 `evidence form`。**复核机制要用机制自己的语言去 grep**，
> 不要用记录里的中文译名——否则会把自己骗成「要重修一遍」。

### 归档记录（9 条）

**1. `[LRN-20260929-020]` correction — 跨章一致性比对只查配置块，漏掉散文式转述与定义句**
- 原记录：阶段 4 跨章比对只覆盖「可照抄的配置块」（且只比冻结标签），不覆盖**对同一来源的散文式
  转述**与**定义 / 判据句**。Hermes 文档的 4 条 profile 用途，第 2 章 L44 概括成「示例用途是「同一个
  人的多个 agent」」，原文 `:14` 是「每个家庭成员一个」——两章对同一份清单做了**相反定性**，靠用户
  读已发布笔记才发现。
- 修复路径：阶段 4 比对扩到**三类**（① 配置块 ② 同一来源的转述 / 定性并排读 ③ 判据 / 分类 / 梯度句
  对术语框架自洽），新增第 ④ 条要求把比对结果写进 state file 的异常记录；明确该比对属**父流程 P4
  关卡**，不下放逐章自检。
- 观察项：下次跑 learning-note-flow 且并行写作 ≥2 章时，确认三类比对是否真的被执行。
- 结果：**归档**

**2. `[LRN-20260929-021]` knowledge_gap — P1 摘要级候选与已抓原文混放，须标注证据形态**
- 原记录：P1 候选记录（标题 / URL / tier / 相关性 / 分数）本身不区分**证据形态**，摘要级与已取正文
  在 `01_explore_result.md` 里外观相同；只写在 §3.1 说明文字里，没变成字段或校验。
- 修复路径：`research-collector` P1 第 3 步要求每个候选标 `snippet-only` / `fetched`，P2 只把
  `snippet-only` 当线索去取、不当证据，完成标准加断言（`SKILL.md:55` / `:61` / `:88`）。
- 观察项：该纪律 2026-10-06 在**流程外**复发过（直写笔记，见 `-026`）；现已由「取证纪律」跨路径
  接管，本轮把两者在 `RULES.md` 里合并成**一条**（Do 段），消除同一纪律两处各说各话的漂移。
- 结果：**归档**

**3. `[LRN-20261006-025]` correction — 配方类内容：文档没逐字给出的取值不得用常识补，派生产物必先实测**
- 原记录：第 11 章「Dashboard 认证配置」两处同源缺陷——① 官方文档只给字段名、没给示例值，撰写时
  用常识补了 bcrypt（Hermes 实为 `scrypt$`）；② 把该字段转写成 compose 片段未实测就落笔，漏了
  Compose 的 `$`+字母插值坑（哈希须写 `$$`）。
- 修复路径：`note-updater` **v1.4.0** 新增「配方类内容：只写『文档逐字给出』或『实测得到』的取值」
  小节；`chapter-writer` **v1.5.0** 加同名要求小节 + Checklist 一条（`.codex/agents/chapter-writer.md:190`
  / `:259`）。三分法：文档逐字给出才直接写 / 未给出就标「待核」或回原始载体取 / 由文档派生的新产物
  落笔前必做最小实测。
- 观察项：下次遇到 env / config / command 类配方内容时，确认是否走了「逐字 / 实测」二分。
- 结果：**归档**

**4. `[LRN-20261006-026]` correction — 直写笔记路径缺「证据形态」闸：二手摘要不能当落笔依据（复发）**
- 原记录：`RULES.md` 已有「P1 候选标证据形态」的规则，但只挂在 `research-collector` 的 P1/P2 上；
  本次**不在该流程内**、直接写 Docker 搭建笔记时，把 WebSearch 摘要当成可落笔的证据，且在一手原文
  （官方 README）与二手摘要冲突时**选错了边**。**复发**——失败模式与流程无关，旧规则作用面按流程
  划得太窄。
- 修复路径：升级为**跨路径纪律**——`.codex/rules/research-tools.md` 新增「取证纪律（落进产物的取值
  必须可回一手）」一节（两形态对照表 + 4 条铁律），经 `.agent-sync` 同步；`RULES.md` 的同一铁律与
  本条的 P1 落地现在合并为一条。
- 观察项：下次任何「要落进产物的取值 / 名称 / 参数」，确认证据是「一手原文逐字」或「实测输出」。
- 结果：**归档**

**5. `[LRN-20261006-027]` workflow — 与上游产物有出入必须显式标注并给出处，不得静默改写**
- 原记录：任务要求「按官方方式搭起来」，却把官方 compose **静默改了**三处（删 `flaresolverr`、
  加 `downloads` 挂载、换 `restart` 策略），笔记里**没有一处**说明「这里与官方不同」；是用户拿官方
  文件来对才发现，可追溯性完全依赖用户自己复核。
- 修复路径：并入「取证纪律」第 4 条——**与上游的任何出入（增删行 / 改默认值 / 换镜像标签）必须
  逐条显式列出并给出处**；本次已就地补 `[!tip]` 列出 `restart` 策略与 `:stable` vs `:preview` 两处偏差。
- 观察项：下次转录上游产物时，确认笔记里带「与官方示例的差异」小节。
- 结果：**归档**

**6. `[ERR-20260929-014]` research-collector / P2 — 对照表行数把表头与分隔行也算进去（「17 轴」实为 15 行）**
- 原记录：官方对照表被记作「17 轴」，实为 **15 条属性行**——属性行计数时把表头与分隔行算了进去；
  错误数字从中转进 3 份上游文件、扩散到全库 12 处。危险点：**同源错误在多处一致**会被误读成「多处印证」。
- 修复路径：全库 12 处订正为「15 行属性对照表」，`02_deep_research.md` 留「口径订正」块；源头闸 =
  `research-collector` 要求数值**重新计数**而非誊抄，明确「数表格只数数据行，表头与分隔行不是属性」
  （`SKILL.md:26`）；`RULES.md` `## Do` 第 34 条保留该铁律。
- 结果：**归档**

**7. `[ERR-20260929-015]` learning-note-flow / P7 后回修 — 判据举证段读不通：判据句措辞与下游术语框架正面冲突**
- 原记录：用户读**已发布**笔记时指出第 1 章判据举证段「看的不是很明白」。根因：判据② 写「服务的
  用户数是单数还是复数」，而同段「多用户」三义 callout 说同一批对象**都能**进多人——判据描述的维度
  **不是**下游框架真正切分的那个维度（应为「所有者 / 信任域个数」）。次因：判据① 引文用错句、判据①
  举三家而判据② 只举两家。**5 处引文逐字正确——引文对 ≠ 论述通。**
- 修复路径：按 A 案改 5 份副本（章节 → 合并件 → 成品 → vault 笔记），改述为「所有者 / 信任域个数」
  并补成 3×2 对称举证；`workflow.md` 阶段 4 跨章比对新增第 ③ 类「上游判据 / 分类 / 梯度句与下游术语
  框架逐条对读，确认两边能同时对同一对象成立」。复测：锚点 107→111、表格行 70/70、Callout 26/27。
- 结果：**归档**（与 `LRN-20260929-020` 同族，同一机制——阶段 4 三类比对）

**8. `[ERR-20261006-019]` note write / 配方转录 — bcrypt 取值编造 + compose `$` 未转义**
- 原记录：已发布成品第 11 章两处「可执行配方」都错——密码哈希写成 bcrypt（实为 scrypt），compose
  片段里 scrypt 哈希未做 `$$` 转义。照抄会得到「Dashboard 永远提示密码错误」，且该症状很难反查回
  「哈希被 Compose 破坏了」这一因。
- 修复路径：重写第 11 章为 scrypt 口径（+ 三种 provider + `HERMES_DASHBOARD_INSECURE` 已废弃 +
  `HERMES_DASHBOARD_HOST`），补 `$$` 转义警告 callout；复测用 `docker compose config`（v5.0.2）逐条
  验证 `$` / `$$` 实际行为，scrypt 前缀与全部字段名回官方文档逐字核对。机制 = 同 `LRN-20261006-025`。
- 结果：**归档**

**9. `[ERR-20261006-020]` note write / 上游配置转录 — 用搜索摘要覆盖官方原文，环境变量名写错 + 凭空多出一条挂载**
- 原记录：① 环境变量名写成 `EXTENSION_REPOS`（官方 docker README 逐字是 `EXTENSION_STORES`）；
  ② 自己加了一条官方没有的 `./data/downloads` 挂载并配了警告。两处都不是打字错，是**用二手材料
  替代一手产物**，且在一手原文与二手摘要冲突时**选错了边**（因为「小模型摘要可能读错」，反而去信了
  搜索摘要）。
- 修复路径：就地修正笔记（`EXTENSION_REPOS` → `EXTENSION_STORES`、删多余挂载与警告、补回官方有的
  `flaresolverr` 与 `user: 1000:1000`、加 `[!tip]` 列出全部差异）；复核用 raw 抓 `Suwayomi-Server-docker`
  的 `README.md` 与 `docker-compose.yml` 原文逐字比对，两段 YAML 用 ruby `YAML.load_file` 解析通过。
  机制 = 「取证纪律」（同 `LRN-20261006-026`）。
- 结果：**归档**

### 压缩结果

| 文件 | 归档前 | 归档后 | 说明 |
| --- | ---: | ---: | --- |
| `LEARNINGS.md` | 212 行 | **约 60 行** | 移出 5 条；头部叙述性历史压缩成一段指向 `archive/` |
| `ERRORS.md` | 194 行 | **约 20 行** | 移出 4 条；活跃计数归 0 |
| `RULES.md` | 87 行 | **86 行** | 合并同一纪律的两处（Do 段「复现上游产物」吸收 Watch For 段「P1 证据形态」），净减 1 行但**消除一处漂移源** |

**结果**：活跃文件回到 `LEARNINGS.md` **1** 条（仅挂起的 `-012`）、`ERRORS.md` **0** 条。
**未归档**：`LRN-20260912-012`（写者身份未定、根因未消除）继续**挂起**。

### 下轮维护提示

- 本节 9 条的「观察项」是**软性**的：下轮若真的遇到对应场景，回来确认机制是否生效；**不生效就新开
  一条**（不要复活已归档条目），并按新门槛重新走一轮。
- 活跃文件已轻，下轮维护应回到「正常审计 → 有复发才修源头」的节奏，不再有积压。
- 本 vault 的**自动备份**（每 3~6 分钟 `zhq vault backup: …`）仍在，核对文件状态时先排除它。

---

## 八、第六次维护（同日，`/maintain-learnings`）—— 配置骨架完整性 + 副本漂移摸底

### 触发（审计信号）

- 审计脚本报 `note-updater` **活跃 2 条**（`LRN-20261006-029` 配置骨架漏字段 + `ERR-20261006-021`
  注释半句当取值）——同一 skill ≥ 2 次，优先修源头。
- `LEARNINGS.md` **114 行** > 100 行阈值。
- 本会话新增 `LRN-20261006-030`（副本漂移没一次摸全）、`ERR-20261006-022`（反向提取越界），
  同属 `note-updater` 面。

### 机制改动

同源纪律落在 **note-updater（更新侧）** 与 **chapter-writer（生成侧）** 两处，避免两者漂移
（这正是 RULES `Do` 段「配方类内容」两处并存的由来）：

1. **canonical `.agents/skills/note-updater/SKILL.md`**（`.claude/` 由同步生成，未手工改）：
   - 「配方类内容」小节新增一条：**配置骨架以官方「完整示例文件」逐字段核对，不只抄教程某一节的
     讲解段**；多文件配方每个代码块标注所属文件（`docker-compose.yml` vs `config.yaml`）。
   - Workflow **Step 6** 改为「摸底**并**登记 vault / workspace 漂移」：① 改拆分子集**任一章前**先跑
     全量副本比对（`publish_copies.py --check`）摸清**全部**漂移章；② 反向同步（vault → workspace）
     须用**未漂移样本**做 byte-exact 往返自证；③ 定位「正文尾部」用章末导航块 / 最后一个匹配项，
     不用 `[-k:]` 这类从文件尾数的索引；④ 方向未定先与用户确认，不默认回写。
   - manifest `1.5.0 → 1.6.0`，description 同步。
2. **canonical `.codex/agents/chapter-writer.md`**：
   - 「配方类内容要求」新增第 4 条（同上「完整示例文件逐字段核对 + 多文件配方标注」）。
   - Checklist 新增一项同样校验。
   - manifest `1.5.0 → 1.6.0`，description 同步。

### 验证（`maintain-learnings` Step 5）

- skill 元数据：`note-updater/SKILL.md` 头部 frontmatter 校验通过（`skill metadata ok`）。
- `python3 .codex/platform/manifest-registry.py --root . validate` → **60 件通过**。
- `.agent-sync/sync_agents.py --check --scope skills` / `--scope agents` → 差异恰为预期 4 个生成文件；
  `--apply` 后全量 `--check` → **`[OK] shared agent configuration is synchronized`**。
- `.claude/scripts/workflow-health-check.sh` → todo-state 动作守卫（15 个 invocation）、routing、manifest、
  可移植性全通过；**唯一 FAIL 是 prompt-cache guard 的 KNOB DRIFT**（`effortLevel` / `thinkingBudget` /
  `savedProviderEffort` 与冻结基线不符）——属**会话侧设置漂移，与本次改动无关**，未处置（改基线会掩盖真问题）。

### 归档记录（5 条）

**1. `[LRN-20261006-028]` correction — 注释半句当权威取值（WebDAV 用户写反）**
- 机制在位复核：note-updater「配方类内容」第 4 条（注释是线索不是权威、逐字留档）已在位。
- 结果：**归档**。

**2. `[ERR-20261006-021]` note-updater — 把模板注释的半个子句当权威取值，结论写反**
- 与 `-028` 同根因；机制 = 同一条 v1.5.0 条款，已复核在位。
- 结果：**归档**。

**3. `[LRN-20261006-029]` knowledge_gap — 配置骨架照抄教程讲解段，漏 `port` / `server.addr`**
- 机制 = 本轮 note-updater v1.6.0「配方类内容」新条 + chapter-writer v1.6.0 第 4 条。
- 结果：**归档**。

**4. `[LRN-20261006-030]` workflow — 改单章前没摸全副本漂移**
- 机制 = 本轮 note-updater Step 6 首条（改前全量 `--check` 摸全）。
- 结果：**归档**。

**5. `[ERR-20261006-022]` 副本同步 — 反向提取发布件正文越界 + off-by-one**
- 机制 = 本轮 note-updater Step 6（反向同步 byte-exact 自证 + 尾部边界用最后一个匹配项）。
- 结果：**归档**。

### 压缩结果

| 文件 | 归档前 | 归档后 |
| --- | ---: | --- |
| `LEARNINGS.md` | 114 行 | 仅挂起的 `-012` + 头部（约 30 行） |
| `ERRORS.md` | 56 行 | **0** 条活跃 |
| `RULES.md` | 91 行 | 保留并新增 3 条铁律（`Do` 1 / `Watch For` 2） |

**未归档**：`LRN-20260912-012`（vault 被本会话之外的写者改动，写者身份未定、根因未消除）继续**挂起**。

### 下轮维护提示

- 本轮 5 条的「观察项」是**软性**的：下轮若真的遇到对应场景，回来确认机制是否生效；**不生效就新开
  一条**（不要复活已归档条目）。
- 活跃文件已轻，下轮维护回到「正常审计 → 有复发才修源头」的节奏。
- prompt-cache guard 的 KNOB DRIFT 若持续 FAIL，应确认是**有意调过会话 effort 设置**还是**基线过期**——
  **不要用改基线的方式消掉 FAIL**。

---
