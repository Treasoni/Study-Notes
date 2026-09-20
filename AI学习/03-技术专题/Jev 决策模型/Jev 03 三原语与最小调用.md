---
title: "第三章：三原语与一次最小调用"
tags: [ai, jev, 决策模型, typesafe-ai]
created: 2026-09-20
updated: 2026-09-20
status: new
source_project: jev-decision-model
---

> [!info] 分册导航
> ← [[Jev 02 性能与定价|第 2 章 · 性能与定价]] · 🗂 [[Jev 决策模型 MOC|目录]] · [[Jev 04 读结果与阈值设计|第 4 章 · 读结果与阈值设计]] →

# 第三章：三原语与一次最小调用

前两章我们看的是定位和数字，都是「读」的部分。这一章开始「写」：一次调用具体往哪里发、请求里放什么、三种问题分别长什么样、回来的东西怎么和你的问题对上。

先给一句结论，好让你带着靶子读：**一次调用的全部结构，就是「一段材料」加上「一组带类型的问题」。** 剩下的都是细节。

> [!warning] 本章代码纪律（请先读这一条）
> - 官方 Quick start 页（`S07`）与 Vercel 指南（`S06`）的代码块在本轮抓取时**结构损坏**——丢了括号、丢了比较运算符；AI/ML API 网关页（`S08`）的 JSON 代码块被截断。
> - 因此：**本章所有代码与 JSON 都是「结构示意」，不是官方原文，也不得原样照抄。** 字段名可以使用（它们取自官方示例），但**嵌套结构与必填 / 可选状态本轮无法确认**，落地前必须回官网原页核对。
> - 官方定义原语的 `/primitives` 页**本轮未抓取**，所以本章（以及全篇）**不会出现「官方 schema」这种表述**，也不会把字段的必填性写成规范。

## 3.1 一次调用的形状

官方文档给出的端点是：

> `POST https://api.typesafe.ai/v1/systemone`[^c3-1]

请求体有两个部分，它们的角色分工可以这样理解：

> The state is whatever you want the model to look at, and each key in questions becomes a key in answers.[^c3-2]

这句话是本章最重要的一句，因为它同时定义了三件事：

| 部分 | 是什么 | 谁决定它 |
|---|---|---|
| `state` | 你想让模型看的材料——「whatever you want the model to look at」 | 你，随便放什么，不需要先规整 |
| `questions` | 一组「问题键 → 带类型的问题」 | 你，每个问题的类型和取值空间都由你事先定义 |
| `answers` | 返回的答案，**键与 `questions` 的键一一对应** | 模型，键由你决定 |

「键一一对应」是这一段最实用的信息：你给问题起什么名，答案就用什么名回来。这意味着**问题的键就是你下游代码的变量名**，起名时按你代码里怎么用最方便来起（例如 `requestsRefund`、`urgencyLevel`），而不是按给人看的标题来起。

请求的整体形状（`scripts/example_request.jsonc`，**结构示意，字段名取自官方示例，嵌套与必填性未确认**）：

```jsonc
// scripts/example_request.jsonc —— 结构示意，非官方原文，需回官网核对
{
  "state": "客户留言：……（这里放你想让它看的材料）",
  "questions": {
    "requestsRefund": {
      "type": "noul",                 // 是否类问题
      "instructions": "客户是否要求退款"
    },
    "category": {
      "type": "choice",               // 多选一
      "instructions": "这条留言属于哪个类别",
      "criteria": {                   // choice 的 criteria 是「字典」：选项名 → 说明
        "billing": "账单与扣费问题",
        "logistics": "物流与配送问题",
        "technical": "技术故障问题"
      }
    }
  }
}
```

**预期结果（形状）**：`answers` 里出现同名的 `requestsRefund` 与 `category` 两个键，键名与你写的完全一致；具体字段见 3.4。

> [!note] 关于上面示例里的 `instructions` 字段
> 素材只在 **Noul** 的问题说明里明确提到问题带 `instructions`（`g1-16`）。本章示例为了让三段结构看起来一致，给 Choice / Score 也写了同名字段——**这只是示意的写法，Choice / Score 是否使用同名的问题描述字段，本轮素材无法确认**，请回官网原页核对。这正是 3.6 第 1、2 条要提醒的事情。

