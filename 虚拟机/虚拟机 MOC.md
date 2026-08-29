---
type: moc
status: active
created: 2026-07-30
updated: 2026-08-28
tags:
  - moc
  - 虚拟机
  - index
---

# 虚拟机 MOC

> [!summary] 目录概览
> 虚拟化技术的实操指南与原理笔记，涵盖 VMware Workstation 使用、虚拟网络模式等内容。

---

## VMware 实操

- [[虚拟机/VMware Workstation Player 安装 Windows 虚拟机.md]] - 从零开始在 VMware Player 上安装 Windows 10/11 虚拟机的完整教程 #VMware #教程
- [[虚拟机/VMware 获取虚拟机所有权失败.md]] - VMware 虚拟机锁文件报错的解决方法 #VMware #故障排查
- [[虚拟机/VMware 启动出现 No Media 报错.md]] - VMware 虚拟机启动时 "No Media" 错误的排查与解决方法 #VMware #故障排查
- [[虚拟机/VMware NAT 模式静态 IP 网关错误排错.md]] - VMware NAT 模式下静态 IP 网关误配 `.1`（应为 `.2`）导致整机外网断连的排错实战 #VMware #排错

## 虚拟网络原理

- [[虚拟机/虚拟网络模式/00_索引.md]] - 虚拟网络模式系列笔记入口（10 章，从 VLAN 到 CNI） #virtual-networking #index

## 镜像与磁盘格式

- [[iso和img.md]] - 镜像文件格式介绍（ISO / IMG / qcow2 / raw 区别） #镜像 #虚拟机

---

## 学习路径建议

> [!tip] 阅读顺序
> 1. **新手入门**: 先看 [[虚拟机/VMware Workstation Player 安装 Windows 虚拟机.md]]，上手创建第一台虚拟机
> 2. **遇到问题**: 锁文件报错参考 [[虚拟机/VMware 获取虚拟机所有权失败.md]]；启动 "No Media" 参考 [[虚拟机/VMware 启动出现 No Media 报错.md]]
> 3. **深入网络**: 进入 [[虚拟机/虚拟网络模式/00_索引.md]] 系统学习虚拟网络原理
