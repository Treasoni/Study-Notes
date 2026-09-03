# 学习笔记大纲：《用 academic-research-skills + nature-skills 完成软件类毕业设计（组合实操指南）》

> 笔记类型：实战笔记（ARS + nature-skills 双库组合实操指南）
> 目标深度：上手（能用、会用、知道每技能在哪个阶段起作用、知道边界和坑）
> 主线：按毕设阶段 0–10 主轴混排双库，两库互补、不设主次
> 预估总字数：约 1.4–1.6 万字（13 个一级章）

## 阅读约定（供 chapter-writer，非正文章，不计入一级章统计）

- 章 = `##`，节 = `###`，小节 = `####`；全篇不超过 4 级层级。
- 每个一级章必须包含：章首一行元信息（篇幅/素材/代码示例）+ 若干 `###` 节 + 章末「写作提示」块。
- **全篇三个贯穿提醒**，每个一级章至少出现一次，做成 callout 或独立小节：① 中文毕设/GB/T 7714 适配；② 系统开发边界（两库均不写代码、不跑实验、不证明系统跑通）；③ AI 诚信与披露（辅助不代写、引用防幻觉、遵守学校披露规范）。
- **素材引用**沿用 02_deep_research.md 的来源 ID（A1–A11 / N1–N15，可带 02 内锚点如「02§4」）。禁止无源断言；区分「官方事实」与「推断/改造建议」。
- **命令标注约定**：ARS 实证命令仅 `/ars-plan`、`/ars-lit-review`、`/ars-reviewer`、`/ars-rebuttal-audit`、`/ars-mark-read`、`/ars-cache-invalidate`（来源 A9/A10）；未实证的 `/ars-*` 一律标注「惯例 /ars-<mode>」并对照 A4 模式注册。nature-* 无统一斜杠命令，按语义路由触发，写清 wrapper/subagent 触发语句（见 02 第 6 节）。
- 正文主线 = 02 第 4 节十阶段表展开为章；每章开头交代「该阶段双库分工、用什么、怎么触发、产出什么、坑」。

---

## 第 1 章 开篇：这套双库指南怎么用

> 篇幅：~800 字 ｜ 素材：A1、N1；02§2、02§4 ｜ 代码示例：无（仅定位速览与路线图）

### 本章定位
- 给读者一张「地图」：本指南解决什么问题、按什么顺序读、现在（已定题、未开始文献）该跳到第几章。
- 双库互补不设主次：ARS = 学术全流程「人机协作」调度器（流程、审稿、诚信 gates）；nature-skills = 可复用科研技能库（图、PPT、文献管线、引文核验、英文润色）。

### 建议正文结构
- 指南读法：目标读者（会用 Claude Code、已定题、未接触双库）；「从头照做」或「按当前阶段跳读」两种读法；上手级定位，不是论文。
- 双库分工速览表：一句话定位 / 首选 runtime / 调用方式 / 核心强项 / 明确不做（含两库都不写代码、不跑实验）。
- 许可与生态差异：ARS CC BY-NC 4.0（非商用）vs nature-skills Apache-2.0；ARS 为 Claude Code 插件体系，nature-skills 以 Codex 为主、需 Claude Code 接线。
- 端到端路线图：0–10 阶段一览表（主用库色标 🔵ARS / 🟢nature / ⚙️工程侧 + 主产物），标出「你现在在这里 = 阶段 1」。

### 写作提示（供 chapter-writer）
- 为什么用：避免读者把两库当「一键毕设工具」，先建立「流程 + 技能」双库心智。
- 用什么：02§2 定位速览表、02§4 映射表（作为路线图数据源）。
- 怎么触发：无命令；只给概念速览与章节导航。
- 产出什么：一张可跳读的路线图 + 分工决策直觉。
- 坑：不要写成纯目录罗列；强调两库不是同一类东西（流程调度 vs 技能库），重叠功能（写作/综述/审稿/引用）的选择留到对应章 + 第 13 章决策表。
- 贯穿提醒：三个主题各一句预告（详见第 13 章）。

---

## 第 2 章 环境准备：Windows 下安装 ARS 与 nature-skills 并接线 Claude Code

> 篇幅：~1100 字 ｜ 素材：A5、A6、A1、N1、N3；02§6 ｜ 代码示例：PowerShell 安装命令、/plugin 命令、git clone、wrapper 文件、autoupdate-skills.sh

### 本章定位
- Windows 上把「Claude Code + ARS + nature-skills」跑通的最小可用环境；本指南后续所有触发都依赖本章成功。

