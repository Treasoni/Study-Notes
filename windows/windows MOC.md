---
title: Windows 学习笔记 MOC
created: 2026-09-11
updated: 2026-09-11
tags: [windows, moc, 索引]
---

# Windows 学习笔记 MOC

> [!info] 概述
> 本 MOC 整理 Windows 系统底层知识的学习笔记，目前涵盖**文件系统 / 注册表 / PowerShell** 三大主题及其串联用法。全部内容以 Microsoft Learn 官方文档为一手来源，零基础入门向，每条命令都标注「环境 / 版本 / 权限」，官方未写明的一律写作"官方未说明"而不做推断。

---

## 📚 快速导航

### 核心笔记

| 笔记 | 说明 |
| --- | --- |
| [[Windows 文件系统、注册表与 PowerShell]] | 零基础入门长文：文件系统 / 注册表 / PowerShell 各自成章，再加一章串联实操与一章速查。含 58 个代码块 / 约 190 条命令，以及完整的注册表备份回滚流程 |

### 按章节定位

| 章节 | 内容 |
| --- | --- |
| [[Windows 文件系统、注册表与 PowerShell#第零章 导读：文件系统、注册表、PowerShell 是什么关系]] | 三者的层次关系：存储层 / 配置层 / 操作层 |
| [[Windows 文件系统、注册表与 PowerShell#第一章 Windows 文件系统——数据到底放在哪]] | 卷 / 目录 / 文件、路径规则与坑区、系统目录地图、NTFS 四特色、链接三兄弟、`icacls` 权限、`robocopy` |
| [[Windows 文件系统、注册表与 PowerShell#第二章 Windows 注册表——系统和程序的配置中心]] | 五个根键、Hive 与磁盘文件、值类型、WOW6432Node、**备份与回滚主线**、`reg` 命令、开机自启键 |
| [[Windows 文件系统、注册表与 PowerShell#第三章 Windows PowerShell——用命令操作前两者]] | 对象管道与参数绑定、Verb-Noun 与自举命令、`Get-Help`、Provider 与 PSDrive、执行策略、编码三条通道、5.1 与 7 差异 |
| [[Windows 文件系统、注册表与 PowerShell#第四章 串联——用 PowerShell 同时操作文件系统与注册表]] | 文件系统与注册表命令清单、三种执行方式选型、端到端「备份 → 改值 → 复核 → 回滚」示例 |
| [[Windows 文件系统、注册表与 PowerShell#第五章 总结与速查]] | 三张命令速查表、九个跨方向易错点、"官方未说明"与留白清单 |

---

## 🎯 最常回来查的三件事

| 想做什么 | 直接看 |
| --- | --- |
| 改注册表前先备份 | [[Windows 文件系统、注册表与 PowerShell#2.7 备份与回滚（本章强制主线）]] |
| 开机自启项在哪 | [[Windows 文件系统、注册表与 PowerShell#2.9.1 开机自启一共四个键]] |
| 脚本跑不起来（禁止运行脚本） | [[Windows 文件系统、注册表与 PowerShell#3.6 执行策略：它防的是手滑，不是防坏人]] |

---

## 📝 待补充

- [ ] Windows 服务与任务计划程序
- [ ] Windows 事件日志与故障排查
- [ ] 用户账户、权限与 UAC 机制
