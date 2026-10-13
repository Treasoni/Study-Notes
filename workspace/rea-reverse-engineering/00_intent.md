# REA: Reverse Engineer Anything - 意图文件

## 基本信息

- **主题**: REA: Reverse Engineer Anything（morluto/rea，把逆向工程能力通过 MCP/CLI 接给 AI agent 的工具）
- **项目标识**: rea-reverse-engineering
- **创建时间**: 2026-10-13
- **当前阶段**: 阶段 0
- **输出目标**: project-output（暂存 `workspace/output/final_note.md`；Obsidian 位置待用户指定）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战 + 概念 混合（practice + concept）：先讲清「REA 是什么、解决什么问题」，再给可跟做的实战路径。

### 学习深度
入门 → 上手

### 用户基础
逆向零基础（会基本命令行）

## 研究计划

### 探索方向
1. REA 是什么、解决什么问题（MCP server + CLI，把逆向能力接给 AI agent）
2. 安装与接入（`npx rea-agents setup` 注册 MCP / 全局 CLI 安装 / 更新）
3. 实战主路径（**零原生引擎**：静态 JS/Electron 分析、网站分析等可立即跑通的目标）
4. 进阶概览：原生二进制分析（Hopper / Ghidra / IDA provider 选择与前置条件）
5. 边界与安全（DISCLAIMER、本地分析、授权范围、evidence/limitation 机制）

### 重点收集
- **核心概念**: MCP、agent 协作、逆向工程、静态分析 vs 运行时捕获、evidence 与 limitation
- **实战命令**: `npx rea-agents setup`、`npx -y rea-agents@latest analyze-javascript-application <path> --json`、`rea --help`、`rea update`
- **常见坑**: Node 版本要求（22.x≥22.19 / 24.x≥24.11 / 26+）、Hopper 首次启动弹窗、provider 选择、平台支持差异
- **工具链**: `rea-agents`（npm）、Hopper / Ghidra / IDA、JADX、pwntools、WABT、tshark 等可选依赖

### 信源偏好
- 官方文档: 是（README / `README_zh.md` / `docs/*.md` / rea.tools 指南与案例）
- 技术博客: 否（优先官方来源）
- 社区讨论: 否
- 学术论文: 否

## 备注

- 输出暂定 `workspace/output/final_note.md`，Obsidian 发布位置后续再定。
- 会话中链接的《自建代理节点/VPS 自建节点零基础全流程/03 购买 VPS（三家厂商对照）.md》与本主题关系未确认；按用户④A 选择，**默认不并入**本主题。
- 内容遵循 `note-style.md` 入门优先契约（结论先行 / 比喻先于术语 / 术语首现即解释 / 概念与操作分离）；格式遵循 `note-system.md`（frontmatter、Callout、双链、代码块语言标识）。
- 正文成句英文引文一律给中译，并在章末留「引文对照（原文/中译/出处）」表。
