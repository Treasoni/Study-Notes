---
title: 用 academic-research-skills + nature-skills 完成软件类毕业设计（实操指南）
type: 学习笔记大纲
status: 待用户确认
source_project: academic-research-skills-graduation-guide
workflow_phase: P3
---

# 学习笔记大纲：《用 academic-research-skills + nature-skills 完成软件类毕业设计（实操指南）》

> - **笔记类型**：实战笔记（双库组合实操指南，按毕设阶段混排，两库互补不设主次）
> - **预计总篇幅**：约 2.0 万–2.5 万字（成稿正文）
> - **章节数**：11 章 + 「学习路径说明」
> - **目标读者**：已定题、会用 Claude Code 的中文软件类毕设生（深度：上手）
> - **结构组织**：第一部分「准备篇」（全景 + 安装）→ 第二部分「毕设主线」（按阶段走查）→ 第三部分「合规与收尾」
> - **重叠区约定**：综述 / 写作 / 审稿 / 引用是两库功能重叠区，每处用 `【重叠区①-④】` 标记，并给出「主用哪套、另一套怎么补」的去重建议，避免选择困难
> - **素材引用格式**：`§x.y` 指 `02_deep_research.md` 第 x 节第 y 小节；`N-* / A-* / GB / CN-AI / CC-P / PD` 指该文件「源表」中的源 ID
> - **行文语言**：中文（代码/命令保留原文）

---

## 第一部分　准备篇：先看清地图，再装好工具

### 第一章：双库全景与分工总览——一张图看懂「何时用哪套」

- **篇幅**：长（约 2500–3000 字）
- **定位**：全书入口；先建立「两库互补、不设主次」的全局心智模型，并给出贯穿后文的去重总表
- **双库分工建议**：是（全局分工总表；预告 4 个重叠区及各自去重章节）
- **计划小节**：
  - 1.1 为什么是「双库组合」：ARS = 学术全流程 + 诚信闸门；nature-skills = Nature 风格写作/绘图/文献/引用核查/PPT，输出优先
  - 1.2 nature-skills 全景：19 个可触发技能 + `nature-shared` 共享支持包；成熟度 Draft/Beta/Stable；Apache-2.0；router 式 SKILL.md 与 5 条共享原则（§3.1）
  - 1.3 ARS 全景：4 技能 / 27 模式 + 约 10 个 `/ars-*` 命令；Fidelity/Balanced/Originality 监督档；integrity gates 7 类阻断式检查；citation trust-chain（§3.4）
  - 1.4 毕设全流程分工总表：选题→开题→文献→综述→大纲→写作→图表→引用→审稿→答辩 × 主责库 × 推荐技能 × 边界
  - 1.5 重叠区预告与去重策略：综述/写作/审稿/引用分别「主用谁、另一套怎么补」，并指向第 4/6/8/9 章
  - 1.6 指南边界：两库都不覆盖系统开发与查重 → 「开发线 + 学术线」双轨配合建议
  - 1.7 概念映射（可略读）：ARS/nature-skills 与本仓库 Study-Notes 技能体系的类比
- **素材引用**：§3.1、§3.4、§3.6、§五 ｜ N-R、N-RE、A-R、A-ZH、A-M
- **命令/代码示例**：无（表格与文字为主）
- **本章产物**：一张可打印的「毕设全流程 × 两库技能分工表」
- **读者行动项/检查点**：
  - [ ] 用 1.4 总表对照自己当前进度，圈出接下来 3 步要用的技能
  - [ ] 确认两库许可对你的影响（ARS CC BY-NC 4.0 非商用 vs nature-skills Apache-2.0）

### 第二章：安装与 Claude Code 适配（Windows 实测路线）

