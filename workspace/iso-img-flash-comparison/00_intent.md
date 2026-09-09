# ISO 与 IMG 镜像烧录/写盘方法对比 - 意图文件

## 基本信息

- **主题**: ISO 与 IMG 镜像烧录/写盘方法对比
- **项目标识**: iso-img-flash-comparison
- **运行标识**: iso-img-flash-comparison
- **创建时间**: 2026-09-09
- **当前阶段**: 阶段 0（意图澄清）
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: 虚拟机/
- **MOC 路径**: 待定（可后续补）
- **关联笔记**: [[iso和img.md]]（vault 根目录，讲 ISO vs IMG 本质区别；本篇作为「操作篇」与其互链）

## 学习目标

### 笔记类型
对比 + 实战操作

### 学习深度
中等

### 用户基础
有了解（已理解 ISO=安装介质 / IMG=成品盘；接触过 PVE、物理机刷 iStoreOS/OpenWRT 等场景）

### 要回答的核心问题
1. ISO 与 IMG 用 Etcher / Rufus / dd 写盘时，操作步骤是否一样？
2. 物理机「刻录 U 盘安装」与「整盘写入直接启动」两种流程的本质差异？
3. 虚拟机里 ISO（挂光驱安装）与 IMG（导入磁盘）操作差异？
4. 为什么有些工具对 ISO/IMG 的处理不同？（文件系统 vs 裸镜像、引导模式、分区表）
5. 常见坑有哪些？（.img.gz 解压、选错目标盘、校验、混合 ISO / Ventoy 等）

## 研究计划

### 探索方向
1. 写盘工具（balenaEtcher / Rufus / dd / Ventoy）对 ISO 与 IMG 的操作流程与差异
2. 物理机刷机：ISO 刻录 U 盘启动安装 vs IMG 全盘写入即开即用
3. 虚拟机场景：ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入（含 PVE 流程）
4. 文件结构差异（ISO9660/安装介质 vs 分区表+文件系统的整盘镜像）如何决定烧录方式
5. 常见坑与最佳实践：.img.gz 解压、目标盘选择、镜像校验、UEFI/Secure Boot、Ventoy 直写 IMG 的兼容性

### 重点收集
- **核心概念**: ISO 9660/UDF、原始写盘(raw write) vs 文件拷贝、分区表(GPT/MBR)、引导扇区/UEFI、整盘镜像
- **实战操作**: Rufus 写 ISO/写 IMG 的界面差异、balenaEtcher 流程、`dd`/`pv` 命令、Ventoy、PVE `qm importdisk`
- **常见坑**: 写入目标盘符写错、Windows 下无法直接写 IMG 的盘、img.gz 未解压、刷完不引导（Secure Boot/引导顺序）
- **工具链**: balenaEtcher、Rufus、dd/coreutils、Ventoy、PVE、7-Zip/gzip、校验工具(sha256)

### 信源偏好
- 官方文档: 是（Rufus、balenaEtcher、各发行版/固件官方说明、PVE 文档）
- 技术博客: 是
- 社区讨论: 是（iStoreOS/OpenWRT 论坛等）
- 学术论文: 否

## 备注

- 用户已有 [[iso和img.md]] 打底，避免重复解释 ISO/IMG 定义，聚焦「烧录/写盘」这一操作面。
- 最终发布到 `虚拟机/` 目录；MOC 待定。
- 若后续发现与软路由教程、Ventoy 使用指南目录内容重叠，可在笔记内双向链接复用。
