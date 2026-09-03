# 双库毕设指南 - 探测式收集结果（P1）

- 运行: academic-research-skills-graduation-guide（learning-note-flow, P1）
- 主题: 使用 academic-research-skills（ARS）+ nature-skills 完成软件类毕业设计（按毕设阶段混排的组合实操指南）
- 日期: 2026-09-03

## 探测视角与候选信源

### 视角 1：nature-skills 全景、技能体系、安装与 Claude Code 适配

| # | 标题 | URL | 层级 | 日期 | 评分 |
|---|------|-----|------|------|------|
| 1 | 官方 GitHub 仓库 README（中文） | https://github.com/Yuan1z0825/nature-skills | 官方文档 | 2026（持续更新） | 5 |
| 2 | 官方英文 README_EN | https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/README_EN.md | 官方文档 | 2026 | 4 |
| 3 | DeepWiki · Getting Started & Skill Index | https://deepwiki.com/Yuan1z0825/nature-skills/1.1-getting-started-and-skill-index | 权威聚合 | 2026-06-23 | 4 |
| 4 | Agent Skill Marketplace 条目 | https://agentskillexchange.com/skills/run-nature-style-academic-writing-and-figure-workflows-with-nature-skills/ | 权威聚合 | 2026-05-21 | 3 |
| 5 | CSDN《Nature-Skills 详细使用手册》（中文） | https://devpress.csdn.net/xclaw/6a114fa9662f9a54cb768bf7.html | 社区经验 | n/a | 3 |

要点：19 技能（Stable 4 / Beta 10 / Draft 5）+ `nature-shared`；安装三路线（git clone + update 脚本 / `npx skills add` / Claude wrapper）；必须保留 references/static/manifest/scripts 全目录；Apache-2.0。

### 视角 2：ARS 命令体系、中文毕设适配、与 nature-skills 的关系

| # | 标题 | URL | 层级 | 日期 | 评分 |
|---|------|-----|------|------|------|
| 1 | academic-research-skills 官方 README | https://github.com/Imbad0202/academic-research-skills | 官方文档 | 2026 (v3.21.x) | 5 |
| 2 | MODE_REGISTRY.md（27 模式 / 命令映射） | https://github.com/Imbad0202/academic-research-skills/blob/main/MODE_REGISTRY.md | 官方文档 | n/a | 4 |
| 3 | 官方简体中文 README.zh-CN.md | https://github.com/Imbad0202/academic-research-skills/blob/main/README.zh-CN.md | 官方文档 | 2026 | 4 |
| 4 | Hacker News 讨论 #48083919 | https://news.ycombinator.com/item?id=48083919 | 社区经验 | n/a | 4 |
| 5 | 知乎《别指望 AI 代写论文》 | https://zhuanlan.zhihu.com/p/2040194533716123781 | 社区经验 | n/a | 3 |

要点：四技能/25+ 模式、7 类 AI 失败模式诚信闸门（Stage 2.5/4.5）、citation trust-chain、Style Calibration；**官方未支持 GB/T 7714，默认 APA 7.0（含中文引文规则）**，中文样例为 LaTeX 编译 PDF 而非 DOCX，无本科学位论文专用流程。

### 视角 3：中文软件类毕设 × AI 学术写作合规与工具链

| # | 标题 | URL | 层级 | 日期 | 评分 |
|---|------|-----|------|------|------|
| 1 | GB/T 7714-2015《参考文献著录规则》 | https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=7714&p.p90=circulation_date&p.p91=desc | 官方文档 | 2015-12-01 实施 | 5 |
| 2 | 《人工智能生成合成内容标识办法》GB 45438-2025 | https://www.gov.cn/zhengce/zhengceku/202503/content_7014286.htm | 官方文档 | 2025-09-01 施行 | 5 |
| 3 | 新华社：高校发布"AI 禁令"评论综述 | https://www.news.cn/comments/20250114/06fc90bcbc784964b916a58b06ab2ba4/c.html | 权威聚合 | 2025-01-14 | 4 |
| 4 | Claude Code Plugins Reference | https://code.claude.com/docs/zh-TW/plugins-reference | 官方文档 | n/a | 5 |
| 5 | pandoc-latex-template Issue #140（中文文档问题） | https://github.com/Wandmalfarbe/pandoc-latex-template/issues/140 | 社区经验 | n/a | 3 |

要点：GB/T 7714-2015 是中文学位论文著录底层依据；2025 起国家层面 AI 生成内容标识 + 高校 AI 披露/查重政策收紧；Claude Code 的 plugin marketplace 与 `SKILL.md → .claude/skills` 是两库现实安装分叉的关键。

## 方向菜单

请选择 P2 深度收集与成文时**侧重哪个维度**（结构仍按毕设阶段混排）：

- **方向 A：端到端毕设路线图为主（推荐）**
  重心放在「毕设阶段 × 双库技能映射」：每阶段给出用哪个库的哪些技能、触发命令/提示词、人工检查点与输出物；安装与中文适配作为支撑章节从轻。
- **方向 B：安装与 Claude Code 适配为主**
  先跑通两库：Windows 安装、目录结构、Claude Code wrapper/插件、依赖与踩坑；用法映射从简。
- **方向 C：中文毕设适配为主**
  侧重中文落地的改造量：GB/T 7714、中文 DOCX/PDF 输出、学校 AI 规范与查重语境下哪些环节可直接用、哪些必须改。
- **方向 D：三者均衡**
  路线图为主线、安装与中文适配各占一章，篇幅均分。

## 覆盖缺口（Gaps）

- nature-skills 各 SKILL.md 内部规则与版本未逐技能核读；Claude Code wrapper 缺第三方实操验证。
- ARS × nature-skills 无官方直接对比材料，互补关系需自行梳理。
- ARS 官方缺 GB/T 7714 与中文 DOCX 模板支持，需实测或靠 community 适配版。
- tectonic 中文 CJK 配置、各校查重/AIGC 阈值差异、AI 使用声明表范本、单一学校 Word 模板字段待结合目标院校核验。

## 预估 P2 范围

- 核心源约 8–10 个：nature-skills README/README_EN + 4–6 个关键 SKILL.md；ARS README/zh-CN/MODE_REGISTRY；GB/T 7714、AI 标识办法、Claude Code Plugins Reference。
- 补充源 3–5 个：DeepWiki、HN 讨论、知乎/CSDN 中文经验、pandoc 中文 issue。
- 输出 `02_deep_research.md`：范围、源表、主张↔信源映射、矛盾点、实操指引、未决问题、下游交接。