### 建议正文结构
- 安装 Claude Code 并配置密钥：PowerShell `irm https://claude.ai/install.ps1 | iex`（免 Node、自动更新）；设置 `ANTHROPIC_API_KEY`。
- 安装 ARS：
  - 推荐 plugin 法：`/plugin marketplace add Imbad0202/academic-research-skills` → `/plugin install academic-research-skills`（建议开 auto-update）。
  - 备选手动法：把 4 个 skill 目录（deep-research / academic-paper / academic-paper-reviewer / academic-pipeline）分别复制进项目 `.claude/skills/`，每目录顶层必须有 `SKILL.md`，勿整仓嵌套。
- 安装 nature-skills：
  - `git clone https://github.com/Yuan1z0825/nature-skills.git`；说明「技能目录 = 安装单元，须保留完整目录 + nature-shared 共享包，不能只拷 SKILL.md」。
  - Claude Code 接线两条路线：wrapper 推荐（给需要的技能写 `~/.claude/agents/nature-<x>.md`，正文 = 先读 clone 内 `skills/<技能>/SKILL.md` 并遵守，按需读同目录与 nature-shared；升级 = `git pull`）；copy 路线（`scripts/autoupdate-skills.sh --force` 同步到 `~/.claude/skills` + settings.json SessionStart hook）。
- 依赖与 Windows 坑：Git Bash（跑 .sh hook，缺失时 ARS guard 降级）；真实 Python（`py -3`→`python3`→`python` 探测，绕过 MS Store 0 字节 stub）；可选 Pandoc（DOCX）/ tectonic + CJK 字体（PDF，缺则自动降级 Markdown）；文献检索 MCP 需 `PUBMED_EMAIL` / Scopus `pybliometrics` 凭据（禁止入库）。
- 项目级偏好：在毕设仓库 `CLAUDE.md` 写 standing preferences 块（引文风格、检索范围、OA），两库会话继承。

### 写作提示（供 chapter-writer）
- 为什么用：两库都是 agent 技能体系，装错一步（缺共享包、缺 Git Bash、python3 stub）会静默失败。
- 用什么：A5（ARS 安装/依赖）、A6（Windows guard 探测）、N1/N3（nature-skills 架构与 Claude Code 接线）、02§6（Windows 实操要点合并）。
- 怎么触发：按上表逐一给命令与验证方法（安装后用一条简单触发确认可用）。
- 产出什么：可运行环境 + 一张「我装了什么、装在哪、如何升级」的本地清单。
- 坑：MS Store python3 stub；Git Bash 缺失致 hook 不激活；只拷 SKILL.md 导致子路由/共享引用断裂；MCP 凭据入库风险；ARS 勿整仓嵌套复制。
- 贯穿提醒：系统开发边界（本章起就明确两库不写代码，开发需另配工程工作流）；AI 诚信（动手前确认学校对 AI 工具的规范）。

---

## 第 3 章 阶段 0 选题与开题：把题目收敛成可辩护的研究论点

> 篇幅：~800 字 ｜ 素材：A1、A2、A10、A3；N6、N1；02§4 ｜ 代码示例：/ars-plan（实证）、nature-proposal-writer compose 模式触发语句

### 本章定位
- 用户「已定题」，本阶段重点是：把既有题目收敛成可辩护的研究问题/论点、产出开题报告骨架与章节契约雏形；若开题报告已交，可快速浏览。

### 建议正文结构
- 为什么这个阶段值得用双库：选题决定后续所有检索范围与章节契约；开题报告 = 第一次「proposal-first」写作演练。
- ARS 侧：`/ars-plan` 苏格拉底式澄清（实证，A10 实录）；plan 前先过 research-readiness；产出论点结晶与证据需求清单；缺料标 `[MATERIAL GAP]` 防脑补。
- nature-skills 侧：`nature-proposal-writer`（Beta，frontmatter researchwrite）的 compose 模式，开题/章节骨架状态机；随附 references 含中文科研写作清理（对中文开题报告有用）。
- 产出验收：一页式研究问题/论点声明、开题报告骨架（初步章节契约：每章核心论点/证据/风险）。

### 写作提示（供 chapter-writer）
- 为什么用：阶段 0 的产出直接当阶段 2 章节契约的输入，避免返工。
- 用什么：A10（/ars-plan 实录）、A1/A2（research-readiness 与 checkpoint 概念）、N6（proposal-writer 三模式 + 中文写作 reference）。
- 怎么触发：给 `/ars-plan` 的一条起始指令样例 + nature-proposal-writer 的一条 wrapper/subagent 触发语句（语义路由，非斜杠命令）。
- 产出什么：研究论点 + 开题骨架 + 检索范围草稿。
- 坑：/ars-plan 是逐问人机对话需预留时间；proposal-writer 为 Beta，三模式（compose/revise/hybrid）要按「从零 vs 已有草稿」选；两库均不代写开题报告正文。
- 贯穿提醒：AI 诚信（开题即定披露基调：辅助不代写）；中文适配（开题报告为中文，两库模板偏英文需对照学校要求）。

---

## 第 4 章 阶段 1 文献调研与综述：建立证据底座（你现在在这里）

