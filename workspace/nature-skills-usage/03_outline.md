## 学习笔记大纲：《如何用好 nature-skills（Codex 上手实战指南）》

> 笔记类型：实战笔记（上手实战指南）
> 预计总篇幅：约 20–28 页
> 章节数：6 章
> 主用环境：Codex（Claude Code 仅作对照，不展开两套安装说明）
> 目标读者：已熟悉 agent skill 机制（SKILL.md / 技能包 / npx skills 概念）

---

### 第一章：项目定位与设计哲学

- **篇幅**：短（约 1–2 页）
- **覆盖要点**：是什么、为什么值得用、Router-style 架构心智、成熟度标签
- **素材来源**：02_deep_research.md §3.1 / §3.2（S1 §1/§3.1/§7.1/§7.3；S5 §3.1/§3.2；S6）
- **代码示例**：无

**子节结构**：
1. nature-skills 是什么：面向全球 AI 学者的可复用科研技能库，按 `SKILL.md` 组织，`skills/` 下每个顶层目录是一个可安装单元
2. 设计目标与 5 条共享原则：真实问题解决 / 可验证工作流 / 可直接使用产物；一手来源优先、显式胜过隐式、感知上下文、输出优先、可扩展
3. Router-style 架构（核心设计洞察）：static/dynamic 分层、`SKILL.md` 只做路由、`manifest.yaml` 声明「轴→文件」映射、一次调用流程
4. 状态标签与项目边界：Draft / Beta / Stable 含义、Apache-2.0、约 19 个可触发技能 + `nature-shared`
5. 一句定位收束 + 引用纪律：作者自述「被 DeepMind 借鉴」仅作转述，不作为外部实证

---

### 第二章：技能全景速查（19 个可触发技能）

- **篇幅**：长（约 5–6 页）
- **覆盖要点**：技能清单读法、六大分组速查表、nature-shared 共享包、实时口径
- **素材来源**：02_deep_research.md §3.4（S1 §6 技能索引；S5 §4.6；S6；S9 仅作 nature-shared 旁证）
- **代码示例**：无（纯速查表 + 少量名词解释）

**子节结构**：
1. 速查表读法：目录名（安装单元）≠ frontmatter name（触发名）；状态标签；「以 `npx skills --list` 实时为准」的口径说明（引用 02 分歧记录 §4）
2. 分组速查 A｜读论文与文献管理：`nature-reader`、`nature-paper-card`、`nature-downloader`、`nature-literature-pipeline`
3. 分组速查 B｜写作与润色：`nature-polishing`、`nature-writing`、`nature-statistics`、`nature-data`、`nature-proposal-writer`（触发名 `researchwrite`）
4. 分组速查 C｜投稿与返修：`nature-reviewer`、`nature-response`
5. 分组速查 D｜检索与引用核验：`nature-citation`、`nature-academic-search`、`nature-ref-verifier`
6. 分组速查 E｜演示与科研绘图：`nature-paper2ppt`、`nature-image2ppt`、`nature-figure`
7. 分组速查 F｜扩展与记录：`nature-paper-to-patent`、`nature-experiment-log`
8. 依赖共享包 `nature-shared`：哪些技能依赖它、为什么单独装容易漏

---

### 第三章：Codex 安装与日常维护

- **篇幅**：中（约 4–5 页）
- **覆盖要点**：两条官方路线、`npx skills` 命令矩阵、整库同步脚本、依赖与合规安装、安装后验证
- **素材来源**：02_deep_research.md §3.3（S1 §5.1/§5.3；S2；S5 §4.2；S6）
- **代码示例**：有（命令矩阵为主）

**子节结构**：
1. 前置准备与「安装路线决策树」：Node.js ≥18；只想要 1–3 个技能 → `npx skills` 按需装；想整库跟上游 → clone + `update-codex-skills.sh`；想长期自动更新 → SessionStart hook
2. 路线 1｜`npx skills add/list/update/remove`：`--global` / `--agent codex` / `--skill` / `--yes --copy` / `--list` / `--all` 语义；frontmatter 名映射；组合装 `nature-reader` + `nature-shared` 的写法
3. 路线 2｜仓库脚本整库同步：`update-codex-skills.sh --pull / --check / --prune`；`rsync` 依赖与 Windows Git Bash 注意点
4. 自动更新：`autoupdate-skills.sh` 6 小时节流 + `hooks.json` 的 `SessionStart` 合并
5. 运行时依赖与合规安装：Python / R / Playwright / MCP server 按各技能 README 单独装；`PUBMED_EMAIL`、OpenRouter key、Scopus 凭据处理
6. 安装验证与「开新会话」规则：最小验证命令与产物形态确认

---

### 第四章：典型科研场景实操：提示词与流程

- **篇幅**：长（约 5–7 页）
- **覆盖要点**：用法心法、官方 8 类场景提示词、端到端工作流解剖、技能→场景映射
- **素材来源**：02_deep_research.md §3.5（S1 §4；S5 §3.2/§3.3；S6；技能映射为 inference，需标注）
- **代码示例**：有（以可复制提示词为主，附少量产物文件形态说明）

