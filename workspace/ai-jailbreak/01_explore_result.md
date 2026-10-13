# AI 破甲（Jailbreak）· 探测结果（P1）

> 三个并行探测子代理，分别负责「定义与边界 / 为何可行 / 攻击分类与防御」三个透镜。
> 范围限定在**概念与防御**：攻击类目只记「机制一句话」，不含可执行载荷。
> 来源以 arXiv 论文、主要 AI 安全机构文档、NIST/OWASP 官方框架为主。

## 一、三条主线的合成结论

### 主线①：什么叫破甲（定义与边界）

- **核心定义**：让**已做安全对齐**的模型产出它被训练去拒绝的内容——即「**绕过护栏（bypass guardrails）**」。三种权威表述：① 绕过安全训练的输入 [U1]；②「为绕过护栏而构造并提交的提示」[U6]；③ NIST 的「以滥用为目的的直接提示注入」[U4]。给入门读者的降级口径：**破甲 = 让模型「说出」它本不该说的**。
- **破甲 ≠ 提示注入**：提示注入攻击的是**应用**（不信输入被拼进开发者指令并覆盖之），破甲攻击的是**模型自身的安全/拒绝行为** [U2][U16]。学界对包含关系不完全一致——Willison 与综述把它们并列为兄弟类 [U16][U13]，OWASP 与 NIST 把破甲当作**直接提示注入**的子类 [U5][U4]。共同根因是**指令没有强制优先级**（system / user / 第三方文本地位近乎相等）[U3]。**速记**：注入 = 让模型「做」它不该做的；破甲 = 让模型「说」它不该说的 [U3][U4][U13][U16]。
- **破甲 ≠ 红队**：红队是**防御方的方法论**（刻意诱发有害输出以发现/度量/降低风险），破甲指的是被发现的**攻击技术/产物** [U8][U9]。两种标准攻击形态：人工「手工」破甲（角色扮演、铺垫、密码、多轮）[U6][U11] 与自动/优化攻击（对抗后缀的梯度搜索、LM 生成攻击）[U10][U9]。红队是做法，破甲是它找到的东西，评测协议（ASR）把它们量出来 [U12]。
- **对齐 / 护栏 / 拒绝**：安全对齐是塑造模型默认行为（helpful/honest/harmless）的训练过程，主要靠 RLHF 与 Constitutional AI / RLAIF [U14]；「护栏」是更广的统称——模型级拒绝行为 + 系统级输入/输出过滤与政策 [U6][U18]。拒绝行为是可度量的一等行为（拒绝率、对无害请求的过度拒绝、攻击成功率 ASR），且由可识别的内部表征中介，并非深层语义属性 [U17][U12]。**关键后果**：对齐是**浅层、概率性**的，不是已解决的边界 [U15][U17][U12]。

### 主线②：为什么能破（对齐的固有局限）

- **对齐是学到的统计倾向，不是硬保证**：护栏来自有限的 SFT/RLHF/Constitutional-AI 数据，可被训练分布之外的输入削弱、遗忘或绕开 [U1][U14][U10]。
- **两大根因（Wei et al.）**：**竞争目标（competing objectives）**——模型的能力/指令遵循/有用性目标与安全目标冲突，能力常常胜出；**泛化不匹配（mismatched generalization）**——安全训练没有泛化到模型能力仍覆盖的领域（编码、非英语、长上下文）[U1][U10]。
- **指令优先级盲区**让提示级技巧生效：模型把 system/user/第三方文本当成几乎同等优先级，被注入或重框的文本能**覆盖**护栏指令，而不是从属于它 [U3]。
- **角色扮演/人格/假设框架**借用通用上下文学习：让能力强的模型学会一个「顺从人格」，多示例上下文按幂律放大——**更大更能干的模型往往更易被攻**，而非更难 [U7][U22][U21]。
- **对齐浅且低维**，小扰动即可抹掉：安全增益集中在输出前几个 token，拒绝由**接近单一内部方向**中介，故预填充、微调或优化的对抗后缀能压掉它而几乎不动其它能力 [U19][U17][U10]。
- **能力-安全权衡**（alignment/safety tax）：安全训练有代价；校准很难——安全调高 → 对无害提示过度拒绝（词法过拟合），有用性调高 → 破甲重开。防御者在帕累托前沿上取舍 [U24][U20][U21]。

### 主线③：如何破甲（攻击分类与原理）＋ 检测与防御

**攻击类目（只记机制，不含载荷）**

