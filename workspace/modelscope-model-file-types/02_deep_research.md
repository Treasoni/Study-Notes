# ModelScope 模型文件类型 - 深度研究素材

收集时间: 2026-08-10
搜索关键词: safetensors, bin, gguf, onnx, config.json, tokenizer, generation_config, sharded checkpoint, 模型格式转换, vLLM, ModelScope 仓库规范

## 一、模型权重文件格式技术细节

### 1. safetensors（`.safetensors`）
- **是什么**: HuggingFace 主导的开源张量存储格式，Rust 核心 + Python 绑定，安全替代 pickle + 零拷贝加载
- **技术原理**: 文件三部分 = 8 字节小端 uint64 记录 JSON 头长度 → UTF-8 JSON 头（每张量 `{dtype, shape, data_offsets}` + `__metadata__`）→ 连续原始字节张量缓冲区。通过 mmap 内存映射零拷贝访问；校验器保证偏移连续无空洞，杜绝 polyglot 文件
- **安全风险**: 无（不含 pickle 可执行操作码；头部封顶 100MB 防 DoS）
- **典型用途**: HF 生态默认权重格式；transformers 4.35+ `save_pretrained` 默认输出它；被 PyTorch/TF/JAX/Paddle 全栈支持
- **关键数据**: BLOOM 176B 加载从 pickle ~10 分钟 → ~45 秒；CPU 快 ~76.6×（GPT-2 307ms→4ms），GPU ~2.1×
- **分片**: 大模型拆为 `model-00001-of-00006.safetensors`，配 `model.safetensors.index.json`（weight_map 张量名→分片文件），防 OOM、绕开单文件 ~5GB 软上限
- **信源**: github.com/safetensors/safetensors；deepwiki.com/huggingface/safetensors

### 2. bin / pytorch_model.bin（`.bin` / `.pt`）
- **是什么**: `torch.save()` 默认产物，即 pickle 序列化的 state dict；曾是 HF 生态默认权重
- **技术原理**: pickle 图式序列化，反序列化时实例化任意 Python 对象并执行 `__reduce__` → 加载文件本身就是代码执行点
- **安全风险**: 有（严重）。可注入 `__reduce__` 实现任意代码执行，是供应链攻击主要载体。JFrog 2024 在 HF 发现约 100 个恶意模型文件，约 95% 针对 PyTorch；相关 CVE：CVE-2026-23001、CVE-2026-15976 等，CVSS 最高 9.8
- **典型用途**: 旧模型仓库存量权重；新项目已基本不生成（transformers 4.35+ 默认 safetensors）
- **关键数据**: 加载 `.bin` 需 `weights_only=True` 才防 RCE；`safe_serialization=False` 可强制退回 `.bin`
- **信源**: github.com/George0Papasotiriou/CVE-2026-23001-...；kb.cert.org/vuls/id/252619

### 3. gguf（`.gguf`）
- **是什么**: llama.cpp 团队的推理模型格式（2023 取代 GGML/GGJT），单文件自包含，本地大模型推理事实标准
- **技术原理**: 头部（magic `GGUF` + 版本 v3 + tensor_count + metadata_kv_count）→ 元数据键值对（架构/超参/tokenizer/chat template）→ 张量信息（name≤64B、维度、ggml_type、32 字节对齐 offset）→ 连续张量数据。天然支持 mmap 直接映射
- **安全风险**: 无（纯二进制权重+元数据）
- **量化**: 内置 Q2~Q8 多档；K-quant 混合精度（attention 保留高精度、FFN 更激进）。7B 参考：Q4_K_M 4.1GB（ppl +1.68%）推荐默认；Q8_0 7.0GB（+0.03%）近无损
- **典型用途**: 本地/边缘推理（CPU/Apple Silicon/低显存 GPU）；Ollama、LM Studio、llama.cpp、Jan、llamafile、KoboldCpp 加载
- **与 safetensors 关系**: 只推理不可训练；量化 GGUF 转回 safetensors 可行但有损（Q4_0 余弦相似度约 0.996，Q8_0 约 0.99998）
- **信源**: raw.githubusercontent.com/ggml-org/ggml/master/docs/gguf.md；github.com/ggml-org/llama.cpp/pull/3049