## 3.2 三原语：Noul、Choice、Score

先说命名，因为这是最容易在生态文档之间走丢的一处。官方文档里的名字是这三个：

> Mix Noul, Choice, and Score in one call and see all results at once.[^c3-1]

你在别的平台文档里会看到 `boolean` 这样的叫法（Vercel 平台侧，`S06`），网关文档里则写 `noul`（`S08`）。**这不是矛盾**：官方名是 **Noul / Choice / Score**，`boolean` 是平台侧的叫法，指的是同一种原语。写代码时以官方文档的字段值为准，读平台文档时知道它说的是同一个东西即可。

三者的区分不在「难易」，而在**答案空间的形状**：

| 原语 | 回答什么 | 答案空间 | `criteria` 字段的形态 |
|---|---|---|---|
| **Noul** | 是否类问题（yes / no） | 两个取值 | **没有 `criteria` 字段**，问题带 `instructions`（`g1-16`） |
| **Choice** | 多选一 | 事先枚举的选项集合，**上限 255 个选项**（`g2-2`） | `"criteria": {` —— **字典**：选项名 → 说明（`g1-17`） |
| **Score** | 有序等级打分 | 事先定义的有序等级序列 | `"criteria": [` —— **列表**：有序等级（`g1-18`） |

> [!tip] 大白话
> 把三个原语想成**三种不同的问卷题型**：Noul 是判断题（打勾或打叉），Choice 是单选题（选项必须提前印在卷子上），Score 是评分题（1 分到 5 分那种有序刻度）。
> 所以：**你不是在教它怎么思考，而是在给这三个题型写题目。** 选错题型的后果很直接——你想问「这条属于哪一类」却用了 Noul，就永远拿不到「技术故障」这个答案。

### 3.2.1 Choice：criteria 是字典，选项名就是返回值

Choice 的 `criteria` 用**字典**表达「选项名 → 说明」。上面 3.1 的示例已经是这个形状。要点有两个：

- **字典的键（选项名）会直接出现在答案里**——它是你下游要分支的值，所以要起成代码里好用的标识符，而不是长句；
- **字典的值（说明）是给人/给模型读的补充描述**，用来消歧。选项边界模糊时，说明写得越清楚越省事。

选项上限是 **255**（`g2-2`，来源 `S06`）。这个上限的意义在第七章还会用到：第三方实测里「超大选项集」是已知弱项（Banking77 那一档），所以 255 是**能力上限，不是舒适区**。

### 3.2.2 Score：criteria 是列表，等级是有序的

Score 的 `criteria` 换成**列表**，表示一条有序的等级序列（`g1-18`）。有序这两个字是关键：列表里的顺序就是等级顺序，`Score` 的答案取值落在这些等级上。示意（**结构示意，需回官网核对**）：

```jsonc
// scripts/example_score_question.jsonc —— 结构示意，非官方原文，需回官网核对
{
  "urgency": {
    "type": "score",
    "instructions": "这条留言的紧急程度",
    "criteria": [          // score 的 criteria 是「列表」：有序等级
      "不紧急",
      "低",
      "中",
      "高",
      "需立即处理"
    ]
  }
}
```

### 3.2.3 Noul：没有 criteria，只有是 / 否加一个概率

Noul 的特别之处在于它**没有 `criteria` 字段**（`g1-16`）——因为答案空间是固定的两个取值，没什么需要枚举的。它返回的是「是 / 否」加上一个概率，这个概率的含义在第四章会专门拆开讲，这里只需要记住它的形状：

```jsonc
// scripts/example_noul_question.jsonc —— 结构示意，非官方原文，需回官网核对
{
  "requestsRefund": {
    "type": "noul",                    // 注意：noul 没有 criteria 字段
    "instructions": "客户是否要求退款"
  }
}
```

## 3.3 state：不用自己序列化

关于 `state` 的内容，官方给了一句很省事的说明：

> you can pass a record or a message history without serializing it yourself[^c3-2]

