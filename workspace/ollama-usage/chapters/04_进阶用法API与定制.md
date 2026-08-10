---
title: "第四章 进阶用法：API / OpenAI 兼容 / Modelfile / 环境变量"
tags:
  - Ollama
  - API
  - Modelfile
  - 环境变量
created: 2026-08-10
---

# 第四章：进阶用法——API / OpenAI 兼容 / Modelfile / 环境变量

上一章我们已经能把模型拉下来、跑起来，学会用命令行管理本地模型了。但如果你想让 Ollama 真正「为你干活」——比如接进自己写的小程序、当某个现成客户端的本地后端、甚至按你的口味定制一个专属模型——光靠命令行是不够的。这一章我们把 Ollama 的「可编程性」一次打开：先认识它自带的 HTTP API，再看怎么用现成的 OpenAI SDK 无缝对接，然后用 Modelfile 定制自己的模型，最后学会用环境变量调整它的运行行为。

> 前置提示：本章所有示例中的模型名（如 `qwen2.5:7b`）只是示例。请先运行 `ollama list` 看看你机器上实际装了什么模型，把示例里的名字替换成真实存在的名字，命令才能跑通。

## 4.1 原生 HTTP API：Ollama 也是本地小服务器

你可能没意识到一件事：从你第一次 `ollama run` 开始，Ollama 就已经在你电脑里开了一个**本地 HTTP 服务**。你在终端里敲的每一句话，本质上都是这个服务在处理。现在我们把「服务」这层窗户纸捅破，你会看到 Ollama 的另一副面孔——一台随时待命的小服务器。

> [!tip] 大白话：本地小服务器
> 把 Ollama 想成你电脑里常驻的一家「本地小餐厅」——装好之后它就在 **11434 号桌**上待命，平时不主动打扰你。程序想找它聊天，就通过 HTTP 这个「送餐窗口」递一张纸条（请求），它回一张纸条（响应）。所以只要知道地址 `http://localhost:11434`，任何语言（curl、Python、Node.js……）都能跟它对话，完全不需要打开命令行界面。

### 4.1.1 服务地址：base_url

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

### 4.1.2 核心端点一览

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

### 4.1.3 第一次调用：`/api/generate`

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

### 4.1.4 流式 NDJSON vs `stream: false`

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

### 4.1.5 多轮对话：`/api/chat`

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
}
```

`messages` 里每条消息的 `role` 常见有四种：`system`（系统设定）、`user`（用户）、`assistant`（模型回答）、`tool`（工具调用返回）。`/api/chat` 会把整个历史一起发给模型，模型据此理解上下文，回答 `"那再加上 3 呢？"` 时知道是 `2 + 3 = 5`。

### 4.1.6 查模型详情：`/api/show`

想快速看某个模型的 Modelfile、参数、license 等信息，用 `/api/show`：

```bash
curl http://localhost:11434/api/show -d '{
  "model": "qwen2.5:7b"
}'
```

返回 JSON 里会有 `modelfile`、`parameters`、`license`、`template` 等字段。它跟命令行的 `ollama show --modelfile 模型名` 是同一件事的 API 版。

### 4.1.7 常用参数速查

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

### 4.1.8 从 Python 调用原生 API

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

## 4.2 OpenAI 兼容 API：用现成 SDK 无缝对接

原生 API 是 Ollama 自己的「方言」。但市面上大量的工具、库、客户端（比如各类 AI 聊天插件、`openai` 官方 Python 库）只认 OpenAI 的接口格式。Ollama 非常贴心地提供了一层**兼容层**：你照常用 OpenAI 的 SDK 和格式写代码，只把地址改到本地，就能调本地模型。

> [!tip] 大白话：api_key = 门禁卡
> 把 OpenAI 兼容接口想成一道门禁。云服务的门禁卡（api_key）必须由服务商签发、逐张校验；而 Ollama 这道门是**虚掩的**——形式上你必须刷一下卡（api_key 字段不能留空），但它根本不检查卡上的字，填 `"ollama"` 或随便什么字符串都能进。方便是方便，代价是它只信任「来敲门的都是本机自己人」，所以千万别把它暴露到公网（第 5 章细讲）。

### 4.2.1 就改两个东西

用 OpenAI 兼容 API，核心只需要改两个配置：

| 配置 | 值 | 说明 |
|------|-----|------|
| `base_url` | `http://localhost:11434/v1` | 注意前缀是 `/v1`，不是 `/api` |
| `api_key` | `"ollama"` | 必填但被忽略，随便填 |

