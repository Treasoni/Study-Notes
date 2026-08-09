---
title: "从零开发 Home Assistant 自定义集成"
tags:
  - HomeAssistant
  - 集成开发
  - 学习笔记
  - MOC
created: 2026-08-08
updated: 2026-08-08
status: 完成
source_project: home-assistant-integration
---

# 从零开发 Home Assistant 自定义集成（custom integration）

> [!summary] 本指南
> 面向会 Python + async/await、用过 HA 的读者，从零开发一个**可运行、可 HACS 分发**的 Home Assistant 自定义集成。主线终点：一个带 config flow + sensor + DataUpdateCoordinator + HACS 分发的最小集成。

## 📚 目录

| 章节 | 内容 | 篇幅 |
|------|------|------|
| [[01_认识HomeAssistant自定义集成\|第 1 章：认识自定义集成]] | 概念 + 生态位置 + 学习路径总览 | 短 |
| [[02_开发环境搭建\|第 2 章：开发环境搭建]] | Dev Container + 本地 venv + 官方脚手架 | 中 |
| [[03_集成骨架与manifest\|第 3 章：集成骨架与 manifest.json]] | 目录结构 + manifest 核心字段 | 中 |
| [[04_ConfigFlow配置流程\|第 4 章：Config Flow 配置流程]] | 表单流程 + 唯一性 + 异常语义 | 长 |
| [[05_Entity平台与Sensor实体\|第 5 章：Entity 平台与 Sensor 实体]] | 实体状态机 + 声明式 SensorEntityDescription | 中 |
| [[06_DataUpdateCoordinator数据轮询\|第 6 章：DataUpdateCoordinator 数据轮询]] | 统一轮询 + 异常映射 + 独立 API 库封装 | 长 |
| [[07_测试与调试\|第 7 章：测试与调试]] | pytest-homeassistant-custom-component + debugpy + logger | 中 |
| [[08_HACS分发\|第 8 章：HACS 分发]] | hacs.json + hassfest/hacs Action + Release | 短 |
| [[09_常见坑与最佳实践\|第 9 章：常见坑与最佳实践]] | 10 坑 + 7 实践，排错手册收尾 | 中 |

> [!tip] 建议阅读顺序
> 按第 1 → 9 章顺序阅读；**第 4、6 章是重点**，值得放慢速度。

## 🎯 学完能做什么

- 用 Dev Container 一键搭好开发环境，F5 断点调试
- 读懂并手写合法的 `manifest.json`
- 用官方脚手架生成骨架 + 实现 config flow 配置流程
- 用 DataUpdateCoordinator 轮询外部 API，暴露 sensor 实体
- 用 pytest 写测试，用 debugpy/logger 定位问题
- 走通 HACS 分发，让集成可被一键安装

---
> [[01_认识HomeAssistant自定义集成|开始第 1 章 ➡️]]
