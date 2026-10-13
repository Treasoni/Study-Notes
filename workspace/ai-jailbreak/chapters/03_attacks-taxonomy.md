# 第 3 章：如何破甲——攻击分类与原理（机制层，不含载荷）

## 3.1 一句话看懂 + 安全边界声明

这一章回答第三个问题：**如何破甲**。但请先把话说在前面——本章讲的是「这东西**凭什么**能钻空子」，**不是**「怎么照做」。

先划边界：本章只写**机制、分类、原理和已核实的统计**。它**不会**给出任何可直接使用的破甲提示、逐步绕过配方或可复现的载荷，也不会写出任何具体密码名、算法实现或对抗后缀串。理由很直接——本手册是安全视角的学习笔记，不是操作手册；把「为什么能钻空子」讲清楚，已经足够让你读懂一手材料、理解防御为什么难。至于「怎么防」，是后面的事。

所谓「不含载荷」，具体一点说：本章连一个能直接复制粘贴去攻击模型的输入片段都不会出现——你读到的是「这一类是怎么起作用的」，而不是「这一类该怎么写」。凡是需要给出示例串才能讲下去的地方，本手册宁可讲到机制为止。

类比先摆上：破甲作者并不需要一把万能钥匙，他更像拿着一把钥匙去**试一排锁**——锁是同一种锁（都建在对齐这一层），钥匙是同一种思路（绕过「拒绝」这个偏好），试到哪把开了就用哪把。本章的七类机制，就是这排锁最常见的七种形态。

## 3.2 一张表看懂七类机制

按「从哪个层面下手」，本章把破甲归成七类。**这张表是自建的**（依据见 3.6），每类只给一句机制说明，不给任何示例串。

**表 3-1　七类机制**

| 类别 | 机制一句话 | 代表（论文名，不含载荷） | 起作用层面 | 出处 |
| --- | --- | --- | --- | --- |
| 多示例 many-shot | 单条提示里塞进大量「已照做」的示范，末接真实问题 | many-shot | 输入上下文 | sources/U7_many-shot.md:29 |
| 角色扮演 roleplay | 让模型扮演一个「不受限」的角色来作答 | Anthropic 红队研究 | 人机交互 | sources/U8_red-teaming-harms.md:138 |
| 自动优化后缀 GCG | 用搜索自动生成一段附加后缀，逼模型更可能「答应」 | GCG | 表征 | sources/U10_gcg.md:10 |
| 编码 / 密码 cipher | 用非自然语言承载请求，绕开只在自然语言上做的对齐 | CipherChat | 表征 | sources/U28_cipher.md:10 |
| 多轮渐进 Crescendo | 从无害问题起步，逐轮引用模型自己的回复升级 | Crescendo | 时间 | sources/U27_crescendo.md:10 |
| 说服 PAP | 用社会科学的说服策略把请求重述一遍 | PAP | 人机交互 | sources/U22_persuasion.md:10 |
| 自动化红队 PAIR | 用一个攻击者 LM 迭代生成、打分、改进攻击 | PAIR | 人机交互 / 自动化 | sources/U9_red-teaming-lms.md:18 |

上面这张表按「机制」分类；如果换成按「下手的位置」看，七类会更清楚地落进四个层面。

**表 3-2　攻击模式 × 作用层面**

| 作用层面 | 涵盖机制 | 为什么在这一层起作用 |
| --- | --- | --- |
| 输入上下文 | 多示例 many-shot | 在提示本身堆示范，改变模型「照做」的先例 |
| 表征 | 自动优化后缀 GCG、编码 / 密码 cipher | 从输入的表征形态下手，绕开只在自然语言上做的对齐 |
| 时间 | 多轮渐进 Crescendo | 把一次越界拆成多轮，每轮看上去都不越界 |
| 人机交互 | 角色扮演 roleplay、说服 PAP、自动化红队 PAIR | 借模型的「乐于助人 / 合作」倾向，或让它自己去找漏洞 |

把两张表叠起来看，会发现一件事：七类机制里真正作用在「说的内容」上的其实只有一类（many-shot 那种在提示里堆示范的做法），其余大多作用在**内容与护栏之间的那层界面**——语言形态、时间顺序、对话关系。这恰好呼应第 2 章：护栏是在「自然语言、单轮、正常对话」的分布上训练出来的；一旦跳出这个分布，它就容易失灵。

