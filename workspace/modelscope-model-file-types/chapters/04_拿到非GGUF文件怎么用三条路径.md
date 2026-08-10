# 拿到非 GGUF 文件怎么用：三条路径

前两章把文件本身讲完了：权重有四种格式，配置和分词器是模型的「说明书」。现在回答最实际的问题——你下载了一个只有 `.safetensors` 分片和一堆 `.json` 的原始仓库，里面没有现成的 GGUF，到底怎么把它跑起来？

其实原始权重有三条完全可走的路：直接用 Transformers 加载、转成 GGUF 喂给 Ollama/llama.cpp、丢给 vLLM 做生产服务。这一章三条路都给你可复制的命令，并讲清各自适合什么场景、有什么坑。还记得第 1 章的比喻吗？safetensors 是「生食材」，现在的问题就是：这袋生食材要怎么做成能上桌的菜。

## 4.1 路径 A：Transformers / ModelScope 直接推理

**适合**：跑通验证、做原型、抽 embedding、微调前检查模型能不能用。这是「成本最低、最快见到效果」的路。

第一步，把模型下载到本地。用 Python SDK 可以按后缀过滤，只下权重、配置和自定义代码：

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    local_dir="./models/Qwen2.5-7B",
    allow_patterns=["*.safetensors", "*.json", "*.py"],  # 只下权重+配置+自定义代码
)
```

第二步，加载并推理：

```python
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.bfloat16,  # 不传默认 fp32，7B 约 28GB 必 OOM
    device_map="auto",           # 显存不够自动溢到 CPU/磁盘
    trust_remote_code=True,      # 仓库有自定义 modeling_*.py 时必须开
)

messages = [{"role": "user", "content": "用三句话解释什么是 KV Cache"}]
inputs = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, return_tensors="pt"
).to(model.device)
out = model.generate(inputs, max_new_tokens=512, do_sample=False)
print(tokenizer.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True))
```

四个关键参数逐个说清 [Transformers 加载文档](https://huggingface.co/docs/transformers/main/en/main_classes/model)：

- `torch_dtype`：权重精度。不传默认 fp32（每参数 4 字节），7B 就要约 28GB 显存，小卡直接 OOM；设 `bfloat16` 减半到约 14GB。
- `device_map="auto"`：让框架自动分配 GPU/CPU 甚至磁盘，显存不够时「溢出」到 CPU 而不是崩掉。
- `trust_remote_code=True`：有些模型的架构不在官方框架里，仓库自带 `modeling_*.py` 自定义代码，不开这个开关会报 KeyError / 找不到模型类。
- `local_files_only=True`：纯离线环境加上它，强制只用本地文件、绝不联网（ModelScope 与 HuggingFace 布局互通，下载到本地后可离线加载）。

**坑**：
- 忘 `torch_dtype` → OOM，这是最经典的入门坑。
- 有自定义代码没开 `trust_remote_code` → KeyError，属于「静默错误」，报错不明显。
- 吞吐低、无并发：一次只能处理一个请求，不适合服务多人。

> [!tip] 大白话
> `torch_dtype` 就像决定用多大的盘子装菜：默认 fp32 是「豪华大盘」，7B 的菜光装盘就要占 28GB 桌位，小桌（小显存）一摆就爆；换成 bfloat16 就是「精简餐盘」，占位减半。所以新手最常犯的错，就是忘了换小盘直接 OOM。

> [!tip] 大白话
> `trust_remote_code` 相当于「允许厨师用私房菜谱」。有的模型用了框架之外的独门手艺（仓库里的 modeling_*.py），你不点头，餐厅管理员（框架）就拒绝让这位厨师开工，报 KeyError。开之前最好瞄一眼这份菜谱，确认没下毒——毕竟是要执行里面的代码。

## 4.2 路径 B：转 GGUF 再喂 Ollama / llama.cpp

**适合**：本地个人长期用、老机器、边缘设备、想压缩显存占用。这是把「原材料」加工成「预制菜」的完整链路。

先转成 FP16 GGUF，再量化成 Q4_K_M（内存压到约 1/4）：

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
pip install -r requirements.txt

# 转换：safetensors 目录 → FP16 GGUF
python convert_hf_to_gguf.py ./models/Qwen2.5-7B-Instruct \
    --outfile ./models/Qwen2.5-7B-f16.gguf \
    --outtype f16 \
    --model-name "Qwen2.5-7B-Instruct"

# 量化：FP16 GGUF → Q4_K_M GGUF
cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release
./build/bin/llama-quantize \
    ./models/Qwen2.5-7B-f16.gguf \
    ./models/Qwen2.5-7B-Q4_K_M.gguf \
    Q4_K_M
```

