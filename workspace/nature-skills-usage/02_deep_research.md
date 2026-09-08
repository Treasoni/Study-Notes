# 如何用好 nature-skills（Codex 上手实战指南）— P2 深度素材

> 运行: nature-skills-usage · 阶段: P2 深度收集 · 检索日期: 2026-09-08
> 采集方法：官方一手材料精读（README 全文 + `npx skills` CLI 文档 + 仓库脚本源码级结构）+ 两篇第三方深度解读 + 社区观点（二传，未直接验证）。

---

## 1. Scope

面向「Codex 上手实战指南」笔记，覆盖用户在 P1 全选的四个方向：

- **A. 技能全景速查**：19 个可触发技能的名称/状态/用途/触发词/运行时依赖/关键文件结构。
- **B. Codex 安装与日常维护**：两条官方安装路线、命令矩阵、frontmatter 名映射、依赖安装、更新/卸载/自动更新。
- **C. 典型科研场景实操**：官方 8 类可复制提示词、技能→场景映射、端到端工作流示例。
- **D. 避坑与最佳实践**：官方明示边界 + 第三方批评 + 社区实操反馈（标注可信度）。

## 2. Source Table

| ID | 标题 | URL | Tier | 抓取/发布日期 | 用途 |
|----|------|-----|------|----------------|------|
| S1 | nature-skills 官方 README（中文） | https://github.com/Yuan1z0825/nature-skills | official | 2026-09-08 抓取 | 定位/理念/安装/技能索引/快速开始/贡献规范 |
| S2 | npx skills CLI 文档（vercel-labs/skills） | https://github.com/vercel-labs/skills | official | 2026-09-08 抓取 | add/list/update/remove 语义、安装路径、排错 |
| S3 | nature-skills 官方在线网站 | https://yuan1z0825.github.io/nature-skills/ | official | unknown | 官方门户（未深抓，仅 P1 探得） |
| S4 | nature-skills README_EN.md | https://github.com/Yuan1z0825/nature-skills/blob/main/README_EN.md | official | 2026-09-08 | 安装命令英文镜像（交叉核对） |
| S5 | 今日开源[45期] nature-skills 项目解读（zhang-yd） | https://www.cnblogs.com/zhang-yd/p/22151100 | implementation-report | 2026-08-02 | Router-style 心智模型、目录结构逐文件拆解、优缺点 |
| S6 | Nature Skills：论文到专利全流程（iTech/itech001） | https://www.cnblogs.com/itech/p/22851434 | implementation-report | 2026-09-05 | 19 技能六类分组、五平台、生态定位 |
| S7 | nature-skills 实测报告（头条） | https://www.toutiao.com/article/7640074589502046746/ | community | unknown（未能抓原文） | 二传：润色 AI 味、绘图一般、多 Draft/Beta |
| S8 | LINUX DO「AI 科研党 skill」讨论串 | https://linux.do/t/topic/2327036/19 | community | unknown（未能抓原文） | 二传：绘图分化、润色冗长、防 AI 率 |
| S9 | skillsmp nature-shared 详情页 | https://skillsmp.com/zh/creators/yuan1z0825/nature-skills/skills-nature-shared | community | unknown | nature-shared 共享依赖旁证（低权威） |

层级统计：official 4 · implementation-report 2 · community 3（其中 2 条未直接验证，记为二传）。
覆盖缺口：S3 站点未深抓；S7/S8 原文未抓取（头条 JS 渲染、linux.do 反爬）；抖音视频教程/知识星球无稳定 URL（仅背景线索）。

---

## 3. Claim / Source Map

### 3.1 项目定位与设计哲学