- **篇幅**：中-长（约 2000–2500 字）
- **双库分工建议**：否（纯安装，但需同时装两套并打通 Claude Code）
- **计划小节**：
  - 2.1 安装前检查清单：Claude Code v3.7.0+、`ANTHROPIC_API_KEY`、Git、真实 Python（避开 Microsoft Store 占位符）；可选：Pandoc/tectonic、Git Bash、MCP（§3.2、§3.7、A-DOC）
  - 2.2 ARS 安装（插件市场路线）：`/plugin marketplace add Imbad0202/academic-research-skills` + `/plugin install`；更新与本地缓存机制（CC-P、A-ZH）
  - 2.3 nature-skills 安装（Codex 原生路线）：`git clone` + `scripts/update-codex-skills.sh`；或 `npx skills add`（Node 18+）（N-RE）
  - 2.4 nature-skills → Claude Code 适配：为何不能用 Codex 脚本；wrapper 法（稳定 clone + slash-command/subagent 指向真实 `skills/*/SKILL.md`）vs SessionStart hook 复制法；硬规则 = **保留完整目录结构**（references/static/manifest.yaml/scripts/_shared/nature-shared），只拷 SKILL.md 会坏依赖（N-RE、N-DOC）
  - 2.5 装完验证：触发 `/ars-plan`、确认 nature 技能可被发现、跑最小 smoke test
  - 2.6 Windows 踩坑清单：`python3` 占位符、Git Bash 缺失致 guard 失效、路径/空格问题、LaTeX 引擎缺字
- **素材引用**：§3.2、§3.7、§3.6 ｜ N-RE、N-DOC、A-ZH、CC-P
- **命令/代码示例**：有（marketplace add/install、git clone、npx skills add、update-codex-skills.sh、wrapper/SessionStart hook 配置片段、验证命令）
- **本章产物**：可运行的双库环境 + 一张「已装/缺什么」验证清单
- **读者行动项/检查点**：
  - [ ] 两条安装路线各完成一次，且 smoke test 通过
  - [ ] 记录本机缺失的可选依赖，标记后续第 11 章格式转换前补齐

---

## 第二部分　毕设主线：按阶段走查（选题 → 答辩）

### 第三章：定题深化与开题报告——把题目收窄到可写

- **篇幅**：短-中（约 1200–1600 字）
- **双库分工建议**：否（主线章节，非重叠区；ARS 主导）
- **计划小节**：
  - 3.1 ARS `/ars-plan`：苏格拉底式提问，界定研究问题、范围与方法（A-R、A-M）
  - 3.2 nature-proposal-writer：开题报告状态机草稿；注意其成熟度（Beta/Draft）需人工校对（§五、N-R）
  - 3.3 从题目到开题四件套：研究问题 / 文献缺口 / 方法路线 / 双轨进度表（学术线 + 开发线里程碑）
  - 3.4 中文适配：开题报告通常按校方 Word 模板填写，AI 草稿需人工改写并在导师沟通中如实说明
- **素材引用**：§3.4、§3.5、§五 ｜ A-R、A-ZH、A-M、N-R
- **命令/代码示例**：有（`/ars-plan` 触发示例、nature-proposal-writer 触发示例）
- **本章产物**：一页研究问题陈述 + 开题报告草稿 + 双轨进度表
- **读者行动项/检查点**：
  - [ ] 与导师确认收窄后的题目边界与工作量
  - [ ] 核对校方开题模板是「AI 草稿可导入」还是「纯手工填写」

### 第四章：文献调研与综述 `【重叠区①：综述】`

