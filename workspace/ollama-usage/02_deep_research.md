# Ollama 使用文档 - 深度收集素材

收集时间: 2026-08-10
阶段: P2 深度收集
方向: A. 全流程主线（是什么 → 安装 → 命令/模型管理 → 进阶 → 常见坑）
信源: 官方文档为主（docs.ollama.com / GitHub），技术博客与社区补充

---

## 1. Ollama 是什么

- **定位**: "用一行命令运行开源大模型"的本地 LLM 运行工具，自带 REST API 与官方 Python/JS 库
- **核心卖点**: 一条命令下载并运行模型；数据不出本机（隐私）；跨平台
- **底层引擎**: llama.cpp（Georgi Gerganov 发起）；支持 llama、gemma、qwen、mistral、deepseek 等主流开源模型
- **类比（大白话）**: 像「本地版应用商店 + 运行时」——商店负责下载模型，运行时负责在电脑上跑起来；也像把 ChatGPT 搬回家，断网也能用，聊天数据不出本机
- **与云端 API 对比**: 本地推理免 API 费用、隐私可控、离线可用；需自备算力（显存/内存），性能取决于硬件

## 2. 安装与快速开始

### 平台安装
| 平台 | 安装方式 | 要求 |
|------|---------|------|
| Windows | 下载 `OllamaSetup.exe`；或 `winget install Ollama.Ollama`；或 `irm https://ollama.com/install.ps1 \| iex` | Win10 22H2+，原生无需 WSL，安装需 ~4GB 磁盘，默认装用户目录免管理员 |
| macOS | 下载 `ollama.dmg` 拖入 Applications | Sonoma 14+；M 芯片支持 GPU，Intel 仅 CPU |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` | 注册为 systemd 服务；NVIDIA 需 CUDA 驱动，AMD 需 ROCm |
| Docker | `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama` | GPU 加 `--gpus=all`（需 nvidia-container-toolkit）或 `:rocm` 标签 |

### 快速开始
- `ollama run gemma4`（或 llama3.2 等）进入对话；`/bye` 退出
- 验证安装: `ollama --version`、`ollama list`
- Docker 内: `docker exec -it ollama ollama run llama3.2`

### 关键路径/默认值
- 默认 API 端口: `127.0.0.1:11434`
- 模型存储: macOS `~/.ollama/models`；Linux `/usr/share/ollama/.ollama/models`；Windows `C:\Users\<用户名>\.ollama\models`；容器 `/root/.ollama`
- 服务方式: Windows/macOS 为后台应用；Linux 为 systemd 服务（`ollama serve`）；Docker 为容器
- `OLLAMA_MODELS` 改存储路径，`OLLAMA_HOST` 改端口

## 3. CLI 命令与模型管理

### 命令全集
| 命令 | 用途 | 示例 |
|------|------|------|
| `run` | 交互式聊天/单次提问 | `ollama run llama3`；`ollama run llama3 "问题"`；多行输入用 `"""` 包裹 |
| `pull` | 下载模型 | `ollama pull qwen2.5:7b` |
| `rm` | 删除模型释放空间 | `ollama rm llama3` |
| `ls` / `list` | 列本地模型（NAME/ID/SIZE/MODIFIED） | `ollama list` |
| `ps` | 列运行中模型（NAME/ID/SIZE/PROCESSOR/CONTEXT/UNTIL） | `ollama ps` |
| `stop` | 停止运行中的模型 | `ollama stop llama3` |
| `serve` | 启动本地服务 | `ollama serve --help` |
| `show` | 查看模型详情 | `ollama show --modelfile 模型名`；`--parameters`/`--license` |
| `cp` | 复制/改名 | `ollama cp llama3.2 my-model` |
| `create` | 从 Modelfile 造模型 | `ollama create 名称 -f Modelfile` |
| `push` | 上传到 registry | `ollama push 用户名/模型` |

### 模型管理流程
- **拉取/切版本**: `ollama pull 模型:tag`；tag 格式 `模型名:参数量-量化`（如 `qwen2.5:7b-q4_K_M`）；不带 tag 默认 `latest`；不同 tag 并存
- **更新**: 重跑 `ollama pull 同名模型` 即拉最新版（无独立 update 命令）
- **删除**: `ollama rm 模型` 清磁盘
- **查看**: `ollama list`（本地模型）；`ollama ps`（运行中，PROCESSOR 显示 CPU/GPU 占比，UNTIL 为自动卸载倒计时，默认保活 5 分钟）
- **复制**: `ollama cp 源 目标`（改名/备份后 push）

### 模型库与量化
- **挑选**: 按参数规模（7b/8b/70b，MoE 用 `8x7b`）+ 能力标签（vision/tools/thinking/embedding）+ 显存；小模型快省显存，大模型更聪明
- **量化（GGUF 压缩权重）**:
  - `f16` 原版最准最大
  - `q8_0` 近无损、约一半体积
  - `q4_K_M` 约 1/4 体积、质量约 96%，显存/质量平衡首选（8GB 显存首选）
  - 质量排序: f16 > q8_0 > q5_K_M > q4_K_M
- **类比（大白话）**: 模型仓库像应用商店，tag 像版本号；量化好比 JPEG——RAW 原图清晰但巨大，q4_K_M 是"高清又不占空间"的平衡档

## 4. 进阶用法：API / OpenAI 兼容 / Modelfile / 环境变量

### 原生 HTTP API
- base_url: `http://localhost:11434/api`，默认端口 11434，**无需认证**
- 核心端点（POST）: `/api/generate`（单轮补全）、`/api/chat`（多轮对话）、`/api/tags`（列出已装模型）、`/api/embed`（向量嵌入）、`/api/pull`、`/api/show`
- 默认流式: NDJSON（每行一个 JSON，末尾 `"done":true` 含 token 统计）；设 `"stream":false` 返回单个 JSON
- 常用参数: `model`、`prompt`（generate）/`messages`（chat，含 system/user/assistant/tool 角色）、`options`（temperature、top_p、seed、num_ctx）、`keep_alive`（如 `"5m"`，`0` 立即卸载）、`format`（`"json"` 或 JSON Schema 约束输出）
- 注: `/api/models` 端点实际不存在，列表用 `/api/tags`

### OpenAI 兼容 API（零基础 SDK 用法）
- base_url = `http://localhost:11434/v1`；api_key 填任意值如 `"ollama"`（**必填但被忽略**）
- 端点: `/v1/chat/completions`（支持流式、tools 函数调用、JSON mode、vision 仅 base64）、`/v1/embeddings`、`/v1/models`、`/v1/completions`
- Python（openai SDK）最小示例:
  ```python
  from openai import OpenAI
  c = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
  r = c.chat.completions.create(model="qwen3:8b",
      messages=[{"role":"user","content":"你好"}])
  print(r.choices[0].message.content)
  ```
- curl 示例:
  ```bash
  curl http://localhost:11434/v1/chat/completions -d '{
    "model":"qwen3:8b",
    "messages":[{"role":"user","content":"你好"}]}'
  ```
- **跨设备访问**: 设 `OLLAMA_HOST=0.0.0.0` 并重启 Ollama；需放行防火墙 11434 端口
- **类比（大白话）**: Ollama 像本地一台小服务器，装好即在 11434 端口待命；程序通过 HTTP API（或 OpenAI 兼容接口）"找它聊天"

### Modelfile（自定义模型）
- **是什么**: 类似 Dockerfile 的模型蓝图，纯文本逐条 `INSTRUCTION` 声明，用命令"构建"成可运行模型
- **核心指令**: `FROM`（基底模型，必填，也可指向 GGUF/Safetensors）、`PARAMETER`（推理参数）、`SYSTEM`（系统提示词）、`TEMPLATE`（Go 模板如 `{{.Prompt}}`）、`ADAPTER`（叠加 (Q)LoRA 微调）、`MESSAGE`（预设示例对话）
- **最小示例**:
  ```
  FROM llama3.2
  PARAMETER temperature 1
  PARAMETER num_ctx 4096
  SYSTEM You are a helpful assistant.
  ```
  构建: `ollama create 模型名 -f Modelfile`
- **常用 PARAMETER**: `temperature`(0.8)、`num_ctx`(默认 2048)、`top_k`(40)、`top_p`(0.9)、`repeat_penalty`(1.1)、`seed`
- **查看配置**: `ollama show --modelfile 模型名`
- **类比（大白话）**: Modelfile 像"给模型的定制食谱"——FROM 是食材（基座模型），PARAMETER/SYSTEM 是火候与口味，`ollama create` 按食谱出锅

### 环境变量（关键）
| 变量 | 默认 | 说明 |
|------|------|------|
| `OLLAMA_HOST` | `127.0.0.1:11434` | 改 `0.0.0.0` 可跨设备访问 |
| `OLLAMA_MODELS` | `~/.ollama/models` | 模型存储目录 |
| `OLLAMA_KEEP_ALIVE` | `5m` | 模型驻留显存时长；`-1` 常驻，`0` 用完即退 |
| `OLLAMA_NUM_PARALLEL` | `1` | 单模型并发请求数（显存≈并发×上下文） |
| `OLLAMA_MAX_LOADED_MODELS` | `3×GPU数` | 常驻模型数 |
| `OLLAMA_CONTEXT_LENGTH` | 按显存自适应 | 全局上下文覆盖 |
| `OLLAMA_FLASH_ATTENTION` | 关 | `1` 开启省显存 |

- 注: `OLLAMA_NUM_GPU` 在新版本已移除，层调度全自动；Windows 改环境变量后需重启 Ollama

## 5. 常见坑与对策

| 坑 | 现象 | 对策 |
|----|------|------|
| 显存不足静默回退 CPU | 无警告但变慢 | `ollama ps` 看 PROCESSOR 列；换小模型/量化版；`OLLAMA_FLASH_ATTENTION=1`、`OLLAMA_KV_CACHE_TYPE=q8_0` 省显存 |
| 下载慢/镜像 | 模型体积大（几十 GB） | 官方无镜像配置；用代理 `HTTPS_PROXY`；WSL2 关闭网卡 Large Send Offload V2 |
| 端口/防火墙 | 无法访问 11434 | 默认只监听 127.0.0.1；跨设备需 `OLLAMA_HOST=0.0.0.0` + 放行防火墙 |
| 安全暴露 | API 无认证 | 勿随意设 `0.0.0.0`；需暴露建议反向代理 + 鉴权；跨域用 `OLLAMA_ORIGINS` 白名单 |

---

## 信源清单

| # | 来源 | 类型 | 覆盖 |
|---|------|------|------|
| 1 | https://docs.ollama.com/quickstart | 官方文档 | 安装/快速开始 |
| 2 | https://docs.ollama.com/cli | 官方文档 | CLI 命令 |
| 3 | https://docs.ollama.com/modelfile | 官方文档 | Modelfile |
| 4 | https://docs.ollama.com/api/introduction | 官方文档 | HTTP API |
| 5 | https://docs.ollama.com/api/openai-compatibility | 官方文档 | OpenAI 兼容 |
| 6 | https://github.com/ollama/ollama | 官方仓库 | 定位/README |
| 7 | https://github.com/ollama/ollama/blob/main/envconfig/config.go | 官方源码 | 环境变量 |
| 8 | https://github.com/ollama/ollama/issues/14258 | 社区 | 显存坑 |
| 9 | https://ollama.com/library | 官方 | 模型库 |
| 10 | 腾讯云/It's FOSS/CSDN 等博客 | 技术博客 | 中文补充 |

## 素材质量评估

- 官方文档覆盖充分（Quickstart / CLI / Modelfile / API / OpenAI 兼容 / envconfig 源码）
- 真实坑案例来自 GitHub Issues，可信
- 中文博客同质化高，仅作补充
- **结论**: 素材足以支撑「入门到上手」概念的完整使用文档（预计 5 章）

## 信息缺口（写作时注意）

- 官方文档示例中的模型名（gemma4、qwen3:8b）为占位符，实际以 `ollama list` 为准
- 新版环境变量与旧教程有差异（如 OLLAMA_NUM_GPU 已移除），写作时以官方为准并注明版本