七类里没有哪一类是「最厉害」的——它们只是下手的位置不同，而威胁之所以成立，共同原因是 3.5 要说的事。

## 3.3 逐类原理展开

下面每一类只讲「机制一句话 + 一条机制性引文」，不出现任何示例串或配方。读的时候请留意一个贯穿七类的套路：多数机制并不是去「破解」护栏，而是去**改变问题的语境**——把一个模型训练时没见过的组合递给它，让它在陌生的语境里做出错误的选择。护栏没有坏，它只是没被这样问过。

### 3.3.1 提示内上下文操纵：多示例（many-shot）

机制：在一条提示里堆进大量「问答示范」，每一对都演示「模型照做了」；示范堆到一定数量后，最后那个真实问题就被顺势回答。研究人员给出的量级是“However, simply including a very large number of faux dialogues preceding the final question—in our research, we tested up to 256—produces a very different response.”（中译：只要在最终问题前放入极大量的虚构对话，就会得到截然不同的回答——在我们的研究中测试了多达 256 段。）出处 sources/U7_many-shot.md:29。它的效果还会随示范数量按**幂律**上升「The effectiveness of many-shot jailbreaking increases as we increase the number of “shots” (dialogues in the prompt) according to a scaling trend known as a power law」（中译：多示例破甲的有效性随「示例」数量按幂律增长。）出处 sources/U7_many-shot.md:39。**示范越多，越难拦**——这正对上第 2 章说的「泛化不匹配」。

### 3.3.2 人格与角色层：角色扮演（roleplay）

机制：利用模型被训练出的「乐于助人」，请它扮演一个反派角色，再借角色的口说出内容“In a roleplay attack we exploit the helpfulness of the model by asking it to roleplay as a malevolent character.”（中译：在角色扮演攻击中，我们利用模型的「乐于助人」倾向，让它扮演一个反派角色。）出处 sources/U8_red-teaming-harms.md:138。要害在于**责任被推给了「角色」**：模型觉得「是那个反派说的，不是我」，护栏的判定就松了。

### 3.3.3 优化式攻击：对抗后缀（GCG）

> [!tip] 进阶 / 可跳过
> 这一节的搜索与梯度细节偏技术，不了解不影响主线。

机制：不靠人手工编，而是让算法**自动搜**出一段「后缀」，把它接在任意有害请求后面，就能让模型更可能「答应」而不是「拒绝」：“our approach automatically produces these adversarial suffixes by a combination of greedy and gradient-based search techniques”（中译：我们的方法通过贪心搜索与梯度搜索的组合，自动生成这些对抗后缀。）出处 sources/U10_gcg.md:10。它最麻烦的地方在于**可迁移**：“the resulting attack suffix is able to induce objectionable content in the public interfaces to ChatGPT, Bard, and Claude, as well as open source LLMs such as LLaMA-2-Chat, Pythia, Falcon, and others”（中译：该后缀能在 ChatGPT、Bard、Claude 的公开接口及 LLaMA-2-Chat、Pythia、Falcon 等开源 LLM 上诱出不良内容。）出处 sources/U10_gcg.md:10。在一批模型上试出来的后缀，能直接搬到另一批模型上——这就是「同一把钥匙试很多把锁」最直白的一例。

### 3.3.4 表征层规避：编码 / 密码（cipher）

> [!tip] 进阶 / 可跳过
> 这一节只讲机制，不涉及任何具体密码或算法实现。

机制：对齐主要在**自然语言**上做，于是有人把请求换成**非自然语言**的形态来承载，绕开只在自然语言上生效的那层对齐“we discover that chat in cipher can bypass the safety alignment techniques of LLMs, which are mainly conducted in natural languages.”（中译：我们发现，用密码交谈可以绕过 LLM 的安全对齐——而这类对齐主要是在自然语言上进行的。）出处 sources/U28_cipher.md:10。这里刻意不写任何具体密码名或算法——你只需记住一句话：**换一种「语言」说同一件事，护栏可能就不认识了**。

### 3.3.5 时间维度：多轮渐进（Crescendo）