> 篇幅：~1800 字 ｜ 素材：A2、A3、A9、A10；N4、N5、N12、N9、N1；02§4 ｜ 代码示例：/ars-lit-review（实证）、deep-research 触发、nature-literature-pipeline / nature-academic-search / nature-reader 触发语句

### 本章定位
- 核心章。读者当前正处于此阶段（已定题、未开始文献）。目标是产出一份「可被审计」的证据底座，供后续综述与写作引用。

### 建议正文结构
- 双库分工先讲清：ARS 粗筛 + 综述骨架与缺口标记；nature-skills 持续发现 + 元数据/他引核验 + 中英对照精读。双保险关系：ARS 检「有没有关键文献被漏」，nature 检「引用的文献/元数据是否为真」。
- ARS 侧流程：deep-research（socratic/full）起手；`/ars-lit-review` 产出 RQ Brief / Annotated Bibliography / Synthesis / INSIGHT；缺料标 `[MATERIAL GAP]`，禁止用模型记忆脑补。
- nature-skills 侧工具链：
  - `nature-literature-pipeline`（Stable）：持续文献发现管线，多源检索 + 六维评分 + 精读卡片 + 推送归档（依赖本机 cron，适合作毕设主题周推）。
  - `nature-academic-search`（Beta）：多源检索 + 元数据核验 + 他引审计 + 引用者画像；需 PUBMED_EMAIL / pybliometrics；二级索引仅作线索，关键字段回 DOI/出版社核实。
  - `nature-reader`（Beta）+ 上游 `nature-downloader`：PDF/DOI → 中英对照 Markdown 精读底稿 + source_map.json；强调「合法取全文」。
  - `nature-ref-verifier`（Stable）在此阶段可提前用于核验已收集条目，尤其 CNKI 中文来源。
- 软件类毕设检索策略提示：除通用学术库外，如何把「系统实现类」文献（技术报告、标准、开源项目文档）纳入证据底座，并区分「学术文献」与「工程资料」两类引用。
- 产出验收：Annotated Bibliography + 综述骨架 + 中英对照精读底稿 + 引用核验报告雏形。

### 写作提示（供 chapter-writer）
- 为什么用：综述质量决定论文论证可信度；双库互补点在此阶段最密。
- 用什么：A2/A9（lit-review 端到端）、A3（gate 矩阵）、N4/N5/N12/N9（nature 四条工具链）。
- 怎么触发：给 `/ars-lit-review` 起始指令样例；给 nature-literature-pipeline、nature-academic-search、nature-reader 各自的语义路由触发语句（wrapper/subagent 指向 SKILL.md）。
- 产出什么：证据底座四件套（RQ Brief、Annotated Bibliography、Synthesis、INSIGHT）+ 精读底稿 + 核验报告。
- 坑：引用幻觉双保险（ARS 缺口标记 + nature 他引审计 + ref-verifier 兜底）；CNKI/图书馆通道决定 nature-downloader 可行性；不要指望两库代写综述正文（AI 诚信）；`ARS_CLAIM_AUDIT=1` 非默认，需说明如何开。
- 贯穿提醒：AI 诚信（文献「真读」与防幻觉）；中文适配（综述最终要落到 GB/T 7714 中文引用，阶段 6 细讲）；系统边界（检索范围含工程资料，但系统本身不在此阶段产出）。

---

## 第 5 章 阶段 2 论文结构与大纲：先签章节契约再动笔

> 篇幅：~900 字 ｜ 素材：A2、A10；N6、N1；02§4 ｜ 代码示例：/ars-plan（实证，逐章确认）、nature-proposal-writer hybrid/revise 触发语句

### 本章定位
- 把阶段 0/1 的论点与证据底座编排成论文骨架；每章形成「核心论点 / 证据 / 风险 / 字数预算」的章节契约，供阶段 4 逐章写作。

### 建议正文结构
- ARS 侧：`/ars-plan` 逐章确认（每章须 User confirmation 检查点）；产出 Chapter Plan + Argument Map + 字数预算。
- nature-skills 侧：`nature-proposal-writer` 的 hybrid/revise 模式——已有草稿或学校章节模板时重排成 proposal-first 骨架。
- 软件类毕设结构映射提示：学校模板（需求分析 → 系统设计 → 实现 → 测试）与 ARS 默认学术论文结构的差异如何处理；何时用 ARS 章节契约字段、何时按学校目录硬约束调整。
- 产出验收：一版带章节契约的论文大纲（含每章核心论点、支撑证据来源、风险与字数）。

