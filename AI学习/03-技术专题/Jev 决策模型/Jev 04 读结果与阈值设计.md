---
title: "第四章：读结果——probability、confidence 与阈值设计"
tags: [ai, jev, 决策模型, typesafe-ai]
created: 2026-09-20
updated: 2026-09-20
status: new
source_project: jev-decision-model
---

# 第四章：读结果——probability、confidence 与阈值设计

> [!info] 分册导航
> ← [[Jev 03 三原语与最小调用|第 3 章 · 三原语与最小调用]] · 🗂 [[Jev 决策模型 MOC|目录]] · [[Jev 05 接入与设计模式|第 5 章 · 接入与设计模式]] →

上一章你把调用的形状跑通了，也看到了答案里的数字。这一章回答三个问题：**这些数字分别是什么**、**哪一个是你真正能拿来卡阈值的**、以及**阈值该定多少、低于阈值时该做什么**。

这一章只差一个词，但这个词差得很关键：`probability` 和 `confidence` 在 Jev 里不是一回事。把它们当同义词用，会直接导致你的门控逻辑在错误的地方生效。

> [!warning] 本章引文范围
> 官方 Confidence 文档页（`G1a`）里的阈值**示例代码**在本轮抓取时**比较运算符丢失**（页面上只剩 `if confidence  0.5:` 这种残缺形态）。因此本章**只引用该页的散文句，不引用任何阈值代码**。若你需要可直接运行的阈值代码，请回官网原页获取。

## 4.1 一个答案里，有三种「看起来都像置信度」的数字

先把三种数字摆在一张表里，它们的区别一眼就能看清：

| 数字 | 回答的问题 | 取值范围 | 能不能直接卡阈值 | 出现在哪些原语上 | 来源 |
|---|---|---|---|---|---|
| `probability` | 「**这件事**成立的概率有多大」——例如客户想要退款的概率 | 0–1 | 不能当答案置信度用，它是**事件概率** | Noul | `g2-8` |
| `probabilities` | 「每个选项 / 每个等级**各自**有多大概率是答案」——一个覆盖全部选项的分布 | 一个分布 | 可以，但要你自己做数学 | Choice、Score | `g1-26`、`g2-6`、`g2-7` |
| `confidence` | 「把上面那个分布的**形状**压成一个数」 | 单一 0–1 | **可以，官方就是为了让你直接阈值而给的** | Choice、Score（**Noul 没有**） | `g1-27`、`g1-28`、`g2-9` |

其中分布那一行，官方 `G1a` 页的原话是：

> All Score and Choice answers from TypeSafe include a probabilities property representing the probability distribution across the options (for Choice) or levels (for Score).[^c4-2]

也就是说：**分布不是可选项，而是 Choice 与 Score 答案的固有组成部分**（`g1-26`）。`confidence` 是在它之上再加工出来的，官方对 `confidence` 的定义原话是：

> The answer's confidence property collapses that shape into a single number from 0 to 1, so you can threshold on it without doing the math yourself.[^c4-2]

> confidence is a statistic computed from the probability distribution the answer already gives you. TypeSafe computes it for you and returns it on every Choice and Score answer[^c4-2]

注意这两句里的两个动词：**collapses**（把分布压扁）和 **computed from**（由分布算出）。这说明 `confidence` 不是额外独立测量出来的东西，而是**对已有分布的一个加工结果**。这个认识是后面 4.5、4.7 两节的基础。

## 4.2 硬结论一：`probability` ≠ `confidence`

这是本章最需要刻进肌肉记忆的一条。官方在 Vercel 指南里的表述非常直白：

> requestsRefund.probability is the estimated probability that the customer wants money back, not a confidence in the answer.[^c4-3]

把这句话拆成两个方向读：

- `probability = 0.9` 的意思是「**客户有 90% 的概率想要退款**」——说的是**世界上的事实**；
- 它**不是**「模型有 90% 的把握」——模型对自己这个答案有多笃定，由 `confidence` 承担。

