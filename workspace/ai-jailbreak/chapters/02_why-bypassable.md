# 第 2 章：为什么能破——对齐的固有局限

## 2.1 一句话看懂：对齐不是给模型「上锁」，而是在输出分布上「轻推一把」

这一章回答第二个问题：**为什么对齐挡不住破甲**。一句话看懂，对齐不是给模型上了一把锁，而是在它「下一句要说什么」的概率分布上**轻轻推一把**，让它更倾向于选安全的那一支。既然只是「推」，那就不是「锁」：推力一弱、方向一变，模型就可能走回老路。

接 1.2 那道闸机继续讲：护栏之所以能落杆，靠的正是对齐训练留下的这层「偏好」，而不是一道物理锁。所以问题从来不是「锁有没有被撬开」，而是「这一推，推得够不够狠、够不够稳」。本章就把「推不稳」的几层原因一层层拆开。

## 2.2 两大失效模式（U1:10）

研究者把安全训练的失效归结为两种模式——这是理解后面一切破甲的**总纲**。

**表 2-1　两大失效模式对照**

| 失效模式 | 定义 | 触发条件 | 后果 |
| --- | --- | --- | --- |
| 竞争目标（competing objectives） | 模型的能力目标与安全目标互相冲突 | 某项能力越强、模型越「想」完成任务 | 能力压过安全，拒绝被绕过 |
| 泛化不匹配（mismatched generalization） | 安全训练没能泛化到模型已经具备能力的领域 | 进入训练分布之外的领域（陌生的语言、编码、形态） | 安全「没覆盖到」，形同虚设 |

两种模式的原话是“We hypothesize two failure modes of safety training: competing objectives and mismatched generalization.”（中译：我们假设安全训练存在两种失效模式——竞争目标与泛化不匹配。）出处 sources/U1_wei-jailbroken.md:10。它们的定义紧接着给出：“Competing objectives arise when a model's capabilities and safety goals conflict, while mismatched generalization occurs when safety training fails to generalize to a domain for which capabilities exist.”（中译：「竞争目标」出现在模型能力目标与安全目标冲突时；「泛化不匹配」出现在安全训练未能泛化到模型已具备能力的领域时。）出处 sources/U1_wei-jailbroken.md:10。

由此引出一个关键概念——**安全-能力对等**（safety-capability parity）：“Our analysis emphasizes the need for safety-capability parity -- that safety mechanisms should be as sophisticated as the underlying model -- and argues against the idea that scaling alone can resolve these safety failure modes.”（中译：强调需要安全-能力对等，即安全机制应当和能力本身一样精细，并反驳「单纯扩大规模即可解决」的观点。）出处 sources/U1_wei-jailbroken.md:10。所以不要指望「模型再大一点自然就安全了」：安全机制必须与能力同等精细，否则缺口会随能力一起放大。

## 2.3 对齐「浅」且「低维」

上面是「为什么会失效」的框架，这一节给两条实验证据：对齐本身既**低维**，又**浅**。

先说「低维」。研究者发现拒绝行为几乎只由一个方向控制“we show that refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models up to 72B parameters in size.”（中译：在 13 个主流开源对话模型（至 72B 参数）上，拒绝行为由一个一维子空间中介。）出处 sources/U17_refusal-direction.md:16。**一个方向**——顺着它抹掉，模型就不再拒绝；反向加上去，连无害问题也会被拒。作者由此下结论：“Our findings underscore the brittleness of current safety fine-tuning methods.”（中译：我们的发现凸显了当前安全微调方法的脆弱性。）出处 sources/U17_refusal-direction.md:16。

> [!tip] 进阶
> 「一维子空间」是白盒分析的术语：把模型内部激活看成一个高维空间，拒绝与否几乎只由其中**一个方向**决定。看不懂这个术语没关系，抓住结论即可——安全行为能被单个方向左右，说明它并不稳固。

再说「浅」。第二条证据是**浅层安全对齐**（shallow safety alignment）：“the alignment adapts a model's generative distribution primarily over only its very first few output tokens. We refer to this issue as shallow safety alignment.”（中译：对齐主要只作用于最前面几个输出 token；这一现象被称为浅层安全对齐。）出处 sources/U19_few-tokens-deep.md:16。翻译成大白话：护栏只在回答的「开头几个字」上用力，一旦模型说出前几个字，后面就基本没管了——所以只要把它「带过头」，后面就失守。

