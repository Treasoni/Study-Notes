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
