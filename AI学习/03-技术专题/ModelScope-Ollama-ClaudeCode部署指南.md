---
title: "ModelScope-Ollama-ClaudeCode部署指南"
tags: [AI学习, 技术专题, LLM, 本地模型, Ollama, ModelScope, 实战指南]
created: 2026-08-10
updated: 2026-08-10
status: 已完成
source_project: modelscope-ollama-claude-code
---

# 使用 ModelScope 拉取模型 + Ollama 部署 + Claude Code 使用

> [!info] 适用范围
> 本笔记是一篇实战步骤指南，面向零基础、能复制命令跟做的读者，带你把「ModelScope 下载 GGUF 模型 → Ollama 本地部署 → Claude Code 接入」整条链路跑通；全程免 Anthropic API Key，数据不出本机。

## 目录

1. [第 1 章：准备工作与环境总览](#第-1-章准备工作与环境总览)
2. [第 2 章：环节一——用 ModelScope 拉取 GGUF 模型](#第-2-章环节一用-ModelScope-拉取-GGUF-模型)
3. [第 3 章：环节二——用 Ollama 部署模型](#第-3-章环节二用-Ollama-部署模型)
4. [第 4 章：环节三——让 Claude Code 接入本地 Ollama](#第-4-章环节三让-Claude-Code-接入本地-Ollama)
5. [第 5 章：端到端速通（从零到 Claude Code 跑起来）](#第-5-章端到端速通从零到-Claude-Code-跑起来)
6. [第 6 章：常见问题与避坑清单速查](#第-6-章常见问题与避坑清单速查)

---

## 第 1 章：准备工作与环境总览

本教程的目标很具体：把一个开源大模型下载到自己的电脑，用 Ollama 在本地跑起来，再让 Claude Code 直接连上这个本地模型——不需要 Anthropic 的 API Key，数据也不出本机。动手之前，先把整条链路、硬件门槛和要装的软件看清楚，后面就不会走偏。

### 三环节链路全景

全流程是单向的三环节管道，后文各章对应一环：

| 环节 | 做什么 | 产出 |
|------|--------|------|
| ① ModelScope 下载 | 从魔搭社区拉取 GGUF 格式模型 | 硬盘上的模型文件 |
| ② Ollama 部署 | 导入 GGUF 并创建可运行模型 | 本地可 `ollama run` 的模型 |
| ③ Claude Code 接入 | 通过本地 API 连上 Ollama | 免 Key 直连本地模型 |

> [!tip] 大白话：GGUF 像「预制菜」
> 把 GGUF 想成**已经打包好的模型文件**——像一袋预制菜，Ollama 这个「锅」拿到就能直接煮，不用再处理生食材。所以第 2 章专门去 ModelScope 下 GGUF 版，就是为了省掉格式转换这一步。

> [!tip] 大白话：本地模型像「装在自己电脑里的 AI」
> 把本地模型想成**只在你电脑里运行的 AI**——推理不联网，数据不发给任何云端服务器，全在本机完成。所以它的好处是免费、隐私可控，代价是速度由你的硬件决定。

### 硬件与系统要求

- 内存：建议 8GB 以上（模型推理时需常驻内存）
- GPU（可选）：NVIDIA 显卡 + 驱动 551.61+ 可获得 GPU 加速
- 纯 CPU 也能跑通，但明显更慢，属于「能跑、别求快」

### 需要安装的软件清单

| 软件 | 用途 | 安装方式 |
|------|------|---------|
| Python + modelscope | 从 ModelScope 下载模型 | `pip install modelscope` |
| Ollama | 本地部署与运行模型 | Windows 装 `OllamaSetup.exe`；验证 `ollama --version` |
| Claude Code | 接入本地模型的编程助手 | Windows：`irm https://claude.ai/install.ps1 \| iex` |

### 预期管理：本地推理慢是常态

先接受一个预期：本地推理的速度取决于你的硬件，输出是「一个字一个字蹦出来」的，和云端大模型差距明显。这正是本教程的意义——**用免费、私有、可控，换更慢的速度**。第 5 章会给出「先用小模型跑通链路，再按显存升级」的选型建议。

### 本章小结

- 整条链路是「下载 → 部署 → 接入」三环节，每个环节对应后文一章
- 8GB+ 内存是基线，NVIDIA 驱动 551.61+ 可加速，纯 CPU 也能跑
- 需要安装 Python + modelscope、Ollama、Claude Code 三样软件
- 本地推理慢是常态，先接受预期再动手

### 下一章预告

环境心里有数了。下一步进入环节一：用 ModelScope 把 GGUF 模型拉到本地。

---

## 第 2 章：环节一——用 ModelScope 拉取 GGUF 模型

上一章我们准备好了环境，现在开始第一步：用 ModelScope（魔搭社区）把 GGUF 模型拉到本地。这一步的产出是一份「拿到就能用」的模型文件，注意认准 GGUF 格式，否则第 3 章导入 Ollama 时会多出格式转换的麻烦。

### 安装 modelscope

Python 环境就绪后，一行命令安装：

```bash
pip install modelscope
```

安装完成后用 `modelscope --version` 验证。下载模型有 CLI 和 Python SDK 两种方式，功能等价，按习惯选一种即可。

### 方式一：CLI 下载（最常用）

```bash
modelscope download --model Qwen/Qwen2.5-7B-Instruct-GGUF --local_dir ./models
```

核心参数：

| 参数 | 说明 |
|------|------|
| `--model` | 模型 ID（必填） |
| `--revision` | 模型版本/分支，默认主分支 |
| `--local_dir` | 直接下载到该目录；与 `--cache_dir` 同时指定时 **`--local_dir` 优先** |
| `--cache_dir` | 缓存目录，文件会落到 `cache_dir/<org>/<model>/` |
| `--include` / `--exclude` | glob 通配符过滤；指定了具体文件时二者被忽略 |

> [!tip] 大白话：量化档（Q4_K_M / Q8_0）像「原图 vs 压缩图」
> 把量化档想成图片的清晰度——Q8_0 像无损 PNG，文件大、质量几乎无损；Q4_K_M 像压缩得比较狠的 JPG，体积只剩约四分之一，质量保留 95-97%，实际体验几乎看不出差别。所以入门默认选 Q4_K_M 这个「甜点位」：省硬盘、跑得快，效果不差。

### 方式二：Python SDK（`snapshot_download`）

适合在脚本里按规则筛选文件，或下载私有模型：

```python
from modelscope import snapshot_download

# 只下某个量化档的 GGUF
model_dir = snapshot_download(
    'Qwen/QwQ-32B-GGUF',
    allow_patterns='Qwen-32b-q4_k_m-gguf',
    local_dir='./qwq32b-q4km',
)

# 忽略非 GGUF 文件（避免下到 safetensors 原始权重）
model_dir = snapshot_download(
    'Qwen/Qwen2.5-7B-Instruct-GGUF',
    revision='master',
    local_dir='./qwen2.5-7b',
    ignore_patterns=['*.h5', '*.safetensors'],
)

# 私有模型鉴权 + 并发下载
model_dir = snapshot_download(
    'your/private-model',
    token='<TOKEN>',
    max_workers=8,
    local_dir='./private-model',
)
```

关键参数：`model_id`（必填）、`revision`、`local_dir`（优先于 `cache_dir`）、`allow_patterns` / `ignore_patterns`（glob 过滤）、`max_workers`（并发数）、`token`（私有模型鉴权）。

### 怎么找到 GGUF 仓库

在 ModelScope 站内直接搜 `GGUF`，仓库名通常带 `-GGUF` 后缀，文件形如 `model-<量化档>.gguf`。示例：`Qwen/QwQ-32B-GGUF`、`Qwen/Qwen2.5-7B-Instruct-GGUF`。

**为什么 GGUF 对 Ollama 友好**：Ollama 底层是 llama.cpp，GGUF 是它的原生格式，**下载即可用、无需转换**；而 safetensors 是原始权重，要先转成 GGUF 才能被 Ollama 吃进去。所以选仓库时认准 `-GGUF` 后缀。

### 环境变量与断点续传

| 环境变量 | 作用 |
|---------|------|
| `MODELSCOPE_CACHE` | 全局缓存根目录，默认 `~/.cache/modelscope/hub`（Windows 为 `C:\Users\<user>\.cache\modelscope\hub`） |
| `MODELSCOPE_ENDPOINT` | 服务端点，默认 `https://www.modelscope.cn`；⚠️ 旧变量 `MODELSCOPE_HUB_ENDPOINT`、`MODELSCOPE_DOMAIN` 已废弃 |
| `MODELSCOPE_DOWNLOAD_PARALLELS` | 并行下载数，默认 `1`，设为大于 1 才真正并行 |
| `MODELSCOPE_API_TOKEN` | 私有模型鉴权 token |

```bash
# Bash
export MODELSCOPE_DOWNLOAD_PARALLELS=4
```

```powershell
# PowerShell
$env:MODELSCOPE_DOWNLOAD_PARALLELS = "4"
```

**断点续传**：SDK 自动支持（`.incomplete` 临时文件 + Range 头 + 完成后 SHA256 校验），**无需显式传参**——下载中断后重跑同一条命令，就会接着上次的进度继续。

### 下载环节常见坑

| 坑 | 解决办法 |
|----|---------|
| 下载中断/慢 | SDK 自动断点续传；`MODELSCOPE_DOWNLOAD_PARALLELS>1`（文件须 >500MB）；加大超时 |
| 缓存路径混乱 | 用 `--local_dir` 显式指定，`--local_dir` 优先于 `--cache_dir` |
| 私有模型 403 | `modelscope login`，或 SDK 传 `token=` / 设置 `MODELSCOPE_API_TOKEN` |
| 下回来 Ollama 用不了 | 下到的是 safetensors 原始权重 → 改下 `-GGUF` 仓库 |
| 多个 `--exclude` 只有最后一个生效 | 改用 SDK 的 `ignore_patterns` 列表 |

### 本章小结

- 安装：`pip install modelscope`，之后 CLI / SDK 二选一
- CLI 用 `--local_dir` 显式指定落盘目录，它优先于 `--cache_dir`
- 找仓库认准 `-GGUF` 后缀；Ollama 能直接用 GGUF，safetensors 需先转换
- SDK 自动断点续传，中断后重跑同命令即续传
- 环境变量用 `MODELSCOPE_ENDPOINT`（`MODELSCOPE_HUB_ENDPOINT` 已废弃）

### 下一章预告

模型文件已经躺在本地了。下一章进入环节二：写一份 Modelfile，用 Ollama 把这份 GGUF 变成可以 `ollama run` 的本地模型。

---

## 第 3 章：环节二——用 Ollama 部署模型

上一章的产物是一份 GGUF 模型文件，现在进入环节二：用 Ollama 把这份文件「变成」能随时对话的本地模型。这一步做完，你就能在终端里 `ollama run` 自己的模型了。

### 安装 Ollama

Ollama 跨平台支持，按你的系统选一种方式：

| 平台 | 安装方式 | 说明 |
|------|---------|------|
| Windows | 运行 `OllamaSetup.exe` | 免管理员权限；GPU 加速需 NVIDIA 驱动 551.61+ |
| macOS | 把 `ollama.dmg` 拖进 Applications | 要求 Sonoma(14)+；Apple Silicon 支持 CPU+GPU |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` | 自动配置 systemd 服务 |

> [!tip] 大白话：Ollama 是什么
> 把 Ollama 想成一台「模型播放器」——GGUF 文件就像一首歌，ModelScope 负责把歌下载到本地，Ollama 就是那个能「播放」它的播放器。所以下载回来的 GGUF 只是原材料，要靠 Ollama 才能把它变成能对话的本地模型。

安装后验证：

```bash
ollama --version    # 确认安装成功
ollama serve        # 启动服务端，默认监听 127.0.0.1:11434
```

`ollama serve` 是后台服务，跑模型之前要确保它已经启动。

### 导入 GGUF：核心四步

Ollama 不能直接「认」一个孤零零的 GGUF 文件，需要先通过 Modelfile 登记入库。四步走：

```bash
# ① 放好 GGUF 文件（假设第 2 章下载到了 ./models/）
mkdir -p models && cp /path/to/model.gguf models/

# ② 写一份 Modelfile，描述这个模型
cat > Modelfile <<'EOF'
FROM ./models/model.gguf
PARAMETER temperature 0.8
PARAMETER num_ctx 4096
SYSTEM You are a helpful assistant.
EOF

# ③ 创建模型（给它起个名字）
ollama create my-model -f Modelfile

# ④ 运行验证
ollama run my-model
```

> [!tip] 大白话：Modelfile 是什么
> 把 Modelfile 想成一张「配货单」——GGUF 文件是食材，Modelfile 写清楚用哪块食材、火候（temperature）、锅的大小（num_ctx）、上菜规矩（SYSTEM）。所以 `ollama create` 就是照着配货单把模型打包成一个有名字的成品，之后 `ollama run my-model` 直接叫名字就能用。

跑通 `ollama run my-model`，出现对话提示符就说明部署成功。

### Modelfile 关键指令

| 指令 | 作用 |
|------|------|
| `FROM`（必填） | 基础模型：现有模型名 / GGUF 路径 / Safetensors 目录 |
| `PARAMETER` | 推理参数：`num_ctx`（默认 2048）、`temperature`（默认 0.8）、`top_k`、`top_p` 等 |
| `SYSTEM` | 系统提示词，设定模型身份与行为 |
| `TEMPLATE` | 完整提示词模板（Go template 语法）；手写会禁用自动检测 |
| `ADAPTER` | 加载 (Q)LoRA 微调适配器 |

### 量化基础：Q4_K_M 甜点位

量化 = 把 FP32/FP16 权重转成低精度，省显存、提速，代价是少量精度损失。第 2 章下载的 Q4_K_M 就是这个思路。

| 档位 | 体积 vs FP16 | 质量 | 速度 | 定位 |
|------|-------------|------|------|------|
| Q8_0 | 约 1/2 | 极佳 | 中 | 高保真 |
| **Q4_K_M** | **约 1/4** | **95-97%** | **快** | **推荐默认（甜点位）** |
| Q4_K_S | 约 1/4.5 | 可接受 | 很快 | 最大压缩 |

直观数字：7B 模型 FP16 ≈ 14GB，Q4_K_M ≈ 3.5GB，困惑度只升约 1%，速度提升 1.5-2 倍。所以入门选 Q4_K_M：省空间、跑得快、质量几乎无损。

如果你拿到的是 FP16/FP32 原始权重，导入时可以让 Ollama 自动量化：

```bash
ollama create -q Q4_K_M my-model
```

注意 `-q` 只支持 FP16/FP32 输入：不能量化已量化的模型，也不支持 IQ 系列量化档。

### 管理命令

```bash
ollama ls                        # 列出已创建的所有模型
ollama ps                        # 查看当前加载在内存中的模型
ollama stop my-model             # 把模型从内存中卸载
ollama rm my-model               # 删除模型
ollama show --modelfile my-model # 查看模型的 Modelfile 配置
ollama cp my-model my-backup     # 备份标签（不占额外磁盘空间）
ollama serve                     # 启动服务端
```

`ollama ls` 和 `ollama ps` 常被混用：`ls` 是「仓库里有谁」，`ps` 是「此刻谁被加载在内存里」。部署排查时先分清这两个。

### Ollama 环境变量

| 环境变量 | 作用 |
|---------|------|
| `OLLAMA_HOST` | 监听地址，默认 `127.0.0.1:11434` |
| `OLLAMA_CONTEXT_LENGTH` | 默认上下文长度（按显存自动：<24GiB=4k、24-48GiB=32k、≥48GiB=256k） |
| `OLLAMA_MODELS` | 模型存储目录 |
| `OLLAMA_KEEP_ALIVE` | 模型驻留内存时间，默认 5m；设 `-1` 常驻 |
| `OLLAMA_KV_CACHE_TYPE` | KV cache 量化（q8_0/q4_0），省显存 |
| `OLLAMA_NUM_PARALLEL` | 每个模型的并行请求数 |

最常用的调法是启动时带上上下文长度：

```bash
OLLAMA_CONTEXT_LENGTH=8192 ollama serve          # Bash
```

```powershell
$env:OLLAMA_CONTEXT_LENGTH = "8192"; ollama serve # PowerShell
```

### 部署环节常见坑

| 坑 | 解决办法 |
|----|---------|
| OOM（显存不足） | `ollama stop` 卸载；`OLLAMA_KEEP_ALIVE=0`；开 KV cache 量化；换更低量化档 |
| 上下文太短（默认 4k） | `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`；或在 Modelfile 里设 `num_ctx` |
| `ollama ls` 看不到模型 | `ollama ps` 只显示已加载进内存的模型；查列表用 `ollama ls` |
| 跑在 CPU 而非 GPU | `ollama ps` 看 Processor 列确认；Windows 需 NVIDIA 驱动 551.61+ |

### 本章小结

- 安装：Windows 跑 `OllamaSetup.exe`、macOS 拖 dmg、Linux 用官方脚本；`ollama --version` 验证，`ollama serve` 起服务
- 导入 GGUF 四步：放文件 → 写 Modelfile → `ollama create` → `ollama run` 验证
- Modelfile 核心是 `FROM`（必填）+ `PARAMETER` / `SYSTEM` / `TEMPLATE` / `ADAPTER`
- Q4_K_M 是甜点位：7B 约 3.5GB、质量 95-97%、速度快 1.5-2 倍；`ollama create -q Q4_K_M` 可自动量化（仅限 FP16/FP32 输入）
- 管理看 `ollama ls`（列表）vs `ollama ps`（内存中运行中的模型）
- 上下文太短、显存不足优先调 `OLLAMA_CONTEXT_LENGTH` 和 `OLLAMA_KEEP_ALIVE`

### 下一章预告

本地模型已经能跑起来了，但还只停留在终端里。下一章进入环节三：让 Claude Code 连上这个本地模型，用 `claude` 命令直接对话——数据不出本机。

---

## 第 4 章：环节三——让 Claude Code 接入本地 Ollama

上一章的 `ollama run` 让你能在终端里跟本地模型对话，但那只是「纯聊天」。现在进入环节三：把 Claude Code——面向 AI 编程的 CLI 助手——接到你本地的 Ollama 上（基础用法见 [[如何使用Claude code]]）。从此写代码、改 bug 都走本地推理，数据不出本机。

### 前提：版本与安装

要让 Claude Code 直连本地 Ollama，靠的是 Ollama 自带的 **Anthropic Messages API 兼容端点**（原生支持，无需第三方代理），但有版本门槛：

| 前提 | 要求 |
|------|------|
| Ollama 版本 | v0.14.0+（v0.15.0+ 另有 `ollama launch` 一键命令，下文会讲） |
| Claude Code | 已安装即可 |

Claude Code 的安装命令按系统选一种：

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

装好之后，终端里就能直接用 `claude` 命令了。

> [!tip] 大白话：ANTHROPIC_BASE_URL 是什么
> 把 Claude Code 想成寄信人，它默认把「请求信」寄到 Anthropic 官方服务器（出国）。`ANTHROPIC_BASE_URL` 就是「改地址」——把收件地址改成 `http://localhost:11434`，信就投进你本机的 Ollama 邮箱。所以设了这个变量，Claude Code 的一切请求都不再出国，只在你自己电脑里打转。

### 环境变量配置（核心）

接入的关键是四个环境变量，其中前三个**一个都不能错**：

| 变量 | 填什么 | 为什么 |
|------|--------|--------|
| `ANTHROPIC_BASE_URL` | `http://localhost:11434`（**不要加 `/v1` 后缀或尾斜杠**） | Claude Code 会自己在后面拼 `/v1/messages`，加多了反而 404 |
| `ANTHROPIC_AUTH_TOKEN` | `ollama`（任意非空值） | Ollama 端要求这个字段存在但内容被忽略，只作占位 |
| `ANTHROPIC_API_KEY` | **必须显式空字符串 `""`**（不是不设置） | 防止回落官方认证，见下方大白话 |
| `ANTHROPIC_MODEL` | 本地模型名（如 `qwen3-coder`） | 等价于启动时 `claude --model <名>` |

> [!tip] 大白话：为什么 API_KEY 要设空串
> 把 Anthropic 官方认证想成一张「门禁卡」。Claude Code 默认会先去刷官方门禁；如果你只是「不设置」`ANTHROPIC_API_KEY`，它手里可能还残留旧卡，就会反复尝试走官方认证、一直要求你登录。显式设成空串 `""` 等于「把旧卡没收」，逼它只能走 `ANTHROPIC_BASE_URL` 指的那个本机门。所以空串不是没意义，而是故意把官方通道关掉。

### 两种配置命令：Bash 与 PowerShell

**macOS / Linux（Bash/Zsh）**，在终端临时生效：

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
claude --model qwen3-coder
```

**Windows（PowerShell）**，写法对应改写：

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
claude --model qwen3-coder
```

这样启动后，`claude` 就会去连本机 Ollama 上的 `qwen3-coder` 模型。

### 一键方式：`ollama launch claude`（v0.15+）

如果你装的是 v0.15.0+ 的 Ollama，可以更省事——让 Ollama 自动选模型并直接拉起 Claude Code：

```bash
ollama launch claude                        # 自动选模型并启动
ollama launch claude --model qwen3-coder    # 指定模型
ollama launch claude --model gpt-oss:20b --yes -- -p "..."   # 非交互直接给提示词
```

### 持久化配置（推荐）

export 的方式只在当前终端窗口生效，新开一个终端就失效。想一劳永逸，把配置写进 `~/.claude/settings.json`（Windows 为 `%USERPROFILE%\.claude\settings.json`）的 `env` 块，新终端、后台 agent 都会自动生效：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

其中 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` 用来进一步关闭非必要外联，让流量更干净地留在本机。

### 工作原理：数据不出本机

配好之后，请求链路是这样的：

```
Claude Code → http://localhost:11434/v1/messages → Ollama → 本地模型推理
```

- 端点：`POST http://localhost:11434/v1/messages`，这是 Ollama 实现的 Anthropic Messages API
- 全程只在本机回环地址 `localhost` 上传输，**数据不出本机**
- 支持：`messages`（含 image / tool_use / tool_result / thinking）、`stream`、`tools`
- 不支持：`tool_choice`、`metadata`、`count_tokens`、`batches`、prompt caching、PDF 等

### 模型选型与硬件

连哪个模型，直接决定 Claude Code 好不好用：

| 模型 | 说明 |
|------|------|
| `qwen3-coder` | 官方推荐的编码模型（30B，至少 24GB 显存） |
| `gpt-oss:20b` | 官方推荐 |
| `glm-4.7:cloud` | 云端模型，免下载 |

- **上下文**：至少 32K，处理大仓库建议 64K：`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`
- **工具调用**：小模型（如 `gemma3:4b`、多数 7B）工具调用弱甚至缺失，会让 Claude Code 退化成纯文本生成器；量化档不建议低于 Q4_K_M
- **硬件预期**：本地推理「慢」是常态，先把预期放低，链路跑通再谈体验

### 备选方案对比（何时才需要）

官方原生方案是主线，多数人用不上备选。以下两个方案在「Ollama 版本过旧、对接非 Ollama 引擎、需要多供应商路由」时才需要考虑：

| 方案 | 用途 | 关键要点 |
|------|------|---------|
| claude-code-router | 多提供商路由 / 会话内 `/model` 切换 | 拦截请求按 model 字段转发；新版：`npm i -g @musistudio/claude-code-router && ccr ui` |
| LiteLLM | Anthropic ⇄ OpenAI 协议翻译代理 | 必须用 `ollama_chat/` 前缀（不是 `ollama/`）+ `drop_params: true`；`ANTHROPIC_BASE_URL=http://localhost:4000` |

判断标准：只要你的 Ollama ≥ v0.14，且只需要连本地模型，就用官方原生方案；要切换多家云端厂商、或接 LM Studio / vLLM 时，再引入备选。

### 接入环节常见坑

| 症状 | 解决办法 |
|------|---------|
| 模型 404 | `ollama ls` 查确切模型名；`ANTHROPIC_BASE_URL` 不带 `/v1` 或尾斜杠 |
| 一直要求登录 | 把凭据写进 `~/.claude/settings.json` 的 env 或 shell export，且 `ANTHROPIC_API_KEY=""` |
| 上下文不足 | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`；会话内 `/compact` |
| 工具调用失败 | 换编码向/工具向模型（`qwen3-coder`、`gpt-oss`、GLM-4）；量化不低于 Q4_K_M |
| Connection refused | 先确认 `ollama serve` 在跑；端口冲突改 `OLLAMA_HOST` 并同步改 base URL |
| VS Code 扩展不生效 | 在 VS Code 用户设置 `claudeCode.environmentVariables` 里配置 |

### 本章小结

- 前提是 Ollama v0.14.0+，提供原生 Anthropic Messages API 兼容端点；Claude Code 安装：Windows 用 `irm`，macOS/Linux 用 `curl`
- 核心是四个环境变量：`ANTHROPIC_BASE_URL` 不带 `/v1`、`ANTHROPIC_AUTH_TOKEN=ollama` 占位、`ANTHROPIC_API_KEY=""` 必须显式空串、`ANTHROPIC_MODEL` 指定模型
- v0.15+ 可 `ollama launch claude` 一键接入；推荐把配置持久化到 `~/.claude/settings.json` 的 env 块
- 请求全程走 `localhost:11434/v1/messages`，数据不出本机；但注意它不支持 prompt caching、PDF 等高级特性
- 编码干活选 `qwen3-coder`（30B / 24GB+ 显存）或 `gpt-oss:20b`；上下文给足 32K-64K，量化别低于 Q4_K_M
- 备选方案（claude-code-router / LiteLLM）只在 Ollama 过旧或对接非 Ollama 引擎时才需要

### 下一章预告

三环节已经逐个打通。下一章把这些步骤串成一条完整命令流，从零开始一路跑到 Claude Code 起来，并给出入门选型建议——先用 7B 模型跑通链路，再按显存升级编码模型。

---

## 第 5 章：端到端速通（从零到 Claude Code 跑起来）

上一章我们把 Claude Code 接上了本地 Ollama，三个环节各自都验证通过；这一章把它们串成一条完整命令流，从零一路跑到 `claude` 起来，并给出入门选型建议——先用 7B 小模型跑通链路，再按显存升级编码模型。

> [!tip] 大白话：整条链路像「食材采购 → 厨房加工 → 顾客点单」
> 把 ModelScope 想成菜市场，GGUF 是第 1 章说过的「预制菜」——直接买回家就能下锅；Ollama 是厨房里的那口锅，`ollama create` 就是把预制菜加工成一道有名字的成品菜，`ollama run` 是出锅试吃；Claude Code 则是下馆子的顾客，把需求写在菜单（请求）上递给后厨（Ollama），后厨做好后端上来。所以这三步**缺一不可，但顺序固定**：先买菜、再下厨、最后才能点单。

### 一条龙命令串讲

下面把三个环节浓缩成一份可直接复制的 Bash 全流程脚本。假设你已经装好 Python、Ollama 和 Claude Code（第 1 章清单），且已启动 `ollama serve`：

```bash
# ===== 环节 1：ModelScope 下载 GGUF 模型 =====
pip install modelscope
modelscope download --model 'Qwen/Qwen2.5-7B-Instruct-GGUF' --local_dir ./models

# ===== 环节 2：Ollama 部署 =====
# 写 Modelfile 并创建本地模型
cat > Modelfile <<'EOF'
FROM ./models/qwen2.5-7b-instruct-q4_k_m.gguf
PARAMETER temperature 0.6
PARAMETER num_ctx 32768
EOF
ollama create qwen2.5-7b -f Modelfile
ollama run qwen2.5-7b "你好"          # 先本地验证模型可用

# ===== 环节 3：Claude Code 接入 =====
# 临时方式：环境变量（新开终端会失效）
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
claude --model qwen2.5-7b
```

整条脚本的编排逻辑就是第 1 章的链路图：**下载 → 部署 → 接入**。`claude --model qwen2.5-7b` 启动后，你在 Claude Code 里发的每句话都会走 `localhost:11434` 由本机模型回答，数据不出本机。

### 每一步的验证检查点

跑脚本不是「执行完就算成功」，每步都要看到明确信号才继续：

| 环节 | 命令 | 看到什么算成功 |
|------|------|----------------|
| ① 下载 | `pip install modelscope` | 输出显示安装成功，无报错 |
| ① 下载 | `modelscope download ...` | `./models/` 下出现 `.gguf` 文件，且大小符合量化档预期（7B Q4_K_M 约 3.5-4GB） |
| ② 部署 | `ollama create qwen2.5-7b -f Modelfile` | 命令无报错结束；`ollama ls` 能看到 `qwen2.5-7b` 这一行 |
| ② 部署 | `ollama run qwen2.5-7b "你好"` | 模型能正常回复一段文字，而不是报 404 / 闪退 |
| ③ 接入 | `claude --model qwen2.5-7b` | 进入 Claude Code 交互界面，能发起对话且得到回答 |

其中 `ollama run` 的试吃环节最关键：**它是「模型本身能用」与「模型已接入 Claude Code」的分界线**。如果这里就回答不了，说明问题在下载或部署，而不是接入环节。

### 入门选型建议

首跑链路不要一上来就追大模型，按显存从低到高走：

| 阶段 | 建议 | 显存需求 |
|------|------|----------|
| 跑通链路 | 7B 级（如 `qwen2.5-7b`，Q4_K_M 约 3.5-4GB） | 8GB 内存起步即可，CPU 也能跑 |
| 编码干活 | `qwen3-coder` 等编码向模型 | 30B 需 24GB+ 显存 |
| 上限参考 | `gpt-oss:20b` | 20B 量级，按显存评估 |

先用 7B 小模型把整条链路跑通、确认环境没问题，再按显存升级 `qwen3-coder` 这类编码向模型。另外记得第 3、4 章的提醒：上下文给足 32K-64K，量化档不要低于 Q4_K_M，否则小模型的工具调用会变弱，Claude Code 容易退化成纯文本生成器。

### 失败时的排查入口

全流程最怕「不知道卡在哪一步」。记住一个原则：**哪一步失败，就回看哪一章**。

| 失败现象 | 大概率卡在 | 排查入口 |
|----------|-----------|----------|
| 下载中断 / 找不到 GGUF 文件 | 环节 ① | 回看第 2 章：断点续传、`--local_dir`、认准 `-GGUF` 后缀 |
| `ollama create` 报错 / `ollama run` 不回复 | 环节 ② | 回看第 3 章：Modelfile 的 `FROM` 路径、显存不足、上下文过短 |
| `claude` 连不上 / 一直要登录 / 模型 404 | 环节 ③ | 回看第 4 章：`BASE_URL` 不带 `/v1`、`API_KEY` 显式空串、`ollama serve` 是否在跑 |

按「症状 → 回看对应章」定位，比从头重跑一遍快得多。

### 本章小结

- 全流程是固定的三段式：`modelscope download` 拉 GGUF → `ollama create` + `ollama run` 部署验证 → 设三个环境变量后 `claude --model` 启动
- 每步都有明确的验证检查点；`ollama run` 是「模型本身能用」与「接入成功」的分界线
- 入门先上 7B 级 Q4_K_M（约 3.5-4GB）跑通链路，再按显存升级 `qwen3-coder` 等编码向模型
- 上下文给足 32K-64K，量化不低于 Q4_K_M，小模型工具调用才靠得住
- 失败排查按「哪一步失败回看哪一章」，不从头重跑

### 下一章预告

链路已经完整跑通。下一章收尾，把三环节最常见的坑整理成一张「症状 → 原因 → 解法」速查表，遇到问题直接翻表，不用再逐章找。

---

## 第 6 章：常见问题与避坑清单速查

第 5 章已经跑通全流程，但真正拦路的多半不是链路本身，而是几个零散的小细节。这一章把三个环节最容易踩的坑合并成一张速查表，外加四个高频易错细节，之后遇到问题直接翻本页，不用再逐章找。

### 三环节「症状 → 原因 → 解法」速查表

先按症状定位环节，再对号入座。每条解法都来自前面各章，可回看对应章补细节：

| 环节 | 症状 | 原因 | 解法 |
|------|------|------|------|
| ① ModelScope | 下载中断 / 慢 | 网络不稳 | 断点续传是自动的，重跑同一条命令即续传；`MODELSCOPE_DOWNLOAD_PARALLELS>1` 并行（文件须 >500MB） |
| ① ModelScope | 下完 Ollama 用不了 | 下成了 safetensors 原始权重 | 认准 `-GGUF` 仓库再下，Ollama 底层是 llama.cpp，GGUF 下载即用 |
| ① ModelScope | 私有模型 403 | 未鉴权 | `modelscope login`，或 SDK 传 `token=` / 设 `MODELSCOPE_API_TOKEN` |
| ② Ollama | OOM 显存不足 | 模型太大 / 常驻模型太多 | `ollama stop`；`OLLAMA_KEEP_ALIVE=0`；KV cache 量化；换更低量化档 |
| ② Ollama | 上下文太短 | 默认 `num_ctx` 只有 4k | `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`，或 Modelfile 里设 `num_ctx` |
| ② Ollama | 跑在 CPU 而非 GPU | 驱动或显存配置 | `ollama ps` 看 Processor 列；NVIDIA 驱动 ≥ 551.61 |
| ③ Claude Code | 模型 404 | 模型名不对 / `BASE_URL` 多了 `/v1` | `ollama list` 查确切名；`ANTHROPIC_BASE_URL` 不带 `/v1` 和尾斜杠 |
| ③ Claude Code | 一直要求登录 | 凭据没持久化 / `API_KEY` 未显式空串 | 写入 `~/.claude/settings.json` 的 `env` 块，且 `ANTHROPIC_API_KEY=""` |
| ③ Claude Code | Connection refused | `ollama serve` 没启动 / 端口被占 | 先启动 `ollama serve`；改 `OLLAMA_HOST` 后同步改 base URL |

### 易错细节汇总（4 个关键）

这四个细节错误率最高，配置时逐条对照：

**易错 1：`MODELSCOPE_HUB_ENDPOINT` 已废弃**

老教程常写 `MODELSCOPE_HUB_ENDPOINT`，新 SDK 已弃用，改用 `MODELSCOPE_ENDPOINT`：

```bash
export MODELSCOPE_ENDPOINT=https://www.modelscope.cn
```

**易错 2：`ANTHROPIC_BASE_URL` 带上了 `/v1`**

Claude Code 会自己拼 `/v1/messages` 路径，你只需给主机地址，不要加 `/v1` 或尾斜杠：

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434   # 别写成 http://localhost:11434/v1
```

**易错 3：`ANTHROPIC_API_KEY` 没设成显式空串**

「不设置」和「显式空字符串」是两回事。`ANTHROPIC_API_KEY=""` 才能防止 Claude Code 回落官方认证：

```bash
export ANTHROPIC_API_KEY=""
```

**易错 4：`ollama create -q` 输入须 FP16/FP32**

`ollama create -q Q4_K_M my-model` 的自动量化只接受 FP16/FP32 输入，拿已量化的模型再量化会失败。所以要么直接下 Q4_K_M 成品（免量化），要么用 FP16/FP32 原始权重让 Ollama 自动量化。

> [!tip] 大白话：为什么一个模型有这么多版本
> 把原始权重想成一张 4K 原图，Q8_0、Q4_K_M 就是压缩程度不同的 JPG——Q4_K_M 压缩约 4 倍、画质还剩 95% 以上，是默认甜点位，就像你不会每张照片都存原图。**所以**看到 `q4_k_m`、`q8_0` 这些后缀不必困惑，按显存挑一个即可；但也别拿已压缩的 JPG 再压一次，这就是 `-q` 只接受 FP16/FP32 的原因。

### 下一步进阶方向

链路稳定后，可按需往三个方向走：

| 方向 | 做法 | 何时需要 |
|------|------|----------|
| 协议 / 路由 | claude-code-router：`npm i -g @musistudio/claude-code-router && ccr ui`，会话内 `/model` 切换 | Ollama < v0.14，或需要多供应商路由 |
| 协议 / 路由 | LiteLLM：用 `ollama_chat/` 前缀 + `drop_params: true`，`ANTHROPIC_BASE_URL=http://localhost:4000` | 对接非 Ollama 引擎（LM Studio / vLLM） |
| 更大模型 | `qwen3-coder`（30B，至少 24GB 显存）、`gpt-oss:20b` | 7B 工具调用不够用、想正经干编码活 |
| 性能调优 | `OLLAMA_KEEP_ALIVE=-1` 常驻；`OLLAMA_KV_CACHE_TYPE=q8_0` 省显存；`OLLAMA_CONTEXT_LENGTH=64000 ollama serve` | 频繁切换慢、上下文不够、显存吃紧 |

### 本章小结

- 三个环节的坑都能归进「症状 → 原因 → 解法」：先定位环节，再按解法执行
- 四个高频易错：`MODELSCOPE_ENDPOINT` 替代旧变量、`BASE_URL` 不带 `/v1`、`API_KEY` 显式空串、`-q` 只吃 FP16/FP32
- 进阶三方向：claude-code-router / LiteLLM 解决协议与路由，更大模型提升能力，环境变量做性能调优

到这里，这条「ModelScope 下载 → Ollama 部署 → Claude Code 接入」的本地链路已经完整走通，剩下的交给你的显存与耐心，遇到问题随时翻回这一章。

---

## 相关笔记

- [[如何使用Claude code]] - Claude Code 基础使用入门
- [[Claude Code 模型与推理设置]] - Claude Code 模型与推理配置
- [[Claude Code CLI 完整参考]] - Claude Code 命令全集参考
- [[Codex手动配置指南]] - 另一款 CLI 工具的手动配置参考
- [[GLM系列模型完整对比]] - GLM 系列模型横向对比
