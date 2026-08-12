---
title: "ModelScope 模型文件类型"
tags: [AI学习, 技术专题, LLM, ModelScope, 模型文件, GGUF, safetensors]
created: 2026-08-10
updated: 2026-08-11
status: 已完成
source_project: modelscope-model-file-types
---

# ModelScope 模型文件类型：看懂仓库、用对格式、选对路径

> [!info] 适用范围
> 本笔记面向「已经能照着部署指南用 ModelScope 下载 GGUF + Ollama 跑本地推理」的读者，补上被跳过的那半认知：一个模型仓库里到底有哪些文件、四种权重格式谁是谁、为什么缺了说明书跑不起来、拿到非 GGUF 原始权重该怎么用。看完你将能看懂任意一个模型仓库的文件列表，并为自己选对下载格式与使用路径。

## 目录

1. [第 1 章：一个模型仓库里到底有什么](#第-1-章一个模型仓库里到底有什么)
   - [1.1 仓库文件全景：四类文件的职责划分](#11-仓库文件全景四类文件的职责划分)
   - [1.2 ModelScope 仓库长什么样](#12-modelscope-仓库长什么样)
   - [1.3 原始仓库 vs GGUF 仓库](#13-原始仓库-vs-gguf-仓库)
   - [1.4 大白话：把模型仓库想成一家餐厅](#14-大白话把模型仓库想成一家餐厅)
2. [第 2 章：权重文件格式：safetensors / bin / gguf / onnx](#第-2-章权重文件格式safetensors-bin-gguf-onnx)
   - [2.1 母版与分发格式的核心分工](#21-母版与分发格式的核心分工)
   - [2.2 safetensors — 现代事实标准](#22-safetensors-现代事实标准)
   - [2.3 bin / pytorch_model.bin — 旧 pickle 格式](#23-bin-pytorch_modelbin-旧-pickle-格式)
   - [2.4 GGUF — 本地推理的单文件事实标准](#24-gguf-本地推理的单文件事实标准)
   - [2.5 ONNX — 跨框架部署中间层](#25-onnx-跨框架部署中间层)
   - [2.6 量化入门：为什么 GGUF 默认带量化档](#26-量化入门为什么-gguf-默认带量化档)
   - [2.7 大白话：生食材、预制菜与中央厨房](#27-大白话生食材预制菜与中央厨房)
   - [2.8 格式对比一张表](#28-格式对比一张表)
3. [第 3 章：配置与分词器文件：模型的说明书](#第-3-章配置与分词器文件模型的说明书)
   - [3.1 config.json — 模型的结构蓝图（必需）](#31-configjson-模型的结构蓝图必需)
   - [3.2 tokenizer 系列 — 模型的语言翻译器（必需且与模型绑定）](#32-tokenizer-系列-模型的语言翻译器必需且与模型绑定)
   - [3.3 generation_config.json — 生成参数（可选）](#33-generationconfigjson-生成参数可选)
   - [3.4 model.safetensors.index.json — 分片索引（分片必需）](#34-modelsafetensorsindexjson-分片索引分片必需)
   - [3.5 README.md / model card — 文档与 Hub 元数据（仅文档）](#35-readmemd-model-card-文档与-hub-元数据仅文档)
   - [3.6 把加载顺序串成一条线](#36-把加载顺序串成一条线)
4. [第 4 章：拿到非 GGUF 文件怎么用：三条路径](#第-4-章拿到非-gguf-文件怎么用三条路径)
   - [4.1 路径 A：Transformers / ModelScope 直接推理](#41-路径-a-transformers-modelscope-直接推理)
   - [4.2 路径 B：转 GGUF 再喂 Ollama / llama.cpp](#42-路径-b-转-gguf-再喂-ollama-llamacpp)
   - [4.3 路径 C：vLLM 高并发生产](#43-路径-c-vllm-高并发生产)
   - [4.4 大白话：开餐厅的三种经营方式](#44-大白话开餐厅的三种经营方式)
   - [4.5 三条路径对比表](#45-三条路径对比表)
5. [第 5 章：怎么选、怎么避坑、怎么衔接既有指南](#第-5-章怎么选怎么避坑怎么衔接既有指南)
   - [5.1 选型决策：GGUF vs 原始权重](#51-选型决策-gguf-vs-原始权重)
   - [5.2 与既有部署指南的衔接](#52-与既有部署指南的衔接)
   - [5.3 常见坑清单](#53-常见坑清单)
   - [5.4 下一步延伸](#54-下一步延伸)
   - [全篇收束](#全篇收束)

---

## 第 1 章：一个模型仓库里到底有什么

你已经会用 `modelscope` 下载 GGUF 并配合 Ollama 跑本地推理了（见 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南]]），但有没有好奇过：为什么有些 ModelScope 仓库点进去全是 `.safetensors` 和一堆 `.json`，连个 GGUF 都找不到？为什么总有人说「只下权重跑不起来」？

这一章先建立一张全景地图：一个模型仓库里到底有哪些文件、每类文件负责什么。看完之后，你拿到任意一个仓库都能看懂文件列表，也就能回答「为什么只下权重跑不起来」。

### 1.1 仓库文件全景：四类文件的职责划分

不管在哪个平台，一个完整模型仓库里的文件都可以归成四类：

| 类别 | 代表文件 | 一句话职责 |
|------|----------|-----------|
| 权重 | `model.safetensors`、`model-00001-of-00004.safetensors`、`.gguf` | 真正干活的部分：模型学到的全部参数 |
| 配置 | `config.json`、`generation_config.json` | 结构蓝图：说明模型是什么架构、有多大 |
| 分词器 | `tokenizer.json`、`tokenizer_config.json`、`vocab.json` | 语言翻译器：把文本变成数字 ID、再把 ID 变回文本 |
| 文档 | `README.md`、`configuration.json` | 给人看的说明与平台元数据，不参与推理 |

关键点：权重只是「会算的大脑」，但没人告诉它自己是什么架构、输入长什么样。加载模型时，框架先读 `config.json` 搭骨架，再用分词器把文字转成 token ID，最后才把权重填进骨架。缺了配置或分词器，模型根本无法启动——这就是「只下权重跑不起来」的原因。

> [!tip] 大白话
> 把模型仓库想成一家餐厅：权重是食材，config 是菜谱，tokenizer 是切菜刀规格，README 是菜单。你光把食材搬回家，没有菜谱不知道该怎么做、没有刀不知道切多大块——当然开不了张。1.4 节我们会把整个比喻完整展开。

### 1.2 ModelScope 仓库长什么样

ModelScope 上每个模型有一个唯一 ID，格式是 `org/model-name`，例如 `Qwen/Qwen2.5-7B-Instruct`：`org` 是机构或用户名，后面是模型名。仓库本身用 git + git-lfs 托管——大文件（权重）走 LFS 存储，小文件（配置、文档）走普通 git，所以下载时能按文件名精确匹配。

这里有个容易踩的坑：ModelScope 的**平台级**元数据文件叫 `configuration.json`（注意不是 `config.json`），它记录 framework / task / pipeline 等平台信息，是「正式发布」的必填项；而 `config.json` 是模型自身的架构超参。两者分工完全不同：

- `configuration.json`：给 ModelScope 平台看的，缺失会导致模型一直停在「预发布」状态
- `config.json`：给模型加载框架（Transformers 等）看的，缺失会导致加载直接报错

> [!tip] 大白话
> `configuration.json` 是给「商场」（ModelScope 平台）看的入驻信息，`config.json` 是给「食客」（加载框架）看的菜谱。你只传了菜谱、忘了入驻信息，商场不会把你正式上架（停在预发布）；反之只上架了却没有菜谱，食客来点菜就报错。

### 1.3 原始仓库 vs GGUF 仓库

同一个模型在 ModelScope 上通常有两种仓库形态：**原始仓库**（如 `Qwen/Qwen2.5-7B-Instruct`）和 **GGUF 仓库**（官方会在末尾加 `-gguf` 后缀，如 `Qwen/Qwen2.5-7B-Instruct-gguf`）。先看下载命令：

```bash
# 下载原始权重仓库（全部文件）
modelscope download --model Qwen/Qwen2.5-7B-Instruct --local_dir ./models/Qwen2.5-7B

# 只下载 GGUF 仓库里某个量化档的所有分片（--include 按名字过滤）
modelscope download --model Qwen/Qwen2.5-7B-Instruct-gguf \
  --include 'qwen2.5-7b-instruct-q4_k_m*' --local_dir .
```

下载完用 `ls -R`（或文件管理器）查看，两个仓库的文件清单长这样：

```text
原始仓库 Qwen/Qwen2.5-7B-Instruct/
├── configuration.json                 # 平台元数据（正式发布必填）
├── config.json                        # 模型架构蓝图
├── generation_config.json             # 生成参数
├── model.safetensors.index.json       # 分片索引：每个张量在哪个分片
├── model-00001-of-00004.safetensors   # 权重分片 1/4
├── model-00002-of-00004.safetensors   # 权重分片 2/4
├── model-00003-of-00004.safetensors   # 权重分片 3/4
├── model-00004-of-00004.safetensors   # 权重分片 4/4
├── tokenizer.json                     # 完整分词管线
├── tokenizer_config.json              # 分词器参数
├── vocab.json / merges.txt            # 词表与 BPE 合并规则
├── special_tokens_map.json
└── README.md
```

```text
GGUF 仓库 Qwen/Qwen2.5-7B-Instruct-gguf/
├── configuration.json
├── qwen2.5-7b-instruct-q2_k.gguf       # 极低比特量化档
├── qwen2.5-7b-instruct-q4_k_m.gguf     # 推荐默认档
├── qwen2.5-7b-instruct-q5_k_m.gguf
├── qwen2.5-7b-instruct-q8_0.gguf       # 近无损档
└── README.md
```

对比一下就能发现：GGUF 仓库「干净」得多——没有 `config.json`、没有 tokenizer 系列、没有分片 index。因为 GGUF 是**自包含**格式：权重、架构元数据、tokenizer、chat template 全部内嵌进单个 `.gguf` 文件里了。它文件少，不是缺东西，而是东西都合在一处。

识别 GGUF 命名有个规律，官方遵循 llama.cpp 规范：

```text
<模型名>-<版本>-<参数规模><量化档>(-<分片>).gguf
例： qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf
     └─模型┘└参┘└版本┘ └─量化档─┘ └─────分片─────┘
```

量化档是固定后缀（`q2_k`、`q4_k_m`、`q8_0` 等），一眼就能看出这是哪个压缩档位；分片用 `-00001-of-000NN` 标注。所以看到「`-gguf` 后缀 + 一堆 `.gguf` 文件 + 量化档标签」，基本就能断定这是 GGUF 仓库。

> [!tip] 大白话
> GGUF 是「预制菜」：食材、菜谱、刀具规格都给你打包进一个袋子，开袋即食。原始仓库是「生鲜市场」：食材（权重）、菜谱（config）、刀具规格（tokenizer）分开卖，你得全买齐才能做菜。

### 1.4 大白话：把模型仓库想成一家餐厅

把整章串起来看：一个模型仓库，就是一家想开张的餐厅。

> [!tip] 大白话
> | 餐厅 | 仓库文件 | 作用 |
> |------|----------|------|
> | 食材 | 权重 `model.safetensors` | 真正被「做」的东西，模型学到的参数 |
> | 菜谱 | `config.json` | 决定用什么灶台、什么锅，结构怎么搭 |
> | 刀具规格 | `tokenizer` 系列 | 决定文本被切成多大块才合适喂进模型 |
> | 上菜节奏 | `generation_config.json` | 决定一次出多少菜、火候（temperature）怎么调 |
> | 菜单 | `README.md` | 给顾客看的说明，不参与做菜 |
> | 入驻信息 | `configuration.json` | 给平台看的，没有就没法正式开业 |

权重相当于「会做菜的厨师」，但厨师再厉害，没有菜谱不知道该做成什么菜，没有刀不知道食材切多大，连顾客点什么都听不懂（没有分词器）。这四类文件各司其职，缺任何一样餐厅都开不了张——对应到技术世界，就是模型加载直接报错。

### 本章小结

- 一个模型仓库 = 权重 + 配置 + 分词器 + 文档四类文件；权重只是「会算的部分」，缺配置/分词器模型无法加载
- ModelScope 仓库 ID 是 `org/model-name`，git-lfs 托管；平台级 `configuration.json` 与模型级 `config.json` 分工不同，前者缺失会一直停在「预发布」
- 原始仓库（safetensors 分片 + config + tokenizer 系列）和 GGUF 仓库（自包含 `.gguf` + 量化档）的文件清单差异明显
- GGUF 命名规范 `<模型名>-<版本>-<参数规模><量化档>.gguf` 可一眼识别量化档位与分片
- 餐厅比喻：权重=食材、config=菜谱、tokenizer=刀具规格、generation_config=上菜节奏、README=菜单

下一章，我们逐个拆解权重文件格式：safetensors、bin、gguf、onnx 各是什么、谁在用、彼此什么关系。

---

## 第 2 章：权重文件格式：safetensors / bin / gguf / onnx

上一章我们建立了「模型仓库 = 权重 + 配置 + 分词器 + 文档」四类文件的心智模型。这一章把目光聚焦在四类文件里最核心、也最让人在下载页犯迷糊的一类——权重文件。同样是「模型的脑子」，你会看到 `.safetensors`、`.bin`、`.gguf`、`.onnx` 一串后缀，它们各自是什么？谁在用？为什么有的仓库只给 GGUF、有的只给原始权重？这一章一次性讲清，让你下次面对下载列表时心里有数。

### 2.1 母版与分发格式的核心分工

先给一条贯穿全章的主线：**这四种格式不是竞争关系，而是分工关系**，分别对应模型生命周期的三个环节：

```text
训练存储（safetensors / bin，fp16/fp32 母版）
   → 本地运行（GGUF，量化单文件）
   → 云端部署（ONNX，跨框架中间层）
```

一个模型在 GPU 集群上训练完成后，首先产出的是高精度原始权重（通常 fp16 或 bf16）——这是「母版」。母版用途最广：供研究人员继续微调、做评测、被各种框架消费。但母版体积巨大、直接喂给本地推理引擎效率不高，于是有了面向本地运行的 GGUF；而要在异构服务器、不同推理引擎上稳定部署，又需要跨框架的 ONNX。理解了这个分工，后面每一种格式「为什么存在」就都顺了。

> 类比电影：母版是拍摄原片（画质最高、可任意剪辑），GGUF 是发到视频网站的压缩版（体积小、打开即播），ONNX 是灌录成不同播放器都能放的标准化碟片。

### 2.2 safetensors — 现代事实标准

**它是什么**：HuggingFace 主导的开源张量存储格式，Rust 内核 + Python 绑定，是当前大模型权重的事实标准。transformers 从 4.35 版起，`save_pretrained` 默认就输出它。

**为什么安全**：老格式权重是 Python pickle 序列化，反序列化时可能执行任意代码；[[safetensors]] 文件里只有纯数据和一段 JSON 头部，不含任何可执行操作码，天然杜绝了「打开文件 = 执行代码」的攻击面。

**为什么快**：safetensors 支持 mmap 内存映射，做到零拷贝、懒加载——只把需要的张量读进内存。官方数据：BLOOM 176B 的加载从 pickle 时代的约 10 分钟降到约 45 秒；CPU 场景快约 76 倍。[safetensors 官方](https://github.com/safetensors/safetensors)

**大模型怎么分片**：几十上百 GB 的权重会拆成多个文件，命名如 `model-00001-of-00006.safetensors`，并配一个 `model.safetensors.index.json` 索引，记录每个张量在哪个分片里。看到这种命名说明模型被分片存储了——下载时不能漏掉任何一个分片和索引文件。

> [!tip] 大白话
> 把 safetensors 想成一个**只装物品的保险箱**：里面满满当当全是数字（权重），没有任何机关，所以你可以放心打开、随手拿去加工。而下面要讲的 `.bin` 老保险箱，里面可能藏着一根「一开箱就触发」的引线——这就是两者最大的区别。

### 2.3 bin / pytorch_model.bin — 旧 pickle 格式

**它是什么**：`torch.save()` 的默认产物，本质是 pickle 序列化的 state dict。它是 transformers 生态的「前任默认权重格式」，在 safetensors 出现前几乎所有仓库都用它。

**安全风险**：pickle 在反序列化时允许实例化任意 Python 对象并执行钩子函数（`__reduce__`），所以「加载一个 `.bin` 文件」本身就是一次潜在代码执行点。JFrog 2024 年在 HuggingFace 上发现约 100 个恶意模型文件，约 95% 针对 PyTorch，相关漏洞 CVSS 评分最高达 9.8。[CERT 通报](https://kb.cert.org/vuls/id/252619)

**何时还会见到**：存量老仓库、老项目、某些非 transformers 的 PyTorch 权重。新发布模型基本不再生成 `.bin`。如果你在下载页同时看到 `.safetensors` 和 `.bin`，优先用 `.safetensors`；如果只有 `.bin`，加载时使用官方支持的 `weights_only=True` 安全模式，别在不可信来源上直接 `torch.load`。

> [!tip] 大白话
> `.bin` 是一个**带机关的快递箱**：你永远不知道拆箱的瞬间会触发什么。不是每个箱子都有机关，但正因为它可能藏机关，所以对来历不明的箱子要保持警惕。safetensors 就是把机关去掉、只留实物的新包装。

### 2.4 GGUF — 本地推理的单文件事实标准

**它是什么**：llama.cpp 团队推出的推理专用格式（2023 年取代旧的 GGML/GGJT），是本地大模型推理的事实标准。[GGUF 规范](https://github.com/ggml-org/llama.cpp/pull/3049)

**自包含是它的灵魂**：一个 [[GGUF]] 文件把权重、模型超参数、分词器、chat template 全部打包进同一个文件。这正是第 1 章提到的——GGUF 仓库里不需要单独的 tokenizer 文件，因为已经内嵌了。

**支持量化**：GGUF 内置 Q2~Q8 多档量化，能把模型压到原来的 1/4 甚至更小，这是它称霸本地推理的关键。你已经在用的 Ollama，以及 llama.cpp、LM Studio、Jan 等工具都原生加载 GGUF。

**与 safetensors 的关系**：一句话——GGUF 是「推理格式」而非「训练格式」。它只用于跑推理，不能直接拿来微调；量化后的 GGUF 理论上可转回 safetensors，但会有精度损失（Q4_0 档余弦相似度约 0.996，Q8_0 约 0.99998）。所以「原始权重 → 量化 GGUF」是单向加工关系。

> [!tip] 大白话
> GGUF 是**开袋即食的预制菜**：肉、菜、调料、烹饪说明全在一包里，倒进锅里加热就能吃。safetensors 是超市买回来的生食材——营养最全、想怎么做都行，但得自己会处理、占地方也大。如果你已经跟着 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南]] 跑通过 GGUF + Ollama，那其实就是一直在吃预制菜。

### 2.5 ONNX — 跨框架部署中间层

**它是什么**：2017 年由微软和 Facebook 发起、现归 LF AI 基金会管理的开放神经网络交换标准。它定义了一种通用的「带类型计算图」，让模型能在不同框架和推理引擎之间搬运。[ONNX Runtime](https://deepwiki.com/microsoft/onnxruntime)

**谁在用**：ONNX Runtime、TensorRT、OpenVINO 等生产级推理引擎。常见于服务端和边缘设备部署——比如把 PyTorch 训练的模型导出成 ONNX，再交给这些引擎加速执行，实现「训练一个框架、部署任意平台」。

**在本主题里的定位**：部署中间层——它既不像 safetensors 那样作为仓库分发格式，也不像 GGUF 那样面向本地量化推理。你在 ModelScope 下载页见到 `.onnx` 的机会相对少，主要出现在偏部署导向的仓库里。概念入门阶段，知道它是「第三种用途」即可。

> [!tip] 大白话
> ONNX 像**中央厨房的标准化半成品**：按统一规格做好，贴上不同餐厅的标签就能上各家餐桌。训练方不用管你用什么设备跑，部署方也不用管模型原来是哪个框架训练的。

### 2.6 量化入门：为什么 GGUF 默认带量化档

量化，通俗说就是**用更少的比特数去表示每个权重数字**。权重数字的精度直接决定文件体积：

| 精度          | 每参数字节  | Llama-3 8B 体积 |
| ----------- | ------ | ------------- |
| FP32        | 4 字节   | ~32 GB        |
| FP16 / BF16 | 2 字节   | ~16 GB        |
| INT8        | 1 字节   | ~8 GB         |
| INT4        | 0.5 字节 | ~4 GB         |

safetensors 默认存 fp16/fp32 的「母版权重」，保留训练精度，供微调、评测、跨框架消费；而 GGUF 把量化做成内建的一级功能，同一份权重可以产出多个量化档位。

> [!note] 澄清：上表的 INT4 和文件名里的 Q4_K_M 是一回事吗？
> 上表 `FP32/FP16/INT8/INT4` 是**讲概念用的粗略位数**；GGUF 文件名里的 `Q2~Q8`（如 `q4_k_m`、`q8_0`）才是**真实实现档位**。两者量级对应——`INT8 ≈ Q8_0`、`INT4 ≈ Q4_K_M`——但实现不是「把每个数砍成整数」那么简单：
> - GGUF 用**分块量化**：权重按小组（如 32 个一组）分块，每组额外存一个浮点 `scale`，组内数值只存相对比例，还原时乘回 scale，有效精度比裸 INT4 高很多。
> - **K-quant**（`Q4_K_M` 里的 K）更进一步：块内混合精度，重要权重给 6 bit、其余给 4 bit。
>
> 一句话：**Q4 大致等于 INT4 的体积档，但质量更好**；Q2~Q8 就是「同一份权重压到 2~8 bit 的各档位」，其中 Q4_K_M 是体积与质量最平衡的甜点档。

**各档怎么取舍**：INT8 近无损（质量保留 99%+）；INT4 质量会降 1-3%，其中数学、代码类任务降幅比知识问答更明显，但换来体积只有原来的 1/4，CPU 也能流畅跑。因此 **Q4_K_M 是本地推理社区公认的「甜点档」**——体积与质量平衡最好（7B 参考：Q4_K_M 约 4.1GB；Q8_0 约 7.0GB，近无损）。[量化指南](https://vife.ai/blog/guide-llm-quantization-gguf-models)

> [!tip] 大白话
> [[量化]] 像**不同压缩程度的真空包装**：FP16 是原装整块肉，INT8 是切成普通片，INT4 是压得紧紧的脱水块——营养差一点，但体积小很多、携带方便。Q4_K_M 就是「压得比较狠但口感还在线」的那个推荐档。

> 提醒：量化后的 INT4 权重只能跑推理、不能训练。另外长上下文的 KV cache 通常仍以 FP16 常驻显存，显存占用可能比「权重体积」更大——这是第 4 章会涉及的话题。

### 2.7 大白话：生食材、预制菜与中央厨房

把四种格式放回生活场景，一套类比收拢全章：

- **safetensors / bin = 生食材**：保留全部营养（fp16/fp32 精度），可以任意加工（微调、评测、转格式），但体积大、需要自己处理。
- **GGUF = 预制菜**：按需压缩（量化档）、开袋即食（自包含、Ollama 直接加载），适合本地日常吃；代价是加工后不易再改回原样（有损）。
- **ONNX = 中央厨房标准化半成品**：为「运到哪都能上桌」而生的中间品，主要供服务端与边缘部署。

> [!tip] 大白话
> 一句话：**生食材想怎么做都行但费事，预制菜省事但定型了，中央厨房半成品是给规模化餐厅用的。** 选哪个，取决于你的厨房（硬件）和今天想做什么菜（目的）——这正是第 5 章选型决策的雏形。

### 2.8 格式对比一张表

| 维度 | safetensors | bin / pytorch_model.bin | GGUF | ONNX |
|------|------------|--------------------------|------|------|
| 精度 | fp16/fp32（母版） | fp16/fp32（母版） | 可量化 Q2~Q8 | 跟随导出时精度 |
| 安全 | 安全（无代码执行） | 危险（pickle） | 安全（纯数据+元数据） | 安全（纯图描述） |
| 用途 | 训练存储、微调、评测 | 老仓库存量权重 | 本地推理、分发携带 | 服务端/边缘部署 |
| 典型加载工具 | transformers / vLLM | torch.load | Ollama / llama.cpp / LM Studio | ONNX Runtime / TensorRT / OpenVINO |
| 是否可训练 | 是 | 是 | 否（只推理） | 否（推理引擎消费） |
| 是否自包含 | 否（需 config + tokenizer） | 否 | 是 | 部分（权重可外置） |

### 本章小结

- 四种权重格式是**分工关系**而非竞争关系：safetensors/bin 管「训练存储」、GGUF 管「本地运行」、ONNX 管「云端部署」。
- **safetensors** 是现代事实标准：安全（无 pickle 代码执行）、零拷贝加载快、大模型用分片 + index.json。
- **bin** 是旧 pickle 格式，有真实安全风险，只在存量仓库见到；优先用 safetensors。
- **GGUF** 是本地推理单文件标准：自包含（权重 + tokenizer + chat template 全内嵌）、内建量化，被 Ollama/llama.cpp/LM Studio 等加载；只推理、不可训练。
- 量化入门记三句话：每参数字节决定体积（fp32=4 → int4=0.5）、压缩越狠质量降越多、**Q4_K_M 是默认推荐档**。

下一章，我们把目光从「权重」转向「说明书」：config.json、tokenizer 系列、generation_config 这些权重之外的必需文件，逐个讲清它们为什么不可或缺。

---

## 第 3 章：配置与分词器文件：模型的说明书

上一章讲完四种权重格式（safetensors / bin / gguf / onnx），现在把目光转向权重之外的「说明书」文件。权重是模型学到的全部参数，但如果你只拿到一堆 `.safetensors`，加载框架根本不知道这些数字该怎么摆放——它需要一份结构蓝图告诉它模型是什么架构、有几层、每层多宽，还需要一个翻译器把人类文字变成模型认识的数字。这一章逐个讲清 `config.json`、tokenizer 系列、`generation_config.json`、分片索引和 README 各自的作用，以及为什么缺了它们模型会直接报错。

### 3.1 config.json — 模型的结构蓝图（必需）

`config.json` 是整个仓库里最先被读取的文件，作用一句话概括：告诉加载框架「这个模型是什么架构、长什么样」。它是纯 JSON 文本，可以直接用编辑器打开。常见字段如下：

| 字段 | 作用 | 例子 |
|------|------|------|
| `architectures` | 指定用哪个模型类 | `["Qwen2ForCausalLM"]` |
| `model_type` | 架构族标识，AutoConfig 的路由键 | `qwen2`、`llama` |
| `hidden_size` | 隐藏状态维度（d_model） | `3584` |
| `num_hidden_layers` | Transformer 层数 | `28` |
| `num_attention_heads` | 注意力头数 | `28` |
| `vocab_size` | 词表大小，同时是 embedding 矩阵第一维 | `152064` |
| `max_position_embeddings` | 位置编码最大序列长度（上下文窗口上限） | `32768` |
| `rope_theta` | RoPE 基础频率，影响长上下文外推 | Qwen2.5 用 `1000000`，Llama 默认 `10000` |
| `bos/eos/pad_token_id` | 特殊 token 的 ID | — |

加载时，`AutoConfig` 会**先读 `config.json`**：用 `model_type` 选对 Config 类，用 `architectures` 实例化对应模型类，按 `hidden_size`、`num_hidden_layers` 等维度把网络骨架搭起来——**最后才把权重填进骨架**。这个顺序很关键：权重只是一堆「裸张量」，没有 config 就不知道该往哪儿填，也不知道该用哪套类去加载。

所以 `config.json` 缺失的后果是**直接抛错**，报错信息长这样（含义很直白：找不到结构蓝图，无法推断架构类与维度）：

```text
OSError: Can't load config for './models/Qwen2.5-7B':
No such file or directory (config.json not found)
```

> [!tip] 大白话
> `config.json` 就是菜谱：它不负责做菜，但决定了「用什么锅、开多大火、先放什么后放什么」。没有菜谱，哪怕你有顶级食材（权重）也只能干瞪眼——报错就是厨师摊手说「我不知道这道菜该怎么做」。

[huggingface.co/docs/transformers/main_classes/configuration](https://huggingface.co/docs/transformers/main_classes/configuration)

### 3.2 tokenizer 系列 — 模型的语言翻译器（必需且与模型绑定）

模型不认识文字，只认识数字。分词器（tokenizer）负责把一段文字切成 token 并分配数字 ID，推理结束后再把 ID 拼回文字。和 config 一样，它是**必需**的——没有它，模型连输入都读不进去。

tokenizer 不是一个文件，而是一组文件（家族图谱）：

| 文件 | 职责 | 何时出现 |
|------|------|----------|
| `tokenizer.json` | Fast 分词器完整自包含状态：词表 + merge 规则 + 整条处理管线 | 现代模型基本都有 |
| `tokenizer_config.json` | 配置参数，不含词表：`tokenizer_class`、`model_max_length`、`chat_template` | 必需 |
| `vocab.txt` | Slow 分词器词表，一行一个 token，第 N 行 = token ID N | WordPiece/BERT 系 |
| `vocab.json` | `{"token": id}` 字典 | BPE 系 |
| `merges.txt` | BPE 合并规则：相邻子词如何按序合并 | BPE 系 |
| `special_tokens_map.json` | 登记特殊 token 字符串（bos/eos/pad/unk） | 常见 |

为什么要一整个家族？因为有两条实现路径：**Fast**（`tokenizer.json`，Rust 写的完整管线，现代默认）和 **Slow**（用 `vocab.json` + `merges.txt` 等散件现场重建）。加载时优先找 `tokenizer.json`，找不到就退回用散件重建。[huggingface.co/docs/transformers/tokenizer_summary](https://huggingface.co/docs/transformers/tokenizer_summary)

**「必须匹配」原理**是这个家族里最重要的一条。模型的 embedding 矩阵有 `vocab_size` 行，每一行对应一个 token ID。分词器把文字切成 token 并分配 ID，加载后模型就把 ID 当**行号**去取对应向量——也就是说，token 和 ID 之间的映射必须和训练时完全一致。

换错分词器会怎样？同一个 ID 指向了不同的文本，模型「以为」输入是别的意思，输出自然变成乱码。更隐蔽的是：**光看 `vocab_size` 相同不够**——大小一样不代表映射顺序一样，必须是同一套 token→ID 映射。这正是「tokenizer 必须与模型绑定」的原因。[theneuralbase.com](https://theneuralbase.com/)

> [!tip] 大白话
> 分词器就是把文字切成「标准食材块」的刀。不同模型用不同的刀（分词算法），切出来的块大小和编号都不一样。你拿切五花肉的刀去切刺身，编号对不上，做出来的菜就全乱了——这就是换错分词器输出乱码的原因。

### 3.3 generation_config.json — 生成参数（可选）

`config.json` 描述「模型是什么结构」，`generation_config.json` 描述「生成文本时怎么出结果」。两者分工不同，后者只在调用 `model.generate()` 时才被读取。

| 字段 | 作用 | 默认值 |
|------|------|--------|
| `max_new_tokens` | 最多生成多少新 token（推荐用这个） | 无（框架默认约 20） |
| `temperature` | 采样温度，越高越随机 | 1.0 |
| `top_k` | 只从概率最高的 k 个 token 里采样 | 50 |
| `top_p` | 累积概率阈值截断采样候选 | 1.0 |
| `repetition_penalty` | 重复惩罚，抑制「复读机」 | 1.0 |
| `do_sample` | 是否开启采样（False = 贪心解码） | False |

它的关键特点是**可选**：缺失**不报错**，会回落默认值（贪心解码、最多约 20 个 token、temperature=1.0）。所以很多仓库里看不到这个文件也正常——作者不提供，框架就用默认。[huggingface.co/docs/transformers/main_classes/text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

> [!tip] 大白话
> `generation_config.json` 是「上菜节奏」：一次上几道菜（`max_new_tokens`）、是重口味还是清淡（`temperature`）、能不能回锅重复（`repetition_penalty`）。后厨（`generate()`）做菜时才看这张单子；没有就按默认节奏上。

### 3.4 model.safetensors.index.json — 分片索引（分片必需）

大模型权重太大，会拆成多个分片：`model-00001-of-00004.safetensors`、`model-00002-of-00004.safetensors`……此时必须有一个配套的 `model.safetensors.index.json`，记录「每个张量放在哪个分片」。

核心内容是 `weight_map`——一张「张量名 → 分片文件名」的对照表：

```json
{
  "weight_map": {
    "model.layers.0.input_layernorm.weight": "model-00001-of-00004.safetensors",
    "model.layers.28.input_layernorm.weight": "model-00002-of-00004.safetensors"
  }
}
```

加载时框架先读 index.json，按 `weight_map` 把张量分组，再按需打开对应分片、逐张量装入。[huggingface.co/docs/safetensors/metadata_parsing](https://huggingface.co/docs/safetensors/metadata_parsing)

怎么判断单文件还是分片？仓库里只有 `model.safetensors`（没有 `-00001-of-` 这种命名）就是单文件，不需要 index；有多个 `model-XXXXX-of-NNNNN.safetensors` 就是分片，**必须有 index.json**。分片模型缺了它，`from_pretrained` 无法解析 shard，加载直接失败——社区里有大量真实案例，比如 unsloth#2355。[github.com/unslothai/unsloth/issues/2355](https://github.com/unslothai/unsloth/issues/2355)

> [!tip] 大白话
> 分片模型就像把一本书分成好几卷放在不同书架上，`index.json` 是索书号目录：哪个张量在第几卷。目录丢了，管理员（加载框架）找不到任何一卷的内容，书就借不出来——加载直接失败。

### 3.5 README.md / model card — 文档与 Hub 元数据（仅文档）

README 是**给人看**的，不参与任何加载逻辑。它的开头有一段 YAML frontmatter，包含 `license`、`pipeline_tag`、`tags`、`datasets`、`base_model`、`library_name` 等字段，这些会被 ModelScope / HuggingFace 平台解析成页面信息。[huggingface.co/docs/hub/model-cards](https://huggingface.co/docs/hub/model-cards)

缺失 README 完全不影响加载——模型照样能跑。它影响的是**可发现性**：没有它，别人（包括未来的你）不知道这个模型能干什么、用什么 license、怎么调用。你之前照着部署的 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南]]，很多关键信息就是从 model card 里读出来的。

### 3.6 把加载顺序串成一条线

把这一章的文件按加载顺序排一下，就是模型启动的完整过程：

```text
AutoModel 加载
  ① 读 config.json             → 定架构、搭骨架
  ② 读 model.safetensors
     （分片先读 index.json）    → 把权重填进骨架
AutoTokenizer 加载
  ③ 读 tokenizer_config.json   → 定分词器类
  ④ 按 tokenizer.json（或 vocab/merges）建分词器
generate() 时
  ⑤ 读 generation_config.json  → 决定怎么出文本
README.md → 全程不参与
```

对照第 1 章的餐厅比喻：`config.json` 是菜谱，决定用什么灶台和锅（结构）；tokenizer 是切菜刀规格，决定每块肉切多大（文本怎么切）；`generation_config.json` 是上菜节奏，决定一次出多少菜、火候怎么调（生成参数）。缺了菜谱（config）餐厅直接开不了张，缺了刀（tokenizer）没法切菜，上菜节奏没有就按默认节奏上。

> [!tip] 大白话
> 加载一个模型就像按菜谱做一桌菜：先看菜谱（`config.json`）确定用什么锅灶、做几道菜；再把每样食材按刀规格（tokenizer）切好、编号；食材（权重）按编号码进锅里；最后按上菜节奏（`generation_config.json`）一道道上。哪个环节的说明书丢了，这桌菜就做不成或做得不对。

### 本章小结

- `config.json` 是**必需**的结构蓝图：AutoConfig 先读它定架构、搭骨架，最后才装权重；缺失直接抛错
- tokenizer 是一个文件家族（`tokenizer.json` / `tokenizer_config.json` / `vocab.json` / `merges.txt` / `special_tokens_map.json`），必需且**必须与模型绑定**；embedding 按 token ID 当行号取向量，换错分词器 → 同一 ID 指向不同文本 → 乱码，光看 `vocab_size` 相同不够
- `generation_config.json` 是**可选**的生成参数（`max_new_tokens` / `temperature` / `top_k` / `top_p` / `repetition_penalty`），缺失不报错、回落默认
- `model.safetensors.index.json` 是分片索引，`weight_map` 记录「张量→分片」的映射；分片模型缺它直接加载失败
- README 是纯文档，不参与加载，只影响可发现性

下一章，我们带着这一章认识的「说明书」文件，去走通三条非 GGUF 使用路径：Transformers 直接加载、转 GGUF 喂 Ollama/llama.cpp、vLLM 生产部署。

---

## 第 4 章：拿到非 GGUF 文件怎么用：三条路径

前两章把文件本身讲完了：权重有四种格式，配置和分词器是模型的「说明书」。现在回答最实际的问题——你下载了一个只有 `.safetensors` 分片和一堆 `.json` 的原始仓库，里面没有现成的 GGUF，到底怎么把它跑起来？

其实原始权重有三条完全可走的路：直接用 Transformers 加载、转成 GGUF 喂给 Ollama/llama.cpp、丢给 vLLM 做生产服务。这一章三条路都给你可复制的命令，并讲清各自适合什么场景、有什么坑。还记得第 1 章的比喻吗？safetensors 是「生食材」，现在的问题就是：这袋生食材要怎么做成能上桌的菜。

### 4.1 路径 A：Transformers / ModelScope 直接推理

**适合**：跑通验证、做原型、抽 embedding、微调前检查模型能不能用。这是「成本最低、最快见到效果」的路。

第一步，把模型下载到本地。用 Python SDK 可以按后缀过滤，只下权重、配置和自定义代码：

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    local_dir="./models/Qwen2.5-7B",
    allow_patterns=["*.safetensors", "*.json", "*.py"],  # 只下权重+配置+自定义代码
)
```

第二步，加载并推理：

```python
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.bfloat16,  # 不传默认 fp32，7B 约 28GB 必 OOM
    device_map="auto",           # 显存不够自动溢到 CPU/磁盘
    trust_remote_code=True,      # 仓库有自定义 modeling_*.py 时必须开
)

messages = [{"role": "user", "content": "用三句话解释什么是 KV Cache"}]
inputs = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, return_tensors="pt"
).to(model.device)
out = model.generate(inputs, max_new_tokens=512, do_sample=False)
print(tokenizer.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True))
```

四个关键参数逐个说清 [Transformers 加载文档](https://huggingface.co/docs/transformers/main/en/main_classes/model)：

- `torch_dtype`：权重精度。不传默认 fp32（每参数 4 字节），7B 就要约 28GB 显存，小卡直接 OOM；设 `bfloat16` 减半到约 14GB。
- `device_map="auto"`：让框架自动分配 GPU/CPU 甚至磁盘，显存不够时「溢出」到 CPU 而不是崩掉。
- `trust_remote_code=True`：有些模型的架构不在官方框架里，仓库自带 `modeling_*.py` 自定义代码，不开这个开关会报 KeyError / 找不到模型类。
- `local_files_only=True`：纯离线环境加上它，强制只用本地文件、绝不联网（ModelScope 与 HuggingFace 布局互通，下载到本地后可离线加载）。

**坑**：
- 忘 `torch_dtype` → OOM，这是最经典的入门坑。
- 有自定义代码没开 `trust_remote_code` → KeyError，属于「静默错误」，报错不明显。
- 吞吐低、无并发：一次只能处理一个请求，不适合服务多人。

> [!tip] 大白话
> `torch_dtype` 就像决定用多大的盘子装菜：默认 fp32 是「豪华大盘」，7B 的菜光装盘就要占 28GB 桌位，小桌（小显存）一摆就爆；换成 bfloat16 就是「精简餐盘」，占位减半。所以新手最常犯的错，就是忘了换小盘直接 OOM。

> [!tip] 大白话
> `trust_remote_code` 相当于「允许厨师用私房菜谱」。有的模型用了框架之外的独门手艺（仓库里的 modeling_*.py），你不点头，餐厅管理员（框架）就拒绝让这位厨师开工，报 KeyError。开之前最好瞄一眼这份菜谱，确认没下毒——毕竟是要执行里面的代码。

### 4.2 路径 B：转 GGUF 再喂 Ollama / llama.cpp

**适合**：本地个人长期用、老机器、边缘设备、想压缩显存占用。这是把「原材料」加工成「预制菜」的完整链路。

先转成 FP16 GGUF，再量化成 Q4_K_M（内存压到约 1/4）：

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
pip install -r requirements.txt

# 转换：safetensors 目录 → FP16 GGUF
python convert_hf_to_gguf.py ./models/Qwen2.5-7B-Instruct \
    --outfile ./models/Qwen2.5-7B-f16.gguf \
    --outtype f16 \
    --model-name "Qwen2.5-7B-Instruct"

# 量化：FP16 GGUF → Q4_K_M GGUF
cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release
./build/bin/llama-quantize \
    ./models/Qwen2.5-7B-f16.gguf \
    ./models/Qwen2.5-7B-Q4_K_M.gguf \
    Q4_K_M
```

转完就能像平时一样喂给 Ollama（Modelfile 指向你的 GGUF 文件，然后 `ollama create` + `ollama run`），走你熟悉的既有部署链路。

**更省事的替代：让 Ollama 直接 FROM safetensors 目录**，前提是模型架构在 Ollama 的白名单里 [Ollama 导入文档](https://docs.ollama.com/import)：

```bash
# Modelfile:
#   FROM ./models/Qwen2.5-7B-Instruct
#   PARAMETER temperature 0.7
#   PARAMETER num_ctx 8192
ollama create my-qwen -f Modelfile
ollama run my-qwen
# 或一步到位直接量化：ollama create my-qwen-q4 -f Modelfile --quantize q4_K_M
```

两个认知修正（网上很多旧教程会误导你）[convert_hf_to_gguf.py](https://github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py)：

1. **当前版本 `convert_hf_to_gguf.py` 已经没有 `--vocab-type` 参数了**，词表类型会自动识别；低比特量化（Q4_K_M）走 `llama-quantize`，`--outtype` 最低只到 q8_0。
2. **Ollama 的「FROM safetensors 目录」只支持 Llama（含 2/3/3.1/3.2）、Mistral（含 Mixtral）、Gemma（1/2）、Phi3 这四类架构**。Qwen2.5 不在名单里，直接 `FROM` 一个 Qwen 的 safetensors 目录会失败——必须先自己走一遍 convert + quantize。

**坑**：转换脚本对超新/冷门架构可能报错；大模型转换内存不足加 `--use-temp-file`；GGUF 分片 Ollama 不支持，需先用 `gguf-split` 合并。

> [!tip] 大白话
> 把 Ollama 想成一家只跟固定几家供应商签约的中央厨房：它愿意直接加工 Llama、Mistral、Gemma、Phi3 的「半成品」（safetensors 目录），但 Qwen 没签约——Ollama 不敢乱接单。这时你得自己先把 Qwen 做成标准预制菜（转成 GGUF），它才肯收。

### 4.3 路径 C：vLLM 高并发生产

**适合**：正式对外服务、多用户并发、长上下文、多卡部署。投入最大但吞吐最高。

```bash
pip install vllm

vllm serve ./models/Qwen2.5-7B-Instruct \
    --load-format safetensors \   # 显式指定，跳过自动探测
    --dtype bfloat16 \
    --max-model-len 32768 \       # 总上下文窗口
    --gpu-memory-utilization 0.9 \
    --tensor-parallel-size 1 \    # 多卡时 = 卡数
    --port 8000
```

启动后用 OpenAI 兼容接口验证 [vLLM serve 文档](https://docs.vllm.ai/en/latest/cli/serve.html)：

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "./models/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "你好"}]}'
```

**为什么 vLLM 喂的是 safetensors 而不是 GGUF？**这是很多人的直觉困惑，但原因很实际：vLLM 的核心竞争力是 PagedAttention 和 continuous batching，这些高性能内核都是为**原生 HF/safetensors 权重**设计的。GGUF 里的 K-quants/IQ-quants 量化是 llama.cpp 系的格式，vLLM 要加载就得先在 meta-device 上建一个假模型做张量名映射，再写几千行 CUDA 反量化内核——工程上既脆弱又难维护。所以 vLLM 官方把内置 GGUF 支持标记为**实验性**并下放给了外部插件 [RFC #39583](https://github.com/vllm-project/vllm/issues/39583)。实践结论：vLLM 吃 safetensors，想省内存就用 GPTQ/AWQ 原生量化，不走 GGUF。

**坑**：只下权重不下 `config.json` / `tokenizer.json` 是最高频的启动失败原因（还记得第 3 章说的「缺说明书加载不了」吗）；模型过新会报 architecture not supported；CUDA illegal memory access 多由显存不足或驱动引起。

### 4.4 大白话：开餐厅的三种经营方式

三条路径的分工，用第 1 章那家餐厅的比喻就能一次记牢：

> [!tip] 大白话
> | 路径 | 餐厅经营方式 | 特点 | 对应选择 |
> |------|--------------|------|----------|
> | A | 自家厨房现做 | 最灵活，客人点什么都能试，但一次只伺候一位、出菜慢 | 验证菜好不好吃、搞研发试菜 |
> | B | 中央厨房预制菜 | 便宜省事，小店面（老机器/小显存）也能开，适合外带 | 本地自用、长期个人用、分发携带 |
> | C | 连锁总店 + 高客流流水线 | 前期投入大（大显存/多卡），但能同时接很多桌 | 正式对外营业、多用户高并发 |
>
> 先想清楚「给谁吃（目的）+ 店开在哪（硬件）」，再决定用哪种经营方式。选对了，省心省钱；选错了，要么跑不动，要么浪费钱。

### 4.5 三条路径对比表

| 维度 | A：Transformers/ModelScope | B：转 GGUF → Ollama/llama.cpp | C：vLLM |
|---|---|---|---|
| 输入格式 | safetensors/bin 目录 | 先转 GGUF（或白名单内 Ollama 自动转） | safetensors 原生（GGUF 仅实验性） |
| 硬件要求 | 最低（CPU 可跑）；fp16 7B≈14GB | 最低（CPU 都能跑）；Q4 显存≈fp16 的 1/4 | 高：NVIDIA GPU，推荐 24GB+，多卡更佳 |
| 量化/省内存 | 仅靠 dtype | ✅ 强项：Q4_K_M 等 | GPTQ/AWQ（原生量化，不走 GGUF） |
| 吞吐 | 低：单流无并发 | 中低：单用户快 | 高：continuous batching + PagedAttention |
| 适合场景 | 跑通验证 / 原型 / 微调前 | 本地个人 / 老机器 / 边缘 / 分发携带 | 生产服务 / 多用户 / 长上下文 / 多卡 |
| 难度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**一句话选型**：先验证模型行不行 → A；自己电脑长期好用、吃配置低 → B（Qwen 等非白名单架构先手动转 GGUF）；正式多用户服务 → C。

### 本章小结

- 非 GGUF 的原始权重有三条可操作路径：Transformers 直接加载、转 GGUF 喂 Ollama/llama.cpp、vLLM 生产部署
- 路径 A 最快跑通验证，关键参数是 `torch_dtype`（防 OOM）、`device_map="auto"`、`trust_remote_code`（自定义代码必须开）
- 路径 B 把原材料加工成预制菜：`convert_hf_to_gguf.py` 转 FP16 → `llama-quantize` 压到 Q4_K_M；Ollama 白名单只有 Llama/Mistral/Gemma/Phi3，Qwen 要手动转
- 路径 C 适合高并发生产，vLLM 实践上喂 safetensors 而非 GGUF（PagedAttention 内核为原生权重设计，GGUF 支持被官方标为实验性）
- 选型看「目的 + 硬件」：验证用 A、本地长期用 B、正式服务用 C

下一章，我们把三条路径收束成一张决策地图，回答「什么时候该下 GGUF、什么时候该下原始权重」，再串起常见坑清单，并和你已有的 GGUF + Ollama 部署指南打通。

---

## 第 5 章：怎么选、怎么避坑、怎么衔接既有指南

前四章讲完了模型仓库里到底有哪些文件、权重格式各是什么、配置与分词器文件怎么读、拿到非 GGUF 文件有三条使用路径。这一章把它们收束成一张**决策地图**：什么时候该下 GGUF、什么时候该下原始权重、常见坑在哪里，以及这篇笔记和你已经会用的部署指南怎么打通。

### 5.1 选型决策：GGUF vs 原始权重

选型其实只需要回答两个问题：**你想拿来干嘛？你的硬件是什么？** 先看用途，再看跑不跑得动。

| 你的目的 | 该下什么 | 走哪条路径 | 为什么 |
|---------|---------|-----------|--------|
| 先验证模型行不行、跑个原型 | 原始权重（safetensors） | 路径 A：直接加载 | 最快看到效果，不折腾转换 |
| 本地个人长期用、机器配置不高 | 现成 GGUF | 路径 B：喂 Ollama/llama.cpp | 量化后体积小，CPU 也能跑 |
| 正式服务多用户、要高吞吐 | 原始权重（safetensors） | 路径 C：vLLM | PagedAttention 内核只认原生权重 |

两个关键提醒：

1. **「先验证」永远优先**：别一上来就花半小时转 GGUF。先用路径 A 直接加载原始权重确认模型效果，再决定要不要转。
2. **GGUF 也能自己造**：不是每个仓库都有人帮你转好 GGUF。找不到现成的，就下原始权重走路径 B 自己转（Qwen 这类不在 Ollama 白名单里的架构，尤其要手动转）。

> [!tip] 大白话
> 把选型想成买菜做饭：GGUF 是超市里处理好的**预制菜**，开袋即食、省事省火；safetensors/bin 是**生食材**，保留全部营养，但要加工熟了才能吃。急着确认口味 → 先买预制菜试一包；要长期自己做饭、还想按自己口味改 → 买生食材自己加工。所以「下 GGUF 还是下原始权重」，本质是「我要省事，还是要灵活」。

### 5.2 与既有部署指南的衔接

你已经会按 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南|ModelScope-Ollama-ClaudeCode 部署指南]] 下载 GGUF 配合 Ollama 跑本地推理（也见 [[Ollama 使用指南]]）。这篇笔记补的是它没讲的那一半认知：

- **GGUF 是「加工过的成品」**：tokenizer、聊天模板、量化全部内嵌在一个文件里，拿来即用，但它只能推理、不能继续训练。
- **safetensors/bin 是「原材料」**：精度完整、可任意加工，但必须配合 config.json 和 tokenizer 文件才能加载。
- **原材料有两条出路**：可以直接吃（路径 A，transformers 加载），也可以自己加工成 GGUF（路径 B，convert 脚本 + llama-quantize）。既有指南教的是「吃成品」，本篇教的是「看懂成分表 + 自己加工」。

还有一个互通要点：ModelScope 上的原始权重仓库保持 HuggingFace 兼容布局，下载到本地后可以用 transformers 的 `from_pretrained(本地目录)` 直接离线加载，不需要联网去 HF 重下。[ModelScope 与 HF 互通](https://blog.csdn.net/2303_80346267/article/details/146553014) 的前提是目录里有完整必需文件：config.json、权重分片及 index.json、tokenizer 系列。

> [!tip] 大白话
> 既有指南是「叫外卖」的手册——点单（下载 GGUF）→ 加热（Ollama 加载）→ 开吃。这篇笔记给你的是**看懂后厨**的能力：知道外卖是预制菜做的（GGUF）、后厨还有一堆生食材（safetensors/bin），你想自己开火（转 GGUF）或直接吃现成的（transformers 加载）都行。两份指南合起来，你既能叫外卖，也能自己下厨。

### 5.3 常见坑清单

这七个坑是实践里最高频的，遇到报错先对着查：

| # | 坑 | 现象 | 原因与解法 |
|---|-----|------|-----------|
| 1 | 下错格式 | 下了 safetensors 想喂 Ollama，报格式不支持 | GGUF 才是 Ollama/llama.cpp 的口粮；下错就去下 `-gguf` 后缀的仓库 |
| 2 | 缺配置文件 | `from_pretrained` 直接抛错 | 权重只是裸张量，缺 config.json 无法搭结构；用 `snapshot_download` 下全目录，别只挑权重文件 |
| 3 | 分片漏下 | 报找不到权重 / 解析失败 | 大模型拆成多个 `model-0000X-of-0000N.safetensors`，配套 index.json 是地图；漏下任何一个都加载失败 |
| 4 | tokenizer 不匹配 | 输出乱码 | 分词器必须和模型是同一套 token→ID 映射；换错分词器，同一 ID 指向不同文本，光看 vocab_size 相同不够 |
| 5 | 忘开 trust_remote_code | 报 KeyError / 找不到类 | 仓库带自定义 `modeling_*.py` 时必须开；不开是静默错误 |
| 6 | vLLM 只下权重 | 启动直接失败 | vLLM 也要 config.json / tokenizer.json；别只下 `.safetensors` 文件 |
| 7 | 校验默认关闭 | 静默加载损坏文件 | ModelScope SDK 下载默认不校验哈希（[`MODELSCOPE_ENABLE_DEFAULT_HASH_VALIDATION` 默认关](https://github.com/modelscope/modelscope/blob/master/modelscope/hub/utils/caching.py)）；关键文件可离线 `sha256sum -c` 自己验 |

> [!tip] 大白话
> 前四个坑可以想成**快递没验货就签收**：明明订的是整套拼图，结果少发了几片（分片漏下）、发错货（下错格式）、说明书丢了（缺 config）、送错图样（tokenizer 不匹配）——没验货，等拆开要拼时才傻眼。所以下载完先核对文件清单、必要时算一遍校验和，比报错后再排查省事得多。

### 5.4 下一步延伸

概念入门到这里就够了；如果你想继续深入，这四个方向是自然的下一站：

1. **量化原理深挖**：GGUF 各量化档（Q4_K_M、Q8_0）到底怎么压缩权重，质量损失从哪里来。
2. **GGUF 内部字节布局**：头部、元数据、张量数据的排列，看懂为什么它能单文件自包含。
3. **GPTQ / AWQ**：面向 GPU 的原生量化，是 vLLM 在生产环境省显存的正规军（替代 GGUF 在 vLLM 里的位置）。
4. **vLLM 多卡部署**：`--tensor-parallel-size` 跨卡并行，把吞吐再往上推。

### 本章小结

- 选型只看两件事：目的 + 硬件——验证用路径 A、本地长期用下 GGUF、生产多用户上 vLLM。
- GGUF 是成品、safetensors/bin 是原材料，两者不是竞争而是分工，原材料可自己加工成成品。
- 高频坑集中在「格式、配置、分片、分词器、远程代码、校验」六个词上，报错先对表查。
- 这篇笔记与既有部署指南互为补充：那篇教「吃成品」，这篇教「看懂成分表 + 自己加工」。

### 全篇收束

> [!summary] 全篇收束
> 到这儿，你已经从「会下载 GGUF 并跑通 Ollama」进阶到「看得懂任意一个模型仓库」：知道仓库里四类文件各管什么、权重四种格式谁是谁、缺文件为什么报错、拿到非 GGUF 文件有三条路径可走。下次再打开一个 ModelScope 仓库，你不再是看文件名瞎猜，而是能一眼分清权重、配置、分词器和文档，并为自己的目的选对那条路。这份认知，是以后玩转量化、微调、生产部署的地基。
