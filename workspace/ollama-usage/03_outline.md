## 学习笔记大纲：《Ollama 使用文档》

> 笔记类型：概念 + 实战混合（零基础入门，核心概念预留 `[!tip] 大白话` 通俗解释 + 类比位）
> 预计总篇幅：中（约 25-30 页）
> 章节数：5
> 适用读者：没用过 Ollama、不熟悉本地 LLM 的零基础读者
> 学习深度：入门到上手

### 第一章：Ollama 是什么 & 为什么用

- **篇幅**：中
- **覆盖要点**：Ollama 定位、本地 LLM 优势、与云端 API 对比、底层引擎与量化概念速览
- **素材引用**：深度素材 §1（Ollama 是什么）；信源 #1, #6, #9
- **代码示例**：无
- **章节结构**：
  - 1.1 一句话认识 Ollama —— 定位与核心卖点（一条命令运行开源大模型、数据不出本机、跨平台）
    - `[!tip] 大白话`：本地版「应用商店 + 运行时」——商店负责下载模型，运行时负责在电脑上跑起来
  - 1.2 为什么用本地 LLM：与云端 API 对比 —— 隐私 / 离线可用 / 无 API 费用 vs 自备算力 / 性能取决于硬件
    - `[!tip] 大白话`：把 ChatGPT 搬回家，断网也能用，聊天数据锁进自己的「保险箱」
  - 1.3 底层原理速览：llama.cpp、GGUF 与量化 —— 不深入源码，只建立心智模型
    - `[!tip] 大白话`：量化 = 照片压缩——RAW 原图清晰但巨大，q4_K_M 是「高清又不占空间」的平衡档
  - 1.4 本章小结 —— Ollama 适合谁、不适合谁（附选型判断表）

### 第二章：安装与快速开始

- **篇幅**：中
- **覆盖要点**：系统要求、Windows/macOS/Linux/Docker 四种安装方式、首次运行对话、默认目录与端口
- **素材引用**：深度素材 §2（安装与快速开始）；信源 #1, #2, #4, #10
- **代码示例**：有（各平台安装命令、`ollama run`、`docker exec`）
- **章节结构**：
  - 2.1 安装前的准备 —— 硬件 / 系统要求一览（Windows/macOS/Linux 各一行说明）
  - 2.2 分平台安装 —— Windows（winget / 安装包 / PS 脚本）、macOS（dmg）、Linux（curl + systemd）、Docker（`docker run` + GPU 参数）
    - `[!tip] 大白话`：Docker = 标准集装箱——把 Ollama 连同运行环境打包，换台电脑也能原样跑起来
  - 2.3 首次运行：跑起第一个模型 —— `ollama --version` 验证、`ollama run` 进入对话、`/bye` 退出
  - 2.4 默认路径与端口一览 —— 模型存储位置（各平台）、默认端口 11434、`OLLAMA_MODELS` / `OLLAMA_HOST` 预告（留待第 4 章展开）

### 第三章：CLI 命令与模型管理

- **篇幅**：长
- **覆盖要点**：`ollama` 全部常用命令、模型生命周期（拉取/更新/删除/查看/复制）、模型库与量化选型
- **素材引用**：深度素材 §3（CLI 命令与模型管理）；信源 #2, #9, #10
- **代码示例**：有（`pull / run / list / ps / rm / cp / show / stop` 各配示例）
- **章节结构**：
  - 3.1 命令总览 —— 一张表看懂 11 个常用命令（run / pull / rm / ls / ps / stop / serve / show / cp / create / push）
    - `[!tip] 大白话`：run = 在应用商店点开应用；ps = 看当前「谁还在运行」
  - 3.2 跑模型：`run` 的三种姿势 —— 交互式聊天 / 单次提问 / 多行输入（`"""` 包裹）
  - 3.3 模型管理：`pull` / `list` / `ps` / `rm` / `cp` —— 标签格式、更新即重跑 `pull`、`ps` 的 PROCESSOR 与 UNTIL 列解读
    - `[!tip] 大白话`：tag（如 `qwen2.5:7b-q4_K_M`）= 版本号，同一模型不同 tag 可并存
  - 3.4 模型库与量化：怎么选模型 —— 参数规模（7b/8b/70b、MoE）、能力标签（vision/tools/embedding）、量化档位（f16 / q8_0 / q4_K_M）与显存匹配建议表
    - `[!tip] 大白话`：量化 = 照片压缩；8GB 显存首选 q4_K_M（约 1/4 体积、质量约 96%）

### 第四章：进阶用法：API / OpenAI 兼容 / Modelfile / 环境变量