| 假设你拿到 | 正确的读法 | 错误的读法 |
|---|---|---|
| `requestsRefund.probability = 0.9` | 客户想要退款这件事发生的概率约 90% | 「模型很确定客户要退款」 |
| `category.confidence = 0.78` | 模型对「它所选的那个类别」的笃定程度被压成 0.78，可直接阈值 | 「这个类别正确率为 78%」 |

> [!tip] 大白话
> 把 `probability` 想成**天气预报的降水概率**：「明天 70% 概率下雨」说的是天会不会下雨，不是预报员对自己有没有把握。`confidence` 才是后者——是预报员那句「这次我挺有底」。
> 所以：**想判断「这件事会不会发生」，看 probability；想判断「这个答案靠不靠得住、要不要交给自动化」，看 confidence。** 两个问题，两个字段。

顺带说清一件事：`confidence` 也不等于「准确率」。它反映的是分布的形状，不是历史命中率。它跟准确率的关系，官方只给了一个方向性表述（「更高置信 = 更高准确」，见第一章 `g1-9`），没有给具体曲线。

## 4.3 硬结论二：`confidence` 只出现在 Choice 与 Score 上

官方 `G1a` 页在同一句里带了一个容易读漏的括号：

> The answer's confidence property collapses that shape into a single number from 0 to 1, so you can threshold on it without doing the math yourself. **(Noul answers don't carry one.)**[^c4-2]

Vercel 指南从另一侧独立印证了同一件事：

> TypeSafe AI also returns a separate confidence statistic for choice and score answers in result.providerMetadata.typesafe.confidence, keyed by question ID.[^c4-3]

两处合起来：

| 原语 | 有没有 `confidence` | 依据 |
|---|---|---|
| **Noul** | **没有** | `g1-27` 官方括号原话；`g2-9` 只提 choice 与 score |
| **Choice** | 有 | `g1-27`、`g1-28`、`g2-9` |
| **Score** | 有 | `g1-27`、`g1-28`、`g2-9` |

这个事实会直接改写你的代码组织方式：**如果你打算写一段通用的「低置信就转人工」的门控逻辑，它不能假设每个答案都带 `confidence` 字段。** Noul 的问题需要另一种判别方式（它自带的是事件概率），Choice / Score 才能走同一套阈值分支。

> [!tip] 大白话
> 把三个原语想成**三种发票**：Choice 和 Score 是那种印了「本单合计」的发票，你可以直接拿合计数字去对账；Noul 是那种只有明细、没有合计的发票，你得自己看明细。
> 所以：门控函数别写成「所有答案都读同一个字段」。先按原语分类，再决定读什么。

## 4.4 硬结论三：`confidence` 是答案对象自己的属性

官方 `G1a` 的措辞是 "**The answer's** `confidence` property"（`g1-27`）——它是答案对象自己的字段。三份响应示例都印证了这一点：

| 示例来源 | 观察到什么 |
|---|---|
| 官方 Quick start 响应示例（`g1-19`） | choice 答案对象内直接出现 `"confidence": 0.78,`，与 `"probabilities": { "technical": 0.85,` 并列[^c4-4] |
| 网关响应示例（`g2-20`） | `"confidence": 0.97,` 直接放在 choice 答案对象内，与 `choice`、`probabilities` 平级[^c4-4] |
| 网关 score 答案（`g2-21`） | 答案含 `score`、`confidence`，另有 `legend` 把等级下标映射回评分文字 |

那么 `result.providerMetadata.typesafe.confidence`（`g2-9`）是什么？它是**平台层把同一个信息重新暴露了一遍**——AI SDK 的调用面习惯把厂商元数据放到 `providerMetadata` 下，并**按问题 ID 索引**。

两处**并存，不是二选一，也不是两套语义**：原生的位置是答案对象内，平台层的位置是 `providerMetadata`。素材对这一点给出的判定是"澄清为调用面差异，非矛盾"。

> [!tip] 大白话
> 想成**快递单上的签收人**：原厂把签收人印在包裹面单上；平台又把这个名字抄了一份到自己系统里，方便按单号查。抄件和原件是同一个信息，不是两个人。
> 所以：你在 AI SDK 里从 `providerMetadata` 读到的 confidence，和原生响应里答案对象内的 confidence，是同一个值。别写两套逻辑去交叉校验它们。

