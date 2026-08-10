# 使用 ModelScope 拉取模型 + Ollama 部署 + Claude Code 使用 - 探测结果

- 收集时间: 2026-08-10
- 当前阶段: P1 探测式收集
- 输出目标: 生成方向菜单，供用户选择学习侧重

---

## 一、探索结果汇总

### 维度 1: ModelScope（魔搭）拉取模型

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | ModelScope 官方 CLI 下载文档 | https://raw.githubusercontent.com/modelscope/modelscope/master/docs/source/command.md | 5 | 官方 |
| 2 | ModelScope 官方 GitHub 仓库 | https://github.com/modelscope/modelscope | 5 | 官方 |
| 3 | 魔搭社区官方文档：模型的下载 | https://www.modelscope.cn/docs/models/download | 5 | 官方 |
| 4 | ModelScope 下载模型三种方式（CSDN） | https://blog.csdn.net/a772304419/article/details/151364347 | 4 | 社区 |
| 5 | fagao-ai/mget 多源模型下载器 | https://github.com/fagao-ai/mget | 4 | 社区 |

**要点**：
- 官方推荐 `modelscope download --model <MODEL_ID>`（CLI）或 `snapshot_download`（Python SDK），`pip install -U modelscope` 后即可用。
- 关键参数：`--local_dir`（指定下载位置，优先级高于 `--cache_dir`）、`--include/--exclude` 通配符过滤、断点续传 `resume_download=True`。
- 国内网络优化：`MODELSCOPE_CACHE` 自定义缓存路径、`MODELSCOPE_HUB_ENDPOINT=https://modelscope.cn` 强制国内源。
- 私有模型需 `modelscope login --token` 后下载。

### 维度 2: Ollama 本地部署

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Ollama 官方文档：Importing a Model | https://docs.ollama.com/import | 5 | 官方 |
| 2 | Ollama 官方文档：Modelfile Reference | https://docs.ollama.com/modelfile | 5 | 官方 |
| 3 | Ollama 量化文档 | https://docs.ollama.com/advanced/model-quantization | 5 | 官方 |
| 4 | GitHub Issue #13760：本地 GGUF 导入需求 | https://github.com/ollama/ollama/issues/13760 | 4 | 社区 |
| 5 | Ollama Modelfile 使用手册（阿里云） | https://developer.aliyun.com/article/1709641 | 3 | 博客 |

**要点**：
- 导入本地 GGUF：Modelfile 中写 `FROM ./model.gguf`，然后 `ollama create my-model -f Modelfile`。
- `ollama create -q Q4_K_M mymodel` 可在导入时自动量化 FP16/FP32 模型（v0.1.35+）；v0.1.42+ 自动检测 chat template。
- 量化 Q4_K_M 是甜点位：体积约为 FP16 的 1/4（7B 约 14GB→3.5GB），保留 95-97% 质量，速度提升约 1.5-2x。
- 也可以直接用 `ollama run hf.co/用户名/模型:UD-Q4_K_XL` 从 Hugging Face 拉取。

### 维度 3: Claude Code 接入本地模型

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Ollama 官方文档：Anthropic API 兼容性 | https://docs.ollama.com/api/anthropic-compatibility | 5 | 官方 |
| 2 | Ollama 官方文档：Claude Code 集成指南 | https://docs.ollama.com/integrations/claude-code | 5 | 官方 |
| 3 | claude-code-router（多提供商路由代理） | https://github.com/musistudio/claude-code-router | 4 | 社区 |
| 4 | KDnuggets: Pairing Claude Code with Local Models | https://www.kdnuggets.com/pairing-claude-code-with-local-models | 4 | 博客 |
| 5 | local-ai-coding-stack（LiteLLM 接入合集） | https://github.com/renezander030/local-ai-coding-stack | 4 | 社区 |

**要点**：
- **Ollama v0.14.0+ 原生支持 Anthropic Messages API 兼容端点**：Claude Code 设 `ANTHROPIC_BASE_URL=http://localhost:11434`、`ANTHROPIC_AUTH_TOKEN=ollama` 即可直接用本地模型，无需 Anthropic API Key，数据留在本机。
- Ollama v0.15 起可用 `ollama launch claude` 自动配置。
- 推荐编码模型：qwen3-coder、gpt-oss:20b、glm-4.7 等；上下文至少 32K，推荐 64K（`OLLAMA_CONTEXT_LENGTH=65536`）。
- 备选方案：claude-code-router（多提供商路由、会话内 `/model` 切换）、LiteLLM（协议翻译，必须用 `ollama_chat/` 前缀 + `drop_params: true`）。
- 注意：小模型工具调用失败率 35-85%，1.5B 级基本不可用于 Claude Code；建议 32GB+ 内存。

---

## 二、综合分析

1. **链路已打通**：ModelScope（下载）→ Ollama（部署，Modelfile + GGUF）→ Claude Code（接入）三环节都有官方文档，且 Ollama 已原生提供 Anthropic 兼容 API，这是当前最简单、最权威的接入方式。
2. **最简路径**：`modelscope download` 拿到模型 → 转/配 GGUF 用 Modelfile `ollama create` → 设两个环境变量 + `claude --model` 启动。
3. **主要风险点**：① ModelScope 下载时的国内网络与断点续传；② 模型须为 GGUF 或可量化格式；③ 本地硬件（显存/内存）决定能跑的模型档位；④ 小模型工具调用能力弱，选型要避开。
4. **信息时效**：Ollama 的 Anthropic 兼容属于较新能力（v0.14.0+），旧资料多推荐 claude-code-router/LiteLLM 代理方案，可作为进阶对比。

---

## 三、方向菜单

- **A. 全流程主线（三环节串联）**：ModelScope 下载 → Ollama 部署 → Claude Code 接入，一步不落，附硬件选型。适合「入门上手」目标。
- **B. 以 Claude Code 接入为中心**：重点讲官方 Anthropic 兼容方案（环境变量、模型要求、常见坑）+ 备选代理方案对比。
- **C. 以 ModelScope 下载为中心**：重点讲下载方式（CLI/SDK/Git）、国内源、断点续传、批量下载与私有模型。
- **D. 以 Ollama 部署为中心**：重点讲 Modelfile、GGUF 导入、量化档位选择、服务与性能。

> 选择后进入 P2 深度收集，按所选方向做精读与素材沉淀。
