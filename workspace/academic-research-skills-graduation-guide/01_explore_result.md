# 01 探测结果 — ARS + nature-skills 双库毕设组合实操指南

> 阶段：P1 探测式收集　|　日期：2026-09-03
> 范围：6 个并行透镜（ARS×3 + nature-skills×3）回收候选信源，去重后形成 P2 深读基础。

## 候选信源汇总（按库）

### ARS — Imbad0202/academic-research-skills（v3.21.1，CC BY-NC 4.0，Claude Code 插件）

| 信源 | Tier | 评分 | 用途 |
|---|---|---|---|
| [README.zh-CN.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/README.zh-CN.md) | T1 | 5 | 官方中文总览：定位、4 大 skill、安装、边界 |
| [POSITIONING.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/POSITIONING.md) | T1 | 5 | "是什么/不是什么"，CC BY-NC、拒绝端到端自动研究 |
| [MODE_REGISTRY.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/MODE_REGISTRY.md) | T1 | 4 | 27 种模式单一事实源（含监督级别） |
| [docs/ARCHITECTURE.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/docs/ARCHITECTURE.md) | T1 | 5 | 阶段×skill×mode×gate 矩阵、人机 checkpoint |
| [academic-pipeline/SKILL.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-pipeline/SKILL.md) | T1 | 5 | 10 阶段全流程骨架（RESEARCH→…→FINALIZE） |
| [academic-pipeline/examples/full_pipeline_example.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-pipeline/examples/full_pipeline_example.md) | T1 | 4 | 端到端对话实录，示范每阶段怎么开口调用 |
| [academic-paper/examples/plan_mode_guided_writing.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/examples/plan_mode_guided_writing.md) | T1 | 4 | /ars-plan 苏格拉底逐轮实录（适合开题/大纲） |
| [docs/SETUP.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/docs/SETUP.md) | T1 | 5 | 安装前置唯一权威源（插件流、依赖、平台边界） |
| [hooks/run_guard.sh](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/hooks/run_guard.sh) + hooks/hooks.json | T1 | 4 | Windows python3 占位 stub、Git Bash 要求的代码实证 |
| [academic-paper/references/apa7_chinese_citation_guide.md](https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/references/apa7_chinese_citation_guide.md) | T1 | 4 | 中文引文=台湾惯例 APA 7.0 扩展（非 GB/T 7714）证据 |
| [GitHub Issue #425](https://github.com/Imbad0202/academic-research-skills/issues/425) | T3 | 3 | 社区已提出对齐中国高校 LaTeX 模板的诉求 |

### nature-skills — Yuan1z0825/nature-skills（Apache-2.0，Codex/Claude Code 多 runtime）

| 信源 | Tier | 评分 | 用途 |
|---|---|---|---|
| [README.md（中文主文档）](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/README.md) | T1 | 5 | 19 技能索引表 + Draft/Beta/Stable + 架构 + 安装 |
| [README_EN.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/README_EN.md) | T1 | 4 | 英文镜像，规范技能英文名引用 |
| [docs/open-source-agent-frameworks.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/docs/open-source-agent-frameworks.md) | T1 | 5 | Claude Code wrapper/subagent/slash vs Codex 脚本差异 |
| [skills/nature-proposal-writer/README.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-proposal-writer/README.md) | T1 | 5 | 开题/大纲状态机（compose/revise/hybrid 三模式） |
| [skills/nature-paper2ppt/README.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-paper2ppt/README.md) | T1 | 4 | 论文→答辩/组会中文 PPTX（ARS 无对应） |
| [skills/nature-figure/README.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-figure/README.md) | T1 | 4 | 投稿级科研图（Python/R、SVG/PDF/TIFF）（ARS 无对应） |
| [skills/nature-academic-search/README.md](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-academic-search/README.md) | T1 | 4 | 可选 MCP 文献检索 + 依赖（引文格式无 GB/T 7714） |
| [Awesome Skills 收录页](https://www.awesomeskills.dev/zh-CN/skill/yuan1z0825-nature-skills) | T2 | 3 | 生态收录佐证 |
| [cnblogs nature-skills 解读（zhang-yd, 2026-08-02）](https://www.cnblogs.com/zhang-yd/p/22151100) | T2 | 3 | 中文二手解读 |
| [今日头条「ARS 管流程 + nature-skills 管图表」](https://m.toutiao.com/article/7652706441303802378/) | T3 | 3 | 中文社区组合用法实操体验 |
| [CSDN Codex 装 nature-skills Windows 排错](https://qtchen.blog.csdn.net/article/details/162627479) | T3 | 3 | Windows 整目录复制/断网/触发词 500 经验 |

> P2 需按技能索引表补读：nature-literature-pipeline、nature-reader、nature-citation、nature-ref-verifier、nature-reviewer、nature-polishing 的 SKILL.md/README.md。

## 关键探测结论（P2 重点验证）

1. **ARS**：human-in-the-loop、2.5/4.5 integrity gates、citation trust-chain / L3 claim audit、中文引文为**台湾惯例 APA 7.0**；`citation_format_switcher` 覆盖 APA/Chicago/MLA/IEEE/Vancouver，**不含 GB/T 7714**。
2. **nature-skills**：Apache-2.0、19 技能分 Draft/Beta/Stable；router 式 SKILL.md；安装需**保留完整技能目录（references/、static/、manifest.yaml、nature-shared）**，不能只拷 SKILL.md；官方 runtime：Codex/Claude Code/OpenClaw/OpenCode/Hermes（**未见 Cursor 官方支持**）；`nature-academic-search` 引文格式同样无 GB/T 7714。
3. **重叠区**（写作/润色/综述/审稿/引用）：双库功能重叠，P3/P4 需给出**分工建议**避免选择困难。
4. **互补区**：ARS = 完整学术 pipeline + 诚信把关；nature-skills = 科研绘图（figure）、答辩/组会 PPT（paper2ppt）、开题状态机（proposal-writer）、中文文献推送。
5. **边界**：两库均**不覆盖系统开发**与查重。

## 覆盖缺口

- 官方与二手均**无**"两库按中文毕设/学位论文阶段组合编排"的现成指南 → 需自行推导（本项目价值所在）。
- 大陆学位论文 GB/T 7714 / 学校 LaTeX 模板：ARS Issue #425 证明属已知需求；两库引用体系默认均不含 GB/T 7714 → 指南须给"外挂模板/人工校正"方案。
- nature-skills 无官方 Windows/WSL 文档；ARS 有 Git Bash/python3 坑但 nature 侧仅社区（T3）经验。
- ARS 引用的繁体中文 Substack 使用指南不可达（HTTP 000），不入 P2 核心。

## 方向菜单（请选择 P2 侧重点）

- **A. 按毕设阶段混排双库（推荐）**：P2 直接以"选题→文献→大纲→写作→图表→引用→自查→答辩"为主轴，每阶段取双库对应技能深读；产出端到端路线图 + 分工建议。
- **B. 双库分深读后合并**：先各自完整深读（ARS 全 pipeline、nature-skills 全 19 技能），P3 大纲时再做阶段合并映射；覆盖最深但 token 消耗与时间最大。
- **C. 中文毕设最小可用集**：P2 只深读"文献综述→写作→图表→答辩"最少技能组合（ARS lit-review/full/reviewer/citation-check + nature literature-pipeline/figure/paper2ppt/ref-verifier），快速产出可直接照做的精简指南。

## P2 范围预估

- 核心深读约 10–12 个 T1 源（ARS ~6 + nature-skills ~6）+ 按所选方向补充（A/C 聚焦，B 全量）。
- 抓取走 research-collector 的 crawl4ai 环境（首次需 `scripts/crawl.sh --help` 探测，必要时 `scripts/setup.sh`）。
- 产出 `02_deep_research.md`：范围 / 源表 / claim-源映射 / 矛盾点 / 实操指导 / 开放问题 / 下游交接。