- **篇幅**：长（约 2200–2800 字）
- **双库分工建议**：是 —— **主用 ARS 做问题驱动综述**（`/ars-lit-review`，走诚信闸门）；**nature-literature-pipeline 做文献条目批量采集/筛选**；中文文献核验提前接第 8 章 ref-verifier
- **计划小节**：
  - 4.1 ARS `deep-research`（8 模式）与 `/ars-lit-review`：综述生成 + Stage 2.5 诚信闸门（A-R、A-ZH、A-M）
  - 4.2 nature-literature-pipeline（Stable）：批量文献采集/筛选流水线；可选 nature-academic-search MCP 增强（§五、N-R）
  - 4.3 中文文献怎么进流程：CNKI/万方/知网导出 → `.bib`/EndNote 预处理；nature-ref-verifier 支持 CNKI/万方多源核验（预告第 8 章）（N-RV）
  - 4.4 综述引用锚：每个关键 claim 落到具体文献编号，不留「孤儿 claim」（衔接 L3 claim-faithfulness）
  - 4.5 「用哪套」决策表：什么场景走 ARS 综述、什么场景走 nature 流水线、两者如何接力
- **素材引用**：§3.3、§3.4、§3.5、§五 ｜ A-R、A-ZH、A-M、N-R、N-RV
- **命令/代码示例**：有（`/ars-plan` → `/ars-lit-review`、literature-pipeline 触发命令）
- **本章产物**：带引用锚的综述章节草稿 + 可检索的文献库（Zotero/EndNote）
- **读者行动项/检查点**：
  - [ ] 综述中所有「据 XX 研究」均有编号引用，无孤儿 claim
  - [ ] 确定主文献管理工具，统一导入与导出格式（为第 8/11 章做准备）

### 第五章：论文结构与大纲——把校方模板装进 ARS 大纲

- **篇幅**：短-中（约 1200–1600 字）
- **双库分工建议**：否（ARS 主导；nature-skills 无对应技能，说明边界即可）
- **计划小节**：
  - 5.1 `/ars-outline` 用法：从综述到章节大纲（A-R、A-M）
  - 5.2 ARS 支持的结构 vs 软件毕设结构：IMRaD / 主题综述 / 理论分析等；**无本科学位论文专用流程** → 需人工映射到校方模板（A-ZH、§四-4）
  - 5.3 软件类毕设大纲骨架：需求 / 设计 / 实现 / 测试章节占位，与系统开发产物对齐（避免空写「实现」）
  - 5.4 中文结构调整：简化字、图表目录、校方章节编号规则
- **素材引用**：§3.4、§3.5、§四(4) ｜ A-R、A-ZH、A-M
- **命令/代码示例**：有（`/ars-outline`）
- **本章产物**：一份与校方模板对齐的全文大纲（每章含要点与预估字数）
- **读者行动项/检查点**：
  - [ ] 大纲经导师确认后再进入正文写作
  - [ ] 把「实现」章节章节号对应到真实代码提交/模块，保证可写实

### 第六章：正文写作与润色 `【重叠区②：写作】`

- **篇幅**：长（约 2500–3200 字）
- **双库分工建议**：是 —— **ARS 写初稿并走 integrity gates**；**nature-polishing 只用于英文摘要/英文表达润色**（面向英文 Nature 风格，对中文正文不直接适用 → 中文正文以人工改写为主）；学术诚信红线两库一致
- **计划小节**：
  - 6.1 `/ars-full` 生成 IMRaD 初稿；`/ars-abstract` 双语摘要（中文 + English）（A-R、A-ZH、A-M）
  - 6.2 Style Calibration：提供 3+ 篇范文学习风格（A-R）
  - 6.3 integrity gates 7 类阻断：Stage 2.5/4.5 运行、验证 MANDATORY、覆写须记录理由（A-R、A-ZH）
  - 6.4 nature-polishing 细节：目标/路由/layout 排版检查、依赖 LaTeX 工具链目检、保留事实与引用意图（N-P）
  - 6.5 学术诚信与「不代写」边界：两库均不代写、不掩饰 AI 使用；无法证明数据真实 → 数据须自行实验采集（A-ZH、§四-3）
  - 6.6 中文适配：ARS 默认繁体中文 → 简体转换；中文学位论文的语气/章节粒度调整