### 4. onnx（`.onnx`）
- **是什么**: 2017 微软+Facebook 发起、现归 LF AI 的跨框架开放神经网络交换标准（通用中间表示）
- **技术原理**: Protobuf 序列化「带类型计算图」：算子节点、数据流边、输入输出定义、权重常量（initializers）、opset 版本；大权重可外置 external data
- **安全风险**: 无直接 pickle 类风险（纯数据图描述）
- **典型用途**: 生产部署与服务端推理——训练/部署分离，`torch.onnx.export` 导出后由 ONNX Runtime / TensorRT / OpenVINO 执行
- **在本主题里的定位**: 部署中间层，既不是仓库分发格式（safetensors）也不是本地量化格式（GGUF）
- **信源**: deepwiki.com/microsoft/onnxruntime

### 5. 量化基础（为什么 GGUF 带量化档而 safetensors 默认 f16/fp32）
- **每参数字节数**: FP32=4、FP16/BF16=2、INT8=1、INT4=0.5。Llama-3 8B：FP32 ~32GB、FP16 ~16GB、INT8 ~8GB、INT4 ~4GB
- **分工**: safetensors 存 fp16/bf16 作「母版权重」（保留训练精度，供微调/评测/各框架消费）；GGUF 面向本地推理，把量化内建为一级公民（`llama-quantize`）
- **各档取舍**: INT8 近无损（99%+ 质量）；INT4 质量降 1-3%（数学/代码类任务降幅大于知识问答）；INT4 只推理不训练；注意 KV cache 长上下文常驻 FP16，显存占用可能超过量化权重
- **信源**: vife.ai/blog/guide-llm-quantization-gguf-models；github.com/firecrawl/ai-research-skills/.../quantization.md

### 格式对比总结
> 原始权重以 safetensors（或旧式 pickle 的 .bin）保存为「母版」（fp16/fp32 精度），用于微调、评测、跨框架消费；GGUF 把同一权重压缩成单文件量化版，是本地推理的分发格式；ONNX 是生产部署的跨框架中间表示。三者对应「训练存储 → 本地运行 → 云端部署」。

## 二、配置文件与分词器文件的字段级作用

### 1. config.json（**必需**）
- **一句话**: 模型的「结构蓝图」，定义架构类型、维度超参、特殊 token ID
- **关键字段**:
  - `architectures`: 如 `["Qwen2ForCausalLM"]`，指定用哪个模型类
  - `model_type`: 架构族标识（`qwen2`/`llama`），AutoConfig 的路由键
  - `hidden_size`: 隐藏状态维度（d_model），须能被 num_attention_heads 整除
  - `num_hidden_layers`: Transformer 层数
  - `num_attention_heads`: 注意力头数
  - `vocab_size`: 词表大小，同时是 embedding 矩阵第一维，必须与分词器一致
  - `max_position_embeddings`: 位置编码最大序列长度（上下文窗口上限）
  - `rope_theta`: RoPE 基础频率（Qwen2.5 用 1000000，Llama 默认 10000）
  - `rope_scaling`: 上下文超长外推时的频率缩放
  - 其他: `intermediate_size`、`num_key_value_heads`（GQA）、`head_dim`、`rms_norm_eps`、`torch_dtype`、`tie_word_embeddings`、`bos/eos/pad_token_id`
- **缺失后果**: 直接抛错（无法推断架构类与维度——权重只是一堆裸张量）
- **加载流程**: AutoConfig 先读它 → 用 model_type 选 Config 类 → AutoModel 用 architectures 实例化类、维度搭网络 → 最后才加载权重
- **信源**: huggingface.co/docs/transformers/main_classes/configuration

