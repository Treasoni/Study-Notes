# Ollama 使用文档 - 意图文件

## 基本信息

- **主题**: Ollama 使用文档
- **项目标识**: ollama-usage
- **创建时间**: 2026-08-10
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes（待 P6 最终确认）
- **笔记目录**: AI学习/03-技术专题（待用户确认）
- **MOC 路径**: AI学习/00-索引/AI学习 MOC.md（待用户确认）

## 学习目标

### 笔记类型
概念 + 实战混合：兼顾 Ollama 定位/原理的通俗讲解与可照做的上手步骤

### 学习深度
入门到上手：安装 → 常用命令 → 模型管理 → 基础配置

### 用户基础
零基础：假设读者没用过 Ollama、不熟悉本地 LLM

## 研究计划

### 探索方向
1. **Ollama 是什么 & 为什么用** — 定位、本地 LLM 优势、与云端 API 对比
2. **安装与快速开始** — Windows/macOS/Linux、Docker 安装、首次运行
3. **模型管理与常用命令** — `ollama pull/run/list/rm`、模型库、切换模型
4. **进阶用法** — Modelfile、运行参数、HTTP/OpenAI 兼容 API、环境变量
5. **常见坑与最佳实践** — 显存不足、下载慢/镜像源、端口占用、安全与隐私

### 重点收集
- **核心概念**: Ollama 定位、模型仓库与量化（GGUF）、本地推理与 GPU、Ollama API、Modelfile
- **实战代码**: 安装命令、`ollama` CLI 常用命令、curl / Python 调用 API 示例
- **常见坑**: 显存不足、模型下载慢与镜像、端口占用、OpenAI 兼容使用方式
- **工具链**: Ollama、Ollama API、OpenAI SDK、Docker、本地模型生态（模型库）

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 零基础读者：核心概念补充 `[!tip] 大白话` 通俗解释 + 类比（门禁卡 / 临时工牌 / 保险箱 等）
- 输出到 Obsidian vault，注意 YAML frontmatter 中特殊字符需正确引用
- 表格不嵌套在列表内，避免 Obsidian 渲染失败
