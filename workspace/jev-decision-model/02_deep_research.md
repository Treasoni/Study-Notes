# 02 深度素材 — Jev 决策模型

## 一、Scope

- **运行**: jev-decision-model · **阶段**: P2 深度收集 · **完成日期**: 2026-09-20
- **深读来源**: 9 个（核心 5 + 为裁决冲突补抓 4）
- **claim 记录**: 100 条（g1 官方线 40 · g2 用法线 24 · g3 验证线 36），全部带锚点与逐字引文
- **覆盖方向**: A 概念定位 · B 使用方式 · C 实战集成（部分）· D 开源复现（未在本轮）· E 局限实测
- **原始抓取产物**: `workspace/jev-decision-model/raw/`（144 KB）
- **本轮未抓取**: `S02` 创始人演讲 · `S03` TechCrunch · `S04` Vercel 概念页 · `S05` 中文质疑稿 · `S09` judge 样板 · `S10` 压缩插件 · `S14` APUS 复现 · `S15` open-jev（均在 P1 列表，P2 核心集外）

> [!warning] 引文性质与禁止事项（下游必读）
> - 本文件所有 `Verbatim` 均为**回源逐字复制**，可直接引用；`Gist` 是概述，**不得当作原文引用**。
> - 标 `vendor-spec` / `official-claim` 的数字全部是**厂商自报**，不得写成独立结论。
> - `S07` 与 `G1a` 的**代码块在抓取时结构损坏**（丢括号、丢比较运算符）。字段名可用，**代码不可原样照抄**。
> - 官方 `/primitives` 页（原语 schema 的权威定义页）**不在本轮来源内**，因此**目前没有任何来源给出原语的规范性 schema**，只有请求/响应示例。

## 二、来源表

| ID | 来源 | 层级 | 日期 | 抓取状态 | 本地原文 |
|---|---|---|---|---|---|
| S01 | TypeSafe 官方博客 | official-doc | 2026-09-15 | 正文完整；FAQ 仅剩标题、答案未取 | `raw/g1/S01/01_typesafe_ai.md` |
| S07 | TypeSafe 官方 Quick start | official-doc | — | 正文完整；**所有代码块结构损坏** | `raw/g1/S07/01_docs_typesafe_ai.md` |
| G1a | TypeSafe 官方 Confidence | official-doc | — | 完整 | `raw/g1/G1a/01_docs_typesafe_ai.md` |
| G1b | TypeSafe 官方 Patterns | official-doc | — | 完整（短索引页） | `raw/g1/G1b/01_docs_typesafe_ai.md` |
| S06 | Vercel AI SDK 指南 | implementation-report | 2026-09-19 | 完整；TS 代码被重排、**比较运算符丢失** | `raw/01_vercel_com.md` |
| S08 | AI/ML API 网关文档 | implementation-report | — | 正文完整；JSON 代码块被截断 | `raw/01_docs_aimlapi_com.md` |
| S11 | 品玩 PingWest 实测 | news-media | 2026-09-20 | 正文完整；`<title>` 元数据乱码（正文引文正常） | `raw/01_www_pingwest_com.md` |
| S12 | Wunderlandmedia 复测 | community | 2026-09-19 | 完整，含两张数据表 | `raw/01_wunderlandmedia_com.md` |
| S13 | jev-decision-bench | community | 运行日 2026-09-18 | README 完整；**仓库文件列表未渲染** | `raw/01_github_com.md` |

**层级分布**：official-doc 4 · implementation-report 2 · news-media 1 · community 2。

## 三、Claim ↔ Source 映射

### A. 概念与定位