### 2. tokenizer 系列（**必需且与模型绑定**）
- **tokenizer.json**: Fast tokenizer 完整自包含状态（Rust tokenizers 库）：词表+merge 规则+整条处理管线。缺失时退回 slow tokenizer 多文件重建
- **tokenizer_config.json**: 配置参数不含词表：`tokenizer_class`（路由类）、`model_max_length`、`chat_template`（Jinja2）、`added_tokens_decoder`、`bos/eos/unk/pad_token`
- **vocab.txt**: Slow tokenizer 词表，一行一个 token，第 N 行 = token ID N（WordPiece/BERT 系）
- **vocab.json**: `{"token": id}` 字典
- **merges.txt**: BPE merge 规则（相邻子词如何按序合并）
- **special_tokens_map.json**: 登记特殊 token 字符串
- **必须匹配原理**: embedding 矩阵有 vocab_size 行，每行对应 token ID；分词器把文本切成 token 并分配 ID，ID 当**行号**取 embedding。换错分词器 → ID 越界或顺序不一致 → 同一 ID 指向不同文本 → 输出变乱码。光看 vocab_size 相同不够，必须是同一套 token→ID 映射
- **信源**: huggingface.co/docs/transformers/tokenizer_summary；theneuralbase.com/model-merging/.../consistent-tokenizer

### 3. generation_config.json（**可选**）
- **一句话**: `generate()` 的生成参数配置，独立于模型结构 config
- **关键字段**: `max_new_tokens`（推荐）、`max_length`（旧）、`early_stopping`、`do_sample`、`num_beams`、`temperature`（默认 1.0）、`top_k`（默认 50）、`top_p`（默认 1.0）、`repetition_penalty`（默认 1.0）、`use_cache`、`num_return_sequences`
- **缺失后果**: 不报错，回落默认（贪心、最多 20 token、temperature=1.0）
- **加载时机**: 仅在 `model.generate()` 时由 GenerationConfig.from_pretrained 读取
- **信源**: huggingface.co/docs/transformers/main_classes/text_generation

### 4. model.safetensors.index.json（**分片必需**）
- **一句话**: 分片 safetensors 的索引，记录每个张量在哪个分片
- **关键内容**: `weight_map`（张量名→分片文件名，如 `"h.0.input_layernorm.bias": "model_00002-of-00072.safetensors"`）；`metadata.total_size`（参数量）
- **单文件 vs 分片**: 单文件只有 model.safetensors 无 index；分片模型多个文件 + index.json
- **缺失后果**: from_pretrained 无法解析 shard，加载直接失败（unsloth#2355 真实案例）
- **加载流程**: 检测到 index.json → 走分片分支 → 读 weight_map 分组 → 按需打开分片 → safe_open 逐张量装入
- **信源**: huggingface.co/docs/safetensors/metadata_parsing；github.com/unslothai/unsloth/issues/2355

### 5. README.md / model card（**仅文档**）
- **一句话**: 人读文档 + Hub 元数据，不参与推理
- **关键 YAML 字段**: `license`、`pipeline_tag`、`tags`、`datasets`、`base_model`、`library_name`、`model-index`
- **缺失后果**: 完全不影响加载，只影响可发现性与页面展示
- **信源**: huggingface.co/docs/hub/model-cards

### 加载顺序总结
> AutoModel 先读 config.json（定结构）→ 建骨架 → 读 model.safetensors[.index.json] 加载权重；AutoTokenizer 先读 tokenizer_config.json 定类 → 按 tokenizer.json（fast）或 vocab/merges（slow）建分词器；generate() 时才读 generation_config.json；README 全程不参与。

## 三、非 GGUF 原始权重的三条使用路径

### 路径 A：Transformers / ModelScope 直接推理
```bash
modelscope download --model Qwen/Qwen2.5-7B-Instruct --local_dir ./models/Qwen2.5-7B
```
```python
from modelscope import snapshot_download
model_dir = snapshot_download(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    local_dir="./models/Qwen2.5-7B",
    allow_patterns=["*.safetensors", "*.json", "*.py"],
)
```
```python
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch
model_dir = "./models/Qwen2.5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.bfloat16,   # 不传默认 fp32，7B 约 28GB 必 OOM
    device_map="auto",            # 显存不够自动溢到 CPU/磁盘
    trust_remote_code=True,       # 目录有自定义 modeling_*.py 时必须开
)
messages = [{"role": "user", "content": "用三句话解释什么是 KV Cache"}]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
out = model.generate(inputs, max_new_tokens=512, do_sample=False)
print(tokenizer.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True))
```
- **关键参数**: `torch_dtype="auto"`（省事）、`device_map="auto"`（自动分派/offload）、`trust_remote_code=True`（自定义架构必需）、`use_safetensors=True`（默认优先）、`local_files_only=True`（纯离线）
- **前置条件**: `pip install modelscope transformers torch accelerate`；fp16 下 7B≈14GB、13B≈26GB、70B≈140GB
- **适合场景**: 跑通验证、原型、embedding、微调前检查
- **常见坑**: 忘 torch_dtype 直接 OOM；有自定义代码没开 trust_remote_code 报 KeyError；吞吐低无并发
- **信源**: modelscope.cn/docs/models/download；huggingface.co/docs/transformers/main/en/main_classes/model