### 写作提示（供 chapter-writer）
- 为什么用：动笔前定契约，避免「写废章」；软件毕设易在实现细节上失控，字数预算先行。
- 用什么：A10（plan 实录）、A2（checkpoint/章节契约概念）、N6（proposal-writer 模式）、02§4 阶段 2 行。
- 怎么触发：给 `/ars-plan` 逐章确认对话的起始指令 + nature-proposal-writer hybrid/revise 触发语句。
- 产出什么：可执行的论文大纲（含每章契约字段）。
- 坑：每章 User confirmation 不可省；两库默认结构未必匹配软件毕设模板，须以学校模板为准微调；不要把大纲做成纯目录。
- 贯穿提醒：中文适配（章节结构对齐中文软件毕设模板与开题报告承诺）；系统边界（实现细节的写作留到阶段 6/7 的 claim 登记，不在此章展开）。

---

## 第 6 章 阶段 3 系统设计与实现：工程侧主战场（双库仅做登记）

> 篇幅：~900 字 ｜ 素材：A2、A3；N1；02§2、02§4 ｜ 代码示例：无 ARS/nature 开发命令（仅登记 claim/provenance 的方式说明，对照阶段 7 自查）

### 本章定位
- 明确告知：本阶段为**工程侧为主**，两库均不写代码、不跑实验、不能证明系统跑通；双库只做「已实现结果登记为 claim/provenance」，供阶段 7 查证与论文引用。
- 需要另配常规软件工程工作流（需求 / 架构 / 编码 / 测试），本指南给出「开发 + 学术」双线如何配合。

### 建议正文结构
- 边界与预期管理：两库在毕设中的职责到本阶段为止；ARS 与 nature-skills 都不覆盖系统开发。
- ARS 侧登记：把已实现的功能/测试结果登记为 claim / experiment provenance（命名、状态、证据位置），这是阶段 4 写作素材与阶段 7 自查证据的来源。
- nature 侧登记：`nature-experiment-log` 仅留痕，不做实验验证。
- 双线配合建议：开发线产物（架构图、ER/类图、流程、测试记录、截图/数据）如何成为阶段 5 图表素材、阶段 6 引用（工程资料）、阶段 7 审计证据。
- 产出验收：可运行系统 + 测试记录 + 一张「claim 登记清单」（每个可写进论文的功能点都有对应证据）。

### 写作提示（供 chapter-writer）
- 为什么用：给读者正确预期——双库在此阶段作用最小，避免「AI 帮我写系统」的误解；同时保证论文里每个「我实现了 X」都有据可查。
- 用什么：02§2（两库对系统开发均不覆盖）、02§4 阶段 3 行（⚙️ 工程侧）、A2/A3（claim/provenance 与 7 失败模式 M3「幻觉实验」的关系）。
- 怎么触发：无触发命令；写「在论文/notes 里登记 claim」的字段模板，并预告阶段 7 会用 integrity gates 查这些 claim。
- 产出什么：系统 + 证据 + claim 登记清单。
- 坑：不要谎报「系统跑通/实验完成」（阶段 7 M3/M5 专门查这个）；不要把本阶段时间花在调双库上。
- 贯穿提醒：系统开发边界（本章主提醒，整章贯穿）；AI 诚信（如实记录哪些是 AI 辅助、哪些是自研）。

---

## 第 7 章 阶段 4 论文写作：从章节契约到完整初稿（中文正文）

> 篇幅：~1700 字 ｜ 素材：A1、A2、A3、A4、A9、A10；N7、N1；02§4、02§5 ｜ 代码示例：/ars-plan（实证）、ARS 写作模式（惯例 /ars-full 等，标注）、nature-polishing 触发语句

### 本章定位
- 核心章。把阶段 2 的章节契约逐章写成初稿；写完初稿跑 2.5 integrity gate 再进入阶段 7 全面自查。
- 明确中文正文润色在两库均为开放问题（详见下），本章只保证「结构、论证、引用骨架」成立。

### 建议正文结构
- ARS 写作流程：academic-paper 写作模式（plan → full；惯例 `/ars-full`、`/ars-abstract` 等标注）+ Style Calibration（风格校准，识别机器腔是为质量把关而非掩饰 AI）。
- 章节粒度：一章一 checkpoint；每章对照章节契约（core argument / evidence / risk）。
- claim 审计：说明 `ARS_CLAIM_AUDIT=1`（非默认）开启 4→5 claim 审计，把论文里的 claim 与阶段 3 登记证据挂钩。
- 2.5 integrity gate：初稿完成后跑 7 类 AI 失败模式自查（M1 实现 bug、M2 幻觉引用、M3 幻觉实验、M4 捷径、M5 bug 包装为发现、M6 方法伪造、M7 框架锁定）。
- nature-skills 侧：
  - `nature-polishing`（Stable）：**仅英文目标**——适用于英文摘要/外文综述，不直接适用于中文正文。
  - `nature-writing`（Draft，成熟度注意）：按需选用，标注未在真实案例充分测试。
  - `nature-proposal-writer` revise：可回头把偏离契约的章节重排。
