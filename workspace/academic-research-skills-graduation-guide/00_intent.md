# 使用 academic-research-skills + nature-skills 完成软件类毕业设计 - 意图文件

## 基本信息

- **主题**: 使用 academic-research-skills（ARS）+ nature-skills 两个开源项目完成软件类毕业设计（按毕设阶段混排的组合实操指南）
- **项目标识**: academic-research-skills-graduation-guide（沿用原 slug；方向调整新增 nature-skills）
- **运行标识**: academic-research-skills-graduation-guide
- **创建时间**: 2026-09-03
- **最近更新**: 2026-09-03
- **当前阶段**: 阶段 0（意图澄清）
- **工作流**: learning-note-flow
- **笔记类型**: 实战笔记（双库组合实操指南）
- **学习深度**: 上手
- **用户基础**: 有了解（已定毕设题目，会用 Claude Code；已规划 ARS，新增 nature-skills）
- **输出目标**: obsidian
- **Vault 路径**: 当前 Study-Notes vault（本地）
- **笔记目录**: 待定（阶段 6 前与用户确认）
- **MOC 路径**: 待定

## 学习目标

### 背景

用户正在做**软件/系统开发 + 毕业论文**类毕业设计，目前已定题、**尚未开始系统文献工作**。希望借助两个 agent 开源技能套件辅助完成毕设：

1. **academic-research-skills（ARS，Imbad0202）**：学术研究全流程辅助（深度研究 → 综述 → 大纲 → 写作 → 审稿自查），强在 human-in-the-loop 与 integrity gates（学术诚信把关）、citation trust-chain。
2. **nature-skills（Yuan1z0825/nature-skills）**：Nature 风格学术写作与科研绘图（`nature-polishing`、`nature-figure`、`nature-ref-verifier`、`nature-literature-pipeline`、`nature-reviewer`、`nature-paper2ppt` 等约 19 个技能 + 共享包），Apache-2.0，覆盖面广、输出优先。

最终在此笔记库沉淀一份**按毕设阶段组织的组合实操指南**：每个阶段列出「该用哪个库的哪些技能」，两库互补、**不设主次**。

### 笔记类型

实战笔记（双库组合实操指南，按毕设阶段混排）

### 学习深度

上手（能用、会用、知道每个 skill/命令在毕设哪个阶段起作用、知道边界和坑）

### 用户基础

- 已定题，方向为软件/系统开发 + 毕业论文
- 会使用 Claude Code，了解 agent 技能库概念（本仓库自身就是一套类似体系）
- 未系统接触 ARS 与 nature-skills
- 对学术写作规范、引用可信度、查重等有一般了解

### 毕设画像（澄清结论）

| 维度 | 结论 |
|------|------|
| 毕设类型 | 软件/系统开发 + 毕业论文 |
| 论文语言 | 中文（毕业设计论文，需 GB/T 7714 中文参考文献等适配） |
| 当前进度 | 已定题，未开始文献 |
| ARS 角色 | 学术全流程 + 诚信把关（深度研究、综述、大纲、写作、审稿自查） |
| nature-skills 角色 | Nature 风格写作/润色、出版级科研绘图、文献流水线、引用核查、答辩/汇报 PPT 等 |
| 组织方式 | 按毕设阶段混排，双库互补、不设主次 |
| 开发侧 | 两者均不覆盖系统开发；需另配工程工作流 |
| 最终产出 | 在此 vault 内的实操指南笔记 |

## 研究计划

### 探索方向

1. **两库全景与定位对比**：各是什么、解决什么问题、设计理念（ARS: human-in-the-loop / integrity gates / 7-mode 阻断清单；nature-skills: 5 条共享原则、router-style SKILL.md、输出优先、技能成熟度 Draft/Beta/Stable）、许可差异（ARS CC BY-NC 4.0 vs nature-skills Apache-2.0）、生态差异（ARS 为 Claude Code 插件；nature-skills 以 Codex 为主、可适配 Claude Code/Cursor 等）。
2. **毕设阶段 × 两库技能映射**：把「软件类毕设」拆成 选题→文献调研/综述→论文结构→写作→图表→引用→自查/降重前→答辩材料，逐一对照 ARS 与 nature-skills 的 skill/命令，标出「用哪个、怎么用、不用在哪」（如系统开发、查重、学校格式）。重点覆盖 nature-skills 明显补强处：科研绘图、答辩/开题/结题 PPT、Nature 表达润色。
3. **中文毕设适配**：两库官方文档与默认流水线偏英文/APA 体系；指南须专门核实并说明中文毕设适配点——GB/T 7714 中文参考文献格式支持、中文排版（字体/PDF/DOCX）、输出语言设置、查重/降重语境下的定位，以及哪些环节可直接用、哪些需人工改造成中文。
4. **实操走查与踩坑**：Windows 环境安装两条路线（ARS: Claude Code plugin marketplace；nature-skills: `git clone` + `scripts/update-codex-skills.sh` 或 `npx skills add`，并给出 Claude Code 适配），依赖（ANTHROPIC_API_KEY、Pandoc/tectonic、Git Bash、真实 Python、可选 MCP/浏览器），关键命令实测记录，常见坑。

