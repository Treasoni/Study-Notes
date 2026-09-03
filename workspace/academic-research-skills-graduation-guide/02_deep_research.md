# 02 深度素材 — ARS + nature-skills 双库毕设组合实操指南

> 阶段：P2 深度收集（方向 A：按毕设阶段混排双库）　|　日期：2026-09-03
> 主题：用 academic-research-skills(ARS) + nature-skills 辅助「软件/系统开发 + 中文毕业论文」类毕设
> 使用说明：本文件为 claim 级素材（每条附来源 ID + 锚点），不粘贴正文。下游（outline-generator / chapter-writer）按来源 ID 引用即可，避免重复抓取。

## 1. 信源总表

### 1.1 ARS（Imbad0202/academic-research-skills，v3.21.1，CC BY-NC 4.0）

| ID | 文件 | Tier | 主要覆盖 |
|---|---|---|---|
| A1 | README.zh-CN.md | T1 | 定位、4 skill/27 mode、边界、诚信立场 |
| A2 | academic-pipeline/SKILL.md | T1 | 10 阶段调度、入口检测、checkpoint、状态机 |
| A3 | docs/ARCHITECTURE.md | T1 | 阶段×skill×gate 矩阵、7 失败模式、数据访问 |
| A4 | MODE_REGISTRY.md | T1 | 27 模式注册、oversight 层级 |
| A5 | docs/SETUP.md | T1 | 安装、依赖、CLAUDE.md standing preferences |
| A6 | hooks/run_guard.sh + hooks.json | T1 | Windows python3 stub、Git Bash、guard 降级 |
| A7 | academic-paper/references/apa7_chinese_citation_guide.md | T1 | 中文引文 = 台湾惯例 APA 7.0 扩展 |
| A8 | academic-paper/references/citation_format_switcher.md | T1 | 格式切换（APA/Chicago/MLA/IEEE/Vancouver） |
| A9 | academic-pipeline/examples/full_pipeline_example.md | T1 | 端到端对话触发实录 |
| A10 | academic-paper/examples/plan_mode_guided_writing.md | T1 | /ars-plan 苏格拉底大纲实录 |
| A11 | GitHub Issue #425（api 未取，scout 佐证） | T3 | 社区要求对齐中国高校 LaTeX 模板 |

### 1.2 nature-skills（Yuan1z0825/nature-skills，Apache-2.0）

| ID | 文件 | Tier | 主要覆盖 |
|---|---|---|---|
| N1 | README.md（中文主文档） | T1 | 19 技能索引、成熟度、架构、安装 |
| N2 | README_EN.md | T1 | 英文镜像 |
| N3 | docs/open-source-agent-frameworks.md | T1 | Claude Code/Codex/其他框架接线 |
| N4 | skills/nature-literature-pipeline/README.md | T1 | 文献持续管线 |
| N5 | skills/nature-academic-search/README.md | T1 | 多源检索/元数据/他引审计/MCP |
| N6 | skills/nature-proposal-writer/README.md | T1 | 开题/章节状态机（compose/revise/hybrid） |
| N7 | skills/nature-polishing/README.md | T1 | 英文 Nature 风格润色 |
| N8 | skills/nature-figure/README.md | T1 | 投稿级科研图 + 自动审计脚本 |
| N9 | skills/nature-ref-verifier/README.md | T1 | 参考文献多源核验（支持 CNKI） |
| N10 | skills/nature-reviewer/README.md | T1 | 三份预投评审模拟 |
| N11 | skills/nature-citation/README.md | T1 | claim→CNS 系支撑文献 |
| N12 | skills/nature-reader/README.md | T1 | 论文→中英对照 Markdown reader |
| N13 | skills/nature-paper2ppt/README.md | T1 | 论文→中文 PPTX |
| N14 | 社区/T2：awesomeskills.dev、cnblogs | T2 | 生态收录、二手解读（低权重） |
| N15 | 社区/T3：头条「ARS+图」、CSDN Windows 坑 | T3 | 组合用法与 Windows 实操（低权重） |

### 1.3 覆盖质量
- 共抓取 **T1 官方源 24 个**（ARS 10 + nature 14），T2 2 个，T3 3 个（其中 2 个经 HTTP 核验）。
- 全部 ARS/nature 技能 README/SKILL 均以 raw.githubusercontent HTTP 200 抓取成功；GitHub api 中途限流，issue/树接口部分缺失（已在表内标注，不影响正文结论）。

## 2. 双库定位速览

