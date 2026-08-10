# ModelScope 模型文件类型 - 意图文件

## 基本信息

- **主题**: ModelScope 模型文件类型（非 GGUF 文件怎么用、其他文件的作用）
- **项目标识**: modelscope-model-file-types
- **创建时间**: 2026-08-10
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: AI学习/03-技术专题/
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
概念笔记

### 学习深度
概念入门

### 用户基础
有了解（已会用 modelscope CLI/SDK 下载 GGUF 并配合 Ollama 部署，见 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南.md]]）

## 研究计划

### 探索方向
1. ModelScope 模型仓库的文件结构全景（一个模型仓库里通常有哪些文件）
2. 常见模型文件格式逐个讲清：`.safetensors`、`.bin`/`.pytorch_model.bin`、`.gguf`、`.onnx` 等，各自是什么、谁在用
3. 权重文件之外的"其他文件"作用：`config.json`、`tokenizer.json`/`tokenizer_config.json`、`generation_config.json`、`model.safetensors.index.json`、`README.md`、示例代码等
4. 拿到非 GGUF 文件后怎么用：用 Transformers 直接加载、转 GGUF 再喂给 Ollama/llama.cpp、用 vLLM/API 平台等路径的取舍
5. 与既有部署指南的衔接：什么时候该下 GGUF、什么时候该下原始权重

### 重点收集
- **核心概念**: safetensors、bin/pytorch_model、gguf、onnx、config.json、tokenizer、generation_config、sharded checkpoint、量化
- **实战代码**: 各格式的最小加载示例（transformers.from_pretrained、llama.cpp 转换、GGUF 目录结构识别）
- **常见坑**: 下错格式、缺配置文件导致加载失败、sharded 文件漏下、tokenizer 与模型不匹配
- **工具链**: ModelScope、Transformers、Ollama、llama.cpp、vLLM、LM Studio

### 信源偏好
- 官方文档: 是（ModelScope 文档、HuggingFace 文档）
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 备注

- 概念入门深度，聚焦"搞清楚每个文件是干嘛的 + 非 GGUF 怎么用"，不做量化原理深挖
- 与既有 [[AI学习/03-技术专题/ModelScope-Ollama-ClaudeCode部署指南.md]] 互补：那篇讲 GGUF+Ollama 实战，这篇补上文件类型认知空白
- 用户偏好：核心概念加 `[!tip] 大白话` 通俗解释 + 打比方类比