| 主张 | 来源 |
|------|------|
| nature-skills 是面向全球 AI 学者的可复用科研技能库，围绕 `SKILL.md` 组织；`skills/` 下每个顶层目录是一个可安装单元 | S1 §介绍/§5；S5 |
| 目标 = 「真实问题解决、可验证工作流、可直接使用的科研产物」 | S1；S5；S6 |
| 核心主张：几乎所有实用科研工具可提炼为标准流程，标准流程可封装为可复用技能 | S1 §3.1；S5；S6 |
| 设计被 Google DeepMind 借鉴并推出 Science Skills（作者自述） | S1 §3.1；S6 标注“无论采信程度如何” |
| 5 条共享设计原则：①一手来源优先 ②显式胜过隐式 ③感知章节/任务上下文 ④输出优先 ⑤可扩展 | S1 §7.1；S5 §1.3；S6 |
| 状态标签：Draft（未实战测试）/ Beta（示例测过、边界存疑）/ Stable（真实学术内容验证） | S1 §7.3；S5 |
| 代码协议 Apache-2.0；规模约 18–19 可触发技能 + `nature-shared` 共享包 | S1 徽章；S5 |
| 创始人袁一哲，核心开发者马昕瑞，主要贡献者胡彬；知识星球 + 抖音教程 + 商业代充 | S1 §1；S5 |

### 3.2 架构：Router-style 技能（重要设计洞察）

| 主张 | 来源 |
|------|------|
| 核心架构创新是「static/dynamic split（静态/动态分层）」的 router-style 技能 | S5 §3.1 |
| 目录：`SKILL.md`（路由器，frontmatter+路由协议）、`manifest.yaml`（声明式：axes/always_load/on_demand 映射）、`static/`（core/ + fragments/）、`references/`（含 workflows/）、`scripts/`、`templates/`、`assets/`、中英 README | S5 §3.1/§4.6 |
| manifest.yaml 声明「轴(axes)→文件」映射；SKILL.md 只做路由决策 → 按需只加载相关片段，避免整本巨型 instruction | S5 §3.1/§5.3 |
| 一次调用流程：描述任务 → Agent 匹配 description 触发词 → 读 manifest 与 always_load 核心片段 → 解析轴值（gate，必要时只问用户一个问题并记住偏好）→ 只读匹配 fragments/references → 执行 → 按需跑 scripts → preflight 校验 → 交付产物+来源标注 | S5 §3.2 |
| manifest 路径校验白名单：除 `../nature-shared/` 外不得越出技能目录（`validate-skill-metadata.py` 强制） | S5 §4.2/§5.3 |
| `nature-proposal-writer` 目录 frontmatter name = `researchwrite`（目录名 ≠ 技能名，`npx skills --list` 显示的是 frontmatter name） | S1 §5.1；S5 §4.4 |

### 3.3 Codex 安装与维护（命令矩阵，均经 S1/S2 双重验证）

**路线 1：`npx skills`（vercel-labs/skills CLI，按技能粒度）**

| 操作 | 命令 | 说明/来源 |
|------|------|-----------|
| 查看可安装技能名 | `npx skills add Yuan1z0825/nature-skills --list` | 显示 frontmatter name（S1 §5.1） |
| 全量装到 Codex（全局） | `npx skills add Yuan1z0825/nature-skills --global --agent codex --skill '*' --yes --copy` | 含 nature-shared（S1 §5.1；S6） |
| 单技能装到当前项目 | `npx skills add Yuan1z0825/nature-skills --agent codex --skill nature-figure --yes --copy` | 省略 `--global`（S1 §5.1） |
| 依赖共享包的技能单独装 | `npx skills add ... --global --agent codex --skill nature-reader --skill nature-shared --yes --copy` | reader/paper2ppt/polishing/writing 需带 nature-shared（S1 §5.1；S5） |
| 装到 CLI 支持的所有 agent | `npx skills add Yuan1z0825/nature-skills --all` | S1 §5.1 |
| 检查全局安装 | `npx skills list --global --agent codex --json` | S1 §5.1；S2 |
| 更新 | `npx skills update --global --yes` / `npx skills update nature-reader --global --yes` / `--project` | S1 §5.1；S2 |
| 删除 | `npx skills remove <skill>` / `--global` / `--agent '*'` / `--all` | S2 |
| 项目/全局路径 | 项目 `.agents/skills/`（Codex）；全局 `~/.codex/skills/` | S2 Supported Agents 表 |