也就是说，`state` 既接受**一条记录**（JSON 对象），也接受**一段消息历史**（数组），你不需要先把它压成字符串再塞进去。实际影响是：

| 你想放进 state 的东西 | 需要自己序列化吗 |
|---|---|
| 一条工单的字段集合 | 不需要，直接作为对象传 |
| 一段多轮对话历史 | 不需要，直接作为数组传 |
| 一段纯文本材料 | 作为字符串传即可 |

> [!tip] 大白话
> 把 `state` 想成一个**透明文件袋**：你把手上的东西直接放进去就行，不用先扫描成 PDF、也不用先抄到标准表格上。
> 所以：省掉的不是一步代码，而是「为了让它能看懂而先规整一遍」的那种前置清洗。真正该操心的是「放多少进去」，那是第五章成本话题的内容。

## 3.4 读响应：答案怎么和问题对上

响应里 `answers` 的键与 `questions` 的键一一对应（3.1 已引 `g2-1`）。每种原语的答案内部形状不同：

| 原语 | 答案里有什么 | 说明 | 来源 |
|---|---|---|---|
| Noul | 一个「是 / 否」的取值 + 一个概率 | 概率的具体含义见第四章，**不要在第三章就把它当置信度用** | `g1-16` |
| Choice | `choice` + `probabilities` | `probabilities` 是**按选项键展开的完整分布**，选中项最高 | `g2-2`、`g2-6` |
| Score | `score` + `probabilities` | 分布的键是**字符串形式的等级下标**（如 `"0"`、`"1"`…），不是等级文字 | `g2-7` |

「字符串形式的等级下标」是一个很容易踩的坑：Score 的分布不是用你写的等级文字做键，而是用下标。这意味着把它映射回可读文字需要你自己持有一份 `criteria` 列表做对照（网关文档的响应示例里还带了一个 `legend` 字段做这件事，`g2-21`——注意那是平台侧的重新暴露形态，不构成对原语语义的另一套定义）。

响应里还带两个和运维直接相关的字段：

| 字段 | 内容 | 用途 | 来源 |
|---|---|---|---|
| `"model"` | 实际执行的具体版本，例如 `"model": "jev-1.13.0"` | 记录日志、复现问题时用这个，不要记请求侧的值 | `g1-22` |
| `"input_tokens"` | 本次请求的输入 token 数，例如 `"input_tokens": 392,` | 成本核算的唯一入场券（输入 token 是唯一付费项，详见第五章） | `g1-23` |

请求侧与响应侧的版本处理方式不同，这一点值得单独记住：

- **请求侧**默认传 `"jev-latest"`（`g1-22`）——你写的是「最新版」这个别名；
- **响应侧**回传的是具体版本号（`g1-22`）——真正跑了哪个版本。

> [!tip] 大白话
> 想成**点外卖**：你下单时写的是「主厨推荐」（`jev-latest`），小票上印的是真正做这道菜的那位师傅的工号（`jev-1.13.0`）。
> 所以：出问题时拿小票上的工号去查，别拿下单时那三个字。日志里记响应侧的 `model` 字段。

## 3.5 用 Python SDK 跑一次最小调用

官方 Quick start 给出的 SDK 前提与默认行为：

> Install the SDK (requires Python >= 3.10).[^c3-1]

> The client reads TYPESAFE_API_KEY from the environment and calls jev-latest by default.[^c3-1]

这两句合起来说明了三件事：**需要 Python 3.10 及以上**；**API key 从环境变量 `TYPESAFE_API_KEY` 读**，不用写进代码；**默认调 `jev-latest`**。

下面这个最小调用是**结构示意**（`scripts/jev_min_call.py`）：三个原语各问一个问题、一次调用拿回全部答案。

