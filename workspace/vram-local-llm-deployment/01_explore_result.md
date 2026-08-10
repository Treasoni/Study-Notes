# 显存（VRAM）与本地部署大模型 - 探测结果

- **主题**: 显存（VRAM）与本地部署大模型
- **收集时间**: 2026-08-10
- **阶段**: P1 探测式收集（3 个并行 subagent，15 条候选资料）
- **学习深度**: 入门 | **用户基础**: 零基础 | **笔记类型**: 概念 + 实战混合

---

## 方向 1：显存基础概念

> 显存是什么、GPU/显存/内存的区别、容量 vs 带宽

| # | 标题 | URL | 相关性 | 摘要 |
|---|------|-----|--------|------|
| 1 | 一文看懂显卡的显存容量/频率/位宽/带宽 | https://diy.zol.com.cn/820/8202505.html | 5/5 | 水池/水管比喻讲透显存四大参数：容量=水池、频率=水流速度、位宽=水管粗细、带宽=进水速度；带宽=频率×位宽÷8 |
| 2 | 别再分不清显存和内存了！一文讲透AI算力的核心秘密 | https://developer.aliyun.com/article/1708501 | 5/5 | 厨房分工比喻区分 RAM 与 VRAM：CPU 用内存（备料台），GPU 用显存（猛火灶台）；显存带宽可达内存数十倍、成本百倍 |
| 3 | 什么是显存：GPU计算的核心存储单元解析 | https://cloud.baidu.com/article/3567924 | 4/5 | 显存 = 与 GPU 直连的高速存储；容量/带宽/位宽三大指标；延伸 CUDA 显存管理与 HBM3/CXL 演进 |
| 4 | 初探GPU：显存有何不同 | https://cloud.tencent.com.cn/developer/article/2702112 | 4/5 | 从 CPU/GPU 架构差异切入；内存求低延迟、显存求高带宽；DDR→GDDR→HBM 演进脉络 |
| 5 | PC Acronyms Explained: RAM vs VRAM | https://www.corsair.com/br/tw/explorer/diy-builder/memory/ram-vs-vram/ | 3/5 | 硬件厂商官方科普：VRAM 就是 GPU 的内存，焊死不可升级，想多只能换卡 |

**关键数据**：带宽 = 频率 × 位宽 ÷ 8；主流位宽 128/192/256bit、旗舰 384bit；显存带宽可达内存数十倍；HBM 带宽 2-5 TB/s

---

## 方向 2：大模型为什么吃显存

> 参数量、精度（FP16/INT8/INT4）、KV Cache、上下文长度

| # | 标题 | URL | 相关性 | 摘要 |
|---|------|-----|--------|------|
| 1 | 估算大模型所需显存（阿里云 PAI） | https://www.alibabacloud.com/help/zh/pai/product-overview/estimation-of-the-required-video-memory-for-the-model | 5/5 | 官方估算框架：显存 = 参数量 × 每参数字节数；FP16=2B/参数、INT8=1B、INT4=0.5B；推理再加 KV Cache + 激活值 + 开销，乘 1.2–2.5 安全系数 |
| 2 | How Much Memory Llama-3?（MLSys） | http://mlsysbook.ai/mlsysim/blog/how-much-memory-llama3.html | 5/5 | 以 Llama-3 逐项拆解推理显存：权重、激活值、KV Cache、峰值内存；KV Cache 随序列长度线性增长，长上下文可反超权重 |
| 3 | LLM 内存需求计算方式（阿里云开发者） | https://developer.aliyun.com/article/1685010 | 4/5 | 推理/训练内存构成逐项公式：权重、梯度、优化器状态、激活值、KV Cache；并行与量化降显存策略 |
| 4 | 使用 NVFP4 KV 缓存优化长上下文推理（NVIDIA） | https://developer.nvidia.cn/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/ | 4/5 | KV Cache 量化方案：16-bit→4-bit 显存降约 50%，上下文容量翻倍，精度损失约 1% |
| 5 | 模型大小和显存大小的关系（腾讯云） | https://cloud.tencent.com.cn/developer/article/2672598 | 3/5 | 不同精度（FP32/FP16/INT8/INT4）下模型大小与显存占用对比；量化让大模型跑上消费级显卡 |

**关键数据**：7B 模型 FP16 权重 ≈ 14GB、INT4 ≈ 3.5-4GB；KV Cache 随上下文长度线性增长，长上下文下可反超权重；全量微调内存系数约 18（7B ≈ 126GB）

---

## 方向 3：本地部署实战

> OOM、量化、选卡估算、Ollama / llama.cpp 工具链

| # | 标题 | URL | 相关性 | 摘要 |
|---|------|-----|--------|------|
| 1 | 国产开源 LLM 本地部署 2026 完整指南：硬件怎么挑 | https://ofox.ai/zh/blog/china-open-source-llm-local-deploy-hardware-guide-2026/ | 5/5 | 按参数量与量化档位给出显存需求矩阵与推荐显卡；显存≈参数量×位宽÷8+3GB |
| 2 | Ollama 官方文档 import.md（GGUF 导入与自动量化） | https://github.com/ollama/ollama/blob/main/docs/import.md | 5/5 | 官方权威：`ollama create -q Q4_K_M` 自动量化命令及全部量化档位；Q4_K_M 为通用首选 |
| 3 | 万字详解：普通开发者如何用 Ollama、llama.cpp 把大模型跑在本地消费级显卡 | https://developer.aliyun.com/article/1735788 | 5/5 | Ollama + llama.cpp 两条路线全流程、显存估算、量化选择、上下文配置；零基础 0→1 最优教程 |
| 4 | RTX4090 单卡跑 Qwen3-32B：4bit 量化 + Transformers 与 vLLM 双方案 | https://developer.aliyun.com/article/1754339 | 4/5 | 24GB 单卡跑 32B 级模型的实战；NF4 4bit 权重约 15GB；vLLM 用 gpu_memory_utilization 控制显存 |
| 5 | What AI Models Can You Run with 8/12/16/24/32 GB VRAM? | https://canitrun.net/blog/what-size-ai-model-can-i-run-with-8gb-vram/ | 4/5 | 按显存档位给出可对照模型清单（Q4_K_M 实际占用）；8GB 卡建议 ≤8B 模型 |

**关键数据**：7B Q4 ≈ 3.5-5GB（RTX 3060 12GB 可跑）；27B Q4_K_M ≈ 18GB；32B Q4_K_M ≈ 23GB；Qwen3-32B NF4 ≈ 15GB（4090 24GB 可跑）

---

## 综合分析

三个方向构成完整的学习链，与「概念 + 实战混合」的意图天然匹配：

1. **概念层**（方向 1）→ 显存是 GPU 的"工作台"，容量决定能装多大模型、带宽决定算得快不快；与内存最通俗的区分是"厨房备料台 vs 猛火灶台"
2. **原理层**（方向 2）→ 模型占用 = 参数量 × 每参数字节数（精度），推理时还要加 KV Cache（随上下文线性增长）；量化（INT4）可把显存需求压到 FP16 的 1/4
3. **实战层**（方向 3）→ 零基础可借助 Ollama / llama.cpp 落地；"我的显卡能跑多大模型"有现成公式和对照表

**信源质量**：官方文档级 4 条（阿里云 PAI、NVIDIA、Ollama、硬件厂商）、技术博客 11 条；近 2 年占比高，时效性满足入门要求。
