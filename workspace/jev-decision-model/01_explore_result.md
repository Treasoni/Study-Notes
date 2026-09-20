# 01 探测结果 — Jev 决策模型

## 元信息

- **运行**: jev-decision-model
- **阶段**: P1 探测式收集
- **检索日期**: 2026-09-20
- **透镜数**: 3（官方与概念定位 / 生态集成与用法 / 独立验证与开源复现）
- **候选来源**: 15 条，按 canonical URL 去重后 15 条（无重复）
- **层级分布**: official-doc 5 · implementation-report 4 · news-media 3 · community 3

> [!warning] 记录性质（下游必读）
> 下表的「相关性」与「冲突」行，全部是探测代理的**摘要级**记录，**尚未回源核对**。
> 任何结论在进入 `02_deep_research.md` 之前必须先打开原页面验证。
> 不得把这些摘要当作原文引用，也不得把带来源 ID 的摘要直接交给写作代理。

## 来源表

| ID | 透镜 | 标题 | 发布方 | 层级 | 日期 | 分 |
|---|---|---|---|---|---|---|
| S01 | L1 | Introducing System One Models & Jev | TypeSafe AI | official-doc | 2026-09-15 | 5 |
| S02 | L1 | What's next after RLHF?（创始人演讲） | AI Engineer World's Fair / Diogo Almeida | official-doc | unknown | 5 |
| S03 | L1 | A new kind of AI model from a ChatGPT inventor is thrilling developers | TechCrunch | news-media | 2026-09-18 | 4 |
| S04 | L1 | What is Jev, TypeSafe AI's System One model? | Vercel | implementation-report | unknown | 4 |
| S05 | L1 | ChatGPT早期研究者做了一个"不会说话"的AI，Jev真是新范式吗？ | 腾讯新闻（转载） | news-media | 2026-09-18 | 3 |
| S06 | L2 | How to classify, route, and score with Jev and AI SDK | Vercel | official-doc | 2026-09-19 | 5 |
| S07 | L2 | Quick Start | TypeSafe AI | official-doc | unknown | 5 |
| S08 | L2 | Jev \| AI/ML API Documentation | AI/ML API | official-doc（第三方网关自有文档） | unknown | 4 |
| S09 | L2 | jev-as-a-judge | GitHub / Daniel Shea (LangChain) | implementation-report | 2026-09-20 | 4 |
| S10 | L2 | fast-jev-compaction | GitHub / tamaratran | implementation-report | unknown | 4 |
| S11 | L3 | 实测Jev：没那么强，但足够给有些乏味的AI圈带来新刺激 | 品玩 PingWest | news-media | 2026-09-20 | 5 |
| S12 | L3 | Jev Is Not Deterministic (I Measured It) | Wunderlandmedia / Kemal Esensoy | community | 2026-09-19 | 5 |
| S13 | L3 | jev-decision-bench | GitHub / OmarMujahid | community | unknown | 5 |
| S14 | L3 | fast-browser-use | GitHub / APUS-AI-Lab（麒麟合盛） | implementation-report | unknown | 4 |
| S15 | L3 | open-jev-typed-decision-engine | GitHub / intikhab49 | community | unknown | 4 |

### 来源 URL

| ID | URL |
|---|---|
| S01 | https://typesafe.ai/blog/introducing-system-one-models-and-jev |
| S02 | https://ai.engineer/talks/cJ0EOzey--o-whats-next-after-rlhf |
| S03 | https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/ |
| S04 | https://vercel.com/i/what-is-jev |
| S05 | https://news.qq.com/rain/a/20260918A058BW00 |
| S06 | https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk |
| S07 | https://docs.typesafe.ai/introduction/quickstart |
| S08 | https://docs.aimlapi.com/api-references/decision-models/typesafe/jev |
| S09 | https://github.com/danielgshea/jev-as-a-judge |
| S10 | https://github.com/tamaratran/fast-jev-compaction |
| S11 | https://www.pingwest.com/a/317597 |
| S12 | https://wunderlandmedia.com/jev-not-deterministic-732-decisions-three-runs |
| S13 | https://github.com/OmarMujahid/jev-decision-bench |
| S14 | https://github.com/APUS-AI-Lab/fast-browser-use |
| S15 | https://github.com/intikhab49/open-jev-typed-decision-engine |
| G1a | https://docs.typesafe.ai/confidence （P2 补抓，填缺口 1） |
| G1b | https://docs.typesafe.ai/patterns （P2 补抓，填缺口 1/4） |

### 各来源相关性（代理摘要，未核）