关键语义（S2）：`--copy` 复制文件而非 symlink（Windows 无管理员/symlink 受限时推荐）；`--yes` 跳过确认；`--list` 不安装；`--all`=`--skill '*' --agent '*' -y`；私库/凭据走 Git credential / gh / GITHUB_TOKEN。

**路线 2：仓库自带脚本（整库同步，官方 Codex 推荐 §5.3）**

| 操作 | 命令 |
|------|------|
| clone + 全量同步 | `git clone ... && cd nature-skills && scripts/update-codex-skills.sh --pull` |
| 校验一致性 | `scripts/update-codex-skills.sh --check` |
| 同步并清理上游已删技能 | `scripts/update-codex-skills.sh --pull --prune` |
| 只删脚本曾记录、仓库已不存在的目录 | `--prune` 语义（首跑不猜删） |
| 自动更新（SessionStart hook） | `scripts/autoupdate-skills.sh --dest ~/.codex/skills --force` + 合并 `~/.codex/hooks.json` `SessionStart` |

脚本特性（S1 §5.3/S5 §4.2）：update-codex-skills.sh 用 `rsync -a --delete` 只动本仓库技能目录、写清单、`diff -qr` 校验、打印可选 Python 依赖提示；autoupdate-skills.sh 有 6h 节流、断网 exit 0、仅 HEAD 变化才 sync、拒绝有未提交改动的 clone。

**依赖与合规（S1 §5.3、S5 §2.1）**
- Node.js ≥18（npx skills）；Python 3.x 按需；R 可选（nature-figure）；Git 推荐。
- 脚本不会自动装 Python 依赖：`pip install -r skills/nature-paper-to-patent/requirements.txt`；国知局检索可选 `.../disclosure/requirements-cnipa.txt` + `python -m playwright install chromium`；`nature-academic-search` MCP server 需 `pip install -r .../mcp-server/requirements.txt` 并配置 `PUBMED_EMAIL`；Scopus/ScienceDirect 用本机凭据，不写 key 入仓库。
- 安装后开**新 Codex 会话**再自然描述任务。
- **关键规则：保留完整技能目录（SKILL.md + references/ + static/ + manifest.yaml + scripts + nature-shared/），不要只复制 SKILL.md。**（S1 §5.3 明确；Claude Code 路线同理）

### 3.4 技能全景速查（19 个可触发技能）

数据来自 S1 §6 技能索引（状态/用途/触发词），结构补充自 S5 §4.6。