## 4.5 `confidence` ≠ 最高选项的概率

这一条特别容易被顺手写错。看官方自己的响应示例（`g1-19`）：

| 量 | 官方示例里的值 | 是同一个数吗 |
|---|---|---|
| `confidence` | `"confidence": 0.78,` | —— |
| 选中项的概率 | `"probabilities": { "technical": 0.85,` | **不是**（0.78 vs 0.85） |

两个数字在同一份官方示例里明确不相等。结合 4.1 已经确立的事实——`confidence` 是「从**整个分布**算出来的统计量」（`g1-28`）——可以得出结论：**它不是「取最大值」**。差异来源是分布的形状：一个最高选项 0.85 但其余选项也各有分量的分布，压缩出来的置信度会低于 0.85。

> [!tip] 大白话
> 想成**评一支球队强不强**：不是只看它最好的那个球员得了几分，还要看剩下的人跟上没跟上。一个「一人 85 分、队友全是 5 分」的分布，和一个「一人 85 分、队友也都不弱」的分布，压出来的单一数字不会一样。
> 所以：**不要自己写 `max(probabilities)` 来代替 `confidence`。** 那是另一个量。

## 4.6 分布形状：越平坦，置信越低

官方对分布形状与置信度的关系给了一句很实用的判读：

> In both cases a flatter distribution means lower confidence: low confidence on a Choice often means none of the options are a clear winner over the others[^c4-2]

| 分布形状 | `confidence` | 适用场景下的解读 |
|---|---|---|
| 尖峰：一个选项明显高于其他 | 高 | 有明确的胜出选项，可以按阈值放行 |
| 平坦：几个选项彼此接近 | 低 | 对 Choice 而言，官方解释是**没有选项明显胜出**（`g1-30`） |
| 落在中间地带 | 中 | 最需要谨慎的区域——见 4.8 关于阈值余量的提醒 |

对设计者的一个直接推论（**这是推论，不是官方原文**）：遇到 Choice 低置信时，先回看你的选项集——是否存在选项之间互相重叠、或者真实答案根本不在你的选项里。这两种情况下，低置信是**题目设计问题的信号**，而不是模型不稳定。

## 4.7 官方没有锁定 `confidence` 的定义

这一条决定了你在这件事上有多少自由：

> We provide confidence as a convenient measure that fits most use-cases, but you are never locked into our definition.[^c4-2]

意思是：`confidence` 的定位是「**适配多数用例的便利度量**」，不是一个你必须接受的行业标准定义，也不是唯一可用的统计量。实践中的含义：

- 想直接用它做门控——可以，官方就是为此提供的；
- 想按自己的业务口径重新定义——也可以，因为 `probabilities` 本来就在答案里（`g1-26`），你可以自己算一个更贴合自己场景的量；
- 但**不要混着用**：一段门控逻辑里要么用官方 `confidence`，要么用你自算的量，两边来回切会让阈值失去意义。

## 4.8 阈值设计：官方给了一个起点和一条风险曲线

### 4.8.1 第一句话就是「没有普适阈值」

> The correct threshold values depend on your domain and the performance of the model for your use case. Start with conservative thresholds, test with your own data, and adjust[^c4-2]

这句话把责任划得很清楚：**阈值是你要用自己的数据标定出来的**，官方不给一个通用数值。任何「业界通用阈值是 0.8」的传言，在官方口径里都没有对应依据。

### 4.8.2 官方示例给出的起点

Vercel 指南的路由表示例给出了一组起始条件：**置信度 ≥ 0.6，且选中项的概率 ≥ 0.7**，两个条件同时满足才自动分派（`g2-10`）。

注意这里是「**且**」不是「或」——两个数字分别盯着两个不同的量（4.2 的 `confidence` 与 `probability`）。把它读成「达标其一即可」会让门控明显变松。

### 4.8.3 按动作风险上调门槛

官方按「猜错的代价」给出了两档参照：

> Read-only actions like showing a screen can tolerate a wrong guess, so a probability of 0.7 might be enough. Destructive actions need a higher bar, closer to 0.9 or above[^c4-3]