| 类别 | 机制一句话 | 为何有效 | 来源 |
| --- | --- | --- | --- |
| 角色扮演 / 人格化 | 让模型扮演「不受限」角色作答 | 「服从角色设定」的能力目标压倒安全目标 | [U1][U7] |
| 假设情境框架 | 把请求包进虚构/学术/假设场景 | 同类竞争目标：模型更愿完成情境任务而非拒绝 | [U1][U8] |
| 编码 / 混淆 | 用 Base64、密码、翻译、低资源语言替换敏感措辞 | 碰「泛化不匹配」：能解码，但安全训练没覆盖这些表示 | [U1][U28] |
| 多轮渐进升级 | 从无害问题起步，逐轮引用模型自身回答推高敏感度 | 步进式「登门槛」，每步都看似无害，跨轮累积绕过单轮判定 | [U27][U7] |
| 多示例攻击（many-shot） | 长上下文塞入大量「已照做」的伪造示范 | 借用模型自身的上下文学习能力，成功率随示例数幂律上升 | [U7] |
| 前缀 / 目标注入 | 诱导或强迫模型以肯定开头、压制拒绝话术 | 直接制造「竞争目标」，让生成延续顺从而非拒绝 | [U1][U8] |
| 迁移攻击（通用对抗后缀） | 优化出可跨提示/跨模型复用的对抗后缀 | 对抗样本在模型间迁移，属「对抗鲁棒性」缺口 | [U10][U8] |
| 自动化对抗优化 | 用另一模型/优化器迭代生成并打分改进 | 把人工红队变成可并行、低成本的搜索（PAIR / GCG） | [U26][U10] |

**检测与防御（分层）**

- **训练期**：安全对齐（RLHF / Constitutional AI 的 RLAIF）+ 对抗训练（如 HarmBench 的 R2D2）提升鲁棒拒绝；但单靠训练会留下失败模式，对未见表示/多轮攻击易失守 [U14][U12][U1][U7]。
- **运行期护栏**：独立分类器审核输入/输出——Llama Guard 同时做 prompt/response 判定 [U31]；Anthropic Constitutional Classifiers 由「宪法」生成合成数据训练，公开红队实测把越狱成功率 **86% → 4.4%**，代价约 **+23.7%** 算力与少量过度拒绝 [U32]。
- **提示级缓解**：对超长/多轮输入做 prompt 分类与改写；Many-Shot 论文报告此路把 ASR **61% → 2%**，是四条缓解路线中最有效的一条 [U7]。
- **评测基准**：AdvBench（500 有害行为）[U10]、HarmBench（标准化 ASR 协议 + 分类器判官）[U12]、JailbreakBench（100 行为 + 公开对抗提示库 + 排行榜）[U30]；**注意各基准 ASR 口径不同、部分结论不可直接横比** [U12][U30]。
- **治理框架**：OWASP 把 Prompt Injection 列为 **LLM01**，强调「没有完美缓解、需纵深防御」[U5]；NIST AI 600-1 把直接/间接提示注入列为 GenAI 独立风险并给出跨框架（OWASP/MITRE ATLAS）映射 [U33]。

## 二、来源总表（去重后，按首次出现编号）