- **素材引用**：§3.3、§3.4、§3.5、§四(3) ｜ A-R、A-ZH、A-M、N-P
- **命令/代码示例**：有（`/ars-full`、`/ars-abstract`、`ARS_CLAIM_AUDIT=1`、nature-polishing 触发）
- **本章产物**：通过闸门的初稿 + 英文摘要润色稿 + AI 使用声明草稿
- **读者行动项/检查点**：
  - [ ] integrity gates 全部跑过；异常项逐条写覆写理由
  - [ ] 英文摘要润色稿回填中文稿后，术语中英一一对应

### 第七章：科研图表与系统插图——用 nature-figure 画出「投稿级」图

- **篇幅**：中（约 1500–2000 字）
- **双库分工建议**：否（ARS 无绘图对应 → 明确「这阶段只靠 nature-skills」的边界）
- **计划小节**：
  - 7.1 nature-figure 定位与成熟度（Stable）：matplotlib/seaborn 或 R ggplot2，输出 SVG/PDF/TIFF（N-F）
  - 7.2 一张图的产出流程：数据 → 图 → 强制 QA（collision audit / validation），不达标阻止交付（N-F）
  - 7.3 AI schematic 路线（OpenRouter GPT Image）适用场景与使用边界（N-F）
  - 7.4 软件类毕设插图补充：架构图 / ER 图 / 界面截图用常规绘图工具（两库不覆盖系统开发图示）
  - 7.5 中文图注与字号规范：按校方模板对齐
- **素材引用**：§3.3(N-F)、§五 ｜ N-F、N-R
- **命令/代码示例**：有（Python/R 绘图代码骨架、QA 报告输出示例）
- **本章产物**：2–4 张论文可用图（算法对比/结果/架构示意图）
- **读者行动项/检查点**：
  - [ ] 每张图通过 QA（无碰撞、分辨率/字号达标）
  - [ ] 图注中英文与正文引用图号一致

### 第八章：引用自查双保险 `【重叠区③：引用】`

- **篇幅**：中（约 1800–2200 字）
- **双库分工建议**：是 —— **ARS 查「该引的引了且被 claim 支撑」**（信任链 + 存在性核验）；**nature-ref-verifier 查「条目信息本身对不对」**（多源交叉验证）；两套都跑一遍作双保险
- **计划小节**：
  - 8.1 ARS citation trust-chain：provenance frontmatter + locator 三层锚 + L3 claim-faithfulness（`ARS_CLAIM_AUDIT=1`）（A-R、A-ZH）
  - 8.2 `/ars-citation-check` 与确定性存在性查验：Semantic Scholar / OpenAlex / Crossref / arXiv（A-R）
  - 8.3 nature-ref-verifier：DOI → `api.crossref.org` 优先；Crossref/IEEE/CNKI/万方/Zotero；🔴Critical/🟡Warning/🟢Info 报告；修正 `.bib` + Zotero 修复命令；依赖可降级（pyzotero 推荐）（N-RV）
  - 8.4 两库分工不重复：查「声称被文献支撑」归 ARS；查「文献元数据正确」归 nature-ref-verifier
  - 8.5 中文引用格式缺口：citation_format_switcher 覆盖 APA/Chicago/MLA/IEEE/Vancouver 但**不含 GB/T 7714** → 转交第 11 章外挂模板处理（A-ZH、§四-1）
- **素材引用**：§3.3(N-RV)、§3.4、§3.5、§四(1)、§五 ｜ A-R、A-ZH、N-RV
- **命令/代码示例**：有（`ARS_CLAIM_AUDIT=1` 运行、`/ars-citation-check`、nature-ref-verifier 命令与分级报告片段）
- **本章产物**：引用自查报告（🔴 Critical 清零）+ 修正后的参考文献库
- **读者行动项/检查点**：
  - [ ] 🔴 Critical 全部处理，🟡 Warning 逐个确认
  - [ ] L3 claim 审计无「引用了但无支撑」项
  - [ ] 确认文献库最终导出样式切换为 GB/T 7714（执行第 11 章）