| 目录 | frontmatter 名 | 状态 | 一句话用途 | 典型触发词 | 额外运行依赖/备注 |
|------|------|------|-----------|-----------|------|
| nature-figure | nature-figure | Stable | Python/R 投稿级科研图 + OpenRouter GPT Image 2 论文示意图草稿 | Nature figure/投稿级图片/论文示意图 | R 后端可选；OpenRouter key 用于 AI 示意图；assets/figures4papers demo |
| nature-polishing | nature-polishing | Stable | 学术文本润色/重构/翻译为 Nature 风格英文 | Nature style/润色/academic writing | 4 轴路由(paper_type/section/language/journal)；LaTeX 排版修复 |
| nature-writing | nature-writing | Draft | 起草 Nature 风格手稿章节、重建论证 | 写摘要/写引言/manuscript draft | 写作类 |
| nature-reviewer | nature-reviewer | Draft | 模拟 Nature 审稿人，3 份互盲 reviewer reports + Major/Minor | 预投稿评审/reviewer report | 写作类 |
| nature-citation | nature-citation | Beta | 严格 Nature/CNS 范围支撑文献检索，导出 ENW/RIS/Zotero RDF | CNS citation/支撑文献/Zotero RDF | scripts/nature_citation.py 调 Crossref（免 key） |
| nature-data | nature-data | Draft | Data Availability + 仓储方案 + FAIR 检查 | Data Availability/FAIR | 写作类 |
| nature-statistics | nature-statistics | Draft | 统计报告审查/改写/起草（实验单位/重复/p值/多重比较/效应量/CI） | Nature statistics/统计审查/p value | 写作类 |
| nature-reader | nature-reader | Beta | 带来源锚点、图文对应、公式渲染、中英对照全文 Markdown reader | 全文 Markdown/图文对应/全文翻译 | 读论文核心 |
| nature-paper-card | nature-paper-card | Beta | 单篇精读生成 01–16 节 Paper Card（证据链/结论边界/批判分析） | Paper Card/论文精读/证据链 | docs/nature-paper-card-tutorial.md |
| nature-response | nature-response | Beta | 返修邮件解析：cover letter + 逐点回复 + 标红稿 + LaTeX 模板 | response to reviewers/rebuttal/返修邮件 | 返修季核心 |
| nature-paper2ppt | nature-paper2ppt | Beta | 论文→中文 PPTX 文献汇报 deck | paper PPT/journal club/论文汇报 | 需带 nature-shared |
| nature-image2ppt | nature-image2ppt | Beta | 图片/扫描 PDF/图片型 PPTX→对象级可编辑 PowerPoint + 渲染 QA | 图片转可编辑PPT/扫描PDF转PPTX | 图片类 |
| nature-paper-to-patent | nature-paper-to-patent | Beta | 论文/报告→中国发明专利草稿（专利点挖掘/查新/交底书） | paper to patent/权利要求书/技术交底书 | Playwright chromium；CNIPA 可选；最重技能 |
| nature-ref-verifier | nature-ref-verifier | Stable | 参考文献多源交叉验证（作者/标题/年份/卷期/页码逐字段） | verify refs/文献验证/ref check | 引文可信度 |
| nature-academic-search | nature-academic-search | Beta | 多源检索 + 严格他引审计 + 高影响力引用者画像 + MCP server | 查文献/verify DOI/严格他引 | MCP server：arxiv/crossref/pubmed/sciencedirect/scopus；PUBMED_EMAIL |
| nature-downloader | nature-downloader | Beta | 图书馆/CARSI/开放获取合法获取全文 | 图书馆下载文献/CARSI/PDF 下载 | Node+Python 双实现；账号合规边界 |
| nature-literature-pipeline | nature-literature-pipeline | Stable | 自动化文献发现管线：多源检索→六维评分→精读推送→本地归档 | literature pipeline/每日文献/cron | Stable；可 cron |
| nature-experiment-log | nature-experiment-log | Draft | 实验图文音标准化记录→Obsidian 实验日志 | 实验日志/Obsidian vault/飞书科研群 | Obsidian 场景 |
| nature-proposal-writer | nature-proposal-writer（name=researchwrite） | Beta | proposal-first 科研写作状态机（证据/论证/契约先于文本） | researchwrite/开题报告/科研写作 QA | 写作类；选技能用 researchwrite |

Stable 共 4 个：nature-figure / nature-polishing / nature-ref-verifier / nature-literature-pipeline。其余 15 个为 Beta 或 Draft（S1 §6；S5 §5.2）。

### 3.5 科研场景实操（官方 8 类提示词 + 技能映射）

S1 §4 快速开始「直接这样说」表格 + S6 场景化转写；技能映射为本研究推断（标注为 inference）：

