---
title: 如何用好 nature-skills（Codex 上手实战指南）
tags:
  - nature-skills
  - Codex
  - 科研效率
  - 上手实战指南
created: 2026-09-08
updated: 2026-09-08
status: final
source_project: nature-skills-usage
---

# 如何用好 nature-skills（Codex 上手实战指南）

> [!info] 相关笔记
> 若你的目标是把 nature-skills 用进**软件类毕业设计**，可配合 [[用 academic-research-skills + nature-skills 完成软件类毕业设计（实操指南）]] 阅读。

## 阅读说明

- 本笔记类型：实战笔记（上手实战指南），主用环境为 Codex；Claude Code 仅作对照，不展开两套安装说明。
- 读者前提：已熟悉 agent skill 机制（`SKILL.md` / 技能包 / `npx skills` 概念），本机能运行 Codex、Node.js ≥ 18；无需精通 Python/R，部分技能要求的额外运行时按提示补装即可。
- 建议顺序：先读第 1 章建立 Router-style 心智模型（约 15 分钟）；对照第 3 章完成安装后，用第 2 章速查表挑选 1–2 个最贴近自己工作的技能；按第 4 章官方模板做最小验证，跑通一个真实小任务；遇到问题再回查第 5 章；最后把第 6 章的 30 分钟行动清单当作收尾自检。

## 目录

