# 从零开发 Home Assistant 自定义集成（custom integration） - 意图文件

## 基本信息

- **主题**: 从零开发 Home Assistant 自定义集成（custom integration）
- **项目标识**: home-assistant-integration
- **创建时间**: 2026-08-08
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: homeassistant/ha-integration
- **MOC 路径**: homeassistant/Home Assistant MOC.md

## 学习目标

### 笔记类型
实战笔记（practice）：从零写一个可运行、可 HACS 分发的 HA 自定义集成。

### 学习深度
上手：能照着教程写完并跑通一个最小自定义集成，理解核心概念。

### 用户基础
有了解：用过 HA、会基本 Python 与 async/await。

## 研究计划

### 探索方向
1. 开发环境搭建（Dev Container / 本地 venv）
2. 集成基本结构与 manifest.json
3. Config Flow 配置流程
4. Entity 平台与 DataUpdateCoordinator
5. 测试、调试与 HACS 分发（进阶延伸）

### 重点收集
- **核心概念**: manifest.json、config_flow、config entry、Entity 平台、DataUpdateCoordinator、services、async/await
- **实战代码**: 最小集成骨架、官方脚手架、sensor 平台示例
- **常见坑**: asyncio 阻塞、manifest 字段错误、ConfigEntryNotReady、调试日志不生效
- **工具链**: VS Code Dev Container、hassfest、pytest-homeassistant-custom-component、HACS

### 信源偏好
- 官方文档: 是（developers.home-assistant.io）
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 已有 HA 相关笔记避免重叠：ha 命令使用（homeassistant/ha-command）、HAOS 部署（homeassistant/haos-deploy）、部署方式对比、AI 智能家居一键部署（homeassistant/ai-smart-home-system）。
- 本笔记聚焦「开发集成」本身，不重复部署/使用层面的内容。
- 用户偏好：每个核心概念添加 `[!tip] 大白话` 通俗解释 + 打比方类比。
- 深度为「上手」，笔记应以动手走通为主线，控制篇幅，避免过度深入边界场景。
