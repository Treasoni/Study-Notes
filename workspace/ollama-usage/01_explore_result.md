# Ollama 使用文档 - 探测式收集结果

收集时间: 2026-08-10
阶段: P1 探测式收集
探测维度: 3 路并行 subagent

## 探测摘要

### 维度 1: 定位与安装入门

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Ollama 官方仓库 (GitHub) | https://github.com/ollama/ollama | 5/5 | 官方文档 |
| 2 | Ollama Quickstart | https://docs.ollama.com/quickstart | 5/5 | 官方文档 |
| 3 | Ollama 安装教程 (Windows/Linux) | https://cloud.tencent.com.cn/developer/article/2690559 | 4/5 | 技术博客 |
| 4 | Docker 部署 Ollama | https://cloud.tencent.cn/developer/article/2661078 | 4/5 | 技术博客 |

**关键发现**:
- 定位："用一行命令运行开源大模型"的本地 LLM 运行工具，基于 llama.cpp
- 安装：Windows `irm https://ollama.com/install.ps1 | iex` 或 `winget install Ollama.Ollama`；macOS/Linux `curl -fsSL https://ollama.com/install.sh | sh`；Docker 镜像 `ollama/ollama`
- 默认端口 `11434`；模型存储 `~/.ollama/models`；8GB 内存可跑 7B 模型（量化）

### 维度 2: 常用命令与模型管理

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Ollama CLI Reference | https://docs.ollama.com/cli | 5/5 | 官方文档 |
| 2 | Must Know Ollama Commands | https://itsfoss.com/ollama-commands/ | 4/5 | 技术博客 |
| 3 | Ollama 使用指南：技巧与问题解决 | https://cloud.tencent.cn/developer/article/2512663 | 4/5 | 技术博客 |
| 4 | Ollama 模型管理完全指南 | https://eastondev.com/blog/zh/posts/ai/20260402-ollama-model-management/ | 4/5 | 技术博客 |
| 5 | 模型文件默认存储位置与更改 | https://cloud.baidu.com/article/3368776 | 3/5 | 技术博客 |

**关键发现**:
- 核心命令：`run` / `pull` / `rm` / `ls` / `ps` / `stop` / `serve` / `show` / `cp` / `create -f Modelfile`
- 标签格式：`模型名:标签`（如 `qwen2.5:7b-q4_K_M`、`llama3.2:1b`）
- 更新模型 = 重跑 `ollama pull`；无独立 update 命令
- 默认路径：Windows `C:\Users\<用户>\.ollama\models`、Linux `/usr/share/ollama/.ollama/models`，用 `OLLAMA_MODELS` 修改

### 维度 3: 进阶用法与常见坑

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | OpenAI compatibility | https://docs.ollama.com/api/openai-compatibility | 5/5 | 官方文档 |
| 2 | 显存不足与 GPU 静默回退 (Issue) | https://github.com/ollama/ollama/issues/14258 | 5/5 | 社区讨论 |
| 3 | Modelfile Reference | https://docs.ollama.com/modelfile | 4/5 | 官方文档 |
| 4 | OLLAMA_HOST 等环境变量 (源码) | https://github.com/ollama/ollama/blob/main/envconfig/config.go | 4/5 | 官方文档 |
| 5 | Ollama API Introduction | https://docs.ollama.com/api/introduction | 4/5 | 官方文档 |

**关键发现**:
- OpenAI 兼容 API：`base_url=http://localhost:11434/v1`，api_key 填 `"ollama"`（被忽略），支持 chat/completions、embeddings、streaming、tools
- 显存坑：Ollama 显存不足时静默回退 CPU（无警告），用 `ollama ps` 看 PROCESSOR 列；对策：换量化版、降 num_ctx、`OLLAMA_NUM_GPU=0`
- Modelfile：类似 Dockerfile，`FROM`/`PARAMETER`/`SYSTEM`/`TEMPLATE`/`ADAPTER`，`ollama create 名称 -f Modelfile`，num_ctx 默认 2048
- 环境变量：默认监听 `127.0.0.1:11434`，跨设备需 `OLLAMA_HOST=0.0.0.0`；`OLLAMA_KEEP_ALIVE` 默认 5m；`OLLAMA_MODELS`
- 原生 API：`POST /api/generate`（无上下文）、`POST /api/chat`（多轮），默认流式 NDJSON

## 信源质量评估

- 官方文档覆盖充足：Quickstart、CLI Reference、Modelfile、API、OpenAI 兼容、envconfig 源码
- GitHub Issues 提供真实坑案例（显存回退）
- 中文博客内容同质化，仅精选 2-3 篇作为补充
- 整体素材足以支撑「入门到上手」的完整使用文档

## 候选学习方向

- **A. 全流程主线**：Ollama 是什么 → 安装 → 常用命令/模型管理 → 进阶（API/OpenAI 兼容/Modelfile）→ 常见坑（推荐，覆盖完整使用文档）
- **B. 安装与入门聚焦**：三平台 + Docker 安装、首次运行对话
- **C. API 集成聚焦**：HTTP API + OpenAI 兼容 SDK 调用（对接自己程序）
- **D. 模型管理聚焦**：pull/run/list/rm、量化选择、显存优化