### 路径 B：转 GGUF 再喂 Ollama/llama.cpp/LM Studio
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
**更省事的替代：Ollama 直接 FROM safetensors 目录**
```bash
# Modelfile:  FROM ./models/Qwen2.5-7B-Instruct
#   PARAMETER temperature 0.7
#   PARAMETER num_ctx 8192
ollama create my-qwen -f Modelfile
ollama run my-qwen
# 或直接量化：ollama create my-qwen-q4 -f Modelfile --quantize q4_K_M
```
- **关键参数**: `--outtype`（f32/f16/bf16/auto，通常只做 fp16/f32，低比特量化交给 llama-quantize）、`--model-name`、`--split-max-size`（分片输出）、`--print-supported-models`
- **⚠️ 认知修正**: 当前版本**已无 `--vocab-type` 参数**（词表类型自动判定）；低比特量化应走 `llama-quantize`，`--outtype` 最低 q8_0
- **⚠️ Ollama FROM safetensors 目录只支持 4 类架构**: Llama（含 2/3/3.1/3.2）、Mistral（含 Mixtral）、Gemma（1/2）、Phi3。**Qwen2.5 不在列表** → 必须自己先 convert_hf_to_gguf.py 转成 GGUF
- **常见坑**: 转换脚本对超新/冷门架构可能报错；`--outtype q4_0` 一步到位官方不建议；大模型转换内存不足加 `--use-temp-file`；分片 GGUF Ollama 不支持需先 gguf-split 合并
- **信源**: github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py；docs.ollama.com/import；huggingface.co/spaces/ggml-org/gguf-my-repo