- **S01** — 官方自我定义「System One 模型」类别、与 LLM 的对照、口径边界、System One 与 Jevons 的命名出处。代理自述已实际抓取验证。
- **S02** — 创始人对「为什么要有决策模型」的第一方论述：RLHF 面向人类偏好、提出按「校准决策」重设优化目标。
- **S03** — 主流媒体对官方定位的转述与外部核验，含创始人访谈表述，可对照官方口径与第三方复述的差异。
- **S04** — 合作平台方对概念定位的解释，落到调用面（模型 ID、AI SDK evaluate API）。
- **S05** — 中文侧对「新范式」叙事的质疑性梳理，讨论「不能幻觉」口径的实际边界与命名是否站得住。
- **S06** — 可复制的 AI SDK 调用：装包、单布尔问题、多问题共享 state、按概率与 confidence 分支、不调模型也能测路由逻辑、阈值与防御式读分布的实践建议。
- **S07** — 原语规范入口：Noul / Choice / Score 三种问题的 schema、state 形式与 confidence 语义。同站还有 `/confidence` 与 `/patterns` 页。代理注明需 early access 才能实际调用。
- **S08** — 第三方网关 API reference：model/state/questions 请求体与 answers 响应体（含 probabilities、score、legend、usage）的字段级说明。
- **S09** — 把 Jev 当 agent 评估器的完整样板：对冻结的 agent 运行输出跑 quality 连续分与 does_pass 二值判断，并与 LLM judge 对比。代理注明样本仅 5 条、作者自述为早期小规模实验。
- **S10** — 上下文压缩的真实配置范例：用两个 noul 问题决定每个 tool call 保留/截断/删除，README 给出 keepThreshold、maxStateTokens、preserveRecentMessages 等默认值。依赖 2.1.274+ 的 function hooks 与 TYPESAFE_API_KEY。
- **S11** — 独立实测：50 条中文客服问题做四项判断，代理转述「完全正确率约 64%」，速度与成本最低；代理注明重复 15 次有 3 题结果漂移。
- **S12** — 独立复测：同一批 732 个判断跑三遍，代理转述「仅 24% 完全逐位一致」，漂移小但有个别判决越过阈值被翻转。
- **S13** — 第三方开源评测集，49 项任务 8225 条数据；代理转述 Jev 在 42/49 项持平或领先，并列出计数、超大选项集、否定式概率不一致等弱点；作者自陈样本小、基准公开。
- **S14** — APUS 开源（MIT）跨平台复现，本地 Qwen3.5-9B/35B-A3B 权重经单 token 反射直接决策，无云端调用。代理注明为企业方复现，非中立第三方。
- **S15** — 开源 150M 类型化决策引擎，自称与 Jev 对比的分数、校准与速度优势，可在免费 Colab T4 上短时训完。代理注明为作者自测、未第三方复核。

## 冲突记录（6 条，待 P2 回源裁决）

| # | 冲突方 | 分歧主题 |
|---|---|---|
| C1 | S01 官方博客 ↔ S05 中文质疑稿 | 「不幻觉」口径的成立范围 |
| C2 | S03 TechCrunch ↔ S05 中文质疑稿 | Jev 是否构成「新范式」 |
| C3 | S06 Vercel 指南 ↔ S10 fast-jev-compaction | 送给 Jev 的历史该压多少（精简 vs 逐字保留） |
| C4 | S07 官方文档 ↔ S08 AI/ML API 网关 | confidence 字段在 Noul 上是否可得 |
| C5 | S13 jev-decision-bench ↔ S15 open-jev | 准确率与校准水平的口径（任务集与对手设置不同） |
| C6 | S12 非确定性实测 ↔ S13 jev-decision-bench | 输出可复现性（阈值翻转 vs 视为平局） |

**不合并、不裁决**：以上冲突在 P2 中逐条回源，原始表述并列保留。

## 覆盖缺口（9 条）

1. **官方 `confidence` 与 `patterns` 子页正文未取**——「Noul 是否返回 confidence」仍无一手确认（对应 C4）。
2. **无第三方独立校准曲线**——「说 80% 时是否真 80% 正确」拿不到可靠性图，只有漂移与阈值翻转证据。
3. **官方性能与定价数字无中立第三方规模化复测**（快 40–200x / 便宜 444x / 延迟 70–500ms）。
4. **无任何复现触及真实权重或 RLCD 训练方法**——全部为行为级重实现，无法证实或证伪 RLCD 效果。
5. **无生产环境具名客户或故障报告**；无对「零幻觉」的独立对抗性测试（提示注入 / 超长选项集 / 多语言）。
6. **Jev 官方 JS SDK 文档与仓库未找到**（仅见 Python SDK 与 curl 端点描述）。
7. **LangChain 官方 provider 文档页未展开**（docs.langchain.com）。
8. **AI Gateway 之外的集成无官方声明**（Bedrock / Vertex 等）。
9. **中文来源多为转述**，无中文一手集成教程。

**口径修正**：官方文档域名是 `docs.typesafe.ai`，不是 `typesafe.ai/docs`（后者 404）。L1 因此一度判定「无官方文档」，该判定已被 L2 推翻。

## P2 规模估算

- **批次**：≤3 个代理，按「官方线 / 用法线 / 验证线」分组，不按来源逐个派发。
- **额外补抓**：`docs.typesafe.ai` 的 `/confidence` 与 `/patterns` 两页（填缺口 1、4）。
- **预计产出**：claim/source map 约 40–60 条，覆盖 A–E 五个已确认方向。
- **风险**：上线 5 天的主题，官方 material 总量有限；「如何使用」一半可以做到权威，「独立验证」一半必然偏薄——届时在 `02_deep_research.md` 的 open questions 中如实记录，不虚构。

## 方向菜单（阶段 2 待用户选择）

| 选项 | 核心源 | 覆盖方向 | 说明 |
|---|---|---|---|
| **1（推荐）核心 5 源** | S01 · S07 · S06 · S11 · S12 | A + B + E | 官方概念定义 + 官方 schema + 可跑代码 + 独立实测 + 非确定性实测，正好对应「概念 + 怎么用」 |
| 2 用法优先 | S07 · S06 · S08 · S09 · S10 | B + C | 偏工程落地：schema、SDK、网关字段、judge 样板、压缩插件 |
| 3 验证优先 | S11 · S12 · S13 · S14 · S15 | D + E | 偏局限与复现：实测、漂移、评测集、两个开源复现 |
| 4 全都要 | 全部 15 源 | A–E | 超出 P2「3–5 核心源」上限，需拆成两轮 P2 |
| 5 自定义 | 用户指定 | — | 直接给 ID 列表 |