| 动作类型 | 官方示例的参考线 | 为什么 |
|---|---|---|
| 只读动作（例如展示一个界面） | 概率 0.7 可能就够 | 猜错的代价低，用户能自己纠正 |
| 破坏性动作 | 门槛更高，接近 **0.9 或以上** | 猜错之后难以撤销 |

这张表的价值不在于那两个具体数字，而在于它给了一种**按后果设计阈值**的方法：不要把阈值当成模型参数来调，要当成**风险预算**来定。

### 4.8.4 低于阈值时：不执行动作

> **Low confidence:** Do not act. Route to a human, request clarification, or fall back to a different system.[^c4-2]

官方给了三条出路，注意**第一条是「不要执行动作」**，后面三条才是怎么收场：

1. **转人工**——把判断交给人；
2. **请求澄清**——信息不足，向用户追问；
3. **降级到另一个系统**——换一个模型或换一条路径处理。

### 4.8.5 关于 0.5 这个数字

官方 `G1a` 页里出现过一条 0.5 的阈值示例：

> The 0.5 confidence floor catches anything the model reports as genuinely uncertain.[^c4-2]

**这是该页示例里的取值，不是普适标准**——这一点必须和 4.8.1 的「没有普适阈值」放在一起读，否则很容易把一个示例数当成默认值抄进生产代码。同理，`S06` 的 0.6 / 0.7 与这里的 0.7 / 0.9 都是**示例起点**，它们之间数值不一致，恰恰印证的正是「按领域自测标定」这条原则。

### 4.8.6 一条落地检查清单（本节建议，非官方原文）

| # | 动作 | 依据 |
|---|---|---|
| 1 | 用自己的数据标定，不要抄通用数值 | `g1-33` |
| 2 | 起点可用「置信度 0.6 **且** 选中项概率 0.7」 | `g2-10` |
| 3 | 按动作风险上调：只读约 0.7、破坏性接近 0.9 以上 | `g2-11` |
| 4 | 低于阈值**不执行动作**，转人工 / 澄清 / 降级 | `g1-32` |
| 5 | 日志里同时记下 `confidence`、`probability` 与响应侧的具体 `model` 版本 | `g1-22`（第三章 3.4） |

第 5 条不是官方要求，是让你能回测阈值的手段：只有记下当时用的具体版本和当时的置信度，事后才能回答「这个阈值到底该往上还是往下调」。

## 4.9 未解：同一厂商两个页面，口径互相矛盾

本节是本章必须如实交代的一处**未解矛盾**，请注意它的性质：**不是官方与第三方的分歧，而是同一个厂商的两个官方页面之间的分歧。**

**一侧：官方博客（`S01`）**

> All answers are accompanied with calibrated probabilities and confidence scores.[^c4-1]

> Always communicates confidence and uncertainty with every output.[^c4-1]

**另一侧：官方 Confidence 文档页（`G1a`）**