| CID | 来源 | 锚点 | 要点 |
|---|---|---|---|
| g1-1 | S01 | 开篇 | 厂商自定义类别：`releasing our first **System One Model**: a new class of frontier models built to make fast, structured decisions that software can use directly.` |
| g1-2 | S01 | 定义段 | 输入输出形态：`Think of Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out.` |
| g1-4 | S01 | 放弃字符串段 | 与文本模型的差别：`While Jev gives up string generation, it's optimized for structured outputs and _can't_ hallucinate.` |
| g1-5 | S01 | Frontiers 表·Outputs 行 | `Possible outputs and structure are defined in advance. The model never makes type errors. All answers are accompanied with calibrated probabilities and confidence scores.` ⚠ 与 G1a 冲突，见 C7 |
| g1-6 | S01 | Frontiers 表·Sampling 行 | `**Parallel.** Generates all outputs in a single query. Incredibly efficient and hardware-aware.` |
| g1-11 | S01 | Evidence·No type errors | `This would be an easy thing to falsify with just a single counter-example, but it is mathematically impossible.` |
| g1-12 | S01 | Hallucination and Type-safety | `Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots.` ⚠ 厂商自认图中 0% 非实测 |
| g1-9 | S01 | Frontiers 表·Confidence 行 | `Always communicates confidence and uncertainty with every output. Calibrated: higher confidence means higher accuracy. More consistent: returns similar answers for similar inputs.` ⚠ 注意用词是 "similar" |
| g1-10 | S01 | Frontiers 表·LLM 列 | `Even if prompted for a confidence estimate, models tend to be overconfident and inconsistent.`（author-opinion，support: low，未给测量来源） |
| g1-35 | G1b | 首段 | 定位：`TypeSafe is designed to sit within a larger system, powering decisions with AI.` |
| g1-36 | G1b | 首段 | 使用范式：`Learning to think in terms of discrete, atomic decisions that compose into complex system behavior is a key skill` |
| g1-37 | G1b | 首段 | 官方把 `primitives` 与 `confidence` 列为两个独立前置文档页 —— **`/primitives` 本轮未抓** |

**命名澄清（原 P2 待定项，已解决）**：官方定名为 **Noul / Choice / Score** —— `g1-14`（S07）：`Mix Noul, Choice, and Score in one call and see all results at once.` 故 P1 中出现的 `boolean`（`S06`，Vercel 平台侧叫法）与 `noul`（`S08`）不是矛盾，**官方名为 Noul**。

### B. 性能与定价（全部厂商自报）

| CID | 来源 | 要点 | 来源自带限定 |
|---|---|---|---|
| g1-3 | S01 | 智能水平与现有 LLM 相近，快两个数量级 | 同页承认评测存在自选偏差 |
| g1-7 | S01 | `End-to-end response time is 70ms-500ms`；`40x-200x faster` | 同页注明评测多在西海岸笔记本上跑；同表 LLM 侧为 3–329 秒 |
| g1-8 | S01 | `Input tokens: $0.042 / MTok ... Output tokens: FREE (too cheap to meter).` | 同页承认无法证明定价未被补贴 |

> [!warning] 这三条**没有任何中立第三方规模化复测**。第三方实测的绝对数字见 F 节，量级不同（S11 测到每题约 0.73–0.75 秒）。

### C. 原语与 Schema

| CID | 来源 | 锚点 | 要点 |
|---|---|---|---|
| g1-15 | S07 | Call it: the API | 官方端点：`POST https://api.typesafe.ai/v1/systemone` |
| g1-16 | S07 | Request body·Noul | `"type": "noul",` — Noul 问题带 instructions，**无 criteria 字段** |
| g1-17 | S07 | Request body·Choice | `"criteria": {` — Choice 的 criteria 是**字典**（选项名→说明） |
| g1-18 | S07 | Request body·Score | `"criteria": [` — Score 的 criteria 是**列表**（有序等级） |
| g1-22 | S07 | Response body | 响应回传具体版本 `"model": "jev-1.13.0"`；请求侧默认传 `"jev-latest"` |
| g1-23 | S07 | Response body | `"input_tokens": 392,` — 响应带 usage 统计 |
| g1-24 | S07 | Python SDK | `Install the SDK (requires Python >= 3.10).` |
| g1-25 | S07 | Python SDK·step 2 | `The client reads TYPESAFE_API_KEY from the environment and calls jev-latest by default.` |
| g2-1 | S06 | Ask one boolean question | `The state is whatever you want the model to look at, and each key in questions becomes a key in answers.` |
| g2-2 | S06 | Three question types 表 | choice 答案为 `choice` + `probabilities`；**选项上限 255** |
| g2-5 | S06 | 多问题段 | state 接受 JSON 对象或数组，`you can pass a record or a message history without serializing it yourself` |
| g2-6 | S06 | 响应示例 | choice 的 `probabilities` 是按选项键展开的完整分布，选中项最高 |
| g2-7 | S06 | 响应示例 | score 答案为 `score` + `probabilities`，分布以**字符串形式的等级下标**为键 |
| g2-12 | S06 | Best practices·Keep state focused | `Input tokens are the only thing you pay for, so pass the fields the decision depends on rather than an entire record.` —— 上下文 **64,000 token/请求**，其中 `state` **32,000** |

> [!warning] **无规范性 schema 来源**。上表字段名取自请求/响应示例，不是 spec 页。`S07` 代码块丢括号，`S08` JSON 被截断，故**嵌套结构与必填/可选状态无法确认**。

