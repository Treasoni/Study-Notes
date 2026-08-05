---
title: "基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建指南）"
type: index
tags:
  - Home-Assistant
  - 架构
  - 部署选型
  - Docker
  - 国内镜像
  - 部署
  - Docker-Compose
  - 一键部署
  - onboarding
  - 跨品牌接入
  - xiaomi_home
  - localtuya
  - midea_ac_lan
  - Matter
  - AI智能体
  - DeepSeek
  - FastAPI
  - 自动化
  - packages
  - Blueprint
  - 产品化
  - 部署分发
  - 时效性
created: 2026-08-05
updated: 2026-08-06
status: 已完成
source_project: ai-smart-home-system
---

# 基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建指南）

> 端到端实战构建指南：从零搭建一套基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统。全文 8 章按「一键部署 → 跨品牌接入 → AI 对话 → 场景自动化」主线组织，每章末尾都有前后导航与下一章衔接。建议按章节顺序阅读。

## 核心结论（先看这个）

> [!summary] 一键速览
> - **部署选型**：HAOS 为主 + Container 为辅（Supervised 已于 2025.12 弃用）
> - **交付形态**：预建 VM 镜像 / 预刷迷你主机 / 定制盒子 → 开机即用；Agent 打包为自定义 Add-on
> - **稳定运行**：Supervisor 全托管（自动更新 + 快照备份 + Add-on 商店），面向完全非技术用户
> - **LLM**：DeepSeek `deepseek-v4-flash`（旧名 `deepseek-chat` 已于 2026-07-24 停用）
> - **跨品牌**：米家 `xiaomi_home` · 涂鸦 `tuya`+`localtuya` · 美的 `midea_ac_lan` · 格力内置 `gree` · 海尔 `hon-revived`；华为无路径；Matter / MQTT / Zigbee 兜底
> - **国内适配**：HAOS-CN 镜像 / 社区加速；Container 走 ghcr 回退链（次级渠道）

## 章节目录

| 章 | 标题 | 内容 |
|----|------|------|
| 1 | [[01_系统架构与部署选型\|第一章 系统架构与部署选型]] | 四层架构 · HAOS 为主 / Container 为辅（Supervised 弃用修正） |
| 2 | [[02_国内镜像链与Docker基础设施\|第二章 镜像与交付：HAOS 镜像 / 国内分发]] | HAOS 镜像 · HAOS-CN 国内分发 · Container ghcr 回退链（次级） |
| 3 | [[03_一键部署install脚本与docker编排\|第三章 一键交付：预建镜像 / 盒子 / Add-on]] | 预建 VM 镜像 / 预刷主机 / 盒子 · Agent Add-on 一键装 · Container compose（次级） |
| 4 | [[04_无头onboarding自动化\|第四章 首次启动：HAOS 引导 / onboarding / Add-on 安装]] | HAOS 首次启动 · onboarding API · 5 分钟承诺边界 |
| 5 | [[05_跨品牌接入矩阵\|第五章 跨品牌接入矩阵（核心章节）]] | 品牌矩阵 · MVP 预置清单 · 首次接入人工步骤 |
| 6 | [[06_AI智能体FastAPI与DeepSeek\|第六章 AI 智能体：FastAPI + DeepSeek Function Calling]] | Agent 代码 · entity_map · 安全设计（可打包为 Add-on） |
| 7 | [[07_场景模板与自动化\|第七章 场景模板与自动化：packages 与 Blueprint]] | 场景三件套 · Blueprint · 组件版本锁定 |
| 8 | [[08_产品化复制与时效性风险\|第八章 产品化复制与时效性风险]] | 预建镜像 / 盒子 / Add-on 仓库 / Blueprint 分发 · 待决策事项 |

## 配套笔记

- [[系统架构图]] - 四层架构总览 + 「把客厅灯调暗」数据流时序图
- [[Home Assistant 三种部署方式对比与选型]] - HAOS / Docker Container / HA Supervised 部署方式对比
- [[Home Assistant MOC]] - Home Assistant 目录

## 如何阅读

- **只看结论**：读上面的「核心结论」即可。
- **想动手搭建**：按 1 → 8 顺序精读，代码示例集中在第 2-4、6 章。
- **重点补课**：跨品牌接入是核心章节（第 5 章），涉及品牌差异与时效性风险。
- **时效性修正**：桌面报告 6 处过时信息的完整回顾在 [[08_产品化复制与时效性风险|第八章 8.3]]。

## 结语

一套「给非技术用户也能 5 分钟用起来」的跨品牌 AI 智能家居系统，真正的壁垒不在代码，而在三件事：**把部署门槛降到一条命令**（第 2-4 章）、**把主流品牌统一到一套系统**（第 5 章）、**把 AI 对话变成真能控制设备的入口**（第 6 章）。这三件事互相支撑，缺一不可。全文 8 章就是围绕它们展开的一条端到端路线图——从选型、部署、接入，到 AI、自动化，最后把整套能力复制给更多用户。

> 需要把本笔记拆成独立章节阅读？每章文件已含前后导航与返回索引；配套架构图见 [[系统架构图]]。