### 路径 C：vLLM 部署（高并发生产 API）
```bash
pip install vllm
vllm serve ./models/Qwen2.5-7B-Instruct \
    --load-format safetensors \
    --dtype bfloat16 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.9 \
    --port 8000
```
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "./models/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "你好"}]}'
```
- **关键参数**: `--load-format safetensors`（显式跳过探测）、`--tensor-parallel-size`（跨卡并行）、`--max-model-len`（总上下文）、`--gpu-memory-utilization`（默认 0.9）、`--trust-remote-code`
- **前置条件**: NVIDIA GPU（CUDA），推荐 24GB+；7B fp16≈14GB 起，KV cache+并发建议显存≥权重的 1.5~2 倍
- **为什么 vLLM 和 GGUF 不对付**: vLLM 核心竞争力是 PagedAttention + continuous batching，这些内核为原生 HF/safetensors 权重设计；GGUF 的 K-quants/IQ-quants 是 vLLM 没有的量化，加载需 meta-device 建假模型映射张量名 + 数千行专用 CUDA 反量化内核，工程脆弱。vLLM 官方已把 in-tree GGUF 支持标记实验性并下放外部插件（RFC #39583）。实践结论：vLLM 喂 safetensors（量化用 GPTQ/AWQ 而非 GGUF）
- **常见坑**: 缺 config.json/tokenizer.json 直接启动失败（只下权重不下配置是最高频报错）；模型过新报 architecture not supported；CUDA illegal memory access
- **信源**: docs.vllm.ai/en/latest/cli/serve.html；docs.vllm.ai/.../quantization/gguf/；github.com/vllm-project/vllm/issues/39583

### 三条路径选型对比表
| 维度 | A：Transformers/ModelScope | B：转 GGUF → Ollama/llama.cpp | C：vLLM |
|---|---|---|---|
| 输入格式 | safetensors/bin（目录） | 先转 GGUF（或 Ollama 内部转） | safetensors（原生），GGUF 仅实验 |
| 硬件要求 | 最低（CPU 可跑）；fp16 7B≈14GB | 最低（CPU 都能跑）；Q4 显存≈fp16 的 1/4 | 高：NVIDIA GPU，推荐 24GB+，多卡更佳 |
| 量化/省内存 | 仅靠 dtype | ✅ 强项：Q4_K_M 等 | GPTQ/AWQ（原生量化），不走 GGUF |
| 吞吐 | 低：单流无并发 | 中低：单用户快 | 高：continuous batching + PagedAttention |
| 场景 | 跑通验证/原型/微调前 | 本地个人/老机器/边缘/分发携带 | 生产服务/多用户/长上下文/多卡 |
| 难度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**一句话选型**: 先看看模型行不行 → A；自己电脑长期好用吃配置低 → B（Qwen 等非白名单架构需手动转 GGUF）；正式服务多用户 → C。

## 四、ModelScope 平台仓库规范

### 1. ModelScope 仓库结构
- 采用 git + git-lfs 托管，布局扁平
- **与 HF 差异**: 平台级元数据文件叫 `configuration.json`（不是 config.json），定义 framework/task/pipeline，是「正式发布」必填项，缺失标记 preview；真实 config.json（架构超参）和权重仍需上传，两者分工不同
- 仓库 ID 格式 `org/model-name`
- **坑**: 只上传 config.json 忘了 configuration.json，模型一直停「预发布」
- **信源**: developer.aliyun.com/ask/563381；modelscope.cn/api/v1/models/...

### 2. snapshot_download 细节
- 官方签名支持: `model_id/repo_id`、`revision`、`cache_dir`、`local_dir`、`allow_patterns`（别名 allow_file_pattern）、`ignore_patterns`（别名 ignore_file_pattern）、`local_files_only`、`max_workers`（默认 4）、`token`、`endpoint`
- **local_dir 指定时文件直接落到 local_dir/ 且 cache_dir 被忽略**；不指定时落 cache_dir/model_id/，默认 `~/.cache/modelscope/hub`（MODELSCOPE_CACHE 可覆盖）
- 大文件并行: 阈值 500MB（MODELSCOPE_PARALLEL_DOWNLOAD_THRESHOLD_MB）、并行数默认 1（MODELSCOPE_DOWNLOAD_PARALLELS）、分块 160MB
- **坑**: CLI 多个 `--exclude` 历史上只生效最后一个；`{a,b}` 花括号失效；复杂过滤用 Python SDK
- **信源**: github.com/modelscope/modelscope/blob/master/modelscope/hub/snapshot_download.py

### 3. checksums.sha256
- **⚠️ 认知修正**: `checksums.sha256` 并非 ModelScope 平台自动生成的文件（实测官方 Qwen GGUF 仓库无校验文件）
- 平台做法: 服务端保存每个文件 SHA256 元数据；SDK 下载默认**不校验**（MODELSCOPE_ENABLE_DEFAULT_HASH_VALIDATION 默认关闭，省性能）；显式开启后下载完实时算哈希比对，不匹配抛 FileIntegrityError 并自动清除重下
- 仓库自带校验文件时（第三方工具/镜像站生成）可离线 `sha256sum -c` 校验
- **坑**: 校验默认关闭，网络抖动/磁盘满可能静默写入损坏文件；报 integrity check failed 时清空 `~/.cache/modelscope/hub/._____temp/` 后重试
- **信源**: github.com/modelscope/modelscope/blob/master/modelscope/hub/utils/caching.py

### 4. GGUF vs 原始权重仓库
- 原始仓库（`Qwen/Qwen2.5-7B-Instruct`）: config.json + model.safetensors（分片带 index.json）+ tokenizer 系列
- GGUF 仓库（官方加 `-gguf`/`-GGUF` 后缀）: 只放 GGUF 分片 + configuration.json + README，tokenizer 已内嵌进 GGUF
- 官方 GGUF 命名遵循 llama.cpp 规范: `<Model>(-<Version>)-(<Experts>x)<Params>-<Quant>(-<Shard>).gguf`，量化标签固定后缀（q4_k_m、q8_0），分片用 -00001-of-000NN
- 下载单个量化档所有分片: `modelscope download --model Qwen/Qwen2.5-7B-Instruct-gguf --include 'qwen2.5-7b-instruct-q4_k_m*' --local_dir .`
- **坑**: 分片需合并才能直接喂 llama.cpp/llama-server；镜像仓库与 HF 原仓库量化档位可能不同步
- **信源**: modelscope.cn/api/v1/models/Qwen/Qwen2.5-7B-Instruct-gguf/repo/files

### 5. ModelScope 与 HuggingFace 互通
- **可以互通**: ModelScope 上的 safetensors 仓库保持 HF 兼容布局，下载到本地后用 `transformers` 的 `AutoModelForCausalLM.from_pretrained(local_dir, trust_remote_code=True)` 离线加载即可，无需联网重下
- 前提: 本地目录包含完整必需文件（config.json、权重分片及其 index.json、tokenizer 文件）
- 完全离线: `HF_HUB_OFFLINE=1` 或 `local_files_only=True`
- **坑**: 加载路径要指向**文件夹**而非单个 .safetensors；分片模型缺 index.json 报找不到权重；trust_remote_code 缺失对自定义代码模型是「静默错误」
- **信源**: blog.csdn.net/2303_80346267/article/details/146553014

### 6. 私有模型鉴权
- 访问私有模型必须带 Access Token（SDK 令牌），平台「我的」页面获取（modelscope.cn/my/myaccesstoken）
- CLI: `modelscope login --token YOUR_ACCESS_TOKEN`（凭证约 30 天有效）
- Python: `snapshot_download(..., token=...)` 或环境变量 `MODELSCOPE_API_TOKEN`
- 报 401/403 先重新 login；token 别硬编码进公共代码
- **信源**: modelscope.cn/my/myaccesstoken；github.com/modelscope/modelscope/releases/tag/v1.35.4

## 综合分析

### 核心共识
1. 一个完整模型仓库 = **权重 + 配置 + 分词器 + 文档**；权重只是其中一部分，缺配置文件模型无法加载
2. **safetensors 已是事实标准**: 安全（无代码执行）、零拷贝/懒加载/分片；.bin/.ckpt 属 pickle 旧格式有安全风险
3. **GGUF 是推理部署格式而非训练格式**: 单文件自包含、支持量化，专为 llama.cpp 系引擎设计；tokenizer 已内嵌
4. 非 GGUF 文件有三条使用路径，按「目的+硬件」选择：研究调试用 Transformers（A）、本地/端侧转 GGUF（B）、生产并发用 vLLM（C）
5. **vLLM 不兼容 GGUF（实践上）**: 应把 vLLM 定位为 safetensors 原生引擎；GGUF 走 llama.cpp/Ollama
6. **Ollama FROM safetensors 目录仅支持 Llama/Mistral/Gemma/Phi3 四类架构**，Qwen 需先转 GGUF

### 与用户既有部署指南的衔接
- 用户已会「下载 GGUF → Ollama 部署」；本笔记补上「为什么有些仓库没有 GGUF？那些文件是什么？要怎么用？」
- 关键洞察: GGUF 是「加工过的成品」，safetensors/bin 是「原材料」；原材料可以自己加工成 GGUF（路径 B），也可以直接吃（路径 A）
- ModelScope 与 HF 布局互通，下载到本地后 transformers 可直接加载

### 认知修正点（写笔记时要强调）
1. `convert_hf_to_gguf.py` 当前版本**没有 `--vocab-type` 参数**，词表类型自动识别；低比特量化（Q4_K_M）走 `llama-quantize`
2. `checksums.sha256` 不是 ModelScope 平台自动生成的文件；SDK 校验默认关闭
3. vLLM 并非「完全不兼容 GGUF」（0.6.2+ 有 `--load-format gguf`），但官方定位实验性、工程脆弱，实践中应喂 safetensors

### 信息缺口
- 概念入门深度下无重大缺口；量化原理细节、GGUF 内部字节布局等留作进阶延伸即可