| 想做什么 | 官方提示词模板 | 大概率命中技能（inference） |
|------|------|------|
| 读论文/中英对照 | 把这篇 PDF 做成图文对应的中英文对照 Markdown reader | nature-reader |
| 文献汇报 PPT | 把这篇论文做成中文组会汇报 PPT，保留关键图件和来源标注 | nature-paper2ppt |
| 润色/翻译 | 把这段中文改写成 Nature 风格英文，保持学术含义不变 | nature-polishing |
| 摘要/引言 | 根据这些结果和图件，帮我起草 Nature 风格的摘要和引言 | nature-writing（+nature-polishing） |
| 预投稿审稿 | 从 Nature 审稿人视角评估这篇稿件，给出三份互盲 reviewer reports；全部定稿后再综合 | nature-reviewer |
| 回复审稿意见 | 根据这封返修邮件，为每位互盲审稿人分别写逐点回复和 cover letter，标出修改稿需标红位置 | nature-response |
| 查文献/他引/引用者画像 | 整理这篇文章的引用数、严格他引数、DOI，看引用者里有没有院士/Fellow/大牛 | nature-academic-search（+nature-citation/nature-ref-verifier） |
| 科研图/示意图 | 根据这段方法和结果，帮我生成投稿级科研图或论文示意图草稿 | nature-figure |

端到端工作流示例（S5 §3.3，nature-citation 为「线性参数化工作流」）：文本/claim/DOI → `segment_text()` 分段（≤700 字符）→ Crossref 检索（polite pool+退避）→ `in_scope()` 期刊族过滤（cns/nature/science/cell/flagship）→ 去重 → 导出 ENW/RIS/Zotero RDF → `--with-artifacts` 生成 JSON/TSV/Markdown/可筛选 HTML 浏览器。

路由用法要点（S1 §4/S5 §3.2）：不确定用哪个技能→自然描述任务即可；已确定→在提示词显式写「使用 `nature-reader`/`nature-response`/…」。部分技能带“gate”，必要时只问用户一个问题并记住偏好（如 nature-figure 后端 Python/R：`nature_figure_backend.py set python`）。

### 3.6 避坑与最佳实践

**官方/结构层面明示（高可信）**
- 只复制 SKILL.md 会坏：必须保留整目录（references/static/manifest.yaml/scripts/assets）与 `nature-shared/`（S1 §5.3/§5.4）。
- 运行时依赖不自动安装：Python/Node/Playwright/MCP 需按各技能 README 单独装（S1 §5.3）。
- 技能名用 frontmatter name：`nature-proposal-writer` 目录选技能时叫 `researchwrite`（S1 §5.1）。
- 单独安装依赖共享包的技能会漏：reader/paper2ppt/polishing/writing 需一并装 `nature-shared`（S1 §5.1）。
- 安装后开新会话；Claude Code 不能跑 `scripts/update-codex-skills.sh`（只同步 Codex），需走本地 clone + wrapper 或 `autoupdate-skills.sh --dest`（S1 §5.2/§5.3）。
- 文献下载/检索合规：`nature-downloader` 强调“合法获取”，依赖用户自身图书馆/CARSI/登录态权限（S1 §5.3；S5 §5.2）。

**第三方批评（中高可信，S5 §5.2 / S6）**
- 产出质量高度依赖底层 LLM，存在编造风险；官方用「metadata-only candidate、草稿、不编造数值」等边界自觉缓解，引用/投稿前仍需人工核验（S5 §5.2/§5.3；S6）。
- 成熟度不均：19 个中仅 4 个 Stable，多数 Beta/Draft 未经充分真实学术验证（S5 §5.2）。
- 外部依赖/合规：Scopus/CARSI/OpenRouter 付费 API/Playwright，账号与合规风险由使用者承担（S5 §5.2）。
- README 含代充/知识星球导流广告，对纯技术用户显喧宾夺主（S5 §5.2）。
- 强绑定宿主代理契约：若 Agent “偷懒不读片段”，分层收益失效（S5 §5.2）。

**社区实操反馈（低可信、二传未验证，S7/S8）**
- 润色有「AI 味」、行文冗长；防 AI 率需人为调整句长。
- 绘图质量评价分化（nature-figure）。
- 多数技能 Draft/Beta，需人工把关。
（注明：S7/S8 未能抓取原文，经 P1 检索代理转述，写入笔记时需弱化或标注。）

### 3.7 与同类库对比 & 生态位置（inference 居多）

