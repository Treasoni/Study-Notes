# git安装配置教程 - 意图文件

## 基本信息

- **主题**: git安装配置教程
- **项目标识**: git安装配置教程
- **创建时间**: 2026-07-31
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes（当前 vault）
- **笔记目录**: `Git/`
- **MOC 路径**: `Git/Git MOC.md`

## 学习目标

### 笔记类型
实战笔记

### 学习深度
入门（实用）——安装 + 基础配置 + 常用命令，能立刻跑起来

### 用户基础
有了解（知道 add/commit 基本概念，未系统安装配置过）

## 研究计划

### 探索方向
1. Windows 平台安装：Git for Windows 安装包、Git Bash、环境变量 PATH、换行符与编码差异
2. macOS 平台安装：官方 pkg / Homebrew / Xcode Command Line Tools、终端集成（zsh/Bash）
3. 基础配置与安全：user.name / user.email、core.editor、SSH 密钥、credential helper、常用 alias、全局 .gitignore

### 重点收集
- **核心概念**: Git 配置层级（system/global/local）、PATH 与终端集成、SSH vs HTTPS 认证、换行符与中文编码
- **实战代码**: 各平台安装命令、`git config` 命令族、SSH key 生成与添加、alias 与全局配置片段
- **常见坑**: Windows 下 `git 不是内部命令`（PATH 未配置）、`autocrlf` 换行符问题、`core.quotepath` 中文乱码、凭据重复输入
- **工具链**: Git for Windows、Homebrew、GitHub CLI、GUI 工具（VSCode / Sourcetree）可选

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 已有 Git 笔记体系：`Git 入门教程.md` 第 2 章已覆盖配置层级，本笔记聚焦**平台化安装步骤 + 基础配置闭环**，与之互补、避免重复。
- 目标平台：Windows + macOS（双平台）。
- 发布到当前 vault 的 `Git/` 目录，最终加入 `Git/Git MOC.md`。
