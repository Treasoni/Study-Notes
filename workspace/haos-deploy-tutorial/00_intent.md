# 部署 HAOS 详细教程 - 意图文件

## 基本信息

- **主题**: 部署 HAOS（Home Assistant Operating System）详细教程：国内源 + 稳定运行
- **项目标识**: haos-deploy-tutorial
- **创建时间**: 2026-08-06
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: homeassistant/haos-deploy/
- **MOC 路径**: homeassistant/Home Assistant MOC.md

## 学习目标

### 笔记类型
实战笔记（practice 实操教程，附选型背景与排障手册）

### 学习深度
精通（含排障 + 长期运维）

### 用户基础
有了解（用户已有 HA 部署选型笔记与 AI 智能家居部署笔记，对 HAOS / Docker / Supervised 选型已熟悉）

## 研究计划

### 探索方向
1. **HAOS 镜像获取与国内加速源**：官方源慢/被墙问题，国内镜像（清华、中科大、国内下载站、群晖/阿里 OSS 加速等）的获取与校验
2. **实体机 + 虚拟机完整安装路线**：U盘/SSD 直装、VMware/PVE/群晖 VM 安装步骤与关键参数
3. **稳定运行保障**：存储介质选型（SSD vs TF 卡）、国内 Docker/Add-on 镜像加速配置、NTP 时间同步、备份策略、升级策略、常见故障排查

### 重点收集
- **核心概念**: HAOS 架构（HA Core + Supervisor + OS + Add-on）、引导方式（UEFI/BIOS）、OS 更新机制
- **实战代码**: Docker daemon.json 国内镜像配置、wget/curl 国内加速下载命令、PVE/VMware 创建 VM 的参数示例
- **常见坑**: 官方源下载慢/失败、TF 卡写入放大损坏、国内网络下 Add-on 商店加载失败、容器镜像拉取超时、时间不同步导致证书/自动化失效
- **工具链**: balenaEtcher / Rufus / Ventoy、PVE、qemu、balena-cli、Home Assistant OS 官方镜像

### 信源偏好
- 官方文档: 是（HAOS 官方安装文档为基线）
- 技术博客: 是（国内部署教程、镜像加速教程）
- 社区讨论: 是（HA 中文社区、官方论坛、少数派/知乎）
- 学术论文: 否

## 备注

- 用户已有 `homeassistant/Home Assistant 三种部署方式对比与选型`（含 HAOS 虚拟机详解与部署实操附录）与 `ai-smart-home-system`（含国内镜像链）。本教程定位为 **HAOS 专项实操教程**，避免重复展开选型对比，聚焦"如何装 + 国内源 + 稳定运行"。
- 发布位置：Obsidian vault `C:\note\Study-Notes`，笔记目录 `homeassistant/haos-deploy/`。
- 完成后同步 MOC：追加索引到 `homeassistant/Home Assistant MOC.md` 的部署指南分组。