| 维度 | ARS（academic-research-skills） | nature-skills |
|---|---|---|
| 定位 | 学术论文生产全流程「人机协作」调度器 | 可复用科研技能库（Nature/CNS 风格基准） |
| 许可 | CC BY-NC 4.0（非商用） | Apache-2.0 |
| 首选 runtime | Claude Code 插件（CLI/VS Code/JetBrains） | Codex 为主，官方也列 Claude Code/OpenClaw/OpenCode/Hermes |
| 安装单元 | 4 个 skill 目录（或 plugin） | 每个 `skills/nature-*` 目录 = 一个技能 |
| 调用方式 | 模式/斜杠命令（/ars-plan、/ars-lit-review…）+ 自然语言 | 主要 LLM 语义路由触发（无统一斜杠命令体系）；Claude Code 用 wrapper/subagent/slash 指向完整目录 |
| 核心强项 | 阶段化流程编排、苏格拉底澄清、**integrity gates**（2.5/4.5 七模式阻断）、引用 trust-chain/L3 claim 审计、风格校准、格式链 | 技能覆盖面广（19 个）、**输出优先**、科研绘图/PPT/文献管线/参考文献核验、成熟度标注（Draft/Beta/Stable） |
| 明确不做什么 | 不代写；不执行实验/代码；不能证明系统跑通；无 GB/T 7714 | 不虚构结果/引用；`nature-citation` 只查 CNS 系；`nature-polishing` 只做英文；无 GB/T 7714 |
| 对系统开发 | 不覆盖（需外部工程工作流 + 已登记声明接回论文） | 不覆盖（nature-experiment-log 仅留痕） |

## 3. 核心事实与 claim/源映射

### 3.1 ARS 全流程与诚信机制
- ARS v3.21.1 = 4 skill（deep-research / academic-paper / academic-paper-reviewer / academic-pipeline）、27 mode、覆盖研究→写作→审查→出版。 [A1][A4]
- 定位「AI 是副驾驶不是机长」；写作质量检查识别机器腔是为质量把关而非掩饰 AI。 [A1]
- pipeline 为 10 阶段（RESEARCH→WRITE→2.5→REVIEW→REVISE→3'→4'→4.5→FINALIZE→PROCESS SUMMARY），每阶段强制用户 checkpoint；中途进入不可跳过 2.5。 [A2]
- checkpoint 三类 FULL/SLIM/MANDATORY；MANDATORY 不可自动跳过。 [A2]
- 2.5/4.5 integrity gates 跑 7 类 AI 失败模式（M1 实现 bug/M2 幻觉引用/M3 幻觉实验/M4 捷径/M5 bug 包装为发现/M6 方法伪造/M7 框架锁定）。 [A1][A3]
- reviewer 采用 Sprint Contract：先盲承诺评分准则再评审，含 Devil's Advocate；让步须评分≥4/5。 [A3][A9]
- 全流程最多 2 个完整修订循环；适合毕业季时间盒。 [A2][A9]
- 断点续跑：`resume_from_passport=<hash>` / `ARS_PASSPORT_RESET=1`。 [A2]
- 预算透明：启动时给 token 估算 + 往返预算。 [A2]
- 反泄露：缺料标 `[MATERIAL GAP]`，禁止用模型记忆脑补。 [A2][A10]

### 3.2 ARS 安装 / 依赖 / 坑
- 最小可用 = Claude Code + ANTHROPIC_API_KEY + 在含 ARS skill 的仓库跑 `claude`。 [A5]
- Windows 装 Claude Code：PowerShell `irm https://claude.ai/install.ps1 | iex`（免 Node，自动更新；npm 已弃用）。 [A5]
- 推荐 plugin 法：`/plugin marketplace add Imbad0202/academic-research-skills` + `/plugin install academic-research-skills`。 [A1][A5]
- 手动装：把 4 个 skill 目录分别复制进项目 `.claude/skills/`，每目录顶层必须有 `SKILL.md`；**勿整仓嵌套**。 [A5]
- `.docx` 需 Pandoc；PDF 需 tectonic + CJK 字体（Times New Roman、Source Han Serif TC、Courier New）；缺则自动降级 Markdown+指引。 [A5]
- Windows：`python3` 常是 MS Store 0 字节 stub；guard 用 `py -3`→`python3`→`python` 探测真 Python（须 probe 打 `ARS_PY_OK`）；无 Git Bash 时 `.sh` hook 不激活（接受的降级）。 [A6]
- 内容偏好无全局配置：官方途径 = 项目 `CLAUDE.md` 的 standing preferences 块（引文风格/检索范围/期刊层级/OA）。 [A5]