1. [第一章：项目定位与设计哲学](#第一章项目定位与设计哲学)
2. [第二章：技能全景速查](#第二章技能全景速查)
3. [第三章：Codex 安装与日常维护](#第三章-codex-安装与日常维护)
4. [第四章 典型科研场景实操：提示词与流程](#第四章-典型科研场景实操提示词与流程)
5. [第五章：避坑与最佳实践](#第五章避坑与最佳实践)
6. [第六章：上手行动清单与生态进阶](#第六章上手行动清单与生态进阶)

---

## 第一章：项目定位与设计哲学

> 本章要解决一个问题：**nature-skills 到底是什么，为什么值得把科研流程交给它？** 它不像"一条提示词"那样拿来就能猜，背后有一套先建立才用得顺的架构心智。本章先给定位，再讲设计目标与 5 条共享原则、Router-style 核心架构、成熟度标签，最后用"一句定位"收束。全章无代码，是第 2–4 章的"读法底座"——先想清楚它是什么，后面选技能、装依赖、排错才不迷糊。

### 1.1 nature-skills 是什么

一句话定位：nature-skills 是**面向全球 AI 学者的可复用科研技能库**，围绕 `SKILL.md` 组织，仓库 `skills/` 下的**每个顶层目录就是一个可安装单元**（S1 介绍/§5；S5）。

具体长这样：

- 仓库根：`Yuan1z0825/nature-skills`（官方 README 见 S1），含 `skills/` 与配套脚本目录。
- `skills/` 下：`nature-reader`、`nature-polishing`、`nature-citation` 等技能目录，外加一个共享支持包 `nature-shared`。
- 一个可安装单元 = 一个技能目录。装技能 = 把整个目录放进 Codex 的 skills 目录（细节见第 3 章）。

**它为什么值得用**，取决于项目的一条核心主张：

> 几乎所有实用的科研工具，都可以提炼成标准流程；而标准流程，可以封装成可复用技能。（S1 §3.1；S5；S6）

这句话是全书的钥匙。按这个主张，你不必每次从零指挥模型"读这篇论文、画这张图、回这封审稿信"，而是把"读论文该走几步、产物该长什么样"预置成技能。第 4 章的端到端工作流（如 `nature-citation` 的"分段 → Crossref 检索 → 期刊族过滤 → 导出"）就是这条主张的具体化。

> [!tip] 大白话
> 把 `skills/` 下的每个顶层目录想成一个 App 安装包：目录里的 `SKILL.md`、`static/`、`scripts/` 就是 App 的代码和资源，"安装"是把整包放进去。所以**只复制 `SKILL.md` 约等于只拿走 App 图标**——这是后文最大的坑之一，第 5 章会再敲一次。

### 1.2 设计目标与 5 条共享原则

项目的目标可以压成三角（S1；S5；S6）：

- **真实问题解决**：不做"演示级玩具"，每个技能对准一个真实科研任务；
- **可验证工作流**：流程可复跑、可校验（有 preflight、有产物清单）；
- **可直接使用的科研产物**：交付物是 `.md`、`.pptx`、`.svg`、`.enw` 这类能直接进工作流的文件，而非一段聊天回复。

落到设计层面，官方提炼了 5 条共享原则（S1 §7.1；S5 §1.3；S6）：

| 原则 | 大白话理解 | 你会在后文看到的落点 |
|------|-----------|---------------------|
| ① 一手来源优先 | 引用、检索默认回原始文献，不靠模型记忆编 | 引用类技能逐字段核验、"metadata-only"候选等边界自觉 |
| ② 显式胜过隐式 | 路由、依赖、路径边界都写进 `manifest.yaml` 和脚本，不靠口头约定 | manifest 声明式映射、路径校验白名单 |
| ③ 感知上下文 | 按章节/任务加载该加载的片段，不整篇硬塞 | Router 的 `always_load` 与按需 `fragments` |
| ④ 输出优先 | 先想清楚交付物形态，再谈过程 | 各技能有明确产物模板（PPT/图/文献格式） |
| ⑤ 可扩展 | 以"可安装单元 + 共享包"组织，新技能能复用 | `nature-shared` 被多个技能依赖 |

这 5 条不是口号，第 1.3 节的架构就是 ②③④ 的直接产物。

### 1.3 Router-style 架构：核心设计洞察

这是全章最重要的心智模型。**别把 nature-skills 的技能想成"一篇很长的提示词"，而要想成"一个薄路由器 + 一个分层资料库"**（S5 §3.1）。设计上叫 **static/dynamic split（静态/动态分层）**：常驻的核心说明与按需加载的动态片段分开存放，只有任务真正命中时才读取相关部分。

一个 Router-style 技能目录的通用骨架（S5 §3.1/§4.6）：

- `SKILL.md`：**路由器**。frontmatter + 路由协议，只做决策，不写长篇 instruction；
- `manifest.yaml`：声明式映射，写清"**轴（axes）→ 文件**"的对应关系（`always_load` 常驻 / `on_demand` 按需）；
- `static/`：静态分层，含 `core/`（常驻核心）与 `fragments/`（按需片段）；
- `references/`：参考资料（含 `workflows/`）；
- `scripts/`：可执行脚本；
- `templates/`：产物模板；`assets/`：静态资源。

**manifest 声明"轴→文件"、SKILL.md 只做路由**，换来一个关键收益：模型按需只加载匹配的片段，**避免把整本巨型 instruction 一次塞进上下文**（S5 §3.1/§5.3）。真实例子：`nature-polishing` 有 4 个轴——`paper_type / section / language / journal`（S1 §6），也就是说"给综述润色成 Nature 英文"与"给实验章节润色成中文"读到的片段不同。

**一次调用流程**（S5 §3.2）：

1. 你描述任务；
2. Agent 依据 `description` 触发词匹配到某个技能；
3. 读取 `manifest.yaml` 与 `always_load` 常驻核心片段；
4. 解析轴值——部分技能带 **gate**，必要时只问你一个问题并记住偏好；
5. **只读取**命中的 `fragments` / `references`；
6. 执行主体任务；
7. 按需运行 `scripts`；
8. preflight 校验；
9. 交付产物 + 来源标注。

注意第 3、5 步的"只读该读的"——router 的全部价值在这里：上下文更省、指令不互相打架、响应更可预期。目录还带一层硬边界：`manifest.yaml` 的路径校验只允许指向技能目录内部，唯一例外是 `../nature-shared/`，由 `validate-skill-metadata.py` 强制（S5 §4.2/§5.3）。这解释了为什么共享依赖必须单列。

> [!tip] 大白话
> 把 Router 技能想成公司前台接待员。你说"我要开组会汇报"，前台不会把整栋楼的资料一次性搬给你，而是只带你去对应的会议室、取对应的文件。所以 `SKILL.md` 很薄，真正干活时模型只加载命中的片段，少占上下文、少串味。

> [!tip] 大白话
> 把 `manifest.yaml` 里的"轴"想成点餐选项：辣度、分量、主食；gate 想成服务员只追问最关键的一个问题（"要辣吗？"），其余按你上次的偏好默认。所以每次调用不会被长篇盘问，只会就影响产物最大的那个分叉确认一次，之后记住你的选择。

### 1.4 状态标签与项目边界

每个技能带一个**成熟度标签**，它是你决定"能不能直接信任产物"的第一信号（S1 §7.3；S5）：

| 标签 | 含义 | 使用建议 |
|------|------|---------|
| **Draft** | 未实战测试 | 当草稿，先做最小验证 |
| **Beta** | 官方示例跑通过，但边界情况存疑 | 当草稿 + 人工核验清单 |
| **Stable** | 经真实学术内容验证 | 可直接进流程，交付物仍建议核对 |

项目边界（S1 徽章；S5）：

- **协议**：Apache-2.0。
- **规模**：约 **19 个可触发技能 + `nature-shared`** 共享支持包；其中仅 **4 个 Stable**：`nature-figure`、`nature-polishing`、`nature-ref-verifier`、`nature-literature-pipeline`（S1 §6；S5 §5.2）。
- `nature-shared` 是共享支持包，被 `nature-reader`、`nature-paper2ppt`、`nature-polishing`、`nature-writing` 等依赖（S1 §5.1；S5）——它不是独立触发技能，而是别人依赖的"公共库"。
- 技能数量口径随版本有出入，精确清单以 `npx skills --list` 实时为准（分歧记录详见第 2 章）。

> [!tip] 大白话
> 把 Draft/Beta/Stable 想成菜品的内测、试营业与正式菜单：内测菜只有朋友尝过、没经大众检验；正式菜单才是后厨反复出过的。所以写论文、投稿这类关键交付优先选 Stable 技能；Beta/Draft 的产物一律当"草稿 + 核验清单"处理，别直接当定稿用。

### 1.5 一句定位 + 引用纪律

**一句定位收束**：nature-skills 是一个把"真实科研问题"拆成"可验证工作流"、再把"可验证工作流"封装成"可直接使用产物"的 **Router-style 可复用科研技能库**。你要学会的是一套"会按需路由、只加载该加载内容"的用法，而不是背 19 条提示词。

**引用纪律**（贯穿全书）：本章事实来自三档信源——官方 README（S1）、基于源码拆解的第三方解读（S5、S6）、社区二传（S7/S8，未抓原文）。特别是一条需要保持边界的说法：

> 官方 README 以**作者自述**称该设计被 Google DeepMind 借鉴并推出 Science Skills；第三方 S6 也只评价为"无论采信程度如何"。（S1 §3.1；S6）

本笔记将其**作为作者自述转述，不作为外部实证**；后文凡遇 S7/S8 这类社区观点，都会标注低可信、个体体验不一，不作结论。

#### 本章小结

- nature-skills = 面向 AI 学者的可复用科研技能库，`skills/` 下每个顶层目录是一个可安装单元，核心主张是"工具 → 标准流程 → 可复用技能"。
- 设计目标三角：真实问题解决、可验证工作流、可直接使用产物；5 条原则以"一手来源优先 / 显式胜过隐式 / 感知上下文 / 输出优先 / 可扩展"为纲。
- 核心洞察是 **Router-style 架构**：`SKILL.md` 只做路由，`manifest.yaml` 声明"轴→文件"映射，一次调用只读匹配片段，避免巨型 instruction。
- 成熟度标签 Draft/Beta/Stable 决定信任度；约 19 个可触发技能 + `nature-shared`，仅 4 个 Stable，Apache-2.0。
- "被 DeepMind 借鉴"是作者自述，仅转述、不作实证。

## 第二章：技能全景速查

> 本章是全书的「字典章」，解决一个问题：**这约 19 个技能到底叫什么、干什么、什么时候用、要什么环境？** 建议别背，当手册查。先讲清读法（三件事：目录名 ≠ 触发名、状态标签怎么读、为什么「以 `npx skills --list` 实时为准」），再按读论文 / 写作 / 投稿 / 检索 / 演示 / 扩展六大组逐张给速查表，最后单独说共享依赖包 `nature-shared`。本章只负责「认得全、选得对」；怎么装、怎么更新在第 3 章，怎么用、怎么排错在第 4、5 章。

### 2.1 速查表读法

先统一三件事，否则下面任何一张表都可能读错：

**① 目录名 ≠ frontmatter 触发名**

- **目录名**是安装单元：仓库 `skills/` 下那个顶层文件夹的名字，你在 clone 的代码里、文档拆解里见到它。
- **frontmatter name（触发名）**是技能的正式「技能名」：`npx skills --list` 列出的是它，你在提示词里显式点名用哪个技能时写的也是它。
- 绝大多数技能两者同名，但有一个著名反例——`nature-proposal-writer` 这个**目录**里，frontmatter 声明的**触发名是 `researchwrite`**（S1 §5.1；S5 §4.4）。也就是说：仓库里按 `nature-proposal-writer` 找文件，装/列/点名时用 `researchwrite`。

```text
仓库目录（安装单元）              frontmatter name（触发名）
skills/nature-proposal-writer/  →  researchwrite        ← 特例
skills/nature-figure/           →  nature-figure        ← 多数同名
```

**② 状态标签**：沿第 1 章 1.4 的定义——Draft（未实战测试）/ Beta（示例跑过、边界存疑）/ Stable（真实学术内容验证）。本章每张表都带一列状态；**Stable 只有 4 个**：`nature-figure`、`nature-polishing`、`nature-ref-verifier`、`nature-literature-pipeline`（S1 §6；S5 §5.2），其余 15 个为 Beta/Draft。

**③ 实时口径**：技能清单与数量随版本有出入。素材阶段就发现口径分歧（02 素材 §4）：README 徽章写 19、索引表列 18 可触发 + `nature-shared`、仓库实测目录数与索引又不完全一致。**结论：本表按 2026-09-08 抓取的 README §6 索引整理（约 19 个可触发技能 + `nature-shared`），精确清单一律以你本机 `npx skills --list` 的实时输出为准**（S1 §6）。

> [!tip] 大白话
> 把目录名想成「房间号」，把 frontmatter 触发名想成「房间里那位同事的正式姓名」。前台（Agent / `npx skills`）只认正式姓名，你报房间号它不一定找对人——尤其 `nature-proposal-writer` 那间房住的人叫 `researchwrite`。所以列表、点名都用触发名。

> [!tip] 大白话
> 把「以 `npx skills --list` 实时为准」想成菜单上的「以当日时价为准」：这份速查是今天拍的照，上游明天可能加技能、改状态。真到装机时，屏幕上列出什么就用什么，表里对不上就以实时为准，不用慌。

下表分组说明：A 读论文 → B 写作润色 → C 投稿返修，正好串起「读进来 → 写出去 → 投出去」的论文主线；D 检索引用管「可信度底座」；E 演示绘图出「看得见的产物」；F 扩展记录管「投稿之外的延伸」。每行字段：目录名 / frontmatter 触发名（若不同，`—` 表示与目录名相同）/ 状态 / 一句话用途 / 典型触发词 / 运行依赖与注意。

### 2.2 分组速查 A｜读论文与文献管理

对应科研流水线的最上游：把一篇 PDF 变成「可读、可查、可存档」的结构化产物。

| 目录名 | 触发名（若不同） | 状态 | 一句话用途 | 典型触发词 | 运行依赖 / 注意 |
|------|------|------|-----------|-----------|------|
| `nature-reader` | — | Beta | 带来源锚点、图文对应、公式渲染、中英对照的全文 Markdown reader | 全文 Markdown / 图文对应 / 全文翻译 | 依赖 `nature-shared`；读论文核心（S1 §6） |
| `nature-paper-card` | — | Beta | 单篇精读生成 01–16 节 Paper Card（证据链 / 结论边界 / 批判分析） | Paper Card / 论文精读 / 证据链 | 教程见 `docs/nature-paper-card-tutorial.md` |
| `nature-downloader` | — | Beta | 走图书馆 / CARSI / 开放获取渠道「合法」获取全文 PDF | 图书馆下载文献 / CARSI / PDF 下载 | Node + Python 双实现；账号与合规边界见第 5 章 |
| `nature-literature-pipeline` | — | Stable | 自动化文献发现管线：多源检索 → 六维评分 → 精读推送 → 本地归档 | literature pipeline / 每日文献 / cron | 可配 cron 每日跑；本组唯一 Stable |

### 2.3 分组速查 B｜写作与润色

对应「把研究结果写成 Nature 风格文稿」：从润色既有文字到从零起草章节，再到统计与数据可用性声明。

| 目录名                      | 触发名（若不同）        | 状态     | 一句话用途                                               | 典型触发词                                | 运行依赖 / 注意                                                                       |
| ------------------------ | --------------- | ------ | --------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| `nature-polishing`       | —               | Stable | 学术文本润色 / 重构 / 翻译为 Nature 风格英文                       | Nature style / 润色 / academic writing | 依赖 `nature-shared`；4 轴路由 `paper_type / section / language / journal`；修 LaTeX 排版 |
| `nature-writing`         | —               | Draft  | 起草 Nature 风格手稿章节、重建论证                               | 写摘要 / 写引言 / manuscript draft         | 依赖 `nature-shared`；写作类                                                          |
| `nature-statistics`      | —               | Draft  | 统计报告审查 / 改写 / 起草（实验单位 / 重复 / p 值 / 多重比较 / 效应量 / CI） | Nature statistics / 统计审查 / p value   | 写作类                                                                             |
| `nature-data`            | —               | Draft  | Data Availability 声明 + 数据仓储方案 + FAIR 检查             | Data Availability / FAIR             | 写作类                                                                             |
| `nature-proposal-writer` | `researchwrite` | Beta   | proposal-first 科研写作状态机：证据 / 论证 / 契约先于文本             | researchwrite / 开题报告 / 科研写作 QA       | 写作类；**装/列/点名都用触发名 `researchwrite`**（S1 §5.1；S5 §4.4）                            |

### 2.4 分组速查 C｜投稿与返修

对应「论文投出去之后」：投稿前先自我审判，收到返修邮件后逐点回应。

| 目录名 | 触发名（若不同） | 状态 | 一句话用途 | 典型触发词 | 运行依赖 / 注意 |
|------|------|------|-----------|-----------|------|
| `nature-reviewer` | — | Draft | 模拟 Nature 审稿人，产出 3 份互盲 reviewer reports + Major/Minor 分级 | 预投稿评审 / reviewer report | 写作类；建议全部定稿后再综合 |
| `nature-response` | — | Beta | 解析返修邮件：cover letter + 逐点回复 + 标红稿 + LaTeX 模板 | response to reviewers / rebuttal / 返修邮件 | 返修季核心 |

### 2.5 分组速查 D｜检索与引用核验

对应「可信度底座」：找支撑文献、审计引用与画像、逐字段核验参考文献，三类交付物都建议人工多源复核后再进投稿。

| 目录名 | 触发名（若不同） | 状态 | 一句话用途 | 典型触发词 | 运行依赖 / 注意 |
|------|------|------|-----------|-----------|------|
| `nature-citation` | — | Beta | 严格 Nature/CNS 范围支撑文献检索，导出 ENW / RIS / Zotero RDF | CNS citation / 支撑文献 / Zotero RDF | `scripts/nature_citation.py` 调 Crossref，免 key |
| `nature-academic-search` | — | Beta | 多源检索 + 严格他引审计 + 高影响力引用者画像 + MCP server | 查文献 / verify DOI / 严格他引 | MCP server 覆盖 arxiv / crossref / pubmed / sciencedirect / scopus；需配置 `PUBMED_EMAIL` |
| `nature-ref-verifier` | — | Stable | 参考文献多源交叉验证：作者 / 标题 / 年份 / 卷期 / 页码逐字段核对 | verify refs / 文献验证 / ref check | 引文可信度首选；本组唯一 Stable |

### 2.6 分组速查 E｜演示与科研绘图

对应「看得见的产物」：组会 PPT 与投稿级图表。

| 目录名 | 触发名（若不同） | 状态 | 一句话用途 | 典型触发词 | 运行依赖 / 注意 |
|------|------|------|-----------|-----------|------|
| `nature-paper2ppt` | — | Beta | 论文 → 中文 PPTX 文献汇报 deck | paper PPT / journal club / 论文汇报 | 依赖 `nature-shared` |
| `nature-image2ppt` | — | Beta | 图片 / 扫描 PDF / 图片型 PPTX → 对象级可编辑 PowerPoint + 渲染 QA | 图片转可编辑 PPT / 扫描 PDF 转 PPTX | 图片类 |
| `nature-figure` | — | Stable | Python/R 投稿级科研图 + OpenRouter GPT Image 2 论文示意图草稿 | Nature figure / 投稿级图片 / 论文示意图 | R 后端可选；OpenRouter key 用于 AI 示意图；demo 见 `assets/figures4papers`；本组唯一 Stable |

### 2.7 分组速查 F｜扩展与记录

对应投稿主线之外的延伸：把论文往专利方向转化、把日常实验沉淀成 Obsidian 日志。

| 目录名 | 触发名（若不同） | 状态 | 一句话用途 | 典型触发词 | 运行依赖 / 注意 |
|------|------|------|-----------|-----------|------|
| `nature-paper-to-patent` | — | Beta | 论文 / 报告 → 中国发明专利草稿（专利点挖掘 / 查新 / 交底书） | paper to patent / 权利要求书 / 技术交底书 | 需 Playwright chromium；CNIPA 可选；全库最重技能 |
| `nature-experiment-log` | — | Draft | 实验图文音标准化记录 → Obsidian 实验日志 | 实验日志 / Obsidian vault / 飞书科研群 | Obsidian 场景（第 6 章有 vault 结合点） |

### 2.8 共享依赖包 `nature-shared`

`nature-shared` 不是可触发技能——它没有面向任务的触发名，你不能单独让 Codex「跑一个 nature-shared」。它的角色是**公共支持包**：多个技能共用的参考资源与文件被抽到这一个目录里，供其他技能引用（第 1 章 1.3 的路径白名单里，唯一允许越出技能目录引用的就是 `../nature-shared/`）。

官方明确点名依赖它的有 **4 个技能**（S1 §5.1；S5；S9 低权威旁证）：

- `nature-reader`（A 组）
- `nature-polishing`（B 组）
- `nature-writing`（B 组）
- `nature-paper2ppt`（E 组）

**为什么单独装容易漏**：上面 4 个技能看名字各有各的任务，不看依赖说明的话，很难想到它们还共用一个支持包。于是常见翻车现场是「单独装了 `nature-reader`，跑起来缺文件」，其实只差把 `nature-shared` 一起带上。第 3 章会给「技能名 + `nature-shared` 并列」的完整安装写法，第 5 章会把它列为必踩坑之一。

> [!tip] 大白话
> 把 `nature-shared` 想成小区的公共水电：上面 4 个技能是「房间」，光把房间搬进来、没接公共管线，灯是不会亮的。所以单独装它们时，命令里要把 `nature-shared` 一并写上——否则一跑就缺胳膊少腿，报错还多半指向找不到 shared 目录。

#### 本章小结

- 读法三件事：**目录名 ≠ frontmatter 触发名**（特例 `nature-proposal-writer` → `researchwrite`）；状态标签决定信任度；清单以 `npx skills --list` 实时为准。
- 六大组：A 读论文（4）→ B 写作润色（5）→ C 投稿返修（2）串起论文主线；D 检索引用（3）管可信；E 演示绘图（3）出产物；F 扩展记录（2）做延伸。
- Stable 仅 4 个：`nature-figure`、`nature-polishing`、`nature-ref-verifier`、`nature-literature-pipeline`；其余 15 个 Beta/Draft，产物一律当草稿。
- `nature-shared` 是共享支持包，`nature-reader` / `nature-polishing` / `nature-writing` / `nature-paper2ppt` 需一并安装。

## 第三章：Codex 安装与日常维护

> 本章解决一个很实际的问题：装哪些、装到哪、怎么更新、怎么拆、装完怎么确认真的能用。读完你会有两条互相配合的「安装路线」和一张命令矩阵，照着敲即可，不用背。

上一章给了 19 个技能的全景速查，但「认识」不等于「能用」。本章从前置检查开始，先给一条安装路线决策树（§1），再讲 `npx skills` 按技能粒度安装的命令矩阵（§2）、仓库脚本整库同步（§3）、SessionStart 自动更新（§4）、运行时依赖与合规安装（§5），最后是安装验证与「开新会话」规则（§6）。

---

### 1. 前置准备与「安装路线决策树」

#### 1.1 装之前先确认三件事

| 前置项 | 要求 | 检查命令 |
|--------|------|----------|
| Node.js | **≥ 18**（`npx skills` 本身就跑在 npx 上） | `node -v` |
| Codex | 本机已可运行 Codex CLI | `codex --version` |
| Git | 推荐安装（私有仓库 / 凭据走 Git credential、`gh` 或 `GITHUB_TOKEN`） | `git --version` |

```bash
node -v          # 期望 v18 或更高，低于 18 先升级 Node
codex --version  # Codex 可用即可继续
```

> [!tip] 大白话
> 把 `npx skills` 想成「上门安装的师傅」：师傅（npx）本身要能跑，前提是 Node.js 这把「工具箱」够新（≥18）。Node 版本太旧，工具箱缺件，师傅来了也干不了活。

#### 1.2 安装路线决策树

nature-skills 官方给的是**两条互补路线**，不是二选一的对立关系（S1 §5.1/§5.3）。先想清楚你要哪种「跟上游」的节奏：

```text
只想要 1–3 个技能（轻、快、可挑）
   └─ 路线 1：npx skills add（按技能粒度，记着带 nature-shared）
想要整库长期跟上游、能一键整体升级/清理
   └─ 路线 2：git clone + scripts/update-codex-skills.sh（整库同步）
想每次开 Codex 自动检查更新、不用手动记
   └─ 路线 2 的专用 clone + autoupdate-skills.sh 注册为 SessionStart hook
```

两条路线的最终落点是同一套目录：全局装到 `~/.codex/skills/`，项目级装到 `.agents/skills/`（见 §2.3）。区别只在**管理方式**——路线 1 由第三方 CLI（vercel-labs/skills）按技能管理，路线 2 由仓库自带脚本整库管理（S2；S1 §5.3）。

> [!tip] 大白话
> 把路线 1 想成「按需点菜」——只点今天想吃的几道，后厨（npx skills）单独给你做；把路线 2 想成「整箱搬货」——直接跟厂家（GitHub 仓库）订一整箱，厂家出新版你就整箱换新。怕麻烦、想要最新最全就整箱；只想用两三个技能就点菜，别为了一道菜买一箱。

---

### 2. 路线 1｜`npx skills add / list / update / remove` 命令矩阵

路线 1 的 CLI 是 vercel-labs/skills，通过 `npx skills` 调用；安装源用 GitHub 仓库缩写 `Yuan1z0825/nature-skills`（S1 §5.1；S2）。所有命令以 `--agent codex` 限定装到 Codex。

#### 2.1 先看有哪些技能可装（不安装）

```bash
npx skills add Yuan1z0825/nature-skills --list
```

`--list` 只列出可安装技能，**不安装**（S2）。关键点：这里列出的名字是 **frontmatter name**（`SKILL.md` 里声明的触发名），不是仓库目录名（S1 §5.1）。

```text
# 输出示意（以仓库当前索引为准，字段措辞随 CLI 版本可能不同）
Available skills from Yuan1z0825/nature-skills:
  nature-reader          # 读论文全文 Markdown
  researchwrite          # ← 目录名其实是 nature-proposal-writer
  ...
```

> [!warning] 目录名 ≠ frontmatter name
> `nature-proposal-writer` 这个**目录**，它的 frontmatter 触发名是 `researchwrite`。凡是 `npx skills` 系列命令里写技能名的地方（`--skill` / `list` / `update` / `remove`），都用 **frontmatter name**。选技能、报技能名时也是 `researchwrite`，不是目录名（S1 §5.1；S5 §4.4）。

> [!tip] 大白话
> 把「目录名」想成工牌上的**部门+岗位**（nature-proposal-writer），把「frontmatter name」想成平时喊人的**花名**（researchwrite）。CLI 和 Agent 都认花名——你在走廊喊他的部门名，他可能不知道在叫你。

#### 2.2 安装（add）

**① 全量装到 Codex（全局）**——一次带上全部技能含 `nature-shared`：

```bash
npx skills add Yuan1z0825/nature-skills --global --agent codex --skill '*' --yes --copy
```

**② 单技能装到当前项目**——省略 `--global` 即项目级，只装 `nature-figure`：

```bash
npx skills add Yuan1z0825/nature-skills --agent codex --skill nature-figure --yes --copy
```

**③ 依赖共享包的技能单独装**——`nature-reader` / `nature-paper2ppt` / `nature-polishing` / `nature-writing` 依赖 `nature-shared`，单独装这类技能时要把共享包一起点名，否则会漏：

```bash
npx skills add Yuan1z0825/nature-skills --global --agent codex --skill nature-reader --skill nature-shared --yes --copy
```

**④ 一次装到 CLI 支持的所有 Agent**（不只 Codex）：

```bash
npx skills add Yuan1z0825/nature-skills --all
```

#### 2.3 关键 flag 语义与安装路径

flag 语义以 vercel-labs/skills 文档为准（S2）：

| flag | 含义 |
|------|------|
| `--global` | 装到全局；**省略**则装到当前项目 |
| `--agent codex` | 指定目标 Agent 为 Codex |
| `--skill '<name>'` | 指定技能名，可用 `'*'` 表示全部；可重复出现组合多个技能 |
| `--yes` | 跳过确认提示 |
| `--copy` | **复制**文件而非建 symlink；Windows 无管理员 / symlink 受限时推荐 |
| `--list` | 只列出可安装技能，不安装 |
| `--all` | 等价 `--skill '*' --agent '*' -y` |

路径映射（S2 Supported Agents 表）：

```text
全局安装   ~/.codex/skills/          # 当前机器所有 Codex 项目可见
项目安装   <项目根>/.agents/skills/  # 只对当前项目生效
```

```text
# 全局安装后的目录形态（示意）
~/.codex/skills/
├── nature-reader/
│   ├── SKILL.md          # frontmatter + 路由协议
│   ├── manifest.yaml     # 声明式「轴 → 文件」映射
│   ├── static/
│   ├── references/
│   └── scripts/
├── nature-shared/
└── ...（其余技能目录）
```

> [!warning] 保留完整技能目录
> 无论哪条路线，都要保留技能**整目录**（`SKILL.md` + `references/` + `static/` + `manifest.yaml` + `scripts/` + 依赖的 `nature-shared/`）。**只复制 `SKILL.md` 会坏**——router-style 技能靠 manifest 和按需加载的片段目录工作，单文件是跑不起来的（S1 §5.3）。

> [!tip] 大白话
> `--copy` 想成「把资料复印一份放进自己文件夹」；不写 `--copy`（symlink）想成「在文件夹里贴一张『去资料室取』的便签」。Windows 没开管理员权限时，便签可能贴不上（symlink 受限），所以官方建议复印一份，省心。

#### 2.4 查看已安装（list）

```bash
npx skills list --global --agent codex --json
```

`--json` 输出结构化结果，方便核对到底装上了哪些、装在哪个路径（S1 §5.1；S2）。

```json
// 输出示意（字段以实际 CLI 版本为准）
{
  "agent": "codex",
  "global": true,
  "skills": [
    { "name": "nature-reader",  "path": "~/.codex/skills/nature-reader" },
    { "name": "nature-shared",  "path": "~/.codex/skills/nature-shared" },
    { "name": "researchwrite",  "path": "~/.codex/skills/nature-proposal-writer" }
  ]
}
```

记不清装了哪些名字时，先 `list --json` 再动手，不要凭目录名猜。

#### 2.5 更新（update）

```bash
npx skills update --global --yes                    # 更新全部全局技能
npx skills update nature-reader --global --yes      # 只更新单个技能
# 项目级更新在项目目录内执行，作用域默认 --project
```

`update` 支持全量、单技能与项目作用域（`--project`），按需选用（S1 §5.1；S2）。

#### 2.6 删除（remove）

```bash
npx skills remove <skill>              # 用 frontmatter name，不是目录名
npx skills remove <skill> --global --agent '*'   # 指定作用域与 Agent
npx skills remove <skill> --all        # 全 Agent 范围删除
```

`remove` 的语义来自 S2：同样支持 `--global` / `--agent` / `--all` 作用域。删之前先 `list --json` 确认技能名拼写。

---

### 3. 路线 2｜仓库脚本整库同步（官方 Codex 推荐）

想整库跟上游、能整体校验和清理，用仓库自带脚本 `scripts/update-codex-skills.sh`（S1 §5.3 官方 Codex 路线）。它只处理**本仓库的技能目录**，不碰你别的配置。

#### 3.1 首次同步

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git
cd nature-skills
scripts/update-codex-skills.sh --pull
```

#### 3.2 三个子命令

| 子命令 | 作用 |
|--------|------|
| `--pull` | clone 后全量同步到 Codex 技能目录 |
| `--check` | 校验本机技能与仓库的一致性（只检查不写入） |
| `--pull --prune` | 同步，并清理上游已删除的技能目录 |

```bash
scripts/update-codex-skills.sh --check        # 校验一致性
scripts/update-codex-skills.sh --pull --prune # 同步 + 清理上游已删目录
```

#### 3.3 脚本行为与 Windows 注意点

脚本内部特性（S1 §5.3；S5 §4.2）：

- 用 `rsync -a --delete` 同步，只动本仓库的技能目录；
- 同步后写一份清单记录，`diff -qr` 校验一致性；
- 跑完打印可选的 Python 依赖安装提示（不会自动装）。

Windows Git Bash 注意：

- `update-codex-skills.sh` **依赖 `rsync`**。Windows 的 Git Bash 不一定自带 rsync，首次跑 `--pull` 前先确认 `rsync --version` 可用；不可用则需自备 rsync 或退回路线 1（S1 §5.3；P2 §5 实践指导）。
- 多技能安装优先 `--copy`（避开 Windows symlink 权限问题）。
- 该脚本**只同步 Codex**；Claude Code 用户不能拿它同步自家环境（那是 Claude Code 路线，走本地 clone + wrapper，本节不展开）（S1 §5.2/§5.3）。

> [!note] `--prune` 的删除语义
> `--prune` 只删「脚本此前记录过、但仓库里已不存在」的技能目录；**首跑不猜删**，不会误删你没同步过的东西（S1 §5.3）。

> [!tip] 大白话
> `rsync -a --delete` 想成「拿仓库当母本做整盘镜像」：本地多出来的、母本已删的旧技能会被清掉（`--prune` 时）。正因为是镜像式同步，它要求你有个**专用、干净**的 clone，别在这个仓库目录里自己乱改文件。

---

### 4. 自动更新：autoupdate-skills.sh + SessionStart hook

想要「每次开工自动检查有没有新版」，官方方案是把 `scripts/autoupdate-skills.sh` 注册成 Codex 的 **SessionStart hook**（S1 §5.3）。

#### 4.1 手动触发一次

```bash
scripts/autoupdate-skills.sh --dest ~/.codex/skills --force
```

#### 4.2 脚本的自我保护行为

- **6 小时节流**：同一仓库 6 小时内不重复同步；
- **断网即退**：连不上网络时 exit 0，不打扰你开工；
- **仅 HEAD 变化才同步**：远端没有新提交就不折腾；
- **拒绝脏 clone**：仓库目录有未提交改动时拒绝执行。

#### 4.3 注册到 SessionStart hook

官方建议把它合并进 Codex 的 `~/.codex/hooks.json` 的 `SessionStart`（S1 §5.3）。每次开新 Codex 会话时，hook 自动触发脚本检查更新。

```json
// ~/.codex/hooks.json —— 结构示意
// Codex 不同版本的 hook schema 字段可能有差异，以你本机版本为准（需实测）
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/nature-skills/scripts/autoupdate-skills.sh --dest ~/.codex/skills"
        }
      ]
    }
  ]
}
```

> [!warning] 需实测项
> `hooks.json` 的**具体 JSON 结构与字段名**随 Codex 版本可能有差异，也可能你本机用的是 `config.toml` 的 hook 写法。上表是「合并进 SessionStart」的**结构示意**，落地前先对照你本机 Codex 的 hook 文档确认一次，别照抄后静默失败。

> [!tip] 大白话
> 把自动更新想成**小区物业的定时巡检**：每次你进门（SessionStart）它先看一眼有没有新公告（仓库新版本），有就顺手更新，但每 6 小时最多跑一次，不会每次进门都大动干戈；没联网它就安静退下，不挡你路。

---

### 5. 运行时依赖与合规安装

`npx skills` / 仓库脚本**只负责把技能文件放到位，不会自动装运行依赖**。技能真正跑起来还差一层：Python 包、浏览器、MCP server、密钥。官方明示：按各技能 README 单独装（S1 §5.3；S5 §2.1）。

#### 5.1 依赖速查

| 技能 / 组件 | 额外依赖 | 典型安装命令 |
|-------------|----------|--------------|
| `nature-paper-to-patent`（最重） | Python 依赖 + Playwright chromium | `pip install -r skills/nature-paper-to-patent/requirements.txt` |
| 同上（可选国知局检索） | CNIPA 附加依赖 + chromium | `pip install -r skills/nature-paper-to-patent/disclosure/requirements-cnipa.txt` + `python -m playwright install chromium` |
| `nature-academic-search`（MCP server） | MCP server 的 Python 依赖 | `pip install -r skills/nature-academic-search/mcp-server/requirements.txt` |
| `nature-figure` | R 后端可选；AI 示意图要 OpenRouter key | R 按需装；OpenRouter key 配置见技能 README |
| 通用 | Node.js ≥18、Python 3.x、Git | 见 §1.1 |

（CNIPA / MCP 依赖的具体相对路径以仓库内实际目录为准；`.../disclosure/...`、`.../mcp-server/...` 为官方文档缩写，安装时先 `ls` 确认。）

#### 5.2 凭据与合规边界

- **`PUBMED_EMAIL`**：`nature-academic-search` 的 MCP server 需要配置一个真实邮箱（PubMed 对检索请求要求联系邮箱），按技能 README 提示设置即可。
- **Scopus / ScienceDirect**：用**本机已有的机构凭据/登录态**，不要把 key 写进仓库（S1 §5.3）。
- **OpenRouter key**：`nature-figure` 生成 AI 示意图走付费 API，费用与账号风险由使用者承担（S5 §2.1）。
- **`nature-downloader` 的「合法获取」**：它只负责在你已有权限的前提下帮你拿全文（图书馆 / CARSI / 开放获取），**账号与合规边界由使用者负责**——没有权限的文献它不该也不应绕过（S1 §5.3；S5 §5.2）。

> [!tip] 大白话
> 把 `PUBMED_EMAIL`、机构登录态、API key 想成**门禁卡**：技能是帮你刷卡的助手，但卡得是你自己的、且你得有进那扇门的权限。技能不负责替你「配钥匙」，更不会帮你翻墙进不该进的房间——配卡和门禁权限都是你自己的事。

#### 5.3 一个「最小依赖闭环」示例

只跑读论文场景的话，最小闭环是 `nature-reader` + `nature-shared`，外加确认 Codex 会话能联网访问 PDF 即可，通常不需要装 Playwright。等用到 `nature-paper-to-patent` 这类重技能，再回来补 §5.1 的安装命令即可——**按技能补齐，别一上来全装**。

---

### 6. 安装验证与「开新会话」规则

#### 6.1 装完必须开新会话

技能是在 **Codex 会话启动时**被发现的。装完 / 更新完技能，**必须开一个新的 Codex 会话**，再自然描述任务；在旧会话里继续聊，Agent 很可能根本看不到新技能（S1 §5.3；P2 §5 实践指导）。

#### 6.2 最小验证三步走

**第 1 步：确认文件到位**

```bash
npx skills list --global --agent codex --json     # 看技能名与路径
ls ~/.codex/skills/nature-reader/SKILL.md         # 确认是整目录，不是单文件
```

**第 2 步：开新会话，丢一句官方模板提示词**——挑一个最贴近你工作的技能做冒烟测试。例如测 `nature-reader`：

```text
把这篇 PDF 做成图文对应的中英文对照 Markdown reader
```

（官方模板提示词见 S1 §4；更多模板在下一章。）

**第 3 步：确认产物形态**——看是否产出该技能承诺的产物，而不是空话：

| 技能 | 期望产物形态 |
|------|--------------|
| `nature-reader` | 图文对应、带来源锚点的 Markdown |
| `nature-paper2ppt` | `.pptx` |
| `nature-citation` | `.enw` / `.ris` / Zotero RDF + 浏览器 HTML |
| `nature-figure` | `.svg` / 图件文件 |

产物形态（`.md` / `.pptx` / `.svg` / `.enw`）冒烟通过，才算「真的能用」；只回了一段文字没有产物，先回查 §5 依赖是否漏装（P2 §5 实践指导）。

#### 6.3 验证清单

- [ ] `node -v` ≥ 18、Codex 可运行
- [ ] 按决策树选了路线，技能装到预期路径（`~/.codex/skills/` 或 `.agents/skills/`）
- [ ] 依赖技能（`nature-shared`）一起装了
- [ ] 运行时依赖按技能 README 补齐（含 `PUBMED_EMAIL` 等凭据）
- [ ] **开了新会话**，官方模板提示词冒烟通过，产物形态正确
- [ ] 保留的是完整技能目录，不是只拷了 `SKILL.md`

---

#### 本章小结

- **两条路线互补**：1–3 个技能用 `npx skills` 按需点菜（记着带 `nature-shared`）；整库跟上游用 `update-codex-skills.sh`；要自动更新再加 SessionStart hook。
- **命令矩阵核心**：`add --global --agent codex --skill '*' --yes --copy` 全量装；省略 `--global` 是项目级；`list --global --agent codex --json` 核对；`update` / `remove` 都支持 `--global` / `--project` / `--all` 作用域。
- **名字用 frontmatter name**：`nature-proposal-writer` 目录的触发名是 `researchwrite`；`list` 显示的就是这个名字。
- **路径**：全局 `~/.codex/skills/`，项目级 `.agents/skills/`；Windows 优先 `--copy`，`update-codex-skills.sh` 依赖 rsync 需实测。
- **运行时依赖不会自动装**：Python 包 / Playwright chromium / MCP server / `PUBMED_EMAIL` / 机构凭据按各技能 README 补齐，合规与账号边界归使用者。
- **装完开新会话再验证**：`list --json` + 官方模板提示词冒烟，确认 `.md` / `.pptx` / `.svg` / `.enw` 产物形态。

## 第四章 典型科研场景实操：提示词与流程

> 本章解决一个问题：装好 nature-skills 之后，开口第一句到底怎么说？前两章给了你 19 个技能的「名单」，这一章把它们放进 8 个真实科研场景，给出一套可以直接复制的提示词、每个场景的期望产物与注意点，最后解剖一条端到端工作流，让你看清「可验证流程」到底长什么样。

### 4.1 用法心法：先会「说话」，再谈技能

先忘掉技能名，记住一条总原则：**先想清楚你要完成什么任务，再决定要不要点名某个技能。** nature-skills 的路由器（router）本身就能从你的自然描述里匹配技能，你不需要每次都精确说出 `nature-xxx`。

两种开口方式的取舍如下：

| 你的状态 | 推荐说法 | 为什么 |
| --- | --- | --- |
| 拿不准该用哪个技能 | 自然描述任务（只说目标，不提技能名） | 路由器按描述匹配最合适的技能，匹配不上会再问你 |
| 已经确定用哪个技能 | 显式写「使用 `nature-xxx`」 | 跳过匹配的不确定性，直接进入技能内部的 gate 与执行 |
| 触发后技能反过来提问 | 只回答它问的那一个问题 | 这类技能带 gate，一次只问一个必要问题，答完就继续 |
| 同一个选择下次还要再答？ | 不用，它会在会话内记住偏好 | 如 `nature-figure` 的 Python/R 后端，用 `nature_figure_backend.py set python` 固化一次即可[^c4-2] |

官方快速开始把这件事说得很直白：「直接这样说」即可——你甚至可以整段不提任何技能名[^c4-1]。显式点名是你在已经读过第 2 章速查表、心里有数时的「加速手段」，两者不是二选一的对错关系，而是同一件事的两档精度。

> [!tip] 大白话：把「自然描述」想成去办事大厅跟前台说需求
> 你跟前台说「我要打印一份带图的 PPT」，前台（路由器）听完把你领到对应窗口；如果你已经知道 3 号窗口专管这事，直接说「我要去 3 号窗口」当然更快。所以：不确定就描述需求，确定了就点名窗口——两种都是合法用法，区别只在速度与可控性。

还有一个容易忽略的体验点：**部分技能带 gate（门禁问题）**。它不是刁难你，而是任务里确实存在一个「你不说它就没法往下走」的分叉。比如 `nature-figure` 要先知道绘图后端用 Python 还是 R，它只会问这一个问题，并把你的选择记进偏好，下次不重复问。别一次抛一堆信息把它绕晕，也别对它的追问不耐烦——答完那个问题，后面就顺了。

> [!tip] 大白话：gate 就像办证窗口问「教师还是学生？」
> 窗口只需要一个信息来决定走哪张表，问完就把你的身份记在档案里，下次直接按档案办。它不会连环审问你，你也不用把身份证户口本全拍在桌上。

### 4.2 场景实操 1–4：读论文与写作的前半程

下面的 8 个场景都按同一格式组织：**触发词 → 官方提示词（可整段复制）→ 期望产物 → 注意点**。官方 README 提供的是「直接这样说」的模板句[^c4-1]；每个场景标注的「命中技能」是本次研究按技能描述推断的映射（inference），不是官方保证——实际命中取决于你的安装范围与路由器的匹配结果。复制模板句时，把其中的「这篇 PDF」「这段中文」替换成你手上的真实材料即可。

#### 场景 1｜读论文：中英对照 Markdown（推断命中 `nature-reader`）

- **何时用/触发词**：手上有 PDF，想精读并保留一份可检索、可追溯原文的 Markdown，而不是只得到一段翻译摘要。
- **官方提示词**：

```text
把这篇 PDF 做成图文对应的中英文对照 Markdown reader
```

- **期望产物**：一份图文对应、中英对照的全文 Markdown。官方定位里，`nature-reader` 的产物带**来源锚点**（正文可追溯到原文位置）、**图文对应**（图和正文挂钩）、**公式渲染**，是「读论文」分组的核心技能[^c4-1]。这份 `.md` 可以直接存进你的 Obsidian vault，作为精读底稿。
- **注意点**：
  - 中英对照不是「机翻全文贴在一起」，而是带结构的 reader 形态；拿到产物后先检查图注与锚点是否对得上原文页码/图号。
  - 若你是按第 3 章的「单技能」路线安装，`nature-reader` 依赖共享包 `nature-shared`，漏装会导致触发后跑不起来。

#### 场景 2｜文献汇报 PPT（推断命中 `nature-paper2ppt`）

- **何时用/触发词**：组会、Journal club 需要把一篇论文讲给课题组听，要中文 deck。
- **官方提示词**：

```text
把这篇论文做成中文组会汇报 PPT，保留关键图件和来源标注
```

- **期望产物**：一份中文文献汇报 `.pptx`。注意模板句里显式要求「保留关键图件和来源标注」——这正是设计原则里「一手来源优先、输出优先」的体现，避免生成一份图全丢了、出处也说不清的汇报稿。
- **注意点**：
  - 产物是 `.pptx` 而不是 Markdown；生成后建议人工过一遍排版与图件清晰度再上会。
  - 与场景 1 一样依赖 `nature-shared`。
  - 推断映射为 `nature-paper2ppt`（论文→中文 PPTX deck），若你的输入是图片型 PDF 或扫描件，那对应的是 `nature-image2ppt` 那条线，不是本场景。

#### 场景 3｜润色 / 翻译为 Nature 风格英文（推断命中 `nature-polishing`）

- **何时用/触发词**：有一段中文初稿想改成英文投稿风格，或英文稿想按 Nature 行文重写。
- **官方提示词**：

```text
把这段中文改写成 Nature 风格英文，保持学术含义不变
```

- **期望产物**：改写后的英文学术文本。`nature-polishing` 内部是一个 **4 轴路由**（paper_type / section / language / journal），gate 可能会追问你：这是什么类型的论文、要处理哪个章节、语言方向、投哪本刊[^c4-1]。答完这些，它才能按对应风格处理；它还能顺带修复 LaTeX 排版问题。
- **注意点**：
  - 状态为 Stable，是可信度较高的技能之一，但仍属于写作类交付物：**语义有没有被改歪，必须你亲自对一遍**。
  - 社区有「润色带 AI 味、行文偏冗长」的反馈（属二传信息，可信度低），若你目标期刊查 AI 率，需要人为调整句长——这一点留到第 5 章细说。

#### 场景 4｜起草摘要与引言（推断命中 `nature-writing`，可叠加 `nature-polishing`）

- **何时用/触发词**：结果和图件已经齐了，但「第一稿」迟迟开不了头。
- **官方提示词**：

```text
根据这些结果和图件，帮我起草 Nature 风格的摘要和引言
```

- **期望产物**：摘要 + 引言的初稿文本。`nature-writing` 的定位是起草 Nature 风格手稿章节、重建论证，是 Draft 状态的写作技能[^c4-1]。
- **注意点**：
  - **把结果和图件作为上下文一起给它**，而不是只丢一句模板句——模板里的「这些结果和图件」指的就是你要附上的材料。
  - 状态是 Draft，意味着未经充分的真实学术内容验证，这稿子要当「可批评的草稿」用，别当可提交的定稿。
  - 推断命中 `nature-writing`，若你拿到的初稿在措辞上还差一口气，可再接场景 3 的 `nature-polishing` 过一遍。

### 4.3 场景实操 5–8：投稿返修与检索绘图的后半程

#### 场景 5｜预投稿互盲审稿（推断命中 `nature-reviewer`）

- **何时用/触发词**：投稿前想先挨一顿「毒打」，把明显缺陷堵在送审之前。
- **官方提示词**：

```text
从 Nature 审稿人视角评估这篇稿件，给出三份互盲 reviewer reports；全部定稿后再综合
```

- **期望产物**：三份**互盲** reviewer reports（彼此独立、互不知晓对方意见），外加最后一份综合意见。`nature-reviewer` 的定位就是模拟 Nature 审稿人、产出 Major/Minor 分级意见[^c4-1]。
- **注意点**：
  - 「互盲」是关键词：三份报告要像三位互不通气的审稿人各自写的，而不是同一套意见换三遍说法。收到产物时检查三份意见是否有实质差异。
  - 这只是**模拟视角**，不能替代真实审稿，也不代表你的稿子真的过了这一关。

> [!tip] 大白话：互盲审稿像三间独立隔间的匿名打分
> 三个评委各坐一间屋子、看不到彼此打分，最后你才把三份成绩单一并打开。这样得到的评价才不容易被「从众」带偏——你要检查 AI 是不是真的给了你三份独立意见，而不是一份意见抄三遍。

#### 场景 6｜返修回复：逐点回复 + cover letter + 标红（推断命中 `nature-response`）

- **何时用/触发词**：收到期刊返修邮件（major / minor revision），要写 rebuttal。
- **官方提示词**：

```text
根据这封返修邮件，为每位互盲审稿人分别写逐点回复和 cover letter，标出修改稿需标红位置
```

- **期望产物**：为**每一位**审稿人分别准备的逐点回复 + 一封 cover letter + 修改稿中需要标红的位点清单。`nature-response` 的定位就是解析返修邮件、产出这套返修季材料，并带 LaTeX 模板[^c4-1]。
- **注意点**：
  - **把返修邮件的原文整封粘贴给它**，别只转述大意——逐点回复要求点对点对应审稿意见。
  - 与场景 5 呼应：审稿意见是「互盲」的，回复也要分开写，每位审稿人只看到针对自己意见的回复。
  - 标红位置清单是给「修改稿标红」用的，拿到后记得回到原文一一核对，别漏标也别多标。

#### 场景 7｜引用数 / 严格他引 / 引用者画像（推断命中 `nature-academic-search`，可叠加 `nature-citation` / `nature-ref-verifier`）

- **何时用/触发词**：想知道一篇文章被引得怎么样、引用者里有没有高影响力学者，或核验一组引文。
- **官方提示词**：

```text
整理这篇文章的引用数、严格他引数、DOI，看引用者里有没有院士/Fellow/大牛
```

- **期望产物**：该文的引用数、**严格他引数**（排除自引后的口径）、DOI，以及高影响力引用者的画像。`nature-academic-search` 的定位就是多源检索 + 严格他引审计 + 高影响力引用者画像，并带 MCP server（arxiv / crossref / pubmed / sciencedirect / scopus）[^c4-1]。
- **注意点**：
  - 这条线对配置最敏感：第 3 章提过，它的 MCP server 需要单独 `pip install` 依赖并配置 `PUBMED_EMAIL`，Scopus/ScienceDirect 走你本机的机构凭据。
  - 检索类产物**务必多源人工核对**——「引用数」「他引」在不同数据库口径不同，AI 给的数字只能当线索，不能直接写进简历或结题报告。
  - 严格他引需要先把「哪些引用是作者自引」排除掉，注意它是否真的做了这一步。

#### 场景 8｜投稿级科研图 / 示意图草稿（推断命中 `nature-figure`）

- **何时用/触发词**：方法结果已定，需要投稿级数据图，或想要一张论文示意图草稿来启发排版。
- **官方提示词**：

```text
根据这段方法和结果，帮我生成投稿级科研图或论文示意图草稿
```

- **期望产物**：投稿级科研图（Python/R 绘图产物，通常是 `.svg`/`.png` 及对应脚本），或 AI 生成的示意图草稿。`nature-figure` 的定位是 Python/R 投稿级科研图 + OpenRouter GPT Image 2 论文示意图草稿[^c4-1]。
- **注意点**：
  - 触发后会遇到 gate：**后端选 Python 还是 R**。只答这一个问题即可，选择会被记住（如 `nature_figure_backend.py set python`）[^c4-2]。
  - AI 示意图那一路需要配置 OpenRouter key；没有 key 就只走数据图那一路。
  - 状态虽是 Stable，但社区对绘图质量评价分化（属低可信二传），出图后仍要按期刊 Figure 规范自查字号、分辨率与配色。

### 4.4 端到端可验证工作流解剖：以 `nature-citation` 为例

单个场景的提示词解决了「怎么开口」，但 nature-skills 真正区别于「让 AI 随手查点文献」的地方，是它把一类任务做成了**可验证、线性参数化的工作流**。官方文档与第三方源码解读以 `nature-citation` 为典型例子：你给它一段文本或一个 DOI，它会按固定管线跑完，而不是「凭感觉给你列几篇参考文献」[^c4-2]。

`nature-citation` 的职责是：为一句 claim / 一段文本找出**严格落在 Nature/CNS 系范围**的支撑文献，并导出文献管理软件可读的格式。它的管线大致如下[^c4-2]：

```text
输入：文本 / claim / DOI
   │
   ▼
① segment_text() 分段        —— 把长文本切成 ≤700 字符的片段
   │                          （适配检索接口，也让每条候选能对齐到原文某句话）
   ▼
② Crossref 检索               —— 走 polite pool + 退避重试
   │                          （礼貌检索池 + 限速退避，避免被封）
   ▼
③ in_scope() 期刊族过滤       —— 只保留 cns/nature/science/cell/flagship
   │                          等 Nature/CNS 系旗舰期刊
   ▼
④ 去重
   ▼
⑤ 导出 ENW / RIS / Zotero RDF —— 三种文献管理格式，直接进 Zotero/EndNote
   ▼
⑥ --with-artifacts            —— 额外产出 JSON / TSV / Markdown / 可筛选 HTML
```

为什么叫「可验证」？因为**每一步都有确定的输入与输出，产物落到磁盘上你能亲眼检查**：分段函数有明确的字符阈值，检索走标准协议，过滤规则是白名单式的 `in_scope()`，导出格式是标准文献格式。带上 `--with-artifacts` 后，产物形态大致如下（示意）：

```text
output/
├── references.enw        # EndNote
├── references.ris        # RIS
├── references_zotero.rdf # Zotero RDF
├── report.json           # 机器可读明细
├── report.tsv            # 表格
├── report.md             # Markdown 报告
└── report.html           # 可筛选的浏览器视图
```

为什么叫「线性参数化」？因为输入是一段文本 / 一个 DOI，整条链路的参数（分段长度、期刊白名单、导出格式）都是显式可调的，你可以在不同段落、不同论文上重复跑同一套流程，而不需要每次人工指挥。对照第 1 章的一次调用流程：描述任务 → 路由 → gate → 执行 → preflight 校验 → 交付产物与来源标注[^c4-2]——`nature-citation` 就是这条流程里「可验证工作流」的样板。

> [!tip] 大白话：可验证工作流像工厂流水线带质检
> 每一步是固定工位：切料（分段）→ 采购（检索）→ 筛料（期刊过滤）→ 打包（导出）。每个工位都有明确标准和产出记录，所以你随时能回头查「这批料是哪个工位筛掉的」。相比之下，让 AI「随便帮我找几篇文献」就像没有流水线、全靠老师傅手感——快但没法复核。

结合上一节的检索场景，三条引用相关技能是这样分工的：`nature-academic-search` 回答「这篇文章被谁引了、引用者是谁」，`nature-citation` 回答「我这个论断该引用哪些 Nature/CNS 系文献」，`nature-ref-verifier` 回答「我列出的参考文献字段对不对」。写论文时三者可以串成一条流水线，但无论哪一条，**提交前都要人工多源核验**——这点在下一章会展开。

### 4.5 交付物形态与来源标注意识

跑完 8 个场景，你会收到不同形态的产物。提前知道「该收到什么」，是判断技能有没有正常工作的第一道关卡：

| 场景 | 推断命中技能 | 主产物形态 |
| --- | --- | --- |
| 1 读论文中英对照 | `nature-reader` | `.md` 全文（图文对应、来源锚点、公式渲染） |
| 2 组会汇报 PPT | `nature-paper2ppt` | `.pptx`（保留关键图件与来源标注） |
| 3 润色/翻译 | `nature-polishing` | 改写后文本 / `.tex`（可含 LaTeX 修复） |
| 4 摘要引言起草 | `nature-writing` | `.md` 草稿 |
| 5 预投稿互盲审稿 | `nature-reviewer` | 三份独立 reports + 综合意见 |
| 6 返修回复 | `nature-response` | cover letter + 逐点回复 + 标红清单 |
| 7 引用/他引画像 | `nature-academic-search` | 引用数/他引/DOI + 引用者画像报告 |
| 8 科研图/示意图 | `nature-figure` | `.svg`/`.png` + 绘图脚本（数据图）；示意图草稿（AI） |
| 支撑文献导出（4.4） | `nature-citation` | `.enw` / `.ris` / Zotero RDF + 附带 artifacts |

读这张表时有两点「元意识」要建立：

**第一，产物格式本身是有信息量的。** 如果你在场景 2 期待一份 `.pptx`，结果只收到一段文字总结，说明技能没有按预期工作（或没触发对技能）。`.enw`/`.ris`/`.rdf` 这类格式不是给人读的，而是给 EndNote/Zotero 读的——收到它们说明流程真的走到了导出这一步。

> [!tip] 大白话：`.enw/.ris` 是给文献管家看的「购物清单」
> 你不需要读懂清单上的条形码，只要确认清单是标准格式、能扫进 Zotero 就行。真正要你眼睛看的，是清单里的条目「是不是你该引的那些」。

**第二，格式完整 ≠ 内容可信。** 官方设计原则强调「一手来源优先、输出优先」，所以在提示词模板里你会反复看到「保留来源标注」「图文对应」「来源锚点」这类要求[^c4-1]——这是设计层面对可追溯性的约束。但**「有来源标注」和「来源是对的」是两回事**：读者类产物要检查锚点是否真指向原文对应位置，引用类产物（场景 7、4.4 的导出）必须逐条人工多源核对，写作与审稿类产物一律按「草稿 + 核验清单」对待。

> [!warning] 交付物形态只是「容器」，不替你做学术判断
> 一份排版漂亮的 `.md`、一叠格式规范的 `.enw`，都只代表流程跑完了，不代表结论经得起推敲。凡是会进投稿系统、结题报告或简历的内容，把「人工核验」当作流程的最后一环，而不是可选项。

#### 本章小结

- 用法分两档：**拿不准就自然描述任务**让路由器匹配，**确定了就显式写「使用 `nature-xxx`」**；带 gate 的技能只问一个关键问题，答一次并被记住。
- 官方提供 8 类可整段复制的场景提示词，覆盖「读论文中英对照、组会 PPT、Nature 风格润色、摘要引言起草、互盲审稿、返修回复、引用他引画像、科研绘图」；每个场景都给出了期望产物形态与注意点。
- 提示词与技能的对应关系来自本次研究的推断（inference）：模板句是官方原文，但「大概率命中哪个技能」需结合你的安装范围与实测确认。
- 以 `nature-citation` 为代表的可验证工作流，把「查支撑文献」从「让 AI 凭感觉列文献」变成「分段 → Crossref 检索 → 期刊族过滤 → 去重 → 导出 ENW/RIS/RDF → 附带 artifacts」的线性管线，产物可检查、可复跑。
- 交付物形态（`.md` / `.pptx` / `.svg` / `.enw` …）是判断技能是否正常工作的信号，但「有来源标注」不等于「来源可信」——引用与写作类产物必须在人工核验后才算完成。

[^c4-1]: nature-skills 官方 README（S1）：<https://github.com/Yuan1z0825/nature-skills>
[^c4-2]: 《今日开源[45期] nature-skills 项目解读》（S5，zhang-yd）：<https://www.cnblogs.com/zhang-yd/p/22151100>
[^c4-3]: 《Nature Skills：论文到专利全流程》（S6，iTech）：<https://www.cnblogs.com/itech/p/22851434>

## 第五章：避坑与最佳实践

> 本章要解决一个问题：**装上了、也能触发，为什么跑出来的东西时好时坏、甚至直接翻车？** 前几章教"怎么装、怎么用"，这一章专讲"哪里会坏、凭什么信它、怎么守住边界"。第 3 章的命令矩阵这里只引用不复述。全章按五节走：官方明示的坑（高可信）→ 质量与成熟度管理 → 合规与账号边界 → 第三方批评与社区反馈（分级呈现）→ 最佳实践清单。每一条都尽量压成能扫读的短块，标注了信源与可信度，你可以只读自己关心的那几段。

### 5.1 必踩的坑（官方高可信）

下面是官方文档与仓库结构层面明确写出的坑位（S1 §5.1/§5.2/§5.3/§5.4），可信度最高，建议逐一对照。

> [!warning] 坑 1：只复制 SKILL.md 会坏
> 症状：装完路由不触发，或触发了却读不到 `manifest.yaml` / `static/`，报"找不到对应片段"。原因：`SKILL.md` 只是**路由器**（第 1 章心智），真正干活靠同目录的 `manifest.yaml`、`static/`、`references/`、`scripts/`、`assets/`。正确做法是**整目录安装**——`npx skills` 和仓库脚本做的都是整目录复制。所谓"装好了"在文件系统里长这样：
> ```text
> ~/.codex/skills/
> ├── nature-reader/          # 一个技能单元 = 一个目录
> │   ├── SKILL.md            # 路由器
> │   ├── manifest.yaml       # 轴→文件 声明
> │   ├── static/  references/  scripts/  assets/
> └── nature-shared/          # 共享支持包（同级依赖）
> ```
> 大白话：只复制 `SKILL.md` 约等于只拿走 App 图标，双击当然打不开。

> [!warning] 坑 2：运行时依赖不会自动安装
> 症状：跑 `nature-paper-to-patent` 提示缺 Playwright；跑 `nature-academic-search` 的 MCP server 连不上。原因：安装/同步脚本**只复制技能文件，不装 Python/Node/Playwright/MCP 依赖**（S1 §5.3）。缓解：每个技能装完翻一下它自带 README 的依赖段，按需补装，例如专利技能要 `pip install -r .../requirements.txt` + `python -m playwright install chromium`，检索 MCP 要装自己的 `requirements.txt` 并配 `PUBMED_EMAIL`（具体命令见第 3 章，不在此复述）。别把"技能装好了"当成"环境就绪了"。

> [!warning] 坑 3：目录名 ≠ frontmatter 技能名（`researchwrite`）
> 症状：照着目录名 `nature-proposal-writer` 去选技能，路由不命中，或在 `--list` 里找不到它。原因：技能**触发名**是 `SKILL.md` frontmatter 里的 `name`，这个技能的值是 **`researchwrite`**（S1 §5.1）。`npx skills --list` 显示的、提示词里显式"使用 `researchwrite`"用的，都是 frontmatter 名。第 2 章速查表因此特意给了"目录名 / 触发名"两列，查的时候别只看目录名。

> [!warning] 坑 4：单独装依赖共享包的技能，会漏 `nature-shared`
> 症状：`nature-reader` / `nature-paper2ppt` / `nature-polishing` / `nature-writing` 单独装完，跑起来报找不到 `../nature-shared/`，或行为残缺。原因：这些技能的 `manifest.yaml` 会引用同级共享包 `nature-shared`（唯一的越目录白名单，见第 1 章）。缓解：按需安装时把共享包一起带上，一条命令多个 `--skill`，如 `--skill nature-reader --skill nature-shared`（写法见第 3 章）。判断哪些技能依赖它，看第 2 章依赖列的标注。

> [!warning] 坑 5：装完不新开会话，等于没装
> 症状：装完立刻在当前会话里自然描述任务，路由像完全没生效。原因：Codex 在**会话启动时**加载 skills 目录，装完的目录不会热插拔进正在跑的会话。缓解：装完**开一个新的 Codex 会话**，再丢官方模板提示词做最小验证（见 5.5）。

> [!warning] 坑 6：Claude Code 环境不能跑 `update-codex-skills.sh`
> 该仓库脚本只同步 **Codex** 的 `~/.codex/skills`，在 Claude Code 环境执行不会把技能装进 Claude Code（S1 §5.2/§5.3）。本笔记主环境是 Codex，这条主要提醒双环境用户：Claude Code 想用同一套技能，走本地 clone + wrapper，或把 `autoupdate-skills.sh --dest` 指到 Claude Code 的 skills 目录。别指望"跑过官方脚本 = 两边都装好"。

### 5.2 质量与成熟度管理

装好、能触发，**不等于产物可以直接信**。这一节管三层：成熟度标签、LLM 编造风险、交付物该怎么用。

**成熟度分布**：约 19 个可触发技能里只有 **4 个 Stable**（`nature-figure` / `nature-polishing` / `nature-ref-verifier` / `nature-literature-pipeline`），其余 15 个是 Beta 或 Draft（S1 §6；S5 §5.2）。标签含义在第 1 章给过，落到使用动作：

| 标签 | 含义 | 使用动作 |
|------|------|---------|
| Draft | 未实战测试 | 当草稿，先最小验证再当真用 |
| Beta | 示例跑通、边界存疑 | 当草稿 + 人工核验清单 |
| Stable | 经真实学术内容验证 | 可直接进流程，交付物仍建议核对 |

**LLM 编造风险与官方缓解**：第三方解读一致指出，产出质量高度依赖底层模型，存在编造风险（S5 §5.2/§5.3；S6）。官方对此有边界自觉，常见缓解手段：

- **metadata-only candidate**：检索类先把候选标成"仅元数据"，不替模型编造数值；
- **来源锚点 / 逐字段核验**：`nature-ref-verifier` 对作者/标题/年份/卷期/页码逐字段多源比对，`nature-citation` 只收严格期刊族范围内文献；
- **显式标"草稿"** + preflight 校验：写作、审稿、专利类技能默认不承诺可直接投稿。

但这些缓解**替代不了人工核验**——它们降低的是"编造发生且不吭声"的概率，不是把错误率清零。

**交付物一律当「草稿 + 核验清单」**（research §5.4）：

| 交付类型 | 代表技能 | 官方缓解 | 你的核验动作 |
|---------|---------|---------|------------|
| 写作/润色 | `nature-polishing`、`nature-writing` | Nature 风格模板、LaTeX 修复 | 逐句看事实与数据有没有被"顺滑地改掉" |
| 审稿/返修 | `nature-reviewer`、`nature-response` | 三份互盲 reports、"全部定稿后再综合" | 只取结构与方法建议，措辞按自己稿件重写 |
| 引用/检索 | `nature-citation`、`nature-academic-search`、`nature-ref-verifier` | Crossref 检索、严格期刊过滤、逐字段核验 | 交付前人工抽样 + **至少一条非模型渠道**复核 |

### 5.3 合规与账号边界

> [!warning] 下载与检索合规：技能只放大你已有的权限，不给新权限
> `nature-downloader` 的定位是**合法获取**（S1 §5.3；S5 §5.2）：它依赖你已有的合法通道——图书馆订阅、CARSI 机构认证、开放获取（OA）、个人登录态。有没有权限由你的机构订阅决定，技能只负责在你有权访问的前提下把"下载全文"自动化。它不能、也不该绕开订阅墙。用之前先确认自己所在机构覆盖了这篇文献。

其他账号边界（S1 §5.3；S5 §5.2）：

- **凭据只放本机**：Scopus / ScienceDirect 用本机凭据、`PUBMED_EMAIL`、`nature-figure` 的 OpenRouter key，一律放环境变量或本地配置，**不写进仓库、不进技能目录、不进提示词**。
- **付费 API 与账号风险由使用者承担**：跑重活前先问一句——这个技能背后要调哪个外部服务？花不花钱（如 OpenRouter 出图）？用的是谁的账号？第三方批评（见 5.4）也点名了这条，属于"工具本身无法替你背锅"的部分。

### 5.4 第三方批评与社区反馈（分级呈现）

nature-skills 不是没有批评。这里按**可信度分两档**摆出来，档位不同，你该给它的权重不同。

**中高可信：第三方深度解读（S5 §5.2 / S6，基于源码拆解）**

- **产出质量依赖底层 LLM、有编造风险** → 官方有缓解但仍需人工（已在 5.2 展开）；
- **成熟度不均**：19 个里仅 4 个 Stable，多数 Beta/Draft 未经充分真实学术验证；
- **外部依赖/合规偏重**：Scopus、CARSI、OpenRouter、Playwright 一长串，账号与合规风险都在使用侧；
- **README 含代充/知识星球导流广告**，对只想用技术的用户显得喧宾夺主；
- **强绑定宿主代理契约**：Router 的分层收益建立在"Agent 会老实读 manifest 与 fragments"之上；如果宿主代理偷懒不读片段，收益就失效。→ 你在产物里应能看到它确实走了路由（来源锚点、分段结构、manifest 对应的行为），否则换更直给的提示词。

> [!note] 低可信档：S7/S8 是社区二传，未直接验证
> 下面三条来自 S7（头条实测报告）与 S8（LINUX DO 讨论串），**原文未能抓取，经检索代理转述，属于"社区二传、未直接验证、个体体验不一"**，只当作试跑前的心理预期，不作结论：
> - 润色有"AI 味"、行文冗长，防 AI 率需人为调整句长；
> - 绘图（`nature-figure`）质量评价分化；
> - 多数技能 Draft/Beta，需人工把关。
> 用你自己任务实测的结果，永远比二传观点更可靠（分歧记录见 02 素材 §4：社区评价好坏参半，归因到"体验因模型/任务而异"）。

### 5.5 最佳实践清单

把前四节反过来，就是一套可执行的动作。以下 5 条按"装 → 验 → 用 → 交付"的顺序排。

> [!tip] 最佳实践 1：最小验证先行
> 装完**立刻新开 Codex 会话**，丢一句官方模板提示词（第 4 章的 8 类场景任选一条最贴近自己的），确认**产物形态**对了（`.md` / `.pptx` / `.svg` / `.enw`），再进入真实任务（research §5.3）。先让技能在一个你知道正确答案的小样本上跑通，别拿第一篇重要论文当试验田。

> [!tip] 最佳实践 2：按需装 vs 整库 clone，先想清楚再动手
> 三条路对应三种诉求（决策树详见第 3 章）：只要 1–3 个技能 → `npx skills` **按需装**（记得带 `nature-shared`）；想整库跟上游更新 → clone + `update-codex-skills.sh --pull/--check/--prune`；想长期自动更新 → 专用 clone + SessionStart hook。**别一上来就全量装 19 个**——装得越多，依赖与核验负担越大。

> [!tip] 最佳实践 3：Windows 用户装多技能优先 `--copy`
> `--copy` 是**复制文件而非 symlink**，Windows 无管理员权限或 symlink 受限时最稳（S2）。另外整库脚本 `update-codex-skills.sh` 依赖 `rsync`，Windows Git Bash 下先确认 `rsync` 可用，否则脚本会卡在同步这一步（research §5.2）。

> [!tip] 最佳实践 4：引用/写作类产物，交付前人工多源核对
> 引用三件套（`nature-citation` / `nature-academic-search` / `nature-ref-verifier`）的产物，进参考文献列表或投稿前**抽样 + 多源核对**一遍；写作与审稿类产物当"草稿 + 引文核验清单"，不直接当定稿。核验是使用者的动作，官方缓解只是降低风险（5.2）。

> [!tip] 最佳实践 5：与 Obsidian 工作流结合
> 两个技能产物可直通 vault：`nature-reader` 产出的是带来源锚点的全文 Markdown 精读，`nature-experiment-log` 本就走 Obsidian 实验日志。跑科研流水线时顺手把产物落进既有笔记体系，避免"技能产出一份、自己又抄一份"的重复劳动（research §5.5）。

#### 本章小结

- **六个官方高可信坑**，四个集中在"安装语义"：整目录装、依赖单独装、触发名用 frontmatter name、别漏 `nature-shared`；另两个是流程纪律：装完新开会话、Claude Code 别跑 Codex 专属脚本。
- **质量**：19 个技能仅 4 个 Stable，15 个 Beta/Draft；写稿、审稿、引用类交付物一律当"草稿 + 核验清单"，官方缓解（metadata-only、来源锚点、逐字段核验）替代不了人工。
- **合规**：`nature-downloader` 只放大你已有的图书馆/CARSI/OA 权限；付费 API 费用与账号风险由使用者承担，凭据不进仓库。
- **批评要分级信**：S5/S6（第三方源码解读）中高可信，可当改进路线；S7/S8 是社区二传、未直接验证、个体体验不一，只当心理预期。
- **五条最佳实践**：最小验证、按需 vs 整库、Windows `--copy`、引用多源核对、产物直通 Obsidian。

## 第六章：上手行动清单与生态进阶

> 前五章把"它是什么、有哪些技能、怎么装、怎么用、怎么避坑"都讲完了。最后一章回答两个收尾问题：**我从哪里开始动手？这套技能在更大的 AI 技能生态里站在什么位置、下一步往哪走？** 先给一张 30 分钟可执行的上手清单，再谈生态位置、与 Claude Code 的取舍、四个待实测的开放问题，最后给出从"用技能"到"写技能"的进阶路线。全章无代码，是整本指南的收尾自检页。

### 6.1 30 分钟上手行动清单

清单假设前置已满足：本机能跑 Codex、Node.js ≥ 18、对 `SKILL.md` / 技能包 / `npx skills` 有基本概念（第 1 章前置要求）。核心策略一句话：**装一个最小的 → 最小验证 → 立刻跑一个真实小任务**，而不是一上来全量装 19 个。

> 时间口径为「新手第 1 次照做」的宽松估计；整库同步路线会超出 30 分钟，本清单默认走按需安装。

**阶段 1（0:00–0:05）前置确认与安装**

- [ ] 确认 Node.js 版本：`node -v` 输出 ≥ 18
- [ ] 只挑 1 个最贴近自己工作的技能（速查见第 2 章）。新手建议从 `nature-reader` 这类"输入 PDF → 输出 Markdown"的低风险、产物好检查的技能入手
- [ ] 用 `npx skills` 按需安装，**记得把依赖的 `nature-shared` 一起装**：
  ```bash
  npx skills add Yuan1z0825/nature-skills --global --agent codex --skill nature-reader --skill nature-shared --yes --copy
  ```
  （Windows 用户保留 `--copy`，避开 symlink 权限问题；装的是**整个技能目录**，不是只复制 SKILL.md，详见第 3、5 章）

**阶段 2（0:05–0:10）最小验证**

- [ ] 开一个**全新的** Codex 会话（第 3 章"开新会话"规则，旧会话不会加载新技能）
- [ ] 丢一句官方模板提示词做冒烟测试。例（读论文）：「把这篇 PDF 做成图文对应的中英文对照 Markdown reader」
- [ ] 确认产物形态正确：得到带来源锚点、图文对应的 `.md`，而不是一段聊天回复。产物形态不对 → 直接回第 5 章排错清单（九成坑位都写在那一章）

**阶段 3（0:10–0:25）跑通一个真实场景**

- [ ] 拿一篇自己手头真实的论文/段落，套第 4 章对应提示词模板，跑一个 20 分钟内能完成的小任务（精读一篇 / 润色一段 / 出一页图，选一个就好）
- [ ] 对产物做一次「草稿 + 核验」检查：引用锚点能回查、没有编造数值（第 5 章质量边界，Beta/Draft 技能尤其要查）
- [ ] 顺手记录：这次用的是自然语言触发路由，还是显式点名「使用 `nature-xxx`」？结果符合预期吗？（这是 6.4 第 1 条开放问题的第一手实测数据）

**阶段 4（0:25–0:30）复盘与下一步**

- [ ] 复盘调用链：哪种触发方式更稳？把结论记进自己的使用笔记
- [ ] 决定后续安装策略：按需继续加技能，还是转整库同步/自动更新（决策树见第 3 章；整库与 hook 自动更新不在 30 分钟内，另约时间做）

如果中途卡住，原则只有一条：**先回第 5 章对照已知坑，再考虑是不是新问题**。不要重装三遍才想起"装完没开新会话"。

### 6.2 生态位置：skills 生态解决的是「懂行」

nature-skills 不是孤立项目。你已经在用 `npx skills`（vercel-labs/skills 这套 CLI/规范）和 `SKILL.md`；Matt Pocock Skills、superpowers 一类通用技能库也活在同一生态里。nature-skills 站的位置，是其中**「研究垂直」那一格**。

第三方解读 S6 给了一个判断：**skills 生态解决的不是"能不能调用工具"，而是"懂行"**——把某个领域内行才知道的标准流程、产物形态、质检点固化进技能。通用库给你"做事的方法"，垂直库给你"这个领域怎么做才算合格"。[^c6-1]

Anthropic 推 **Agent Skills 规范**后，垂直领域技能库成为一个新竞争面：只要遵守同一套技能规范，同一份技能包理论上可以**零适配跑在多个宿主平台上**（S6 称口径为 5 个平台，未逐一枚举）。落地含义是：你在 Codex 里学会的这套技能，换一个遵循规范的宿主时，技能包本身不必重写——但"装得上"不等于"触发得稳"，后者按宿主实测（见 6.4）。

与通用技能库的差异，落在**研究垂直深度**，而不是通用工程能力。仓库级对照如下（S5 §5.1/§6；"通用库"行为第三方观察，非官方对比）：

| 维度 | 通用技能库（Matt Pocock Skills / superpowers 等） | nature-skills（研究垂直） |
|------|------|------|
| 解决的问题 | 通用开发/效率工作流 | 科研工作流：读论文、投稿、返修、绘图、引用核验、专利 |
| 内容厚度 | 偏"方法 + 少量模板" | 内容厚重、工程化完整：CI 门禁、MCP server、单元测试、双语 README 镜像 |
| 典型产物 | 多为文本/代码产出 | `.md / .pptx / .svg / .enw / RIS / Zotero RDF` 等科研产物 |
| 迁移成本 | 跨领域通用 | 绑定科研场景；换研究领域需自行改写技能内容 |

引用纪律：官方 README **没有**提供与 Matt Pocock Skills / superpowers 的直接对比，上述生态位置主要是第三方（S6）的观点，部分是本研究推断。请把它当"生态观察"，不是官方口径。

> [!tip] 大白话
> 把通用技能库想成"家用工具箱"，垂直技能库想成"老师傅的专用车间"：工具箱里是扳手电钻谁都能用，车间里是"处理这种料该走哪几道工序、成品该验哪几个点"的行活。所以 nature-skills 卖的不是"会读 PDF"，而是"像科研老手一样把论文读成带证据链的卡片、把返修信回成能直接投的稿"。

### 6.3 与 Claude Code 的取舍对照

nature-skills 官方把 **Codex 当作一等公民**：README 的安装、仓库维护脚本、验证命令全部围绕 Codex（S1 §5.1/§5.3）。Claude Code 路线存在，但脚本维护是短板。本节对照建立在笔记意图"主用 Codex、Claude Code 仅作对照"之上。

**官方主推的 Codex 路线**（第 3 章已详述）：

- 按需装：`npx skills add ... --agent codex`，落到 `~/.codex/skills/`
- 整库跟上游：clone + `scripts/update-codex-skills.sh --pull / --check / --prune`
- 长期自动更新：`scripts/autoupdate-skills.sh` + `SessionStart` hook

特点是**维护脚本齐备**——同步、校验、清理、节流更新都有人写好。

**Claude Code 路线的现实**：仓库脚本 `update-codex-skills.sh` 只同步 Codex，**Claude Code 不能直接跑**（S1 §5.2/§5.3）。想用只能自维护，社区通行做法是**本地 clone + 自写 wrapper**：clone 仓库后，用你自己的拷贝脚本把技能**完整目录**（`SKILL.md` + `references/` + `static/` + `manifest.yaml` + `scripts/` + 依赖的 `nature-shared/`）同步进 Claude 的 skills 目录；或把 `autoupdate-skills.sh` 的 `--dest` 指向你自己的目录。关键规则与 Codex 一致：**不要只复制 SKILL.md**。本次研究未逐字核验 README §5.2 的 Claude Code 安装命令，精确做法以仓库 README 为准（标为需实测项）。

| 维度 | Codex 官方路线 | Claude Code（本地 clone + wrapper） |
|------|------|------|
| 维护脚本 | 官方提供（update / autoupdate / hook） | 无官方脚本，同步、更新自己写 |
| 适配地位 | 一等公民 | 二等公民：README 有章节，但仓库脚本不覆盖 |
| 上手成本 | 最低 | 中：多一层自维护 |
| 触发可靠性 | 官方主推场景 | 未系统验证（见 6.4） |

**何时值得用 Claude Code**：判断锚点不是"哪个模型更强"，而是**你日常主力 agent 是谁**。值得用 Claude Code 当 host 的情形是：① 你已经重度生活在 Claude Code 里，不想为科研技能再双开一个终端 agent；② 你接受技能包同步自维护；③ 你愿意先花几次真实会话确认 router 触发在 Claude Code 上可靠（不能默认 Codex 的体验等于 CC 的体验）。

第三条尤其要当真：第 5 章引过第三方批评——技能**强绑定宿主 agent 契约**，如果宿主 agent"偷懒不读片段"，Router 分层收益会失效（S5 §5.2）。不同宿主对 `SKILL.md` 的遵从度可能不同，这是结构性的、需要实测的点，不是装上就能假设一样。反过来，如果你已选定 Codex，就没有理由为同一套技能再维护第二套安装——那是高维护成本、低新增收益。

> [!tip] 大白话
> 同一套电器，一边是官方上门安装（Codex 路线），一边是你按说明书自己接线（clone + wrapper）。两条路都能点亮，区别在"坏了谁负责、要不要自己保养"。想清楚你长期住哪个屋（主力 agent），就给哪个屋接线，别两间屋都拉一套要自己保养的线。

### 6.4 待实测的开放问题

以下是研究阶段（`02_deep_research.md` §6）留下的、本笔记**无法替你拍板**的验证项。它们不是"缺点清单"，而是"需要你在真实会话里收集数据"的自测单。每条给三件事：问题是什么、为什么重要、怎么自己测。

**1. Router 触发稳定性：description 匹配是否可靠**
nature-skills 的核心玩法是"自然描述任务 → 靠 `description` 触发词路由到技能"。这个匹配在真实 Codex 会话里命中率多高，官方没有系统评测；Router 架构又依赖宿主遵守"只读该读的片段"的契约。自测方法：每次真实任务记一行"触发方式 + 是否命中预期技能"，攒 10 次看命中率；命中不稳时，退化方案就是第 4 章说的——显式点名「使用 `nature-xxx`」。

**2. Windows 上 symlink vs copy 的真实表现**
研究只确认了两件事：官方推荐 Windows 用户用 `--copy`（避开 symlink 权限问题，S2）；`npx skills` 默认可能建 symlink。但"symlink 在 Windows 上到底会不会失败、`--copy` 装完后续 `update` 是否需要重装"没有一手实测。自测方法：装完看 `~/.codex/skills/` 下是指向仓库的链接还是真实文件副本（`ls -l` / `dir`），再分别走一次 `add` 与 `update` 对比表现。

**3. `nature-academic-search` MCP server 的配置成本与检索质量**
这个技能是检索/严格他引/引用者画像的核心，但要先 `pip install -r .../mcp-server/requirements.txt` 并配置 `PUBMED_EMAIL`（第 3 章）。配置路径有文档，"多花多少时间、检索准不准、他引审计可不可信"则无一手实测。自测方法：按第 3 章配完，拿一篇自己熟悉引用情况的论文跑一次"严格他引 + 引用者画像"，与人工核对结果。

**4. 社区负面反馈（S7/S8）无法核实**
第 5 章提到的"润色有 AI 味、绘图质量分化、多数 Draft/Beta 需把关"来自两条未能抓取原文的社区二传（头条、LINUX DO），研究只拿到转述，个体体验差异大。自测方法：自己用 `nature-polishing` 和 `nature-figure` 各跑一单真实任务，结论以你的实测为准，别把二传当结论。

（另有一条低优先级：官方在线网站 yuan1z0825.github.io 的交互式导航未深抓；需要更全的技能演示可自行前往，不影响上手。）

> [!tip] 大白话
> 把这几条想成菜谱角落的注脚"各家灶台火力不同，需实测"——菜谱（本笔记）把步骤写清楚了，但你家灶台（Windows？Claude Code？哪个模型？）的火力只有你开火才知道。所以别问"到底行不行"，直接跑一单，记录比结论值钱。

### 6.5 进阶路线：从「用技能」到「为实验室定制技能」

上手之后有两条自然进阶路，都不需要等官方出新技能。

**路线 A：为实验室写自己的技能。** nature-skills 是 Apache-2.0，且把"可扩展"写进了设计原则（第 1 章原则⑤）；工程上 CI 门禁、单元测试、双语 README 镜像都齐（S5 §5.1），是照着写自有技能的好模板。最小起步不是从空文件开始，而是**复刻一个离你工作最近的现有技能**的目录骨架，把"轴 + 片段"的内容换成你实验室的流程：

```text
my-lab-skill/                  # 新技能目录 = 一个可安装单元
├── SKILL.md                   # 路由器：frontmatter(触发名/描述) + 路由决策，不写长篇指令
├── manifest.yaml              # 声明"轴(axes) → 文件"：always_load 常驻 / on_demand 按需
├── static/
│   ├── core/                  # 常驻核心（必读）
│   └── fragments/             # 按需片段（命中轴才读，省上下文）
├── references/                # 参考资料（可含 workflows/）
├── scripts/                   # 可执行脚本（取数、转换、校验）
├── templates/                 # 产物模板（.md / .xlsx / .pptx …）
└── assets/                    # 静态资源
```

两条硬约束要记住：manifest 路径校验白名单只允许 `../nature-shared/` 越出技能目录（第 1 章，由 `validate-skill-metadata.py` 强制）——若你的技能要复用公共逻辑，正确做法是依赖 `nature-shared`，而不是各写各的；另一点是结构必须完整，"只复制 SKILL.md 会坏"在写技能时同样成立。写"研究垂直"技能 ≠ 写一条长提示词：把内行的标准流程（分几步、先做哪步、产物长什么样、验收哪几个点）固化成**分层片段**，才是这个生态里"懂行"的价值所在。

**路线 B：让技能产物直通 Obsidian。** 两个技能和笔记工作流天然咬合：`nature-reader` 交付"图文对应、带来源锚点的 Markdown reader"，是 `.md`，可直接落入 vault；`nature-experiment-log` 的定位就是"实验图文音标准化记录 → Obsidian 实验日志"（Draft，产物当草稿）。落地建议：让产物先落 vault 的收件/临时目录，再按你自己的 Obsidian 规范补 frontmatter、标签与双链——不要让技能产物裸奔进正式笔记结构，格式统一这步留给你的美化/入库流程。

> [!tip] 大白话
> 从"用技能"到"写技能"，是从照菜谱做菜到自己写菜谱。最稳的入门不是凭空创作，而是拿一道离你最近的菜（现有技能）当底稿，把配料换成你实验室的流程。等你能把自己那套"先分几步、产物长什么样、怎么验收"写成分层片段，你就从食客变成了师傅。

#### 本章小结

- 30 分钟上手 = 装 1 个最小技能（务必带 `nature-shared`）→ 新会话最小验证 → 跑一个真实小任务 → 复盘触发方式；卡住就回第 5 章排错。
- 生态位置：skills 生态解决"懂行"；Agent Skills 规范下垂直技能库可跨宿主零适配；nature-skills 的差异在"研究垂直深度"（第三方观察，非官方口径）。
- 与 Claude Code 的取舍：Codex 官方脚本齐备、是一等公民；Claude Code 需本地 clone + 自写 wrapper，只在它已是你的日常主力、且接受自维护与"触发行为需实测"时才值得。
- 四个开放问题——Router 触发稳定性、Windows symlink/copy 表现、`nature-academic-search` MCP server 检索质量、S7/S8 社区反馈——留给你实测，记录比结论值钱。
- 进阶两条路：复刻现有技能骨架为实验室定制技能；`nature-reader` / `nature-experiment-log` 的 Markdown 产物直通 Obsidian vault。

#### 全篇收束

从第 1 章的 Router 心智，到第 2 章认全约 19 个技能、第 3 章装好并维护好、第 4 章跑通典型场景、第 5 章避开已知坑位，再到这一章的 30 分钟行动清单——本指南能教的部分到此为止。剩下的事情只有一件：把一个真实任务跑起来，用 6.4 的开放问题写下你的第一份实测笔记。这套技能到底好不好用，最终不由 README 或本指南回答，而由你手头那篇论文、那张图、那封返修信来回答。

[^c6-1]: 生态位置与"懂行"判断主要来自 S6 的第三方解读；官方 README 未提供与通用技能库的直接对比，本节相关表述以第三方观察呈现。

---

## 参考来源说明

本笔记正文中的 `S1` / `S2` / … 是研究阶段对信源的统一编号，出现形如 `（S1 §5.1）` 的标注时，`§` 后指该来源内的对应小节。各编号含义与可信度分级如下：

| 来源 ID | 指向 | 可信度 |
|---------|------|--------|
| S1 | nature-skills 官方 README（中文）：<https://github.com/Yuan1z0825/nature-skills> | 一手官方 |
| S2 | vercel-labs/skills CLI 文档（`npx skills` 工具官方） | 工具官方文档 |
| S5 | 今日开源[45期] nature-skills 项目解读（zhang-yd）：<https://www.cnblogs.com/zhang-yd/p/22151100> | 第三方源码解读（中高可信） |
| S6 | Nature Skills：论文到专利全流程（iTech）：<https://www.cnblogs.com/itech/p/22851434> | 第三方场景化转写（中高可信） |
| S9 | skillsmp nature-shared 详情页：<https://skillsmp.com/zh/creators/yuan1z0825/nature-skills/skills-nature-shared> | 低权威旁证（仅第 2 章 nature-shared 一节引用） |
| S7 | 头条实测报告（社区二传） | 低可信：原文未能抓取，经检索代理转述，个体体验不一，不作结论 |
| S8 | LINUX DO「AI 科研党 skill」讨论串（社区二传） | 低可信：同上，仅作试跑前的心理预期 |

正文中另出现的 `02 素材 §4`、`research §5.x`、`P2 §5` 等标识，是研究阶段工作文件（`02_deep_research.md`、收集笔记等）的内部引用，读者可直接忽略，不影响正文理解。凡标注「推断 / inference」的技能→场景映射，请以你本机实测为准。
