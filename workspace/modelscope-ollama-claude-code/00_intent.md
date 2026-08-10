# 使用 ModelScope 拉取模型 + Ollama 部署 + Claude Code 使用 - 意图文件

## 基本信息

- **主题**: 使用 ModelScope 拉取模型并用 Ollama 部署接入 Claude Code
- **项目标识**: modelscope-ollama-claude-code
- **创建时间**: 2026-08-10
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:/note/Study-Notes
- **笔记目录**: AI学习/03-技术专题/
- **MOC 路径**: AI学习/00-索引/AI学习 MOC.md

## 学习目标

### 笔记类型

实战步骤指南

### 学习深度

入门上手

### 用户基础

零基础可跟做（面向能复制命令跑通全流程的读者）

## 研究计划

### 探索方向

1. **ModelScope 拉取模型**：魔搭社区是什么、如何用网页/CLI/Python SDK 搜索与下载模型（含国内源、镜像、断点续传）
2. **Ollama 本地部署**：Ollama 安装（Windows/macOS/Linux）、`ollama pull/create/run`、Modelfile、GGUF 格式与量化基础
3. **Claude Code 接入本地模型**：Ollama 的 OpenAI 兼容 API、Claude Code 环境变量配置（`ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_MODEL`），以及可选方案（claude-code-router / LiteLLM / 代理）

### 重点收集

- **核心概念**: ModelScope（魔搭）、GGUF 格式、量化（Q4_K_M 等）、Ollama 运行架构、Modelfile、OpenAI 兼容 API、Claude Code 模型接入机制
- **实战代码**: ModelScope CLI 下载命令、Python `snapshot_download`、`ollama create` 创建模型、Claude Code 启动与切换模型的配置示例
- **常见坑**: 模型下载慢/失败（网络与国内源）、模型格式不兼容（需转 GGUF）、显存/内存不足、Claude Code 对接口协议兼容性问题、Ollama 服务未启动/端口占用
- **工具链**: ModelScope（魔搭社区）、Ollama、Claude Code、可选（ollama-model 转换脚本、claude-code-router、LiteLLM、WSL）

### 信源偏好

- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户选择「入门上手 + 实战步骤指南」，笔记应以可复制的命令和验证步骤为主线，避免过多原理深挖。
- 每章为核心概念保留 `[!tip] 大白话` 通俗解释 + 类比。
- 完成后直接发布到 Obsidian vault `AI学习/03-技术专题/`，并同步 MOC（`AI学习/00-索引/AI学习 MOC.md`）。
- 表格不可嵌套在列表项内，Obsidian 无法渲染列表内的表格。
