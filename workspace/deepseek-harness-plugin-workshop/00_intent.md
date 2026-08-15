# DeepSeek-Harness 插件实战教学 - 意图文件

## 基本信息

- **主题**: DeepSeek-Harness 插件实战教学
- **项目标识**: deepseek-harness-plugin-workshop
- **创建时间**: 2026-08-15
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: AI学习
- **笔记目录**: DeepSeek-Harness 教程
- **MOC 路径**: AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md

## 学习目标

### 笔记类型
实战笔记（手把手、可照做的分册）

### 学习深度
完整上手：写插件 + 配置 + schema + 打包发布（dsh 插件全链路）

### 用户基础
有了解：已读过本系列理论分册（插件开发核心 / 配置体系 / 配置实战），源码环境已跑通（`pnpm dsh web --patch`），但尚未独立写出插件

## 研究计划

### 探索方向
1. 一个完整插件从零到跑通的每一步（照做可复现）
2. 工具 DSL（defineTool）与生命周期 apply(ctx) 的实操写法
3. 配置项（Config schema）+ 补丁加载（--patch）验证
4. bundle 打包 + profile 安装发布
5. 实战中的坑（git 安装 build / allowBuilds / 路径引用）

### 重点收集
- **核心概念**: apply(ctx) / 生命周期 / defineTool 工具 DSL / Config schema / 补丁树 / bundle vs profile
- **实战代码**: 完整可运行的插件代码（从最小工具到带配置项），example-plugin 脚手架（repo_status）作为基础
- **常见坑**: git 安装拉源码非构建产物、allowBuilds 放行、name 按包名引用、HMR 热替换行为
- **工具链**: pnpm / dsh CLI（--patch / --dump-config / plugin add）/ Schemastery

### 信源偏好
- 官方文档: 是（dsh 官方「第一个插件 / 插件配置 / 打包并安装插件」）
- 技术博客: 否
- 社区讨论: 否
- 已有系列笔记: 是（插件开发核心 / 配置体系 / 配置实战 / 常见坑与速查）

## 备注

- 本分册是现有系列的新增配套，编号/风格需与系列约定一致（H1=章标题，H2=X.Y 节，[!tip] 大白话 Callout，[!note] 这在 Claude Code 里相当于 桥接视角）。
- 产出后同步更新 README 分册清单与 MOC。
- 重点解决「读完理论仍不会写」的缺口：每步给可复现命令 + 预期输出 + 出错排查。