转完就能像平时一样喂给 Ollama（Modelfile 指向你的 GGUF 文件，然后 `ollama create` + `ollama run`），走你熟悉的既有部署链路。

**更省事的替代：让 Ollama 直接 FROM safetensors 目录**，前提是模型架构在 Ollama 的白名单里 [Ollama 导入文档](https://docs.ollama.com/import)：

```bash
# Modelfile:
#   FROM ./models/Qwen2.5-7B-Instruct
#   PARAMETER temperature 0.7
#   PARAMETER num_ctx 8192
ollama create my-qwen -f Modelfile
ollama run my-qwen
# 或一步到位直接量化：ollama create my-qwen-q4 -f Modelfile --quantize q4_K_M
```

两个认知修正（网上很多旧教程会误导你）[convert_hf_to_gguf.py](https://github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py)：

1. **当前版本 `convert_hf_to_gguf.py` 已经没有 `--vocab-type` 参数了**，词表类型会自动识别；低比特量化（Q4_K_M）走 `llama-quantize`，`--outtype` 最低只到 q8_0。
2. **Ollama 的「FROM safetensors 目录」只支持 Llama（含 2/3/3.1/3.2）、Mistral（含 Mixtral）、Gemma（1/2）、Phi3 这四类架构**。Qwen2.5 不在名单里，直接 `FROM` 一个 Qwen 的 safetensors 目录会失败——必须先自己走一遍 convert + quantize。

**坑**：转换脚本对超新/冷门架构可能报错；大模型转换内存不足加 `--use-temp-file`；GGUF 分片 Ollama 不支持，需先用 `gguf-split` 合并。

> [!tip] 大白话
> 把 Ollama 想成一家只跟固定几家供应商签约的中央厨房：它愿意直接加工 Llama、Mistral、Gemma、Phi3 的「半成品」（safetensors 目录），但 Qwen 没签约——Ollama 不敢乱接单。这时你得自己先把 Qwen 做成标准预制菜（转成 GGUF），它才肯收。

## 4.3 路径 C：vLLM 高并发生产

**适合**：正式对外服务、多用户并发、长上下文、多卡部署。投入最大但吞吐最高。

```bash
pip install vllm

vllm serve ./models/Qwen2.5-7B-Instruct \
    --load-format safetensors \   # 显式指定，跳过自动探测
    --dtype bfloat16 \
    --max-model-len 32768 \       # 总上下文窗口
    --gpu-memory-utilization 0.9 \
    --tensor-parallel-size 1 \    # 多卡时 = 卡数
    --port 8000
```

启动后用 OpenAI 兼容接口验证 [vLLM serve 文档](https://docs.vllm.ai/en/latest/cli/serve.html)：

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "./models/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "你好"}]}'
```

**为什么 vLLM 喂的是 safetensors 而不是 GGUF？**这是很多人的直觉困惑，但原因很实际：vLLM 的核心竞争力是 PagedAttention 和 continuous batching，这些高性能内核都是为**原生 HF/safetensors 权重**设计的。GGUF 里的 K-quants/IQ-quants 量化是 llama.cpp 系的格式，vLLM 要加载就得先在 meta-device 上建一个假模型做张量名映射，再写几千行 CUDA 反量化内核——工程上既脆弱又难维护。所以 vLLM 官方把内置 GGUF 支持标记为**实验性**并下放给了外部插件 [RFC #39583](https://github.com/vllm-project/vllm/issues/39583)。实践结论：vLLM 吃 safetensors，想省内存就用 GPTQ/AWQ 原生量化，不走 GGUF。

**坑**：只下权重不下 `config.json` / `tokenizer.json` 是最高频的启动失败原因（还记得第 3 章说的「缺说明书加载不了」吗）；模型过新会报 architecture not supported；CUDA illegal memory access 多由显存不足或驱动引起。

## 4.4 大白话：开餐厅的三种经营方式

三条路径的分工，用第 1 章那家餐厅的比喻就能一次记牢：

> [!tip] 大白话
> | 路径 | 餐厅经营方式 | 特点 | 对应选择 |
> |------|--------------|------|----------|
> | A | 自家厨房现做 | 最灵活，客人点什么都能试，但一次只伺候一位、出菜慢 | 验证菜好不好吃、搞研发试菜 |
> | B | 中央厨房预制菜 | 便宜省事，小店面（老机器/小显存）也能开，适合外带 | 本地自用、长期个人用、分发携带 |
> | C | 连锁总店 + 高客流流水线 | 前期投入大（大显存/多卡），但能同时接很多桌 | 正式对外营业、多用户高并发 |
>
> 先想清楚「给谁吃（目的）+ 店开在哪（硬件）」，再决定用哪种经营方式。选对了，省心省钱；选错了，要么跑不动，要么浪费钱。

## 4.5 三条路径对比表

| 维度 | A：Transformers/ModelScope | B：转 GGUF → Ollama/llama.cpp | C：vLLM |
|---|---|---|---|
| 输入格式 | safetensors/bin 目录 | 先转 GGUF（或白名单内 Ollama 自动转） | safetensors 原生（GGUF 仅实验性） |
| 硬件要求 | 最低（CPU 可跑）；fp16 7B≈14GB | 最低（CPU 都能跑）；Q4 显存≈fp16 的 1/4 | 高：NVIDIA GPU，推荐 24GB+，多卡更佳 |
| 量化/省内存 | 仅靠 dtype | ✅ 强项：Q4_K_M 等 | GPTQ/AWQ（原生量化，不走 GGUF） |
| 吞吐 | 低：单流无并发 | 中低：单用户快 | 高：continuous batching + PagedAttention |
| 适合场景 | 跑通验证 / 原型 / 微调前 | 本地个人 / 老机器 / 边缘 / 分发携带 | 生产服务 / 多用户 / 长上下文 / 多卡 |
| 难度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**一句话选型**：先验证模型行不行 → A；自己电脑长期好用、吃配置低 → B（Qwen 等非白名单架构先手动转 GGUF）；正式多用户服务 → C。

## 本章小结

- 非 GGUF 的原始权重有三条可操作路径：Transformers 直接加载、转 GGUF 喂 Ollama/llama.cpp、vLLM 生产部署
- 路径 A 最快跑通验证，关键参数是 `torch_dtype`（防 OOM）、`device_map="auto"`、`trust_remote_code`（自定义代码必须开）
- 路径 B 把原材料加工成预制菜：`convert_hf_to_gguf.py` 转 FP16 → `llama-quantize` 压到 Q4_K_M；Ollama 白名单只有 Llama/Mistral/Gemma/Phi3，Qwen 要手动转
- 路径 C 适合高并发生产，vLLM 实践上喂 safetensors 而非 GGUF（PagedAttention 内核为原生权重设计，GGUF 支持被官方标为实验性）
- 选型看「目的 + 硬件」：验证用 A、本地长期用 B、正式服务用 C

下一章，我们把三条路径收束成一张决策地图，回答「什么时候该下 GGUF、什么时候该下原始权重」，再串起常见坑清单，并和你已有的 GGUF + Ollama 部署指南打通。