- 中文正文润色开放问题：两库均无中文母语级润色；给出可行组合（学校模板 + 人工 + 其他中文润色工具），并标注为「待学校确认的开放问题」。
- 产出验收：逐章草稿 + 双语摘要 + 英文润色稿（如需要）+ 2.5 gate 验证报告。

### 写作提示（供 chapter-writer）
- 为什么用：阶段 4 是产出密度最高的阶段；gate 前置可省掉阶段 7/8 大返工。
- 用什么：A1（定位与诚信立场）、A2（10 阶段状态机与 checkpoint）、A3（7 失败模式）、A4（模式注册）、A9/A10（触发实录）、N7（polishing 边界）。
- 怎么触发：给 `ars-plan` 逐章起始指令；写作模式命令一律标注「惯例」；nature-polishing 给英文摘要触发语句。
- 产出什么：初稿 + gate 报告 + 双语摘要。
- 坑：中文正文润色无现成方案别硬套 nature-polishing；别让 AI 直接「代写」整章（诚信）；写作阶段就要挂引用占位（阶段 6 统一核验）；`ARS_CLAIM_AUDIT` 默认关，需显式开。
- 贯穿提醒：AI 诚信与披露（本章最密：辅助不代写、机器腔检查目的、如实披露）；中文适配（正文语言与排版）；系统边界（不把阶段 3 未做之事写进论文）。

---

## 第 8 章 阶段 5 图表：投稿级科研图与架构图的审计化生产

> 篇幅：~900 字 ｜ 素材：N8、N1；A3；02§4 ｜ 代码示例：nature-figure 触发语句（契约先行 + 自动审计）、可选 GPT Image 2 概念草图

### 本章定位
- 产出软件毕设所需的图：系统架构图、ER/类图、流程图、对比实验图、机制图；以 nature-figure 为生产与审计主力，ARS 侧作 caption-图一致性兜底。

### 建议正文结构
- nature-figure（Stable）工作流：图件契约先行 → 多面板对齐门 → PDF 字号/碰撞自动审计（PyMuPDF）；输出 SVG/PDF/TIFF + 审计报告；可选 GPT Image 2 出概念草图。
- 软件毕设常见图分类：哪些适合 nature-figure 管线（科研结果图、多面板对比），哪些仍用工程绘图工具（架构图/类图可入图件契约但模板需自建）。
- 与阶段 3 产物的衔接：系统截图/测试数据如何在「不加工数据」前提下进入图件。
- 中文适配点：图内中文与字体（CJK）在 PDF 审计中的处理；图注/分辨率按 Nature 契约裁剪到学校要求。
- 产出验收：一批已审计图件（SVG/PDF/TIFF）+ 每图的审计报告。

### 写作提示（供 chapter-writer）
- 为什么用：图表在毕设评审中是「工作量证据」；自动审计把字号/清晰度问题前置。
- 用什么：N8（nature-figure README）、A3（gate 矩阵中 caption-图一致相关 gate，作为 ARS 侧兜底）。
- 怎么触发：给 nature-figure 的语义路由触发语句（先给图件契约再生成，再触发自动审计脚本）；说明依赖（Python/R、PyMuPDF）。
- 产出什么：可插入论文的图 + 审计报告。
- 坑：中文字体在 PDF 审计里可能缺字形；系统截图 ≠ 科研图，别把「界面截图」包装成「结果图」；图表诚信（不 PS 数据、不夸大）。
- 贯穿提醒：中文适配（图内中文与字体）；系统边界/诚信（图为阶段 3 真实产物的可视化，阶段 7 会核对）。

---

## 第 9 章 阶段 6 引用与参考文献：核验链 + GB/T 7714 改造路径

> 篇幅：~1100 字 ｜ 素材：A7、A8、A5、A11；N9、N5、N11；02§3.3、02§5 ｜ 代码示例：/ars-citation-check（惯例，标注）、nature-ref-verifier 触发语句（含 CNKI 条目）

### 本章定位
- 把阶段 1/4 攒下的引用做成「可信、格式合规」的参考文献表；本阶段是中文毕设适配的重灾区（GB/T 7714 全线缺失）。

### 建议正文结构
- ARS 引文能力现状：中文引文指南 = 台湾学术惯例 APA 7.0 繁体扩展（A7）；switcher 覆盖 APA 7 / Chicago(Notes) / Chicago(Author-Date) / MLA 9 / IEEE / Vancouver（A8）；**无 GB/T 7714**。
- nature-skills 侧：
  - `nature-ref-verifier`（Stable）：参考文献逐条多源交叉验证、字段级报告 + 严重度分级 + BibTeX/Zotero patch；**明确支持 CNKI 中文来源**——对中文毕设直接有用。
  - `nature-academic-search`：提供 Nature/APA/IEEE/Vancouver 引文格式（无 GB/T 7714）。
  - `nature-citation`（Beta）：只补 CNS 系支撑文献 → 软件/中文文献需另接 ARS 检索，勿误用。