```python
# scripts/jev_min_call.py —— 结构示意，非官方原文，需回官网核对后再运行
# 前置：Python >= 3.10；环境变量 TYPESAFE_API_KEY 已设置
from typesafe import TypeSafe  # 客户端从环境读取 TYPESAFE_API_KEY

client = TypeSafe()

result = client.systemone.create(
    state="客户留言：上周下的单到现在还没发货，我要退款！",
    questions={
        # ① Noul：判断题
        "requestsRefund": {
            "type": "noul",
            "instructions": "客户是否要求退款",
        },
        # ② Choice：单选题（选项名会成为返回值）
        "category": {
            "type": "choice",
            "instructions": "这条留言属于哪个类别",
            "criteria": {
                "billing": "账单与扣费问题",
                "logistics": "物流与配送问题",
                "technical": "技术故障问题",
            },
        },
        # ③ Score：有序评分题（等级顺序即列表顺序）
        "urgency": {
            "type": "score",
            "instructions": "这条留言的紧急程度",
            "criteria": ["不紧急", "低", "中", "高", "需立即处理"],
        },
    },
)

# answers 的键与 questions 的键一一对应
print(result.answers)
print(result.model)          # 响应侧回传的具体版本，如 jev-1.13.0
print(result.input_tokens)   # 本次输入 token 数，用于成本核算
```

**预期输出（形状示意，数值为占位符，不是官方实测数据）**：

```text
# 预期输出形状（字段名取自官方示例；数值为占位符）
{
  "requestsRefund": { "answer": true,  "probability": 0.9x },
  "category":       { "choice": "logistics",
                      "probabilities": { "billing": 0.0x,
                                         "logistics": 0.8x,
                                         "technical": 0.1x } },
  "urgency":        { "score": 3,
                      "probabilities": { "0": 0.0x, "1": 0.0x,
                                         "2": 0.2x, "3": 0.6x, "4": 0.1x } }
}
# model: jev-1.13.0（示意）
# input_tokens: 392（官方示例中出现的数值）
```

请特别注意上面这段的每一处标注：**字段名可用，数值是占位符**。之所以不给出一份「看起来像真的」响应示例，是因为官方响应示例所在的代码块在抓取时已损坏，本轮无法确认完整的嵌套结构与字段必填性——任何补全都是我替你猜的。

关于 SDK 生态，还有一条需要明确的边界：**本轮素材中没有找到官方 JavaScript SDK**，只有 Python SDK 与 curl 两种调用途径（`g1-24`、`g1-25`，素材缺口六·7）。如果你的技术栈是 TS，目前要靠 HTTP 直接调端点，或者走第三方平台侧封装（`S06`、`S08` 那类）。

## 3.6 本章必须一起带走的六条注意

| # | 注意 | 为什么 |
|---|---|---|
| 1 | **没有规范性 schema 来源**：`/primitives` 页本轮未抓，字段名只来自请求 / 响应示例 | 所以本章（全篇）不出现「官方 schema」表述；字段的必填 / 可选状态**未确认** |
| 2 | **嵌套结构未确认**：`S07` 代码块丢括号，`S08` JSON 被截断 | 不要按本章的缩进层级去推断真实嵌套，回原页核对 |
| 3 | **代码不可照抄**：`S06`（Vercel）的 TS 被重排且比较运算符丢失 | 本章代码仅作形状示意；照抄会得到跑不起来的代码 |
| 4 | **Noul 是官方名**，平台侧叫 `boolean`、网关侧叫 `noul` | 这是同一原语的不同叫法，不是矛盾 |
| 5 | **官方未找到 JS SDK** | 只有 Python SDK（≥3.10）与 curl；key 从 `TYPESAFE_API_KEY` 读 |
| 6 | **Score 的分布键是字符串下标**，不是等级文字 | 映射回可读文字需要自己持有 `criteria` 列表对照 |

## 3.7 一次最小调用的落地检查表

把本章的内容压成一张动手时的清单。**「需核对」一栏请务必回官网原页确认后再落地**——本章素材不足以替你确认这些字段。