- **篇幅**：长
- **覆盖要点**：原生 HTTP API、OpenAI 兼容接口 + SDK 调用、Modelfile 定制模型、关键环境变量
- **素材引用**：深度素材 §4（进阶用法）；信源 #3, #4, #5, #7
- **代码示例**：有（Python openai SDK、curl、Modelfile 示例、`ollama create`）
- **章节结构**：
  - 4.1 原生 HTTP API：Ollama 也是本地小服务器 —— base_url `/api`、核心端点（generate / chat / tags / embed）、NDJSON 流式与 `stream:false`
    - `[!tip] 大白话`：Ollama 像本地一台小服务器，装好即在 11434 端口待命，程序通过 HTTP「找它聊天」
  - 4.2 OpenAI 兼容 API：用现成 SDK 无缝对接 —— base_url `/v1`、api_key 填任意值（`"ollama"`）、Python + curl 最小示例
    - `[!tip] 大白话`：api_key = 门禁卡——形式上必须刷一下，但 Ollama 不校验内容，随便一张卡都能进
  - 4.3 Modelfile：定制自己的模型 —— 类似 Dockerfile 的蓝图；FROM / PARAMETER / SYSTEM / TEMPLATE / ADAPTER；最小示例 + `ollama create`
    - `[!tip] 大白话`：Modelfile = 给模型的定制食谱——FROM 是食材（基座模型），PARAMETER / SYSTEM 是火候与口味
  - 4.4 环境变量：按需调整运行行为 —— OLLAMA_HOST / OLLAMA_MODELS / OLLAMA_KEEP_ALIVE / OLLAMA_NUM_PARALLEL / OLLAMA_FLASH_ATTENTION 等；Windows 改后需重启
    - `[!tip] 大白话`：环境变量 = 服务「开机前」的设置项，改完要重启才生效

### 第五章：常见坑与最佳实践

- **篇幅**：中
- **覆盖要点**：显存不足静默回退、下载慢与镜像、端口占用与跨设备访问、安全与隐私、最佳实践清单
- **素材引用**：深度素材 §5（常见坑与对策）；信源 #7, #8, #10
- **代码示例**：有（`ollama ps` 诊断、`OLLAMA_HOST` / 代理设置，少量）
- **章节结构**：
  - 5.1 显存不足与静默回退 CPU —— 现象（无警告但变慢）、诊断（`ollama ps` 看 PROCESSOR 列）、对策（换量化版、OLLAMA_FLASH_ATTENTION、降 num_ctx）
    - `[!tip] 大白话`：显存不够时 Ollama 会「偷偷换人干活」——GPU 换成 CPU，看起来在跑但慢很多
  - 5.2 下载慢 / 镜像 / 网络问题 —— 官方无镜像配置；代理 HTTPS_PROXY；WSL2 网卡 Large Send Offload V2
  - 5.3 端口占用与跨设备访问 —— 默认只监听 127.0.0.1；`OLLAMA_HOST=0.0.0.0` + 放行防火墙 11434
  - 5.4 安全与隐私：API 无认证怎么办 —— 勿随意设 `0.0.0.0`；反向代理 + 鉴权；OLLAMA_ORIGINS 白名单
    - `[!tip] 大白话`：设成 `0.0.0.0` 等于把门敞开——API 没有身份校验，知道地址的人就像拿到「临时工牌」，谁都能调用你的模型
  - 5.5 最佳实践清单 —— 从第 1-5 章提炼的可勾选 checklist（选型 / 安装 / 运维 / 安全）

## 学习路径说明

### 前置要求
- 零基础可读，无需任何本地 LLM 使用经验
- 会用命令行：能打开终端 / PowerShell 并输入命令即可
- 第 4 章的 API 部分需要一点点 Python（或任意语言）与 HTTP 概念；不会 Python 可只看 curl 示例
- 硬件：能运行 Ollama 的电脑（8GB 内存起步；想顺畅跑 7B 量化模型建议 8GB 显存）

### 学完能做什么
- 在 Windows / macOS / Linux（含 Docker）上装好 Ollama，跑起第一个本地大模型
- 熟练用 `ollama pull / run / list / ps / rm` 管理模型，能按显存选量化档位（q4_K_M 等）
- 用 HTTP API 和 OpenAI 兼容接口，通过 Python / curl 调用本地模型，对接自己的小程序
- 用 Modelfile 自定义模型参数、系统提示词，`ollama create` 生成专属模型
- 会排查显存回退、下载慢、端口访问、安全暴露四类常见坑

### 建议学习顺序
- 第 1 → 2 → 3 章是零基础主线，务必按顺序读并跟着敲命令
- 第 4 章可按需跳读：只想用现成客户端看 4.2；想自己写程序调看 4.1-4.2；想定制模型看 4.3；遇到性能 / 并发问题再看 4.4
- 第 5 章建议实操 1-2 天后再读（踩过坑更有体感），也可当作速查表随时回查
- 预估总时间：完整通读 + 跟着实操约 4-6 小时

## 写作注意事项（供 chapter-writer）

- 素材中的模型名（如 `gemma4`、`qwen3:8b`）为官方文档占位符，写作时以 `ollama list` 或模型库实际名为准，并在正文注明
- 环境变量以官方 envconfig 为准（如 `OLLAMA_NUM_GPU` 在新版已移除），写作时注明版本差异
- 核心概念均需 `[!tip] 大白话` 解释 + 类比；类比对照：1.1 应用商店+运行时、1.2 保险箱、1.3/3.4 照片压缩、2.2 集装箱、4.1 本地小服务器、4.2 门禁卡、4.3 定制食谱、5.1 偷偷换人、5.4 临时工牌
- 遵守 Obsidian 规范：表格不嵌套在列表内；正文 YAML frontmatter 中特殊字符正确引用