| ID | 来源 | 机构/作者 · 年份 | 链接 |
| --- | --- | --- | --- |
| U1 | Jailbroken: How Does LLM Safety Training Fail? | Wei, Haghtalab, Steinhardt · NeurIPS 2023 | https://arxiv.org/abs/2307.02483 |
| U2 | Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Greshake et al. · ACM AISec 2023 | https://arxiv.org/abs/2302.12173 |
| U3 | The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions | Wallace et al. (OpenAI) · 2024 | https://arxiv.org/abs/2404.13208 |
| U4 | Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations (NIST AI 100-2e2025) | NIST / US+UK AISI · 2025 | https://csrc.nist.gov/pubs/ai/100/2/e2025/final |
| U5 | OWASP Top 10 for LLM Applications — LLM01: Prompt Injection | OWASP GenAI Security Project · 2025 | https://genai.owasp.org/llm-top-10/ |
| U6 | International AI Safety Report 2025 | Bengio et al. · 2025 | https://internationalaisafetyreport.org/publication/international-ai-safety-report-2025 |
| U7 | Many-Shot Jailbreaking | Anil et al. (Anthropic) · NeurIPS 2024 | https://www.anthropic.com/research/many-shot-jailbreaking |
| U8 | Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned | Ganguli et al. (Anthropic) · 2022 | https://arxiv.org/abs/2209.07858 |
| U9 | Red Teaming Language Models with Language Models | Perez et al. · 2022 | https://arxiv.org/abs/2202.03286 |
| U10 | Universal and Transferable Adversarial Attacks on Aligned Language Models (GCG) | Zou, Wang, Kolter, Fredrikson · 2023 | https://arxiv.org/abs/2307.15043 |
| U11 | "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on LLMs | Shen et al. · ACM CCS 2024 | https://arxiv.org/abs/2308.03825 |
| U12 | HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal | Mazeika et al. · ICML 2024 | https://arxiv.org/abs/2402.04249 |
| U13 | The Prompt Report: A Systematic Survey of Prompting Techniques | Schulhoff et al. · 2024 | https://arxiv.org/abs/2406.06608 |
| U14 | Constitutional AI: Harmlessness from AI Feedback | Bai et al. (Anthropic) · 2022 | https://arxiv.org/abs/2212.08073 |
| U15 | Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To! | Qi et al. · 2023 | https://arxiv.org/abs/2310.03693 |
| U16 | Prompt injection and jailbreaking are not the same thing | Simon Willison · 2024 | https://simonwillison.net/2024/Mar/5/prompt-injection-jailbreaking/ |
| U17 | Refusal in Language Models Is Mediated by a Single Direction | Arditi et al. · NeurIPS 2024 | https://arxiv.org/abs/2406.11717 |
| U18 | GPT-4 System Card / Model Spec | OpenAI · 2023–2024 | https://arxiv.org/abs/2303.08774 · https://model-spec.openai.com/ |
| U19 | Safety Alignment Should Be Made More Than Just a Few Tokens Deep | Qi et al. (Princeton/DeepMind) · 2024 | https://arxiv.org/abs/2406.05946 |
| U20 | OR-Bench: An Over-Refusal Benchmark for Large Language Models | Cui et al. · 2024 | https://arxiv.org/abs/2405.20947 |
| U21 | XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in LLMs | Röttger et al. · NAACL 2024 | https://arxiv.org/abs/2308.01263 |
| U22 | How Johnny Can Persuade LLMs to Jailbreak Them (Persuasion) | Zeng et al. · ACL 2024 | https://arxiv.org/abs/2401.06373 |
| U23 | Claude's Constitution | Anthropic · rev. 2026 | https://www.anthropic.com/news/claudes-constitution |
| U24 | Safety Tax: Safety Alignment Makes Your Large Reasoning Models Less Reasonable | Huang et al. · 2025 | https://arxiv.org/abs/2503.00555 |
| U25 | Jailbreak Attacks and Defenses Against LLMs: A Survey | Yi, Yang et al. · 2024 | https://arxiv.org/abs/2407.04295 |
| U26 | Jailbreaking Black Box LLMs in Twenty Queries (PAIR) | Chao et al. · NeurIPS 2023 | https://arxiv.org/abs/2310.08419 |
| U27 | Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack | Russinovich et al. (Microsoft) · USENIX Sec 2025 | https://arxiv.org/abs/2404.01833 |
| U28 | GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher | Yuan et al. · 2023 | https://arxiv.org/abs/2308.06463 |
| U29 | JailbreakZoo: Survey, Landscapes, and Horizons in Jailbreaking LLMs and VLMs | Jin et al. · 2024 | https://arxiv.org/abs/2407.01599 |
| U30 | JailbreakBench: An Open Robustness Benchmark for Jailbreaking LLMs | Chao et al. · NeurIPS 2024 D&B | https://arxiv.org/abs/2404.01318 |
| U31 | Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations | Inan et al. (Meta) · 2023 | https://arxiv.org/abs/2312.06674 |
| U32 | Constitutional Classifiers: Defending against Universal Jailbreaks | Anthropic Safeguards · 2025 | https://arxiv.org/abs/2501.18837 |
| U33 | NIST AI 600-1: Generative AI Profile (AI RMF) | NIST · 2024 | https://doi.org/10.6028/NIST.AI.600-1 |

> 注：U25（Jailbreak Attacks and Defenses Survey）与 U34（A Domain-Based Taxonomy of Jailbreak Vulnerabilities, arXiv:2504.04976）为分类学补充来源，正文引用时按需补编号。

## 三、方向菜单（供用户选择）

| 方向 | 覆盖 | 规模 | 适合 |
| --- | --- | --- | --- |
| A 概念优先 | 是什么 + 为什么 | ~3 章 / 0.8–1.0 万字 | 只想搞懂原理 |
| **B 三问均衡（推荐）** | 是什么 → 为什么 → 攻击分类与原理 → 检测与防御 → 术语/速查 | ~5 章 / 1.2–1.5 万字 | 正好对齐你问的三问 |
| C 安全工程视角 | 在 B 上把「防御」扩为独立重头（护栏/分类器/评测基准/治理映射） | ~6–7 章 / 1.8–2.2 万字 | 偏防御工程落地 |