### 3.3 ARS 中文引文 / GB/T 7714
- 中文引文指南 = **台湾学术惯例 APA 7.0 繁体扩展**（作者姓,名 倒置、中英混排排序、全角括号、公元年、2024a/b 等）。 [A7]
- switcher 实际覆盖 6 种格式：APA 7 / Chicago(Notes) / Chicago(Author-Date) / MLA 9 / IEEE / Vancouver（文件头自述 "5 formats"，与矩阵 6 项不一致）。 [A8]
- **无 GB/T 7714**：大陆国标（顺序编码制 `[1]`、著者-出版年制、文献类型标识 `[J]/[M]/[D]/[C]/[EB/OL]`、拼音排序）均无现成支持。 [A7][A8]
- 可行改造（推断建议，非现成能力）：仿 `apa7_chinese_citation_guide.md` 新增 `gb7714_citation_guide.md`；在 switcher 加 "→GB/T 7714" 转换块；项目 CLAUDE.md 写 GB/T 7714 standing preference。 [A5][A8]
- 软件工程论文若走编号制，可先用现成 **IEEE**（同为顺序编号制，形态最近）降改造成本。 [A8]

### 3.4 nature-skills 总览 / 架构 / 安装
- 19 个可触发技能（Stable 4 + Beta 10 + Draft 5）；nature-shared 为共享支持包，不计入。 [N1]
- 技能目录 = 安装单元；含 SKILL.md（agent 入口）+ README(中英镜像) + references/ + static/ + manifest.yaml（router 式）+ nature-shared 依赖。 [N1]
- **不能只拷 SKILL.md**：须保留完整目录与 nature-shared，否则共享引用/子路由断裂。 [N1][N3]
- Claude Code 接线：官方**无同步脚本**（update-codex-skills.sh 只写 ~/.codex/skills）；推荐「稳定 clone + wrapper(.claude/agents 或 slash command 指向 clone 内 SKILL.md)」或「copy 进 ~/.claude/skills + autoupdate-skills.sh」。 [N1][N3]
- 依赖：npx 方式需 Node 18+；脚本/MCP 技能需手动 pip install（nature-paper-to-patent、nature-academic-search/mcp-server 等）；浏览器技能需 playwright chromium；MCP 凭据（PUBMED_EMAIL、Scopus pybliometrics）禁止入库。 [N1][N5]
- 定位：Apache-2.0；创始人自述 DeepMind Science Skills 借鉴其设计（作者自述，非第三方证实）。 [N1]
- 关键技能调用约定：**nature-* 无统一斜杠命令，LLM 语义路由触发**。 [N4–N13]

### 3.5 nature-skills 逐技能能力（毕设相关）
- **nature-literature-pipeline**（Stable）：持续文献发现管线，多源检索 + 六维评分 + 精读卡片 + 推送归档；依赖本机 cron；适合毕设主题周推。 [N4]
- **nature-academic-search**（Beta）：多源检索 + 元数据核验 + 引用格式（Nature/APA/IEEE/Vancouver，无 GB/T 7714）+ 严格他引审计 + 引用者画像；依赖 PUBMED_EMAIL / pybliometrics；二级索引仅作线索，关键字段回 DOI/出版社核实。 [N5]
- **nature-proposal-writer**（Beta，frontmatter researchwrite）：proposal-first 写作状态机，compose/revise/hybrid 三模式；随附 20 个按需加载 references（含中文科研写作清理）；适合开题/章节骨架。 [N6]
- **nature-polishing**（Stable）：润色/重构/翻译成 Nature 风格英文；不新增结果/夸大 novelty；**对中文正文不直接适用**（英文目标）。 [N7]
- **nature-figure**（Stable）：投稿级科研图（Python/R），图件契约先行，多面板对齐门 + PDF 字号/碰撞自动审计（PyMuPDF）；可选 GPT Image 2 概念草图；图表阶段核心。 [N8]
- **nature-ref-verifier**（Stable）：参考文献逐条多源交叉验证，字段级报告 + 严重度分级 + BibTeX/Zotero patch；明确支持中文来源 CNKI → **对中文毕设参考文献核验直接有用**。 [N9]
- **nature-reviewer**（Draft）：三份互盲预投评审 + cross-review synthesis + Major/Minor/Blocking；维度是 Nature 口径，需换算成软件毕设自查清单。 [N10]
- **nature-citation**（Beta）：段落拆 claim(S001…) + 只补 CNS 系文献 → 软件/中文文献需另接 ARS 检索。 [N11]
- **nature-reader**（Beta）：PDF/DOI→中英对照 Markdown + source_map.json；精读底稿；上游依赖 nature-downloader 合法取全文。 [N12]
- **nature-paper2ppt**（Beta）：论文/毕设→10–16 页**中文** PPTX + speaker notes；答辩/组会汇报。 [N13]

