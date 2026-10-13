# 02 深度素材 — AI 破甲（Jailbreak，安全与防御视角）

> ⚠️ **本文件是中间产物**：所有英文引文与数值请回 `sources/` 按行号核对，不要当成权威引用。
> 逐字引文格式：“…”（引文内自带弯引号时外层改用 「…」）；出处写 `sources/<文件>:<行号>`。
> 安全边界：全文只收**概念 / 机制 / 分类法 / 统计 / 评测 / 防御 / 治理**，**不含**任何可执行攻击载荷或可复现绕过步骤。

---

## 1. 范围与选择

- **主题**：什么叫 AI 破甲、为什么能破、如何破（机制层）→ 检测与防御。
- **方向**：**B｜三问均衡**（用户已确认），约 5 章 / 1.2–1.5 万字。
- **章维度素材映射**：
  - 第 1 章（定义与边界）← §3.1
  - 第 2 章（为何可破）← §3.2
  - 第 3 章（攻击分类与原理）← §3.3
  - 第 4 章（检测与防御 + 评测 + 治理）← §3.4 / §3.5 / §3.6
  - 第 5 章（术语与速查）← §3.7
- **取源方式**：父流程用 `.claude/skills/research-collector/scripts/crawl.sh` 确定性抓取（不派推理代理搬正文）；U4/U33 为 NIST PDF，用 `curl` 下载后 `pdftotext -layout` 转文本；U32/U12 另补全文 HTML（`*-full.md`）用于坐实数字。
- **主语言**：英文一手材料；正文引文一律附中译并留「引文对照」表（见 §7）。

## 2. 来源清单

| ID | 来源 | 机构 / 作者 · 年份 | 层级 | 落盘文件 | 行数 |
| --- | --- | --- | --- | --- | --- |
| U1 | Jailbroken: How Does LLM Safety Training Fail? | Wei, Haghtalab, Steinhardt · NeurIPS 2023 | 预印本（摘要页） | sources/U1_wei-jailbroken.md | 85 |
| U2 | Indirect Prompt Injection | Greshake et al. · 2023 | 预印本（摘要页） | sources/U2_indirect-injection.md | 86 |
| U3 | The Instruction Hierarchy | Wallace et al. (OpenAI) · 2024 | 预印本（摘要页） | sources/U3_instruction-hierarchy.md | 86 |
| U4 | NIST AI 100-2e2025（对抗 ML 分类学） | NIST / US+UK AISI · 2025-03 | 官方（PDF 全文） | sources/U4_nist-ai100-2e2025.md | 5981 |
| U5 | OWASP LLM01:2025 Prompt Injection | OWASP GenAI Security Project · 2025 | 官方/行业标准 | sources/U5_owasp-llm01.md | 121 |
| U6 | International AI Safety Report 2025 | Bengio et al. · 2025 | 官方 | **缺失（Cloudflare 挑战页）** | 5 |
| U7 | Many-shot jailbreaking | Anthropic · 2024 | 厂商研究（全文页） | sources/U7_many-shot.md | 58 |
| U8 | Red Teaming LMs to Reduce Harms | Ganguli et al. (Anthropic) · 2022 | 论文全文 | sources/U8_red-teaming-harms.md | 566 |
| U9 | Red Teaming LMs with LMs | Perez et al. · 2022 | 论文全文 | sources/U9_red-teaming-lms.md | 797 |
| U10 | Universal & Transferable Adversarial Attacks (GCG) | Zou et al. · 2023 | 预印本（摘要页） | sources/U10_gcg.md | 86 |
| U11 | "Do Anything Now"（in-the-wild 破甲提示） | Shen et al. · 2023/24 | 预印本（摘要页） | sources/U11_do-anything-now.md | 84 |
| U12 | HarmBench | Mazeika et al. · 2024 | 预印本（摘要 + 全文） | sources/U12_harmbench.md + U12_harmbench-full.md | 90 + 1238 |
| U14 | Constitutional AI: Harmlessness from AI Feedback | Bai et al. (Anthropic) · 2022 | 预印本（摘要页） | sources/U14_constitutional-ai.md | 86 |
| U15 | Fine-tuning Aligned LMs Compromises Safety… | Qi et al. · 2023 | 预印本（摘要页） | sources/U15_finetuning-safety.md | 83 |
| U16 | Prompt injection and jailbreaking are not the same thing | Simon Willison · 2024-03-05 | 可信博客 | sources/U16_willison.md | 84 |
| U17 | Refusal Is Mediated by a Single Direction | Arditi et al. · 2024 | 预印本（摘要页） | sources/U17_refusal-direction.md | 88 |
| U19 | Safety Alignment… Few Tokens Deep | Qi et al. · 2024 | 预印本（摘要页） | sources/U19_few-tokens-deep.md | 86 |
| U20 | OR-Bench（过度拒绝基准） | Cui et al. · 2024/25 | 同行评审（ICML 2025） | sources/U20_or-bench.md | 85 |
| U21 | XSTest（夸大安全行为测试） | Röttger et al. · 2023 | 同行评审（NAACL 2024） | sources/U21_xstest.md | 85 |
| U22 | How Johnny Can Persuade LLMs… | Zeng et al. · 2024 | 预印本（摘要页） | sources/U22_persuasion.md | 84 |
| U24 | Safety Tax | Huang et al. · 2025 | 预印本（摘要页） | sources/U24_safety-tax.md | 83 |
| U26 | PAIR（Twenty Queries） | Chao et al. · 2023/24 | 预印本（摘要页） | sources/U26_pair.md | 86 |
| U27 | Crescendo Multi-Turn Jailbreak | Russinovich et al. (MSFT) · 2024/25 | 预印本（摘要页） | sources/U27_crescendo.md | 85 |
| U28 | GPT-4 Is Too Smart To Be Safe（Cipher） | Yuan et al. · 2023/24 | 预印本（摘要页） | sources/U28_cipher.md | 84 |
| U29 | JailbreakZoo（综述） | Jin et al. · 2024 | 综述（摘要页） | sources/U29_jailbreakzoo.md | 84 |
| U30 | JailbreakBench | Chao et al. · NeurIPS 2024 D&B | 同行评审（摘要页） | sources/U30_jailbreakbench.md | 84 |
| U31 | Llama Guard | Inan et al. (Meta) · 2023 | 预印本（摘要页） | sources/U31_llama-guard.md | 84 |
| U32 | Constitutional Classifiers | Sharma et al. (Anthropic) · 2025 | 预印本（摘要 + 全文） | sources/U32_constitutional-classifiers.md + U32_constitutional-classifiers-full.md | 84 + 393 |
| U33 | NIST AI 600-1（Generative AI Profile） | NIST · 2024 | 官方（PDF 全文） | sources/U33_nist-ai-600-1.md | 3101 |