机制：单轮被拦，就拆成多轮。从一个人畜无害的问题起步，每一轮都引用模型上一轮自己的回答，慢慢把话题推到敏感处“Crescendo is a simple multi-turn jailbreak that interacts with the model in a seemingly benign manner.”（中译：Crescendo 是一种简单的多轮破甲，它以看似无害的方式与模型交互。）出处 sources/U27_crescendo.md:10。要害在于**每一步看上去都不越界**：护栏在每一轮都觉得「这没什么」，于是被一步步带过了界。

### 3.3.6 社会工程：说服（PAP）

机制：用源自社会科学的说服策略，把同一个请求「换个说法」再说一遍“we propose a persuasion taxonomy derived from decades of social science research.”（中译：我们提出一套源自数十年社会科学研究的说服分类法。）出处 sources/U22_persuasion.md:10。它攻的不是技术漏洞，而是模型被训练出来的「对人的礼貌与合作」——你说得越像在讲道理，它越容易顺着你走。

### 3.3.7 自动化红队：PAIR / LM 生成攻击

机制：前几类是「人想出来的招」，这一类是「让模型自己找招」——用**一个语言模型当攻击者**，自动生成、迭代、改进对目标模型的攻击“we generate test inputs using an LM itself, and we use a classifier to detect harmful behavior on test inputs”（中译：我们用一个语言模型自身来生成测试输入，并用分类器检测测试输入上的有害行为。）出处 sources/U9_red-teaming-lms.md:18。它的效率很高“Empirically, PAIR often requires fewer than twenty queries to produce a jailbreak, which is orders of magnitude more efficient than existing algorithms.”（中译：实测中，PAIR 常能在少于二十次查询内产出一次破甲，比既有算法高效了数个数量级。）出处 sources/U26_pair.md:10。**攻击开始自动化，就意味着它不再依赖个人的「灵感」**。

## 3.4 关键统计速览（只列已核数字）

- **在野规模**：一项研究分析了 **1,405** 条破甲提示，时间跨度 2022 年 12 月至 2023 年 12 月“we conduct a comprehensive analysis of 1,405 jailbreak prompts spanning from December 2022 to December 2023.”（中译：我们对 2022 年 12 月至 2023 年 12 月间的 1,405 条破甲提示做了全面分析。）出处 sources/U11_do-anything-now.md:10。其中 **5** 条高效提示在 GPT-3.5 / GPT-4 上达到 **0.95** 攻击成功率，最早的一条已在线超过 **240** 天（数据同源，sources/U11_do-anything-now.md:10）。
- **可迁移性**：自动生成的对抗后缀能跨模型生效（见 3.3.3，sources/U10_gcg.md:10）。
- **自动化效率**：自动化版 Crescendo 在 AdvBench 子集上超过当时的最好方法——GPT-4 上高 **29–61%**、Gemini-Pro 上高 **49–71%**（据摘要，sources/U27_crescendo.md:10）。

**口径提醒**：以上数字各自出自不同论文的**自己的设定与判官**，不能横向直接比大小。要比较，先得统一「成功率」怎么算——这属于评测口径问题，留待讲评测时再展开。

还要补一句纪律：本章只写**已经回源核对过**的数字。论文里那些必须读到全文曲线才能拿到的细节——比如某一类攻击在某个具体模型上的精确成功率、需要几轮才能得手——本手册一律不写。**拿不到的数字就不猜**，这比写一个看起来很像样的数字更重要。

## 3.5 攻防不对称原理（只做交叉引用）

七类机制为什么都值得警惕？根本原因不在某一类特别神，而在于第 2 章 2.6 讲过的那条**攻防不对称**：攻击者只需一次成功，防御方却必须防住所有可能。本节不重复那里的整句引文，只留一个逻辑指向——**本章的七类，正是「所有可能」这个词的具体内容**。

换句话说，防御方要对付的不是七个彼此孤立的技巧，而是一个**会不断增生、还能自动化**的攻击面：今天你堵住七类，明天可能有第八类从同一个根因里长出来；而 3.3.7 那种「让模型自己找招」的做法，还会让新招式的出现速度超过人工应对的速度。

## 3.6 分类学与「七类」来源说明

最后交代一句「七类」的来路，避免你把它当成某个权威分类的原样搬运。

