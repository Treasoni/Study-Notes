# Home Assistant 部署方式对比 - 意图文件

## 基本信息

- **主题**: Home Assistant 中 HAOS 虚拟机、Docker Container、HA Supervised 这些部署方式的区别与选择
- **项目标识**: home-assistant-deployment-methods
- **创建时间**: 2026-08-05
- **当前阶段**: 阶段 0
- **输出目标**: Obsidian vault
- **Vault 路径**: `C:\note\Study-Notes`
- **笔记目录**: `homeassistant/`
- **MOC 路径**: `homeassistant/Home Assistant MOC.md`

## 学习目标

### 笔记类型
对比笔记 + 实战指南（practice + compare 混合）

### 学习深度
精通（系统掌握各部署方式差异，支持选型决策）

### 用户基础
熟悉（已用过或了解 Home Assistant，想系统对比部署方式）

## 研究计划

### 探索方向
1. HAOS 虚拟机（HAOS VM）：官方推荐的全功能部署，含 Supervisor、Add-on、OTA 更新
2. Docker Container：仅运行 Home Assistant Core 容器，轻量、无 Supervisor，无官方 Add-on
3. HA Supervised：在完整 Linux 系统上安装 Supervisor + Core，接近 HAOS 但依赖宿主环境
4. 三者对比与迁移：资源占用、维护成本、易用性、插件/Add-on 生态、适用场景、相互迁移路径

### 重点收集
- **核心概念**: Home Assistant Core、Supervisor、Operating System (HAOS)、Add-on、Docker、虚拟机/容器差异
- **实战代码**: 三种部署方式的安装命令（Docker compose、Supervised 安装脚本、HAOS 虚拟机镜像部署）
- **常见坑**: Supervised 对宿主系统的严格检测（OS 兼容性检查）、Docker 部署缺少 Add-on 与 OTA 更新、权限/设备直通（USB、Zigbee 硬件）差异
- **工具链**: Docker CLI/compose、Proxmox/VMware/ESXi 虚拟机平台、Home Assistant 安装镜像（qcow2/vmdk/ova）

### 信源偏好
- 官方文档: 是（home-assistant.io 安装与部署章节、Supervised 要求）
- 技术博客: 是
- 社区讨论: 是（Home Assistant 社区论坛、Reddit）
- 学术论文: 否

## 备注

- 用户已确认发布到 Obsidian vault：`homeassistant/` 目录（当前为空，可用）
- MOC 需要新建：`homeassistant/Home Assistant MOC.md`
- 笔记类型采用对比 + 实战混合：每个部署方式提供步骤指南，并给出对比表
- 注意 Obsidian 规则：表格不要嵌套在列表项内；表格独立段落展示
