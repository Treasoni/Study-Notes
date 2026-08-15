# DeepSeek-Harness 从零写插件 - 意图文件

## 基本信息

- **主题**: DeepSeek-Harness 从零写插件（空目录手写全文件）
- **项目标识**: deepseek-harness-plugin-from-scratch
- **创建时间**: 2026-08-15
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: AI学习
- **笔记目录**: DeepSeek-Harness 教程
- **MOC 路径**: AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md

## 学习目标

### 笔记类型
实战教学分册（learning-note / outline 模式）

### 学习深度
上手（完整走通「写 → 配 → 验证 → 打包 → 安装」，从空目录起步）

### 用户基础
有了解（已读系列理论：插件开发核心 / 配置体系 / 配置实战；源码环境已跑通；读过《插件实战》但感觉仍依赖脚手架）

## 研究计划

### 探索方向
1. 空目录起步：一个 dsh 插件工程最少需要哪几个文件，各自作用
2. 每个文件怎么写：package.json / tsconfig / src/index.ts / 工具文件 / 两份 patch
3. 与「改造脚手架」路线的差异点（用户选择：不用 example-plugin，全部手写）

### 重点收集
- **核心概念**: apply(ctx) / export const name / inject=['tools'] / Config schema / defineTool / patch（dev 绝对路径 vs bundle 包名）/ bundle vs profile
- **实战代码**: 从空目录手写的最小可跑插件全文件清单 + 每文件逐行解释
- **常见坑**: tsconfig 编译目标、package.json name 与 patch id 与 defineTool name 四名分离、pnpm allowBuilds、git 安装 #sha 固定
- **工具链**: pnpm / esbuild 或 tsc 构建、dsh web --patch / --dump-config / headless / dsh plugin add

### 信源偏好
- 官方文档: 是（deepseek-harness 官方 docs）
- 技术博客: 是（按需）
- 社区讨论: 否
- 学术论文: 否

## 与既有分册的分工

- 第 3 章《插件开发核心》: 讲机制原理 → 本篇聚焦「从零动手把文件建起来」
- 第 4 章《与ClaudeCode对照迁移》: 从零写 repo_status、逐步对照 Claude Code → 本篇不同：空目录起步 + 手写全部工程文件 + 明确不碰脚手架
- 《插件实战》(04·实战): 基于 example-plugin 脚手架改造 → 本篇是「不依赖脚手架」的姊妹篇，形成【改造 vs 从零】双路线

## 备注

- 用户原话：「我还是不会写 deepseek 插件」「写一个新的，从零开始」
- 期望结果：一篇能照着在空目录里一步步建出插件并跑通打包的新分册，发布到 AI学习/DeepSeek-Harness 教程/
- 示范工具沿用 git_log（与《插件实战》一致），保证系列内可对照