### 4.2.2 Python 最小示例（openai SDK）

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

### 4.2.3 curl 示例

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

### 4.2.4 换回云端只需改两行

兼容层的最大价值是**切换零成本**。同样的代码，想从本地模型换回 OpenAI 云端，只需改两行：

```python
client = OpenAI(
    base_url="https://api.openai.com/v1",  # 云端地址
    api_key="sk-你的真实密钥",             # 云端需要真实密钥
)
```

其它所有 `client.chat.completions.create(...)` 调用一行都不用动。这就是「无缝对接」的含义——你的业务代码跟模型跑在哪无关。

### 4.2.5 兼容层支持哪些能力

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

## 4.3 Modelfile：定制自己的模型

你有没有过这种体验：每次调用都要在请求里写一遍「你是我的助手，请用中文、简洁地回答……」？或者想让模型默认用某种语气、固定上下文长度？这些「固定偏好」其实可以**烧进一个全新命名的模型里**——这就是 Modelfile 的用武之地。

> [!tip] 大白话：定制食谱
> 把 Modelfile 想成一份「定制食谱」。`FROM` 是食材（你选哪个基座模型，比如 `qwen2.5:7b`）；`PARAMETER` 是火候和佐料（temperature 多激进、num_ctx 锅有多大）；`SYSTEM` 是开饭前的「主厨训话」（模型每次回答前都会默念这段系统提示词）。`ollama create` 就是按这份食谱下锅，出锅后得到一个名字全新的专属模型。

### 4.3.1 什么是 Modelfile

Modelfile 是一个纯文本文件，类似 Dockerfile，但内容是「模型蓝图」。它由一行行**指令（INSTRUCTION）**组成，告诉 Ollama：从哪个基座模型开始、用什么参数、配什么系统提示词。然后用 `ollama create` 命令把它「构建」成一个可运行的模型。

### 4.3.2 核心指令一览

| 指令 | 作用 | 示例 |
|------|------|------|
| `FROM` | 指定基座模型（必填），也可以指向 GGUF/Safetensors 文件 | `FROM qwen2.5:7b` |
| `PARAMETER` | 设置推理参数 | `PARAMETER temperature 0.7` |
| `SYSTEM` | 设置系统提示词（每次对话都生效） | `SYSTEM 你是简洁的编程助手` |
| `TEMPLATE` | 自定义对话模板（Go 模板语法） | `TEMPLATE """{{.Prompt}}"""` |
| `ADAPTER` | 叠加 (Q)LoRA 微调权重 | `ADAPTER ./lora.gguf` |
| `MESSAGE` | 预设示例对话（few-shot 示例） | `MESSAGE user 你好` |

### 4.3.3 最小示例 + `ollama create`

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

### 4.3.4 查看模型的配置：`ollama show --modelfile`

想看看某个模型当初是用什么配置构建的（或者反推一个现成模型怎么调出来的）：

```bash
ollama show --modelfile my-coding-assistant
```

输出就是一份完整的 Modelfile 内容，包含所有指令和参数。这是排查「为什么这个模型回答风格这么怪」的第一站。

### 4.3.5 常用 `PARAMETER` 速查

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `temperature` | 0.8 | 越高越随机/有创意，越低越确定/保守 |
| `num_ctx` | 2048 | 上下文窗口长度（token 数），越大能记住越多但越吃显存 |
| `top_k` | 40 | 采样时只从概率最高的前 K 个 token 里选 |
| `top_p` | 0.9 | 核采样：累计概率达到该阈值的最小 token 集里采样 |
| `repeat_penalty` | 1.1 | 抑制重复内容，越大越不爱重复 |
| `seed` | 随机 | 固定随机种子后，相同输入可复现相同输出 |

### 4.3.6 `SYSTEM` 和 `TEMPLATE` 的区别

容易混淆的两个指令：

- `SYSTEM`：设定模型的**行为准则**，相当于「每次对话前先默念一遍这句话」。绝大多数定制需求用它就够了。
- `TEMPLATE`：控制「用户消息如何被拼成模型真正吃进去的格式」（比如 `{{.System}}`、`{{.Prompt}}`、`{{.Messages}}` 这些占位符怎么摆放）。一般**不需要改**——除非你明确知道自己在调什么，改错会导致模型输出乱套。

