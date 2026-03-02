---
tags: [linux, ubuntu, 服务器, 系统安装]
created: 2026-03-02
updated: 2026-03-02
---

# Ubuntu Server 安装教程

> [!info] 概述
> **Ubuntu Server** 是 Canonical 公司推出的企业级 Linux 服务器操作系统，无图形界面、轻量高效，适合部署各种网络服务。

## 核心概念

### 是什么
Ubuntu Server 是 Ubuntu 的服务器版本，特点：
- 无图形界面（纯命令行）
- 占用资源少、性能高
- 5年免费安全更新（LTS 版本）
- 稳定可靠、适合生产环境

### 为什么需要
- 搭建 Web 服务器、数据库服务器
- 运行容器化应用（Docker/K8s）
- 文件存储、NAS 系统
- 开发测试环境

### 通俗理解
**🎯 比喻**：Ubuntu Desktop 就像精装修的公寓（有家具、装修），Ubuntu Server 就像毛坯房（只有基础结构，自己按需求装修）。服务器不需要图形界面，就像公寓不需要厨房一样——节省空间、专注功能。

**📦 版本选择**：
- **LTS（长期支持）**：每2年发布一次，支持5年（推荐生产环境）
- **普通版本**：每6个月发布，支持9个月（适合尝鲜）

---

## 系统要求

### 最低配置
| 项目 | 要求 |
|------|------|
| 处理器 | 1 GHz 或更好 |
| 内存 | 1 GB RAM |
| 硬盘空间 | 5 GB 可用空间 |
| 安装介质 | USB 接口或 DVD 驱动器 |

### 推荐配置
| 项目 | 要求 |
|------|------|
| 内存 | 2 GB RAM 或更多 |
| 硬盘 | 20 GB 或更多（取决于服务需求） |
| 网络 | 有线网络连接 |

---

## 安装前准备

### 1. 下载 ISO 镜像

```bash
# 官网下载
https://ubuntu.com/download/server

# 国内镜像源（推荐）
# 清华大学
https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/24.04/
# 中科大
https://mirrors.ustc.edu.cn/ubuntu-releases/24.04/
```

### 2. 制作启动盘