> **层级口径**：预印本 = arXiv（多为**摘要页**，见 §5 存疑）；官方 = NIST / OWASP 等标准文件；厂商研究 = Anthropic 官方研究页。
> **未纳入**：U13 / U18 / U23 / U25（P1 列为可选补充，本方向 B 不依赖，未抓取）。

---

## 3. 关键事实与 claim ↔ 来源对照

### 3.1 什么叫破甲（定义与边界）— 供第 1 章

**核心定义**（三条权威表述，措辞各异，**不可混引**）：

- NIST（最贴「破甲 = 绕过输出限制」；此处取术语表原句，正文 `:2524-2525` 同句，PDF 断词作 `circum-venting`）：
  “A DIRECT PROMPTING ATTACK intended to circumvent restrictions placed on model outputs, such as circumventing refusal behaviour to enable misuse.”
  中译：一种**直接提示攻击**，意在绕过施加于模型输出上的限制，例如绕过拒绝行为以促成滥用。
  出处 sources/U4_nist-ai100-2e2025.md:5791
- NIST AI 600-1（把「构造提示以绕开输出控制」直接命名为 jailbreaking；引文内自带弯引号，故外层用 「」）：
  「Crafting such prompts deliberately is known as “jailbreaking,” or, manipulating prompts to circumvent output controls.」
  中译：蓄意构造此类提示即所谓「越狱」，也就是操纵提示以绕过输出控制。
  出处 sources/U33_nist-ai-600-1.md:369-370
- OWASP：
  “Jailbreaking is a form of prompt injection where the attacker provides inputs that cause the model to disregard its safety protocols entirely.”
  中译：越狱是提示注入的一种形式：攻击者提供的输入使模型完全无视其安全协议。
  出处 sources/U5_owasp-llm01.md:11
- Willison（区分 prompt injection 与 jailbreaking）：
  “Jailbreaking is the class of attacks that attempt to subvert safety filters built into the LLMs themselves.”
  中译：越狱是一类试图颠覆**内建于 LLM 自身**的安全过滤器的攻击。
  出处 sources/U16_willison.md:16

**破甲 ≠ 提示注入**（两条判据）：

