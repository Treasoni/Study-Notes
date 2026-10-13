这份笔记围绕「AI 破甲（jailbreak，也译「越狱」）」依次回答几件事：它是什么、为什么能成、在机制层是怎么做到的、以及我们能怎么办。全篇按「概念 → 机制 → 防御」三段展开，阅读顺序也照此推进：先用定义与判据把「破甲」是什么、和哪些近邻容易混说清，再讲为什么对齐拦不住它，然后在机制层看攻击分成哪几类、各凭什么起作用，接着转到防御方看检测、护栏、评测与治理，最后把散在各章的术语与出处收成便于回查的速查表。前两章是理解一切的基础，第 3 章只讲机制、不含任何可照做的载荷，第 4、5 章偏应用与回查——时间有限时，可顺着「是什么 → 为什么 → 怎么防」直读，把第 3 章的机制细节留作参考。每章末尾都附有该章的英文引文对照表（原文 / 中译 / 出处），术语首次出现处就地解释，方便随时回源核对。

**目录**

1. 第 1 章：什么叫 AI 破甲——定义、边界与三个近邻。先给「破甲」下定义，并把它和提示注入、红队、对齐三个近邻切开。
2. 第 2 章：为什么能破——对齐的固有局限。解释对齐为什么挡不住破甲——它只是「轻推一把」，不是「上锁」。
3. 第 3 章：如何破甲——攻击分类与原理（机制层，不含载荷）。从机制层把破甲归成几类，只讲「凭什么能钻空子」，不含载荷。
4. 第 4 章：所以怎么办——检测、防御、评测与治理。讲防御——检测、训练期与运行期护栏、评测口径与治理。
5. 第 5 章：术语与速查——把全篇收成几张表。全篇术语、判据、数字与出处的回查页，不引入新概念。

# 第 1 章：什么叫 AI 破甲——定义、边界与三个近邻

## 1.1 一句话看懂：破甲 = 让模型「说」出它本不该说的

这一章只回答一个问题：**什么叫 AI 破甲**。一句话看懂，破甲（jailbreak，也译「越狱」）就是想办法让一个被训练成「危险内容不开口」的模型，把那些它本该拒绝的话**说出来**。要理解它，还得把它和三个容易混淆的近邻切开：提示注入（prompt injection）、红队（red teaming），以及「对齐」（alignment）。

先把全篇要反复用到的第一句速记记下来：**注入让模型「做」它不该做的；破甲让模型「说」它不该说的。** 本章后面所有的定义与判据，都是在给这句话划边界。

## 1.2 比喻先于术语：把模型想成一道有「安全护栏」的出口闸机

想象一栋大楼的出口闸机。厂家在出厂时给每道闸机都装了一道**安全护栏**（guardrail）：一旦检测到某个「不该拿出去的东西」，闸杆就自动落下挡住它——这个落杆动作，就是模型安全里说的**拒绝**（refusal）。你走到闸机前说一句敏感请求，闸杆落下，模型回答「抱歉，我不能帮你做这个」。

技术上，护栏其实是「对齐」（alignment）训练留在模型里的一层输出偏好：模型仍然「知道」那些内容，只是被训练成优先输出拒绝。请特别注意这一点——护栏**不是一把锁**，它更像出口处的一道检查，拦的是「往外出」的通道，而不是把知识从模型里删掉。

所以，破甲就是**硬要把闸杆掰开**：攻击者不改动闸机本身，而是找一个护栏没覆盖到的角度，让模型把本该被拦下的内容放出去。这正好对应 1.1 的速记——破甲要的是模型「说」出不该说的。

## 1.3 三条权威定义并列（不可混引）

「破甲」没有一个全球统一的一句话定义。下面三个来源措辞各异，**必须分开引用、不能揉成一句**；第四条（Willison）只作对照，用来看清分歧在哪。

**表 1-1　三源定义对照（附 Willison 对照口径）**

| 来源 | 英文原文 | 说人话 | 归类口径 |
| --- | --- | --- | --- |
| NIST AI 100-2e2025（**主口径**，sources/U4_nist-ai100-2e2025.md:5791） | “A DIRECT PROMPTING ATTACK intended to circumvent restrictions placed on model outputs, such as circumventing refusal behaviour to enable misuse.” | 一种**直接提示攻击**，意在绕过施加于模型输出上的限制，例如绕过拒绝行为以促成滥用。 | 把 jailbreak 定为一种 direct prompting attack |
| NIST AI 600-1（sources/U33_nist-ai-600-1.md:369-370） | 「Crafting such prompts deliberately is known as “jailbreaking,” or, manipulating prompts to circumvent output controls.」 | 蓄意构造这类提示就叫「越狱」，也就是操纵提示以绕过输出控制。 | 直接命名为 jailbreaking，与提示注入并列出现 |
| OWASP LLM01:2025（sources/U5_owasp-llm01.md:11） | “Jailbreaking is a form of prompt injection where the attacker provides inputs that cause the model to disregard its safety protocols entirely.” | 越狱是提示注入的一种形式：攻击者提供的输入让模型彻底无视它的安全协议。 | 归为 prompt injection 的一种形式（包含关系） |
| Willison（**对照口径**，sources/U16_willison.md:16） | “Jailbreaking is the class of attacks that attempt to subvert safety filters built into the LLMs themselves.” | 越狱是一类攻击，目标是颠覆**内建于 LLM 自身**的安全过滤器。 | 与 prompt injection 不同类（判据=有无拼接，见 1.4） |

前三行（NIST、NIST AI 600-1、OWASP）是本章的**权威定义**，Willison 那条放进只作对照。**本手册的主口径取 NIST AI 100-2e2025 术语表那句**（sources/U4_nist-ai100-2e2025.md:5791），也就是表 1-1 的第一行。

这里要给你埋一颗「读书种子」：NIST 这份文件里同一句话出现在两处，拼写并不一致。术语表（:5791）写的是 `behaviour`；正文（:2524-2525）写的是 `behavior`，而且正文那处还带着 PDF 提取留下的断词 `circum-venting`。**本章引的是术语表 :5791，所以照抄 `behaviour`**——你以后引用时要说清自己取的是哪一处，别把两处当成同一个字符串。

顺带交代「国际口径」：本手册能落盘的权威来源是 NIST（sources/U4、sources/U33）与 OWASP（sources/U5），它们已经覆盖「国家标准机构 + 国际社区项目」两类；正文不引用语料里缺失的其它报告。

## 1.4 三条判据：破甲与「提示注入」怎么分

破甲和提示注入经常被当成同义词，但两条权威判据能把它们分开。