- 官方未提供与 Matt Pocock Skills / superpowers 的直接对比；生态对比主要在第三方（S6）。S6 观点：skills 生态解决「懂行」，Anthropic 推 Agent Skills 规范后垂直领域技能库成新竞争面；Nature Skills 遵守规范可零适配跑在 5 个平台上（S6）。
- 本库是 vercel-labs/skills 规范下内容厚重、工程化完整的实例（CI 门禁、MCP server、单元测试、双语 README 镜像）（S5 §5.1/§6）。仓库级差异点为「研究」垂直深度，非通用工程 skills。

---

## 4. Contradictions / 分歧

| 分歧点 | 各方说法 | 处理建议 |
|--------|----------|---------|
| 技能数量口径 | S1 徽章=19；README 索引=18 可触发 + nature-shared；S5 §4.4 也写 19 个顶层目录（18+1）；仓库实测 21 个目录 = 20 可触发 + nature-shared？ | 以 README §6 索引表为准（19 行含 researchwrite 等），仓库目录数因含非索引目录有出入；笔记写「约 19 个可触发技能」并注明以 `npx skills --list` 实时为准 |
| 「被 DeepMind 借鉴」 | S1 作者自述；S6「无论采信程度如何」 | 作为作者自述转述，不当作外部实证 |
| 社区评价好坏参半 | S7/S8 反馈 vs 官方/深度解读正面 | 归因到「实操体验因模型/任务而异」，弱化绝对值 |

## 5. Practical Guidance（写给下游章节目）

1. 给 Codex 用户一条「决策树」：只想要 1–3 个技能 → `npx skills` 按需装（记着带 `nature-shared`）；想要整库跟上游 → `update-codex-skills.sh --pull/--check/--prune`；想要长期自动更新 → 专用 clone + SessionStart hook。
2. Windows 用户：装多技能优先 `--copy`（避开 symlink 权限）；`update-codex-skills.sh` 依赖 `rsync`，Windows Git Bash 需确认可用。
3. 每个技能做「最小验证」：装完立刻开新 Codex 会话，丢一句官方模板提示词，确认产物形态（.md/.pptx/.svg/.enw）再进入真实任务。
4. 写作/审稿类技能交付物一律当「草稿 + 引文核验清单」用；引用类（citation/academic-search/ref-verifier）产物交付前过一遍人工/多源核对。
5. 与既有 Obsidian 工作流结合点：`nature-reader`（精读产出 Markdown）与 `nature-experiment-log`（Obsidian 实验日志）产物可直通 vault；可作为笔记「生态结合」章节素材。

## 6. Open Questions / 待验证

- 各技能实际触发稳定性：router 技能对 Codex 的 description 匹配是否可靠 → 需真实会话试跑（可在大纲模式写作时补「实测手记」）。
- `npx skills` 装到 Codex 后技能是被 symlink 还是 copy：Windows 上 `--copy` 的具体表现。
- `nature-academic-search` MCP server 的配置成本与真实检索质量。
- 社区负面反馈（S7/S8）原文无法抓取，写笔记时列为「待用户实测验证」而非结论。
- 官方在线网站（yuan1z0825.github.io）更多交互式导航未抓取。

## 7. Downstream Handoff（给 outline-generator / chapter-writer）

- **可用章节骨架建议**（供大纲参考）：① 项目定位与设计哲学；② 技能全景速查表；③ Codex 安装与维护；④ 科研场景实操提示词与流程；⑤ 避坑与最佳实践；⑥ 上手行动清单 / 生态与进阶。
- **素材强度**：官方安装/技能索引/快速开始——强（一手+已核）；架构/router 心智——强（zhang-yd 基于源码）；社区负面评价——弱（二传）。
- **引用纪律**：写作时区分 official vs implementation-report vs community(二传)；S7/S8 观点需标注「社区反馈，个体体验不一」。
- 本文件已含 claims 与其来源 ID，章节写作无需重抓原始 URL。