- GB/T 7714 改造路径（**推断建议，非现成能力，必须标注**）：仿 A7 在 ARS 新增 `gb7714_citation_guide.md`；在 switcher 加「→GB/T 7714」转换块；项目 CLAUDE.md 写 GB/T 7714 standing preference。最省力降级路线：先用现成 **IEEE**（同为顺序编号制，形态最近）再人工微调。
- 社区信号：Issue #425（社区要求对齐中国高校 LaTeX 模板）佐证需求真实存在。
- 防幻觉把关链：ref-verifier 字段核验 + academic-search 他引审计 + ARS citation 检查（惯例 `/ars-citation-check`）三段式。
- 产出验收：全篇参考文献表 + 核验报告 + 需人工改 GB/T 7714 的差异清单。

### 写作提示（供 chapter-writer）
- 为什么用：中文毕设参考文献格式常是硬性扣分点，而两库默认都不支持国标，必须显式处理。
- 用什么：A7/A8（中文引文现状与 switcher）、A5（standing preference 途径）、A11（社区佐证）、N9（CNKI 核验）、N5/N11（格式与边界）。
- 怎么触发：nature-ref-verifier 语义路由触发语句（含一条 CNKI 中文条目样例）；ARS citation 命令标「惯例」。
- 产出什么：可提交的参考文献表 + 核验 patch + 国标差异清单。
- 坑：A8 文件头自述「5 formats」与矩阵 6 项不一致（引用时说明）；GB/T 7714 任何「自动输出」均为社区改造/推断，不是官方支持；引用幻觉仍属最高风险，需走完整把关链。
- 贯穿提醒：中文适配/GB/T 7714（本章主提醒）；AI 诚信（引用必须真实存在、真实读过）。

---

## 第 10 章 阶段 7 自查与审稿模拟：integrity gates + 双审稿人

> 篇幅：~1800 字 ｜ 素材：A1、A2、A3、A4、A9；N10、N1；02§4、02§5 ｜ 代码示例：/ars-reviewer（实证）、/ars-rebuttal-audit（实证，预告阶段 8）、nature-reviewer 触发语句

### 本章定位
- 核心章。提交前的全面自查：ARS 2.5/4.5 integrity gates（不可跳过）+ `/ars-reviewer` 审稿模拟 + nature-reviewer 三份预投评审；产出可执行的 Revision Roadmap。

### 建议正文结构
- 自查编排顺序：4.5 gate（提交前强制）→ `/ars-reviewer` → nature-reviewer 交叉；说明 2.5/4.5 MANDATORY checkpoint 不能自动跳过。
- ARS reviewer 机制：Sprint Contract（先盲承诺评分准则再评审）+ Devil's Advocate；让步须评分 ≥4/5；产出 reviewer reports。
- 7 类 AI 失败模式在软件毕设中的具体化：M1 实现 bug、M2 幻觉引用、M3 幻觉实验、M4 捷径、M5 bug 包装为发现、M6 方法伪造、M7 框架锁定——逐一给「在毕设里长什么样」的自查问题（如「功能真实现？数据/截图真？文献真读？」）。
- nature-reviewer（Draft）侧：三份互盲预投评审 + cross-review synthesis + Major/Minor/Blocking；注明维度是 Nature 口径，需换算成软件毕设自查清单。
- 与阶段 3/6 联动：用 claim 登记清单与引用核验报告作为自查证据；缺证据的 claim 标 `[MATERIAL GAP]`。
- 产出验收：Material Passport + 验证报告 + reviewer reports + Revision Roadmap。

### 写作提示（供 chapter-writer）
- 为什么用：查重/降重不是两库职责，但「真实现、真实验、真文献」是它们能兜底的；此阶段把「论文主张 vs 实际证据」对齐。
- 用什么：A1/A2/A3（gates 与 7 模式）、A4（oversight 层级）、A9（reviewer 实录）、N10（nature-reviewer）。
- 怎么触发：给 `/ars-reviewer` 起始指令；给 nature-reviewer 三份评审的语义路由触发语句。
- 产出什么：自查报告四件套 + 修订路线图（给阶段 8）。
- 坑：nature-reviewer 是 Draft（未在真实案例充分测试）；两库审稿口径不同（Nature 维度 vs 软件毕设清单）需人工换算；integrity gates 是质量把关不是掩盖 AI；此阶段不替代学校查重。
- 贯穿提醒：AI 诚信（审稿防自我美化，如实回答「是否 AI 代做/代写」）；系统边界（自查「系统真跑通？」）；中文适配（自查清单中加 GB/T 7714 合规项）。

---

## 第 11 章 阶段 8 返修与迭代：把导师意见当作 External Review