### D. confidence 与 probability 语义（本轮最关键的一节）

| CID | 来源 | 要点（逐字） |
|---|---|---|
| g1-26 | G1a | `All Score and Choice answers from TypeSafe include a probabilities property representing the probability distribution across the options (for Choice) or levels (for Score).` |
| g1-27 | G1a | `The answer's confidence property collapses that shape into a single number from 0 to 1, so you can threshold on it without doing the math yourself. (Noul answers don't carry one.)` |
| g1-28 | G1a | `confidence is a statistic computed from the probability distribution the answer already gives you. TypeSafe computes it for you and returns it on every Choice and Score answer` |
| g1-29 | G1a | `We provide confidence as a convenient measure that fits most use-cases, but you are never locked into our definition.` |
| g1-30 | G1a | `In both cases a flatter distribution means lower confidence: low confidence on a Choice often means none of the options are a clear winner over the others` |
| g2-8 | S06 | `requestsRefund.probability is the estimated probability that the customer wants money back, not a confidence in the answer.` |
| g2-9 | S06 | `TypeSafe AI also returns a separate confidence statistic for choice and score answers in result.providerMetadata.typesafe.confidence, keyed by question ID.` |
| g1-19 | S07 | 官方响应示例：choice 答案内 `"confidence": 0.78,` 与 `"probabilities": { "technical": 0.85,` —— **注意二者不相等** |
| g2-20 | S08 | 网关响应示例把 `"confidence": 0.97,` 直接放在 choice 答案对象内，与 `choice`、`probabilities` 平级 |
| g2-21 | S08 | score 答案含 `score`、`confidence`，另有 `legend` 把等级下标映射回评分文字 |

**三条硬结论**（均可直接支撑正文）：
1. **probability ≠ confidence**：前者是「陈述为真/事件发生的概率」，后者是把分布形状压成 0–1 的可阈值化统计量（`g2-8` + `g1-27` + `g1-28`）。
2. **confidence 只出现在 Choice 与 Score 上，Noul 没有**（`g1-27` 官方括号原话 + `g2-9` 的 "boolean 不返回" 独立印证）。
3. **`confidence` 是答案对象自己的属性**（`g1-27` 措辞 "The answer's `confidence` property"；`g1-19`、`g2-20`、`g2-21` 三个响应示例都在答案对象内）；AI SDK 走 `providerMetadata` 是**平台层重新暴露**，不是另一套语义。

### E. 阈值与实践模式（官方）

| CID | 来源 | 要点 |
|---|---|---|
| g1-32 | G1a | `**Low confidence:** Do not act. Route to a human, request clarification, or fall back to a different system.` |
| g1-33 | G1a | `The correct threshold values depend on your domain and the performance of the model for your use case. Start with conservative thresholds, test with your own data, and adjust` |
| g1-34 | G1a | `The 0.5 confidence floor catches anything the model reports as genuinely uncertain.`（示例取值） |
| g2-10 | S06 | 路由表示例：置信度 ≥0.6 **且** 选中项概率 ≥0.7 才自动分派 |
| g2-11 | S06 | `Read-only actions like showing a screen can tolerate a wrong guess, so a probability of 0.7 might be enough. Destructive actions need a higher bar, closer to 0.9 or above` |
| g1-38 | G1b | 模式一 Speculative Fan-Out：一次调用发多个问题（含投机性问题），由调用方代码筛相关性 |
| g1-39 | G1b | 模式二 Confidence-Gated Routing：把置信度当第二条决策轴 |
| g1-40 | G1b | 模式三 Composite Scoring：多维度合成单一得分 |

> `G1a` 页里有 0.5 / 0.9 两档示例阈值，但**抓取时比较运算符丢失**（页面上只剩 `if confidence  0.5:`），故只引用了散文句，未引用代码。

### F. 独立验证与已知局限（第三方）

**S11 品玩实测**（中文电商客服场景）