- 应用层 vs 模型层：“Prompt injection is a class of attacks against applications built on top of Large Language Models (LLMs) that work by concatenating untrusted user input with a trusted prompt constructed by the application’s developer.”（中译：提示注入针对**构建在 LLM 之上的应用**，手法是把不受信的用户输入与开发者构造的可信提示拼接在一起。）出处 sources/U16_willison.md:15
- 判据句：“if there’s no concatenation of trusted and untrusted strings, it’s _not prompt injection_.”（中译：若没有「可信字符串与不受信字符串的拼接」，那就**不是**提示注入。）出处 sources/U16_willison.md:17
- 间接提示注入的原始定义：“We reveal new attack vectors, using Indirect Prompt Injection, that enable adversaries to remotely (without a direct interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved.”（中译：攻击者无需直接接口，只要把提示策略性地注入很可能被检索到的数据中，即可远程利用集成 LLM 的应用。）出处 sources/U2_indirect-injection.md:16
- **共同根因 = 指令无强制优先级**：“one of the primary vulnerabilities underlying these attacks is that LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties.”（中译：这些攻击之所以成立的主要漏洞之一，是 LLM 常把系统提示与来自不受信用户及第三方的文本视为**同等优先级**。）出处 sources/U3_instruction-hierarchy.md:16
- NIST 的根因类比（数据/指令同通道，类比 SQL 注入）：“underlying many of the security vulnerabilities in LLM applications is the fact that data and instructions are not provided in separate channels to the LLM, which allows attackers to use data channels to inject malicious instructions in inference-time attacks (a similar flaw to that which underlies decades-old SQL injection attacks).”（中译：许多 LLM 应用安全漏洞的根源在于数据与指令并非经由**分离的通道**提供，使攻击者能借数据通道注入恶意指令。）出处 sources/U4_nist-ai100-2e2025.md:2268-2271

**破甲 ≠ 红队**（红队是防御方方法论）：

- “One potentially useful tool for addressing harm is red teaming—using manual or automated methods to adversarially probe a language model for harmful outputs, and then updating the model to avoid such outputs”（中译：应对危害的一个可能有用工具是**红队**——用人工或自动化方法对抗性地探测语言模型的有害输出，再据此更新模型。）出处 sources/U8_red-teaming-harms.md:15

> **归一化写作口径（给下游）**：速记 = **注入让模型「做」它不该做的；破甲让模型「说」它不该说的**。归类关系三源不一致（见 §4 冲突 1），正文须**分述**而非合并。

### 3.2 为什么能破（对齐的固有局限）— 供第 2 章

**主根因：两大失效模式**（Wei et al.）：

- “We hypothesize two failure modes of safety training: competing objectives and mismatched generalization.”（中译：安全训练的两种失效模式——**竞争目标**与**泛化不匹配**。）出处 sources/U1_wei-jailbroken.md:10
- “Competing objectives arise when a model's capabilities and safety goals conflict, while mismatched generalization occurs when safety training fails to generalize to a domain for which capabilities exist.”（中译：「竞争目标」出现在模型能力目标与安全目标冲突时；「泛化不匹配」出现在安全训练未能泛化到模型已具备能力的领域时。）出处 sources/U1_wei-jailbroken.md:10
- “Our analysis emphasizes the need for safety-capability parity -- that safety mechanisms should be as sophisticated as the underlying model -- and argues against the idea that scaling alone can resolve these safety failure modes.”（中译：强调需要**安全-能力对等**，并反驳「单纯扩大规模即可解决」的观点。）出处 sources/U1_wei-jailbroken.md:10

**对齐浅且低维，小扰动即可抹掉**：

- 单一方向中介拒绝：“we show that refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models up to 72B parameters in size.”（中译：在 13 个主流开源对话模型（至 72B 参数）上，拒绝行为由**一个一维子空间**中介。）出处 sources/U17_refusal-direction.md:16
- “Our findings underscore the brittleness of current safety fine-tuning methods.”（中译：凸显当前安全微调方法的**脆弱性**。）出处 sources/U17_refusal-direction.md:16
- 浅层对齐（只在最前面几个输出 token 上生效）：“the alignment adapts a model's generative distribution primarily over only its very first few output tokens. We refer to this issue as shallow safety alignment.”（中译：对齐主要只作用于**最前面几个输出 token**；这称为**浅层安全对齐**。）出处 sources/U19_few-tokens-deep.md:16

**微调即可破坏安全（低成本）**：

- “we jailbreak GPT-3.5 Turbo's safety guardrails by fine-tuning it on only 10 such examples at a cost of less than $0.20 via OpenAI's APIs, making the model responsive to nearly any harmful instructions.”（中译：仅用 **10 条**样本、花费**不足 0.20 美元**微调，即破掉 GPT-3.5 Turbo 的安全护栏。）出处 sources/U15_finetuning-safety.md:10
- “even without malicious intent, simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent.”（中译：即便毫无恶意，仅用**常见良性数据集**微调也会在较小程度上无意退化安全对齐。）出处 sources/U15_finetuning-safety.md:10

**能力-安全权衡（安全税）**：

- “Safety alignment leads to a degradation of the reasoning capability of LRMs.”（中译：安全对齐会导致大推理模型（LRM）推理能力下降。）出处 sources/U24_safety-tax.md:10
- “there exists a trade-off between reasoning and safety capability”（中译：推理能力与安全能力之间存在**权衡**。）出处 sources/U24_safety-tax.md:10

### 3.3 如何破甲 · 攻击分类与原理（机制层，**不含载荷**）— 供第 3 章

| 类别 | 机制一句话 | 逐字引文（出处） |
| --- | --- | --- |
| 多示例（many-shot） | 单条提示内塞入大量「已照做」示范，末接真实问题 | “However, simply including a very large number of faux dialogues preceding the final question—in our research, we tested up to 256—produces a very different response.” sources/U7_many-shot.md:29 |
| 角色扮演 / 人格化 | 让模型扮演「不受限」角色作答 | “In a roleplay attack we exploit the helpfulness of the model by asking it to roleplay as a malevolent character.” sources/U8_red-teaming-harms.md:138 |
| 自动/优化攻击（对抗后缀 GCG） | 贪心+梯度搜索自动生成可迁移后缀 | “our approach automatically produces these adversarial suffixes by a combination of greedy and gradient-based search techniques” sources/U10_gcg.md:10 |
| 编码 / 密码混淆 | 用非自然语言承载请求，绕开只在自然语言上做的对齐 | “we discover that chat in cipher can bypass the safety alignment techniques of LLMs, which are mainly conducted in natural languages.” sources/U28_cipher.md:10 |
| 多轮渐进升级 | 从无害问题起步，逐轮引用模型自身回复升级 | “Crescendo is a simple multi-turn jailbreak that interacts with the model in a seemingly benign manner.” sources/U27_crescendo.md:10 |
| 说服 / 劝说（PAP） | 用社会科学说服策略重述请求 | “we propose a persuasion taxonomy derived from decades of social science research.” sources/U22_persuasion.md:10 |
| 自动化红队（PAIR / LM 生成攻击） | 用攻击者 LM 迭代生成并打分改进 | “we generate test inputs using an LM itself, and we use a classifier to detect harmful behavior on test inputs” sources/U9_red-teaming-lms.md:18 |

**关键统计（据摘要/全文，均已回源核对）**：

- many-shot 有效性随示范数按**幂律**上升（引文内自带弯引号，外层用 「」）：「The effectiveness of many-shot jailbreaking increases as we increase the number of “shots” (dialogues in the prompt) according to a scaling trend known as a power law」（中译：多示例破甲的有效性随「示例」数量按**幂律**增长。）出处 sources/U7_many-shot.md:39；测试上限 **256** 段示范（sources/U7_many-shot.md:29）。
- in-the-wild 规模（U11）：**1,405** 条破甲提示（2022-12→2023-12）；主要策略为 prompt injection 与 privilege escalation；**5** 条高效提示在 GPT-3.5/GPT-4 上达 **0.95** 攻击成功率、最早一条已在线 **240+** 天。引文：“we conduct a comprehensive analysis of 1,405 jailbreak prompts spanning from December 2022 to December 2023.” 出处 sources/U11_do-anything-now.md:10
- 对抗后缀可跨模型迁移：“the resulting attack suffix is able to induce objectionable content in the public interfaces to ChatGPT, Bard, and Claude, as well as open source LLMs such as LLaMA-2-Chat, Pythia, Falcon, and others”（中译：该后缀能在 ChatGPT、Bard、Claude 的公开接口及 LLaMA-2-Chat、Pythia、Falcon 等开源 LLM 上诱出不良内容。）出处 sources/U10_gcg.md:10
- PAIR 高效：“Empirically, PAIR often requires fewer than twenty queries to produce a jailbreak, which is orders of magnitude more efficient than existing algorithms.”（中译：PAIR 常能在**少于二十次查询**内产出一次破甲，比既有算法高效数个数量级。）出处 sources/U26_pair.md:10
- Crescendo 自动化版在 AdvBench 子集上超过 SOTA：GPT-4 上 **高 29–61%**、Gemini-Pro 上 **高 49–71%**（据摘要，sources/U27_crescendo.md:10）。
- 密码攻击：**某些密码在若干安全域几乎 100% 绕过 GPT-4**（据摘要，sources/U28_cipher.md:10）。
- 分类学：JailbreakZoo 把破甲归为 **七类**：“Our study categorizes jailbreaks into seven distinct types and elaborates on defense strategies that address these vulnerabilities.” 出处 sources/U29_jailbreakzoo.md:10
- 攻防不对称（防御方要防住全部攻击）：“Adversaries only need one attack to succeed, while red teams must be defend against all possible attacks.”（原文如此，`be defend` 为原文笔误）出处 sources/U9_red-teaming-lms.md:230

> **安全边界执行记录**：U7 第 29 行附近的 faux dialogue 含具体目标问句示例 → **已跳过，未记录**；其余文件为摘要/机制/统计，未出现可复现载荷。

### 3.4 检测与防御（分层）— 供第 4 章

**训练期**：

- Constitutional AI / RLAIF：“The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'.”（中译：唯一的人类监督通过一份规则或原则清单提供，故称「**宪法式 AI**」。）出处 sources/U14_constitutional-ai.md:10；同源 “we use 'RL from AI Feedback' (RLAIF)”（中译：使用「**基于 AI 反馈的强化学习**」。）出处 sources/U14_constitutional-ai.md:10
- 对抗训练（robust refusal）：HarmBench 论文提出 “we propose a new adversarial training method for robust refusal, called Robust Refusal Dynamic Defense (R2D2).”（中译：提出一种面向鲁棒拒绝的新对抗训练方法，名为 R2D2。）出处 sources/U12_harmbench-full.md:127；效果 = 把 GCG 上的 ASR 压到 **5.9%**，优于 Llama 2 7B Chat（**31.8**）与 13B Chat（**30.2**）（数值回原文重计，sources/U12_harmbench-full.md:183）；训练成本 **16 小时 / 8×A100**（sources/U12_harmbench-full.md:181）；MT-Bench 由 6.5 降至 **6.0**，即鲁棒性提升伴随轻微通用能力损失（sources/U12_harmbench-full.md:185）。

**运行期护栏（独立分类器）**：

- Llama Guard 同时做输入/输出判定：“This taxonomy is also instrumental in classifying the responses generated by LLMs to these prompts, a process we refer to as response classification.”（中译：该分类法也有助于对 LLM 生成的**回答**进行分类，即**回答分类**。）出处 sources/U31_llama-guard.md:10
- Constitutional Classifiers（合成数据 + 宪法）：“safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted content”（中译：用**合成数据**训练的护栏，数据由 LLM 依据一组用自然语言描述允许与受限内容的规则（即一部「宪法」）生成。）出处 sources/U32_constitutional-classifiers.md:10
  - 公开红队强度：“In over 3,000 estimated hours of red teaming, no red teamer found a universal jailbreak”（中译：在估计**超过 3,000 小时**的红队中，没有任何红队员找到「通用破甲」。）出处 sources/U32_constitutional-classifiers.md:10
  - 部署代价：“with an absolute 0.38% increase in production-traffic refusals and a 23.7% inference overhead”（中译：生产流量拒绝率**绝对上升 0.38%**，推理开销 **23.7%**。）出处 sources/U32_constitutional-classifiers.md:10

**提示级缓解**：

- many-shot 论文报告分类/改写法把攻击成功率从 **61% 降到 2%**：“One such technique substantially reduced the effectiveness of many-shot jailbreaking — in one case dropping the attack success rate from 61% to 2%.” 出处 sources/U7_many-shot.md:44

> ⚠️ **数字更正**：P1 汇总里写的「越狱成功率 86% → 4.4%」**不可溯源**——`sources/U32_constitutional-classifiers-full.md` 全文 **0 处** `4.4`。U32 全文的原文是 “reducing the jailbreak success rate from 86% against a HHH model to less than 5%”（出处 sources/U32_constitutional-classifiers-full.md:98），另有 “our classifier-guarded system refuses over 95% of held-out jailbreaking attempts, compared to only 14% without classifiers”（出处 sources/U32_constitutional-classifiers-full.md:16）。**正文一律改用 86%→<5%（以及 >95% vs 14%），不得再写 4.4%。**

### 3.5 评测基准与口径 — 供第 4 章

- HarmBench 的 ASR 定义：“The primary measure of a red teaming method’s success is its attack success rate (ASR) on a given target model, which is the percentage of test cases that elicit the behavior from the target model.”（中译：衡量红队方法成败的首要指标是它对给定目标模型的**攻击成功率（ASR）**，即能诱出目标行为的测试用例占比。）出处 sources/U12_harmbench-full.md:51
- HarmBench 规模（**已按去重后计数**）：**510** 条行为（400 条文本 + 110 条多模态）、**18** 种红队方法（来自 12 篇论文）、**33** 个目标 LLM。
  - ⚠️ 缓存文本出现数字重影（`510510` / `1818` / `3333` / `400400` / `110110`，为 HTML 导入时把「数值 + 脚注」粘连所致）→ 正确值取 **510（400+110）/ 18 / 33**，不取重影串。
- HarmBench 结论：“no current attack or defense is uniformly effective, and that robustness is independent of model size.”（中译：当前**没有任何攻击或防御是普遍有效的**，且鲁棒性与模型规模无关。）出处 sources/U12_harmbench-full.md:15；“No model is robust to all attacks, and no attack breaks all models.”（中译：没有模型能抗住所有攻击，也没有哪种攻击能攻破所有模型。）出处 sources/U12_harmbench-full.md:103
- JailbreakBench：“existing works compute costs and success rates in incomparable ways”（中译：既有工作在成本与成功率的算法上**互不可比**。）出处 sources/U30_jailbreakbench.md:10；组件含 “a jailbreaking dataset comprising 100 behaviors” 与排行榜（同源）。
- 过度拒绝基准 OR-Bench：“OR-Bench, the first large-scale over-refusal benchmark”（中译：首个**大规模过度拒绝基准**。）出处 sources/U20_or-bench.md:10；含 **80,000** 条过度拒绝 prompt（10 类）+ **~1,000** 条 hard + **600** 条有毒对照。机理：“the enhanced safety often come with the side effect of over-refusal, where LLMs may reject innocuous prompts and become less helpful”（中译：安全性增强常带来**过度拒绝**副作用。）出处 sources/U20_or-bench.md:10
- XSTest：“XSTest comprises 250 safe prompts across ten prompt types that well-calibrated models should not refuse to comply with, and 200 unsafe prompts as contrasts that models, for most applications, should refuse.”（中译：250 条安全提示 + 200 条不安全提示作对照。）出处 sources/U21_xstest.md:10

> **口径提醒（给下游）**：「各基准不可直接横比」在本地**只有半证据**——U30 的 “incomparable ways” 指既有工作算法不一致，并非显式说「HarmBench 与 JailbreakBench 不能横比」。正文表述宜收敛为「不同基准的 ASR 口径与判官不同，**跨基准数字不可直接并列**」，并给 U30 该句为据。

### 3.6 治理框架 — 供第 4 章

- NIST AI 600-1 把提示注入/越狱并入风险清单（**无独立条目**）：越狱归入 2.3 节 Dangerous, Violent, or Hateful Content（节标题逐字见 sources/U33_nist-ai-600-1.md:346）；提示注入归入 2.9 节 Information Security（节标题逐字见 sources/U33_nist-ai-600-1.md:524）。
  - “it expands the available attack surface, as GAI itself is vulnerable to attacks like prompt injection or data poisoning.”（中译：它扩大了攻击面，因为生成式 AI 本身就可能遭受提示注入或数据投毒之类的攻击。）出处 sources/U33_nist-ai-600-1.md:529-531
  - TEVV 局限：“Similarly, jailbreaking or prompt engineering tests may not systematically assess validity or reliability risks.”（中译：越狱或提示工程测试可能**无法系统性地评估**有效性或可靠性风险。）出处 sources/U33_nist-ai-600-1.md:2649-2651
- NIST 的「纵深防御」原文（**注意：出自 U4，不是 OWASP**）：“These may provide supplementary assurance through a defense-in-depth philosophy.”（中译：这些可通过**纵深防御**的理念提供补充性保证。）出处 sources/U4_nist-ai100-2e2025.md:2788
- OWASP 的对应表述是「无万无一失的防范」（**不是** defense-in-depth）：“Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention for prompt injection.”（中译：鉴于模型工作方式的核心存在随机性影响，**尚不清楚**提示注入是否存在万无一失的防范方法。）出处 sources/U5_owasp-llm01.md:28

### 3.7 术语与速查源 — 供第 5 章

| 术语 | 定义源（本地行号） |
| --- | --- |
| jailbreak（越狱） | sources/U4_nist-ai100-2e2025.md:5791；sources/U33_nist-ai-600-1.md:369-370；sources/U5_owasp-llm01.md:11；sources/U16_willison.md:16 |
| prompt injection（提示注入） | sources/U16_willison.md:15（应用层，判据=可信/不受信字符串拼接）；sources/U33_nist-ai-600-1.md:551-556（直接/间接） |
| 间接提示注入 | sources/U2_indirect-injection.md:16；sources/U5_owasp-llm01.md:16 |
| red teaming（红队） | sources/U8_red-teaming-harms.md:15 |
| alignment / 对齐 | sources/U1_wei-jailbroken.md:10；sources/U14_constitutional-ai.md:10 |
| refusal（拒绝行为） | sources/U17_refusal-direction.md:16 |
| ASR（攻击成功率） | sources/U12_harmbench-full.md:51 |
| over-refusal（过度拒绝） | sources/U20_or-bench.md:10；sources/U21_xstest.md:10 |
| safety tax（安全税） | sources/U24_safety-tax.md:10 |
| many-shot | sources/U7_many-shot.md:29 / :39 / :44 |

第 3.7 表「间接提示注入」条对应引文：“Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files.”（中译：间接提示注入发生在 LLM 接受来自外部来源（如网站或文件）的输入时。）出处 sources/U5_owasp-llm01.md:16

---

## 4. 冲突与存疑（已记录，不静默合并）

1. **jailbreak 与 prompt injection 的归类关系三源不一致**（对第 1 章边界关键）：
   - OWASP（sources/U5_owasp-llm01.md:11）：「Jailbreaking **is a form of** prompt injection」→ 包含关系。
   - Willison（sources/U16_willison.md:15-17）：二者**不同类**，判据是「有无可信/不受信字符串拼接」。
   - NIST（sources/U4_nist-ai100-2e2025.md:5791）把 jailbreak 定义为一种「DIRECT PROMPTING ATTACK」；而 direct prompt injection 也被归为 direct prompting attack 的**子集** → jailbreak 与 direct prompt injection 是**兄弟还是包含**，原文未判死。
   - **写作口径**：分述三家措辞，指出「学界未统一」，**不要**替它们下结论式等价。
2. **U32 的 86%→4.4% 在本地不存在**（见 §3.4）。已定位为 P1 中间产物引入的错误，正确值 86%→<5%。
3. **HarmBench 数字重影**（510510/1818/3333）→ 取 510（400+110）/18/33（见 §3.5）。
4. **「纵深防御」归属**：原文在 U4(NIST)，不在 U5(OWASP)（见 §3.6）。
5. **U19 无确切 token 数**：摘要只说「very first few output tokens」，无可引用的 N。
6. **arXiv 摘要页普遍限制**：U1/U2/U3/U10/U11/U14/U15/U17/U19/U20/U21/U22/U24/U26/U27/U28/U29/U30/U31 本地仅摘要页 → 正文可引的数字以摘要所载为限，实验细节/曲线数值**不可得**。
7. **U8/U9 时代问题**：2022 年研究早于现代 RLHF 管线，其对**当前前沿模型**的结论应标注为**历史基线**。
8. **U8 内部张力**：RS 干预「最难攻破」但同时「靠回避而无害」；HHH prompt 在对话红队下与 plain LM 无显著差异，与其此前静态评测结论不一致 → 须并列陈述。
9. **U4 术语表与正文拼写不一致**：术语表（`:5791`）作 `behaviour`，正文（`:2525`）作 `behavior`；正文该处更有 PDF 断词 `circum-venting`。引用时须注明取的是哪一处。

## 5. 未决问题（P2 → P3 前可知；写作时回避或标注）

- **U6 缺失**：国际 AI 安全报告被 Cloudflare 挡下（Wayback 亦不可用）→ 第 1 章「国际治理口径」缺一手来源，改用 NIST（U4/U33）+ OWASP（U5）替代，并在来源表注明。
- **U29 缺「七类」分面名称**：只知「seven distinct types」，无各类标签 → 第 3 章分类表**以 §3.3 自建的 7 类机制表为准**，不冒充 JailbreakZoo 的原始七类。
- **U22 缺说服分类法类别**、**U26/U27/U28 缺具体成功率/轮数/密码名** → 第 3 章这些点只写机制，不写未核实的细节数字。
- **U32 的「过度拒绝代价」**：摘要无独立过度拒绝数字，只有 0.38% 生产流量拒绝率增量可作代理指标。

## 6. 下游交接（给 outline-generator / chapter-writer）

- **章维映射**：§3.1→第 1 章；§3.2→第 2 章；§3.3→第 3 章；§3.4+§3.5+§3.6→第 4 章；§3.7→第 5 章。
- **必须跨章冻结的口径（逐条照抄）**：
  1. 破甲定义以 NIST（sources/U4_nist-ai100-2e2025.md:5791）为主口径；OWASP/Willison 作并列表述，**不合并**。
  2. **禁用数字**：`4.4%`（本地不存在）。用 `86% → <5%`、`>95% vs 14%`、`0.38%`、`23.7%`、`61% → 2%`。
  3. HarmBench 规模 = **510（400 文本 + 110 多模态）/ 18 / 33**。
  4. 引文一律英文原文 + 中译 + 出处（`sources/<文件>:<行号>`）；**代码/命令/术语保留原文**。
  5. 「纵深防御」归 NIST(U4)；OWASP 只给「无万无一失方法」。
  6. R2D2 是 HarmBench 论文的对抗训练方法（`Robust Refusal Dynamic Defense`），可正常命名与引用（sources/U12_harmbench-full.md:127）。
  7. 安全边界：只写机制/分类/防御，**不产出可执行载荷**。
- **写作素材来源**：正文引用的每处英文引文，均可在 `sources/` 按行号回源；请勿凭本文件的概述二次转写引文（本文件是**中间产物**）。
- **术语白话化**（note-style 入门优先）：jailbreak / prompt injection / red teaming / alignment / refusal / ASR / over-refusal / safety tax 首次出现均需一句大白话。

## 7. 英文引文对照（原文 / 中译 / 出处）

> 「出处」列 = `sources/<文件>:<行号>`。中译为**成句引文**的中文翻译；代码/术语不译。引文内自带弯引号者，原文列外层用 「」。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “A DIRECT PROMPTING ATTACK intended to circumvent restrictions placed on model outputs, such as circumventing refusal behaviour to enable misuse.” | 一种**直接提示攻击**，意在绕过施加于模型输出上的限制，例如绕过拒绝行为以促成滥用。 | sources/U4_nist-ai100-2e2025.md:5791 |
| 2 | 「Crafting such prompts deliberately is known as “jailbreaking,” or, manipulating prompts to circumvent output controls.」 | 蓄意构造此类提示即所谓「越狱」，也就是操纵提示以绕过输出控制。 | sources/U33_nist-ai-600-1.md:369-370 |
| 3 | “Jailbreaking is a form of prompt injection where the attacker provides inputs that cause the model to disregard its safety protocols entirely.” | 越狱是提示注入的一种形式：攻击者提供的输入使模型完全无视其安全协议。 | sources/U5_owasp-llm01.md:11 |
| 4 | “Prompt injection is a class of attacks against applications built on top of Large Language Models (LLMs) that work by concatenating untrusted user input with a trusted prompt constructed by the application’s developer.” | 提示注入针对构建在 LLM 之上的应用，手法是把不受信的用户输入与开发者构造的可信提示拼接在一起。 | sources/U16_willison.md:15 |
| 5 | “Jailbreaking is the class of attacks that attempt to subvert safety filters built into the LLMs themselves.” | 越狱是一类试图颠覆**内建于 LLM 自身**的安全过滤器的攻击。 | sources/U16_willison.md:16 |
| 6 | “if there’s no concatenation of trusted and untrusted strings, it’s _not prompt injection_.” | 若没有「可信字符串与不受信字符串的拼接」，那就**不是**提示注入。 | sources/U16_willison.md:17 |
| 7 | “one of the primary vulnerabilities underlying these attacks is that LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties.” | 这些攻击之所以成立的主要漏洞之一，是 LLM 常把系统提示与来自不受信用户及第三方的文本视为**同等优先级**。 | sources/U3_instruction-hierarchy.md:16 |
| 8 | “We reveal new attack vectors, using Indirect Prompt Injection, that enable adversaries to remotely (without a direct interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved.” | 攻击者无需直接接口，只要把提示策略性地注入很可能被检索到的数据中，即可远程利用集成 LLM 的应用。 | sources/U2_indirect-injection.md:16 |
| 9 | “underlying many of the security vulnerabilities in LLM applications is the fact that data and instructions are not provided in separate channels to the LLM, which allows attackers to use data channels to inject malicious instructions in inference-time attacks (a similar flaw to that which underlies decades-old SQL injection attacks).” | 许多 LLM 应用安全漏洞的根源在于数据与指令并非经由**分离的通道**提供，使攻击者能借数据通道注入恶意指令。 | sources/U4_nist-ai100-2e2025.md:2268-2271 |
| 10 | “One potentially useful tool for addressing harm is red teaming—using manual or automated methods to adversarially probe a language model for harmful outputs, and then updating the model to avoid such outputs” | 应对危害的一个可能有用工具是**红队**——用人工或自动化方法对抗性地探测语言模型的有害输出，再据此更新模型。 | sources/U8_red-teaming-harms.md:15 |
| 11 | “We hypothesize two failure modes of safety training: competing objectives and mismatched generalization.” | 安全训练的两种失效模式——**竞争目标**与**泛化不匹配**。 | sources/U1_wei-jailbroken.md:10 |
| 12 | “Competing objectives arise when a model's capabilities and safety goals conflict, while mismatched generalization occurs when safety training fails to generalize to a domain for which capabilities exist.” | 「竞争目标」出现在模型能力目标与安全目标冲突时；「泛化不匹配」出现在安全训练未能泛化到模型已具备能力的领域时。 | sources/U1_wei-jailbroken.md:10 |
| 13 | “Our analysis emphasizes the need for safety-capability parity -- that safety mechanisms should be as sophisticated as the underlying model -- and argues against the idea that scaling alone can resolve these safety failure modes.” | 强调需要**安全-能力对等**，并反驳「单纯扩大规模即可解决」的观点。 | sources/U1_wei-jailbroken.md:10 |
| 14 | “we show that refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models up to 72B parameters in size.” | 在 13 个主流开源对话模型（至 72B 参数）上，拒绝行为由**一个一维子空间**中介。 | sources/U17_refusal-direction.md:16 |
| 15 | “Our findings underscore the brittleness of current safety fine-tuning methods.” | 凸显当前安全微调方法的**脆弱性**。 | sources/U17_refusal-direction.md:16 |
| 16 | “the alignment adapts a model's generative distribution primarily over only its very first few output tokens. We refer to this issue as shallow safety alignment.” | 对齐主要只作用于**最前面几个输出 token**；这称为**浅层安全对齐**。 | sources/U19_few-tokens-deep.md:16 |
| 17 | “we jailbreak GPT-3.5 Turbo's safety guardrails by fine-tuning it on only 10 such examples at a cost of less than $0.20 via OpenAI's APIs, making the model responsive to nearly any harmful instructions.” | 仅用 **10 条**样本、花费**不足 0.20 美元**微调，即破掉 GPT-3.5 Turbo 的安全护栏。 | sources/U15_finetuning-safety.md:10 |
| 18 | “even without malicious intent, simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent.” | 即便毫无恶意，仅用**常见良性数据集**微调也会在较小程度上无意退化安全对齐。 | sources/U15_finetuning-safety.md:10 |
| 19 | “Safety alignment leads to a degradation of the reasoning capability of LRMs.” | 安全对齐会导致大推理模型（LRM）推理能力下降。 | sources/U24_safety-tax.md:10 |
| 20 | “there exists a trade-off between reasoning and safety capability” | 推理能力与安全能力之间存在**权衡**。 | sources/U24_safety-tax.md:10 |
| 21 | “However, simply including a very large number of faux dialogues preceding the final question—in our research, we tested up to 256—produces a very different response.” | 只要在最终问题前放入**极大量**的虚构对话，就会得到截然不同的回答——我们测试了**多达 256 段**。 | sources/U7_many-shot.md:29 |
| 22 | 「The effectiveness of many-shot jailbreaking increases as we increase the number of “shots” (dialogues in the prompt) according to a scaling trend known as a power law」 | 多示例破甲的有效性随「示例」数量按**幂律**增长。 | sources/U7_many-shot.md:39 |
| 23 | “One such technique substantially reduced the effectiveness of many-shot jailbreaking — in one case dropping the attack success rate from 61% to 2%.” | 其中一种技术大幅削弱了多示例破甲——有一例把攻击成功率从 **61% 降到 2%**。 | sources/U7_many-shot.md:44 |
| 24 | “In a roleplay attack we exploit the helpfulness of the model by asking it to roleplay as a malevolent character.” | 在角色扮演攻击中，我们利用模型的「乐于助人」倾向，让它扮演一个**反派角色**。 | sources/U8_red-teaming-harms.md:138 |
| 25 | “our approach automatically produces these adversarial suffixes by a combination of greedy and gradient-based search techniques” | 我们的方法通过**贪心搜索与梯度搜索**的组合，自动生成这些对抗后缀。 | sources/U10_gcg.md:10 |
| 26 | “the resulting attack suffix is able to induce objectionable content in the public interfaces to ChatGPT, Bard, and Claude, as well as open source LLMs such as LLaMA-2-Chat, Pythia, Falcon, and others” | 该后缀能在 ChatGPT、Bard、Claude 的公开接口及 LLaMA-2-Chat、Pythia、Falcon 等开源 LLM 上诱出不良内容。 | sources/U10_gcg.md:10 |
| 27 | “we conduct a comprehensive analysis of 1,405 jailbreak prompts spanning from December 2022 to December 2023.” | 我们对 2022 年 12 月至 2023 年 12 月间的 **1,405 条**破甲提示做了全面分析。 | sources/U11_do-anything-now.md:10 |
| 28 | “we propose a persuasion taxonomy derived from decades of social science research.” | 我们提出一套源自数十年社会科学研究的**说服分类法**。 | sources/U22_persuasion.md:10 |
| 29 | “Empirically, PAIR often requires fewer than twenty queries to produce a jailbreak, which is orders of magnitude more efficient than existing algorithms.” | 实测中，PAIR 常能在**少于二十次查询**内产出一次破甲，比既有算法高效了数个数量级。 | sources/U26_pair.md:10 |
| 30 | “Crescendo is a simple multi-turn jailbreak that interacts with the model in a seemingly benign manner.” | Crescendo 是一种简单的多轮破甲，它以**看似无害**的方式与模型交互。 | sources/U27_crescendo.md:10 |
| 31 | “we discover that chat in cipher can bypass the safety alignment techniques of LLMs, which are mainly conducted in natural languages.” | 我们发现，**用密码交谈**可以绕过 LLM 的安全对齐——而这类对齐主要是在**自然语言**上进行的。 | sources/U28_cipher.md:10 |
| 32 | “we generate test inputs using an LM itself, and we use a classifier to detect harmful behavior on test inputs” | 我们用**一个语言模型自身**来生成测试输入，并用分类器检测测试输入上的有害行为。 | sources/U9_red-teaming-lms.md:18 |
| 33 | “Adversaries only need one attack to succeed, while red teams must be defend against all possible attacks.” | 攻击者**只需一次成功**，而红队必须防住**所有可能的攻击**。 | sources/U9_red-teaming-lms.md:230 |
| 34 | “Our study categorizes jailbreaks into seven distinct types and elaborates on defense strategies that address these vulnerabilities.” | 我们的研究把破甲归为**七种不同类型**，并详述了针对这些脆弱性的防御策略。 | sources/U29_jailbreakzoo.md:10 |
| 35 | “The primary measure of a red teaming method’s success is its attack success rate (ASR) on a given target model, which is the percentage of test cases that elicit the behavior from the target model.” | 衡量红队方法成败的首要指标是它对给定目标模型的**攻击成功率（ASR）**，即能诱出目标行为的测试用例占比。 | sources/U12_harmbench-full.md:51 |
| 36 | “no current attack or defense is uniformly effective, and that robustness is independent of model size.” | 当前**没有任何攻击或防御是普遍有效的**，且鲁棒性与模型规模无关。 | sources/U12_harmbench-full.md:15 |
| 37 | “No model is robust to all attacks, and no attack breaks all models.” | 没有模型能抗住所有攻击，也没有哪种攻击能攻破所有模型。 | sources/U12_harmbench-full.md:103 |
| 38 | “The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'.” | 唯一的人类监督通过一份规则或原则清单提供，因此我们把该方法称为「**宪法式 AI**」。 | sources/U14_constitutional-ai.md:10 |
| 39 | “we use 'RL from AI Feedback' (RLAIF)” | 我们使用「**基于 AI 反馈的强化学习**」（RLAIF）。 | sources/U14_constitutional-ai.md:10 |
| 40 | “This taxonomy is also instrumental in classifying the responses generated by LLMs to these prompts, a process we refer to as response classification.” | 该分类法也有助于对 LLM 针对这些提示生成的**回答**进行分类，这一过程我们称为**回答分类**。 | sources/U31_llama-guard.md:10 |
| 41 | “safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted content” | 用**合成数据**训练的护栏，这些数据由 LLM 依据一组用自然语言描述允许与受限内容的规则（即一部「宪法」）生成。 | sources/U32_constitutional-classifiers.md:10 |
| 42 | “In over 3,000 estimated hours of red teaming, no red teamer found a universal jailbreak” | 在估计**超过 3,000 小时**的红队中，没有任何红队员找到一个能通杀各类请求的「通用破甲」。 | sources/U32_constitutional-classifiers.md:10 |
| 43 | “with an absolute 0.38% increase in production-traffic refusals and a 23.7% inference overhead” | 代价是生产流量拒绝率**绝对上升 0.38%**，以及 **23.7%** 的推理开销。 | sources/U32_constitutional-classifiers.md:10 |
| 44 | “reducing the jailbreak success rate from 86% against a HHH model to less than 5%” | 把越狱成功率从 HHH 模型上的 **86%** 降到 **不足 5%**。 | sources/U32_constitutional-classifiers-full.md:98 |
| 45 | “our classifier-guarded system refuses over 95% of held-out jailbreaking attempts, compared to only 14% without classifiers” | 我们的分类器防护系统拒绝了**超过 95%** 的留出集越狱尝试，而无分类器时只有 **14%**。 | sources/U32_constitutional-classifiers-full.md:16 |
| 46 | “OR-Bench, the first large-scale over-refusal benchmark” | OR-Bench，首个**大规模过度拒绝基准**。 | sources/U20_or-bench.md:10 |
| 47 | “the enhanced safety often come with the side effect of over-refusal, where LLMs may reject innocuous prompts and become less helpful” | 安全性的增强常带来**过度拒绝**的副作用——LLM 可能拒绝无害提示，从而变得不那么有用。 | sources/U20_or-bench.md:10 |
| 48 | “XSTest comprises 250 safe prompts across ten prompt types that well-calibrated models should not refuse to comply with, and 200 unsafe prompts as contrasts that models, for most applications, should refuse.” | XSTest 含 **250 条**安全提示（跨十种提示类型，校准良好的模型不应拒绝）与 **200 条**不安全提示作对照（在多数应用中模型应拒绝）。 | sources/U21_xstest.md:10 |
| 49 | “existing works compute costs and success rates in incomparable ways” | 既有工作在成本与成功率的算法上**互不可比**。 | sources/U30_jailbreakbench.md:10 |
| 50 | “it expands the available attack surface, as GAI itself is vulnerable to attacks like prompt injection or data poisoning.” | 它扩大了攻击面，因为生成式 AI 本身就可能遭受提示注入或数据投毒之类的攻击。 | sources/U33_nist-ai-600-1.md:529-531 |
| 51 | “Similarly, jailbreaking or prompt engineering tests may not systematically assess validity or reliability risks.” | 同理，越狱或提示工程测试可能**无法系统性地评估**有效性或可靠性风险。 | sources/U33_nist-ai-600-1.md:2649-2651 |
| 52 | “These may provide supplementary assurance through a defense-in-depth philosophy.” | 这些可通过**纵深防御**的理念提供补充性保证。 | sources/U4_nist-ai100-2e2025.md:2788 |
| 53 | “Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention for prompt injection.” | 鉴于模型工作方式的核心存在随机性影响，**尚不清楚**提示注入是否存在万无一失的防范方法。 | sources/U5_owasp-llm01.md:28 |
| 54 | “Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files.” | 间接提示注入发生在 LLM 接受来自外部来源（如网站或文件）的输入时。 | sources/U5_owasp-llm01.md:16 |
| 55 | “we propose a new adversarial training method for robust refusal, called Robust Refusal Dynamic Defense (R2D2).” | 我们提出一种面向鲁棒拒绝的新对抗训练方法，名为 R2D2。 | sources/U12_harmbench-full.md:127 |

## 8. P2 自检记录

- **引文逐字回源**：`python3.12 .claude/scripts/note-citation-check.py workspace/ai-jailbreak --mode verbatim --file 02_deep_research.md` → 结果见下方「运行结果」。
- **数值重新计数**（回原文核对，非誊抄）：
  - U32：`86% → <5%`（全文 :98）、`>95% vs 14%`（全文 :16）、`0.38%` / `23.7%`（摘要 :10）；**`4.4%` 已确认 0 处，弃用**。
  - U12：`510（400 文本 + 110 多模态）/ 18 / 33`（原文 `510510 / 1818 / 3333` 为重影，取去重值）。
  - U7：`256` 段示范上限（:29）、`61% → 2%`（:44）。
  - U11：`1,405` 条 / `0.95` / `240+` 天（:10）。
  - U32 红队：`3,000` 小时（:10）。
  - R2D2：GCG 上 ASR `5.9%`，对比 Llama 2 7B Chat `31.8` / 13B Chat `30.2`（U12full:183）；`16 小时 / 8×A100`（:181）；MT-Bench `6.5 → 6.0`（:185）。
- **snippet-only / fetched**：本方向 B 依赖的来源**全部为 fetched**（已落盘 `sources/`）；无仅凭搜索摘要即当作证据的行。
- **安全边界**：全程只收机制/统计/防御；U7 的载荷示例已显式跳过；无攻击配方入库。

### 运行结果

命令与输出（2026-10-13 实跑，逐字誊抄）：

```
$ python3.12 .claude/scripts/note-citation-check.py workspace/ai-jailbreak --mode verbatim --file 02_deep_research.md
[V] 逐字回源：英文整句引文 109 处；原始来源命中 109 / 仅自己中间产物命中 0 / 未命中 0
    语料 34 个文件（primary 31 / derived 3）
判定：✅ 无硬失败（S1/S2/S3 是候选清单，仍需人工判）        EXIT=0

$ python3.12 .claude/scripts/note-citation-check.py workspace/ai-jailbreak --file 02_deep_research.md
[S1] 边界叠字候选：0 处
[S2] LCS 撞车候选（>= 5 个汉字）：0 处
[S3] 反引号外的相邻 ASCII 词串：0 处
[S4] 引文对照表结构：0 处不合格
[C] 多副本一致：0 份副本（P2 尚无 chapters/ 与组装件——C 在此阶段天然不可判定，故 mode=all 退出码 1 属预期）

$ python3.12 .claude/scripts/check-md-structure.py workspace/ai-jailbreak/02_deep_research.md
结构自检：扫描 1 个文件，发现 0 处可疑                        EXIT=0
```

**V 门修复记录（两处，均为本文件自身排版问题，非引文失真）**：

1. **反引号 span 包住整段引文 → 假阳性 weak 55 处**。原写法 `` `“…”` `` 让 `quotes_in_line()` 的反引号分支把「含引号的一整段」当成引文去回源，而弯引号 `“”` 不是语料里的字符 → 一律失配。改为**引文不再套反引号**（`“…”` 直接写，指针保持纯文本 `sources/f:NN`）后，109/109 全中。共去壳 62 处。
2. **U9 指针行号错 1 处**：`sources/U9_red-teaming-lms.md:25` → 真实位置 `:18`（该文件是长行 HTML 提取件，第 18 行即含该句；`:25` 是另一段）。