> (Noul answers don't carry one.)[^c4-2]

矛盾点很具体：博客的说法是「所有答案都伴随校准概率与置信分数」「每次都传达置信与不确定」；而 Confidence 页明确括号注明 **Noul 的答案不带 `confidence`**。

**本轮素材对这一条的裁决状态是「未解」。** 原话是：同一厂商两页互相矛盾，**本轮没有第三份官方材料可以裁决**。

本笔记在这里不做以下三件事：

- 不说「博客那句话只是写得宽泛」——这是猜测，不是依据；
- 不说「可能是两个页面更新不同步」——素材里没有任何时间戳证据支持；
- 不给一个「其实两边都对」的调和说法。

**存在的就是矛盾本身，本轮无法判定谁代表当前实现。**

对你的实际影响只有一条，但它很重要：**如果 Noul 的 `confidence` 字段对你的门控设计是必需的，不要依据博客那句话写代码**——先实测一次 Noul 的答案里到底有没有这个字段，再决定你的分支怎么写。Confidence 页与博客两处都已列在脚注里，你可以自己去核对这两个页面的当前状态。

> [!tip] 大白话
> 像**同一家店的两张宣传单**：一张写着「所有商品都送赠品」，另一张小字写着「赠品不含 X 类商品」。你不知道哪张是印刷错误、哪张是后来改的规。此时正确的做法不是自己挑一张信，而是去柜台问清楚。
> 所以：这一节的作用不是给你答案，是提醒你这块地界**还没定论**，别把它写进无人复核的自动化逻辑里。

## 本章小结

- 一个答案里有三种数字，**不能混用**：`probability` 说的是事件成立的概率（`g2-8`）；`probabilities` 是各选项 / 各等级的完整分布（`g1-26`、`g2-6`、`g2-7`）；`confidence` 是把分布形状压成的 0–1 统计量，专为直接阈值而给（`g1-27`、`g1-28`）。
- `confidence` **只出现在 Choice 与 Score 上，Noul 没有**（`g1-27` 官方括号原话 + `g2-9` 独立印证）；门控代码不能假设每个答案都带这个字段。
- `confidence` 是**答案对象自己的属性**；AI SDK 在 `providerMetadata.typesafe.confidence` 的暴露是平台层重新显影，**不是另一套语义**（`g1-27`、`g1-19`、`g2-20`、`g2-21`、`g2-9`）。
- `confidence` **不等于最高选项概率**：官方示例中 0.78 与 0.85 并不相等（`g1-19`）；它由整个分布算出，分布越平坦置信越低，Choice 低置信常意味着没有明显胜出选项（`g1-28`、`g1-30`）。
- 官方**没有普适阈值**，需按领域自测标定（`g1-33`）；示例起点为「置信度 ≥0.6 且选中项概率 ≥0.7」（`g2-10`），并按动作风险上调——只读约 0.7、破坏性接近 0.9 以上（`g2-11`）；低置信时**不执行动作**，转人工、请求澄清或降级（`g1-32`）；0.5 是该页示例取值，不是通用标准（`g1-34`）。
- **未解矛盾（C7）**：`S01` 博客称答案都伴随校准概率与置信分数、每次都传达置信与不确定（`g1-5`、`g1-9`），而 `G1a` 页括号写明 Noul 答案不带 `confidence`（`g1-27`）。同一厂商两页互相矛盾，本轮无第三份官方材料可裁决——本笔记并列原文，不做调和。

## 下一章预告

到这里，「读一次结果」的闭环已经完成：发得出调用，也看得懂答案里的每个数字。第五章换到工程视角：**怎么把它接进一个真实系统**——输入 token 是唯一付费项带来的成本控制思路、上下文上限的约束、官方给出的三种设计模式（投机性一次多问、置信度门控路由、多维度合成分），以及生态接入点目前能确认到哪一步。

第五章也有两处会明确标成**待补**：LangChain 的「Jev-as-a-Judge」样板与 Claude Code 的 `fast-jev-compaction` 压缩插件，本轮素材均未抓取。

---

[^c4-1]: TypeSafe 官方博客《Introducing System One Models and Jev》，2026-09-15。[typesafe.ai](https://typesafe.ai/blog/introducing-system-one-models-and-jev)（来源 ID `S01`）
[^c4-2]: TypeSafe 官方 Confidence 文档页（来源 ID `G1a`）。[docs.typesafe.ai](https://docs.typesafe.ai/confidence)（该页阈值示例代码在本轮抓取时比较运算符丢失，故本章仅引其散文句）
[^c4-3]: Vercel AI SDK 指南《TypeSafe Jev and AI SDK》，2026-09-19（来源 ID `S06`）。[vercel.com](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)
[^c4-4]: 官方 Quick start 响应示例与 AI/ML API 网关文档（来源 ID `S07`、`S08`）。[docs.typesafe.ai](https://docs.typesafe.ai/introduction/quickstart) · [docs.aimlapi.com](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev)（两页代码块在本轮抓取时均有损坏，本章仅使用其中的字段名）

---

> [!info] 分册导航
> ← [[Jev 03 三原语与最小调用|第 3 章 · 三原语与最小调用]] · 🗂 [[Jev 决策模型 MOC|目录]] · [[Jev 05 接入与设计模式|第 5 章 · 接入与设计模式]] →