| # | 检查项 | 本章给出的答案 | 状态 |
|---|---|---|---|
| 1 | 端点 | `POST https://api.typesafe.ai/v1/systemone`（`g1-15`） | 可用 |
| 2 | 认证 | Python SDK 从环境变量 `TYPESAFE_API_KEY` 读取（`g1-25`） | 可用 |
| 3 | 请求三件套 | `state`（材料）+ `questions`（问题键 → 带类型问题）→ 响应 `answers`（键一一对应）（`g2-1`） | 可用 |
| 4 | 问题键怎么起名 | 按数值在下游代码里的用途起名，键名会直接成为答案的键（`g2-1`） | 可用 |
| 5 | 原语选型 | 是 / 否 → `noul`；多选一 → `choice`（选项 ≤255）；有序打分 → `score`（`g1-16`、`g1-17`、`g1-18`、`g2-2`） | 可用 |
| 6 | `state` 怎么给 | 对象、数组（消息历史）、字符串都可以，不用自己序列化（`g2-5`） | 可用 |
| 7 | 日志记什么 | 响应侧的具体版本（如 `jev-1.13.0`）与 `input_tokens`（`g1-22`、`g1-23`） | 可用 |
| 8 | 字段嵌套与必填性 | **无规范性来源**，字段名只来自示例 | **需核对** |
| 9 | Choice / Score 是否也有 `instructions` 类字段 | 素材只在 Noul 上确认过（`g1-16`） | **需核对** |
| 10 | JS / TS 官方 SDK | 本轮**未找到**，仅 Python SDK 与 curl | 现状，非缺陷 |

## 本章小结

- 一次调用的全部结构是「`state`（随便放什么材料）+ `questions`（问题键 → 带类型的问题）」，答案的键与问题的键**一一对应**；问题的键就是你下游的变量名（`g1-15`、`g2-1`）。
- 三原语的区分在**答案空间形状**：Noul（是 / 否，**无 `criteria`**）、Choice（多选一，`criteria` 是**字典**，选项上限 **255**）、Score（有序等级，`criteria` 是**列表**）；官方名就是 Noul / Choice / Score，平台侧 `boolean` 不是矛盾（`g1-14`、`g1-16`、`g1-17`、`g1-18`、`g2-2`）。
- `state` 接受对象或消息历史，**不需要自己序列化**（`g2-5`）。
- 读响应：Choice 返回 `choice` + 按选项键展开的完整 `probabilities`，Score 返回 `score` + **字符串下标为键**的 `probabilities`；响应带 `input_tokens` 用量，并回传**具体版本**（请求侧默认 `jev-latest`）（`g2-6`、`g2-7`、`g1-22`、`g1-23`）。
- Python SDK 需 **≥3.10**，从环境读 `TYPESAFE_API_KEY`，默认调 `jev-latest`；**未找到官方 JS SDK**（`g1-24`、`g1-25`）。
- 本章代码与 JSON 全部是**结构示意**，字段名可用、嵌套与必填性未确认、不得原样照抄；本篇不出现「官方 schema」表述。

## 下一章预告

一次调用你已经会发了，问题随之变成：**回来的那些数字怎么读**。

下一章的题目听起来只差一个词，但差得很关键——`probability` 和 `confidence` 在 Jev 里**不是一回事**：一个说的是「这件事有多少概率成立」，另一个是把整个分布压成一个 0–1 的数好让你直接卡阈值。第四章还会给出官方的阈值建议（以及官方明确「没有普适阈值」这句话）、低置信时该做什么，并且在末尾如实并列一处**同一厂商两个页面互相矛盾**的表述——那一处本轮没有第三份官方材料可以裁决。

---

[^c3-1]: TypeSafe 官方 Quick start（来源 ID `S07`）。[docs.typesafe.ai](https://docs.typesafe.ai/introduction/quickstart)（该页代码块在本轮抓取时结构损坏，故本章仅使用其字段名与散文句）
[^c3-2]: Vercel AI SDK 指南《TypeSafe Jev and AI SDK》，2026-09-19（来源 ID `S06`）。[vercel.com](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)（该页 TS 代码被重排、比较运算符丢失，本章仅引其散文说明）

---

> [!info] 分册导航
> ← [[Jev 02 性能与定价|第 2 章 · 性能与定价]] · 🗂 [[Jev 决策模型 MOC|目录]] · [[Jev 04 读结果与阈值设计|第 4 章 · 读结果与阈值设计]] →