## 2.4 低成本即可破坏

浅和低维之外，还有一条更扎心的性质：破坏对齐**很便宜**。研究者只用了 10 条样本，就破掉了 GPT-3.5 Turbo 的安全护栏“we jailbreak GPT-3.5 Turbo's safety guardrails by fine-tuning it on only 10 such examples at a cost of less than $0.20 via OpenAI's APIs, making the model responsive to nearly any harmful instructions.”（中译：仅用 10 条样本、花费不足 0.20 美元微调，即破掉 GPT-3.5 Turbo 的安全护栏，使模型几乎对任何有害指令都有求必应。）出处 sources/U15_finetuning-safety.md:10。**10 条、不到两毛钱**——这就是「推一把」的成本量级，门槛低到个人就能完成。

更麻烦的是，即使毫无恶意也会中招：“even without malicious intent, simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent.”（中译：即便毫无恶意，仅用常见良性数据集微调，也会在较小程度上无意退化安全对齐。）出处 sources/U15_finetuning-safety.md:10。也就是说，日常的业务微调，也可能顺手把安全对齐磨薄一层。

## 2.5 能力-安全权衡（安全税 safety tax）

第四层原因是「跷跷板」：安全与能力常常此消彼长，研究者把这份代价命名为**安全税**（safety tax）。“Safety alignment leads to a degradation of the reasoning capability of LRMs.”（中译：安全对齐会导致大推理模型（LRM）推理能力下降。）出处 sources/U24_safety-tax.md:10；同一处还有“there exists a trade-off between reasoning and safety capability”（中译：推理能力与安全能力之间存在权衡。）出处 sources/U24_safety-tax.md:10。

这带来一个两难：想更安全，就得多付能力上的代价；不想付代价，安全就留着缺口。理解了这块跷跷板，你就能预判后面防御篇里会出现的怪现象——**防得太狠，会把无害请求也一起拒掉**；那不是实现 bug，而是安全税被推到了另一头。

把 2.3 到 2.5 的证据按「层」摊开，就是下面四层。它们不是四个彼此不相干的毛病，而是同一次「轻推」从不同角度露出的不稳——一层比一层更说明问题，所以叫「递进」。

**表 2-2　对齐脆弱的四层（从现象到代价）**

| 层 | 这一层在说什么 | 一句话证据 | 后果 | 出处 |
| --- | --- | --- | --- | --- |
| 低维 | 安全行为能被**单个方向**左右 | 拒绝由一维子空间中介（13 个开源模型至 72B） | 沿该方向抹掉，模型就不再拒绝；反向加回去，连无害问题也拒 | sources/U17_refusal-direction.md:16 |
| 浅 | 只在回答「最前面几个字」上用力 | 对齐主要作用于最初几个 output token | 把模型「带过头」，后面就没人管 | sources/U19_few-tokens-deep.md:16 |
| 廉价可破 | 破坏对齐的门槛极低 | 10 条样本、不足 $0.20 微调即破 GPT-3.5 Turbo | 个人就能做到；良性微调也可能无意磨薄护栏 | sources/U15_finetuning-safety.md:10 |
| 能力-安全权衡（安全税） | 安全与能力此消彼长 | 安全对齐会拉低推理能力，两者存在权衡 | 想更安全就得付能力代价；防得太狠会误伤无害请求 | sources/U24_safety-tax.md:10 |

## 2.6 攻防不对称：为什么这件事「值得了解」

前面讲的都是「为什么能破」的技术原因；这一节回答一个更实际的问题——**知道了这些又怎样**。

红队研究里有一句话点破了整件事的性质：“Adversaries only need one attack to succeed, while red teams must be defend against all possible attacks.”（中译：攻击者只需一次成功，而红队必须防住所有可能的攻击。）（原句里的 be defend 为原文笔误，此处照录。）出处 sources/U9_red-teaming-lms.md:230。请体会这种**不对称**：攻击方只要蒙中一条路就算数，防御方却要堵住所有的路。