已有综述确实提到过「七类」，例如 JailbreakZoo：“Our study categorizes jailbreaks into seven distinct types and elaborates on defense strategies that address these vulnerabilities.”（中译：我们的研究把破甲归为七种不同类型，并详述了针对这些脆弱性的防御策略。）出处 sources/U29_jailbreakzoo.md:10。但要注意：这份材料只说了「七种类型」，**并没有**留下这七类的**具体名称**（见研究记录的缺口说明）。所以本手册的七类，是按 3.3 的机制**自行归纳**的，**不冒充** JailbreakZoo 的原始分类——两者数量上都是「七」，只是巧合，不代表分类内容相同。

如果你在别处看到另一套破甲分类，不必纠结谁「对」——分类是工具，不是标准答案。有用的分类能让你把新出现的攻击一眼放进已知框架里；至于它切成六类、七类还是八类，只要切法自洽、能帮你判断「这一招从哪层下手」，就够用了。

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 21 | “However, simply including a very large number of faux dialogues preceding the final question—in our research, we tested up to 256—produces a very different response.” | 只要在最终问题前放入极大量的虚构对话，就会得到截然不同的回答——在我们的研究中测试了多达 256 段。 | sources/U7_many-shot.md:29 |
| 22 | 「The effectiveness of many-shot jailbreaking increases as we increase the number of “shots” (dialogues in the prompt) according to a scaling trend known as a power law」 | 多示例破甲的有效性随「示例」数量按幂律增长。 | sources/U7_many-shot.md:39 |
| 24 | “In a roleplay attack we exploit the helpfulness of the model by asking it to roleplay as a malevolent character.” | 在角色扮演攻击中，我们利用模型的「乐于助人」倾向，让它扮演一个反派角色。 | sources/U8_red-teaming-harms.md:138 |
| 25 | “our approach automatically produces these adversarial suffixes by a combination of greedy and gradient-based search techniques” | 我们的方法通过贪心搜索与梯度搜索的组合，自动生成这些对抗后缀。 | sources/U10_gcg.md:10 |
| 26 | “the resulting attack suffix is able to induce objectionable content in the public interfaces to ChatGPT, Bard, and Claude, as well as open source LLMs such as LLaMA-2-Chat, Pythia, Falcon, and others” | 该后缀能在 ChatGPT、Bard、Claude 的公开接口及 LLaMA-2-Chat、Pythia、Falcon 等开源 LLM 上诱出不良内容。 | sources/U10_gcg.md:10 |
| 27 | “we conduct a comprehensive analysis of 1,405 jailbreak prompts spanning from December 2022 to December 2023.” | 我们对 2022 年 12 月至 2023 年 12 月间的 1,405 条破甲提示做了全面分析。 | sources/U11_do-anything-now.md:10 |
| 28 | “we propose a persuasion taxonomy derived from decades of social science research.” | 我们提出一套源自数十年社会科学研究的说服分类法。 | sources/U22_persuasion.md:10 |
| 29 | “Empirically, PAIR often requires fewer than twenty queries to produce a jailbreak, which is orders of magnitude more efficient than existing algorithms.” | 实测中，PAIR 常能在少于二十次查询内产出一次破甲，比既有算法高效了数个数量级。 | sources/U26_pair.md:10 |
| 30 | “Crescendo is a simple multi-turn jailbreak that interacts with the model in a seemingly benign manner.” | Crescendo 是一种简单的多轮破甲，它以看似无害的方式与模型交互。 | sources/U27_crescendo.md:10 |
| 31 | “we discover that chat in cipher can bypass the safety alignment techniques of LLMs, which are mainly conducted in natural languages.” | 我们发现，用密码交谈可以绕过 LLM 的安全对齐——而这类对齐主要是在自然语言上进行的。 | sources/U28_cipher.md:10 |
| 32 | “we generate test inputs using an LM itself, and we use a classifier to detect harmful behavior on test inputs” | 我们用一个语言模型自身来生成测试输入，并用分类器检测测试输入上的有害行为。 | sources/U9_red-teaming-lms.md:18 |
| 34 | “Our study categorizes jailbreaks into seven distinct types and elaborates on defense strategies that address these vulnerabilities.” | 我们的研究把破甲归为七种不同类型，并详述了针对这些脆弱性的防御策略。 | sources/U29_jailbreakzoo.md:10 |