> 篇幅：~700 字 ｜ 素材：A2、A9、A10；N1；02§4 ｜ 代码示例：/ars-rebuttal-audit（实证）、/ars-mark-read（实证）、nature-response 触发语句（可选）

### 本章定位
- 接收外部意见（导师/评阅人/自查发现的 Major/Minor）后，按「R-A-C 回复 → 修改 → 再审」循环收敛；ARS 全流程最多 2 轮完整修订，适合毕业季时间盒。

### 建议正文结构
- 把导师意见映射为 External Review：将意见拆成点对点条目；区分「事实/论证/格式」三类。
- ARS revision 机制：R-A-C（Response / Action / Change）逐条回复 + re-review；`/ars-rebuttal-audit`（实证）审计 rebuttal 质量；`/ars-mark-read`（实证）管理已读状态、`/ars-cache-invalidate`（实证）清理缓存。
- 断点续跑与状态复位：`resume_from_passport=<hash>`；`ARS_PASSPORT_RESET=1`。
- nature 侧（可选）：`nature-response`（投稿返修回复，按需）。
- 修改闭环：若返修暴露新实验/新实现缺口 → 回阶段 3/7 补证据，再回到本章。
- 产出验收：Point-by-Point Response + Delta Report（改了什么、证据在哪）。

### 写作提示（供 chapter-writer）
- 为什么用：毕设返修常是「导师意见散、学生改得乱」；R-A-C 让每次修改可追踪。
- 用什么：A2（最多 2 轮 + 断点续跑）、A9/A10（rebuttal-audit 等实证命令）、N1（nature-response 索引）。
- 怎么触发：给出 `rebuttal-audit`、`mark-read`、`cache-invalidate` 的实证命令及用途表；revision 命令若写成 `/ars-revision` 须标「惯例」。
- 产出什么：逐条回复 + 改动清单。
- 坑：2 轮上限是时间盒策略，别无限返修；返修不得新增未做实验的 claim；rebuttal 语气是「回应审稿人」而非「辩解」。
- 贯穿提醒：AI 诚信（返修是真实修改，不是让 AI 把意见「圆过去」）；中文适配（格式修改类意见归入 GB/T 7714 差异清单）。

---

## 第 12 章 阶段 9+10 答辩汇报与格式提交：PPT、导出与披露

> 篇幅：~1100 字 ｜ 素材：N13、N1；A5、A8、A2；02§4、02§6 ｜ 代码示例：nature-paper2ppt 触发语句（中文 PPTX）、nature-image2ppt、ARS format 模式（惯例，标注）、Pandoc/tectonic 导出命令

### 本章定位
- 两个收尾环节合并成「答辩与提交」冲刺章：答辩/组会材料（nature 独占）与终稿格式导出（ARS 为主 + 学校模板兜底）。

### 建议正文结构
- 答辩/组会 PPT（nature-skills 独占段）：`nature-paper2ppt`（Beta）把论文/毕设转成 10–16 页**中文** PPTX + speaker notes；`nature-image2ppt`（图→PPT）；按汇报时长裁剪页数。
- 终稿格式导出（ARS 侧）：format 模式把 MD 转 DOCX（Pandoc）→ tectonic PDF（需 CJK 字体：Times New Roman / Source Han Serif TC / Courier New）；缺依赖自动降级 Markdown + 指引。
- 学校模板为准：两库导出未必匹配学校 Word/PDF 模板 → 以学校模板/查重系统要求为最终准绳；Stage 3/3' 可当「投稿前预演」跑一遍。
- AI 披露 bundle：随提交附 AI 使用披露材料（Material Passport / disclosure 摘要），与学校规范对齐。
- 提交前 checklist：格式合规、引用格式终检、图表字体、查重前置、披露材料齐全。
- 产出验收：答辩 PPT + speaker notes + 最终 .md/.docx/.pdf + 披露 bundle。

### 写作提示（供 chapter-writer）
- 为什么用：答辩 PPT 与导出是两库互补最直观的一段（nature 出图/PPT、ARS 出流程与导出），同时是 AI 披露的最后一关。
- 用什么：N13（paper2ppt 中文）、N1（image2ppt 索引）、A5（Pandoc/tectonic + CJK）、A8（format switcher 背景）、A2（3/3' 预演）。
- 怎么触发：nature-paper2ppt / nature-image2ppt 语义路由触发语句；format 导出命令若写成 `/ars-format-convert` 须标「惯例」。
- 产出什么：可答辩材料 + 终稿文件集 + 披露材料。
- 坑：PDF 需 CJK 字体否则中文乱码；PPT 页数要按答辩时限裁剪；学校模板优先于任何自动导出；披露不是「藏 AI」，是如实声明辅助范围。
- 贯穿提醒：中文适配（学校模板、中文排版、GB/T 7714 终检）；AI 诚信（披露 bundle 本章主提醒）。

---