**表 1-2　破甲 vs 提示注入判据表**

| 判据维度 | 破甲（jailbreak） | 提示注入（prompt injection） | 出处 |
| --- | --- | --- | --- |
| 攻击对象 | 模型**自身**内建的安全过滤器 | 构建在 LLM 之上的**应用** | sources/U16_willison.md:16 / :15 |
| 是否含可信-不受信拼接 | 不作为定义要件 | 定义上要求「可信字符串 + 不受信字符串」拼接 | sources/U16_willison.md:17 |
| 判据句出处 | sources/U16_willison.md:16 | sources/U16_willison.md:15、:17 | — |

判据一是「攻击对象」。Willison 说提示注入针对的是**应用**——“Prompt injection is a class of attacks against applications built on top of Large Language Models (LLMs) that work by concatenating untrusted user input with a trusted prompt constructed by the application’s developer.”（中译：提示注入针对构建在 LLM 之上的应用，手法是把不受信的用户输入与开发者构造的可信提示拼接在一起。）出处 sources/U16_willison.md:15。而 jailbreak 针对的是模型本身——“Jailbreaking is the class of attacks that attempt to subvert safety filters built into the LLMs themselves.”（中译：越狱是一类试图颠覆内建于 LLM 自身的安全过滤器的攻击。）出处 sources/U16_willison.md:16。

判据二是「拼接」：“if there’s no concatenation of trusted and untrusted strings, it’s _not prompt injection_.”（中译：若没有「可信字符串与不受信字符串的拼接」，那就不是提示注入。）出处 sources/U16_willison.md:17。这是最好用的一把尺子：**看有没有「把外部输入和开发者提示拼在一起」这个动作**——有，才叫提示注入。