- `g3-1` 测试集：50 条中文客服问题，每题四项判断（紧急度/售前概率/类别/严重度），**四项全对才算正确**
- `g3-2` 对比 12 个模型，Jev 与「便宜小模型组」（DeepSeek V4 Flash、GPT-5 nano、Gemini 2.5 Flash Lite）同组
- `g3-3` `Jev 的平均得分大约在 32～32.6 分之间，50 道题的完整准确率约为 64%～65.2%。它排在便宜小模型组第二，只比 DeepSeek V4 Flash 少 1.2 分。`
- `g3-4` `Jev 平均每道题的完整响应时间约 0.73～0.75 秒，50 道题总成本约 0.002 美元，两项都是我们测试中的最低值。DeepSeek V4 Flash 虽然多拿了一点分，但平均每题需要 5.58 秒，成本约为 Jev 的 2.5 倍。`
- `g3-5` 跨组参照：MiniMax M3 约 38 分，`完整准确率高出约 10.8 个百分点`
- `g3-6` `50 道题，MiniMax M3 只多花了大约 0.0035 美元，平均每题响应时间约 1.80 秒。`
- `g3-7` 失分集中在阈值附近：`人工标注认为某条客服消息的严重度下限应该是 2.00，Jev 给出了 1.99；某条临期食品问题的人工紧急度是 0.75，Jev 的结果在 0.71～0.72 左右。`
- `g3-8` `我们重复测试了 15 次，还有 3 道题出现过通过和失分交替的情况。`
- `g3-9` 自述局限：`这 50 条中文客服样本，也不足以代表它在所有任务上的表现。`
- `g3-11` 自述局限：`我们这组按题目判分的测试，也不能验证概率校准做得有多好。`
- `g3-12` 结论：`因此，这组测试很难支持"Jev 是更聪明的模型"这个结论。它展示的是一组具体取舍：少等一会儿，少花一点钱，同时接受一定的准确率差距。`

**S12 非确定性复测**（作者自有 183 篇文章 × 4 问题 = 732 判断）

- `g3-14` `That is 732 separate judgements. One run took **20.1 seconds** at eight parallel requests, burned 445,794 input tokens, and cost **$0.0187**.`
- `g3-16` `I ran the same 732 decisions three times and diffed them. 177 answers were bit-identical across all three runs. That is 24 percent. The other 555 moved.`
- `g3-17` 漂移分布：中位 `0.010` / p90 `0.030` / p99 `0.050` / 最差 `0.070`
- `g3-18` `Seven hundredths, across 732 decisions, as the single worst thing that happened. The flagged-post count came out 56, 56, and 57.`
- `g3-19` 作者的修正：`So Jev is not deterministic in the sense I had claimed, and "the same input gives the same answer" is wrong. "The same input gives an answer within about a tenth" is right` ⚠ 针对**打分型**输出，未涵盖分类型输出
- `g3-20` 漂移按区间分布：两端最小（<0.15 → 0.004；>0.85 → 0.007），中段最大（0.40–0.70 → 0.020）
- `g3-21` `Of 732 decisions, **12 crossed a threshold and changed the verdict** between runs.`
- `g3-22` 归因：`The slop_shapes scores across my archive run from 0.36 to 0.85 with a median of 0.55, so the distribution is one compressed lump and 0.70 lands inside the thick part of it.`（作者自述 12 次翻转中 10 次是自身阈值设计问题）
- `g3-23` 明确弱点：`It does not do arithmetic. It does not compare dates, because it reads them as text rather than as ordered quantities. Extraction of the pieces with it, then do the comparison in code.`
- `g3-24` 自述未验证：`The gate in front of a live production LLM I have not built or measured yet, so the cost saving I described is reasoning, not a result.`

**S13 jev-decision-bench**（49 项任务 / 8,225 条样本）

- `g3-26` 独立性声明：`I have no affiliation with TypeSafe. Run date: 18 September 2026, model jev-1.13.0.`
- `g3-25` `**Jev matched or beat the LLM baseline on 42 of 49 tasks, at about a seventh of the latency and a quarter of the cost.**`
- `g3-27` `Tasks where Jev led / tied / trailed the better baseline | **29 / 13 / 7**`（分差 <0.005 记持平）
- `g3-28` 中位服务端耗时 `105 ms` vs `710 / 808 ms`；每千条成本 `$0.04` vs `$0.16 / $0.19`；ECE `0.07` vs `0.18 / 0.14`
- `g3-30` `**clear** means the 95% bootstrap intervals do not overlap. Only seven leads are clear: six for Jev, one for the baseline.` ⚠ 其余「领先」落在误差范围内
- `g3-31` 强项：LogiQA 0.77 vs 0.59、WinoGrande 0.89 vs 0.66、ARC-Challenge 0.97 vs 0.87、MMLU 0.94 vs 0.87、NFCorpus reranking 0.73 vs 0.63
- `g3-32` 抗污染证据：代码生成的 120 道新数学题得 `0.75`，与 GSM8K 的 `0.72` 相当
- `g3-33` 校准可用性：`calibration error is about half the baseline's, and keeping only its most confident half of answers raised accuracy by 7.6 points on average.`
- `g3-34` 弱项：`counting (0.87 vs 0.99), very large option sets (Banking77 0.81 vs 0.87), and a question plus its negation did not get consistent probabilities (off by 0.32 on average).`
- `g3-35` 自述局限：`**Public benchmarks.** Most tasks are well known, and any model may have seen them in training. The only contamination control here is the fresh math task.`
- `g3-36` 自述无法复现的私有观察：`In a separate private test with around 100 long documents per request, Jev gave high relevance scores to a handful of plainly unrelated documents. Nothing in this repo reproduces that.`（support: low）

