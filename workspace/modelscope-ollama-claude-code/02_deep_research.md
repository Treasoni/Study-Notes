# 使用 ModelScope 拉取模型 + Ollama 部署 + Claude Code 使用 - 深度素材

- 收集时间: 2026-08-10
- 当前阶段: P2 深度收集
- 方向: A. 全流程主线（三环节串联）
- 素材来源: 官方文档为主 + 社区佐证，均经精读验证

---

## 素材质量概览

| 环节 | 官方文档 | 技术博客/社区 | 深度文章 | 质量结论 |
|------|---------|--------------|---------|---------|
| ModelScope 拉取 | 4（CLI/SDK/源码/文档中心） | 2 | 0 | ✅ 高 |
| Ollama 部署 | 6（import/modelfile/量化/安装/CLI/FAQ） | 2 | 1 | ✅ 高 |
| Claude Code 接入 | 5（兼容性/集成指南/博客/v0.15 release） | 4 | 2 | ✅ 高 |

> 三环节均有官方一手资料支撑，足以支撑实战教程写作。

---

# 第一部分：ModelScope（魔搭）拉取模型

## 1.1 下载方式总览

### CLI 方式（官方命令 `modelscope download`）

```bash
modelscope download [-h] --model MODEL [--revision REVISION]
                    [--cache_dir CACHE_DIR] [--local_dir LOCAL_DIR]
                    [--include [INCLUDE ...]] [--exclude [EXCLUDE ...]]
                    [files ...]
```

| 参数 | 说明 |
|------|------|
| `--model` | 模型 ID（必填） |
| `--dataset` | 数据集 ID |
| `--revision` | 模型版本/分支 |
| `--local_dir` | 直接下载到该目录；与 `cache_dir` 同时指定时 **local_dir 优先** |
| `--cache_dir` | 缓存目录，文件落于 `cache_dir/<org>/<model>/` |
| `--include` / `--exclude` | glob 通配符过滤；指定了具体文件则忽略 |

### Python SDK 方式（`snapshot_download`）

```python
from modelscope import snapshot_download
model_dir = snapshot_download('Qwen/Qwen2.5-7B-Instruct')

# 指定版本 + local_dir + 忽略格式
model_dir = snapshot_download(
    'Qwen/Qwen2.5-7B-Instruct',
    revision='master',
    local_dir='./qwen2.5-7b',
    ignore_patterns=['*.h5', '*.safetensors'],
)

# GGUF 只下某个量化档
model_dir = snapshot_download(
    'Qwen/QwQ-32B-GGUF',
    allow_patterns='Qwen-32b-q4_k_m-gguf',
    local_dir='./qwq32b-q4km',
)

# 私有模型鉴权 + 并发
model_dir = snapshot_download('your/private-model',
    token='<TOKEN>', max_workers=8, local_dir='./private-model')
```

关键参数：`model_id`（必填）、`revision`、`cache_dir`、`local_dir`（优先于 cache_dir）、`allow_patterns`/`ignore_patterns`（glob）、`max_workers`、`token`。

### 其他方式

- **Git LFS**：`git clone https://www.modelscope.cn/<owner>/<repo>.git`（需装 Git LFS）
- **网页下载**：模型详情页按钮

## 1.2 环境与网络

| 环境变量 | 说明 |
|---------|------|
| `MODELSCOPE_CACHE` | 全局缓存根目录，默认 `~/.cache/modelscope/hub`（Windows: `C:\Users\<user>\.cache\modelscope\hub`） |
| `MODELSCOPE_ENDPOINT` | 端点，默认 `https://www.modelscope.cn`（国内）⚠️ 最新 SDK 用它；`MODELSCOPE_HUB_ENDPOINT`/`MODELSCOPE_DOMAIN` 已弃用 |
| `MODELSCOPE_DOWNLOAD_PARALLELS` | 并行下载数，默认 `1`（设 >1 才真正并行） |
| `MODELSCOPE_PARALLEL_DOWNLOAD_THRESHOLD_MB` | 启用并行分片的大小阈值，默认 `500` |
| `MODELSCOPE_API_HTTP_CLIENT_TIMEOUT` | API 超时，默认 90s |
| `MODELSCOPE_API_TOKEN` | 私有模型鉴权 token |

**断点续传**：SDK 自动支持（`.incomplete` 临时文件 + Range 头 + 完成后 SHA256 校验），**无需显式传参**，重跑同一命令即续传。

## 1.3 在 ModelScope 找 GGUF 模型（对 Ollama 友好）