这句话正是全篇第二句速记的出处——**攻击者只需一次成功，防御方必须防住所有可能**。它解释了「破甲」为什么值得了解：不是因为它有多难，而是因为它**结构上就不对称**，所以防御永远不可能靠单点做到万无一失。后面讲攻防时，请一直把这句话带在身边。

## 2.7 历史基线与内部张力

> [!tip] 新手可跳过
> 这一节是研究元信息，只想要结论的读者可以直接跳到下一部分。

读上面的证据要留两个心眼。

第一，**时代**。本节引用的 U8、U9 都是 **2022 年**的研究，早于现代 RLHF 训练管线。它们对**当前前沿模型**只应作**历史基线**看待——那批模型的行为不代表今天最新的模型，但「对齐为什么会漏」的机理是一脉相承的。

第二，**U8 自己内部并不一致，必须并列陈述，不可只取一面**。一方面，RS（rejection sampling）模型被描述为「在任何规模下都最难攻破」，但同一处又说它「是靠回避才显得无害」——难攻破不等于真的更安全（sources/U8_red-teaming-harms.md:16）。另一方面，在对话式红队下，HHH 提示的模型与普通 prompting 的模型**没有显著差别**，这与该团队此前用静态评测得出的「HHH 提示是有效安全干预」结论相冲突（sources/U8_red-teaming-harms.md:122）。把任何一面单独拎出来，都会把结论说过头。

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 11 | “We hypothesize two failure modes of safety training: competing objectives and mismatched generalization.” | 我们假设安全训练存在两种失效模式——竞争目标与泛化不匹配。 | sources/U1_wei-jailbroken.md:10 |
| 12 | “Competing objectives arise when a model's capabilities and safety goals conflict, while mismatched generalization occurs when safety training fails to generalize to a domain for which capabilities exist.” | 「竞争目标」出现在模型能力目标与安全目标冲突时；「泛化不匹配」出现在安全训练未能泛化到模型已具备能力的领域时。 | sources/U1_wei-jailbroken.md:10 |
| 13 | “Our analysis emphasizes the need for safety-capability parity -- that safety mechanisms should be as sophisticated as the underlying model -- and argues against the idea that scaling alone can resolve these safety failure modes.” | 强调需要安全-能力对等——安全机制应当和能力本身一样精细——并反驳「单纯扩大规模即可解决」的观点。 | sources/U1_wei-jailbroken.md:10 |
| 14 | “we show that refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models up to 72B parameters in size.” | 我们证明：在 13 个主流开源对话模型（至 72B 参数）上，拒绝行为由一个一维子空间中介。 | sources/U17_refusal-direction.md:16 |
| 15 | “Our findings underscore the brittleness of current safety fine-tuning methods.” | 我们的发现凸显了当前安全微调方法的脆弱性。 | sources/U17_refusal-direction.md:16 |
| 16 | “the alignment adapts a model's generative distribution primarily over only its very first few output tokens. We refer to this issue as shallow safety alignment.” | 对齐主要只作用于最前面几个输出 token；这一现象被称为浅层安全对齐。 | sources/U19_few-tokens-deep.md:16 |
| 17 | “we jailbreak GPT-3.5 Turbo's safety guardrails by fine-tuning it on only 10 such examples at a cost of less than $0.20 via OpenAI's APIs, making the model responsive to nearly any harmful instructions.” | 仅用 10 条样本、花费不足 0.20 美元微调，即破掉 GPT-3.5 Turbo 的安全护栏，使模型几乎对任何有害指令都有求必应。 | sources/U15_finetuning-safety.md:10 |
| 18 | “even without malicious intent, simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent.” | 即便毫无恶意，仅用常见良性数据集微调，也会在较小程度上无意退化安全对齐。 | sources/U15_finetuning-safety.md:10 |
| 19 | “Safety alignment leads to a degradation of the reasoning capability of LRMs.” | 安全对齐会导致大推理模型（LRM）推理能力下降。 | sources/U24_safety-tax.md:10 |
| 20 | “there exists a trade-off between reasoning and safety capability” | 推理能力与安全能力之间存在权衡。 | sources/U24_safety-tax.md:10 |
| 33 | “Adversaries only need one attack to succeed, while red teams must be defend against all possible attacks.” | 攻击者只需一次成功，而红队必须防住所有可能的攻击。 | sources/U9_red-teaming-lms.md:230 |