## 第 13 章 收尾：三个贯穿主题 + 触发速查附录

> 篇幅：~1000 字 ｜ 素材：02§5、02§7、02§8；A4、N1 ｜ 代码示例：附录速查表（实证 vs 惯例命令、nature 语义路由触发）

### 本章定位
- 把散落在各章的三个贯穿主题收拢成可决策的结论；给全篇最需要的两张速查表与素材索引；列出需用户/学校确认的开放问题。

### 建议正文结构
- 贯穿主题一：中文毕设 / GB/T 7714 适配——汇总各章适配点（开题报告、章节模板、中文正文润色开放问题、参考文献国标改造路径、PDF 中文字体、答辩 PPT 中文）；给出「IEEE 先行 vs 自建 gb7714 guide」的决策说明。
- 贯穿主题二：系统开发边界——两库均不写代码/不跑实验/不证明系统跑通；给「开发线 × 学术线」的并行节奏图与 claim 登记习惯。
- 贯穿主题三：AI 诚信与披露——两库官方「辅助不代写」立场；如何写学校要求的披露说明；引用/claim 双保险的最终责任在人。
- 双库重叠功能选择决策表：写作 / 综述 / 审稿 / 引用四个重叠点「何时用 ARS、何时用 nature、何时都不用」。
- 附录 A：ARS 命令速查——实证命令（/ars-plan、/ars-lit-review、/ars-reviewer、/ars-rebuttal-audit、/ars-mark-read、/ars-cache-invalidate，来源 A9/A10）与「惯例 /ars-<mode>」（对照 A4 27 模式）分列，禁止混标。
- 附录 B：nature-* 技能触发速查——技能 / 成熟度（Stable/Beta/Draft）/ 语义路由触发语句 / Claude Code 接线方式 / 对应毕设阶段。
- 附录 C：素材来源索引（A1–A11 / N1–N15 一句话说明）。
- 开放问题清单（需用户/学校确认）：是否强制 GB/T 7714；学校对 AI 披露/比例要求；系统具体技术栈；中文润色工具选型；文献获取通道（CNKI/图书馆/CARSI）。

### 写作提示（供 chapter-writer）
- 为什么用：让读者合上指南后带走三张「可执行记忆」：决策表、命令速查、开放问题清单。
- 用什么：02§5（矛盾与缺口，作为三个贯穿主题的论据池）、02§7（开放问题）、02§8（交接约定）、A4（模式注册）、N1（技能索引）。
- 怎么触发：不触发新命令；只汇总速查。
- 产出什么：三主题决策结论 + 附录速查 + 待办确认清单。
- 坑：附录 A 不得把「惯例」命令写成实证；成熟度差异（Draft/Beta/Stable）要保留标注；开放问题不能替用户/学校做决定，只能给选项与默认建议。
- 贯穿提醒：三个主题在此章全部正式收口。

---

## 学习路径说明

### 前置要求
- 已定题（用户已满足）；会用 Claude Code（用户已满足）；本机可装 Claude Code 并有 `ANTHROPIC_API_KEY`。
- 建议具备：Git Bash、真实 Python（`py -3` 可用）；可选 Pandoc / tectonic + CJK 字体用于导出；文献获取通道（CNKI/图书馆/CARSI）影响阶段 1 用法。
- 阅读前先确认学校两条规范：参考文献是否强制 GB/T 7714；AI 辅助写作的披露/比例要求。

### 学完能做什么
- 按毕设 0–10 阶段，知道每一阶段该用 ARS 还是 nature-skills、怎么触发、产出什么、坑在哪。
- 能独立走通：文献调研（阶段 1）→ 章节契约（阶段 2）→ 写作 + 2.5 gate（阶段 4）→ 引用核验与国标改造（阶段 6）→ 自查审稿（阶段 7）→ 返修（阶段 8）→ 答辩 PPT 与提交导出（阶段 9/10）。
- 能正确管理预期：两库不写系统、不做中文母语润色、不自动输出 GB/T 7714、不代写；知道每条 AI 辅助产出的披露与验证责任在自己。

### 建议学习顺序
- 从头通读（1 → 13）约 2–3 小时；时间紧则：第 1 章必读 → 第 2 章装好环境 → 跳到当前阶段章（现在为第 4 章）实操 → 后续按阶段推进，遇到自查/返修/导出再回看第 10–12 章。
- 每完成一个阶段章，回到第 13 章附录 A/B 核对命令与技能，再进入下一阶段章。

---

## 大纲统计

- 一级章总数：13（第 1–13 章；另有一个非正文「阅读约定」块，不计入）
- 预估总字数：约 1.46 万字（各章 ~700–1800 字，合计落在 1.4–1.6 万区间）
- 是否按十阶段主轴推进：是（0–10 阶段顺序展开；其中阶段 9+10 合并为第 12 章「答辩与提交」，仍沿主轴推进）