- 站内搜 `GGUF`，仓库名常带 `-GGUF` 后缀；文件名形如 `model-<量化档>.gguf`（`q4_k_m`、`q8_0`…）。
- **为何友好**：Ollama 底层是 llama.cpp，GGUF 是其原生格式，**下载即可用、无需转换**；safetensors 原始权重需先转 GGUF。
- 示例仓库：`Qwen/QwQ-32B-GGUF`、`Qwen/Qwen2.5-7B-Instruct-GGUF`（社区镜像）、`unsloth/Qwen3.5-4B-GGUF`。

## 1.4 常见坑

| 坑 | 解决办法 |
|----|---------|
| 下载中断/慢 | SDK 自动断点续传；`MODELSCOPE_DOWNLOAD_PARALLELS>1`（文件须 >500MB）；加大 timeout |
| 缓存路径混乱 | 用 `--local_dir` 显式指定；`local_dir` 优先于 `cache_dir` |
| 私有模型 403 | `modelscope login` 或 SDK `token=` / `MODELSCOPE_API_TOKEN` |
| 下载后 Ollama 不能用 | 下的是 safetensors 原始权重 → 直接下 `-GGUF` 仓库 |
| 多个 `--exclude` 只有最后生效 | 改用 SDK `ignore_patterns` 列表 |

---

# 第二部分：Ollama 本地部署

## 2.1 安装

| 平台 | 方式 |
|------|------|
| Windows | `OllamaSetup.exe`（免管理员）；可与 WSL2 二选一；GPU 需 NVIDIA 驱动 551.61+ |
| macOS | 拖 `ollama.dmg` 到 Applications；要求 Sonoma(14)+；Apple Silicon 支持 CPU+GPU |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh`；配 systemd 服务 |

验证：`ollama --version`、`ollama serve`（默认监听 `127.0.0.1:11434`）。

## 2.2 导入 GGUF 模型（核心流程）

```bash
# ① 放好 GGUF 文件
mkdir -p models && cp /path/to/model.gguf models/

# ② 写 Modelfile
cat > Modelfile <<'EOF'
FROM ./models/model.gguf
PARAMETER temperature 0.8
PARAMETER num_ctx 4096
SYSTEM You are a helpful assistant.
EOF

# ③ 创建（v0.1.35+ 可加 -q 自动量化）
ollama create my-model -f Modelfile

# ④ 运行验证
ollama run my-model
```

### Modelfile 关键指令

| 指令 | 作用 |
|------|------|
| `FROM`（必填） | 基础模型：现有模型名 / GGUF 路径 / Safetensors 目录 |
| `PARAMETER` | 推理参数（`num_ctx` 默认 2048、`temperature` 默认 0.8、`top_k`、`top_p`…） |
| `SYSTEM` | 系统提示词 |
| `TEMPLATE` | 完整提示词模板（Go template 语法） |
| `ADAPTER` | 加载 (Q)LoRA 适配器 |

### 自动量化 & 自动模板

- **v0.1.35+**：`ollama create -q Q4_K_M my-model` 导入时自动量化。仅支持 FP16/FP32 输入，不能量化已量化模型；不支持 IQ 系列。
- **v0.1.42+**：自动从 GGUF 元数据检测聊天模板；手写 `TEMPLATE` 会禁用自动检测。

## 2.3 量化基础（GGUF）

量化 = 把 FP32/FP16 权重转低精度，省显存、提速，代价是少量精度损失。

| 档位 | 大小 vs FP16 | 质量 | 速度 | 定位 |
|------|-------------|------|------|------|
| Q8_0 | ~2x 小 | 极佳 | 中 | 高保真 |
| **Q4_K_M** | **~4x 小** | **95-97%** | **快** | **推荐默认（甜点位）** |
| Q4_K_S | ~4.5x 小 | 可接受 | 很快 | 最大压缩 |

> 7B 模型直观数字：FP16≈14GB → **Q4_K_M≈3.5GB**，困惑度仅升 ~1%，速度 1.5-2x。

## 2.4 管理命令与环境变量

```bash
ollama ls                    # 列出模型
ollama pull llama3.2:8b      # 拉取官方模型
ollama show --modelfile my-model
ollama cp my-model my-backup # 备份标签（不占额外磁盘）
ollama rm my-model
ollama ps                    # 查看内存中运行的模型
ollama stop my-model         # 卸载
ollama serve                 # 启动服务端
```

| 环境变量 | 作用 |
|---------|------|
| `OLLAMA_HOST` | 监听地址，默认 `127.0.0.1:11434` |
| `OLLAMA_CONTEXT_LENGTH` | 默认上下文（按显存自动：<24GiB=4k、24-48GiB=32k、≥48GiB=256k） |
| `OLLAMA_MODELS` | 模型存储目录 |
| `OLLAMA_KEEP_ALIVE` | 驻留内存时间，默认 5m；`-1` 常驻 |
| `OLLAMA_KV_CACHE_TYPE` | KV cache 量化（q8_0/q4_0）省显存 |
| `OLLAMA_NUM_PARALLEL` | 每模型并行请求数 |

## 2.5 常见坑

| 坑 | 解决办法 |
|----|---------|
| OOM（显存不足） | `ollama stop`；`OLLAMA_KEEP_ALIVE=0`；KV cache 量化；换更低量化档 |
| 上下文太短（默认 4k） | `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`；或 Modelfile `num_ctx` |
| `ollama ls` 看不到 | 先 `ollama ls`；`ollama ps` 只显示已加载进内存的模型 |
| 跑在 CPU 而非 GPU | `ollama ps` 看 Processor 列；驱动 ≥551.61 |

---

# 第三部分：Claude Code 接入本地模型

## 3.1 官方原生方案（Ollama v0.14.0+，推荐主线）

> ⭐ **Ollama v0.14.0+ 提供 Anthropic Messages API 兼容端点**，Claude Code 无需 Anthropic API Key 即可直连本地 Ollama，数据留在本机。

### 前提

- Ollama **v0.14.0+**（v0.15.0+ 有 `ollama launch` 一键命令）
- Claude Code 已安装：macOS/Linux `curl -fsSL https://claude.ai/install.sh | bash`；Windows PowerShell `irm https://claude.ai/install.ps1 | iex`