## 4. 毕设阶段 × 双库映射（主轴）

> 图例：🔵=ARS　🟢=nature-skills　⚙️=工程侧（双库不覆盖，需另配工作流）

| # | 毕设阶段 | 用哪个/怎么用 | 主要产物 | 关键注意 |
|---|---|---|---|---|
| 0 | 选题/开题 | 🔵 `/ars-plan` 苏格拉底；🟢 nature-proposal-writer（compose） | 研究问题/论点结晶、开题报告骨架、章节契约 | ARS plan 先做 research-readiness；proposal-writer 有中文科研写作 reference |
| 1 | 文献调研/综述 | 🔵 `/ars-lit-review`、deep-research socratic/full；🟢 nature-literature-pipeline（持续）、nature-academic-search、nature-reader（精读）、nature-downloader（取全文） | RQ Brief、Annotated Bibliography、Synthesis、INSIGHT；中英对照精读底稿 | 双保险：ARS 粗检 + nature 元数据/他引核验；`[MATERIAL GAP]` 防脑补 |
| 2 | 论文结构/大纲 | 🔵 `/ars-plan`（逐章确认，每章须 User confirmation）；🟢 nature-proposal-writer（hybrid/revise） | Chapter Plan、Argument Map、字数预算 | 每章 core argument/evidence/risk/字数 |
| 3 | 系统设计/实现 | ⚙️ 常规软件工程工作流（需求/架构/编码/测试） | 系统、测试、数据/截图 | ARS：把已实现结果登记为 claim/experiment provenance；两库均不写代码不跑实验 |
| 4 | 论文写作 | 🔵 academic-paper plan/full、风格校准；🟢 nature-writing(Draft)、nature-polishing（仅英文摘要/外文部分） | 草稿、双语摘要、英文润色 | 中文正文润色两库均不直接覆盖→需中文润色方案（开放问题） |
| 5 | 图表 | 🟢 nature-figure（多面板图/机制图/架构图 + 自动审计） | SVG/PDF/TIFF、审计报告 | 图注/分辨率按 Nature 契约裁剪到学校要求；ARS VLM 图检守护 caption-图一致 |
| 6 | 引用/参考文献 | 🔵 citation compliance/formatter（APA 中文扩展）；🟢 nature-ref-verifier（字段核验，含 CNKI）、nature-citation（仅 CNS） | 引用清单、核验报告、BibTeX/Zotero patch | **GB/T 7714 需自建**：最省力先用 IEEE 编号制或加 gb7714 guide |
| 7 | 自查/审稿模拟 | 🔵 integrity gates（2.5/4.5 七模式）+ `/ars-reviewer`；🟢 nature-reviewer（三份预投评审） | Material Passport、验证报告、reviewer reports、Revision Roadmap | 2.5/4.5 不可跳过——正好查「功能真实现？数据/截图真？文献真读？」 |
| 8 | 返修/迭代 | 🔵 revision（R-A-C 回复 + re-review，最多 2 轮）；🟢 nature-response（投稿返修回复，可选） | Point-by-Point Response、Delta Report | 毕设可按「导师意见=External Review」走 |
| 9 | 答辩/组会 | 🟢 nature-paper2ppt（中文 PPTX）、nature-image2ppt；🔵（可选）格式导出 | 10–16 页中文汇报 PPT + speaker notes | ARS 无 PPT 对应，此段 nature 独占 |
| 10 | 格式导出/提交 | 🔵 formatter（MD→DOCX(Pandoc)→tectonic PDF + disclosure bundle） | .md/.docx/.tex/.pdf、AI 披露材料 | 学校模板/查重为准；Stage 3/3' 当投稿前预演 |

## 5. 矛盾与缺口（写正文时要显式处理）

