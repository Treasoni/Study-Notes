---
tags: [pve]
---

# PVE 创建 Windows 虚拟机教程

> [!info] 概述
> 在 PVE 中创建 Windows 虚拟机需要安装 VirtIO 驱动以获得最佳性能，否则网络和磁盘性能会大幅下降。
> 类比：就像给虚拟机安装"专用驱动程序"，让虚拟硬件能够被 Windows 识别和高效使用。

## 核心概念 💡
- **VirtIO 驱动**：半虚拟化驱动，提供接近物理机的性能
- **不用 VirtIO**：Windows 也能用，但性能差、CPU 占用高
- **使用 VirtIO**：获得直通级性能、IOPS 高、延迟小

## VirtIO 驱动说明

| 状态 | 性能 | CPU 占用 | 驱动 |
|------|------|----------|------|
| 不用 VirtIO | 差 | 高 | Windows 通用驱动 |
| 使用 VirtIO | 直通级 | 低 | VirtIO 专用驱动 |

> [!tip] 下载地址
> https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers

## 操作步骤

### 1. 准备工作

#### 1.1 下载 Windows ISO

- Windows 10/11 官方 ISO
- 或其他 Windows 版本

#### 1.2 下载 VirtIO 驱动

访问：https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers

下载最新版本的 VirtIO 驱动 ISO。

#### 1.3 上传到 PVE

1. 打开 PVE Web 界面
2. 选择 `Datacenter → Storage → local → ISO Images`
3. 上传 Windows ISO 和 VirtIO 驱动 ISO

### 2. 创建 Windows 虚拟机

详细步骤参考 [[如何创建PVE虚拟机]]，以下是针对 Windows 的重点配置：

#### 2.1 基本配置

| 配置项 | 值 |
|--------|-----|
| 操作系统 | Windows 11/10 |
| ISO 文件 | 选择上传的 Windows ISO |

#### 2.2 系统配置

| 配置项 | 值 |
|--------|-----|
| BIOS | **OVMF (UEFI)** |
| 机型 | **q35** |
| SCSI Controller | **VirtIO SCSI single** |
| EFI Disk | ✅ 勾选 |
| Storage | local-lvm |

#### 2.3 硬盘配置

| 配置项 | 值 |
|--------|-----|
| 磁盘大小 | 根据需求（建议 60GB+） |
| Storage | local-lvm |

#### 2.4 CPU 配置

| 配置项 | 值 |
|--------|-----|
| 核心 | 2+ |
| 类型 | **host** |

#### 2.5 内存配置

| 配置项 | 值 |
|--------|-----|
| 最小内存 | 4GB+ |

#### 2.6 网络配置

| 配置项 | 值 |
|--------|-----|
| 型号 | **VirtIO (paravirtualized)** |
| 网桥 | vmbr0 |

### 3. 添加 VirtIO 驱动 ISO

1. 创建完虚拟机后
2. 选择虚拟机 → Hardware → CD/DVD
3. 添加 VirtIO 驱动 ISO

### 4. 安装 Windows

1. 启动虚拟机
2. 进入 Windows 安装界面
3. 到"选择安装位置"时：
   - **看不到硬盘**（正常，因为缺少 VirtIO 驱动）
4. 点击 `加载驱动程序`
5. 浏览到 VirtIO 驱动 ISO
6. 选择对应驱动：
   - **磁盘驱动**：`viostor\w11\amd64`
   - **网络驱动**：`NetKVM\w11\amd64`
7. 安装驱动后，硬盘应该可见

### 5. 配置网络

#### 5.1 安装网络驱动

1. Windows 安装完成后
2. 打开设备管理器
3. 会看到带黄色感叹号的网络适配器
4. 右键 → 更新驱动
5. 浏览到 VirtIO 驱动 ISO
6. 选择 `NetKVM\w11\amd64`
7. 安装驱动

#### 5.2 配置网络

1. 打开网络设置
2. 配置 IP 地址（静态或 DHCP）
3. 测试网络连接

## VirtIO 驱动结构

```
virtio-win.iso
├── viostor/          # 磁盘驱动
│   ├── w10/
│   │   └── amd64/
│   └── w11/
│       └── amd64/
├── NetKVM/           # 网络驱动
│   ├── w10/
│   │   └── amd64/
│   └── w11/
│       └── amd64/
├── Balloon/          # 内存气球驱动
├── qemupciserial/     # 串口驱动
├── qxldod/           # 显示驱动
└── viorng/           # RNG 驱动
```

## 注意事项 ⚠️

1. **UEFI 必须有 EFI Disk**
   - Windows 11 要求 UEFI
   - 没有 EFI Disk 无法启动

2. **Windows 版本匹配**
   - Windows 10 用 `w10` 驱动
   - Windows 11 用 `w11` 驱动

3. **Secure Boot**
   - 建议关闭
   - 可能导致驱动签名问题

4. **VirtIO SCSI vs VirtIO Block**
   - VirtIO SCSI 性能更好
   - 推荐使用 VirtIO SCSI

5. **CPU 类型**
   - 使用 `host` 模式
   - 性能最优

## 常见问题 ❓

**Q: 为什么看不到硬盘？**
A: 因为缺少 VirtIO 磁盘驱动，需要加载驱动程序。

**Q: 为什么网络不可用？**
A: 需要安装 VirtIO 网络驱动（NetKVM）。

**Q: VirtIO 驱动安装失败？**
A: 检查 Windows 版本和驱动版本是否匹配，尝试关闭 Secure Boot。

**Q: 必须用 VirtIO 吗？**
A: 不是必须，但强烈推荐。不用的性能会差很多。

**Q: 可以用 E1000 网卡吗？**
A: 可以，E1000 是模拟网卡，不需要驱动，但性能差很多。

**Q: Windows 11 安装有什么要求？**
A: 需要 UEFI、Secure Boot（可关闭）、TPM 2.0（可绕过）。

**Q: 如何绕过 Windows 11 TPM 检查？**
A: 创建 VM 时机型选 i440fx，或修改注册表绕过检查。

## 相关文档

[[如何创建PVE虚拟机]] | [[PVE的网络逻辑讲解]] | [[PVE存储库]] | [[PVE直通]] | [[安装和使用PVE]] | [[PVE学习笔记MOC]]