### 第九章：模拟审稿与修改 `【重叠区④：审稿】`

- **篇幅**：中（约 1600–2000 字）
- **双库分工建议**：是 —— **ARS 主审**（结构化：5 份审稿报告 + 编辑决定 + 修改路线）；**nature-reviewer 作第二意见**（成熟度 Draft/Beta，谨慎采信）
- **计划小节**：
  - 9.1 `/ars-reviewer`：5 份审稿报告 + 编辑决定 + 修改路线；`academic-paper-reviewer` 6 模式（A-R、A-M）
  - 9.2 `academic-pipeline`（10 阶段调度器）与审稿/修改环节的衔接（A-R、A-M）
  - 9.3 nature-reviewer：Nature 风格审稿视角；成熟度 Draft → 仅作补充意见（§3.1、§四-4）
  - 9.4 按审稿意见改稿：`/ars-revision` 修改稿 + 逐点回复；或对中文稿人工修改后复跑自查
  - 9.5 提交前合并清单：integrity gates + 审稿意见 + 引用自查 → 一条 checklist
- **素材引用**：§3.1、§3.4、§四(4)、§五 ｜ A-R、A-ZH、A-M、N-R
- **命令/代码示例**：有（`/ars-reviewer`、`/ars-revision`、nature-reviewer 触发）
- **本章产物**：审稿意见汇总 + 修改路线图 + 逐点回复表
- **读者行动项/检查点**：
  - [ ] 对每条 major/minor 意见给出「已改 / 反驳理由」
  - [ ] 改稿后复跑第 8 章引用自查，确认未引入新问题

### 第十章：答辩材料——用 nature-paper2ppt 把论文变成汇报

- **篇幅**：短-中（约 1200–1600 字）
- **双库分工建议**：否（ARS 无对应 → 明确「答辩 PPT 只用 nature-skills」的边界）
- **计划小节**：
  - 10.1 nature-paper2ppt 定位：论文 → PPT 草稿；成熟度与输入输出格式确认（N-R、§五）
  - 10.2 从草稿到汇报：按「1 页 1 要点」删减 + 写讲稿
  - 10.3 软件类毕设答辩 PPT 结构：背景/问题 → 方案 → 实现亮点（配真实截图/图表）→ 实验 → 总结展望
  - 10.4 复用：开题/中期/结题汇报走同一流程
- **素材引用**：§3.1、§五 ｜ N-R、N-RE
- **命令/代码示例**：有（nature-paper2ppt 触发示例）
- **本章产物**：答辩 PPT 草稿 + 讲稿要点
- **读者行动项/检查点**：
  - [ ] 答辩前用导师/同学做一次模拟提问（可配合第 9 章审稿清单）
  - [ ] 确认校方 PPT 模板与页数/时长限制

---

## 第三部分　合规与收尾：让论文「交得上去」

### 第十一章：中文格式落地、GB/T 7714 与查重边界

- **篇幅**：中-长（约 2000–2600 字）
- **双库分工建议**：是（集中回答中文合规——两库默认流程均偏英文/APA，需外挂人工环节；明确查重两库都不管）
- **计划小节**：
  - 11.1 GB/T 7714-2015 要点：顺序编码制；学位论文 `[D]`；电子资源双标 `[J/OL]`/`[EB/OL]` + 引用日期与路径；DOI 著录项；作者 ≤3 全列、>3 前 3 +「等」（GB）
  - 11.2 两库的格式缺口与补救：ARS 默认 APA 7.0 中文扩展、`citation_format_switcher` 无 GB/T 7714；nature-academic-search 同样无 → 外挂 EndNote/Zotero 官方 GB/T 7714 样式或校方 Word 模板（A-ZH、§四-1、GB）
  - 11.3 中文 DOCX/PDF 转换：Pandoc `--pdf-engine=xelatex` + `CJKmainfont`/xeCJK（默认 pdflatex 不支持中文）；ARS 的 MD + DOCX + LaTeX(apa7) → tectonic 链路的中文注意点；禁用 HTML-to-PDF（PD、A-ZH）
  - 11.4 AI 披露与合规：《AI 生成合成内容标识办法》(2025-09-01 施行) 概要；学生发布 AI 辅助论文内容应主动声明；按所在学校 AI 政策填写（CN-AI、§四-3）
  - 11.5 查重/AIGC 检测边界：两库不做查重；integrity gates 不保证数据真实可复现；通用自查建议（阈值因校而异）（§3.6、§六-3）
