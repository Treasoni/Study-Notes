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
