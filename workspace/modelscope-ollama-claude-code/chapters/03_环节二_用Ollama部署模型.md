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
