# 使用 academic-research-skills 完成毕业设计 - 意图文件

## 基本信息

- **主题**: 使用 academic-research-skills（ARS）开源项目完成软件类毕业设计（实操指南）
- **项目标识**: academic-research-skills-graduation-guide
- **运行标识**: academic-research-skills-graduation-guide
- **创建时间**: 2026-09-03
- **当前阶段**: 阶段 0（意图澄清）
- **工作流**: learning-note-flow
- **笔记类型**: 实战笔记（实操指南）
- **学习深度**: 上手
- **用户基础**: 有了解（已定毕设题目，会用 Claude Code，尚未系统接触 ARS）
- **输出目标**: obsidian
- **Vault 路径**: 当前 Study-Notes vault（本地）
- **笔记目录**: 待定（阶段 6 前与用户确认）
- **MOC 路径**: 待定

## 学习目标

### 背景

用户正在做**软件/系统开发 + 毕业论文**类毕业设计，目前已定题、**尚未开始系统文献工作**。希望借助 Claude Code 的开源学术研究技能套件 **academic-research-skills（ARS）** 来辅助完成毕设，最终在此笔记库沉淀一份**按毕设阶段组织的实操指南**。

### 笔记类型

实战笔记（如何用 ARS 完成软件类毕设的分阶段实操指南）

### 学习深度

上手（能用、会用、知道每个 skill/命令在毕设哪个阶段起作用、知道边界和坑）

### 用户基础

- 已定题，方向为软件/系统开发 + 毕业论文
- 会使用 Claude Code，了解 agent 技能库概念（本仓库自身就是一套类似体系）
- 未系统接触 ARS；对学术写作规范、引用可信度、查重等有一般了解

### 毕设画像（澄清结论）

| 维度 | 结论 |
|------|------|
| 毕设类型 | 软件/系统开发 + 毕业论文 |
| 当前进度 | 已定题，未开始文献 |
| ARS 角色 | 辅助「文献调研 → 论文写作 → 引用/质量自查」的学术侧；系统开发侧需另配工程工作流 |
| 最终产出 | 在此 vault 内的实操指南笔记 |

## 研究计划

### 探索方向

1. **ARS 全景与定位**：它是什么、解决什么问题、设计理念（human-in-the-loop、integrity gates）、四大 skill 与命令体系、能力边界（不代写、CC BY-NC 许可）。
2. **毕设阶段 × ARS 用法映射**：把「软件类毕设」拆成 选题→文献调研/综述→论文结构→写作→图表与引用→自查/降重前→答辩材料，逐一对照 ARS 的 skill/命令，标出"用在哪、怎么用、不用在哪（如系统开发）"。
3. **实操走查与踩坑**：Windows 环境安装（Claude Code plugin marketplace）、依赖（ANTHROPIC_API_KEY、Pandoc/tectonic、Git Bash、真实 Python），关键命令实测记录，常见坑。

### 重点收集

- **核心概念**: ARS pipeline 阶段划分、human-in-the-loop、integrity gates（7-mode 阻断清单）、Style Calibration、citation trust-chain / locator / L3 claim-faithfulness、deep-research skill、Socratic /ars-plan。
- **实战代码**: `/plugin marketplace add Imbad0202/academic-research-skills` + `/plugin install`；命令 `/ars-plan`、`/ars-lit-review`、`/ars-outline`、`/ars-full`、`/ars-abstract`、`/ars-reviewer`、`/ars-citation-check`、`/ars-format-convert`、`/ars-revision` 等；hooks/agents 可选加固。
- **常见坑**: Windows 上 `python3` 可能是 Microsoft Store 占位符；Git Bash 缺失时 PreToolUse guard 失效；ARS 不代写（学术诚信红线）；授权为 CC BY-NC 4.0（非商用）；引用幻觉仍是高风险（需 ARS_CLAIM_AUDIT / citation-check 把关）。
- **工具链**: Claude Code（v3.7.0+）、ANTHROPIC_API_KEY、可选 Pandoc(DOCX)/tectonic(PDF)、Git Bash、真实 Python、Obsidian（本笔记最终落点）。

### 信源偏好

- 官方文档: 是（README / README.zh-CN / QUICKSTART / docs/ARCHITECTURE.md / docs/SETUP.md / MODE_REGISTRY.md）
- 技术博客: 否（缺针对该库的中文深度博客，以官方为准）
- 社区讨论: 是（GitHub issues / 讨论区，了解真实使用反馈）
- 学术论文: 是（ARS 引用的 Lu et al. 2026 Nature、Zhao et al.、Ren et al. 等作为理念背景，不必深入）

## 备注

1. 最终产物按「毕设阶段」组织，让用户拿到就能对着自己当前阶段（文献调研）直接操作。
2. 需明确区分：ARS **管不了系统开发部分**，指南里要给出"开发 + 学术"两条线如何配合的建议。
3. 因本仓库（Study-Notes 学习系统）与 ARS 都是 agent 技能体系，指南可适当做"概念映射"，帮助用户快速上手。
4. 输出到 Obsidian：note_folder 与 MOC 路径在阶段 6 发布前与用户确认，不写死绝对路径。
5. 使用 ARS 前确认符合所在学校对 AI 辅助写作的规范（ARS 官方立场：辅助不代写，需如实披露）。