还有第三种情形叫**间接提示注入**——“We reveal new attack vectors, using Indirect Prompt Injection, that enable adversaries to remotely (without a direct interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved.”（中译：攻击者无需直接接口，只要把提示策略性地注入到很可能被检索到的数据里，即可远程利用集成 LLM 的应用。）出处 sources/U2_indirect-injection.md:16。要点是攻击者**不直接和模型对话**，而是把恶意指令藏进模型之后会去「检索」的资料里（另见 sources/U5_owasp-llm01.md:16；直接/间接的划分见 sources/U33_nist-ai-600-1.md:551-556）。

> [!tip] 不熟悉数据库可略读
> 破甲与提示注入背后有一个共同根因，NIST 借一个老漏洞来类比：“underlying many of the security vulnerabilities in LLM applications is the fact that data and instructions are not provided in separate channels to the LLM, which allows attackers to use data channels to inject malicious instructions in inference-time attacks (a similar flaw to that which underlies decades-old SQL injection attacks).”（中译：许多 LLM 应用安全漏洞的根源在于数据与指令并非经由**分离的通道**提供，使攻击者能借数据通道注入恶意指令——这与存在了数十年的 SQL 注入是同一类缺陷。）出处 sources/U4_nist-ai100-2e2025.md:2268-2271。

另一条共同根因是「指令没有强制优先级」（出处 sources/U3_instruction-hierarchy.md:16）：“one of the primary vulnerabilities underlying these attacks is that LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties.”（中译：这些攻击之所以成立的主要漏洞之一，是 LLM 常把系统提示与来自不受信用户及第三方的文本视为**同等优先级**。）换句话说，系统提示本该「嗓门更大」，实际上却和用户输入一个音量——这正是 1.2 那道闸机容易被绕开的深层原因。

## 1.5 破甲 ≠ 红队：红队是防御方的方法论

第三个容易混的近邻是**红队**（red teaming）。红队不是「破甲的一种」，它是**防御方拿来修模型的方法**。

“One potentially useful tool for addressing harm is red teaming—using manual or automated methods to adversarially probe a language model for harmful outputs, and then updating the model to avoid such outputs”（中译：应对危害的一个可能有用工具是**红队**——用人工或自动化方法对抗性地探测语言模型的有害输出，再据此更新模型。）出处 sources/U8_red-teaming-harms.md:15。

读这句话要抓住结尾的 `and then updating the model`：红队的产出不是「一个能用的破甲」，而是**一份让模型变好的修改清单**。所以破甲是攻击者的动作，红队是防御者的动作；两者的技术手法可能重叠，但**目的相反**。一句话：红队是拿来修模型的，不是拿来破的。

## 1.6 归类关系三源不一致：学界未统一

> [!tip] 新手可跳过
> 这是研究元信息，只想要结论的读者可以直接跳到 1.7。

把 1.3 的四个定义横着看，会发现三家对「破甲和提示注入是什么关系」并不一致：

- OWASP（sources/U5_owasp-llm01.md:11）说 jailbreaking **is a form of** prompt injection——包含关系。
- Willison（sources/U16_willison.md:15-17）以「有无可信/不受信拼接」为判据，认为两者**不同类**。
- NIST（sources/U4_nist-ai100-2e2025.md:5791）把 jailbreak 定义为一种 **direct prompting attack**；而 direct prompt injection 也被归进 direct prompting attack——于是 jailbreak 与 direct prompt injection 到底是「兄弟」还是「包含」，原文**没有判死**。

**结论：学界未统一。** 本手册的处理办法是分述三家、指出未定，**不替它们下结论式的等价**；以后看到有人把两者划等号，回到这一节核对他引的是哪一家即可。

## 1.7 名词扫盲表

**表 1-3　名词扫盲**（每条一句大白话 + 定义源行号，方便回查）

| 术语 | 一句大白话 | 定义源行号 |
| --- | --- | --- |
| jailbreak（越狱） | 想办法让模型「说」出它本该拒绝的内容 | sources/U4_nist-ai100-2e2025.md:5791；sources/U33_nist-ai-600-1.md:369-370；sources/U5_owasp-llm01.md:11；sources/U16_willison.md:16 |
| prompt injection（提示注入） | 让模型「做」它不该做的；判据是「可信提示 + 不受信输入」被拼在一起 | sources/U16_willison.md:15、:17；sources/U33_nist-ai-600-1.md:551-556 |
| indirect prompt injection（间接提示注入） | 攻击者不直接对话，把指令藏进模型会去检索的资料里 | sources/U2_indirect-injection.md:16；sources/U5_owasp-llm01.md:16 |
| red teaming（红队） | 防御方对抗性地试探模型，找出问题再回去修 | sources/U8_red-teaming-harms.md:15 |
| alignment（对齐） | 训练时给模型装的「输出偏好」，让它优先选择安全回答 | sources/U1_wei-jailbroken.md:10；sources/U14_constitutional-ai.md:10 |
| guardrail（护栏） | 挡在输入/输出通道上的检查，不合格就落杆 | sources/U16_willison.md:16；sources/U5_owasp-llm01.md:11 |
| refusal（拒绝） | 模型遇到敏感请求时「不照做」的那句回复 | sources/U17_refusal-direction.md:16 |

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “A DIRECT PROMPTING ATTACK intended to circumvent restrictions placed on model outputs, such as circumventing refusal behaviour to enable misuse.” | 一种**直接提示攻击**，意在绕过施加于模型输出上的限制，例如绕过拒绝行为以促成滥用。 | sources/U4_nist-ai100-2e2025.md:5791 |
| 2 | 「Crafting such prompts deliberately is known as “jailbreaking,” or, manipulating prompts to circumvent output controls.」 | 蓄意构造此类提示即所谓「越狱」，也就是操纵提示以绕过输出控制。 | sources/U33_nist-ai-600-1.md:369-370 |
| 3 | “Jailbreaking is a form of prompt injection where the attacker provides inputs that cause the model to disregard its safety protocols entirely.” | 越狱是提示注入的一种形式：攻击者提供的输入使模型完全无视其安全协议。 | sources/U5_owasp-llm01.md:11 |
| 4 | “Prompt injection is a class of attacks against applications built on top of Large Language Models (LLMs) that work by concatenating untrusted user input with a trusted prompt constructed by the application’s developer.” | 提示注入针对构建在 LLM 之上的应用，手法是把不受信的用户输入与开发者构造的可信提示拼接在一起。 | sources/U16_willison.md:15 |
| 5 | “Jailbreaking is the class of attacks that attempt to subvert safety filters built into the LLMs themselves.” | 越狱是一类试图颠覆内建于 LLM 自身的安全过滤器的攻击。 | sources/U16_willison.md:16 |
| 6 | “if there’s no concatenation of trusted and untrusted strings, it’s _not prompt injection_.” | 若没有「可信字符串与不受信字符串的拼接」，那就不是提示注入。 | sources/U16_willison.md:17 |
| 7 | “one of the primary vulnerabilities underlying these attacks is that LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties.” | 这些攻击之所以成立的主要漏洞之一，是 LLM 常把系统提示与来自不受信用户及第三方的文本视为同等优先级。 | sources/U3_instruction-hierarchy.md:16 |
| 8 | “We reveal new attack vectors, using Indirect Prompt Injection, that enable adversaries to remotely (without a direct interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved.” | 攻击者无需直接接口，只要把提示策略性地注入很可能被检索到的数据中，即可远程利用集成 LLM 的应用。 | sources/U2_indirect-injection.md:16 |
| 9 | “underlying many of the security vulnerabilities in LLM applications is the fact that data and instructions are not provided in separate channels to the LLM, which allows attackers to use data channels to inject malicious instructions in inference-time attacks (a similar flaw to that which underlies decades-old SQL injection attacks).” | 许多 LLM 应用安全漏洞的根源在于数据与指令并非经由分离的通道提供，使攻击者能借数据通道注入恶意指令。 | sources/U4_nist-ai100-2e2025.md:2268-2271 |
| 10 | “One potentially useful tool for addressing harm is red teaming—using manual or automated methods to adversarially probe a language model for harmful outputs, and then updating the model to avoid such outputs” | 应对危害的一个可能有用工具是红队——用人工或自动化方法对抗性地探测语言模型的有害输出，再据此更新模型。 | sources/U8_red-teaming-harms.md:15 |

第 1 章把「破甲是什么」讲清了；顺理成章的问题是：既然模型被训练成会拒绝，为什么还能被绕过？

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

理解了「为什么能破」，接下来就在机制层看这些原理落成了哪几类攻击——本章只讲机制，不含任何可照做的配方。

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

看清了攻击的机制，问题自然转向防御方：既然没有万能锁，究竟该怎么防、怎么评、怎么管？

# 第 4 章：所以怎么办——检测、防御、评测与治理

## 4.1 一句话看懂：防御是「纵深防御」，不是单点拦截

前 3 章回答了「是什么」「为什么」「怎么破」，这一章回答第四个问题：**所以怎么办**。一句话看懂——**破甲防不住「一次都不发生」，能做的只是把「成功一次」的门槛、成本和被发现的机会都拉高；所以防御不是一道闸机，而是一串互为兜底的闸机。**

单点拦截这条路走不通，原因第 2 章已交代：护栏是在输出分布上「轻推一把」，推总有力弱、方向偏的时候。所以「把这句话加进黑名单」这种点状拦截，追不上攻击的增生速度。两大红队基准把话说得很直。HarmBench 的结论是“no current attack or defense is uniformly effective, and that robustness is independent of model size.”（中译：当前没有任何一种攻击或防御是普遍有效的，而且鲁棒性与模型规模无关。）出处 sources/U12_harmbench-full.md:15。同文另一处更短：“No model is robust to all attacks, and no attack breaks all models.”（中译：没有哪个模型能扛住所有攻击，也没有哪种攻击能攻破所有模型。）出处 sources/U12_harmbench-full.md:103。这两句是一体两面：**既没有万能攻击，也没有万能防御**——所以答案不是「找一把万能锁」，而是「排一串各挡一面的闸机」。

> [!tip] 大白话
> 把模型安全想成一栋楼的门禁。单点防御像只装一道门，保安还是「模型自己」；一句话骗过它，整栋楼就开了。纵深防御像门口、电梯、每层走廊、保险柜各有一道：哪道被绕过，后面都还有下一道。所以「破甲成功」不再等于「大楼失守」，只是「你被拦在了下一道闸机前」。

「纵深防御」这个定位出自 NIST 讲 LLM 检测系统时（注意：不是 OWASP）：“These may provide supplementary assurance through a defense-in-depth philosophy.”（中译：这类检测系统可以借「纵深防御」的理念，提供一层补充性的保障。）出处 sources/U4_nist-ai100-2e2025.md:2788。悲观的那一半底牌，主流指南也不回避——OWASP 在讲**提示注入**时说：“Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention for prompt injection.”（中译：鉴于模型的运作核心本身带着随机性，目前尚不清楚是否存在万无一失的提示注入预防方法。）出处 sources/U5_owasp-llm01.md:28。

> [!warning] 常被读错
> 上面这句说的是**提示注入**（另一类风险，别和破甲混为一谈，见第 1 章），不能直接挪到破甲头上。而且「没有 fool-proof 方法」讲的是「没有万无一失的单点预防」，**不等于**「防御没用」——NIST 与 OWASP 立场一致：单点拦不住，所以要多层互补。

## 4.2 训练期防御

第一层思路：不等模型往外吐时再拦，而是**在训练时就把「不照做」写进权重**，让防御成为模型自己的一部分。

代表一，**宪法式 AI（Constitutional AI）**：拿一份写好的原则清单当「宪法」，让模型按它批评、改写自己的回答，人工监督被压缩到「只给原则」——“The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'.”（中译：唯一的人工监督，就是提供一份规则或原则清单，因此我们把这套方法称为「宪法式 AI」。）出处 sources/U14_constitutional-ai.md:10。它其中的强化学习环节，打分的也不是人：“we use 'RL from AI Feedback' (RLAIF)”（中译：我们使用「基于 AI 反馈的强化学习」，即 RLAIF。）出处 sources/U14_constitutional-ai.md:10。

代表二，**对抗训练（adversarial training）**：让红队不停找新攻击，再拿新攻击去微调模型，代表是 R2D2——“we propose a new adversarial training method for robust refusal, called Robust Refusal Dynamic Defense (R2D2).”（中译：我们提出一种用于「稳健拒绝」的对抗训练新方法，名为 Robust Refusal Dynamic Defense（R2D2）。）出处 sources/U12_harmbench-full.md:127。关键在「动态」：它不在固定坏例集上练，而在一个由强攻击方法不断更新的样本池上持续微调。效果（口径见 4.4）：对 GCG 这类攻击，把 Llama 2 7B Chat 的成功率从 31.8% 降到 5.9%，13B Chat 从 30.2% 降到 5.9%。出处 sources/U12_harmbench-full.md:183。诚实的补充：它对「不像 GCG 的攻击」（如 PAIR、TAP）增益会变小——训练期防御同样吃「分布」这碗饭。

> [!tip] 进阶 / 可跳过
> 成本细节：R2D2 这次微调约 16 小时、跑在一台 8×A100 节点上；副作用是通用能力略降，MT-Bench 从 6.5 掉到 6.0（出处 sources/U12_harmbench-full.md:181、sources/U12_harmbench-full.md:185）。不了解不影响主线——记住一句即可：训练期防御换来「权重里的稳健拒绝」，代价是要重训、要算力，还可能牺牲一点通用能力。

## 4.3 运行期护栏（独立分类器）

第二层换了位置：**不动模型权重，另外养一个专门的「门卫模型」**，读输入、也读输出，判定该不该放行。好处是它能单独升级、单独替换，不必动主模型。

代表一，**Llama Guard**，一个独立的输入 / 输出安全模型：“This taxonomy is also instrumental in classifying the responses generated by LLMs to these prompts, a process we refer to as response classification.”（中译：这套风险分类法还适合用来给 LLM 针对这些提示所产生的**回复**分类，这一过程我们称为「回复分类」。）出处 sources/U31_llama-guard.md:10。它点明护栏有两种查法：查「提示」是 prompt classification，查「回复」是 response classification。

代表二，**Constitutional Classifiers**，护栏本身也用「宪法 + 合成数据」训出来：“safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted content”（中译：这套护栏用合成数据训练——这些数据由 LLM 依据一份用自然语言写成、规定「允许什么、限制什么」的规则（即一部「宪法」）生成。）出处 sources/U32_constitutional-classifiers.md:10。它的红队成绩很扎眼：“In over 3,000 estimated hours of red teaming, no red teamer found a universal jailbreak”（中译：在累计约 3,000 小时的对抗性红队测试中，没有任何一名红队成员找到过一个通用破甲。）出处 sources/U32_constitutional-classifiers.md:10。效果（口径见 4.4）有两组：“our classifier-guarded system refuses over 95% of held-out jailbreaking attempts, compared to only 14% without classifiers”（中译：在我们这套带分类器护栏的系统上，对留出的越狱尝试拒绝率超过 95%，而没有分类器时只有 14%。）出处 sources/U32_constitutional-classifiers-full.md:16；“reducing the jailbreak success rate from 86% against a HHH model to less than 5%”（中译：把越狱成功率从（对付 HHH 模型时的）86% 压到不足 5%。）出处 sources/U32_constitutional-classifiers-full.md:98。但护栏不是白加的：“with an absolute 0.38% increase in production-traffic refusals and a 23.7% inference overhead”（中译：生产流量上的拒绝率绝对增加 0.38%，推理开销增加 23.7%。）出处 sources/U32_constitutional-classifiers.md:10——要多花约四分之一推理开销，还会多拒掉一点无害请求（0.38%）；后者即「误伤」，也叫过度拒绝，是 4.5 要专门量的指标。

> [!tip] 大白话
> 运行期护栏像商场门口的第二道安检：主安保（模型本身）可能被骗过，于是另配一队「只干安检」的人。好处是独立、可换、可升级；坏处是每个顾客都得多排一次队（推理开销），有时还会误拦老实人（误伤）。

## 4.4 提示级缓解 + 效果数字口径

第三层更轻：不改权重、不加分类器，只在**应用层**对提示动手术——先分类、再改写，或补一层说明。一个实测例子来自多示例（many-shot）攻击：“One such technique substantially reduced the effectiveness of many-shot jailbreaking — in one case dropping the attack success rate from 61% to 2%.”（中译：其中一种技术大幅削弱了多示例破甲的效果——在某个案例里把攻击成功率从 61% 压到了 2%。）出处 sources/U7_many-shot.md:44。

> [!warning] 必读：这是数字口径，不是「药到病除」
> 61%→2% 是**某一种**技术、在**某一次**多示例攻击上的结果；换攻击、换技术，数字就会变。凡是防御效果数字，都要连着「在什么攻击、什么模型、什么判定下测出来的」一起读，单独拎出来最容易被误当普适结论。下表把全篇数字的口径一次列清，请连读「口径 / 前提」列。

**表 4-1　效果数字口径表（读数字必须连读「口径 / 前提」列）**

| 方法 | 报告数字 | 口径 / 前提 | 出处 |
| --- | --- | --- | --- |
| 提示级缓解（针对多示例） | 61% → 2% | 「某一种」分类加改写技术、「某一次」多示例攻击；非普适 | sources/U7_many-shot.md:44 |
| 对抗训练 R2D2（对 GCG） | 31.8 / 30.2 → 5.9 | 仅对 GCG 这一族攻击的 ASR；对不像 GCG 的攻击增益变小 | sources/U12_harmbench-full.md:183 |
| Constitutional Classifiers | 86% → <5% | 对某一组留出的越狱尝试；换一组数字会变 | sources/U32_constitutional-classifiers-full.md:98 |
| Constitutional Classifiers（有 / 无护栏） | >95% vs 14% | 同一组留出尝试下，有分类器对无分类器 | sources/U32_constitutional-classifiers-full.md:16 |
| 部署开销 | 0.38% / 23.7% | 前者是生产流量拒绝率的绝对增幅，后者是推理开销 | sources/U32_constitutional-classifiers.md:10 |

**一条纪律**：本表只收**能回到原始来源件**的数字。凡是回不到出处的数字，一律不采用——宁可少写一个，也不写一个「看起来很合理」的数；数字的可信度不来自它像不像，而来自它能不能指出在哪一行。

## 4.5 评测：ASR 定义与基准

要谈「防住了多少」，先定义「怎么算破甲成功」。最常用的量是 **ASR（Attack Success Rate，攻击成功率）**：“The primary measure of a red teaming method’s success is its attack success rate (ASR) on a given target model, which is the percentage of test cases that elicit the behavior from the target model.”（中译：衡量一种红队方法是否成功，首要指标是它在某个目标模型上的攻击成功率（ASR），即「让目标模型做出该行为的测试用例占比」。）出处 sources/U12_harmbench-full.md:51。

注意 ASR 定义里藏着一个**判官（judge）**——什么算「诱发该行为」。判官怎么定，直接决定数字高低，这正是跨基准数字不能直接用的原因：“existing works compute costs and success rates in incomparable ways”（中译：既有工作在计算成本与成功率时，用的方式彼此不可比。）出处 sources/U30_jailbreakbench.md:10。所以关键判据是：**不同基准的 ASR 口径与判官不同，跨基准的数字不能直接并排比较。** 同一句「ASR 90%」在不同基准里可能根本不是一回事——读「某某防住了 99%」时，先问三件事：哪个基准、哪个判官、哪一组测试用例。

另有几个基准专门盯**误伤**，是对 ASR 的补充。OR-Bench 是「过度拒绝」专场：“OR-Bench, the first large-scale over-refusal benchmark”（中译：OR-Bench，首个大规模的「过度拒绝」基准。）出处 sources/U20_or-bench.md:10；它要量的是安全增强的副作用：“the enhanced safety often come with the side effect of over-refusal, where LLMs may reject innocuous prompts and become less helpful”（中译：安全性增强往往伴随「过度拒绝」这一副作用——LLM 可能连无害的提示也拒答，从而变得不那么有用。）出处 sources/U20_or-bench.md:10。XSTest 则测「标定」：“XSTest comprises 250 safe prompts across ten prompt types that well-calibrated models should not refuse to comply with, and 200 unsafe prompts as contrasts that models, for most applications, should refuse.”（中译：XSTest 包含 10 种类型的 250 条安全提示，标定良好的模型不应拒绝它们；另配 200 条不安全提示作为对照，模型在多数应用场景下应当拒绝。）出处 sources/U21_xstest.md:10。

**表 4-2　评测基准对照表**

| 基准 | 规模 | 它量的是什么（ASR 口径相关） | 局限 | 出处 |
| --- | --- | --- | --- | --- |
| HarmBench | 510 个有害行为（400 文本 + 110 多模态）、18 种攻击方法、33 个模型 | 标准化 ASR：用统一判官判「是否诱出该行为」 | 判官口径固定，未必适配其他场景；只反映榜上攻击与模型的组合 | sources/U12_harmbench-full.md:80、:15 |
| JailbreakBench | 100 个行为 + 不断演进的攻击样本库 | 强调威胁模型、系统提示、打分函数都标准化 | 明确指出既有工作口径不可比，它自己也不是唯一标准 | sources/U30_jailbreakbench.md:10 |
| OR-Bench | 约 80,000 条过度拒绝提示（含约 1,000 条硬例 + 600 条有毒对照） | 量的是**过度拒绝**（误伤），不是越狱成功率 | 测的是「安全过头」，与 ASR 是相反方向的指标 | sources/U20_or-bench.md:10 |
| XSTest | 250 条安全提示 + 200 条不安全对照 | 量的是**标定**：该拒的拒、该答的答 | 规模小，用于诊断过度拒绝，不用于刷 ASR 排行榜 | sources/U21_xstest.md:10 |

> [!tip] 进阶 / 可跳过
> 各基准的完整构成、攻击库与打分细节属进阶内容，不看也能读懂「有几种基准、各自盯什么」。要回查时，逐字口径都在上表与各条出处行里。

## 4.6 治理框架

前三层都是技术动作，还有一层是**治理**：把破甲当成一类系统性风险来管，而不是只防某一次攻击。

先看一个容易忽略的事实：NIST 的生成式 AI 风险清单（AI 600-1）**并没有给「越狱」单列一节**，只在两处顺带点到——危害内容一节（2.3）与信息安全一节（2.9）。出处 sources/U33_nist-ai-600-1.md:346、sources/U33_nist-ai-600-1.md:524。这个「没有独立条目」本身说明：破甲不是孤立风险，而是**寄生在其他风险上的一个放大手法**。

治理视角下有两条提醒，都指向「别把话说满」。其一，生成式 AI 会**扩大攻击面**：“it expands the available attack surface, as GAI itself is vulnerable to attacks like prompt injection or data poisoning.”（中译：它扩大了可被攻击的面，因为生成式 AI 自身就容易受到提示注入或数据投毒等攻击。）出处 sources/U33_nist-ai-600-1.md:529-531。其二，**测试本身也有盲区**：“Similarly, jailbreaking or prompt engineering tests may not systematically assess validity or reliability risks.”（中译：同理，越狱或提示工程类测试未必能系统性地评估有效性或可靠性风险。）出处 sources/U33_nist-ai-600-1.md:2649-2651。所以治理的意义，是把「防住某一次攻击」升级成「用一套流程持续去测」；但同一份清单也承认，这套测试未必覆盖全部风险——**「测过了」不等于「没问题」**。

> [!tip] 大白话
> 治理框架像小区消防规定：不是买一个灭火器就完事，而是规定「几层楼要有几个灭火器、多久检一次、谁来检、记录留档」。技术防御是灭火器，治理就是那套「多久复查、谁负责」的规矩——少了规矩，灭火器再多也可能过期。

## 4.7 一张表收束

**表 4-3　防御三层（含治理层）：方法、代价、出处**

| 层级 | 方法（代表） | 代价 / 局限 | 出处 |
| --- | --- | --- | --- |
| 训练期 | 宪法式 AI / RLAIF、对抗训练 R2D2 | 要重训、要持续的红队样本、可能牺牲一点通用能力 | sources/U14_constitutional-ai.md:10、sources/U12_harmbench-full.md:127 |
| 运行期 | 独立分类器护栏：Llama Guard、Constitutional Classifiers | 多一层推理开销（如 23.7%）、会有误伤（过度拒绝） | sources/U31_llama-guard.md:10、sources/U32_constitutional-classifiers.md:10 |
| 提示级 / 应用层 | 对提示先分类再改写、补一层说明 | 往往只在特定攻击上有效，换攻击即失效，非普适 | sources/U7_many-shot.md:44 |
| 治理 / 流程 | 风险清单（如 NIST AI 600-1）、持续评测流程 | 流程本身也有盲区，测试未必覆盖有效性 / 可靠性风险 | sources/U33_nist-ai-600-1.md:346、sources/U33_nist-ai-600-1.md:2649-2651 |

四句话收束：

- 破甲的目标不是「一次都不发生」，而是把「成功一次」的门槛、成本与可发现性拉高——**防御是一串互为兜底的闸机，不是一道门**。
- 训练期（宪法式 AI、对抗训练）把稳健拒绝写进权重，代价是重训与算力；运行期（Llama Guard、宪法分类器）另配独立模型查输入输出，代价是推理开销与误伤。
- 提示级缓解只在特定攻击上有效；治理框架把「防一次」升级成「持续测」，但也承认测试有盲区。
- 效果数字必须连口径读：不同基准的 ASR 口径与判官不同，跨基准数字不可直接并列；回不到出处的数字一律不用。

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 36 | “no current attack or defense is uniformly effective, and that robustness is independent of model size.” | 当前没有任何一种攻击或防御是普遍有效的，而且鲁棒性与模型规模无关。 | sources/U12_harmbench-full.md:15 |
| 37 | “No model is robust to all attacks, and no attack breaks all models.” | 没有哪个模型能扛住所有攻击，也没有哪种攻击能攻破所有模型。 | sources/U12_harmbench-full.md:103 |
| 52 | “These may provide supplementary assurance through a defense-in-depth philosophy.” | 这类检测系统可以借「纵深防御」的理念，提供一层补充性的保障。 | sources/U4_nist-ai100-2e2025.md:2788 |
| 53 | “Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention for prompt injection.” | 鉴于模型的运作核心本身带着随机性，目前尚不清楚是否存在万无一失的提示注入预防方法。 | sources/U5_owasp-llm01.md:28 |
| 38 | “The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'.” | 唯一的人工监督，就是提供一份规则或原则清单，因此我们把这套方法称为「宪法式 AI」。 | sources/U14_constitutional-ai.md:10 |
| 39 | “we use 'RL from AI Feedback' (RLAIF)” | 我们使用「基于 AI 反馈的强化学习」，即 RLAIF。 | sources/U14_constitutional-ai.md:10 |
| 55 | “we propose a new adversarial training method for robust refusal, called Robust Refusal Dynamic Defense (R2D2).” | 我们提出一种用于「稳健拒绝」的对抗训练新方法，名为 Robust Refusal Dynamic Defense（R2D2）。 | sources/U12_harmbench-full.md:127 |
| 40 | “This taxonomy is also instrumental in classifying the responses generated by LLMs to these prompts, a process we refer to as response classification.” | 这套风险分类法还适合用来给 LLM 针对这些提示所产生的回复分类，这一过程我们称为「回复分类」。 | sources/U31_llama-guard.md:10 |
| 41 | “safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted content” | 这套护栏用合成数据训练——这些数据由 LLM 依据一份用自然语言写成、规定「允许什么、限制什么」的规则（即一部「宪法」）生成。 | sources/U32_constitutional-classifiers.md:10 |
| 42 | “In over 3,000 estimated hours of red teaming, no red teamer found a universal jailbreak” | 在累计约 3,000 小时的对抗性红队测试中，没有任何一名红队成员找到过一个通用破甲。 | sources/U32_constitutional-classifiers.md:10 |
| 45 | “our classifier-guarded system refuses over 95% of held-out jailbreaking attempts, compared to only 14% without classifiers” | 在我们这套带分类器护栏的系统上，对留出的越狱尝试拒绝率超过 95%，而没有分类器时只有 14%。 | sources/U32_constitutional-classifiers-full.md:16 |
| 44 | “reducing the jailbreak success rate from 86% against a HHH model to less than 5%” | 把越狱成功率从（对付 HHH 模型时的）86% 压到不足 5%。 | sources/U32_constitutional-classifiers-full.md:98 |
| 43 | “with an absolute 0.38% increase in production-traffic refusals and a 23.7% inference overhead” | 生产流量上的拒绝率绝对增加 0.38%，推理开销增加 23.7%。 | sources/U32_constitutional-classifiers.md:10 |
| 23 | “One such technique substantially reduced the effectiveness of many-shot jailbreaking — in one case dropping the attack success rate from 61% to 2%.” | 其中一种技术大幅削弱了多示例破甲的效果——在某个案例里把攻击成功率从 61% 压到了 2%。 | sources/U7_many-shot.md:44 |
| 35 | “The primary measure of a red teaming method’s success is its attack success rate (ASR) on a given target model, which is the percentage of test cases that elicit the behavior from the target model.” | 衡量一种红队方法是否成功，首要指标是它在某个目标模型上的攻击成功率（ASR），即「让目标模型做出该行为的测试用例占比」。 | sources/U12_harmbench-full.md:51 |
| 49 | “existing works compute costs and success rates in incomparable ways” | 既有工作在计算成本与成功率时，用的方式彼此不可比。 | sources/U30_jailbreakbench.md:10 |
| 46 | “OR-Bench, the first large-scale over-refusal benchmark” | OR-Bench，首个大规模的「过度拒绝」基准。 | sources/U20_or-bench.md:10 |
| 47 | “the enhanced safety often come with the side effect of over-refusal, where LLMs may reject innocuous prompts and become less helpful” | 安全性增强往往伴随「过度拒绝」这一副作用——LLM 可能连无害的提示也拒答，从而变得不那么有用。 | sources/U20_or-bench.md:10 |
| 48 | “XSTest comprises 250 safe prompts across ten prompt types that well-calibrated models should not refuse to comply with, and 200 unsafe prompts as contrasts that models, for most applications, should refuse.” | XSTest 包含 10 种类型的 250 条安全提示，标定良好的模型不应拒绝它们；另配 200 条不安全提示作为对照，模型在多数应用场景下应当拒绝。 | sources/U21_xstest.md:10 |
| 50 | “it expands the available attack surface, as GAI itself is vulnerable to attacks like prompt injection or data poisoning.” | 它扩大了可被攻击的面，因为生成式 AI 自身就容易受到提示注入或数据投毒等攻击。 | sources/U33_nist-ai-600-1.md:529-531 |
| 51 | “Similarly, jailbreaking or prompt engineering tests may not systematically assess validity or reliability risks.” | 同理，越狱或提示工程类测试未必能系统性地评估有效性或可靠性风险。 | sources/U33_nist-ai-600-1.md:2649-2651 |

上面的概念、数字和出处散在各章，最后一章把它们收成几张便于回查的表。

# 第 5 章：术语与速查——把全篇收成几张表

## 5.1 一句话看懂：这是「回查页」，不是新内容

这一章**不引入任何新概念**，只把前 4 章的术语、判据、数字和出处压成几张能一眼扫到的表。一句话看懂——**这是全篇的「回查页」：当你在别处读到「ASR」「纵深防御」「宪法分类器」而不确定指什么时，回到这里查一行就知道。**

所以本章的「大字量」其实是「大表量」：正文只负责交代每张表怎么用，真正的信息都落在表里。术语的**逐字原文**不在这里重复——它们各自留在最合适的那一章（用「见第 N 章」指路），这样同一条引文只出现一次，引用链不会散。

## 5.2 术语扫盲表汇总

**表 5-1　术语扫盲（术语 / 一句大白话 / 出处）**

| 术语 | 一句大白话 | 出处 |
| --- | --- | --- |
| jailbreak（越狱 / 破甲） | 想办法让模型「说」出它本该拒绝的内容 | 见第 1 章；sources/U4_nist-ai100-2e2025.md:5791 |
| prompt injection（提示注入） | 让模型「做」它不该做的；判据是「可信提示 + 不受信输入」被拼在一起 | 见第 1 章；sources/U16_willison.md:15 |
| indirect prompt injection（间接提示注入） | 攻击者不直接对话，把指令藏进模型会去检索的资料里 | 见第 1 章、本章 5.2 末 |
| red teaming（红队） | 防御方对抗性地试探模型，找出问题再回去修 | 见第 1 章；sources/U8_red-teaming-harms.md:15 |
| alignment（对齐） | 训练时给模型装的「输出偏好」，让它优先选安全回答 | 见第 1 章；sources/U1_wei-jailbroken.md:10 |
| guardrail（护栏） | 挡在输入 / 输出通道上的检查，不合格就落杆 | 见第 1 章；sources/U16_willison.md:16 |
| refusal（拒绝） | 模型遇到敏感请求时「不照做」的那句回复 | 见第 1 章；sources/U17_refusal-direction.md:16 |
| ASR（攻击成功率） | 让目标模型做出有害行为的测试用例占比——破甲好不好使的头号指标 | 见第 4 章；sources/U12_harmbench-full.md:51 |
| over-refusal（过度拒绝 / 误伤） | 安全过了头，连无害请求也拒答 | 见第 4 章；sources/U20_or-bench.md:10 |
| defense-in-depth（纵深防御） | 不指望一道门，而是门口、电梯、保险柜各有一道，互为兜底 | 见第 4 章；sources/U4_nist-ai100-2e2025.md:2788 |
| Constitutional AI（宪法式 AI） | 给模型一份「原则清单」，让它自己按清单改自己的回答 | 见第 4 章；sources/U14_constitutional-ai.md:10 |
| RLAIF（基于 AI 反馈的强化学习） | 打分的不是人，是模型自己 | 见第 4 章；sources/U14_constitutional-ai.md:10 |
| R2D2（Robust Refusal Dynamic Defense） | 一边让红队找新攻击，一边拿新攻击微调模型，练出「稳健拒绝」 | 见第 4 章；sources/U12_harmbench-full.md:127 |
| Llama Guard | 一个独立的「门卫模型」，既查提示也查回复 | 见第 4 章；sources/U31_llama-guard.md:10 |
| Constitutional Classifiers（宪法分类器） | 用「宪法 + 合成数据」训出来的护栏模型 | 见第 4 章；sources/U32_constitutional-classifiers.md:10 |
| many-shot（多示例） | 一条提示里堆进大量「已照做」的示范，末接真问题 | 见第 3 章；sources/U7_many-shot.md:29 |
| GCG（对抗后缀） | 用搜索自动生成一段附加后缀，逼模型更可能答应 | 见第 3 章；sources/U10_gcg.md:10 |
| cipher（编码 / 密码） | 用非自然语言承载请求，绕开只在自然语言上做的对齐 | 见第 3 章；sources/U28_cipher.md:10 |
| Crescendo（多轮渐进） | 从无害问题起步，逐轮引用模型自己的回复升级 | 见第 3 章；sources/U27_crescendo.md:10 |
| PAP（说服） | 用社会科学的说服策略把请求重述一遍 | 见第 3 章；sources/U22_persuasion.md:10 |
| PAIR（自动化红队） | 用一个攻击者 LM 迭代生成、打分、改进攻击 | 见第 3 章；sources/U26_pair.md:10 |
| TEVV（测试、评估、验证与确认） | 治理里的「持续测」流程——把防一次变成长期盯着 | 见第 4 章 |

> [!note] 唯一一条留在本章的逐字定义
> 上表所有术语的逐字原文都留在各自的章节里（见 5.5），**只有「间接提示注入」这一条**，因为它的定义正好把「外部来源」这个关键点说清楚，所以放一份在这里：“Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files.”（中译：间接提示注入发生在 LLM 接受来自外部来源（如网站或文件）的输入时。）出处 sources/U5_owasp-llm01.md:16。

## 5.3 概念判据速查

光记术语不够，真正容易搞混的是「两种情况怎么分」。下表把全篇出现的几组判据收在一起。

**表 5-2　概念判据速查（问题 / 一句话判据 / 出处）**

| 要判断的事 | 一句话判据 | 出处 |
| --- | --- | --- |
| 是 jailbreak 还是 prompt injection？ | 看有没有「可信提示 + 不受信输入」被拼接——拼了才是注入；单发一条越界请求是越狱 | 见第 1 章；sources/U16_willison.md:17 |
| 是「攻击」还是「红队」？ | 同样在试探模型，防御方为找问题去试探叫红队，攻击者为滥用去试探叫攻击 | 见第 1 章；sources/U8_red-teaming-harms.md:15 |
| 这个百分比是 ASR 还是过度拒绝？ | 量「该拒的没拒」是 ASR；量「该答的却拒」是过度拒绝 | 见第 4 章 |
| 这个「防住了 X%」能横比吗？ | 看基准、判官、测试用例是不是同一套——不同就不能直接并列 | sources/U30_jailbreakbench.md:10 |
| 单点被绕过，就算失守了吗？ | 在纵深防御下，绕过一道只是到了下一道，不等于整体失守 | sources/U4_nist-ai100-2e2025.md:2788 |
| 这招从输入下手还是从输出下手？ | 攻击多从输入进（提示、多轮、编码）；护栏必须输入 / 输出两侧都查 | 见第 3 章、第 4 章 |

## 5.4 关键数字速查表（冻结口径）

下表把全篇用到的数字连同「口径」一起冻结下来。**读数字必须连读口径列**；带叠字的抓取件按真值写（叠字是 PDF 抽取的产物，不是原文）。

**表 5-3　关键数字速查（数字 / 含义 / 口径与冻结说明 / 出处）**

| 数字 | 它是什么 | 口径 / 冻结说明 | 出处 |
| --- | --- | --- | --- |
| 510 | HarmBench 整理的有害行为总数（400 文本 + 110 多模态） | 抓取件呈叠字 510510，真值 510 | sources/U12_harmbench-full.md:80 |
| 18 / 33 | HarmBench 初始评测覆盖的 18 种攻击方法 / 33 个 LLM | 抓取件呈叠字 1818 / 3333，真值 18 / 33 | sources/U12_harmbench-full.md:15 |
| 256 | many-shot 研究里测试过的「虚构对话」最大段数 | 引自原文 | sources/U7_many-shot.md:29 |
| 61% → 2% | 某一种提示级技术对多示例攻击的效果 | 单次、单技术，非普适 | sources/U7_many-shot.md:44 |
| 31.8 / 30.2 → 5.9 | R2D2 对 GCG 的成功率（Llama 2 7B / 13B Chat） | 仅对 GCG 一族 | sources/U12_harmbench-full.md:183 |
| 16 小时 / 8×A100 | R2D2 对抗训练的成本 | 抓取件呈叠字 1616，真值 16 | sources/U12_harmbench-full.md:181 |
| 6.5 → 6.0 | R2D2 带来的 MT-Bench 通用能力变化 | 抓取件呈叠字 6.56.5 / 6.06.0，真值 6.5 / 6.0 | sources/U12_harmbench-full.md:185 |
| 3,000 小时 | Constitutional Classifiers 的红队小时数 | 见第 4 章引文 42 | sources/U32_constitutional-classifiers.md:10 |
| 86% → <5% | 宪法分类器把越狱成功率压到的水平 | 对某一组留出尝试 | sources/U32_constitutional-classifiers-full.md:98 |
| >95% / 14% | 有 / 无护栏对留出越狱尝试的拒绝率 | 同一组尝试 | sources/U32_constitutional-classifiers-full.md:16 |
| 0.38% / 23.7% | 拒绝率绝对增幅 / 推理开销 | 生产流量口径 | sources/U32_constitutional-classifiers.md:10 |
| 250 + 200 | XSTest 的安全提示 / 不安全对照数 | 见第 4 章引文 48 | sources/U21_xstest.md:10 |
| 80,000 / 1,000 / 600 | OR-Bench 的过度拒绝提示 / 硬例 / 有毒对照 | 见第 4 章表 4-2 与引文 46、47 | sources/U20_or-bench.md:10 |
| 1,405 | 某研究分析的破甲提示条数（2022-12 至 2023-12） | 见第 3 章 | sources/U11_do-anything-now.md:10 |
| 少于 20 次查询 | PAIR 产出一次破甲所需的查询量级 | 见第 3 章 | sources/U26_pair.md:10 |

本表是**硬规矩**下的产物，不是笔误清单：**只要数字回不到原始来源件的那一行，就不用**。所以你在别处若见到一个讲破甲的数字，而它给不出「哪个文件、哪一行」，就当它没有出处——不是因为它大或小，而是因为它不可核。

## 5.5 归属速查

同一件事常被安到错误的出处上。下表把容易错位的几条单独拎出来。

**表 5-4　归属速查（说法 / 正确归属 / 常见误归 / 出处）**

| 说法 | 正确归属 | 常见误归 | 出处 |
| --- | --- | --- | --- |
| 「纵深防御（defense-in-depth）」这个措辞 | NIST（讲 LLM 检测系统时） | 常被误归给 OWASP | sources/U4_nist-ai100-2e2025.md:2788 |
| 「没有万无一失的预防方法」 | OWASP——且它讲的是提示注入 | 常被当成破甲的结论 | sources/U5_owasp-llm01.md:28 |
| 「越狱」的定义主源 | NIST 术语表（jailbreak 条目） | 易与提示注入定义混用 | sources/U4_nist-ai100-2e2025.md:5791 |
| 「提示注入 vs 越狱」的判据 | Simon Willison 的拆分 | 常被合并成一类 | sources/U16_willison.md:17 |
| R2D2 这个方法名 | HarmBench 论文给出的方法名 | 易被当成通用术语 | sources/U12_harmbench-full.md:127 |
| 「拼接即成攻击」的根因 | NIST：数据与指令未走分离通道 | — | sources/U4_nist-ai100-2e2025.md:2268-2271 |

## 5.6 来源层级与已知缺口

> [!tip] 进阶 / 可跳过
> 本节交代「材料可不可信、哪块是空白」，偏整理性说明，不影响你对内容的理解，按需再读。

材料分两层：**原始来源层**（NIST 文档、OWASP 指南、各论文的摘要与正文——本手册逐字引文都回这一层）与**自制中间产物层**（本手册的大纲与研究记录——它只是索引，不是出处）。凡引文只在中间产物里能命中、回不到原始来源层的，一律视为引用链断了。

几条已知空白，列出来免得你按图索骥找不到：

**表 5-5　已知缺口（缺口 / 说明 / 处理）**

| 缺口 | 说明 | 处理 |
| --- | --- | --- |
| 某个来源件缺失 | 有一份预先编号的来源件在本项目缺失，无法逐字回源 | 全文不引用它 |
| 「七类」的具体名称 | JailbreakZoo 只说了「七种类型」，并未列出名称 | 第 3 章的七类系自建归纳，不冒充其原分类 |
| 某些数字只出现在中间产物里 | 自制大纲 / 研究记录不是出处；里面的数字若回不到原始来源件 | 一律不采用，见 5.4 末的纪律 |
| 抓取件的叠字 | PDF 抽取导致 510510 / 1818 / 3333 / 1616 / 6.06.0 等 | 按真值写 510 / 18 / 33 / 16 / 6.0，见 5.4 |

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。其余术语的逐字原文见第 1、3、4 章各自的对照表。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 54 | “Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files.” | 间接提示注入发生在 LLM 接受来自外部来源（如网站或文件）的输入时。 | sources/U5_owasp-llm01.md:16 |