### 环境变量（手动方式）

| 变量 | 填什么 | 为什么 |
|------|--------|--------|
| `ANTHROPIC_BASE_URL` | `http://localhost:11434`（**不要加 `/v1` 后缀/尾斜杠**） | Claude Code 自己拼 `/v1/messages` 路径 |
| `ANTHROPIC_AUTH_TOKEN` | `ollama`（任意非空值） | Ollama 端必填但忽略，仅占位 |
| `ANTHROPIC_API_KEY` | **必须空字符串 `""`**（不是不设置） | 防止回落官方认证 |
| `ANTHROPIC_MODEL` | 本地模型名（如 `qwen3-coder`） | 等价于 `claude --model` |

```bash
# Bash/Zsh
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
claude --model qwen3-coder
```

```powershell
# Windows PowerShell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
claude --model qwen3-coder
```

### 一键方式（v0.15+）

```bash
ollama launch claude                       # 自动选模型并启动
ollama launch claude --model qwen3-coder   # 指定模型
ollama launch claude --model gpt-oss:20b --yes -- -p "..."  # 非交互
```

### 持久化配置（推荐）

写入 `~/.claude/settings.json`（Windows 为 `%USERPROFILE%\.claude\settings.json`）的 `env` 块，新开终端/后台 agent 均生效：

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

### 工作原理

- 端点：`POST http://localhost:11434/v1/messages`（Ollama 实现的 Anthropic Messages API）
- 请求流：Claude Code → `localhost:11434` → Ollama → 本地模型推理，**数据不出本机**
- 支持：messages（含 image/tool_use/tool_result/thinking）、stream、tools 等
- 不支持：tool_choice、metadata、count_tokens、batches、prompt caching、PDF 等

## 3.2 模型选型

| 模型 | 说明 |
|------|------|
| `qwen3-coder` | 官方推荐编码模型（30B，至少 24GB 显存） |
| `gpt-oss:20b` | 官方推荐 |
| `glm-4.7:cloud` | 云端模型，免下载 |

- **上下文**：至少 32K，大仓库建议 64K（`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`）。
- **工具调用**：小模型（如 gemma3:4b、多数 7B）工具调用弱/缺失，会让 Claude Code 退化成纯文本生成器；量化下限建议 Q4_K_M。
- **硬件**：本地推理"慢"是常态，需管理预期。

## 3.3 备选方案（进阶对比）

| 方案 | 用途 | 要点 |
|------|------|------|
| **claude-code-router** | 多提供商路由 / 会话内 `/model` 切换 | 拦截请求按 model 字段转发；新版 `npm i -g @musistudio/claude-code-router && ccr ui` |
| **LiteLLM** | Anthropic⇄OpenAI 协议翻译代理 | 必须用 `ollama_chat/` 前缀（非 `ollama/`）+ `drop_params: true`；`ANTHROPIC_BASE_URL=http://localhost:4000` |

> 何时才需要备选：Ollama < v0.14、对接非 Ollama 引擎（LM Studio/vLLM）、需要多供应商路由或观测层。

## 3.4 常见坑