### 重点收集

- **核心概念**: ARS pipeline 阶段划分、human-in-the-loop、integrity gates（7-mode 阻断清单）、Style Calibration、citation trust-chain / locator / L3 claim-faithfulness、deep-research skill、Socratic `/ars-plan`；nature-skills router-style `SKILL.md`、5 shared principles、`nature-shared` 共享包、技能成熟度标签、output-first。
- **实战代码/命令**: ARS：`/plugin marketplace add Imbad0202/academic-research-skills` + `/plugin install`；`/ars-plan`、`/ars-lit-review`、`/ars-outline`、`/ars-full`、`/ars-abstract`、`/ars-reviewer`、`/ars-citation-check`、`/ars-format-convert`、`/ars-revision` 等；hooks/agents 可选加固。nature-skills：安装命令（git clone + update 脚本 / `npx skills add`）、按技能触发示例（figure / polish / ref-verifier / literature-pipeline / citation / reader / reviewer / paper2ppt 等）、**保持 references/static/manifest.yaml/scripts/_shared 全目录结构**。
- **常见坑**: Windows 上 `python3` 可能是 Microsoft Store 占位符；Git Bash 缺失时 PreToolUse guard 失效；nature-skills 不能只拷 `SKILL.md`（必须保留全目录与共享包）；ARS 与 nature-skills 都不代写（学术诚信红线）；学校对 AI 辅助写作的披露规范；引用幻觉仍属高风险（需 ARS_CLAIM_AUDIT / citation-check / nature-ref-verifier 把关）；许可差异对毕设（是否开源/商用）的影响；中文 GB/T 7714 与英文 APA 的差异。
- **工具链**: Claude Code（v3.7.0+，可选 Codex）、ANTHROPIC_API_KEY、可选 Pandoc(DOCX)/tectonic(PDF)、Git Bash、真实 Python、可选 MCP（如 nature-academic-search）、Obsidian（本笔记最终落点）。

### 信源偏好

- 官方文档: 是（ARS: README / README.zh-CN / QUICKSTART / docs/ARCHITECTURE.md / docs/SETUP.md / MODE_REGISTRY.md；nature-skills: README / README_EN / 各 SKILL.md / manifest.yaml）
- 技术博客: 是（nature-skills 已有中文解读；ARS 缺针对该库的中文深度博客，以官方为准）
- 社区讨论: 是（GitHub issues / 讨论区 / awesome-skills 聚合站）
- 学术论文: 是（ARS 引用的 Lu et al. 2026 Nature、Zhao et al.、Ren et al. 等，以及 Nature 风格背景，不必深入）

## 备注

1. 最终产物按「毕设阶段」组织，形成一张端到端路线图，让用户拿到就能对着自己当前阶段（文献调研）直接操作。
2. 两库互补不设主次，但需在指南中给出明确分工建议，避免用户对重叠功能（写作/综述/审稿/引用）选择困难。
3. nature-skills 以 Codex 为第一 runtime，需给出到 Claude Code 的适配步骤或等价用法；ARS 的 integrity gates 与 nature-skills 的引用核查可作双保险。
4. 明确两库都管不了系统开发部分，指南要给出「开发 + 学术」两条线如何配合的建议。
5. 因本仓库（Study-Notes 学习系统）与两库都是 agent 技能体系，指南可适当做「概念映射」，帮助用户快速上手。
6. 输出到 Obsidian：note_folder 与 MOC 路径在阶段 6 发布前与用户确认，不写死绝对路径。
7. 使用前确认符合所在学校对 AI 辅助写作的规范（两库官方立场均为辅助不代写，需如实披露）。
8. **论文语言为中文**：两库默认流程偏英文/APA 体系，指南须专门核实并说明中文毕设使用时的适配点——GB/T 7714 中文参考文献格式支持、中文排版（字体/PDF/DOCX）、输出语言设置、查重/降重语境下的定位，以及哪些环节可直接用、哪些需人工改造成中文。