> [!tip] 实践建议
> 新手定制模型，记住三件套就够：`FROM`（选基座）、`PARAMETER`（调温度/上下文）、`SYSTEM`（定人设）。`TEMPLATE` 和 `ADAPTER` 属于进阶中的进阶，先留个印象即可。

## 4.4 环境变量：按需调整运行行为

有些行为——监听哪个地址、模型存在哪、模型驻留多久、能不能并发——不适合写在 Modelfile 或请求里，它们是**服务本身的属性**。这些由环境变量控制，Ollama 服务启动时读取一次。

> [!tip] 大白话：开机前设置
> 把环境变量想成服务器的「开机前设置」——就像你调整咖啡机的水温、研磨度，必须在**开机前**调好，开机之后再改就晚了。Ollama 服务只在启动时读一次这些设置，之后不再读取，所以改完必须**重启 Ollama** 才生效。

### 4.4.1 关键环境变量一览

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

### 4.4.2 Windows 上怎么设置

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

### 4.4.3 Linux（systemd）上怎么设置

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

### 4.4.4 三个最常用的组合场景

| 场景 | 需要的环境变量 | 效果 |
|------|---------------|------|
| 局域网内多台设备共用一台机器的模型 | `OLLAMA_HOST=0.0.0.0` + 防火墙放行 11434 | 其他设备可访问（务必先读第 5 章安全部分） |
| 频繁多轮对话、不想每次等加载 | `OLLAMA_KEEP_ALIVE=-1` | 模型常驻显存，响应更快，代价是显存一直被占 |
| C 盘空间紧张 | `OLLAMA_MODELS=D:\ollama-models` | 模型改存其他盘 |

> [!tip] 实践建议
> 环境变量是一把双刃剑：`OLLAMA_HOST=0.0.0.0` 和 `OLLAMA_KEEP_ALIVE=-1` 都很实用，但前者会打开安全缺口、后者会长期占用显存。建议按需开启，用不到就保持默认。

## 本章小结

- **原生 HTTP API**：Ollama 安装后就是一个本地 HTTP 服务，默认地址 `http://localhost:11434/api`，无需认证。核心端点有 `/api/generate`（单轮）、`/api/chat`（多轮）、`/api/tags`（列模型，**不是** `/api/models`）、`/api/show`（看详情）、`/api/embed`（向量）。默认流式返回 NDJSON，设 `"stream": false` 一次拿完整 JSON。
- **OpenAI 兼容 API**：把 `base_url` 设为 `http://localhost:11434/v1`、`api_key` 随便填（如 `"ollama"`），就能用现成的 OpenAI SDK 调本地模型。换回云端只需改这两行。
- **Modelfile 定制**：用 `FROM` 选基座、`PARAMETER` 调参数、`SYSTEM` 定人设，`ollama create 名称 -f Modelfile` 构建出专属模型，`ollama show --modelfile` 可查看已有模型的配置。
- **环境变量**：`OLLAMA_HOST` / `OLLAMA_MODELS` / `OLLAMA_KEEP_ALIVE` / `OLLAMA_NUM_PARALLEL` / `OLLAMA_CONTEXT_LENGTH` / `OLLAMA_FLASH_ATTENTION` 等控制服务行为，**改完必须重启 Ollama**。注意 `OLLAMA_NUM_GPU` 已在新版移除。
- **核心心智**：API 是把 Ollama 从「命令行玩具」变成「可编程组件」的钥匙；Modelfile 是把「每次都要重复的偏好」固化成「开箱即用的模型」；环境变量是「服务开机前的全局开关」。

## 下一章预告

这一章我们把 Ollama 的「可编程性」全部打开了，但进阶用法往往伴随着新的坑：为什么推理会突然变慢、下载卡住不动、局域网里别人访问不到你的服务、甚至模型裸奔在公网上？下一章我们进入「常见坑与最佳实践」，把这些实战中的拦路虎逐个拆掉——踩过坑再回来读，体感更佳。

---

**参考来源**

- Ollama HTTP API 官方文档：https://docs.ollama.com/api/introduction
- Ollama OpenAI 兼容官方文档：https://docs.ollama.com/api/openai-compatibility
- Ollama Modelfile 官方文档：https://docs.ollama.com/modelfile
- Ollama CLI 官方文档：https://docs.ollama.com/cli
- Ollama 环境变量源码 envconfig：https://github.com/ollama/ollama/blob/main/envconfig/config.go
