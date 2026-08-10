---
title: "Ollama 使用文档"
tags:
  - Ollama
  - 本地LLM
  - 学习笔记
  - 教程
created: 2026-08-10
updated: 2026-08-10
status: 已完成
source_project: ollama-usage
---

# Ollama 使用文档

> [!summary] 笔记概览
> 本笔记是「概念 + 实战」混合的 Ollama 入门到上手教程，面向零基础读者。你将学会：Ollama 是什么、如何安装并跑起第一个本地大模型、用 CLI 管理模型、用 API / OpenAI 兼容接口对接自己的程序、用 Modelfile 定制专属模型，以及避开最常见的四个坑。全程无需云端 API Key，数据不出本机。

## 目录

- [第一章：Ollama 是什么 & 为什么用](#第一章ollama-是什么--为什么用)
  - [1.1 一句话认识 Ollama：定位与核心卖点](#11-一句话认识-ollama定位与核心卖点)
  - [1.2 为什么用本地 LLM：与云端 API 对比](#12-为什么用本地-llm与云端-api对比)
  - [1.3 底层原理速览：llama.cpp、GGUF 与量化](#13-底层原理速览llamacppgguf-与量化)
  - [1.4 本章小结：Ollama 适合谁、不适合谁](#14-本章小结ollama-适合谁不适合谁)
- [第二章：安装与快速开始](#第二章安装与快速开始)
  - [2.1 安装前的准备：你的电脑需要什么](#21-安装前的准备你的电脑需要什么)
  - [2.2 分平台安装：四种方式选一种](#22-分平台安装四种方式选一种)
  - [2.3 首次运行：跑起第一个模型](#23-首次运行跑起第一个模型)
  - [2.4 默认路径与端口一览](#24-默认路径与端口一览)
- [第三章：CLI 命令与模型管理](#第三章cli-命令与模型管理)
  - [3.1 命令总览：一张表看懂 11 个命令](#31-命令总览一张表看懂-11-个命令)
  - [3.2 跑模型：run 的三种姿势](#32-跑模型run-的三种姿势)
  - [3.3 模型管理：pull / list / ps / rm / cp](#33-模型管理pull--list--ps--rm--cp)
  - [3.4 模型库与量化：怎么选模型](#34-模型库与量化怎么选模型)
- [第四章：进阶用法——API / OpenAI 兼容 / Modelfile / 环境变量](#第四章进阶用法api--openai-兼容--modelfile--环境变量)
  - [4.1 原生 HTTP API：Ollama 也是本地小服务器](#41-原生-http-apiollama-也是本地小服务器)
  - [4.2 OpenAI 兼容 API：用现成 SDK 无缝对接](#42-openai-兼容-api用现成-sdk-无缝对接)
  - [4.3 Modelfile：定制自己的模型](#43-modelfile定制自己的模型)
  - [4.4 环境变量：按需调整运行行为](#44-环境变量按需调整运行行为)
- [第五章：常见坑与最佳实践](#第五章常见坑与最佳实践)
  - [5.1 显存不足静默回退 CPU](#51-显存不足静默回退-cpu)
  - [5.2 下载慢 / 镜像 / 网络问题](#52-下载慢--镜像--网络问题)
  - [5.3 端口占用与跨设备访问](#53-端口占用与跨设备访问)
  - [5.4 安全与隐私：API 无认证怎么办](#54-安全与隐私api-无认证怎么办)
  - [5.5 最佳实践清单](#55-最佳实践清单)

---

## 第一章：Ollama 是什么 & 为什么用

第一次听说「在本地跑大模型」，你脑子里可能全是问号：模型到底从哪里来？我的电脑跑得动吗？为什么放着现成的 ChatGPT 不用，非要折腾本地？这一章用最通俗的语言回答三个问题：**Ollama 是什么、为什么值得用本地大模型、它底层大致怎么工作**。看完你就能判断：Ollama 到底适不适合自己。

### 1.1 一句话认识 Ollama：定位与核心卖点

Ollama 是一个**本地运行开源大模型的工具**。官方对它的定位是「用一行命令运行开源大模型」，而它的核心卖点可以浓缩成三句话：

1. **一条命令下载并运行模型**——不需要懂 Python、不需要手动配置 GPU，`ollama run` 就能把模型跑起来；
2. **数据不出本机**——模型在你自己的电脑上运行，聊天记录不经过任何第三方服务器；
3. **跨平台**——Windows、macOS、Linux 都能装，还支持 Docker 容器方式运行。

需要特别澄清一点：**Ollama 本身不是模型**。它不生产智商，只负责「把别人训练好的开源模型搬到你电脑上跑起来」。这些模型来自 llama、gemma、qwen、mistral、deepseek 等开源社区 [官方仓库 README](https://github.com/ollama/ollama)。

Ollama 还自带一个 REST API 和官方 Python/JavaScript 库，意味着你装好之后，不光能像聊天软件一样用，还能把它当成本地小服务器，让程序来调用（这一点到第 4 章会展开）。

> [!tip] 大白话
> 把 Ollama 想成一个**本地版「应用商店 + 运行时」**：商店负责下载模型（`ollama pull`），运行时负责在电脑上把模型跑起来（`ollama run`）。所以它就像手机上的应用商店 + 播放器二合一——你自己不生产应用，但能一键下载、一键打开。对用户来说，**你不需要关心模型是怎么装上、怎么运行的，Ollama 都替你搞定了**。

### 1.2 为什么用本地 LLM：与云端 API 对比

你可能已经在用 ChatGPT、Claude、通义这些「云端大模型」。它们和本地 Ollama 的本质区别在于：**模型跑在谁的地盘上**。云端模型跑在厂商的服务器上，你通过网页或 API 访问；本地模型跑在你自己的电脑上，用你自己的算力。

一张表看清两者的差异：

| 对比维度 | 本地 Ollama | 云端 API（ChatGPT / Claude / 通义等） |
|---------|------------|--------------------------------------|
| 隐私 | 数据不出本机，完全自己掌控 | 对话会上传厂商服务器，受其隐私政策约束 |
| 联网要求 | 拉取模型时需要网络，跑模型可断网 | 每次使用都必须联网 |
| 费用 | 免费，只花电费 | 按用量付费，或订阅会员 |
| 算力 | 自备，靠你的 CPU / 显存 / 内存 | 厂商的服务器，多贵的硬件也不用你操心 |
| 性能天花板 | 取决于本地硬件 | 取决于厂商，通常可用更大更强的模型 |
| 可控性 | 模型版本、参数、微调完全自己说了算 | 受平台限制，可定制空间小 |
| 上手门槛 | 需要装软件、懂一点命令行 | 打开网页就能用 |

核心权衡一句话：**本地 LLM 用「自备算力」换「隐私、离线、免费、可控」**。

- 想保护隐私、处理敏感内容 → 本地是明显优势；
- 断网、内网、出差没信号的场景 → 本地依然能用；
- 高频调用、担心 API 账单 → 本地一次投入，长期零费用；
- 但代价是：**性能取决于你的硬件**。没有好显卡也能跑，只是慢；想要顶级模型的聪明程度，本地一般达不到——开源模型和顶级云端闭源模型之间仍有差距 [官方快速开始](https://docs.ollama.com/quickstart)。

> [!tip] 大白话
> 用本地 LLM 就像**把 ChatGPT 搬回家**：断网也能用，聊天数据锁进自己的「保险箱」，钥匙只在你手里。所以云端是「住酒店」——方便省心，但你的东西都存在别人房间；本地是「住自己家」——什么都自己管，安全自由，但要自己打扫、自己交水电费。**它不保证比酒店更豪华，但保证完全属于你**。

### 1.3 底层原理速览：llama.cpp、GGUF 与量化

这一节不深入源码，只建立三个「心智模型」，帮你理解 Ollama 这台机器大致由哪几块组成：

**引擎（llama.cpp）**：Ollama 的底层推理引擎是 llama.cpp，由 Georgi Gerganov 发起的开源项目 [官方仓库 README](https://github.com/ollama/ollama)。它的最大贡献是让大模型能跑在「普通硬件」上——甚至只有 CPU 的老电脑也能跑，只是慢。它是 Ollama 的「发动机」。

**模型文件格式（GGUF）**：大模型训练完是一大坨权重数据，需要一个统一格式打包成单个文件，方便下载、分发、加载。GGUF 就是这个「打包盒」。你 `ollama pull` 下载到本地的，就是一个个 GGUF 文件。

**量化（quantization）**：模型的权重默认是 16 位浮点数（f16），体积巨大。量化把这些数字的精度压缩到更低位（比如 8 位、4 位），换来**体积更小、更省显存**，代价是质量略有损失。这就是为什么同一个模型会有 `f16`、`q8_0`、`q4_K_M` 等不同版本：

| 版本 | 体积 | 质量 | 典型用途 |
|------|------|------|---------|
| `f16` | 原版，最大 | 最准 | 显存充足、追求极致 |
| `q8_0` | 约 1/2 | 近无损 | 质量与体积平衡 |
| `q4_K_M` | 约 1/4 | 约 96% | 8GB 显存首选，性价比最高 |

> [!tip] 大白话
> 量化就像**照片压缩**：RAW 原图最清晰，但一张好几 MB；压缩成 JPEG 后细节略减，肉眼几乎看不出差别，体积却小得多。`q4_K_M` 就是「高清又不占空间」的平衡档——**牺牲一点点画质，换来能装进你电脑的尺寸**。这决定了你 8GB 显存到底能跑多大的模型（详细选型表留到第 3 章）。

### 1.4 本章小结：Ollama 适合谁、不适合谁

看完前三节，你已经能给自己做个判断了。对照这张选型表：

| 你的情况 | 适合本地 Ollama？ | 建议 |
|---------|------------------|------|
| 对话内容敏感，不想上传给任何厂商 | ✅ 非常适合 | 本地运行，数据完全不出本机 |
| 常驻内网 / 经常断网 / 出差无信号 | ✅ 非常适合 | 断网也能用的本地模型是刚需 |
| 高频调用，不想付 API 账单 | ✅ 适合 | 一次装好，长期零费用 |
| 想深度定制模型（改参数、微调） | ✅ 适合 | 本地全可控，可玩性高 |
| 追求当前最强的模型智商 | ⚠️ 看情况 | 开源模型与顶级云端仍有差距，跑重活建议云 API |
| 只有老电脑、没有独立显卡 | ⚠️ 可以但吃力 | 能跑，但只能选小模型，且速度慢 |
| 完全不想碰命令行 | ❌ 不太适合 | 安装和日常操作都离不开终端 / PowerShell |

### 本章小结

- **Ollama 是一个「本地跑开源大模型」的工具**，本身不是模型，一条命令即可下载并运行模型，数据不出本机，跨平台 [官方仓库 README](https://github.com/ollama/ollama)。
- **本地 vs 云端**：本地用「自备算力」换「隐私、离线、免费、可控」；云端省心但数据过手、按量收费 [官方快速开始](https://docs.ollama.com/quickstart)。
- **底层三件套**：llama.cpp 是发动机（让模型跑在普通硬件上）、GGUF 是打包盒（模型文件格式）、量化是照片压缩（减体积省显存，质量略降）。
- **选型结论**：隐私敏感、离线场景、高频低成本调用的人最适合；追求顶级能力、不想动手的人更适合云端。
- 模型库里的模型名和量化版本，可以到 [官方模型库](https://ollama.com/library) 提前逛逛，感受一下「应用商店」里有哪些货。

### 下一章预告

下一章我们开始动手：按你的系统把 Ollama 装好，并跑起第一个本地模型，亲眼看看「把 ChatGPT 搬回家」到底是什么体验。

---

## 第二章：安装与快速开始

上一章我们知道了 Ollama 是什么——一个能把开源大模型「一键拉回家」的本地运行时，数据不出本机，断网也能用。光说不练假把式，这一章我们就动手把它装到自己的电脑上，并跑起第一个本地大模型。整个过程不复杂：选一种安装方式，跑一条命令，然后开始聊天。

### 2.1 安装前的准备：你的电脑需要什么

在动手之前，先花一分钟确认你的电脑满足最低要求。Ollama 本身是个很轻的安装包，真正「吃硬件」的是后面要下载的模型，所以**系统要求很宽松，硬件要求看你想跑多大的模型**。

| 平台 | 最低系统要求 | 补充说明 |
|------|------------|---------|
| Windows | Windows 10 22H2 及以上 | 原生运行，**不需要 WSL**；安装包约占 4GB 磁盘，默认装到用户目录、无需管理员权限 |
| macOS | macOS Sonoma 14 及以上 | Apple Silicon（M 系列）支持 GPU 加速；Intel Mac 只能 CPU 运行 |
| Linux | 无特殊版本要求 | 安装脚本会自动注册为 systemd 服务，开机自启；NVIDIA 显卡需装 CUDA 驱动，AMD 显卡需装 ROCm 驱动 |
| Docker | 已装好 Docker Engine / Docker Desktop | 需要把 GPU 传给容器时，Linux 主机需额外装 `nvidia-container-toolkit` |

**硬件上**，官方和社区的经验是：内存（RAM）**8GB 起步**；如果想顺畅地跑一个 70 亿参数（7B）的量化模型，建议有 **8GB 显存**（VRAM）。显存不足也不会装不了，只是模型会被迫用 CPU 慢慢跑——这一点我们留到第 5 章详细讲。

> [!tip] 大白话
> 把「安装 Ollama」和「下载模型」想成两件事：**安装 = 给手机装一个应用商店**，几乎不占空间；**下载模型 = 在商店里下载一个大 App**，这个才占地方。所以装 Ollama 的电脑要求很低，但你想玩多大的模型，就要准备多大的「仓库」（内存/显存/磁盘）。

**磁盘建议**：一个 7B 量化模型约 4-5GB，更大的 70B 模型要几十 GB。建议至少预留 20GB 空闲磁盘，后面下载模型时心里有数。

### 2.2 分平台安装：四种方式选一种

Ollama 支持 Windows、macOS、Linux，也支持用 Docker 跑。你只需要按自己的平台选一种，照着敲就行。**[Ollama 官方快速开始](https://docs.ollama.com/quickstart) 是权威来源**，下面命令都来自官方文档。

#### Windows：三种方式任选

方式一，**命令行（推荐）**：打开 PowerShell，输入：

```powershell
winget install Ollama.Ollama
```

`winget` 是 Windows 自带的软件包管理器，装完还能用它更新。

方式二，**图形安装包**：去 [Ollama 下载页](https://ollama.com/download) 下载 `OllamaSetup.exe`，双击一路「下一步」即可。

方式三，**官方 PowerShell 脚本**（适合想一条命令搞定的同学）：

```powershell
irm https://ollama.com/install.ps1 | iex
```

> [!note] 关于 WSL
> 网上很多旧教程会让你先去装 WSL2 再装 Ollama——那是老黄历了。**Windows 版本现在原生支持 Ollama**，不需要 WSL，直接装即可。

#### macOS：拖拽式安装

去 [Ollama 下载页](https://ollama.com/download) 下载 `ollama.dmg`，打开后把 Ollama 图标拖进「应用程序」文件夹，和装微信一样简单。首次打开如果提示「来自互联网的 App」，在「系统设置 → 隐私与安全性」里点「仍要打开」即可。

#### Linux：一条 curl 命令

在终端执行：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

脚本会自动下载二进制文件并注册为 systemd 服务（服务名 `ollama`），装好后开机自启。NVIDIA 显卡用户记得先确认已装好 CUDA 驱动；AMD 显卡用户需要 ROCm 驱动。

#### Docker：最省心的「集装箱」方式

如果你已经在用 Docker，也可以直接拉官方镜像跑。这是我最推荐「想体验又不想污染系统」的人用的方式：

```bash
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

拆开解释一下：

- `-d`：后台运行（detach）
- `-v ollama:/root/.ollama`：把容器的模型目录挂载到一个叫 `ollama` 的卷上，**删容器不丢模型**
- `-p 11434:11434`：把容器内的 11434 端口映射到本机，让外部程序能访问
- `--name ollama`：给容器起名，方便后面 `docker exec` 操作

**想让容器用上显卡**，加一个参数（需先装 `nvidia-container-toolkit`）：

```bash
docker run -d --gpus=all \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

AMD 显卡用户则把镜像换成 ROCm 专用标签（如 `ollama/ollama:rocm`）。

> [!tip] 大白话
> 把 Docker 想成 **标准集装箱**——Ollama 连同它的运行环境（依赖库、配置）被整体打包进一个箱子里，箱子在任何「港口」（你的电脑、服务器、别人的机器）都能原样打开运行。所以「用 Docker 装 Ollama」不是把软件散装进系统，而是直接搬一个现成的箱子过来。**换电脑、删系统，都不会污染你原来的环境**，这也是它叫「隔离」的原因。

### 2.3 首次运行：跑起第一个模型

装好之后，先验证一下安装是否成功。打开终端（Windows 用 PowerShell，macOS/Linux 用终端），输入：

```bash
ollama --version
```

如果能看到类似 `ollama version 0.x.x` 的输出，说明安装成功。

#### 进入对话

接下来是最激动人心的一步——运行第一个模型。输入：

```bash
ollama run qwen2.5:7b
```

> [!note] 模型名以模型库实际为准
> 这里的 `qwen2.5:7b` 是一个常用示例名。模型名格式是 `名称:标签`，实际可用的名字以 [Ollama 模型库](https://ollama.com/library) 或你本机 `ollama list` 显示的为准。想先下载快一点的，可以把 7b 换成 `3b` 之类的小模型。

第一次运行时，Ollama 会先自动下载这个模型（几 GB，看网速可能要几分钟），下载完立刻进入对话界面，出现 `>>>` 提示符。这时就可以像聊天一样输入内容了：

```text
>>> 你好，请用一句话介绍你自己
你好！我是一个本地运行的开源大模型，我的名字叫 qwen2.5。很高兴认识你！

>>> 3 的平方根是多少？
3 的平方根约等于 1.732...

>>>
```

**退出对话**：输入 `/bye` 回车即可：

```text
>>> /bye
```

> [!tip] 大白话
> 把 `ollama run 模型名` 想成在 **应用商店里点「安装并打开」**——如果本地还没有这个模型，它会先自动下载；下载完立刻进入聊天界面。所以**第一次运行等得久是在下模型，第二次再跑就快多了**（模型已在本地）。

`run` 还有一种「单次提问」的用法，不进对话界面、直接给答案，适合写脚本或快速测试：

```bash
ollama run qwen2.5:7b "用一句话解释什么是 HTTP"
```

#### 验证已下载的模型

回到终端，执行：

```bash
ollama list
```

输出类似：

```text
NAME            ID              SIZE      MODIFIED
qwen2.5:7b      aea2b4e2e9a8    4.7 GB    2 minutes ago
```

看到这一行，说明模型已经躺在你本地了。`ollama list` 会一直记住它，下次 `ollama run qwen2.5:7b` 会秒开。

> [!note] Docker 用户怎么运行？
> 如果你是用 Docker 装的，进入容器里执行同样的命令即可：
> ```bash
> docker exec -it ollama ollama run llama3.2
> ```
> 外面想用 `ollama --version`、`ollama list` 的话，也要通过 `docker exec -it ollama ollama ...` 这样包一层。

### 2.4 默认路径与端口一览

最后，把几个「默认值」记在心里，后面排查问题和配置时会用到。

#### 模型都存在哪

Ollama 把下载的模型统一存在一个目录里（各平台默认位置不同）：

| 平台 | 模型默认存储路径 |
|------|-----------------|
| Windows | `C:\Users\<你的用户名>\.ollama\models` |
| macOS | `~/.ollama/models` |
| Linux | `/usr/share/ollama/.ollama/models` |
| Docker 容器内 | `/root/.ollama` |

> [!tip] 大白话
> 把模型存储目录想成 **书架**——Ollama 下载的每个模型都是一本「书」，全部放在这个书架上。想腾磁盘空间，就把不用的「书」从架子上抽掉（第 3 章的 `ollama rm` 就是干这个的）。

#### 服务端口 11434

Ollama 装好之后，其实是一个**常驻的本地小服务**，默认监听在：

```text
127.0.0.1:11434
```

- **11434** 是它的 HTTP API 端口，程序（包括第 4 章的 Python 脚本）都通过这个端口跟它通信
- **127.0.0.1** 表示「只允许本机访问」——这是安全的默认值，外面的人访问不到

不同平台的「服务」形态不一样：Windows/macOS 是后台应用，Linux 是 systemd 服务，Docker 是容器，但对外都是同一个 11434 端口。

> [!tip] 大白话
> 把端口 11434 想成 Ollama 的 **固定门牌号**——程序要跟 Ollama 说话，就对着这个门牌号敲门。前面的 `127.0.0.1` 是「本地地址」，相当于在门上写「只在自己家开门，不对外接待」。

#### 环境变量预告

这两个默认值其实都可以改：`OLLAMA_MODELS` 可以改模型存储路径，`OLLAMA_HOST` 可以改监听端口（比如改成 `0.0.0.0:11434` 让局域网其他设备也能访问）。这两个都是环境变量，属于第 4 章的进阶内容，这里先混个脸熟，等用到时再回来查。

### 本章小结

- Ollama 安装要求宽松：Windows 10 22H2+ / macOS Sonoma 14+ / Linux 均可，8GB 内存起步；模型体积才是磁盘和显存的主要开销
- 四种安装方式任选：Windows 用 `winget install Ollama.Ollama`、macOS 用 dmg 拖拽、Linux 用 `curl -fsSL https://ollama.com/install.sh | sh`、Docker 用 `docker run`；Docker 方式的精髓是「标准集装箱」式隔离
- 用 `ollama --version` 验证安装；`ollama run 模型名` 一条命令完成「下载 + 进入对话」，`/bye` 退出，`ollama list` 查看已下载的模型
- 模型默认存储在 `~/.ollama/models`（Windows 在用户目录、Linux 在 `/usr/share/ollama/.ollama/models`）；服务默认监听 `127.0.0.1:11434`
- 端口、路径都可通过环境变量 `OLLAMA_MODELS` / `OLLAMA_HOST` 修改，具体留到第 4 章

### 下一章预告

电脑装好、第一个模型也跑起来了，但 `ollama` 这个工具远不止 `run` 和 `list` 两条命令。下一章我们进入 **CLI 命令与模型管理**：11 个常用命令一表看懂、`run` 的三种用法、模型怎么拉取/删除/复制，以及最重要的——怎么按自己的显存挑一个合适的量化档位。

---

## 第三章：CLI 命令与模型管理

上一章我们成功把 Ollama 装好、跑起了第一个模型，完成了「从零到能用」的跨越。但那时我们只是机械地敲一条 `ollama run`，对命令背后那整套模型管理能力还一无所知。这一章就解决这个问题：先一张表看清 11 个常用命令分别干什么，再逐个掌握模型从下载、运行、查看、更新到删除的完整生命周期，最后学会在眼花缭乱的模型库里，挑到最适合自己电脑的那一款。

> [!note] 本章定位
> 如果说第 2 章是「会用」，这一章就是「会管」。学完本章，你就能像熟练的老用户一样：想换模型就拉、想省空间就删、想看谁占着显存就 `ps`，并且知道自己的显卡该配哪个量化档位。

---

### 3.1 命令总览：一张表看懂 11 个命令

`ollama` 命令行工具是你管理这台「本地模型电脑」的控制面板。全部常用命令一共 11 个，先在一张表里看个全景，心里有个地图，后面再逐个展开。

| 命令 | 作用 | 一句话记忆 | 常用示例 |
|------|------|-----------|----------|
| `run` | 运行模型（交互式聊天或单次提问） | 点开应用开始用 | `ollama run llama3.2` |
| `pull` | 从模型库下载模型 | 安装应用 | `ollama pull qwen2.5:7b` |
| `rm` | 删除模型，释放磁盘 | 卸载应用 | `ollama rm llama3.2` |
| `ls` / `list` | 列出本地已下载的模型 | 看已安装应用列表 | `ollama list` |
| `ps` | 列出当前正在运行的模型 | 看「谁还在运行」 | `ollama ps` |
| `stop` | 停止运行中的模型，立即释放显存 | 退出应用 | `ollama stop llama3.2` |
| `serve` | 启动 Ollama 后台服务 | 打开运行时开关 | `ollama serve` |
| `show` | 查看模型详情（参数/模板/许可） | 看应用详情页 | `ollama show llama3.2` |
| `cp` | 复制模型（改名/备份） | 复制一份应用 | `ollama cp llama3.2 my-llama` |
| `create` | 从 Modelfile 构建自定义模型 | 定制专属应用 | `ollama create my-model -f Modelfile` |
| `push` | 上传模型到远程仓库 | 把应用发布到商店 | `ollama push user/my-model` |

> [!tip] 大白话
> 把模型仓库想成手机上的**应用商店**：`run` 是点开应用开始用，`ps` 是看后台「谁还在运行」，`pull` 是安装，`rm` 是卸载。Ollama 的 CLI 就是你这台电脑上的「应用商店管理页」，11 个命令约等于商店里的安装、卸载、查看、复制、发布这些按钮。

命令虽多，但日常用到 90% 的只有前五个：`pull`、`run`、`list`、`ps`、`rm`。剩下的可以按需查：`stop` 和 `serve` 偏运维，`show` 偏查看，`cp`/`create`/`push` 属于进阶定制（第 4 章会详细用到 `create`）。想不起来某个命令的用法时，随时给任意命令加 `--help` 就行，例如：

```bash
# 查看 run 命令的帮助
ollama run --help

# 查看 rm 命令的帮助
ollama rm --help
```

不需要死记硬背——命令太多时，用 `ollama --help` 就能列出一级命令清单，再对具体命令加 `--help` 看细节。[Ollama CLI 官方文档](https://docs.ollama.com/cli) 也是随时可查的权威参考。

---

### 3.2 跑模型：`run` 的三种姿势

`run` 是最常用的命令，它有三种打开方式，对应三种不同场景。理解它们，你就能在「聊天」和「程序化调用」之间自由切换。

#### 姿势一：交互式聊天

直接敲 `ollama run 模型名`，进入一个聊天界面，像跟人对话一样一问一答：

```bash
ollama run qwen2.5:7b
```

进入后终端会出现 `>>>` 提示符，直接输入问题即可：

```text
>>> 你好，你是什么模型？
你好！我是 Qwen2.5，由阿里云训练的大语言模型。今天想聊点什么？

>>> /bye
```

在这个会话里有一些斜杠命令：

| 斜杠命令 | 作用 |
|---------|------|
| `/bye` | 退出会话（等价于在别处按 Ctrl+D） |
| `/?` | 列出所有可用斜杠命令 |
| `/clear` | 清空当前对话历史，重新开始 |
| `/set` | 临时设置参数，如 `/set parameter temperature 0.5` |

交互式聊天适合「人肉使用」：追问、改需求、多轮对话。退出后模型并不会立刻消失，它还会在后台驻留一小段时间（详见 3.3 的 `ps` 命令）。

#### 姿势二：单次提问

如果只想问一个问题、拿到答案就走，不用进入交互界面，直接把问题作为参数传给 `run`：

```bash
ollama run qwen2.5:7b "用一句话解释什么是大语言模型"
```

终端会直接输出答案然后退出：

```text
大语言模型是通过海量文本训练、能够理解和生成自然语言的深度学习模型。
```

这种姿势最适合脚本和自动化：写一个循环、逐个把问题丢给本地模型，拿到结果继续处理，全程不需要人守着。

#### 姿势三：多行输入（`"""` 包裹）

当问题里含有换行——比如翻译一段话、让模型写一段多行代码、整理一段长文本——单行参数就不好使了。这时用 `"""` 把完整内容包起来：

```bash
ollama run qwen2.5:7b """
请把下面这段中文翻译成英文：
机器学习是一门让计算机从数据中学习的科学。
"""
```

输出：

```text
Machine learning is a science that enables computers to learn from data.
```

`"""` 包裹的内容里可以自由换行，模型会把整段内容当作一个完整的提示词。在交互式会话里同样能用：先敲 `"""` 回车进入多行模式，输入完内容后再敲一个 `"""` 结束并提交。

> [!note] 模型名小贴士
> 本文示例中的 `qwen2.5:7b`、`llama3.2` 都是真实存在过的模型名，但模型库会持续更新、改名。如果拉取时报错 `manifest not found`，请到 [Ollama 模型库](https://ollama.com/library) 搜一下当前实际可用的名字，或者先 `ollama list` 看看本地已有的模型。

---

### 3.3 模型管理：`pull` / `list` / `ps` / `rm` / `cp`

模型下载下来之后，就进入「本地管理」阶段。这一节掌握模型的完整生命周期：拉取、查看、监控运行、停止、删除、复制。

#### 先搞懂 tag（标签）

下载模型时，模型名后面往往带着冒号和一段后缀，例如 `qwen2.5:7b-q4_K_M`。这里的 `tag` 就是版本号。格式一般是 `模型名:参数量-量化档位`。如果不写 tag，默认拉取 `latest`。

```bash
# 这两个等价：不带 tag 默认 latest
ollama pull qwen2.5
ollama pull qwen2.5:latest
```

> [!tip] 大白话
> tag 就像软件的**版本号**。同一个模型可以同时装多个版本：`qwen2.5:7b` 是完整版，`qwen2.5:7b-q4_K_M` 是精简版，它们各自独立、互不覆盖，想用哪个就用哪个——就像手机里同一款 App 既留着旧版又装了新版。同一模型不同 tag 并存，正是 tag 存在的意义。

#### `pull`：下载模型

下载模型就是一句话：

```bash
ollama pull qwen2.5:7b
```

会看到下载进度条：

```text
pulling manifest
pulling 8ab4849b0381... 100% ▕████████████████████▏ 4.7 GB
pulling 1b22655f2b37... 100% ▕████████████████████▏  739 B
verifying sha256 digest
writing manifest
success
```

`pull` 支持断点续传：下载中途断了，重新执行同一条命令会接着传，不用从头再来。模型体积通常有几个 GB 到几十 GB，下载慢很常见（解决办法见第 5 章）。

**更新模型 = 重新 pull 一次。** Ollama 没有单独的 update 命令，想要最新版，直接重跑同名的 `pull` 即可：

```bash
# 模型有新版本时，重跑 pull 就会拉到最新版
ollama pull qwen2.5:7b
```

如果已经是最新版，这个过程会很快结束；如果模型库发布了新版本，就会像首次下载一样走一遍下载流程。这个「重跑即更新」的设计非常省心——你只需要记得「想更新就再 pull 一次」。

#### `list`：查看本地已下载的模型

```bash
ollama list
```

输出：

```text
NAME              ID              SIZE      MODIFIED
qwen2.5:7b        a4a4b2b4c5d6   4.7 GB    5 minutes ago
llama3.2:3b       b0e3f4a0a1b2   2.0 GB    2 days ago
```

各列含义：

| 列名 | 含义 |
|------|------|
| `NAME` | 模型名 + tag，例如 `qwen2.5:7b` |
| `ID` | 模型内容指纹，同一模型不同 tag 的 ID 不同 |
| `SIZE` | 占用磁盘大小（注意是量化后的体积） |
| `MODIFIED` | 最近一次使用/下载的时间 |

`list` 看的是「硬盘上装了哪些」，它回答的是「我有哪些模型可用」。

#### `ps`：查看正在运行的模型

`list` 看硬盘，`ps` 看显存/内存——它列出**当前正在运行**的模型：

```bash
ollama ps
```

输出：

```text
NAME              ID              SIZE      PROCESSOR       UNTIL
qwen2.5:7b        a4a4b2b4c5d6   4.7 GB    100% CPU        5 minutes from now
```

如果没有任何模型在运行，`ps` 只会输出一个空表头。

两列最值得关注：

- **`PROCESSOR`**：模型正跑在什么硬件上。`100% GPU` 表示全部吃显卡，`100% CPU` 表示全在跑 CPU。如果显示 `40%/60% CPU/GPU` 之类的混合值，说明显存不够、部分层被放到了内存里。**当它变成 `100% CPU` 而你又没主动改过配置时，多半是显存不够被「悄悄降级」了**——这是第 5 章排查性能问题的第一个检查点。
- **`UNTIL`**：模型什么时候被自动卸载。Ollama 默认让模型在显存里驻留 5 分钟（`5 minutes from now`），期间再来请求不用重新加载，能明显提速；超过时间没有新请求就自动卸载，把显存让出来。这个驻留时长由环境变量 `OLLAMA_KEEP_ALIVE` 控制，第 4 章会展开。

#### `stop`：停止运行中的模型

想让模型立刻退出、把显存让出来，用 `stop`：

```bash
ollama stop qwen2.5:7b
```

命令成功通常没有输出。在交互式会话里，`/bye` 也能达到同样效果。`stop` 之后再用 `ollama ps`，列表就空了。

#### `rm`：删除模型释放磁盘

下载多了磁盘会满，删掉不用的模型：

```bash
ollama rm llama3.2:3b
```

输出：

```text
deleted 'llama3.2:3b'
```

删除是**不可恢复**的，之后想用只能重新 `pull`。所以删之前先 `ollama list` 确认一下名字和 tag 没写错。如果你想保留但暂时不用，更稳妥的做法是留它在硬盘上（不占显存、只占磁盘）。

#### `cp`：复制 / 改名

给模型做备份、或者起个自己的名字，用 `cp`：

```bash
ollama cp llama3.2:3b my-llama
```

输出：

```text
copied 'llama3.2:3b' to 'my-llama'
```

注意 `cp` 复制的是整份权重，磁盘占用会翻倍。它最常见的用途是：复制一份后，用第 4 章的 Modelfile 对它做定制、再 `push` 到自己的远程仓库。相当于「把官方应用复制一份，改装成自己的版本再发布」。

#### 一个完整的模型生命周期串联

把上面的命令串起来，就是模型管理的标准流程：

```bash
# 1. 下载一个模型
ollama pull qwen2.5:7b

# 2. 跑起来聊天
ollama run qwen2.5:7b

# 3. （另开一个终端）确认它在运行、看跑在 CPU 还是 GPU
ollama ps

# 4. 用完了，让它立刻让出显存
ollama stop qwen2.5:7b

# 5. 不想要了，删掉释放磁盘
ollama rm qwen2.5:7b
```

---

### 3.4 模型库与量化：怎么选模型

打开 [Ollama 模型库](https://ollama.com/library)，就像走进了满目琳琅的应用商店——成百上千个模型，名字五花八门。怎么挑？看三个维度就够了：**参数规模**、**能力标签**、**量化档位**。

#### 维度一：参数规模（多少 B）

模型名里的 `7b`、`70b` 代表参数量，`b` 是 billion（十亿）。**参数越多，模型越「聪明」，但越吃硬件、跑得越慢。**

| 参数规模 | 常见代表 | 硬件门槛 | 特点 |
|---------|---------|---------|------|
| `3b`/`7b`/`8b` | `qwen2.5:7b`、`llama3.2:3b` | 8GB 显存或 16GB 内存 | 快、省资源，日常问答/翻译/写代码够用 |
| `13b`/`14b` | `qwen2.5:14b` | 建议 16GB 显存 | 更聪明，生成更稳定 |
| `32b` | `qwen2.5:32b` | 24GB 显存或大内存 | 接近中大型模型 |
| `70b`+ | `llama3.3:70b` | 48GB 显存 / 多卡 | 最强，但普通家用电脑跑不动 |

有一种特殊架构叫 **MoE（Mixture of Experts，混合专家）**，模型名写成 `8x7b` 这种形式——总参数量是 8 个 7b 专家的总和，但**每次只激活其中一部分**。用大白话说就是「养了一支大团队，但每次只按需叫几个人干活」，所以它比同样总参数量的小模型快很多，是「又聪明又不算太慢」的折中方案。

#### 维度二：能力标签

同一个模型名在模型库里往往有多个变体，靠后缀标签区分能力：

| 标签 | 含义 | 典型用途 |
|------|------|---------|
| （无标签） | 纯文本对话 | 通用问答、写作、翻译 |
| `vision` | 能看图（多模态） | 图片理解、OCR 识别 |
| `tools` | 支持工具/函数调用 | 让模型调用代码、API、外部工具 |
| `embedding` | 专门生成向量嵌入 | 做 RAG 知识库检索 |
| `thinking` | 推理增强（先想后答） | 数学、逻辑、复杂推理题 |

选型时先问自己：我只是日常聊天？那我选无标签的纯文本版就够；我要做本地知识库问答？那就选 `embedding` 模型配一个对话模型。

#### 维度三：量化档位（最关键）

**量化（Quantization）** 是把模型权重从高精度压缩到低精度的过程，目的是减小体积、降低显存占用。同一个模型发布时往往会附带多个量化档位，后缀如 `q8_0`、`q4_K_M`：

| 量化档位 | 体积（相对 `f16`） | 质量 | 适用场景 |
|---------|-------------------|------|---------|
| `f16` | 100%（原版） | 最准 | 显存非常充足、追求极致精度 |
| `q8_0` | 约 50% | 近无损 | 显存较足、在意精度 |
| `q5_K_M` | 约 40% | 好 | 中间档，精度/体积均衡 |
| `q4_K_M` | 约 25% | 约 96% | 家用平衡首选 |

> [!tip] 大白话
> 量化就是**照片压缩**。`f16` 是 RAW 原图，最清晰但体积巨大；`q4_K_M` 是「高清又不太占空间」的 JPEG 平衡档——体积只有原版的四分之一，画质保留约 96%，人眼基本看不出差别。对 8GB 显存的家用电脑来说，`q4_K_M` 就是那个「不占地方又够清晰」的首选。

质量排序大致是 `f16 > q8_0 > q5_K_M > q4_K_M`。注意量化在提升速度的同时会轻微损失精度，但如果你的目的是「在现有显卡上跑起来」，量化的收益远大于那点精度损失——跑不起来再准也没用。

#### 综合选型：显存匹配建议表

把三个维度合起来，结合你手头的硬件，直接用这张表对号入座：

| 你的硬件 | 推荐模型规模 | 推荐量化 | 一句话理由 |
|---------|-------------|---------|-----------|
| 8GB 显存（主流笔记本/台式机） | `7b`~`8b` | `q4_K_M` | 显存/质量最平衡，家用首选 |
| 12-16GB 显存 | `7b`~`14b` | `q4_K_M` 或 `q8_0` | 可以上 14b 的量化版 |
| 24GB 显存 | `14b`~`32b` | `q4_K_M` | 能跑更大参数 |
| 48GB+ 显存 / 多卡 | `70b`+ | `q4_K_M` / `q8_0` | 大模型，但需要足够算力 |
| 无独显（纯 CPU + 16GB 内存） | `3b`~`7b` | `q4_K_M` | 能跑但偏慢，别硬上大模型 |

挑好之后，把三个信息拼起来就是一个完整的下载命令：

```bash
# 模型名 + 参数量 + 量化档位，一次拉全
ollama pull qwen2.5:7b-q4_K_M
```

不少模型的默认 tag（`latest`）本身就是 `q4_K_M` 量化版，所以不带 tag 直接 `ollama pull qwen2.5:7b` 通常就是平衡档，省心。

> [!warning] 显存不够会发生什么
> 当模型超过显存容量时，Ollama 不会报错，而是把一部分层放到内存里、**静默回退到 CPU 计算**——表面看起来还在跑，实际慢了好几倍。遇到这种情况，换更小的模型或更低的量化档（比如从 `q8_0` 换到 `q4_K_M`）通常立竿见影。如何用 `ollama ps` 诊断、有哪些省显存参数，留到第 5 章细讲。

---

### 本章小结

- **11 个命令分三类**：下载运行类（`pull`/`run`/`ps`/`stop`）、本地管理类（`list`/`rm`/`cp`/`show`）、进阶共享类（`serve`/`create`/`push`）；日常 90% 时间只用前五个。
- **`run` 有三种姿势**：交互式聊天、单次提问、`"""` 包裹的多行输入；要自动化就选后两种。
- **tag 就是版本号**：`模型名:参数量-量化档`，同一模型多 tag 可并存；**更新模型 = 重跑一次 `pull`**，没有单独的 update 命令。
- **`ps` 是体检入口**：`PROCESSOR` 列看 CPU/GPU 占比（`100% CPU` 通常是显存不够被降级），`UNTIL` 列看自动卸载倒计时（默认驻留 5 分钟）。
- **选模型看三维度**：参数规模、能力标签、量化档位；家用 8GB 显存首选 `7b`~`8b` + `q4_K_M`。

### 下一章预告

到这儿，你已经能熟练地下载、运行、查看、停止和删除模型了——但 Ollama 的能力远不止「人肉聊天」。第 4 章我们将揭开它藏在 11434 端口的 API 大门：用 Python 和 curl 调用本地模型，用 OpenAI 兼容接口对接现成工具，用 Modelfile 定制你自己的专属模型，再用环境变量给性能做最后的调优。

---

## 第四章：进阶用法——API / OpenAI 兼容 / Modelfile / 环境变量

上一章我们已经能把模型拉下来、跑起来，学会用命令行管理本地模型了。但如果你想让 Ollama 真正「为你干活」——比如接进自己写的小程序、当某个现成客户端的本地后端、甚至按你的口味定制一个专属模型——光靠命令行是不够的。这一章我们把 Ollama 的「可编程性」一次打开：先认识它自带的 HTTP API，再看怎么用现成的 OpenAI SDK 无缝对接，然后用 Modelfile 定制自己的模型，最后学会用环境变量调整它的运行行为。

> 前置提示：本章所有示例中的模型名（如 `qwen2.5:7b`）只是示例。请先运行 `ollama list` 看看你机器上实际装了什么模型，把示例里的名字替换成真实存在的名字，命令才能跑通。

### 4.1 原生 HTTP API：Ollama 也是本地小服务器

你可能没意识到一件事：从你第一次 `ollama run` 开始，Ollama 就已经在你电脑里开了一个**本地 HTTP 服务**。你在终端里敲的每一句话，本质上都是这个服务在处理。现在我们把「服务」这层窗户纸捅破，你会看到 Ollama 的另一副面孔——一台随时待命的小服务器。

> [!tip] 大白话：本地小服务器
> 把 Ollama 想成你电脑里常驻的一家「本地小餐厅」——装好之后它就在 **11434 号桌**上待命，平时不主动打扰你。程序想找它聊天，就通过 HTTP 这个「送餐窗口」递一张纸条（请求），它回一张纸条（响应）。所以只要知道地址 `http://localhost:11434`，任何语言（curl、Python、Node.js……）都能跟它对话，完全不需要打开命令行界面。

#### 4.1.1 服务地址：base_url

Ollama 服务的默认地址是：

```text
http://localhost:11434
```

其中：

- `localhost` / `127.0.0.1`：只监听本机，外部设备访问不到（这是安全默认，第 5 章会讲怎么放开）。
- `11434`：默认端口。
- 原生 API 的所有端点都挂在 `/api` 前缀下，所以完整的基础地址是 `http://localhost:11434/api`。

而且**原生 API 默认不需要任何认证**——谁访问到这个地址都能调用。这一点在本机没问题，一旦暴露到网络就危险了（第 5 章「安全与隐私」专门讲）。

先做一个最无痛的验证——问它本地装了哪些模型：

```bash
curl http://localhost:11434/api/tags
```

你会看到一段 JSON，里面有个 `models` 数组，列出你 `ollama list` 看到的那几个模型：

```json
{
  "models": [
    {
      "name": "qwen2.5:7b",
      "model": "qwen2.5:7b",
      "size": 4680000000,
      "modified_at": "2026-08-01T10:00:00Z"
    }
  ]
}
```

能返回 JSON，说明服务活着、地址正确、API 通了。

#### 4.1.2 核心端点一览

Ollama 原生 API 的核心端点如下（除了标注 GET 的，其余都是 POST）：

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/generate` | POST | 单轮补全：给一段 prompt，返回续写或回答 |
| `/api/chat` | POST | 多轮对话：携带 messages 历史，适合聊天 |
| `/api/tags` | GET | 列出已安装模型（对应 `ollama list`） |
| `/api/show` | POST | 查看某模型的详细信息（含 Modelfile、参数、license） |
| `/api/embed` | POST | 把文本转成向量（embedding，供检索/向量库用） |
| `/api/pull` | POST | 拉取模型（对应 `ollama pull`） |
| `/api/ps` | GET | 列出当前已加载到内存/显存的模型（对应 `ollama ps`） |

> [!warning] 易错点
> **`/api/models` 这个端点并不存在。** 网上有些旧文章会写 `curl http://localhost:11434/api/models` 来列模型，那是错的。列模型请用 `/api/tags`。这也是为什么示例里我直接给你 `/api/tags`。

#### 4.1.3 第一次调用：`/api/generate`

`/api/generate` 是最简单的端点——你给一段 prompt，它补全一段回答。用 curl 发一个「非流式」请求：

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "用一句话解释什么是 HTTP",
  "stream": false
}'
```

注意 `-d` 后面跟的是请求体（JSON），`"stream": false` 表示**一次性返回完整结果**。返回是一个大的 JSON：

```json
{
  "model": "qwen2.5:7b",
  "created_at": "2026-08-10T12:00:00.123Z",
  "response": "HTTP 是客户端和服务器之间传输超文本数据的应用层协议。",
  "done": true,
  "total_duration": 1283456789,
  "prompt_eval_count": 24,
  "eval_count": 28,
  "eval_duration": 987654321
}
```

几个字段的意思：

| 字段 | 含义 |
|------|------|
| `response` | 模型生成的正文（你要的核心结果） |
| `done` | 是否生成完毕 |
| `prompt_eval_count` / `eval_count` | 输入/输出各消耗了多少 token |
| `total_duration` | 总耗时（纳秒） |

#### 4.1.4 流式 NDJSON vs `stream: false`

刚才我们在请求里写了 `"stream": false`，所以拿到一个完整的 JSON。但 Ollama 的**默认行为其实是流式**——把「不写 `stream` 字段」或写 `"stream": true`，它会逐字逐句地把结果一行一行吐出来，格式叫 **NDJSON**（Newline-Delimited JSON，每行一个独立的 JSON 对象）：

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "从 1 数到 3"
}'
```

输出会是这样（每行一个 JSON）：

```text
{"model":"qwen2.5:7b","created_at":"...","response":"1","done":false}
{"model":"qwen2.5:7b","created_at":"...","response":"2","done":false}
{"model":"qwen2.5:7b","created_at":"...","response":"3","done":false}
{"model":"qwen2.5:7b","created_at":"...","response":"","done":true,"total_duration":...}
```

最后一行 `"done": true` 才携带 token 统计等汇总信息。

**两种模式怎么选？**

| 模式 | 优点 | 适合场景 |
|------|------|----------|
| 流式 NDJSON | 第一个字立刻出现，体验像打字机 | 聊天界面、需要「边生成边显示」 |
| `stream: false` | 一次拿完整结果，代码简单 | 脚本、批量任务、只要最终答案 |

> [!note] 关键理解
> 「流式」只是**返回方式**的差别，不影响模型本身。同一个问题，流式拿到的是逐片段的同一个回答，`stream:false` 拿到的是拼好的完整版。

#### 4.1.5 多轮对话：`/api/chat`

聊天的正确姿势是用 `/api/chat`，它接受一个 `messages` 数组，可以带历史记录：

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b",
  "messages": [
    {"role": "system", "content": "你是一个简洁的助手，用中文回答。"},
    {"role": "user", "content": "1+1 等于几？"},
    {"role": "assistant", "content": "等于 2。"},
    {"role": "user", "content": "那再加上 3 呢？"}
  ],
  "stream": false
}'
```

`messages` 里每条消息的 `role` 常见有四种：`system`（系统设定）、`user`（用户）、`assistant`（模型回答）、`tool`（工具调用返回）。`/api/chat` 会把整个历史一起发给模型，模型据此理解上下文，回答 `"那再加上 3 呢？"` 时知道是 `2 + 3 = 5`。

#### 4.1.6 查模型详情：`/api/show`

想快速看某个模型的 Modelfile、参数、license 等信息，用 `/api/show`：

```bash
curl http://localhost:11434/api/show -d '{
  "model": "qwen2.5:7b"
}'
```

返回 JSON 里会有 `modelfile`、`parameters`、`license`、`template` 等字段。它跟命令行的 `ollama show --modelfile 模型名` 是同一件事的 API 版。

#### 4.1.7 常用参数速查

无论 `/api/generate` 还是 `/api/chat`，请求体里常用的参数有这些：

| 参数 | 位置 | 作用 | 示例 |
|------|------|------|------|
| `model` | 顶层 | 指定模型（必填） | `"qwen2.5:7b"` |
| `prompt` | generate | 输入文本 | `"你好"` |
| `messages` | chat | 多轮对话消息数组 | 见 4.1.5 |
| `stream` | 顶层 | 是否流式返回 | `false` |
| `options` | 顶层 | 推理参数包（温度、采样等） | `{"temperature": 0.7}` |
| `keep_alive` | 顶层 | 模型驻留内存/显存时长 | `"5m"`、`"0"`、`"-1"` |
| `format` | 顶层 | 强制输出 JSON | `"json"` |

`options` 里的推理参数和 Modelfile 的 `PARAMETER` 是同一套（温度、top_p、num_ctx 等），4.3 节会集中讲。`keep_alive` 和 4.4 节的 `OLLAMA_KEEP_ALIVE` 作用相同，只是这里针对**单次请求**，那里是**全局默认**。

> [!tip] 实践建议
> 需要程序化取结果的，优先用 `stream: false` 简化解析；做聊天产品再开流式。`format: "json"` 适合想让模型输出结构化数据、方便程序解析的场景。

#### 4.1.8 从 Python 调用原生 API

不装任何第三方库，Python 标准库就能调。下面用 `urllib` 发一个 `/api/generate` 请求：

```python
import json
import urllib.request

body = json.dumps({
    "model": "qwen2.5:7b",
    "prompt": "用一句话解释 HTTP",
    "stream": False,
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=body,
    headers={"Content-Type": "application/json"},
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))

print(data["response"])
```

预期输出（一行）：

```text
HTTP 是客户端和服务器之间传输超文本数据的应用层协议。
```

这段代码就是「本地小服务器」模型的最直观体现——没有 API 密钥、没有注册、没有费用，localhost 直接对话。

### 4.2 OpenAI 兼容 API：用现成 SDK 无缝对接

原生 API 是 Ollama 自己的「方言」。但市面上大量的工具、库、客户端（比如各类 AI 聊天插件、`openai` 官方 Python 库）只认 OpenAI 的接口格式。Ollama 非常贴心地提供了一层**兼容层**：你照常用 OpenAI 的 SDK 和格式写代码，只把地址改到本地，就能调本地模型。

> [!tip] 大白话：api_key = 门禁卡
> 把 OpenAI 兼容接口想成一道门禁。云服务的门禁卡（api_key）必须由服务商签发、逐张校验；而 Ollama 这道门是**虚掩的**——形式上你必须刷一下卡（api_key 字段不能留空），但它根本不检查卡上的字，填 `"ollama"` 或随便什么字符串都能进。方便是方便，代价是它只信任「来敲门的都是本机自己人」，所以千万别把它暴露到公网（第 5 章细讲）。

#### 4.2.1 就改两个东西

用 OpenAI 兼容 API，核心只需要改两个配置：

| 配置 | 值 | 说明 |
|------|-----|------|
| `base_url` | `http://localhost:11434/v1` | 注意前缀是 `/v1`，不是 `/api` |
| `api_key` | `"ollama"` | 必填但被忽略，随便填 |

#### 4.2.2 Python 最小示例（openai SDK）

先装官方 `openai` 库：

```bash
pip install openai
```

然后写一个最小调用：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # 指向本地 Ollama
    api_key="ollama",                      # 必填但被忽略，随便填
)

resp = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍你自己"}
    ],
)

print(resp.choices[0].message.content)
```

预期输出：

```text
我是通义千问，一个由阿里云训练的大语言模型，可以回答问题、编写代码、提供建议等。
```

注意取值路径是 `resp.choices[0].message.content`——这正是 OpenAI Chat Completions 的标准返回结构。也就是说，你以前为 OpenAI 写的调用代码，**只改 base_url 和 api_key 两行**就能跑在本地模型上。

#### 4.2.3 curl 示例

不写 Python 的话，curl 同样可以：

```bash
curl http://localhost:11434/v1/chat/completions -d '{
  "model": "qwen2.5:7b",
  "messages": [{"role": "user", "content": "你好"}]
}'
```

返回结构（已省略部分字段）：

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！有什么可以帮你的吗？"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 14,
    "total_tokens": 26
  }
}
```

#### 4.2.4 换回云端只需改两行

兼容层的最大价值是**切换零成本**。同样的代码，想从本地模型换回 OpenAI 云端，只需改两行：

```python
client = OpenAI(
    base_url="https://api.openai.com/v1",  # 云端地址
    api_key="sk-你的真实密钥",             # 云端需要真实密钥
)
```

其它所有 `client.chat.completions.create(...)` 调用一行都不用动。这就是「无缝对接」的含义——你的业务代码跟模型跑在哪无关。

#### 4.2.5 兼容层支持哪些能力

Ollama 的 OpenAI 兼容层主要支持这些端点与能力：

| 端点 | 支持情况 |
|------|----------|
| `/v1/chat/completions` | 支持流式、tools 函数调用、JSON mode；vision 模型只接受 base64 图片 |
| `/v1/completions` | 兼容（补全接口） |
| `/v1/embeddings` | 支持（向量嵌入） |
| `/v1/models` | 支持（列出模型） |

```bash
curl http://localhost:11434/v1/models
```

> [!note] 局限说明
> 兼容层是「尽力兼容」，不是 OpenAI 的完整克隆。个别前沿特性（某些新参数、特定的多模态行为）可能不被支持，以官方文档为准：https://docs.ollama.com/api/openai-compatibility

### 4.3 Modelfile：定制自己的模型

你有没有过这种体验：每次调用都要在请求里写一遍「你是我的助手，请用中文、简洁地回答……」？或者想让模型默认用某种语气、固定上下文长度？这些「固定偏好」其实可以**烧进一个全新命名的模型里**——这就是 Modelfile 的用武之地。

> [!tip] 大白话：定制食谱
> 把 Modelfile 想成一份「定制食谱」。`FROM` 是食材（你选哪个基座模型，比如 `qwen2.5:7b`）；`PARAMETER` 是火候和佐料（temperature 多激进、num_ctx 锅有多大）；`SYSTEM` 是开饭前的「主厨训话」（模型每次回答前都会默念这段系统提示词）。`ollama create` 就是按这份食谱下锅，出锅后得到一个名字全新的专属模型。

#### 4.3.1 什么是 Modelfile

Modelfile 是一个纯文本文件，类似 Dockerfile，但内容是「模型蓝图」。它由一行行**指令（INSTRUCTION）**组成，告诉 Ollama：从哪个基座模型开始、用什么参数、配什么系统提示词。然后用 `ollama create` 命令把它「构建」成一个可运行的模型。

#### 4.3.2 核心指令一览

| 指令 | 作用 | 示例 |
|------|------|------|
| `FROM` | 指定基座模型（必填），也可以指向 GGUF/Safetensors 文件 | `FROM qwen2.5:7b` |
| `PARAMETER` | 设置推理参数 | `PARAMETER temperature 0.7` |
| `SYSTEM` | 设置系统提示词（每次对话都生效） | `SYSTEM 你是简洁的编程助手` |
| `TEMPLATE` | 自定义对话模板（Go 模板语法） | `TEMPLATE """{{.Prompt}}"""` |
| `ADAPTER` | 叠加 (Q)LoRA 微调权重 | `ADAPTER ./lora.gguf` |
| `MESSAGE` | 预设示例对话（few-shot 示例） | `MESSAGE user 你好` |

#### 4.3.3 最小示例 + `ollama create`

新建一个文件，名字就叫 `Modelfile`（无扩展名），内容如下：

```Modelfile
FROM qwen2.5:7b

PARAMETER temperature 0.7
PARAMETER num_ctx 4096
PARAMETER top_p 0.9

SYSTEM You are a concise coding assistant. Always answer in Chinese.
```

逐行解释：

- `FROM qwen2.5:7b`：以 `qwen2.5:7b` 为基座模型。
- `PARAMETER temperature 0.7`：回答更收敛、更少发散（默认 0.8）。
- `PARAMETER num_ctx 4096`：把上下文窗口从默认 2048 提到 4096，能记住更长的对话。
- `SYSTEM ...`：给模型一个固定的「人设 + 语气」。

然后构建它：

```bash
ollama create my-coding-assistant -f Modelfile
```

构建完成后，`ollama list` 里就会出现一个叫 `my-coding-assistant` 的新模型：

```text
NAME                    ID              SIZE       MODIFIED
my-coding-assistant     a1b2c3d4e5f6    4.7 GB      1 minute ago
qwen2.5:7b              abcdef123456    4.7 GB      3 hours ago
```

之后直接运行它，不需要再带任何系统提示词：

```bash
ollama run my-coding-assistant "写一个打印 Hello 的 Python 程序"
```

它每次都会按食谱里设定的语气和规则回答。你甚至可以把这份 Modelfile 分享给朋友，让对方 `ollama create` 出一模一样的模型。

#### 4.3.4 查看模型的配置：`ollama show --modelfile`

想看看某个模型当初是用什么配置构建的（或者反推一个现成模型怎么调出来的）：

```bash
ollama show --modelfile my-coding-assistant
```

输出就是一份完整的 Modelfile 内容，包含所有指令和参数。这是排查「为什么这个模型回答风格这么怪」的第一站。

#### 4.3.5 常用 `PARAMETER` 速查

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `temperature` | 0.8 | 越高越随机/有创意，越低越确定/保守 |
| `num_ctx` | 2048 | 上下文窗口长度（token 数），越大能记住越多但越吃显存 |
| `top_k` | 40 | 采样时只从概率最高的前 K 个 token 里选 |
| `top_p` | 0.9 | 核采样：累计概率达到该阈值的最小 token 集里采样 |
| `repeat_penalty` | 1.1 | 抑制重复内容，越大越不爱重复 |
| `seed` | 随机 | 固定随机种子后，相同输入可复现相同输出 |

#### 4.3.6 `SYSTEM` 和 `TEMPLATE` 的区别

容易混淆的两个指令：

- `SYSTEM`：设定模型的**行为准则**，相当于「每次对话前先默念一遍这句话」。绝大多数定制需求用它就够了。
- `TEMPLATE`：控制「用户消息如何被拼成模型真正吃进去的格式」（比如 `{{.System}}`、`{{.Prompt}}`、`{{.Messages}}` 这些占位符怎么摆放）。一般**不需要改**——除非你明确知道自己在调什么，改错会导致模型输出乱套。

> [!tip] 实践建议
> 新手定制模型，记住三件套就够：`FROM`（选基座）、`PARAMETER`（调温度/上下文）、`SYSTEM`（定人设）。`TEMPLATE` 和 `ADAPTER` 属于进阶中的进阶，先留个印象即可。

### 4.4 环境变量：按需调整运行行为

有些行为——监听哪个地址、模型存在哪、模型驻留多久、能不能并发——不适合写在 Modelfile 或请求里，它们是**服务本身的属性**。这些由环境变量控制，Ollama 服务启动时读取一次。

> [!tip] 大白话：开机前设置
> 把环境变量想成服务器的「开机前设置」——就像你调整咖啡机的水温、研磨度，必须在**开机前**调好，开机之后再改就晚了。Ollama 服务只在启动时读一次这些设置，之后不再读取，所以改完必须**重启 Ollama** 才生效。

#### 4.4.1 关键环境变量一览

以下变量以官方 envconfig 为准（来源：https://github.com/ollama/ollama/blob/main/envconfig/config.go ）：

| 变量 | 默认值 | 作用 |
|------|--------|------|
| `OLLAMA_HOST` | `127.0.0.1:11434` | 服务监听地址。改 `0.0.0.0` 可让局域网其他设备访问（注意安全，见第 5 章） |
| `OLLAMA_MODELS` | `~/.ollama/models` | 模型存储目录，改到其他盘可释放 C 盘空间 |
| `OLLAMA_KEEP_ALIVE` | `5m` | 模型驻留内存/显存时长。`-1` 常驻不卸载，`0` 用完立即卸载 |
| `OLLAMA_NUM_PARALLEL` | `1` | 同一模型允许的并发请求数。显存占用 ≈ 并发数 × 上下文大小 |
| `OLLAMA_MAX_LOADED_MODELS` | `3 × GPU 数` | 同时常驻内存的模型个数上限 |
| `OLLAMA_CONTEXT_LENGTH` | 按显存自适应 | 全局默认上下文长度，覆盖单模型默认值 |
| `OLLAMA_FLASH_ATTENTION` | 关闭 | 设为 `1` 启用 Flash Attention，可节省显存（需要新显卡） |

> [!warning] 版本提醒
> `OLLAMA_NUM_GPU`（手动指定 GPU 层数）在新版本中**已移除**，层调度现在全自动。网上很多老教程还在教它，遇到别困惑，以官方 envconfig 为准。

#### 4.4.2 Windows 上怎么设置

Windows 上最直接的方式是用 `setx` 命令写入**用户环境变量**（永久生效）：

```powershell
# 让模型常驻显存，不自动卸载
setx OLLAMA_KEEP_ALIVE -1

# 允许局域网设备访问（注意安全！）
setx OLLAMA_HOST 0.0.0.0

# 把模型目录改到 D 盘
setx OLLAMA_MODELS "D:\ollama-models"
```

关键一步：**设置完成后必须重启 Ollama**。Windows 上 Ollama 是系统托盘里的后台应用——右键托盘图标退出，再重新打开「Ollama」应用，新设置才会生效。

> [!note] `setx` 的注意点
> `setx` 只对**之后新启动的进程**生效，不会改变你当前已打开的那个终端。改完重启 Ollama 后，建议重新开一个终端再验证。

#### 4.4.3 Linux（systemd）上怎么设置

Linux 上 Ollama 以 systemd 服务运行，推荐用 `systemctl edit` 覆盖配置（不会破坏原文件）：

```bash
sudo systemctl edit ollama
```

在打开的编辑器里写入：

```ini
[Service]
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_MODELS=/data/ollama-models"
```

保存后重启服务：

```bash
sudo systemctl restart ollama
```

macOS 则是在「应用程序」里退出 Ollama 再重新打开，或通过 launchd 环境配置（一般用 GUI 设置即可）。

#### 4.4.4 三个最常用的组合场景

| 场景 | 需要的环境变量 | 效果 |
|------|---------------|------|
| 局域网内多台设备共用一台机器的模型 | `OLLAMA_HOST=0.0.0.0` + 防火墙放行 11434 | 其他设备可访问（务必先读第 5 章安全部分） |
| 频繁多轮对话、不想每次等加载 | `OLLAMA_KEEP_ALIVE=-1` | 模型常驻显存，响应更快，代价是显存一直被占 |
| C 盘空间紧张 | `OLLAMA_MODELS=D:\ollama-models` | 模型改存其他盘 |

> [!tip] 实践建议
> 环境变量是一把双刃剑：`OLLAMA_HOST=0.0.0.0` 和 `OLLAMA_KEEP_ALIVE=-1` 都很实用，但前者会打开安全缺口、后者会长期占用显存。建议按需开启，用不到就保持默认。

### 本章小结

- **原生 HTTP API**：Ollama 安装后就是一个本地 HTTP 服务，默认地址 `http://localhost:11434/api`，无需认证。核心端点有 `/api/generate`（单轮）、`/api/chat`（多轮）、`/api/tags`（列模型，**不是** `/api/models`）、`/api/show`（看详情）、`/api/embed`（向量）。默认流式返回 NDJSON，设 `"stream": false` 一次拿完整 JSON。
- **OpenAI 兼容 API**：把 `base_url` 设为 `http://localhost:11434/v1`、`api_key` 随便填（如 `"ollama"`），就能用现成的 OpenAI SDK 调本地模型。换回云端只需改这两行。
- **Modelfile 定制**：用 `FROM` 选基座、`PARAMETER` 调参数、`SYSTEM` 定人设，`ollama create 名称 -f Modelfile` 构建出专属模型，`ollama show --modelfile` 可查看已有模型的配置。
- **环境变量**：`OLLAMA_HOST` / `OLLAMA_MODELS` / `OLLAMA_KEEP_ALIVE` / `OLLAMA_NUM_PARALLEL` / `OLLAMA_CONTEXT_LENGTH` / `OLLAMA_FLASH_ATTENTION` 等控制服务行为，**改完必须重启 Ollama**。注意 `OLLAMA_NUM_GPU` 已在新版移除。
- **核心心智**：API 是把 Ollama 从「命令行玩具」变成「可编程组件」的钥匙；Modelfile 是把「每次都要重复的偏好」固化成「开箱即用的模型」；环境变量是「服务开机前的全局开关」。

### 下一章预告

这一章我们把 Ollama 的「可编程性」全部打开了，但进阶用法往往伴随着新的坑：为什么推理会突然变慢、下载卡住不动、局域网里别人访问不到你的服务、甚至模型裸奔在公网上？下一章我们进入「常见坑与最佳实践」，把这些实战中的拦路虎逐个拆掉——踩过坑再回来读，体感更佳。

---

## 第五章：常见坑与最佳实践

上一章你学会了用 HTTP API、OpenAI 兼容接口、Modelfile 和环境变量这些「进阶武功」。能走到这里，说明你已经能正经地把 Ollama 用起来了。但真正上手 1-2 天后，你大概率会撞上四类「看不见的墙」：模型突然变慢、下载卡住不动、别人访问不到、或者——更危险的——被局域网里的陌生人白嫖。这一章就是这份使用文档的「避坑手册」：先带你认出四个最常见的坑，再给一张从第 1 章到第 5 章提炼出来的最佳实践清单。踩过坑再读体感最佳，没踩过也可以把它当速查表留着。

### 5.1 显存不足静默回退 CPU

#### 现象：没有报错，只是变慢

本地跑大模型最阴的坑，不是报错，而是**不报错**。当你拉了一个超出显存容量的模型（比如 8GB 显存硬跑 70B 量化模型），Ollama 不会拒绝启动，而是悄悄把计算从 GPU 换到 CPU。结果就是：对话看起来一切正常，但一个字一个字往外蹦，速度慢了十倍不止。

> [!tip] 大白话
> 把显存不够理解成「主力员工（GPU）忙不过来了」。Ollama 不会当场甩手不干，而是**偷偷换人干活**——叫来速度慢得多的「替补员工（CPU）」顶班。表面上看工作还在推进，实际上效率完全不是一个档次。所以问题不是「它坏了」，而是「它在用最慢的方式硬撑」。

#### 诊断：`ollama ps` 看 PROCESSOR 列

怎么确认自己被「偷偷换人」了？用第 3 章学过的 `ollama ps`：

```bash
# 查看当前正在运行的模型
ollama ps
```

重点看 **PROCESSOR** 这一列：

```bash
# 正常情况：GPU 在跑
# NAME               ID            SIZE    PROCESSOR   UNTIL
# qwen2.5:7b-q4_K_M  abc12345      4.7GB   100% GPU    4 minutes from now

# 异常情况：回退到了 CPU
# NAME               ID            SIZE    PROCESSOR   UNTIL
# qwen2.5:7b-q4_K_M  abc12345      4.7GB   100% CPU    4 minutes from now
```

只要 `PROCESSOR` 列出现 `CPU`（或 `GPU/CPU` 混合且 GPU 占比很低），基本就能断定显存不够了。这是官方社区里排查此类问题最常用的第一步 [Ollama GitHub Issue #14258](https://github.com/ollama/ollama/issues/14258)。

#### 对策：换模型 + 省显存开关

确认是显存不足后，按「先换模型、再调参数」的顺序处理：

| 优先级 | 对策 | 说明 |
|--------|------|------|
| 1 | 换更小或量化更高的模型 | 从 `7b` 换 `3b/1.5b`；或把 `q8_0` 换成 `q4_K_M`，体积约减半 |
| 2 | 开 Flash Attention | `OLLAMA_FLASH_ATTENTION=1`，省显存 |
| 3 | 降低 KV 缓存精度 | `OLLAMA_KV_CACHE_TYPE=q8_0`，牺牲少量精度换显存 |
| 4 | 调小上下文长度 | 把 `num_ctx` 从 8192 降到 4096，KV 缓存占用直接减半 |

```bash
# Linux/macOS：启用 Flash Attention 省显存
OLLAMA_FLASH_ATTENTION=1 ollama serve

# 降低 KV 缓存精度，进一步省显存
OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve

# 临时跑一个模型时，用 --verbose 观察显存占用与速度
ollama run qwen2.5:7b --verbose
```

上下文长度（`num_ctx`）是显存杀手之一：KV 缓存的大小和上下文长度成正比。想一劳永逸，就在 Modelfile 里固定参数，再 `ollama create` 生成专属模型（第 4.3 节的做法）：

```bash
# Modelfile 片段：把上下文固定为 4096
FROM qwen2.5:7b
PARAMETER num_ctx 4096
```

> [!warning] 注意
> 环境变量改完**必须重启 Ollama 才生效**（Windows 上尤其容易忽略这一步）。新版 Ollama 已移除 `OLLAMA_NUM_GPU`，层调度全自动，别再照旧教程设置它，详见官方 [envconfig 源码](https://github.com/ollama/ollama/blob/main/envconfig/config.go)。

### 5.2 下载慢 / 镜像 / 网络问题

#### 为什么慢：模型体积大 + 官方无镜像

本地模型的「体重」远超你想象：一个 7B 量化模型 4-7GB，70B 模型轻松几十 GB。国内直连下载时，慢、断、卡是常态。更麻烦的是，**Ollama 官方没有提供国内镜像配置项**，网上流传的「改镜像源」大多是旧版本或第三方方案，未必可靠 [Ollama 官方文档](https://docs.ollama.com/)。

#### 对策一：走代理（HTTPS_PROXY）

最通用的办法是给 Ollama 设置 HTTPS 代理。代理设置通过环境变量注入，下载走代理通道：

```bash
# Linux/macOS：临时使用代理下载模型
export HTTPS_PROXY=http://127.0.0.1:7890
ollama pull qwen2.5:7b
```

```powershell
# Windows PowerShell：同样临时生效
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
ollama pull qwen2.5:7b
```

> [!tip] 大白话
> 把下载流量想成「直行堵车的高速路」，代理就是一条绕行路线——**流量绕道走，绕过拥塞点**。设了 `HTTPS_PROXY`，Ollama 拉模型时不直连官方源，而是先到代理再转发，国内连不上的问题就绕开了。代理端口换成你自己代理软件的即可（Clash 常见 `7890`、v2ray 常见 `10809`）。

#### 对策二：WSL2 关闭 Large Send Offload V2

如果你是在 **WSL2** 里用 Ollama，还有一个 Windows 特有的坑：WSL 虚拟网卡开启的 **Large Send Offload V2（LSO）** 会导致下载时大包乱序、速度奇慢。关闭它通常能显著提速（中文博客社区总结的常见解法）：

```powershell
# Windows 上以管理员身份打开 PowerShell，关闭 WSL 虚拟网卡的 LSO
Get-NetAdapter -IncludeHidden |
  Where-Object { $_.InterfaceDescription -like "*WSL*" } |
  Disable-NetAdapterLso -IPv4 -IPv6
```

> [!note] 小结
> 下载慢先看三件事：模型是不是真的很大（几十 GB 很正常）、有没有走代理、WSL2 的 LSO 关了没。前两个是通用方案，第三个只影响 WSL2 用户。

### 5.3 端口占用与跨设备访问

#### 默认只监听本机

Ollama 装好后默认监听 `127.0.0.1:11434`。`127.0.0.1` 的意思是「只有本机能访问」——这是安全的默认值，但也意味着：你想用手机、另一台电脑、或局域网里的 NAS 去连它，默认是**连不上的**。

> [!tip] 大白话
> `127.0.0.1` 相当于**只在自家门口挂门牌**，外人根本不知道这里有个服务；`0.0.0.0` 则是把门牌挂到小区大门口，所有进小区的人都能看到。默认是前者，所以跨设备访问前必须主动改成后者。

#### 端口被占用怎么办

`11434` 也可能被别的程序抢走，现象是启动 Ollama 时报端口冲突或服务起不来。用系统自带命令查谁占用了端口：

```bash
# 查看 11434 端口被哪个进程占用
netstat -ano | grep 11434

# 用输出里的 PID 反查进程名（Windows）
tasklist | findstr <PID>
```

确认是无关程序占用后，杀掉对应进程，或改走另一个端口（把 `OLLAMA_HOST` 改成 `127.0.0.1:11435` 之类）。

#### 跨设备访问：OLLAMA_HOST=0.0.0.0 + 防火墙

要让局域网内其他设备访问，需要两步：改监听地址 + 放行防火墙。

```bash
# Linux/macOS：监听所有网卡，允许局域网其他设备访问
OLLAMA_HOST=0.0.0.0 ollama serve

# 长期生效可写入 systemd 服务的 Environment 或 shell 配置文件
```

```powershell
# Windows：系统设置 → 环境变量 → 新建 OLLAMA_HOST=0.0.0.0，重启 Ollama

# 再以管理员身份放行防火墙 11434 端口
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow
```

之后局域网里的其他设备就能通过 `http://<你这台电脑的IP>:11434` 访问了。查自己 IP：Windows 用 `ipconfig`，Linux/macOS 用 `ip addr` 或 `ifconfig`。

> [!warning] 注意
> 一旦 `OLLAMA_HOST=0.0.0.0`，**任何能连到你这台机器的人都能访问 11434**。请务必先读完 5.4 再决定要不要这么做。

### 5.4 安全与隐私：API 无认证怎么办

#### 危险根源：API 没有身份校验

Ollama 的 API **默认没有任何认证**。回想第 4.2 节：OpenAI 兼容接口的 `api_key` 填任意值（`"ollama"`）都能通过——因为 Ollama 根本不校验它。本地单机使用时这是便利，可一旦监听 `0.0.0.0`，就等于把门敞开了。

> [!tip] 大白话
> 设成 `0.0.0.0` 等于**把大门敞开**：Ollama 的 API 没有身份校验，知道地址的人就像拿到一张**临时工牌**，谁都能进来自助调用你的模型。轻则被白嫖算力，重则你的对话记录（可能含隐私）被第三方看到。

#### 对策一：除非必要，别设 0.0.0.0

能只在本地用，就保持默认 `127.0.0.1`。多数场景（本地写代码、接 VS Code / 各种客户端）根本不需要跨设备访问。

#### 对策二：要暴露就用反向代理 + 鉴权

如果确实需要对外提供服务（比如部署给团队用），不要直接暴露 11434，而是套一层反向代理（Nginx / Caddy），在代理层加 TLS 和鉴权。这样即使端口暴露，没有合法凭证的人也进不来。这是一个典型的安全架构：Ollama 只监听本机，代理负责对外和对内转发，鉴权在代理层完成。

#### 对策三：OLLAMA_ORIGINS 白名单

如果你的场景是「网页前端（浏览器）直接调 Ollama」，浏览器跨域请求（CORS）会触发校验。这时用 `OLLAMA_ORIGINS` 限制允许的网页来源，防止任意网站调用你的模型：

```bash
# 只允许指定网页域名跨域调用
OLLAMA_ORIGINS="https://my-web-app.example.com" ollama serve

# 多个来源用逗号分隔
OLLAMA_ORIGINS="https://a.example.com,https://b.example.com" ollama serve
```

#### 安全决策表

| 使用场景 | 监听地址 | 需要做的事 |
|----------|----------|-----------|
| 仅本机使用（默认推荐） | `127.0.0.1` | 什么都不用改 |
| 局域网内信任设备访问 | `0.0.0.0` | 放行防火墙 11434；仅在可信网络内使用 |
| 对外提供服务 | `127.0.0.1` + 反向代理 | 代理层加 TLS 与鉴权；不要直接暴露 11434 |
| 网页前端直接调用 | 视情况 | 配 `OLLAMA_ORIGINS` 白名单限制来源 |

> [!warning] 铁律
> 一句话总结：**API 无认证是默认事实，所有安全都要靠自己补。** 图省事直接暴露 `0.0.0.0` 到公网，等于把家门钥匙挂门口。

### 5.5 最佳实践清单

最后，把第 1-5 章的要点浓缩成一份可勾选的 checklist。逐项打钩，你的 Ollama 就处于「省心、够快、安全」的稳定状态。

#### 选型

- [ ] 显存够大再选大模型：8GB 显存首选 7B 的 `q4_K_M` 量化档（第 3.4 节）
- [ ] 不确定模型能不能跑，先 `ollama pull` 小模型试水，再看 `ollama ps` 的 PROCESSOR 列
- [ ] 按用途选能力标签：需要视觉选 `vision` 模型，要接工具调用选 `tools` 模型

#### 安装

- [ ] Windows / macOS / Linux 任选一种安装方式，装完用 `ollama --version` 验证（第 2 章）
- [ ] 用 Docker 时记得带 GPU 参数，否则默认跑 CPU 白浪费硬件（第 2.2 节）
- [ ] 想换模型存放盘符，提前设好 `OLLAMA_MODELS`（第 4.4 节）

#### 运维

- [ ] 模型异常变慢先跑 `ollama ps`，确认 PROCESSOR 列没偷偷变成 CPU（5.1）
- [ ] 下载慢：走代理设 `HTTPS_PROXY`；WSL2 用户关闭网卡 Large Send Offload V2（5.2）
- [ ] 跨设备访问前，确认 `OLLAMA_HOST` 和防火墙 11434 都已就位（5.3）
- [ ] 改任何环境变量后重启 Ollama 再验证，别被「改了没生效」卡住（第 4.4 节）

#### 安全

- [ ] 除非必要，保持默认 `127.0.0.1`，不设 `0.0.0.0`（5.4）
- [ ] 必须对外服务时，套反向代理 + TLS + 鉴权，不直接暴露 11434（5.4）
- [ ] 网页端调用配好 `OLLAMA_ORIGINS` 白名单（5.4）
- [ ] 不在公网裸奔：记住 API 无认证，安全全靠自己补（5.4）

### 本章小结

- 显存不足不会报错，只会「静默回退 CPU」：用 `ollama ps` 看 PROCESSOR 列确诊，靠换量化模型、`OLLAMA_FLASH_ATTENTION`、`OLLAMA_KV_CACHE_TYPE`、调小 `num_ctx` 解决
- 下载慢的通用解是 `HTTPS_PROXY` 代理；WSL2 用户额外关掉网卡 LSO V2
- 默认 `127.0.0.1` 只能本机访问；跨设备要 `OLLAMA_HOST=0.0.0.0` + 放行防火墙，但这会带来安全风险
- Ollama API **没有身份校验**：避免随意设 `0.0.0.0`，对外服务必须走反向代理 + 鉴权，网页端用 `OLLAMA_ORIGINS` 限定来源
- 最后用 5.5 的 checklist 逐项自检，把「能用」升级成「稳定、够快、安全」

到这里，这份《Ollama 使用文档》就讲完了。回顾一下整条路线：第 1 章你知道了 Ollama 是什么、为什么值得本地跑；第 2 章装好并跑起了第一个模型；第 3 章掌握了 CLI 与模型管理，学会了按显存选量化档位；第 4 章把 Ollama 变成了可编程的本地小服务器，还能定制专属模型；第 5 章则帮你避开最常见的四个坑。从「零基础」到「能独立部署、排查、防护」，你已经具备把本地大模型真正用进日常工具链的全部能力。剩下的，就是在实操中积累手感了。

---

## 参考来源

- [Ollama 官方仓库 README](https://github.com/ollama/ollama) — 项目定位、架构与模型列表
- [Ollama 官方快速开始](https://docs.ollama.com/quickstart) — 分平台安装与首个模型
- [Ollama 官方模型库](https://ollama.com/library) — 模型名、tag 与量化档位查询
- [Ollama CLI 官方文档](https://docs.ollama.com/cli) — 全部命令行参考
- [Ollama HTTP API 官方文档](https://docs.ollama.com/api/introduction) — 原生 API 参考
- [Ollama OpenAI 兼容官方文档](https://docs.ollama.com/api/openai-compatibility) — OpenAI 兼容层参考
- [Ollama Modelfile 官方文档](https://docs.ollama.com/modelfile) — Modelfile 指令参考
- [Ollama 环境变量源码 envconfig](https://github.com/ollama/ollama/blob/main/envconfig/config.go) — 环境变量权威来源
- [Ollama GitHub Issue #14258](https://github.com/ollama/ollama/issues/14258) — 显存不足静默回退 CPU 的社区排查