**Windows（使用 Rufus）**：
1. 下载 [Rufus](https://rufus.ie/)
2. 插入 U 盘（8GB 以上）
3. 选择 ISO 和 U 盘，点击开始

**macOS/Linux（使用 dd）**：
```bash
# 查看磁盘列表
diskutil list

# 卸载 U 盘（假设是 /dev/disk2）
diskutil unmountDisk /dev/disk2

# 写入镜像
sudo dd if=ubuntu-server.iso of=/dev/rdisk2 bs=4m status=progress

# 弹出 U 盘
diskutil eject /dev/disk2
```

**使用 BalenaEtcher（跨平台）**：
1. 下载 [BalenaEtcher](https://www.balena.io/etcher/)
2. 选择 ISO → 选择 U 盘 → Flash

---

## 安装流程与初始配置

### 安装界面导航

> [!tip] 操作说明
> - **方向键**：移动光标
> - **空格/回车**：选择/确认
> - **Tab 键**：切换焦点区域
> - **Esc 键**：返回上一级

---

### 第一步：启动安装

```
Try or Install Ubuntu Server
├── Try Ubuntu without installing
└── Install Ubuntu Server ← 选择这个
```

按回车或等待 30 秒自动开始。

---

### 第二步：选择语言

```
Language selection
└── English ← 默认（推荐使用英文）
```

> [!warning] 语言选择提示
> 选择中文可能会导致某些命令输出显示乱码，建议使用英文安装。

---

### 第三步：配置网络连接

```
Network connections
├── enp0s3  ← 网卡名称
└── IPv4/IPv6  ← 显示 IP 地址
```

**配置方式**：
- **DHCP（自动）**：自动获取 IP（默认）
- **Manual（手动）**：静态 IP 配置

**静态 IP 配置**（可选）：
```
IPv4 method: Manual
Subnet: 192.168.1.0/24
Address: 192.168.1.100
Gateway: 192.168.1.1
DNS: 8.8.8.8, 8.8.4.4
```

---

### 第四步：配置代理（可选）

```
Proxy address
└── [Leave empty] ← 如果不需要代理，留空继续
```

---

### 第五步：配置镜像地址

```
Configure Ubuntu archive mirror
└── http://archive.ubuntu.com/ubuntu ← 默认官方源
```

**国内用户推荐选择**：
- 清华源：`https://mirrors.tuna.tsinghua.edu.cn/ubuntu`
- 中科大源：`https://mirrors.ustc.edu.cn/ubuntu`
- 阿里云源：`https://mirrors.aliyun.com/ubuntu`

---

### 第六步：配置存储（重点！）

这是安装过程中最重要的部分，决定了磁盘的分区方式。

#### 存储配置选项

```
Storage configuration
├── Use an entire disk        ← 使用整块磁盘（推荐新手）
├── Custom storage (partitioning)  ← 自定义分区（高级用户）
└── LVM / RAID 配置选项
```

#### 选项 1：自动分区（推荐新手）

```
Use an entire disk
├── 选择磁盘：/dev/sda
├── File system summary
│   ├── /boot    1GB  ext4   ← 引导分区
│   ├── /        剩余  ext4   ← 根分区
│   └── swap     2GB  swap   ← 交换分区
└── Set up this disk as an LVM group ← 使用 LVM（推荐勾选）
```

**LVM（逻辑卷管理）的优势**：
- ✅ 灵活扩展：可以动态调整分区大小
- ✅ 快照备份：支持 LVM 快照
- ✅ 多磁盘管理：可以跨磁盘扩展

#### 选项 2：自定义分区（推荐生产环境）

选择 `Custom storage (partitioning)` 后：

**推荐分区方案**：

| 挂载点 | 大小 | 类型 | 说明 |
|--------|------|------|------|
| `/boot` | 1GB | ext4 | 引导分区，独立存放内核 |
| `/` | 20-50GB | ext4/xfs | 系统根目录 |
| `/var` | 根据需求 | ext4/xfs | 日志、数据库（增长快） |
| `/home` | 剩余空间 | ext4/xfs | 用户数据 |
| `swap` | 内存大小的1-2倍 | swap | 交换分区 |

**创建步骤**：
1. 选择 `Free space` → `Create a new partition`
2. 设置大小和文件系统
3. 选择挂载点
4. `Done` 完成该分区
5. 重复以上步骤创建所有分区
6. `Finish partitioning` 完成分区

> [!tip] 生产环境建议
> - `/var` 单独分区：防止日志占满根分区
> - `/home` 单独分区：重装系统时保留用户数据
> - 使用 LVM：方便后期调整分区大小

---

### 第七步：配置用户账户

```
Profile setup
├── Your name: Server Admin
├── Your server's name: ubuntu-server
├── Pick a username: admin  ← 你的用户名
├── Choose a password: ********
└── Confirm your password: ********
```

> [!warning] 重要提示
> Ubuntu 默认禁用 root 账户，创建的用户通过 `sudo` 获得管理员权限。

---

### 第八步：SSH 配置（重点！）

```
SSH Setup
├── Install OpenSSH server: Yes ← 必须勾选！
├── Allow password authentication: Yes
└── Import SSH identity: No（可稍后配置）
```

**为什么要安装 OpenSSH Server？**
- ✅ 远程管理服务器（无图形界面必需）
- ✅ 文件传输（SCP/SFTP）
- ✅ 安全加密连接

---

### 第九步：选择附加软件

```
Featured Server Snaps
├── Ubuntu Pro: Expand package security... ← 可选
└── 其他 snaps
```

通常不需要选择，安装完成后可以手动安装。

---

### 第十步：安装完成

```
Installation complete
└── Reboot now ← 重启进入新系统
```

移除安装介质，按回车重启。

---

## 首次登录与基础配置

### 登录系统

```bash
# 本地登录
用户名: admin
密码: ********

# 或通过 SSH 远程登录
ssh admin@192.168.1.100
```

### 基础配置命令

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 查看系统信息
lsb_release -a        # 查看 Ubuntu 版本
uname -r              # 查看内核版本
ip a                  # 查看 IP 地址

# 配置时区
sudo timedatectl set-timezone Asia/Shanghai

# 同步时间
sudo apt install -y ntp
```

---

## 常见安装场景配置

### 场景 1：LVM 分区方案

```bash
# 查看 LVM 信息
sudo pvdisplay         # 物理卷
sudo vgdisplay         # 卷组
sudo lvdisplay         # 逻辑卷

# 扩展根分区（如果需要）
sudo lvextend -L +10G /dev/ubuntu-vg/ubuntu-lv
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

### 场景 2：软件 RAID 配置

在安装时选择 `Custom storage`：
1. 选择多个磁盘
2. 配置 RAID 级别（RAID 0/1/5/10）
3. 创建分区

### 场景 3：静态 IP 配置

使用 Netplan 配置网络：

```bash
# 编辑网络配置文件
sudo nano /etc/netplan/00-installer-config.yaml
```

配置示例：
```yaml
network:
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
  version: 2
```

应用配置：
```bash
sudo netplan apply
```

---

## 最佳实践

### 安装阶段

| 建议 | 说明 |
|------|------|
| 使用 LTS 版本 | 稳定、支持周期长 |
| 勾选 LVM | 方便后期扩展 |
| 勾选 OpenSSH Server | 必需！远程管理依赖 |
| `/var` 单独分区 | 防止日志占满根分区 |

### 安全建议

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 配置防火墙
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 禁用 root 远程登录（默认已禁用）
# 确认 PermitRootLogin no
sudo grep "PermitRootLogin" /etc/ssh/sshd_config
```

---

## 常见问题

### Q1: 安装后无法远程连接？

```bash
# 检查 IP 地址
ip a

# 检查 SSH 服务状态
sudo systemctl status ssh

# 如果未安装 OpenSSH，手动安装
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Q2: 如何重置用户密码？

```bash
# 重启进入恢复模式
# 然后执行：
passwd username
```

### Q3: 如何切换到 root 用户？

```bash
# 不推荐直接登录 root，使用 sudo 代替
sudo <命令>

# 需要 root shell 时
sudo -i
# 或
sudo su -
```

### Q4: 分区方案选择？

| 使用场景 | 推荐方案 |
|----------|----------|
| 个人学习/测试 | 自动分区（LVM） |
| 生产服务器 | 自定义分区（/var 独立） |
| 虚拟机 | 自动分区即可 |
| 数据库服务器 | 自定义（/data 独立） |

---

## 个人笔记
> [!personal] 💡 我的理解与感悟
> 记录 Ubuntu Server 安装中的个人经验和踩坑记录

---

## 相关文档
- [[Linux换源]] - 国内镜像源配置
- [[linux的LVM管理]] - LVM 逻辑卷管理
- [[linux磁盘相关的知识]] - 磁盘和分区深入理解
- [[linux如何修改网络信息]] - Netplan 网络配置详解

## 参考资料
- [Ubuntu 官方下载](https://ubuntu.com/download/server)
- [Ubuntu 官方文档](https://help.ubuntu.com/)
- [Ubuntu Server 安装教程](https://ubuntu.com/server/docs)

---

**最后更新**：2026-03-02
