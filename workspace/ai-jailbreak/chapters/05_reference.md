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
| 80,000 / 1,000 / 600 | OR-Bench 的过度拒绝提示 / 硬例 / 有毒对照 | 见第 4 章引文 46、47 | sources/U20_or-bench.md:10 |
| 1,405 | 某研究分析的破甲提示条数（2022-12 至 2023-12） | 见第 3 章 | sources/U11_do-anything-now.md:10 |
| 少于 20 次查询 | PAIR 产出一次破甲所需的查询量级 | 见第 3 章 | sources/U26_pair.md:10 |
| 无 4.4% | 本手册明确**不使用**的数字 | 核不到原始出处，全文任何位置都不写 4.4% | — |

最后一行是硬规矩，不是笔误：**只要数字回不到原始出处，就不用**。写作与更新时若见到 4.4% 这个数，一律按「无出处」处理。

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
| 4.4% 这个数字 | 回不到原始出处 | 全文不采用，见 5.4 |
| 抓取件的叠字 | PDF 抽取导致 510510 / 1818 / 3333 / 1616 / 6.06.0 等 | 按真值写 510 / 18 / 33 / 16 / 6.0，见 5.4 |

## 引文对照（原文 / 中译 / 出处）

> 下表列出本章正文出现过的全部英文引文。出处列写 `sources/<文件>:<行号>`；`—` 表示该条没有独立来源件（本表本次无此情况）。其余术语的逐字原文见第 1、3、4 章各自的对照表。

| # | 原文（verbatim） | 中译 | 出处 |
| --- | --- | --- | --- |
| 54 | “Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files.” | 间接提示注入发生在 LLM 接受来自外部来源（如网站或文件）的输入时。 | sources/U5_owasp-llm01.md:16 |