1. **GB/T 7714 全线缺失**：ARS（台湾 APA7 + switcher 六格式）与 nature-skills（academic-search 四格式、ref-verifier 支持 CNKI 但无国标输出）均不直接输出大陆国标；Issue #425 证明社区已知需求。→ 指南需给「改造路径」与「先用 IEEE 编号制」的降级建议。
2. **中文正文写作/润色无现成方案**：nature-polishing 只做英文目标；ARS 无中文母语级润色模式。→ 开放问题：中文正文如何润色（学校模板 + 人工 + 其他工具）。
3. **ARS switcher 自述 "5 formats" 与矩阵实际 6 项不一致**；A8 头注释与矩阵矛盾，引用时注意。
4. **成熟度差异**：nature-writing/reviewer/statistics 等为 Draft（未在真实案例测试）；毕设硬依赖优先 Stable（figure/polishing/ref-verifier/literature-pipeline）。
5. **Cursor 适配**：nature-skills 官方未列 Cursor；「可适配 Cursor」仅社区推断，勿写成官方支持。
6. **第三方经验低可信**：头条「ARS 管流程 + nature 管图表」、CSDN Windows 排错属 T3 经验，可参考不背书。
7. **ARS claim audit 非默认**：ARS_CLAIM_AUDIT=1 才插 4→5 审计（v3.8）；指南须说明如何开启。
8. **两库调用方式不同**：ARS 斜杠命令 + 模式；nature-* 语义路由 + wrapper → 组合指南必须给触发路由表，避免用户困惑。

## 6. 实操要点合并（写给 Windows 用户）

1. 装 Claude Code：PowerShell `irm https://claude.ai/install.ps1 | iex`；设 `ANTHROPIC_API_KEY`。
2. ARS：`/plugin marketplace add Imbad0202/academic-research-skills` → `/plugin install academic-research-skills`（建议开 auto-update）。
3. nature-skills：`git clone https://github.com/Yuan1z0825/nature-skills.git`；Claude Code 下二选一：
   - wrapper 路线（推荐）：给需要的技能写 `~/.claude/agents/nature-<x>.md`，正文 =「先读 clone 内 `skills/<技能>/SKILL.md` 并遵守，按需读同目录与 nature-shared，勿退化为通用回答」；升级 = clone 内 `git pull`。
   - copy 路线：`scripts/autoupdate-skills.sh --force` 同步到 `~/.claude/skills`，并在 settings.json 加 SessionStart hook。
4. 前置与依赖：Git Bash（跑 .sh hook）；真 Python（`py -3`/`python3`/`python`，绕过 MS Store stub）；可选 Pandoc(DOCX)/tectonic+CJK 字体(PDF)；需要文献检索 MCP 时配 PUBMED_EMAIL / Scopus 凭据（**禁止入库**）。
5. 项目级偏好：在毕设仓库 `CLAUDE.md` 写 standing preferences（引文风格、检索范围），两库 agent 会话继承。
6. 目录纪律：nature-* 必须保留完整技能目录 + nature-shared；ARS 勿整仓嵌套装。

## 7. 开放问题（P3/P4 需用户确认或后续补充）

- 学校是否强制 **GB/T 7714** 或指定参考文献格式？（决定改造路径：IEEE 先行 vs 自建 gb7714 guide）
- 学校对 **AI 辅助写作的披露/比例**要求？（决定哪些阶段建议用 ARS/nature、如何写披露）
- 毕设系统的**具体类型/技术栈**？（决定 examples 与架构图模板建议）
- 中文正文润色方案：学校模板 + 人工 + 是否需要额外中文润色工具？
- 是否需要 **文献获取通道**（CNKI/图书馆/CARSI）？影响 nature-downloader/academic-search 用法。

## 8. 下游交接（给 outline-generator / chapter-writer）

- 建议正文主线 = **第 4 节十阶段表**展开为章；每章开头给「用哪个库的技能、触发什么、得到什么、注意什么」。
- 引用规范：用来源 ID（A1–A11 / N1–N15）+ 锚点，禁止无源断言；区分「官方事实」与「推断/改造建议」。
- 命令/代码示例：ARS 命令名以 A9/A10 实证为准（/ars-plan、/ars-lit-review、/ars-reviewer、/ars-rebuttal-audit、/ars-mark-read、/ars-cache-invalidate），未实证命令标注「惯例 /ars-<mode>」。
- 章内须有「中文毕设适配」「系统开发边界」「AI 诚信与披露」三个贯穿提醒。
- 指南的最终形态 = 用户拿到能对着自己当前阶段（文献调研）直接操作；用户当前处于阶段 1。
