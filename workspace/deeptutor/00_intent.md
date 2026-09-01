# HKUDS DeepTutor - 意图文件

## 基本信息

- **主题**: HKUDS DeepTutor
- **项目标识**: deeptutor
- **创建时间**: 2026-09-01
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: GitHub项目
- **MOC 路径**: GitHub项目/GitHub项目 MOC.md

## 学习目标

### 笔记类型
实战 + 概念（使用为主，兼顾原理理解）

### 学习深度
上手

### 用户基础
有基本了解（知道 Docker、LLM 概念，部署过简单项目，不熟 Agent/RAG）

## 研究计划

### 探索方向
1. DeepTutor 是什么、能做什么（功能全景、适用场景）
2. 快速上手：Docker 部署 + 基础使用（上传教材、问答、生成习题、可视化）
3. 核心原理：Agent-Native 多智能体架构、RAG 混合检索、记忆系统
4. 进阶玩法：TutorBots、深研（Deep Research）、Living Book、考试模拟

### 重点收集
- **核心概念**: 智能体（Agent）、多智能体协作、RAG、个性化学习档案（Learner Profile）、TutorBot、知识中心（Knowledge Center）、三层持久记忆
- **实战代码**: Docker 部署命令、docker-compose 配置、环境变量、模型接入（OpenAI/DeepSeek/Ollama 等）、Web UI 使用流程
- **常见坑**: 模型 API 密钥配置、显存/内存要求、检索索引构建（LlamaIndex/FAISS/LightRAG/GraphRAG）、多用户隔离与权限
- **工具链**: Docker、FastAPI、React/Next.js、LlamaIndex/FAISS、LightRAG、GraphRAG

### 信源偏好
- 官方文档: 是（GitHub README、deeptutor.info）
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 是（DeepTutor 论文 / arXiv）

## 备注

- 最终笔记输出到 Obsidian vault `GitHub项目/` 目录，并加入 `GitHub项目 MOC` 索引。
- 用户基础为"有基本了解"，教程需覆盖必要的 Docker/LLM 前置概念，但不从零讲起。
- 笔记目标：让用户能独立部署并上手使用 DeepTutor，同时理解其多智能体与 RAG 的核心原理。

## 执行决策（P2 确认）

- **执行模式**：大纲模式（结构化逐章写作）
- **部署方式**：尚未部署 → 笔记以上手教程形式覆盖 Docker 路径（ghcr.io/hkuds/deeptutor 单容器），并附排错
- **LLM 接入**：云端 API 为主（OpenAI / DeepSeek / Anthropic 等），本地 Ollama 作为可选补充
- 素材就绪：`01_explore_result.md`（P1）、`02_deep_research.md`（P2，含 claim→源映射 [S1]–[S6]）
