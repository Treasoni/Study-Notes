# Ventoy 使用实战：多系统启动 U 盘 - 意图文件

## 基本信息

- **主题**: 如何使用 Ventoy（多系统启动U盘）
- **项目标识**: ventoy-usage
- **创建时间**: 2026-09-08
- **当前阶段**: 阶段 0
- **输出目标**: obsidian（Obsidian vault）
- **Vault 路径**: 待指定（发布阶段确认）
- **笔记目录**: 待指定（发布阶段确认）
- **MOC 路径**: 待指定（可选，发布阶段确认）

## 学习目标

### 笔记类型
实战操作指南

### 学习深度
上手会用（能独立安装配置并完成常见任务）

### 用户基础
有动手基础（会用电脑、能下载安装软件、熟悉进 BIOS/UEFI 选启动项）

## 研究计划

### 探索方向
1. Ventoy 是什么：核心概念、分区结构、与 Rufus 等传统烧录工具的差异
2. 安装与制作：Windows / Linux 下安装 Ventoy 到 U 盘、日常增删 ISO 镜像
3. 进阶与排错：Secure Boot、UEFI/Legacy 兼容、启动失败与常见坑

### 重点收集
- **核心概念**: Ventoy 引导原理、双分区结构（引导分区 + 数据分区）、启动菜单、持久化（persistence）
- **实战代码**: 各平台安装步骤、Ventoy2Disk 用法、ISO/WIM/IMG/VHD/EFI 等镜像直拷流程、命令行工具
- **常见坑**: 安装会清空 U 盘数据、个别老机器/Legacy BIOS 兼容问题、Secure Boot 开关、不支持自动安装的镜像特殊处理
- **工具链**: Ventoy2Disk、VentoyPlugson 配置、Ventoy 兼容镜像格式、与 Rufus/balenaEtcher 的对比与取舍

### 信源偏好
- 官方文档: 是（github.com/ventoy/Ventoy）
- 技术博客: 是
- 社区讨论: 是（Ventoy 官方论坛/GitHub Issues）
- 学术论文: 否

## 备注

- 用户原始输入「如何使用ventory」经确认指 **Ventoy（多系统启动 U 盘工具）**。
- 最终笔记发布到 Obsidian vault；发布前需确认 vault 内目录与是否需要 MOC。