> [!warning] **`S13` 的基线不可当作满血模型**：基线是 `gpt-5.6-luna` 的**无 / 低推理强度**设置。「42/49 追平或领先」「快约 1/7、便宜约 1/4」都建立在**刻意限制对手**之上，不得直接对外引用为「Jev 打得过前沿模型」。

## 四、冲突与口径澄清（相对 P1 的更新）

| # | P1 记录 | P2 裁决 | 依据 |
|---|---|---|---|
| **C7（新增）** | — | 🔴 **未解的第一方矛盾** | `S01`：`All answers are accompanied with calibrated probabilities and confidence scores` + `Always communicates confidence and uncertainty with every output`；`G1a`：`(Noul answers don't carry one.)`。**同一厂商两页互相矛盾**，本轮无第三份官方材料可裁决 |
| C4 | 官方文档 ↔ 网关，confidence 位置 | ✅ **澄清为调用面差异，非矛盾** | 原生语义为**答案对象的属性**（`g1-27` 措辞 + `g1-19`/`g2-20`/`g2-21` 三个示例）；AI SDK 在 `providerMetadata.typesafe.confidence` 重新暴露（`g2-9`）。两处并存，不是二选一 |
| C5 | S13 ↔ S15 准确率口径 | ✅ **澄清为不可比** | `S13` 基线为刻意限制推理强度的 `luna`；`S11` 是 50 条中文客服题集。任务集、对手设置均不同，**不得相加或并列比较** |
| C6 | S12 ↔ S13 复现性 | ✅ **澄清为不同指标，且第一方从未承诺确定性** | `S11` 报「15 次重复中 3 题通过与失分交替」（条目级翻转率）；`S12` 报「3 次运行 177/732 逐位相同」（逐位一致率）。官方最强表述仅 `returns similar answers for similar inputs`（`g1-9`）。**三方一致：无确定性承诺** |
| C1 | 官方博客 ↔ 中文质疑稿 | ⏸ 未回源 | `S05` 不在 P2 核心集，保持 P1 记录 |
| C2 | TechCrunch ↔ 中文质疑稿 | ⏸ 未回源；且双方均为**观点**分歧 | `S03`/`S05` 均未抓取 |
| C3 | Vercel 指南 ↔ 压缩插件，state 压多少 | ⏸ 部分 | 官方一侧已取到明确主张（`g2-12`：只传决策所依赖字段；输入 token 是唯一付费项）；`S10` 未回源，故未做裁决 |

## 五、实践指引（可直接写进笔记的部分）

1. **调用形状**：`POST https://api.typesafe.ai/v1/systemone`，body 为 `state`（待评估内容）+ `questions`（问题键 → 带类型问题）；`answers` 的键与 `questions` 一一对应（`g1-15`、`g2-1`、`g2-16`）。
2. **原语三种**：`noul`（是否 + 概率，无 criteria）、`choice`（criteria 为字典，≤255 选项）、`score`（criteria 为列表，有序等级）—— `g1-16`/`g1-17`/`g1-18`/`g2-2`。
3. **读结果**：先看 `probability`（事件概率，**不是**答案置信度），再用 `confidence`（0–1，服务端由分布算出）做阈值；`confidence` 只在 Choice/Score 上（`g2-8`、`g1-27`、`g1-28`）。注意 `confidence` ≠ 最高选项概率（`g1-19` 中 0.78 vs 0.85）。
4. **阈值**：官方明确**没有普适阈值**，需按领域自测标定（`g1-33`）；示例起点为置信度 0.6 + 选中项概率 0.7（`g2-10`），并按动作风险上调——只读动作约 0.7，破坏性动作接近 0.9 以上（`g2-11`）；低置信时**不执行动作**，转人工或降级（`g1-32`）。
5. **控制成本**：输入 token 是唯一付费项，只传决策依赖的字段（`g2-12`）；上限 64,000 token/请求，其中 `state` 32,000（`g2-12`）。
6. **SDK**：Python SDK 需 ≥3.10，读 `TYPESAFE_API_KEY`，默认 `jev-latest`（`g1-24`、`g1-25`）。
7. **设计范式**：把问题拆成离散、原子化的决策（`g1-36`）；三个官方模式 —— 投机性一次多问、置信度门控路由、多维度合成分（`g1-38`/`g1-39`/`g1-40`）。
8. **不要在 Jev 里做的事**（第三方一致）：算术、日期比较（按文本读取，需在代码里比）；计数、超大选项集、否定式表述是已知弱项（`g3-23`、`g3-34`）。
9. **非确定性要显式处理**：同输入重复运行会出现小幅漂移（打分型输出中位 0.010、最差 0.070），**若阈值落在分数密集区，判定会翻转**（`g3-17`、`g3-21`、`g3-22`）。设计阈值时留出余量，或对临界结果二次确认。