| 症状 | 解决办法 |
|------|---------|
| 模型 404 | `ollama list` 查确切名；`ANTHROPIC_BASE_URL` 不带 `/v1`/尾斜杠 |
| 一直要求登录 | 凭据写进 `~/.claude/settings.json` env 或 shell export，且 `ANTHROPIC_API_KEY=""` |
| 上下文不足 | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`；`/compact` |
| 工具调用失败 | 换编码向/工具向模型（qwen3-coder、gpt-oss、GLM-4）；量化不低于 Q4_K_M |
| Connection refused | 先 `ollama serve`；端口冲突改 `OLLAMA_HOST` 并同步改 base URL |
| VS Code 扩展不生效 | 在 VS Code 用户设置 `claudeCode.environmentVariables` 里配置 |

---

# 第四部分：端到端速通（全流程推荐路径）

```bash
# ===== 环节 1：ModelScope 下载 GGUF 模型 =====
pip install modelscope
modelscope download --model 'Qwen/Qwen2.5-7B-Instruct-GGUF' --local_dir ./models

# ===== 环节 2：Ollama 部署 =====
# 安装 Ollama 后，写 Modelfile 并创建
cat > Modelfile <<'EOF'
FROM ./models/qwen2.5-7b-instruct-q4_k_m.gguf
PARAMETER temperature 0.6
PARAMETER num_ctx 32768
EOF
ollama create qwen2.5-7b -f Modelfile
ollama run qwen2.5-7b "你好"        # 先本地验证模型可用

# ===== 环节 3：Claude Code 接入 =====
# 方式 A：环境变量（临时）
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
claude --model qwen2.5-7b

# 方式 B：持久化到 ~/.claude/settings.json 的 env 块
```

> 入门建议：先用 7B 级（Q4_K_M≈4GB）跑通链路，再根据显存升级 qwen3-coder 等编码模型。Claude Code 实际干活建议编码向模型。

---

# 第五部分：综合分析

1. **链路完整且官方化**：ModelScope 下载 → Ollama 部署 → Claude Code 接入，三环节均有官方文档，无黑盒。
2. **核心新能力**：Ollama v0.14.0+ 原生 Anthropic API 兼容，让「Claude Code 直连本地 Ollama」成为最简路径；旧资料多推 claude-code-router/LiteLLM，应作为进阶对比而非主线。
3. **最大现实瓶颈是硬件**：qwen3-coder(30B) 需 24GB+ 显存；入门档 7B Q4_K_M≈3.5-4GB 可跑但工具调用能力有限。笔记应给出「由低到高」的选型梯度。
4. **易错细节**：`MODELSCOPE_HUB_ENDPOINT` 已废弃→用 `MODELSCOPE_ENDPOINT`；`ANTHROPIC_BASE_URL` 不带 `/v1` 尾缀；`ANTHROPIC_API_KEY` 须显式空串；`ollama create -q` 输入须 FP16/FP32。
5. **信息缺口**：具体模型名与版本随时间变动，写作时应标注「以 ollama.com 官方模型库为准」；`ollama launch claude --config` 仅社区提及，需标注。

---

# 素材来源清单

## ModelScope
- CLI 文档: https://raw.githubusercontent.com/modelscope/modelscope/master/docs/source/command.md
- SDK 文档: https://tessl.io/registry/tessl/pypi-modelscope/1.29.0/files/docs/hub.md
- 源码: snapshot_download.py / file_utils.py / constants.py / modelscope_hub config.py / _download.py
- 官方下载文档中心: https://www.modelscope.cn/docs/models/download
- 社区: CSDN、GitCode 博客、阿里云开发者问答、issue #845

## Ollama
- 导入: https://docs.ollama.com/import
- Modelfile: https://docs.ollama.com/modelfile
- 量化: https://docs.ollama.com/advanced/model-quantization
- 安装: https://docs.ollama.com/windows.md / linux.md / macos.md
- CLI/FAQ/Context: https://docs.ollama.com/cli.md / faq.md / context-length.md
- v0.1.35/0.1.42 release notes

## Claude Code 接入
- Anthropic 兼容: https://docs.ollama.com/api/anthropic-compatibility
- 集成指南: https://docs.ollama.com/integrations/claude-code
- 官方博客: https://ollama.com/blog/claude
- v0.15.0: https://github.com/ollama/ollama/releases/tag/v0.15.0
- Anthropic LLM Gateway: https://code.claude.com/docs/en/llm-gateway-connect
- claude-code-router: https://github.com/musistudio/claude-code-router
- LiteLLM: https://docs.litellm.ai/docs/providers/ollama
- 社区: DevelopersIO、KDnuggets、PortOS
