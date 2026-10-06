# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 长篇笔记（>30KB 或多于 3 章）组装后主动建议拆分：独立章节文件 + 前后导航双链 + MOC 索引页
- Phase 4 beautify 前主动询问用户是否需要 Canvas/Base 配置
- GitHub 项目类主题，先通过 API 获取基本信息再进 Phase 0 提问
- 混合笔记 concept + cheat_sheet 适合"入门+速查"场景
- 工具对比/迁移类主题优先用 practice + compare 混合类型，每个领域同时提供步骤指南和对比表
- 每个学习笔记为核心概念添加 `[!tip] 大白话` 通俗解释 + 打比方类比（临时工牌 / 门禁卡 / 保险箱 / 双保险 / 岗位说明书 / 料理包 / 千层饼 等）；写作新笔记与 update 旧笔记时都补，用户偏好（3x）
- 教程类笔记「一章一节一文件」：顶级小节对应一个文件/产物；同一文件的字段（package.json 的 name/deps/files 等）收进该文件小节的 `####` 子节，不升格为顶级小节
- 教程代码块用文件头注释标注所属路径，并先展示完整文件（先睹为快）再逐段拆讲
- 用户报命令/路径错误时，先读源码核实路径解析基准与文件真实位置，一次改对再写入笔记；改完全文 grep 确认无残留旧表述
- 用户决策点用紧凑文本菜单 + 推荐默认值，不要用多问题 AskUserQuestion 对话框（用户会拒绝）
- 合并多篇独立章节前/后按章命名空间化脚注 ID（`[^cN-…]`），并 grep 校验无重复
- GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/...`；github.io 镜像可能 404
- 中文文本处理优先 python；**但 `python3` 版本随机器而异**（Windows 侧曾为原生 CPython 3.14；macOS 侧默认可能是 3.9），且本仓库部分脚本（`sync-workflow-routing.sh` / `workflow-health-check.sh`）要求 3.10+——在旧 `python3` 上会假报 FAIL，需显式指定更高版本：`PYTHON=$(command -v python3.12) .claude/scripts/workflow-health-check.sh`，不要据此改内容。若用 perl 兜底，必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则字符类正则静默 no-op
- 写 OpenWrt/iStoreOS 第三方插件安装步骤前，先用 GitHub API（`curl api.github.com/.../contents`、`/releases/tags/{tag}`）核实软件源 feed 内容与 release 真实文件名，再写命令；示例 URL 必须来自实际存在的文件
- 用户明确说「删掉」误导内容时，直接删除整节并重排编号，不要加 warning 补丁保留
- 解释抽象概念按「它是什么/解决什么问题 → 具体产物长什么样 → 带具体值的可代入例子（目录树/路径/命令输出）→ 对比表 → 大白话类比」落地；正文去掉类比后仍要能让「没懂」的读者靠表格/例子读懂，不只抛抽象结论（默认写作标准，用户当日连续两次明确要求「都要这样」）
- 给子 agent 派活时**不要转述来源论断**：只传来源 ID + 检索位置，要求「先回原文核对再落笔」；确需带结论必须成对标注（原文加引号 / 概述标「待核对」）。章节验收对每处「官方口径是 / 官方说明 / 原文」逐条回源比对，不只看有没有挂来源 ID
- 中文文本的组装、拆分、统计一律走 python（`re.findall(r'[一-鿿]', t)` 计字数）；批量文本改写脚本必须打印「本次改动 N 处」，N=0 时人工复核，不许静默通过
- 生成类脚本要「先清空再重生成」时，用**前缀白名单删除 + 外来文件即失败退出**，不要用 shell `rm -rf`；在 vault 路径上被 Permission denied 时，把它当成「该把清理逻辑收进脚本」的信号，不要找绕过手段
- 拼接式文档生成（切源文件 → 改尾部 → 拼装）：追加前先对既有尾部做**幂等归一**，并断言目标小标题在成品里出现次数 **== 期望值**（不是 ≥1）；名字的生成侧与校验侧必须调用**同一个函数**（一处带 `.md`、一处不带 → 46 条假死链）
- 单源多下游的管道（合并件 / 分册发布件 / 索引页各取一遍源）：「归一 / 清洗」只能有**一个归属层**，且必须在**最上游的源文件**上；下游只做机械变换。规则只写在某一条下游里 → 另一条下游（尤其**直接读源文件**的发布器）静默漏掉。幂等与归一的验收 = **连跑两遍 diff 为空**（不是「看着不会重复」），且定位插入点要用**尾部连续块 / 最后一个匹配项**，不要用「第一个匹配项」；零宽前瞻类规则（`^(?=…)`）不消费文本，重复运行必重复插入，必须做**前置判定**，后置折叠只能当兜底
- 写进记录（workflow state file / 交付报告）的体积、字数、章数、脚注数：**当场重新运行取数或重新计数**，不留「从上下文旧输出誊抄」的口子；产物在记录之后又被改动时，grep 同一数字的**所有**出现处一并更新。手算的合计不算数——用 `ls -l` / python 计数并复核一遍
- 快照与中间产物**直接落到仓库内路径**（`workspace/<slug>/sources/…`），用仓库相对路径读回；不要拿 `/tmp` 当跨调用中转（沙箱 `/tmp` 映射在 Bash 调用之间不保证一致），也不要把「命令存在」当成「命令可用」——能否用某 API 落配置，先做一次最小可用性探测再写进方案
- 自校验脚本报出「几十条同一性质告警」时，先怀疑**校验器自己**再改被检对象；校验通过 ≠ 产物正确，发布类脚本跑绿之后仍要**逐行读一遍成品**
- 「合并 / 保留外部条目」型生成器（如 hook 配置 bootstrap），校验必须跑在**合并之后的完整结果**上，而不是只跑本次渲染的子集；否则「保留路径」天然免检。退役一个 hook 时，删脚本与删注册必须**同时**做（脚本在 git 里被删，不会让注册表自动更新）
- 核对**联邦 / 聚合式**注册表（Skills Hub、插件市场、包索引、模型仓库）时，先找到它自己的**中央索引 / API 端点**并在索引上检索，**不要**用「本仓库内的目录清单」代替；写全称否定结论（「没有 X」「不存在 Y」）前先自问**作用范围是否等同**，并把范围写进句子本身（「`official` 支里只有 X」而非「Hub 里只有 X」）
- `01_explore_result.md` / `02_deep_research.md` 是**中间产物**、不是可信终点：**引文**要逐字回 `sources/` 比对后再落盘（一个字都不能凭记忆或凭更早的摘要重构——`and argue that` 曾被写成 `we argue that`，沿引用链传进正文，且骗过所有「有没有挂来源」的检查）；**数值/默认值/版本号/行数**要重新计数而不是誊抄（数表格只数**数据行**，表头与分隔行不是属性——15 行属性表曾被记成「17 轴」并扩散到 3 份文件 12 处；同源错误在多处一致会被误读成「多处印证」）；产物要在 handoff 头部自述「本文件是中间产物：引文与数值请回 sources/ 按行号核对」；核对不了就只写语义、不写数值
- RULES 里出现「X 不存在，所以走 Y」这类**绕行规则**时，先查 X 是否本该存在（状态模板、上下游文档、调用点）；能修实现就修，修完把那条绕行规则改写或删除。把缺陷写成规则会让缺口变成「既定契约」，再没人回头
- **官方引文摆放**：一段要摆 ≥3 处引文、或含任一整句英文、或长度 >300 字符时，改用「官方原文 / 说人话」两列对照表 + 结论单独成句 + 关键误读用 `[!warning]`；**只有 1 处短引文时行内保留**，不为形式套表。引文逐字与脚注编号/来源归属一律不动，只改摆放；验收时遮住英文列读一遍「说人话」列，不能只核对引文是否正确（用户反馈「让人很难去理解和看懂啊」）

- **引文只用共享校验器，不要为单个项目再写一个**：`python .codex/scripts/note-citation-check.py <项目目录> [--mode text|verbatim|all|style|copies] [--file 02_deep_research.md] [--corpus 别的项目的/research] [--vault-note "<vault 成品>"]`——三族一次扫完：**V 逐字回源**（未命中、以及**只在本项目中间产物里命中**，都是硬失败；weak 会打印「最长可回源 N/M + 语料最接近处」，一眼判「提取件标记差异 / 跨项目来源 / 自己的概括被当成引文」）· **S 引文体例**（S1 边界叠字、S2 LCS 撞车、S3 反引号外 ASCII 词串、S4 对照表结构）· **C 多副本一致**。判据缺哪条就**补进这个脚本**——历史上每轮都现写一个 `_lcs.py` / `_bare.py` / `_dup2.py` 丢在项目工作区，随项目废弃，下一轮同类缺陷照犯。**门禁必须能红**：改完跑 `python .codex/scripts/note-citation-check-selftest.py`（六个用例全过），一个从没红过的门禁不是门禁。**绿灯 ≠ 通过**：S1/S2/S3 是候选清单要逐条判「真缺陷 / 巧合」，C 要同时看 `实际比对 N 组` 的 **N > 0**（副本一份都没认出来 = 根本没比，属硬失败），`--allow-weak` 放行必须写下理由
- **引文语言**（**生成阶段就照此写**，不要等美化阶段回改）：笔记正文里的**成句英文引文**给中译，**代码 / 命令 / 配置键 / 路径 / 文件名 / 产品名 / 单个技术术语**保留原文（用户明确要求：「那个英文我不是很想看，我更想直接看中文」）。只换不留档不行：逐字原文要另存到章末「引文对照（原文 / 中译 / 出处）」表，否则引用链断掉、读者无法回源核对。译完必须复查两件事——原文是英文时都看不出来：① 引导语 / 括注与中译**撞车**（变成了同一句话。判据：两者最长公共汉字子串 ≥ 5，**只覆盖中译 ≥ 5 个汉字的长引文**；短引文另扫**边界叠字**——译文首字 == 紧邻其前的末字，如「合计约 `约 1,300 token`」的里外两个「约」；改法：引导语缩成话题标签，或把括注里那截中译删掉只留出处）② 「出处」列有没有把正文列举的**产品文件名**（`SOUL.md`、`MEMORY.md`）当来源——**错的出处比空着更糟**，查不到就写 `—` 并在表格引导句里说明 `—` 的含义
- **改「多文件（拆分）笔记」前先列齐整套**：目标若是「总览 + 分章文件（另有 `chapters/`、`output/`、vault 副本）」的**集合**，先一次列齐全部成员、通读总览与各章标题/小结，得出**受影响文件集**，**再**逐文件最小读取改写；口径类改动横跨多章，**不要边改边发现还有文件没看**——结束时对**未修改成员**说明「为何没动」、对集合外相关笔记登记同步范围（机制已落 `note-updater` SKILL.md Step 1）
- **回答澄清问题 / 下定性结论前，回一手来源 + 用户实际处境，并把作用范围写进句子**：「有没有 / 能不能 / 只有…才…」只对**本体库**成立的，就写「**本体库**不能…」，**不要**写成「小雅不能…」（抹掉作用范围的绝对否定是本类错误的典型形态）；无来源的数字 / 比例（「覆盖 85%~90%」）**不写进笔记**。**既有笔记——乃至自己上一轮写进笔记的结论——不是可信起点**，它可能正是待修正对象（机制已落 `note-updater` SKILL.md「口径核对」）
- **配方类内容（env / config / command）只写「文档逐字给出」或「实测得到」的取值**：官方文档只给字段名、没给示例值时，**不要用常识补**（第 11 章曾把文档里的 `scrypt$…` 字段填成 bcrypt `$2b$12$`）——标「待核」或回原始载体（源码 / 官方示例 / 实测输出）取；把文档**转写成派生产物**（docker-compose 片段 / 示例配置 / 命令拼接）落笔前**必做最小实测**（如 `docker compose config`），**「读文档」不等于「跑得通」**——Compose 会把 `$`+字母当变量插值，scrypt 哈希须写成 `$$`（YAML 引号 / `env_file` / `.env` 都挡不住，只有 `$$` 有效；`$`+数字反而安全）（机制已落 `note-updater` v1.4.0「配方类内容」+ `chapter-writer` v1.5.0 同名小节与 Checklist；原记录见同批 `LRN-20261006-025` / `ERR-20261006-019`）

## Don't

- 不要把表格嵌套在列表项内（带缩进），Obsidian 无法渲染列表内的表格；同理，callout（`> [!type]`）里要放表格或分多段时，**中间每个空行也必须写成 `>`**——裸空行会终止 callout，其后的表格/段落掉出框外、渲染散架。发布前跑 `python .codex/scripts/check-md-structure.py "<成品目录>"`（`note-beautifier` Step 4 已挂）：查 ① callout 内表格（`> |`）**前一行**是否带 `>` ② 表格行**前一行**是否为空 ③ 缩进表格（疑似嵌列表）。这些同属「合法 Markdown 却渲染异常」，内容校验器（V/S/C）查不到，必须单独跑结构自检（原记录见 `.learnings/archive/2026-10-06-maintenance.md`）
- 不要用 python 的 `read_text()`/`write_text()`（或 `newline=None` 的文本模式）改 workflow state file 及任何被 shell/perl/awk 按行解析的文件：Windows 上 `write_text` 会按 `os.linesep` 把整篇 LF 写成 CRLF，静默打穿 `todo-state.sh` 的阶段判定（`previous phase is not complete`）。用 `read_bytes`/`write_bytes`，改完数一遍 `b.count(b"\r\n") == 0`。`todo-state.sh` 现已内置行尾守卫（检测到 CRLF 即告警并归一）；出现该告警说明有工具在文本模式下重写了 state file，要去查那个工具而不是手工把它修回去
- 不要手工改 workflow state file 的 `> [PN] …` 阶段行（只能由 `todo-state.sh` 写）；手写 `{complete}` 会让脚本的 `phase_has_status "in_progress"` 预检失败

## Domain

- GitHub Packages / GHCR 认证只支持 Classic PAT（`write:packages` 等 scope）；Fine-grained PAT 无 packages 权限项，遇到"expected scopes"报错先认 `github_pat_` 前缀换 classic

## Watch For

- YAML frontmatter 的 sources 字段中所有含特殊字符（`[]`, `:`）的值必须正确引用，否则 Obsidian 解析失败
- 并行派发 chapter-writer 时，章节过渡语必须自包含（按大纲），不要依赖读取上一章文件
- `todo-state.sh` 动作为 `start|complete|skip|block|mode|confirm`：常规走 `start PN` → `complete PN`；`mode PN <值>` 只改 frontmatter `mode` 键、`confirm PN "说明"` 只追加一行到 `## 用户确认记录`，**两者都不动阶段状态行、不要求前置阶段闭幕**；**最后一个阶段**还需 frontmatter 写 `quality_gate: passed`（走豁免则同时补 `quality_gate_owner` + `quality_gate_due`）
- 并行写作 ≥2 章前先冻结**跨章共享口径**（字段名、术语、命名风格）并写进每个 dispatch：各章「忠于自己手边的来源」合起来可能互相矛盾（官方示例写 `network: "tcp"`、权威文档只文档化 `method` → 同一篇笔记里两章打架）；交付后做**三类**跨章一致性比对，缺一类等于没查：① 可照抄的配置块（跨章 grep 同名键取值）② 同一来源被 ≥2 章引用时，各章**怎么转述它**的并排读（同一份清单 A 章写「用途是 X」、B 章写「用途是 not-X」，两处都能引到原文却互相打脸；并列项要说「**其中一条**」，过强概括是主要形态）③ 上游「判据/分类/梯度」句与下游术语框架逐条对读，确认两边能**同时对同一对象成立**（判据句描述的对象必须是框架真正切分的那个维度——判据写「用户数单复数」而框架按「所有者/信任域」切分时，读者必然读不通）
- note-assembler 等 writer 子 agent 无 Bash/Edit 且 Write 有输出上限；>100KB 长文档由父进程 python 合并；反向扫描定位插入点时必须**同时跳过空行和 `---` 分隔线**，否则扫描停错位置且静默不生效
- 组装脚本调整标题层级时必须**级联到子标题**：只把章标题降一级、不管章内 `## N.M` 与 `## 小结`，会让章标题与节标题同级、大纲整体塌陷；降级后要重新解析标题树逐层校验
- 「合并/保留外部条目」的生成器，校验必须跑在**合并结果**上，不是只跑本次渲染的子集，否则保留路径天然免检（`.agent-sync/bootstrap.py --check` 曾对指向已删脚本的 hook 注册报 `[OK]`）
- 并行子 agent 不得直接修改共享 workflow state file；状态推进由 orchestrator 集中经 todo-state.sh 处理
- workflow 已 `done` 的笔记再被 note-updater 单篇更新时，workspace 侧 `chapters/`、`output/` 副本**不会**跟着变，两边同名文件必然长期漂移：至少登记「vault 已于 <日期> 更新，workspace 副本停留在 <日期>」，并让用户二选一（重跑 note-assembler 同步 / 明确弃用副本），不要默认「以 vault 为准」就收工
- P6 发布前校验最终产物并**建议**拆分：>30KB 或多于 3 章时给出「分册子目录 + README + 每章独立文件 + 前后导航 + MOC 指向 README」方案，但**用户明确选单文件就按单文件发布**（2026-09-11 一篇 43k 汉字 / 228KB 笔记经用户确认单文件落地，非违规）
- iStoreOS 官方 iStore 商店不含代理插件；Passwall SourceForge 源只含 passwall_luci/passwall_packages/passwall2（不含 OpenClash）；OpenClash `.run` 包 `+core` 表示内置内核
- WebFetch 拦截的域名（raw.githubusercontent.com、github.com）改用 `curl api.github.com` 替代
- Discourse 论坛（`community.home-assistant.io`、`community.simon42.com` 这类 `/t/<slug>/<id>` 结构）取**帖子正文**只走 `curl 'https://<host>/t/<id>.json'`（多页 `?page=N`，或读 `post_stream.stream`）；HTML / crawl4ai 路径会 403/522，或**静默只给壳与首帖摘要**。抓取产物里没有目标段落时，先当成**取回方式问题**换取回路径重试，再决定是否把证据置信度降格——漏抓 ≠ 来源不可得（2026-09-18 靠这一条把两帖的「置信度中 / 未核验」闭成「高 / 已核验」）
- 往 Obsidian 笔记加双链前，先核实目标笔记**真实存在**（逐条 `os.path.exists` 断言），不要给 vault 里不存在的概念词埋死链；章级锚点**避开含反引号/箭头/竖线的标题**（如 `2.7.3 主路径：导出 \`.reg\` → …`），改链到不含特殊字符的上级标题
- P1 候选必须标**证据形态**：`snippet-only`（只有搜索摘要）还是 `fetched`（正文已取回）；两者不得在 `01_explore_result.md` 里静默混放——搜索摘要被后来当作已取回的来源用，与「转述带引用」是同一类错。P2 只把 `snippet-only` 当线索去取，不当证据
- 文本比对工具一律**行尾不敏感**比较：本机 `core.autocrlf=true`，工作区是 CRLF，而 `Path.read_text` 会把 CRLF 折成 LF——按原始字节比较的工具在这里会**永久误报**（`[DRIFT] updated: CLAUDE.md` 拖了整轮），把本该可信的门变成人人忽略的噪音。`--check` 退出 1 就先怀疑换行符，别先改内容
- 把某个区域纳入同步范围前，**先双向 diff 两侧**再决定 canonical 方向：`.claude/agents/` 曾严格领先于 `.codex/agents/`（多出 5 处经验），若直接以 `.codex` 为 canonical 跑 `--apply` 会静默删掉它们。正确顺序是「先把领先侧回收进 canonical → 再加 `paths.<area>` 与 `canonical_scopes` → 再 apply」，并用「apply 后镜像逐字节不变」证明回收完整
- 在 canonical 文档里**不要写死 canonical/目标路径字面量**：同步的路径替换会把镜像里那句 `.codex/agents/` 改写成 `.claude/agents/`，于是「canonical 是 X」在镜像里变成「canonical 是 Y」——方向说反。描述方向时用 profile 键名（`paths.agents`、`canonical_scopes`），或写成「哪一侧由 profile 决定」
- 校验脚本**绝不能依赖 `rg`**：在本运行时里 `rg` 只是交互式 shell 上的一个 Claude Code 函数（`type -a rg` 会显示 `rg is a function`），任何**子进程**（`bash script.sh`、pre-commit、CI、别的 runtime）里都是 `command not found`。此时 `if rg ...; then fail; fi` 会退化成「无命中 = 通过」，守卫**静默失效且永远绿灯**。用 `command -v` 探测 + `grep -rnE --exclude-dir=...` 兜底，或让工具缺失直接失败退出；判断命中用 `[ -s "$tmp" ]` 而不是命令退出码
- 守卫和文档引用的路径**必须指向 canonical/现行目录**，指向已退役目录（如 `.codex/skills` 之于 `.agents/skills`）等于零覆盖：被扫的是过期副本，canonical 改动永远不会被抓到。改同步范围或搬迁目录后，grep 一遍 `scripts/`、`rules/`、`agents/` 里的旧路径字面量
- 退役/搬迁目录前先**枚举消费者**，不能只扫源码：**已打包的第三方产物**（`.obsidian/plugins/*/main.js` 这类 bundle）各自持有硬编码路径常量，既不随项目同步、也不出现在 diff 里——Claudian 插件就同时硬编码了 `.codex/skills` 与 `.agents/skills` 两个扫描根。若某消费者还有「默认写回该路径」的行为（插件新建 skill 的弹窗默认根是 `.codex/skills`，且没有可持久化的默认根设置），删除时必须同时记下规避方式（改哪个 UI 选项），否则退役目录会被下游悄悄重建
- 「每台机器一份」的生成物，**默认值必须可移植**：生成器不要把自己的运行时绝对路径（`sys.executable`、`/Library/...`）写进**受跟踪**产物——那会把仓库钉死在最后跑生成器的那台机器上（本仓库因此把一个 macOS 解释器路径提交进 Windows 检出，SessionStart hook 长期是死的）；机器身份只写进明确 untracked 的文件（如 `.agent-sync/local/`）。校验器**不能跳过**生成出来的受跟踪产物（`GENERATED_HOOK_CONFIGS`）：宿主绝对路径恰好出现在那里，跳过它们等于放过唯一会中招的文件；正确做法是**解析**配置取 hook `command` 的可执行 token 再判绝对性（`/Library/...` 通不过 `ABSOLUTE_PATH` 那种只认 `/Users/`·`/home/`·盘符的通用正则），且**不要**顺手放宽通用正则——`/opt/...conda` 之类「候选探针清单」是可移植代码
- 守卫写完要**问三件事：谁调用它、它在本仓库能不能变绿、绿是不是空绿**。三条任一不成立就等于没有守卫：`validate_portability.py` 曾同时三缺（无调用点；`core.autocrlf=true` 下按工作区字节判换行 → 每次调用 567 条全红 → 必然被无视；查表失败也会「绿」）。落地方式：接进 `workflow-health-check.sh`；换行符改判 `git ls-files --eol` 的 `i/` 字段（提交的是索引内容，工作区 CRLF 是策略产物不是缺陷）；用程序化断言证明查表真读到数据（条数 > 0），再配双向注入证明该层承重
- 双向注入测试**要确认注入物真的进了被检对象**：Git Bash 会把 `/Library/...` 这种 POSIX 绝对路径实参自动改写成 `C:/Program Files/Git/Library/...`，于是「通用正则」也会命中，看起来通过了、实际测的不是新写的那层。加 `MSYS2_ARG_CONV_EXCL='*'` 让路径原样落盘，再看 findings 是否仍由目标层产生
- Stop hook 反复报 `Background subagents are still running` 时：Claudian 的子代理注册表是**每标签页、纯内存**的，一次**被取消的异步子代理**会永久占用 → 每次 Stop 都阻断，且无文件可清；处置是重载插件 / 关闭重开标签页 / 重启 Obsidian。先用 `TaskOutput task_id=<id> block=false` 证伪（返回 `No task found` 即为残留），**绝不编造或预测未到达的结果**，也不要反复刷屏解释（`hasRunningSubagents` 无超时，属插件缺陷，项目侧修不了）
- 编辑 workflow state file 时**只允许改**：复选框、frontmatter（`quality_gate*`）、说明段落；`> [PN] …` 阶段行**只能由 `todo-state.sh` 写**（手写会被下次脚本调用覆盖或与状态机不一致）
- Bash 的工作目录**在调用之间持久化**：一旦某次用了 `cd <子目录>`（如 `cd .obsidian/plugins/claudian`），之后所有相对路径（`.learnings/…`、`workspace/…`）都会解析到错误位置并报 `No such file or directory`。要么每次写成 `cd /d/Study-Notes && …` 复合命令，要么全程用绝对路径
- 执行中偏离**已批准的具体方案**（落点/顺序/形式）时：可以按更合理的方式做，但报告里必须写明「原方案 / 实际做法 / 理由」三要素，放在显眼处，不与其他结果混在一起
- `.agent-sync/validate_portability.py` 的 `ABSOLUTE_PATH` 会**误报源码里的正则字面量**：字符类里「单个字母 + 冒号 + 反斜杠」的一段会被读成盘符路径，于是一行合法正则让整个共享资产判「不可移植」（`.codex/scripts/note-citation-check.py` 的分隔行判定就中过）。规避：字符类换个**等价排列**（如把空白、连字符、竖线、`\s` 重排），源码与注释里都别写那段字面量。**不要**为消假阳性去放宽 `ABSOLUTE_PATH`——它抓到过被提交进 Windows 检出的 macOS 解释器路径；要放宽就先写一个能红的用例
- 生成物不参与同步镜像：canonical 脚本目录里被 python 顺手写出的 `__pycache__/*.pyc` 会让 `sync_agents.py --check` 永远报一条 `[DRIFT] created`（apply 复制过去、下次 check 又追不平）。同步器已按 `__pycache__` / `*.pyc` 忽略（`.agent-sync/sync_agents.py` 的 `IGNORED_PARTS` / `IGNORED_SUFFIXES`）；目录里出现别的构建产物时按同一原则处理，不要靠 `--apply` 追平
- 会打印 `.learnings`／笔记内容的脚本**必须自己把输出流设成 UTF-8**：Windows 上 `print()` 继承 ANSI 代码页（GBK），而学习记录全是中文 → `UnicodeEncodeError` → 脚本非零退出，提醒**静默消失**。入口处 `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`（stderr 同理），不要指望宿主设 `PYTHONUTF8`。核实「某脚本在这台机器上能不能跑」要看**退出码**，不能只看它打出了标题行——`read_learnings.py` 就是先正常打印头部、再在第一个汉字处崩掉