**子节结构**：
1. 用法心法：不确定选哪个 → 自然描述任务；已确定 → 提示词显式「使用 `nature-xxx`」；gate 只问一个问题并记忆偏好
2. 场景实操 1–4：读论文中英对照（`nature-reader`）；组会汇报 PPT（`nature-paper2ppt`）；润色/翻译为 Nature 风格（`nature-polishing`）；摘要/引言起草（`nature-writing`）
3. 场景实操 5–8：预投稿互盲审稿（`nature-reviewer`）；返修逐点回复 + cover letter + 标红（`nature-response`）；引用数/他引/引用者画像（`nature-academic-search`）；投稿级科研图/示意图（`nature-figure`）
4. 端到端可验证工作流解剖：以 `nature-citation` 为例（文本/DOI → 分段 → Crossref 检索 → 期刊族 `in_scope()` 过滤 → 去重 → 导出 ENW/RIS/Zotero RDF → artifacts）
5. 交付物形态与来源标注意识：`.md / .pptx / .svg / .enw` 等产物、图文对应、逐条引用锚点

---

### 第五章：避坑与最佳实践

- **篇幅**：中（约 3–5 页）
- **覆盖要点**：官方明示的坑、第三方批评、质量与合规边界、最佳实践清单
- **素材来源**：02_deep_research.md §3.6 / §3.7（S1 §5.2/§5.3/§5.4；S5 §2.1/§5.2/§5.3；S6；S7/S8 为社区二传、须弱化标注）
- **代码示例**：无（少量命令引用第 3 章，不复述）

**子节结构**：
1. 必踩的坑（官方高可信）：只复制 `SKILL.md` 会坏；运行时依赖不自动安装；目录名 ≠ frontmatter 技能名（`researchwrite`）；单独装依赖技能漏 `nature-shared`；装完不新开会话；Claude Code 不可跑 `update-codex-skills.sh`
2. 质量与成熟度管理：仅 4 个 Stable、多数 Beta/Draft；LLM 编造风险与官方缓解手段；写作/审稿交付物一律当「草稿 + 核验清单」
3. 合规与账号边界：`nature-downloader` 的「合法获取」、CARSI/图书馆权限、付费 API 与账号风险由使用者承担
4. 第三方批评与社区反馈：S5/S6 批评点 + S7/S8「AI 味 / 绘图分化」观点，按可信度分级呈现
5. 最佳实践清单：最小验证、按需 vs 整库取舍、Windows `--copy`、引用类产物人工多源核对、与 Obsidian 工作流结合

---

### 第六章：上手行动清单与生态进阶

- **篇幅**：中（约 3–4 页）
- **覆盖要点**：30 分钟上手清单、生态位置与对照、待实测开放问题、进阶路线
- **素材来源**：02_deep_research.md §3.7 / §5 / §6（S1 §3.2；S5 §5.1/§6；S6；S7/S8 弱化）
- **代码示例**：无

**子节结构**：
1. 30 分钟上手行动清单：装 → 最小验证 → 跑通一个真实科研场景 → 遇到问题按第 5 章排错
2. 生态位置：skills 生态解决「懂行」；Agent Skills 规范下垂直技能库可多平台零适配；与通用 skills 库的差异在「研究垂直深度」
3. 与 Claude Code 的取舍对照：官方主推 Codex 路线 vs 本地 clone + wrapper；何时值得用 Claude Code
4. 待实测开放问题（来自 02 记录 §6）：router 触发稳定性、Windows symlink/copy 表现、MCP server 检索质量
5. 进阶路线：从「用技能」到「为实验室定制技能」；`nature-reader` / `nature-experiment-log` 产物直通 Obsidian vault

---

## 学习路径说明

### 前置要求
- 理解 `SKILL.md` / 技能包 / `npx skills` 的基本概念（用户已具备，本章节不重讲基础）
- 本机可运行 Codex，Node.js ≥ 18
- 无需精通 Python/R；但需知道部分技能（nature-figure / nature-downloader / MCP 相关）要求额外运行时，会按提示安装

### 学完能做什么
- 能独立完成 nature-skills 在 Codex 上的安装、更新、卸载与自动维护
- 能读懂 19 个技能的用途与触发词，任务一来就选对技能（或用自然语言触发路由）
- 能跑通「读论文中英对照 → 组会 PPT → 润色 → 摘要/引言 → 预投稿评审 → 返修回复」等典型科研流水线
- 能避开已知坑位，对写作/审稿/引用类交付物建立「草稿 + 核验」意识，守住合规边界

### 建议学习顺序
- 先读第 1 章建立心智模型（约 15 分钟）
- 对照第 3 章完成安装后，用第 2 章速查表挑选 1–2 个最贴近自己工作的技能
- 按第 4 章用官方模板做最小验证，跑通一个真实小任务
- 遇到问题再回查第 5 章；把第 6 章行动清单当作收尾自检
- 若后续要用 Claude Code 或写自有技能，再进入第 6 章生态部分深读

---

> ⏳ 本大纲等待用户确认后再进入逐章写作（P4 阶段）。
