# 虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI) - 意图文件

## 基本信息

- **主题**: 虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI)
- **项目标识**: vm-bios-uefi
- **运行标识**: vm-bios-uefi
- **工作流**: learning-note-flow
- **创建时间**: 2026-09-17
- **当前阶段**: 阶段 7（已完成；2026-09-18 发布）
- **输出目标**: obsidian（vault 内 `虚拟机/`；项目内保留副本 `workspace/vm-bios-uefi/output/final_note.md`）
- **Vault 路径**: 当前 Obsidian vault 根目录
- **笔记目录**: `虚拟机/`
- **MOC 路径**: `虚拟机/虚拟机 MOC.md`（已追加「固件与启动」分组索引）
- **发布文件**: `虚拟机/虚拟机固件选择 BIOS 与 UEFI.md`

## 用户原始诉求

> 虚拟机中创建的BIOS和UEFI时不知道用哪个，使用UEFI时总是出问题

补充（阶段 0 澄清）：范围要包含 PVE。

## 学习目标

### 笔记类型
practice + compare 混合：选择决策表 + 双平台实操 + UEFI 排错专章

### 学习深度
入门 → 上手

### 用户基础
有了解。已用 VMware Workstation / VirtualBox / PVE 创建过虚拟机，卡在「固件模式怎么选」与「选 UEFI 后启动/安装报错」。

## 范围界定

| 平台 | 处理方式 |
| --- | --- |
| VMware Workstation | 主线，独立成节（固件模式选择、EFI 相关选项） |
| VirtualBox | 主线，独立成节（EFI 勾选项、启用 EFI 的后果） |
| PVE | 主线，独立成节（SeaBIOS vs OVMF、EFI 磁盘、q35/i440fx 组合） |
| Hyper-V | 仅作简短对照（第 2 代虚拟机 = UEFI + 无 Legacy 支持） |

## 研究计划

### 探索方向
1. 概念层：Legacy BIOS 与 UEFI 的启动链路差异（MBR/GPT、EFI 分区、固件驱动模型）
2. 决策层：什么场景必须选 UEFI（Windows 11、Secure Boot、>2TB 系统盘、GPU 直通），什么场景选 Legacy 更省事
3. 排错层：选 UEFI 后常见的失败模式与逐条排查路径
4. 实操层：三大平台的具体操作步骤与选项含义

### 重点收集
- **核心概念**: Legacy BIOS / UEFI / CSM / Secure Boot / MBR / GPT / EFI 系统分区（ESP）/ SeaBIOS / OVMF / q35 / i440fx
- **实战步骤**: VMware 固件选项、VirtualBox 启用 EFI、PVE 创建虚拟机时 BIOS 选项与 EFI 磁盘
- **常见坑**: GPT/MBR 与固件模式不匹配、缺 EFI 分区、Secure Boot 拦截未签名驱动、OVMF 需额外 EFI 磁盘、UEFI 下旧显卡/直通异常
- **工具链**: 各平台的固件与磁盘配置界面、Windows/Linux 下检测当前固件模式的方法

### 信源偏好
- 官方文档: 是（VMware Docs、VirtualBox Manual、Proxmox VE Wiki）
- 技术博客: 是
- 社区讨论: 是（仅用于收集真实报错现象）
- 学术论文: 否

## 备注

- **待补素材**：用户实际遇到的 UEFI 报错原文/截图。收到后并入排错专章，按真实报错写；未收到前该章按通用原理覆盖。
- 排错章需覆盖用户已有笔记未涉及的角度：现有 [[虚拟机/虚拟机的概念和使用.md]] 讲的是宿主机 BIOS 开 VT-x，[[PVE的学习/00-准备工具/WinPE.md]] 只给了 BIOS/UEFI ↔ MBR/GPT 匹配表，均未讲客户机固件选型。
- 写出后应与 [[虚拟机/虚拟机 MOC.md]] 及 PVE 相关笔记建立双链，不重复其内容。
- 发布位置在阶段 6 前最终确认；未确认前只写入 `workspace/vm-bios-uefi/output/`。