- **素材引用**：§3.5、§3.6、§3.7、§四(1)、§六(3) ｜ A-ZH、GB、CN-AI、PD
- **命令/代码示例**：有（Pandoc xelatex 中文转换命令、字体/引擎设置片段）
- **本章产物**：符合校方模板的最终 DOCX/PDF + GB/T 7714 参考文献表 + AI 使用声明
- **读者行动项/检查点**：
  - [ ] 用 Zotero/EndNote 官方 GB/T 7714 样式重新生成文献表，并人工抽查至少 5 条
  - [ ] 提交前完成查重/自查，按学校模板填写 AI 披露表

---

## 学习路径说明

### 前置要求
- 已定毕设题目（本指南不负责选题生成，只帮收窄/开题）
- 会基本使用 Claude Code；机器已装 Git 与真实 Python（非 Microsoft Store 占位符）
- 已备 `ANTHROPIC_API_KEY`；可选依赖（Pandoc/tectonic、Git Bash）在做到第 11 章前补齐即可
- 不需要预先熟悉 ARS 或 nature-skills——第 1、2 章会带你入门

### 学完能做什么
- 拿到一张「毕设全流程 × 两库技能」的分工地图，随时知道当前阶段该触发哪个 skill/命令
- 能在 Claude Code（Windows）中装好两库并验证可用，绕开常见踩坑
- 能独立跑通：选题收窄 → 文献综述 → 大纲 → 初稿（过诚信闸门）→ 图表 → 引用自查双保险 → 模拟审稿 → 答辩 PPT
- 能把产出收敛为符合校方模板的中文 DOCX/PDF，并产出 GB/T 7714 文献表与 AI 使用声明
- 清楚两库的边界（不代写、不保证数据真实、不覆盖系统开发与查重），从而合规使用

### 建议学习顺序
- **第 1 遍（读图）**：第 1 章 + 每章开头的「分工建议」和「检查点」，建立全流程地图（约 1–2 天）
- **第 2 遍（随做随查，推荐）**：从自己当前阶段（如文献调研）切入对应章节实操，按「本章产物 + 检查点」验收后再进下一阶段（每章约 1–3 天）
- **第 3 遍（收尾）**：写作后期集中读第 6、8、11 章，把格式/引用/AI 披露一次补齐
- 顺序提示：第 1→2 章应最优先（工具底座）；第 3→10 章可按毕设实际进度跳跃；第 11 章内容建议在首次出现引用时就扫读 11.1/11.2，最终提交前精读全章

---

## 待用户确认 / 已知素材缺口

1. 第 10 章「答辩材料」位于第 11 章「格式合规」之前：若你希望「查重/格式」先于「答辩 PPT」，可交换两章顺序。
2. nature-skills 在 Claude Code 下的 wrapper 写法缺第三方实测：第 2 章将以「官方推荐 + 需实机验证」措辞呈现，建议写作阶段结束后由你实机跑一遍。
3. 目标院校的学位论文 Word/LaTeX 模板与 AI 披露表尚未提供：第 11 章先给通用步骤，精确适配需你提供校名/模板。
4. 总篇幅约 2.0–2.5 万字：若偏长可把第 6、11 章拆为两章，或压缩第 1 章 1.7 节等可略读内容。
5. ARS 默认输出繁体中文：本指南按「简体中文毕设」处理，若你学校要求繁体或中英双语摘要请指出。
