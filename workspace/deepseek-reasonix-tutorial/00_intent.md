# DeepSeek-Reasonix 配置教程 - 意图文件

## 基本信息

- **主题**: DeepSeek-Reasonix 配置教程
- **项目标识**: deepseek-reasonix-tutorial
- **创建时间**: 2026-08-10
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: `.`（vault 根目录 /Users/zhqznc/Documents/项目）
- **笔记目录**: `AI学习/DeepSeek-Reasonix 教程`
- **MOC 路径**: `AI学习/DeepSeek-Reasonix 教程/DeepSeek-Reasonix MOC.md`

## 学习目标

### 笔记类型
实战配置教程（对齐 `AI学习/Claude Code 教程/` 的结构与风格：分册目录 + MOC + 实用速查 + Callout）

### 学习深度
上手到精通（完整系列，参考 Claude Code 教程的 01-入门 / 02-基础功能 / 03-进阶应用 / 04-高级功能 四级结构）

### 用户基础
熟悉 Claude Code（教程侧重 DeepSeek-Reasonix 与 Claude Code 的对比与迁移，减少通用概念铺垫）

## 研究计划

### 探索方向
1. DeepSeek-Reasonix 是什么：定位、前缀缓存优化原理、与 Claude Code 的关系（esengine/DeepSeek-Reasonix）
2. 安装与入门：npm / Homebrew / npx / 源码构建 / 桌面应用 / VS Code 扩展，`reasonix setup` 首次配置
3. 配置详解：`reasonix.toml`（provider、agent、启用的工具、插件）、API Key、运行模式、多模型协同（执行器 + 规划器）
4. CLI 与会话：`reasonix` / `code` / `chat` / `run` / `doctor` / `update` / `acp`，会话内命令（/init、/effort fast|smart|max）
5. 进阶应用：MCP 配置、插件系统、ACP 协议、缓存优化与成本监控
6. 对比与迁移：与 Claude Code 的命令/交互/概念对齐（PR #6431），成本对比，迁移指南

### 重点收集
- **核心概念**: 前缀缓存（prefix cache）、reasonix.toml 配置模型、运行模式（smart/fast/max）、ACP 协议
- **实战代码**: 安装命令、setup 向导、配置文件示例、CLI 调用示例、MCP 接入示例
- **常见坑**: 国内网络/镜像安装、API Key 配置、缓存命中率问题、与 Claude Code 命令差异
- **工具链**: npm registry、Homebrew、GitHub Releases、VS Code 扩展、npm 包 `reasonix`

### 信源偏好
- 官方文档: 是（esengine/DeepSeek-Reasonix README 及 README.zh-CN）
- 技术博客: 是
- 社区讨论: 是（GitHub PR、CSDN 等）
- 学术论文: 否

## 备注

- 用户已确认：完整系列规模、发布到 Obsidian vault 新建目录、熟悉 Claude Code
- 教程风格对齐 Claude Code 教程：YAML frontmatter（title/tags/created/updated/status/source_project）、Callout（info/tip/warning/note/example）、双链只加高价值概念
- 最终发布时同步 MOC（`AI学习/DeepSeek-Reasonix 教程/DeepSeek-Reasonix MOC.md`），只维护索引不复制正文