## 六、开放问题（未解，不得在正文中想当然）

1. **第一方 Noul confidence 矛盾（C7）未解**。
2. **`/primitives` 页未抓** → 原语的规范性 schema（字段必填性、嵌套、取值范围）**至今无权威来源**，只有示例。
3. **`S07` 代码块结构损坏** → 无法确认字段嵌套与必选性。
4. **无独立校准曲线**：`S11` 自述不覆盖校准；`S13` 给出 ECE 0.07 但为自建口径，非第三方复测官方声称。
5. **官方性能/定价三项数字无中立规模化复测**。
6. **无生产环境具名客户或故障报告**；无对「零幻觉」的独立对抗性测试（提示注入/超长选项集/多语言）。
7. **Jev 官方 JS SDK 未找到**（只有 Python SDK 与 curl）。
8. **`S01` FAQ 答案未取**，含官方对「Is Jev just a smaller LLM?」的自答。
9. **C3（state 精简 vs 逐字保留）未回源裁决**，`S10` 不在核心集。

## 七、下游交接（给 outline-generator）

- **建议结构**（对齐用户诉求「概念 + 怎么用」）：
  - 概念章 ← 三·A + 三·B（厂商口径必须标注为自报）+ C7 矛盾如实写出
  - 用法章 ← 三·C + 三·D + 三·E + 五·1–7
  - 局限与边界章 ← 三·F + 四 + 五·8–9
- **可直接引用的原文**：本文件所有 `Verbatim` 字段（已回源逐字）。`Gist` 与本文其他概述**不得当引文用**。
- **必须标注来源性质的数字**：70–500ms、40–200x、$0.042/MTok、输出免费（全部厂商自报）；64%–65.2%、0.73–0.75 秒、$0.002/50 题（S11 独立实测，样本 50 条）；24% 逐位一致、中位漂移 0.010（S12 单站 3 次运行）；42/49、105ms、$0.04/千条、ECE 0.07（S13，基线为刻意限制推理强度的 luna）。
- **写作禁令**：① 不把 `S13` 的 42/49 与满血模型对比；② 不把 64% 写成官方口径；③ 不把「零幻觉」写成「判断不会错」；④ 不写「确定性」；⑤ 不原样照抄 `S07`/`G1a` 的代码块；⑥ 不把 `probability` 与 `confidence` 混用。

## 八、工具缺陷记录（本轮实测）

1. **抓取脚本按 host 命名输出文件 → 同域多页互相覆盖**。实测：`docs.typesafe.ai` 的 4 个 URL 写进同一目录后只剩最后一个（`Patterns`），已在 `raw/` 平铺目录留下 `01_docs_typesafe_ai.md`（实为 Patterns）。g1 代理改用每 URL 一个子目录（`raw/g1/{S01,S07,G1a,G1b}/`）规避，故 4 页原文均在。**这是继 `todo-state.sh` CRLF 敏感之后的第二个 Windows/本地化缺陷，建议一并纳入维护任务。**
2. **`S07`/`G1a` 代码块结构损坏**（丢括号、丢比较运算符）—— 影响官方文档的代码可用性，不阻塞收录，但阻塞「照抄代码」。
3. **`S11`（品玩）`<title>` 元数据乱码**，正文引文正常；疑为编码探测失败。
4. **`S13` 仓库文件列表未渲染**，`RESULTS.md`/`report.json`/`SPEC.md` 等文件的存在与内容未确认。
